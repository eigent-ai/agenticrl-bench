from setuptools import setup, find_packages

setup(
    name="gameengine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "toml",
    ],
    python_requires=">=3.11",
)
