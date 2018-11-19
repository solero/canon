import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canon",
    version="0.0.1",
    author="Ben",
    author_email="ben@solero.me",
    description="Canon is a tool for emulating the compression found in two of the Club Penguin mini-games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ketnipz/Canon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)