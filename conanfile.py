from conans import ConanFile, CMake, tools
import os
from conans.tools import untargz
import os.path


class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.10.1"
    license = "<Put the package license here>"
    url = "https://www.hdfgroup.org/downloads/hdf5/source-code/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        archive_file = "hdf5-1.10.1.tar.bz2"
        untargz(archive_file,"hdf5")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("hdf5/CMakeLists.txt", "PROJECT(HDF5 C CXX)", 
        '''PROJECT(HDF5 C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake_defs = {}
        
        if self.options.shared:
            cmake_defs["BUILD_SHARED_LIBS"] = "ON"
        
        cmake_defs["HDF5_BUILD_EXAMPLES"] = "OFF"
        cmake_defs["HDF5_BUILD_TOOLS"]="OFF"
        cmake_defs["HDF5_BUILD_HL_LIB"]="OFF"
        cmake_defs["HDF5_BUILD_CPP_LIB"]="OFF"
        cmake.configure(src_dir = self.conanfile_directory,
                        defs = cmake_defs,
                        build_dir = os.path.join(self.conanfile_directory,"build"))

        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hdf5"]