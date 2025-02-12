add_library(ky_calculator_4
    calculator4.cc
)
target_include_directories(ky_calculator_4
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
