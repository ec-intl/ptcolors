# ptcolors Repository

`ptcolors` is a lightweight Python package designed to add vibrant, customizable colors to your terminal output with minimal effort. Whether you’re building command-line applications, scripts, or simply want to enhance the readability of your terminal messages, `ptcolors` provides an easy-to-use interface to bring your text to life.

With `ptcolors`, you can apply a wide range of colors and styles to your terminal text, making it more engaging and visually appealing. It's perfect for developers who want to add a splash of color to their terminal without dealing with the complexities of ANSI escape codes.

## Project Status

Here's the current status of our workflows:

| Workflow                | Status |
|-------------------------|--------|
| Documentation           | ![Docs](https://img.shields.io/badge/Docs-passing-brightgreen) |
| Guard Main Branch       | ![Guard Main Branch](https://img.shields.io/badge/Guard%20Main%20Branch-passing-brightgreen) |
| Code Quality Checker           | ![Lint Code Base](https://img.shields.io/badge/Lint%20Code%20Base-passing-brightgreen) |

## Components

The ptcolors's codebase structure is as shown below:

```plaintext
.
├── LICENSE
├── README.md
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
from ptcolors.ptcolors import TColors

ptcolors = ptcolors()
ptcolors.headermsg("This is a header message.")
ptcolors.okmsg("This is a success message.")
ptcolors.warnmsg("This is a warning message.")
ptcolors.failmsg("This is a failure message.")
ptcolors.infomsg("This is an info message.")
```

This should create a terminal output similar to the one below.

<pre style="color: lightgreen; background-color: black;">
2024-08-21 10:33:39 [ <span style="color: magenta;">NOTICE</span> ] This is a header message.
2024-08-21 10:33:39 [ <span style="color: green;">SUCCESS</span> ] This is a success message.
2024-08-21 10:33:39 [ <span style="color: yellow;">WARNING</span> ] This is a warning message.
2024-08-21 10:33:39 [ <span style="color: red;">FAILURE</span> ] This is a failure message.
2024-08-21 10:33:39 [ <span style="color: blue;">INFORMATION</span> ] This is an info message.
</pre>

Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently.

```python
from ptcolors.ptcolors import TColors

msg = TColors()

def __call__(self):
    """Run the target sequence."""
    # The context manager is entered here, and the messages are set up.
    with self.msg.messages(
        f"Starting {self.name()}...",  # Message displayed at the start
        f"{self.name()} complete.",    # Message displayed on successful completion
        f"{self.name()} failed.",      # Message displayed on failure
        self.config["function"],       # The function to be executed
        *self.config["function-arguments"],  # Positional arguments for the function
        **self.config,                 # Keyword arguments for the function
    ) as status:
        # The status is set based on the outcome of the context manager block
        self.status = status
```
