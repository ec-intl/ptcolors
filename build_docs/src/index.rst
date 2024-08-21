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

Below, you can find more information on the TColors class source code.

.. toctree::
   :maxdepth: 2
   :caption: API Contents:
   
   ptcolors


Examples
--------

Here are a few examples of how you can use **ptcolors** to enhance your terminal output:

.. code-block:: python

   from ptcolors.ptcolors import TColors

   tcolors = TColors()
   tcolors.headermsg("This is a header message.")
   tcolors.okmsg("This is a success message.")
   tcolors.warnmsg("This is a warning message.")
   tcolors.failmsg("This is a failure message.")
   tcolors.infomsg("This is an info message.")

Here’s an example of using a context manager to handle resources, like managing messages during a function’s execution. Context managers in Python, typically implemented with the with statement, allow you to control resource allocation and release efficiently.

.. code-block:: python

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
