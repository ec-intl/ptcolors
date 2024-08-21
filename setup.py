from setuptools import setup

setup(
    name="ptcolors",
    version="0.1.3",
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
