from conans import ConanFile, CMake, tools
import shutil
import os

CMakeOptions = [("NCNN_OPENMP", True), ("NCNN_STDIO", True), ("NCNN_STRING", True), ("NCNN_INSTALL_SDK", True),
                ("NCNN_OPENCV", False), ("NCNN_BENCHMARK",
                                         False), ("NCNN_PIXEL", True), ("NCNN_PIXEL_ROTATE", False),
                ("NCNN_CMAKE_VERBOSE", False), ("NCNN_VULKAN", False), ("NCNN_REQUANT", False), ("NCNN_AVX2", False),
                ("NCNN_BUILD_TOOLS", False)]

class NcnnConan(ConanFile):
    name = "ncnn"
    version = "latest"
    license = "BSD-3-Clause"
    author = "Tencent"
    url = "https://github.com/Tencent/ncnn"
    description = "ncnn is a high-performance neural network inference framework optimized for the mobile platform"
    topics = ("C++", "machine learning")
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False], "NCNN_DISABLE_RTTI": [True, False, "Default"],
               "NCNN_DISABLE_EXCEPTION": [True, False, "Default"]}
    options.update({CMakeOption[0]: [True, False]
                    for CMakeOption in CMakeOptions})

    default_options = [
        "shared=False", "NCNN_DISABLE_RTTI=Default", "NCNN_DISABLE_EXCEPTION=Default"]
    default_options.extend(
        ["{}={}".format(CMakeOption[0], CMakeOption[1]) for CMakeOption in CMakeOptions])
    default_options = tuple(default_options)

    generators = "cmake"

    exports_sources = ["CMakeLists.txt"]

    _source_dir = "ncnn"

    def source(self):
        git = tools.Git(folder=self._source_dir)
        git.clone("https://github.com/Tencent/ncnn.git", "master")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"

        if self.options.NCNN_VULKAN:
            raise RuntimeError("Sorry, vulkan not supported for now.")

        disableRtti = self.options.NCNN_DISABLE_RTTI
        if disableRtti != "Default":
            cmake.definitions["NCNN_DISABLE_RTTI"] = disableRtti

        disableException = self.options.NCNN_DISABLE_EXCEPTION
        if disableException != "Default":
            cmake.definitions["NCNN_DISABLE_EXCEPTION"] = disableException

        for CMakeOption in CMakeOptions:
            cmake.definitions[CMakeOption[0]] = getattr(
                self.options, CMakeOption[0])
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

        # These steps are needed because headers of ncnn is installed in child folder...
        shutil.move(self.package_folder + "/include/ncnn",
                    self.package_folder + "/include_tmp")
        os.rmdir(self.package_folder + "/include")
        shutil.move(self.package_folder + "/include_tmp",
                    self.package_folder + "/include")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
