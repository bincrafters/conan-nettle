import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration


class NettleConan(ConanFile):
    name = "nettle"
    version = "3.4.1"
    url = "https://github.com/bincrafters/conan-nettle"
    homepage = "https://www.lysator.liu.se/~nisse/nettle"
    description = "The Nettle and Hogweed low-level cryptographic libraries"
    license = ("GPL-2.0", "GPL-3.0")
    topics = ("conan", "nettle", "crypto", "low-level-cryptographic", "cryptographic")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    requires = 'gmp/6.1.2'
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("GNU nettle is not supported on Windows")
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        sha256 = "f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad"
        source_url = "https://ftp.gnu.org/gnu/nettle"
        tools.get("{0}/nettle-{1}.tar.gz".format(source_url, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            config_args = []
            if self.options.shared:
                config_args = ["--enable-shared", "--disable-static"]
            else:
                config_args = ["--enable-static", "--disable-shared"]
            self._autotools.configure(args=config_args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING*", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
