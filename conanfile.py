from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from os import path

class QtandroidcmakeConan(ConanFile):
    name = "QtAndroidCMake"
    version = "0.1"
    license = "Android NDK"
    author = "Bittner Ede Ede.BITTNER@nng.com"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Wraps the https://github.com/OlivierLDff/QtAndroidCMake package"
    topics = ("cmake", "qt", "android")
    settings = {"os"}
    exports_sources = "patch/patch0.patch"

    def configure(self):
        if self.settings.os != "Android":
            raise ConanInvalidConfiguration("This package is needed only for Android Qt builds")

    def build(self):
        git = tools.Git(folder="QtAndroidCMake")
        git.clone("https://github.com/OlivierLDff/QtAndroidCMake.git", "master")
        git.checkout("9ad26790ecb8350dbee1885a0130b83c036e7509")

        src_path = path.join(self.build_folder, "patch", "patch0.patch")
        dst_path = path.join(self.build_folder, "QtAndroidCMake")
        tools.patch(patch_file=src_path, base_path=dst_path)

    def package(self):
        self.copy("*.cmake", dst=".", keep_path=False)
        self.copy("*.in", dst=".", keep_path=False)
        pass

    def package_info(self):
        self.env_info.CMAKE_MODULE_PATH.append(self.package_folder)
