@echo off
mkdir build_vs2022
pushd build_vs2022
"C:\Program Files\CMake\bin\cmake" -G "Visual Studio 17 2022" -A x64 -DVCPKG_TARGET_TRIPLET=x64-windows -DCMAKE_TOOLCHAIN_FILE="C:\dev\vcpkg\scripts\buildsystems\vcpkg.cmake" ..
popd
