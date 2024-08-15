from setuptools import find_packages, setup

setup(
    name="tcolors",
    version="0.1.0",
    author="Elizabeth Consulting International Inc.",
    author_email="info@ec-intl.com",
    description=(
        "A lightweight Python package for adding customizable terminal colors."
    ),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ec-intl/tcolors",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=open("requirements.txt", encoding="utf-8")
    .read()
    .splitlines(),
)
