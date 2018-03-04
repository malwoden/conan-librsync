from conans import ConanFile, CMake, tools


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

    def source(self):
        tools.get("https://github.com/librsync/librsync/archive/v%s.tar.gz" % self.version)

    def build(self):
        rsync_src_path = "%s/librsync-%s" % (self.source_folder, self.version)
        install_path = "%s/buildinstall" % self.build_folder
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = install_path
        cmake.configure(source_folder=rsync_src_path)
        cmake.build()
        cmake.install()

    def package(self):
        install_path = "%s/buildinstall" % self.build_folder

        self.copy("librsync.h", dst="include", src=install_path + "/include")
        self.copy("*.lib", dst="lib", src=install_path+"/lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("librsync.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
