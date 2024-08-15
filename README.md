# tcolors Repository

`tcolors` is a lightweight Python package designed to add vibrant, customizable colors to your terminal output with minimal effort. Whether you’re building command-line applications, scripts, or simply want to enhance the readability of your terminal messages, `tcolors` provides an easy-to-use interface to bring your text to life.

With `tcolors`, you can apply a wide range of colors and styles to your terminal text, making it more engaging and visually appealing. It's perfect for developers who want to add a splash of color to their terminal without dealing with the complexities of ANSI escape codes.

## Project Status

Here's the current status of our workflows:

| Workflow                | Status |
|-------------------------|--------|
| Continuous Integration  | ![Continuous-Integration](https://img.shields.io/badge/Continuous--Integration-passing-brightgreen) |
| Continuous Deployment   | ![Continuous-Deployment](https://img.shields.io/badge/Continuous--Deployment-passing-brightgreen) |
| Documentation           | ![Docs](https://img.shields.io/badge/Docs-passing-brightgreen) |
| Guard Main Branch       | ![Guard Main Branch](https://img.shields.io/badge/Guard%20Main%20Branch-passing-brightgreen) |
| Lint Codebase           | ![Lint Code Base](https://img.shields.io/badge/Lint%20Code%20Base-passing-brightgreen) |
| Release Log             | ![Release Log](https://img.shields.io/badge/Release%20Log-passing-brightgreen) |

## Components

The tcolors's codebase structure is as shown below:

```plaintext
.
├── LICENSE
├── README.md
├── VERSION
├── build_docs
│   ├── Makefile
│   ├── __init__.py
│   ├── build
│   │   ├── doctrees
│   │   │   ├── environment.pickle
│   │   │   ├── index.doctree
│   │   │   └── tcolors.doctree
│   │   └── html
│   │       ├── _sources
│   │       │   ├── index.rst.txt
│   │       │   └── tcolors.rst.txt
│   │       ├── _static
│   │       │   ├── alabaster.css
│   │       │   ├── basic.css
│   │       │   ├── custom.css
│   │       │   ├── doctools.js
│   │       │   ├── documentation_options.js
│   │       │   ├── file.png
│   │       │   ├── jquery-3.5.1.js
│   │       │   ├── jquery.js
│   │       │   ├── language_data.js
│   │       │   ├── minus.png
│   │       │   ├── plus.png
│   │       │   ├── pygments.css
│   │       │   ├── searchtools.js
│   │       │   ├── underscore-1.13.1.js
│   │       │   └── underscore.js
│   │       ├── genindex.html
│   │       ├── index.html
│   │       ├── objects.inv
│   │       ├── py-modindex.html
│   │       ├── search.html
│   │       ├── searchindex.js
│   │       └── tcolors.html
│   ├── make.bat
│   └── src
│       ├── __init__.py
│       ├── _static
│       ├── _templates
│       ├── conf.py
│       ├── index.rst
│       └── tcolors.rst
├── environments
│   ├── development.env
│   ├── production.env
│   ├── staging.env
│   └── testing.env
├── requirements.txt
└── src
    ├── __init__.py
    ├── tcolors.py
    └── tests
        ├── __init__.py
        └── test_tcolors.py

```
