add_library(ky_calculator_3
    calculator3.cc
)
target_include_directories(ky_calculator_3
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
