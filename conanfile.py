from conans import ConanFile, CMake, tools
from os import path

class QtandroidcmakeConan(ConanFile):
    name = "QtAndroidCMake"
    version = "0.1"
    license = "Android NDK"
    author = "Bittner Ede ede.bittner@nng.com"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Wraps the https://github.com/OlivierLDff/QtAndroidCMake package"
    topics = ("cmake", "qt", "android")
    settings = "os"
    exports_sources = "patch/patch0.patch"

    def build(self):
        git = tools.Git(folder="QtAndroidCMake")
        git.clone("https://github.com/OlivierLDff/QtAndroidCMake.git", "master")
        git.checkout("9ad26790ecb8350dbee1885a0130b83c036e7509")

        src_path = path.join(self.build_folder, "patch", "patch0.patch")
        dst_path = path.join(self.build_folder, "QtAndroidCMake")
        tools.patch(patch_file=src_path, base_path=dst_path)

    def package(self):
        self.copy("*.cmake", dst=path.join("lib", "cmake"))
        self.copy("*.in", dst=path.join("lib", "cmake"))
        pass

    def package_info(self):
        self.env_info.CMAKE_MODULE_PATH.append(path.join(self.package_folder, "lib", "cmake", "QtAndroidCMake", ""))
