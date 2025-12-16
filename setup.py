from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'dct_cpp',
        ['dct_cpp.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-O3', '-std=c++11'],
    ),
]

setup(
    name='dct_fast',
    ext_modules=ext_modules,
)