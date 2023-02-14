cmake_minimum_required(VERSION 3.20)

project(SbNext)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Set a default build type if none was specified
set(default_build_type "Debug")
 
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -D_DEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-DTOOLS_ENABLED)
add_definitions(-DDEBUG_ENABLED)

if(WIN32)
    set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} /Od")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /MP")
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
	add_definitions(-D_SCL_SECURE_NO_WARNINGS)
    add_definitions(-DNOMINMAX)
    add_definitions(-DTYPED_METHOD_BIND)

    add_definitions(-DWINDOWS_ENABLED)
    add_definitions(-DWASAPI_ENABLED)
endif()

if (APPLE)
    add_definitions(-DUNIX_ENABLED)
    add_definitions(-DMACOS_ENABLED)
endif()

#set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/..")
set(SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../godot")

message("SOURCE_DIR=${SOURCE_DIR}")

add_executable(SbNext)

set(PYTHON_CMD "python3")

# --------------------- Platform -----------------------

# Not using CONFIGURE_DEPENDS as we assume files will not be added or removed very often.
# When they are we need to trigger a cmake by hand.
set(PLATFORM_ROOT_DIR "${SOURCE_DIR}/platform")

if (APPLE)
    set(PLATFORM_DIR "${PLATFORM_ROOT_DIR}/macos")
    file(GLOB_RECURSE MACOS_MM_SOURCES "${PLATFORM_DIR}/*.mm")
    file(GLOB_RECURSE MACOS_CXX_SOURCES "${PLATFORM_DIR}/*.cpp")
    file(GLOB_RECURSE MACOS_HEADERS "${PLATFORM_DIR}/*.h")
    list(APPEND PLATFORM_FILES "${MACOS_MM_SOURCES}" "${MACOS_CXX_SOURCES}" "${MACOS_HEADERS}")
elseif(WIN32)
    set(PLATFORM_DIR "${PLATFORM_ROOT_DIR}/windows")
    file(GLOB_RECURSE WIN_CXX_SOURCES "${PLATFORM_DIR}/*.cpp")
    file(GLOB_RECURSE WIN_HEADERS "${PLATFORM_DIR}/*.h")

    list(APPEND PLATFORM_FILES "${WIN_CXX_SOURCES}" "${WIN_HEADERS}")
else()
    message("unix not yet supported")
endif()

source_group(TREE "${PLATFORM_ROOT_DIR}" PREFIX "platform" FILES ${PLATFORM_FILES})
list(APPEND APP_SOURCES "${PLATFORM_FILES}")

# --------------------- Core ---------------------------

set(CORE_DIR "${SOURCE_DIR}/core")
file(GLOB_RECURSE CORE_HEADERS "${CORE_DIR}/*.h")
file(GLOB_RECURSE CORE_CXX "${CORE_DIR}/*.cpp")
list(APPEND CORE_FILES "${CORE_CXX}" "${CORE_HEADERS}")
list(APPEND APP_SOURCES "${CORE_FILES}")
source_group(TREE "${CORE_DIR}" PREFIX "core" FILES ${CORE_FILES})

# ----------------------- core/disabled_classes.gen.h ---------------

set(GENFILE_DIR "${CMAKE_BINARY_DIR}/genfiles")

file(MAKE_DIRECTORY "${GENFILE_DIR}/core")
file(WRITE "${GENFILE_DIR}/core/disabled_classes.gen.h" "/* THIS FILE IS GENERATED DO NOT EDIT */\n")

file(MAKE_DIRECTORY "${GENFILE_DIR}/modules")
file(WRITE "${GENFILE_DIR}/modules/modules_enabled.gen.h" "/* THIS FILE IS GENERATED DO NOT EDIT */\n")

# ---------------------- generate core headers ---------------------------

file(MAKE_DIRECTORY "${GENFILE_DIR}/core")
execute_process(WORKING_DIRECTORY ${ROOT_DIR} COMMAND "${PYTHON_CMD}" "make_core_headers.py" "${SOURCE_DIR}" "${GENFILE_DIR}")

execute_process(WORKING_DIRECTORY ${ROOT_DIR} COMMAND "${PYTHON_CMD}" "make_version_headers.py" "${SOURCE_DIR}" "${GENFILE_DIR}")

# ---------------------- make_virtuals ---------------------------

file(MAKE_DIRECTORY "${GENFILE_DIR}/core/object")
execute_process(WORKING_DIRECTORY ${ROOT_DIR} COMMAND "${PYTHON_CMD}" "run_make_virtuals.py" "${GENFILE_DIR}/core/object/gdvirtual.gen.inc")

# ---------------------- make_wrappers ---------------------------

file(MAKE_DIRECTORY "${GENFILE_DIR}/core/extension")
execute_process(WORKING_DIRECTORY ${ROOT_DIR} COMMAND "${PYTHON_CMD}" "run_make_wrappers.py" "${SOURCE_DIR}" "${GENFILE_DIR}")

# ---------------------- make_platforms ---------------------------

file(MAKE_DIRECTORY "${GENFILE_DIR}/platform/windows")
file(MAKE_DIRECTORY "${GENFILE_DIR}/platform/macos")
execute_process(WORKING_DIRECTORY ${ROOT_DIR} COMMAND "${PYTHON_CMD}" "make_platforms.py" "${SOURCE_DIR}" "${GENFILE_DIR}")

# --------------------- Third Party ---------------------------

set(THIRDPARTY_DIR "${SOURCE_DIR}/thirdparty")

# --------- mbedtls ------

set(MBEDTLS_DIR "${THIRDPARTY_DIR}/mbedtls")
file(GLOB_RECURSE MBEDTLS_HEADERS "${MBEDTLS_DIR}/*.h")
file(GLOB_RECURSE MBEDTLS_CXX "${MBEDTLS_DIR}/*.cpp")
list(APPEND MBEDTLS_FILES "${MBEDTLS_CXX}" "${MBEDTLS_HEADERS}")

list(APPEND APP_SOURCES "${MBEDTLS_FILES}")
target_include_directories(SbNext PRIVATE "${MBEDTLS_DIR}/include")
source_group(TREE "${MBEDTLS_DIR}" PREFIX "mbedtls" FILES ${MBEDTLS_FILES})

# ----------------------

target_sources(SbNext PRIVATE ${APP_SOURCES})
#target_link_libraries(SbNext ${APP_LIBS})
target_include_directories(SbNext PRIVATE ${SOURCE_DIR})
target_include_directories(SbNext PRIVATE ${PLATFORM_DIR})
target_include_directories(SbNext PRIVATE ${GENFILE_DIR})


