cmake_minimum_required(VERSION 3.29)
project(ky_modules CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_FIND_FRAMEWORK NEVER)
set(CMAKE_PREFIX_PATH "/Users/kamen/maigic/.venv/lib/python3.12/site-packages")

set(Python_ROOT_DIR /Users/kamen/maigic/.venv)
set(Python_FIND_VIRTUALENV ONLY)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(nanobind CONFIG REQUIRED)

add_subdirectory(ky_cc_calculator)
add_subdirectory(ky_cc_test)