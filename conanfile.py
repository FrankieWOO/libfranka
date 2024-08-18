import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class libfrankaRecipe(ConanFile):
    name = "libfranka"
    version = "0.9.2"
    author = "Fan Wu"
    license = "Apache License v2.0"
    url = "https://github.com/FrankieWOO/libfranka/tree/0.9.2"
    description = "Conan recipe for libfranka"
    topics = ("Franka Robot", "Robot Control")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "common/*", "test/*", "examples/*", "cmake/*"
    tool_requires = "cmake/[>=3.22]"

    def requirements(self):
        self.requires("poco/1.13.3")
        self.requires("eigen/3.4.0")


    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={ "BUILD_TESTS":"OFF", "CMAKE_BUILD_TYPE":"Release" })
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["franka"]
        self.cpp_info.set_property("cmake_file_name", "Franka")
        self.cpp_info.set_property("cmake_target_name", "Franka::Franka")
        self.cpp_info.set_property("pkg_config_name", "Franka")
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
