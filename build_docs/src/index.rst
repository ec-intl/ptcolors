.. tcolors documentation master file, created by
   sphinx-quickstart on Thu Aug 15 09:48:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

    <h1>
        <span style="color:purple;">p</span>
        <span style="color:blue;">t</span>
        <span style="color:green;">c</span>
        <span style="color:yellow;">o</span>
        <span style="color:red;">l</span>
        <span style="color:black;">o</span>
        <span style="color:purple;">r</span>
        <span style="color:blue;">s</span> Documentation!
    </h1>


**ptcolors** is a lightweight Python package designed to add vibrant, customizable colors to your terminal output with minimal effort. Whether you’re building command-line applications, scripts, or simply want to enhance the readability of your terminal messages, **ptcolors** provides an easy-to-use interface to bring your text to life.

With **ptcolors**, you can apply a wide range of colors and styles to your terminal text, making it more engaging and visually appealing. It's perfect for developers who want to add a splash of color to their terminal without dealing with the complexities of **ANSI** escape codes.

Julia Version
-------------

Looking for the Julia package? See `PTColors.jl <https://github.com/ec-intl/PTColors.jl>`_, ECI's related Julia package for color-coded, timestamped terminal messages.

Below, you can find more information on the PTColors class source code.

.. toctree::
   :maxdepth: 2
   :caption: API Contents:
   
   ptcolors


Examples
--------

Here are a few examples of how you can use **ptcolors** to enhance your terminal output:

.. code-block:: python

   from ptcolors.ptcolors import PTColors

   tcolors = PTColors()
   tcolors.headermsg("This is a header message.")
   tcolors.okmsg("This is a success message.")
   tcolors.warnmsg("This is a warning message.")
   tcolors.failmsg("This is a failure message.")
   tcolors.infomsg("This is an info message.")

This should create a terminal output similar to the one below.

.. raw:: html

    <pre style="color: lightgreen; background-color: black;">
    2024-08-21 10:33:39 [ <span style="color: magenta;">NOTICE</span> ] This is a header message.
    2024-08-21 10:33:39 [ <span style="color: green;">SUCCESS</span> ] This is a success message.
    2024-08-21 10:33:39 [ <span style="color: yellow;">WARNING</span> ] This is a warning message.
    2024-08-21 10:33:39 [ <span style="color: red;">FAILURE</span> ] This is a failure message.
    2024-08-21 10:33:39 [ <span style="color: blue;">INFORMATION</span> ] This is an info message.
    </pre>


Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently.

.. code-block:: python

    from ptcolors.ptcolors import PTColors

    msg = PTColors()

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

Custom headers and multiline messages
-------------------------------------

Use ``defaultmsg`` with ``typ`` to choose your own header. Labels have a
minimum width of 11 terminal columns. Short labels are centered, and
longer labels are preserved in full.

Messages can be strings containing ``\n`` or lists of strings. Each call
prints one timestamp and header. Continuation lines align beneath that
call's first message line, and intentional blank lines are preserved.
The standard message methods also support multiline input.

Multiline messages have spaced dashed connections on their first and last
lines, joined by a solid right-hand bracket. Intermediate lines, including
blank rows, have only the vertical marker. The bracket sits beyond the
longest visible message line.

Set ``color`` to an existing ANSI color such as ``PTColors.INFO``, or omit
it for an uncolored header and guide. Each grouping marker uses the header's
color, independently of any ANSI styling inside the message.

Multiline terminal output wraps at spaces where possible, reserving room
for the actual header width and grouping guide. Long words split between
Unicode grapheme clusters, keeping accents and joined characters together.
Width calculations also account for combined emoji. Their actual appearance
and width can still vary with the terminal's rendering support.
Files, pipes, and ordinary buffers keep their supplied line breaks.
Single-line messages keep their existing layout.

If the guide cannot fit, a grapheme is too wide, or the message contains
controls other than ANSI color/style codes, the supplied text is printed
without a guide. Very narrow output may still wrap naturally in the
terminal. Resizing after printing does not reformat earlier messages.

.. code-block:: python

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

Example terminal output:

.. image:: https://ecilsite-staging.s3.us-east-1.amazonaws.com/static/img/ptcolors/ptcolors-python-multiline-grouping.png
   :alt: Custom headers and multiline messages with matching right-hand grouping guides
   :width: 100%

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
