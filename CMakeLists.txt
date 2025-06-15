cmake_minimum_required(VERSION 3.15...3.29)
project(PySTE LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(DIM_FIXED_SIZES RANGE CACHE STRING "The which fixed size methods to compile. Can take the values: 'RANGE', 'SINGLE', 'POWER',  'OFF'.")
set(NCTRL_FIXED_SIZES RANGE CACHE STRING "The which fixed size methods to compile. Can take the values: 'RANGE', 'SINGLE', 'POWER', 'OFF'.")

# Default values are large enough for upto 4 qubits each with 2 single-qubit
#   controls and each pair (all-to-all connectivity) with a single two-qubit
#   control
set(MAX_NCTRL 14 CACHE STRING "The maximum number of controls to compile fixed size methods for.")
set(MAX_DIM 16 CACHE STRING "The maximum vector space dimension to compile fixed size methods for.")

# Default values give a single qubit with one control for prototypical examples
#   such as Rabi Oscillations
set(NCTRL 1 CACHE STRING "The maximum number of controls to compile fixed size methods for.")
set(DIM 2 CACHE STRING "The maximum vector space dimension to compile fixed size methods for.")

# Default values are large enough for upto 4 qubits each with 2 single-qubit
#   controls
set(NCTRL_BASE 2 CACHE STRING "The base used to generate fixed size methods with n_ctrl=base^n.")
set(DIM_BASE 2 CACHE STRING "The base used to generate fixed size methods with dim=base^n.")
set(MAX_POWER_NCTRL 3 CACHE STRING "The maxinum power n used to generate fixed size methods with n_ctrl=base^n.")
set(MAX_POWER_DIM 4 CACHE STRING "The maxinum power n used to generate fixed size methods with dim=base^n.")

# As camke only supports non-negative integers but we need -1 we represent each
#   integer with the integer that is one larger.
if(${NCTRL_FIXED_SIZES} STREQUAL  POWER)
    set(MAX_NCTRL ${MAX_POWER_NCTRL})
    set(NCTRL_IS_POWER 1)
else()
    set(NCTRL_IS_POWER 0)
    if(${NCTRL_FIXED_SIZES} STREQUAL OFF)
        set(NCTRL_FIXED_SIZES SINGLE)
        set(NCTRL 0)
    elseif(${NCTRL_FIXED_SIZES} STREQUAL SINGLE)
        math(EXPR NCTRL "${NCTRL}+1" OUTPUT_FORMAT DECIMAL)
    else()
        math(EXPR MAX_NCTRL "${MAX_NCTRL}+1" OUTPUT_FORMAT DECIMAL)
    endif()
endif()
if(${DIM_FIXED_SIZES} STREQUAL POWER)
    set(MAX_DIM ${MAX_POWER_DIM})
    set(DIM_IS_POWER 1)
else()
    set(DIM_IS_POWER 0)
    if(${DIM_FIXED_SIZES} STREQUAL OFF)
        set(DIM_FIXED_SIZES SINGLE)
        set(DIM 0)
    elseif(${DIM_FIXED_SIZES} STREQUAL SINGLE)
        math(EXPR DIM "${DIM}+1" OUTPUT_FORMAT DECIMAL)
    else()
        math(EXPR MAX_DIM "${MAX_DIM}+1" OUTPUT_FORMAT DECIMAL)
    endif()
endif()

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP)
find_package(Eigen3 3.3 NO_MODULE)
if (NOT TARGET Eigen3::Eigen)
    message("Eigen3 not found. Installing Eigen3 from submodule:")
    execute_process(COMMAND cmake -S dependencies/eigen -B dependencies/eigen/build
                    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    execute_process(COMMAND cmake --build dependencies/eigen/build --target install
                    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    find_package(Eigen3 3.3 REQUIRED NO_MODULE)
endif()
add_subdirectory(dependencies/Suzuki-Trotter-Evolver)
add_subdirectory(dependencies/eigen)

macro(configure)
    # Set variables for configuration
    set(INIT_DEFS "void init_evolver_${NCTRL}_${DIM}(py::module_ &m, py::class_<ste::UnitaryEvolver<-1, -1, ste::DMatrix<-1, -1>>> &dense_parent, py::class_<ste::UnitaryEvolver<-1, -1, SMatrix>> &sparse_parent);\n@INIT_DEFS@")
    set(INIT_CALLS "init_evolver_${NCTRL}_${DIM}(m, dense_parent, sparse_parent);\t\n@INIT_CALLS@")
    # Update counters
    math(EXPR EVOLVERS_HPP_COUNTER "${EVOLVERS_HPP_COUNTER}+1" OUTPUT_FORMAT HEXADECIMAL)
    math(EXPR EVOLVERS_CPP_COUNTER "${EVOLVERS_CPP_COUNTER}+1" OUTPUT_FORMAT HEXADECIMAL)
    # Configure files into new files with updated counters in name
    configure_file(${EVOLVERS_HPP} ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_HPP_COUNTER}.hpp.in @ONLY)
    configure_file(${EVOLVERS_CPP} ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_CPP_COUNTER}.cpp.in @ONLY)
    configure_file(src/pyste/cpp_bindings/single_evolver.cpp.in src/pyste/cpp_bindings/single_evolver_${NCTRL}_${DIM}.cpp @ONLY)
    # Update current file paths to the latest configured
    set(EVOLVERS_HPP ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_HPP_COUNTER}.hpp.in)
    set(EVOLVERS_CPP ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_CPP_COUNTER}.cpp.in)
    # Adding files that have finished configuring to the source
    set(PYBIND_SRC ${PYBIND_SRC}
        ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/single_evolver_${NCTRL}_${DIM}.cpp
    )
    math(EXPR NCTRL_VALUE "${NCTRL}-1" OUTPUT_FORMAT DECIMAL)
    math(EXPR DIM_VALUE "${DIM}-1" OUTPUT_FORMAT DECIMAL)
    message(STATUS "Added fixed size evolver with n_ctrl=${NCTRL_VALUE} and dim=${DIM_VALUE}.")
