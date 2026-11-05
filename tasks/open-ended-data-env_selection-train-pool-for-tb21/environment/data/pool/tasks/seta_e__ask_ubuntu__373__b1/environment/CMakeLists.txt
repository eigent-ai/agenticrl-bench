cmake_minimum_required(VERSION 3.16)
project(libsamplecmake VERSION 1.0 LANGUAGES C)

include(GNUInstallDirs)
set(CMAKE_INSTALL_LIBDIR "lib")
include(CMakePackageConfigHelpers)

# Build the shared library
add_library(samplecmake SHARED samplecmake.c)
target_include_directories(samplecmake PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
set_target_properties(samplecmake PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER samplecmake.h
)

# Build the binary tool
add_executable(samplecmake-tool samplecmake-tool.c)
target_link_libraries(samplecmake-tool PRIVATE samplecmake)

# Install library and binary
install(TARGETS samplecmake samplecmake-tool
    EXPORT SampleCMakeTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Install CMake package config files
install(EXPORT SampleCMakeTargets
    FILE SampleCMakeTargets.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/SampleCMake
)

configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/SampleCMakeConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/SampleCMakeConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/SampleCMake
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/SampleCMakeConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/SampleCMakeConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/SampleCMakeConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/SampleCMake
)

# Generate and install pkg-config file
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/libsamplecmake.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/libsamplecmake.pc
    @ONLY
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/libsamplecmake.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig
)

# Install config file
set(SYSCONF_INSTALL_DIR "/etc" CACHE PATH "System configuration directory")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/samplecmake.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/samplecmake.conf
    @ONLY
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/samplecmake.conf
    DESTINATION ${SYSCONF_INSTALL_DIR}
)

# Install documentation
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/README
    DESTINATION ${CMAKE_INSTALL_DOCDIR}
)
