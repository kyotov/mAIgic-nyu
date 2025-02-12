cmake_minimum_required(VERSION 3.29)
project(ky_modules CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_FIND_FRAMEWORK NEVER)
set(CMAKE_PREFIX_PATH "${CMAKE_SOURCE_DIR}/.venv/lib/python3.12/site-packages")

set(Python_ROOT_DIR "${CMAKE_SOURCE_DIR}/.venv")
set(Python_FIND_VIRTUALENV ONLY)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(nanobind CONFIG REQUIRED)

add_subdirectory(ky_cc_calculator)
add_subdirectory(ky_cc_calculator_2)
add_subdirectory(ky_cc_calculator_3)
add_subdirectory(ky_cc_calculator_4)
add_subdirectory(ky_cc_calculator_5)
add_subdirectory(ky_cc_test)