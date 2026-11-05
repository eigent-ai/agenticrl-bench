from setuptools import setup, find_packages

setup(
    name="scidata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas"],
    package_data={"scidata": ["data/*.csv"]},
)
