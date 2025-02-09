add_library(ky_calculator STATIC
    calculator.cc
)
target_include_directories(ky_calculator PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

nanobind_add_module(_calculator
    py_calculator.cc
)
target_link_libraries(_calculator PRIVATE
    ky_calculator
)