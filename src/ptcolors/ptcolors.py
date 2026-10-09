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
import os
import sys
import unicodedata
from contextlib import contextmanager

import regex


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

    @staticmethod
    def _text_width(text):
        """Return the column width, excluding ANSI color and style codes."""
        width = 0

        for character in regex.sub(r"\x1b\[[0-9;:]*m", "", text):
            if unicodedata.category(character) in ("Mn", "Me", "Cf", "Cc"):
                continue

            if unicodedata.east_asian_width(character) in ("W", "F"):
                width += 2
            else:
                width += 1

        return width

    @staticmethod
    def _output_columns():
        """Return stdout's terminal width, leaving other streams unbounded."""
        try:
            if sys.stdout.isatty():
                return os.get_terminal_size(sys.stdout.fileno()).columns
        except (AttributeError, OSError, ValueError):
            pass

        return None

    def _wrap_message_line(self, line, columns):
        """Wrap at spaces or grapheme boundaries, retaining ANSI styles."""
        # 1. Check whether the line can be measured safely.
        plain = regex.sub(r"\x1b\[[0-9;:]*m", "", line)
        if columns < 1 or regex.search(r"[\x00-\x1f\x7f-\x9f]", plain):
            return None
        if self._text_width(plain) <= columns:
            return [line]

        # 2. Keep complete grapheme clusters and ANSI codes together.
        tokens = regex.findall(r"\x1b\[[0-9;:]*m|\X", line)
        widths = [self._text_width(token) for token in tokens]
        if any(width > columns for width in widths):
            return None

        # 3. Fit each row, preferring the last available word boundary.
        wrapped_lines = []
        first_index = 0
        while first_index < len(tokens):
            row_width = 0
            stop_index = first_index
            last_space = None

            for index in range(first_index, len(tokens)):
                if row_width + widths[index] > columns:
                    if tokens[index] == " ":
                        last_space = index
                    break

                row_width += widths[index]
                stop_index = index + 1
                if tokens[index] == " ":
                    last_space = index

            if stop_index == len(tokens):
                wrapped_lines.append("".join(tokens[first_index:]))
                break
            if last_space is not None and last_space > first_index:
                wrapped_lines.append("".join(tokens[first_index:last_space]))
                first_index = last_space + 1
            else:
                wrapped_lines.append("".join(tokens[first_index:stop_index]))
                first_index = stop_index

        return wrapped_lines

    def _isolate_message_styles(self, lines):
        """Reset styles before each guide and restore them on the next row."""
        active_style = ""
        styled_lines = []

        for line in lines:
            opening_style = active_style
            for sequence in regex.findall(r"\x1b\[[0-9;:]*m", line):
                if sequence in ("\033[0m", "\033[m"):
                    active_style = ""
                else:
                    active_style += sequence

            closing_style = self.ENDC if active_style else ""
            styled_lines.append(opening_style + line + closing_style)

        return styled_lines

    def _format_message(self, msg, typ, color, time_text, columns=None):
        """Align and group multiline messages within the available columns."""
        # 1. Center short labels and preserve longer labels.
        label = typ.strip()
        padding = max(0, 11 - self._text_width(label))
        left_padding = padding // 2
        header = (
            f"[{' ' * left_padding}{label}"
            f"{' ' * (padding - left_padding)}]"
        )

        # 2. Convert the message into individual lines.
        if isinstance(msg, list) and all(
            isinstance(line, str) for line in msg
        ):
            message_text = "\n".join(msg)
        else:
            message_text = str(msg)

        message_lines = message_text.replace("\r\n", "\n").split("\n")

        # 3. Measure the prefix before applying color.
        prefix = f"{time_text}  {header}  "
        prefix_width = self._text_width(prefix)
        indentation = " " * prefix_width

        if color is not None:
            prefix = f"{time_text} {color} {header} {self.ENDC} "

        # 4. Preserve the existing single-line layout.
        if len(message_lines) == 1:
            return prefix + message_lines[0]

        # 5. Validate controls and reserve space for the grouping guide.
        fallback = prefix + ("\n" + indentation).join(message_lines)
        for line in message_lines:
            plain = regex.sub(r"\x1b\[[0-9;:]*m", "", line)
            if regex.search(r"[\x00-\x1f\x7f-\x9f]", plain):
                return fallback

        # Reserve seven guide columns and one spare terminal column.
        if columns is not None:
            message_width = columns - prefix_width - 8
            wrapped_lines = []
            for line in message_lines:
                wrapped = self._wrap_message_line(line, message_width)
                if wrapped is None:
                    return fallback
                wrapped_lines.extend(wrapped)
            message_lines = wrapped_lines

        message_lines = self._isolate_message_styles(message_lines)
        line_widths = [self._text_width(line) for line in message_lines]
        longest_width = max(line_widths)
        formatted_lines = []

        # 6. Align the message lines and add matching grouping markers.
        for index in range(len(message_lines)):
            line_prefix = prefix if index == 0 else indentation
            leader_width = longest_width - line_widths[index] + 5

            if index == 0 or index == len(message_lines) - 1:
                leader = " ─" * (leader_width // 2)
                if leader_width % 2:
                    leader = "─" + leader
                corner = "┐" if index == 0 else "┘"
                marker = leader + corner
            else:
                marker = " " * leader_width + "│"

            if color is not None:
                marker = color + marker + self.ENDC
            formatted_lines.append(
                line_prefix + message_lines[index] + " " + marker
            )

        return "\n".join(formatted_lines)

    def defaultmsg(
        self,
        msg,
        typ: str = "  NOTICE  ",
        color=None,
    ):
        """Print a timestamped message with an optional colored header.

        Short labels are centered within 11 visible columns. Longer labels
        are preserved in full. Existing surrounding padding is normalized.

        Strings containing line breaks and lists of strings print one
        timestamp and header, with continuation lines aligned beneath the
        first message line. Dashed connections on the first and last rows
        join a right-hand bracket. Blank rows retain their place in the group.
        The guide uses the header color, or the normal terminal foreground.

        Multiline terminal output wraps before grouping, accounting for the
        actual header and guide widths. Long words split between Unicode
        grapheme clusters. Files, pipes, and ordinary buffers retain their
        supplied line breaks. Single-line output keeps its existing layout.

        If the guide cannot fit, a grapheme is too wide, or unsupported
        controls occur, preserve the text without a guide. Very narrow output
        may still wrap naturally. Resizing after printing does not reformat
        earlier output.

        :param msg: Message text or a list of message strings.
        :type msg: str or list of str
        :param str typ: Header label.
        :param color: Optional ANSI color for the header and grouping guide.

        Example:

        .. code-block:: python

            msg = PTColors()
            msg.defaultmsg(
                ["Calculation completed.", "Results saved locally."],
                typ="LOCAL",
                color=PTColors.INFO,
            )
        """
        self.timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = self._format_message(
            msg, typ, color, self.timestamp, columns=self._output_columns()
        )
        print(formatted_message)

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
