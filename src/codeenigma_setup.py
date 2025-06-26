import os

from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.extension import Extension

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the extension module
codeenigma_extension = Extension(
    name="codeenigma",
    sources=[os.path.join(current_dir, "codeenigma.pyx")],
    extra_compile_args=["-O3", "-fPIC"],
    language="c",
)

# Setup configuration
setup(
    name="codeenigma",
    version="0.1.0",
    description="Python code obfuscation tool using AES and Base64 encryption",
    ext_modules=cythonize(
        [codeenigma_extension],
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "initializedcheck": False,
            "nonecheck": False,
            "cdivision": True,
            "c_string_type": "str",
            "c_string_encoding": "utf8",
            "legacy_implicit_noexcept": False,
        },
        nthreads=4,
    ),
    packages=find_packages(),
    zip_safe=False,
)
