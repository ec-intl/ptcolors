#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the tcolors module.

Created Aug 2022
@authors: St. Rose, A. Popo, L. Andrew, and C. O. Mbengue
"""
import unittest
from unittest.mock import patch

from src.ptcolors import tcolors as wu


class TestTColors(unittest.TestCase):
    """Test the TColors class."""

    def setUp(self):
        self.colors = wu.TColors()

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
