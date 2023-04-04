import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pad_asset_manager",
    version="0.0.1",
    author="Aradia Megido#2552 and Cody Watts",
    author_email="chasehult@gmail.com",
    license="MIT",
    description="An asset and extra manager for Puzzle and Dragons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TsubakiBotPad/tsutils",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
