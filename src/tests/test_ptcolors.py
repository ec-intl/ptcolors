#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the tcolors module.

Created Aug 2022
@authors: St. Rose, A. Popo, L. Andrew, and C. O. Mbengue
"""
import unittest
from unittest.mock import patch

from ptcolors import ptcolors as ptc


class TestPTColors(unittest.TestCase):
    """Test the PTColors class."""

    def setUp(self):
        self.colors = ptc.PTColors()

    def does_nothing(self, arg1: str, **kwargs) -> None:
        """A function that does nothing."""

    def problem_function(self) -> None:
        """A function that raises an exception."""
        raise RuntimeError("An exception occurred!")

    @patch("builtins.print")
    def test_defaultmsg(self, mock_print):
        """Test the defaultmsg method."""
        self.colors.defaultmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp}  [  NOTICE  ]  Test message"
        )

    @patch("builtins.print")
    def test_headermsg(self, mock_print):
        """Test the headermsg method."""
        self.colors.headermsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[95m " "[  NOTICE   ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_failmsg(self, mock_print):
        """Test the failmsg method."""
        self.colors.failmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} " "\033[91m [  FAILURE  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_okmsg(self, mock_print):
        """Test the okmsg method."""
        self.colors.okmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[92m " "[  SUCCESS  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_warnmsg(self, mock_print):
        """Test the warnmsg method."""
        self.colors.warnmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} " "\033[93m [  WARNING  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_infomsg(self, mock_print):
        """Test the infomsg method."""
        self.colors.infomsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[94m " "[INFORMATION] \033[0m Test message"
        )

    def test_context_manager(self):
        """Test the context manager with arg and kwarg."""
        with self.colors.messages(
            "Running the does_nothing function...",
            "does_nothing function complete...",
            "does_nothing function experienced a problem!",
            self.does_nothing,
            *["bar",],
            **{"kwarg1": "baz", "Exception": IndexError},
        ) as status:
            self.assertFalse(status)

    def test_context_manager_no_args(self):
        """Test the context manager with no args."""
        with self.colors.messages(
            "Running the does_nothing function...",
            "does_nothing function complete...",
            "does_nothing function experienced a problem!",
            self.does_nothing,
        ) as status:
            self.assertTrue(status)

    def test_context_manager_no_kwargs(self):
        """Test the context manager with no exception."""
        with self.colors.messages(
            "Running the does_nothing function...",
            "does_nothing function complete...",
            "does_nothing function experienced a problem!",
            self.does_nothing,
            *["bar",],
        ) as status:
            self.assertFalse(status)

    def test_context_manager_exception(self):
        """Test the context manager with an exception."""
        with self.colors.messages(
            "Running the problem_function function...",
            "problem_function function complete...",
            "problem_function function experienced a problem!",
            self.problem_function,
        ) as status:
            self.assertTrue(status)
