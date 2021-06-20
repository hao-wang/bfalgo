from setuptools import setup, find_packages

NAME = "bfalgo"
DESCRIPTION = "Barefoot Algorithm: implements of fundamental algorithms."
VERSION = "0.1.0"
with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    author="hao wang",
    author_email="hwang.phy@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(where="bfalgo", exclude=["dat.*", "dat"]),
    install_requires=['numpy', 'scikit-learn', 'scipy'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3+",
    ],
    zip_safe=False,
)
