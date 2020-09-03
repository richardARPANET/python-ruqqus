import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruqqus",
    version="0.0.1",
    author="Ruqqus LLC",
    author_email="info@ruqqus.com",
    description="Ruqqus API Wrapper",
    long_description="Ruqqus API Wrapper. Work in progress.",
    long_description_content_type="text/markdown",
    url="https://github.com/ruqqus/python-ruqqus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