endmacro()

macro(dim_flow)
    if(${DIM_FIXED_SIZES} STREQUAL SINGLE)
        configure()
        if(NOT (${DIM} EQUAL 0))
            set(DIM_STORE ${DIM})
            set(DIM 0)
            configure()
            set(DIM ${DIM_STORE})
        endif(NOT (${DIM} EQUAL 0))
    else()
        foreach(DIM RANGE ${MAX_DIM})
            configure()
        endforeach()
    endif()
endmacro()

# Initialise counters
math(EXPR EVOLVERS_HPP_COUNTER "0" OUTPUT_FORMAT HEXADECIMAL)
math(EXPR EVOLVERS_CPP_COUNTER "0" OUTPUT_FORMAT HEXADECIMAL)
# Initialise configuration file paths
set(EVOLVERS_HPP ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_HPP_COUNTER}.hpp.in)
set(EVOLVERS_CPP ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers${EVOLVERS_CPP_COUNTER}.cpp.in)
# Copy files into binary dir
configure_file(src/pyste/cpp_bindings/evolvers.hpp.in ${EVOLVERS_HPP} COPYONLY)
configure_file(src/pyste/cpp_bindings/evolvers.cpp.in ${EVOLVERS_CPP} COPYONLY)
if(${NCTRL_FIXED_SIZES} STREQUAL SINGLE)
    dim_flow()
    if(NOT (${NCTRL} EQUAL 0))
        set(NCTRL_STORE ${NCTRL})
        set(NCTRL 0)
        dim_flow()
        set(NCTRL ${NCTRL_STORE})
    endif()
else()
    foreach(NCTRL RANGE ${MAX_NCTRL})
        dim_flow()
    endforeach()
endif()

# Clear variables to end recursive configuration
set(INIT_DEFS "")
set(INIT_CALLS "")
# Final configureation
configure_file(${EVOLVERS_HPP} src/pyste/cpp_bindings/evolvers.hpp @ONLY)
configure_file(${EVOLVERS_CPP} src/pyste/cpp_bindings/evolvers.cpp @ONLY)
# Copy files into binary dir
configure_file(src/pyste/cpp_bindings/single_evolver.hpp src/pyste/cpp_bindings/single_evolver.hpp COPYONLY)
configure_file(src/pyste/cpp_bindings/get_name.cpp src/pyste/cpp_bindings/get_name.cpp COPYONLY)
# Add files to source
set(PYBIND_SRC ${PYBIND_SRC}
    ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/evolvers.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/single_evolver.hpp
    ${CMAKE_CURRENT_BINARY_DIR}/src/pyste/cpp_bindings/get_name.cpp
)

pybind11_add_module(evolvers ${PYBIND_SRC})

target_link_libraries(evolvers INTERFACE Eigen3::Eigen)
target_link_libraries(evolvers PUBLIC  Suzuki-Trotter-Evolver)
install(TARGETS evolvers DESTINATION ./pyste)