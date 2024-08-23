#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility module for clidapp application.

:authors: J. St. Rose [#]_,
    A.M.E. Popo [#]_,
    C.O. Mbengue [#]_

:synopsis: This module encapsulates utility functions and objects for clidapp.

:created on: Feb 2022

.. [#] jstrose@ec-intl-com
.. [#] apopo@ec-intl-com
.. [#] cmbengue@ec-intl-com

"""
import datetime as dt
from contextlib import contextmanager


class PTColors:
    """Terminal colors."""

    HEADER = "\033[95m"
    INFO = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

    def __init__(self):
        """Initialize PTColors class."""
        self.timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def defaultmsg(
        self,
        msg: str,
        typ: str = "  NOTICE  ",
        color=None,
    ):
        """Print default message.

        :param str msg: message to be printed
        :param str color: color of the message
        :param str typ: type of the message
        """
        self.timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if color is None:
            print(f"{self.timestamp}  [{typ}]  {msg}")
        else:
            print(f"{self.timestamp} {color} [{typ}] {self.ENDC} {msg}")

    def headermsg(self, msg):
        """Print header message.

        :param str msg: message to be printed
        """
        self.defaultmsg(msg, "  NOTICE   ", self.HEADER)

    def failmsg(self, msg):
        """Print fail message.

        :param str msg: message to be printed
        """
        self.defaultmsg(msg, "  FAILURE  ", self.FAIL)

    def okmsg(self, msg):
        """Print ok message.

        :param str msg: message to be printed
        """
        self.defaultmsg(msg, "  SUCCESS  ", self.OKGREEN)

    def warnmsg(
        self,
        msg,
    ):
        """Print warning message.

        :param str msg: message to be printed
        """
        self.defaultmsg(msg, "  WARNING  ", self.WARNING)

    def infomsg(self, msg):
        """Print ok blue message.

        :param str msg: message to be printed
        """
        self.defaultmsg(msg, "INFORMATION", self.INFO)

    @contextmanager
    def messages(
        self,
        info_msg,
        success_msg,
        failure_msg,
        callback,
        *args,
        **kwargs,
    ):
        """Context manager that prints messages and runs a callback.

        :param str info_msg: Info message to be printed on entry.
        :param str success_msg: Success message to be printed on exit if the
            callback succeeds.
        :param str failure_msg: Failure message to be printed on exit if the
            callback fails.
        :param callable callback: Callback function to be run in the context.
        :param args: Positional arguments for the callback.
        :param kwargs: Keyword arguments with expected Exception.

        To use this context manager, you can do the following:

        .. code-block:: python

                with PTColors().messages(
                    "Starting...",
                    "Success...",
                    "Failure...",
                    callback,
                    *args,
                    **kwargs,
                ) as status:
                    if status:
                        # Do something if the callback fails
                    else:
                        # Do something if the callback succeeds
        """
        exception = kwargs.get("Exception", Exception)
        try:
            self.infomsg(info_msg)
            callback(*args, **kwargs)
            self.okmsg(success_msg)
            yield 0
        except exception as e:
            self.failmsg(failure_msg)
            self.failmsg(str(e))
            yield 1
