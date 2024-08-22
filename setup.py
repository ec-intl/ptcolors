from setuptools import setup

# Read the version from the VERSION file
with open("VERSION", "r", encoding="utf-8") as version_file:
    version = version_file.read().strip()

setup(
    name="ptcolors",
    version=version,
    author="Elizabeth Consulting International Inc.",
    author_email="info@ec-intl.com",
    description=(
        "A lightweight Python package for adding customizable terminal colors."
    ),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ec-intl/ptcolors",
    project_urls={
        "Homepage": "https://github.com/ec-intl/ptcolors",
        "Issues": "https://github.com/ec-intl/ptcolors/issues",
    },
    packages=["ptcolors"],
    package_dir={"": "src"},
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
