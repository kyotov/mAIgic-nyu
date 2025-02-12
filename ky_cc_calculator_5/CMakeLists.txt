add_library(ky_calculator_5
    calculator5.cc
)
target_include_directories(ky_calculator_5
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
