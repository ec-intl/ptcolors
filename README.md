# ptcolors Repository

`ptcolors` is a lightweight Python package designed to add vibrant, customizable colors to your terminal output with minimal effort. Whether you’re building command-line applications and scripts or simply want to enhance the readability of your terminal messages, `ptcolors` provides an easy-to-use interface to bring your text to life.
`ptcolors` is a lightweight Python package designed to add vibrant, customizable colors to your terminal output with minimal effort. Whether you’re building command-line applications and scripts or simply want to enhance the readability of your terminal messages, `ptcolors` provides an easy-to-use interface to bring your text to life.

With `ptcolors`, you can apply a wide range of colors and styles to your terminal text, making it more engaging and visually appealing. It's perfect for developers who want to add a splash of color to their terminal without dealing with the complexities of ANSI escape codes.

## Project Status

Here's the current status of our workflows:

| Workflow                | Status |
|-------------------------|--------|
| Continuous Integration  | [![Continuous-Integration](https://github.com/ec-intl/ptcolors/actions/workflows/ci.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/ci.yml) |
| Documentation           | [![Sphinx-docs](https://github.com/ec-intl/ptcolors/actions/workflows/docs.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/docs.yml) |
| Guard Main Branch       | [![Guard Main Branch](https://github.com/ec-intl/ptcolors/actions/workflows/guard.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/guard.yml) |
| Code Quality Checker           | [![Lint Codebase](https://github.com/ec-intl/ptcolors/actions/workflows/super-linter.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/super-linter.yml) |

## Components

The ptcolors's codebase structure is as shown below:

```plaintext
.
├── LICENSE
├── README.md
├── MANIFEST.in
├── MANIFEST.in
├── VERSION
├── build_docs
│   ├── Makefile
│   ├── __init__.py
│   ├── build
│   ├── make.bat
│   └── src
│       ├── __init__.py
│       ├── _static
│       ├── _templates
│       ├── conf.py
│       ├── index.rst
│       └── ptcolors.rst
├── requirements
│   ├── testing.txt
├── requirements.txt
├── setup.py
└── src
    ├── ptcolors
    │   ├── __init__.py
    │   └── ptcolors.py
    └── tests
        ├── __init__.py
        └── test_ptcolors.py

```

## Example

Here's an example of how to use `ptcolors`:

```python
# import the PTColors class
from ptcolors.ptcolors import PTColors
# import the PTColors class
from ptcolors.ptcolors import PTColors

# create a msg object
msg = PTColors()

# use the msg methods
msg.headermsg("This is a header message.")
msg.okmsg("This is a success message.")
msg.warnmsg("This is a warning message.")
msg.failmsg("This is a failure message.")
msg.infomsg("This is an info message.")
# create a msg object
msg = PTColors()

# use the msg methods
msg.headermsg("This is a header message.")
msg.okmsg("This is a success message.")
msg.warnmsg("This is a warning message.")
msg.failmsg("This is a failure message.")
msg.infomsg("This is an info message.")
```

This should create a terminal output similar to the one below.

![Example 1 Output](https://ecisite.s3.amazonaws.com/static/img/example1.jpeg)

Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently. Here we demonstrate using the PTColors context manager.
Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently. Here we demonstrate using the PTColors context manager.

```python
# import the PTColors class
from ptcolors.ptcolors import PTColors
from builtins import RuntimeError

# instanstiate a PTColors object called msg
msg = PTColors()


# define a callback function foo that takes an argument bar
def foo(bar: str) -> None:
    """A function that does nothing."""


# Use the context manager messages in the script
with msg.messages(
    "Running the foo function...",          # Message displayed at the start
    "foo function complete...",             # Message displayed on successful completion
    "foo function experienced a problem!",  # Message displayed on failure
    foo,                                    # The callback or function to be executed (foo)
    *["bar",],                              # Positional arguments for the function (bar)
    **{"Exception": RuntimeError, },        # The Required keyword arguments
) as status:
    if not status:
        print("Hooray!")
    else:
        print("Oh no!")
```

This should create a terminal output similar to the one below.

![Example 2 Output](https://ecisite.s3.amazonaws.com/static/img/example2.jpeg)
