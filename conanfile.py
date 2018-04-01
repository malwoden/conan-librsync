from conans import ConanFile, CMake, tools
import os

class LibrsyncConan(ConanFile):
    name = "librsync"
    version = "2.0.2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Rsync here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    source_subfolder = "source_subfolder"
    exports_sources = "rsync_exports.def"

    def source(self):
        tools.get("https://github.com/librsync/librsync/archive/v%s.tar.gz" % self.version)
        os.rename("librsync-%s" % self.version, self.source_subfolder)

    def build(self):
        install_path = "%s/buildinstall" % self.build_folder
        cmake = CMake(self)

        if self.settings.compiler != "Visual Studio":
            cmake.definitions["CMAKE_C_FLAGS"] = "-m32" if self.settings.arch == "x86" else "-m64"

        if not self.options.shared:
            with tools.chdir(self.source_subfolder):
                tools.replace_in_file("CMakeLists.txt", "rsync SHARED", "rsync STATIC")

        if self.settings.compiler == "Visual Studio" and self.options.shared:
            with tools.chdir(self.source_subfolder):
                tools.replace_in_file("CMakeLists.txt", "src/whole.c", "src/whole.c %s/rsync_exports.def" % self.source_folder)

        cmake.definitions["CMAKE_INSTALL_PREFIX"] = install_path
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build(target="rsync")
        cmake.install()

    def package(self):
        install_path = "%s/buildinstall" % self.build_folder

        self.copy("librsync.h", dst="include", src=install_path + "/include")
        self.copy("*.lib", dst="lib", src=install_path + "/lib", keep_path=False)
        self.copy("*.dll", dst="bin", src=install_path + "/lib", keep_path=False)
        self.copy("librsync.so*", dst="lib", src=install_path + "/lib", keep_path=False)
        self.copy("*.dylib", dst="lib", src=install_path + "/lib", keep_path=False)
        self.copy("*.a", dst="lib", src=install_path + "/lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
