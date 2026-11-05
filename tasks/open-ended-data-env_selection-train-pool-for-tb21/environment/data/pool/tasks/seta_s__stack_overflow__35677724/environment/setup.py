from setuptools import setup, Extension

fastmath_ext = Extension(
    "datacrunch._fastmath",
    sources=["src/_fastcalc.c"],
    include_dirs=[],
)

setup(
    name="datacrunch",
    version="0.1.0",
    packages=["datacrunch"],
    ext_modules=[fastmath_ext],
)
