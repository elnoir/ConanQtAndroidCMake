from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from os import path


class QtandroidcmakeConan(ConanFile):
    name = "QtAndroidCMake"
    version = "1.0.2"
    license = "Android NDK"
    author = "Bittner Ede bittner.ede@gmail.com"
    url = "https://github.com/elnoir/ConanQtAndroidCMake.git"
    description = "Wraps the https://github.com/OlivierLDff/QtAndroidCMake package"
    topics = ("cmake", "qt", "android")
    settings = {"os"}
    exports_sources = "patch/patch0.patch"
    requires = 'android-sdk/26.1.1@tereius/stable'
    options = {
        "use_patch": [True, False],
        "use_version_tag": ["v1.1.0", "v1.1.1", "v19.0.0"]
    }
    default_options = {
        "use_patch": False,
        "use_version_tag": "v19.0.0"
    }

    def package_info(self):
        android_sdk_root = self.deps_env_info['android-sdk'].ANDROID_SDK_ROOT
        self.env_info.ANDROID_SDK = android_sdk_root
        self.env_info.ANDROID_HOME = android_sdk_root

    def configure(self):
        if self.settings.os != "Android":
            raise ConanInvalidConfiguration("This package is needed only for Android Qt builds")

    def build(self):
        git = tools.Git(folder="QtAndroidCMake")
        git.clone("https://github.com/OlivierLDff/QtAndroidCMake.git", "master")
        if self.options.use_patch:
            git.checkout("9ad26790ecb8350dbee1885a0130b83c036e7509")

            src_path = path.join(self.build_folder, "patch", "patch0.patch")
            dst_path = path.join(self.build_folder, "QtAndroidCMake")
            tools.patch(patch_file=src_path, base_path=dst_path)
        else:
            git.checkout(self.options.use_version_tag)

    def package(self):
        self.copy("*", dst=".", excludes="*.patch", keep_path=False)
