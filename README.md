# ptcolors Package

![GitHub license](https://img.shields.io/github/license/ec-intl/ptcolors)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ec-intl/ptcolors)
![GitHub issues](https://img.shields.io/github/issues/ec-intl/ptcolors)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ec-intl/ptcolors)
![GitHub contributors](https://img.shields.io/github/contributors/ec-intl/ptcolors)
![GitHub last commit](https://img.shields.io/github/last-commit/ec-intl/ptcolors)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ec-intl/ptcolors)
![GitHub top language](https://img.shields.io/github/languages/top/ec-intl/ptcolors)
![GitHub search hit counter](https://img.shields.io/github/search/ec-intl/ptcolors/ptcolors)
![GitHub stars](https://img.shields.io/github/stars/ec-intl/ptcolors)
![GitHub watchers](https://img.shields.io/github/watchers/ec-intl/ptcolors)

`ptcolors` is a lightweight Python package designed to add vibrant color messages to your terminal output with minimal effort. Whether you’re building command-line applications and scripts or simply want to enhance the readability of your terminal messages, `ptcolors` provides an easy-to-use interface to bring your text to life.

With `ptcolors`, you can apply a wide range of colors and styles to your terminal text, making it more engaging and visually appealing. It's perfect for developers who want to add a splash of color to their terminal without dealing with the complexities of ANSI escape codes.

## Julia Version

Looking for the Julia package? See [PTColors.jl](https://github.com/ec-intl/PTColors.jl), ECI’s related Julia package for color-coded, timestamped terminal messages.

## Project Status

Here's the current status of our workflows:

| Workflow                | Status |
|-------------------------|--------|
| Testing Suite  | [![Continuous-Integration](https://github.com/ec-intl/ptcolors/actions/workflows/ci.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/ci.yml) |
| Deployment Suite | [![Continuous-Deployment](https://github.com/ec-intl/ptcolors/actions/workflows/cd.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/cd.yml)|
| Sphinx Documentation           | [![Sphinx-docs](https://github.com/ec-intl/ptcolors/actions/workflows/docs.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/docs.yml) |
| Guard Main Branch       | [![Guard Main Branch](https://github.com/ec-intl/ptcolors/actions/workflows/guard.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/guard.yml) |
| Code Quality Checker    | [![Lint Codebase](https://github.com/ec-intl/ptcolors/actions/workflows/super-linter.yml/badge.svg)](https://github.com/ec-intl/ptcolors/actions/workflows/super-linter.yml) |

## Components

The ptcolors's codebase structure is as shown below:

```plaintext
.
├── LICENSE
├── README.md
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

![Example 1 Output](https://ecisite.s3.amazonaws.com/static/img/ptcolors/example1.jpeg)

Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently. Here we demonstrate using the PTColors context manager.

```python
# import the PTColors class
from ptcolors.ptcolors import PTColors
from builtins import RuntimeError

# instanstiate a PTColors object called msg
msg = PTColors()

# define a callback function foo that takes an argument bar and variable keyword arguments
def foo(bar: str, **kwargs) -> None:
    """A function that does nothing."""

# Use the context manager messages in the script
with msg.messages(
    "Running the foo function...",          # Message displayed at the start
    "foo function complete...",             # Message displayed on successful completion
    "foo function experienced a problem!",  # Message displayed on failure
    foo,                                    # The callback or function to be executed (foo)
    *["bar",],                              # Positional arguments for the function (bar)
    **{"Exception": RuntimeError, },        # Optional keyword arguments and optional arguments
                                            # for the callback function
) as status:
    if status:
        print("Oh no!")
    else:
        print("Hooray!")
```

This should create a terminal output similar to the one below.

![Example 2 Output](https://ecisite.s3.amazonaws.com/static/img/ptcolors/example2.jpeg)

## Custom headers and multiline messages

Use `defaultmsg` with `typ` to choose your own header. Labels have a
minimum width of 11 terminal columns. Short labels are centered, and
longer labels are preserved in full.

Messages can be strings containing `\n` or lists of strings. Each call
prints one timestamp and header. Continuation lines align beneath that
call's first message line, and intentional blank lines are preserved.
The standard message methods also support multiline input.

Multiline messages have spaced dashed connections on their first and last
lines, joined by a solid right-hand bracket. Intermediate lines, including
blank rows, have only the vertical marker. The bracket sits beyond the
longest visible message line.

Set `color` to an existing ANSI color such as `PTColors.INFO`, or omit it
for an uncolored header and guide. Each grouping marker uses the header's
color, independently of any ANSI styling inside the message.

Multiline terminal output wraps at spaces where possible, reserving room
for the actual header width and grouping guide. Long words split between
Unicode grapheme clusters, keeping accents and joined characters together.
Files, pipes, and ordinary buffers keep their supplied line breaks.
Single-line messages keep their existing layout.

If the guide cannot fit, a grapheme is too wide, or the message contains
controls other than ANSI color/style codes, the supplied text is printed
without a guide. Very narrow output may still wrap naturally in the
terminal. Resizing after printing does not reformat earlier messages.

```python
from ptcolors.ptcolors import PTColors

msg = PTColors()

msg.defaultmsg(
    "Sending the workload.\nUsing the selected configuration.",
    typ="LOCAL",
    color=PTColors.INFO,
)

msg.defaultmsg(
    ["Calculation running.", "Waiting for results."],
    typ="REMOTE CONTROLLER",
    color=PTColors.INFO,
)

lines = [
    "Calculation completed.",
    "Results saved locally.",
    "Temporary machine removed.",
]
msg.okmsg(lines)
```

Example terminal output:

![Custom headers and multiline messages with matching right-hand grouping guides](https://ecilsite-staging.s3.us-east-1.amazonaws.com/static/img/ptcolors/ptcolors-python-multiline-grouping.png)
