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

if(WIN32)
    set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} /Od")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /MP")
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
	add_definitions(-D_SCL_SECURE_NO_WARNINGS)
	add_definitions(-D_UNICODE)
	add_definitions(-DUNICODE)
endif()

#set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../godot")

message("SOURCE_DIR=${SOURCE_DIR}")

add_executable(SbNext)

# --------------------- Platform -----------------------

# Not using CONFIGURE_DEPENDS as we assume files will not be added or removed very often.
# When they are we need to trigger a cmake by hand.
set(PLATFORM_DIR "${SOURCE_DIR}/platform")

set(MACOS_PLATFORM_DIR "${PLATFORM_DIR}/macos")
set(WIN_PLATFORM_DIR "${PLATFORM_DIR}/windows")
if (APPLE)
    file(GLOB_RECURSE MACOS_MM_SOURCES "${MACOS_PLATFORM_DIR}/*.mm")
    file(GLOB_RECURSE MACOS_CXX_SOURCES "${MACOS_PLATFORM_DIR}/*.cpp")
    file(GLOB_RECURSE MACOS_HEADERS "${MACOS_PLATFORM_DIR}/*.h")

    list(APPEND PLATFORM_FILES "${MACOS_MM_SOURCES}" "${MACOS_CXX_SOURCES}" "${MACOS_HEADERS}")
elseif(WIN32)
    file(GLOB_RECURSE WIN_CXX_SOURCES "${WIN_PLATFORM_DIR}/*.cpp")
    file(GLOB_RECURSE WIN_HEADERS "${WIN_PLATFORM_DIR}/*.h")

    list(APPEND PLATFORM_FILES "${WIN_CXX_SOURCES}" "${WIN_HEADERS}")
else()
    message("unix not yet supported")
endif()

source_group(TREE "${PLATFORM_DIR}" PREFIX "platform" FILES ${PLATFORM_FILES})
list(APPEND APP_SOURCES "${PLATFORM_FILES}")

# --------------------- Core ---------------------------

set(CORE_DIR "${SOURCE_DIR}/core")
file(GLOB_RECURSE CORE_HEADERS "${CORE_DIR}/*.h")
file(GLOB_RECURSE CORE_CXX "${CORE_DIR}/*.cpp")
list(APPEND CORE_FILES "${CORE_CXX}" "${CORE_HEADERS}")
list(APPEND APP_SOURCES "${CORE_FILES}")
source_group(TREE "${CORE_DIR}" PREFIX "core" FILES ${CORE_FILES})


target_sources(SbNext PRIVATE ${APP_SOURCES})
#target_link_libraries(SbNext ${APP_LIBS})
target_include_directories(SbNext PRIVATE "${SOURCE_DIR}")


