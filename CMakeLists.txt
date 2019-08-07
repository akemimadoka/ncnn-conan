cmake_minimum_required(VERSION 3.10)
project(CMakeWrapper)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
else()
    include(conanbuildinfo.cmake)
endif()
conan_basic_setup()

add_subdirectory("ncnn")
