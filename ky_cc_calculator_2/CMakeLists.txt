add_library(ky_calculator_2_api STATIC
    calculator2.cc
    registrar.cc
)
target_include_directories(ky_calculator_2_api
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

add_library(ky_calculator_2_impl STATIC
    calculator2impl.cc
)
target_include_directories(ky_calculator_2_impl
    # this is not great to overlap with the previous one!
    INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include" 
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include" 
)
target_link_libraries(ky_calculator_2_impl
    PRIVATE ky_calculator_2_api
)
