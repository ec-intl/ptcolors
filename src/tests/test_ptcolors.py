#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the tcolors module.

Created Aug 2022
@authors: St. Rose, A. Popo, L. Andrew, and C. O. Mbengue
"""
import io
import os
import re
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

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
            f"{self.colors.timestamp}  [  NOTICE   ]  Test message"
        )

    @patch("builtins.print")
    def test_headermsg(self, mock_print):
        """Test the headermsg method."""
        self.colors.headermsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[95m "
            "[  NOTICE   ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_failmsg(self, mock_print):
        """Test the failmsg method."""
        self.colors.failmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} "
            "\033[91m [  FAILURE  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_okmsg(self, mock_print):
        """Test the okmsg method."""
        self.colors.okmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[92m "
            "[  SUCCESS  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_warnmsg(self, mock_print):
        """Test the warnmsg method."""
        self.colors.warnmsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} "
            "\033[93m [  WARNING  ] \033[0m Test message"
        )

    @patch("builtins.print")
    def test_infomsg(self, mock_print):
        """Test the infomsg method."""
        self.colors.infomsg("Test message")
        mock_print.assert_called_with(
            f"{self.colors.timestamp} \033[94m "
            "[INFORMATION] \033[0m Test message"
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


class TestMessageFormatter(unittest.TestCase):
    """Test custom headers and multiline terminal output."""

    def setUp(self):
        """Create a message writer and the expected standard layout."""
        self.colors = ptc.PTColors()
        self.expected_local = (
            "2000-01-01 00:00:00  [   LOCAL   ]  first  ─ ─ ─┐\n"
            + " " * 36
            + "second ─ ─ ─┘\n"
        )

    @staticmethod
    def capture_output(message_function, *args, columns=None, **kwargs):
        """Capture output with an optional simulated terminal width."""
        output = io.StringIO()

        with redirect_stdout(output):
            with patch.object(
                ptc.PTColors, "_output_columns", return_value=columns
            ):
                message_function(*args, **kwargs)

        return output.getvalue()

    @classmethod
    def capture_layout(cls, message_function, *args, **kwargs):
        """Capture output with ANSI colors removed and a fixed timestamp."""
        raw = cls.capture_output(message_function, *args, **kwargs)
        text = re.sub(r"\x1b\[[0-9;:]*m", "", raw)
        return re.sub(
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
            "2000-01-01 00:00:00",
            text,
            count=1,
        )

    def test_custom_header_layouts(self):
        """Check header widths with and without ANSI colors."""
        cases = [
            {"label": "LOCAL", "header": "[   LOCAL   ]", "indent": 36},
            {"label": "  LOCAL   ", "header": "[   LOCAL   ]", "indent": 36},
            {"label": "INFORMATION", "header": "[INFORMATION]", "indent": 36},
            {
                "label": "REMOTE CONTROLLER",
                "header": "[REMOTE CONTROLLER]",
                "indent": 42,
            },
            {"label": "測試", "header": "[   測試    ]", "indent": 36},
            {
                "label": "Cafe\u0301",
                "header": "[   Cafe\u0301    ]",
                "indent": 36,
            },
        ]

        for case in cases:
            for color in (None, ptc.PTColors.INFO):
                with self.subTest(label=case["label"], color=color):
                    out = self.capture_layout(
                        self.colors.defaultmsg,
                        ["first", "second"],
                        typ=case["label"],
                        color=color,
                    )
                    expected = (
                        f"2000-01-01 00:00:00  {case['header']}  "
                        "first  ─ ─ ─┐\n"
                        + " " * case["indent"]
                        + "second ─ ─ ─┘\n"
                    )
                    self.assertEqual(out, expected)

    def test_message_input_forms(self):
        """Check that strings and lists produce the same line layout."""
        for message in (
            "first\nsecond",
            "first\r\nsecond",
            ["first", "second"],
            ["first\nsecond"],
        ):
            with self.subTest(message=message):
                out = self.capture_layout(
                    self.colors.defaultmsg, message, typ="LOCAL"
                )
                self.assertEqual(out, self.expected_local)

    def test_blank_lines_and_embedded_breaks(self):
        """Preserve blank items and line breaks within list items."""
        out = self.capture_layout(
            self.colors.okmsg, ["first", "", "third\nfourth"]
        )
        expected = (
            "2000-01-01 00:00:00  [  SUCCESS  ]  first  ─ ─ ─┐\n"
            + " " * 48
            + "│\n"
            + " " * 36
            + "third       │\n"
            + " " * 36
            + "fourth ─ ─ ─┘\n"
        )
        self.assertEqual(out, expected)

    def test_trailing_blank_line(self):
        """Preserve an intentional blank line at the end of a message."""
        for message in ("first\n", ["first", ""]):
            with self.subTest(message=message):
                out = self.capture_layout(
                    self.colors.defaultmsg, message, typ="LOCAL"
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  first ─ ─ ─┐\n"
                    + " " * 36
                    + "  ─ ─ ─ ─ ─┘\n",
                )

    def test_standard_message_methods(self):
        """Check multiline alignment through every message method."""
        for message_function in (
            self.colors.defaultmsg,
            self.colors.headermsg,
            self.colors.infomsg,
            self.colors.okmsg,
            self.colors.warnmsg,
            self.colors.failmsg,
        ):
            with self.subTest(method=message_function.__name__):
                out = self.capture_layout(
                    message_function, ["first", "second"]
                )
                lines = out.split("\n")

                self.assertEqual(len(lines), 3)
                self.assertEqual(lines[1], " " * 36 + "second ─ ─ ─┘")

    def test_printable_value(self):
        """Continue accepting other printable message values."""
        out = self.capture_layout(
            self.colors.defaultmsg, 42, typ="LOCAL"
        )
        self.assertEqual(
            out, "2000-01-01 00:00:00  [   LOCAL   ]  42\n"
        )

    def test_return_value(self):
        """Keep the existing None return value."""
        with redirect_stdout(io.StringIO()):
            result = self.colors.defaultmsg(
                ["first", "second"], typ="LOCAL"
            )

        self.assertIsNone(result)

    def test_guide_alignment_for_each_longest_line_position(self):
        """Keep the bracket aligned whichever message line is longest."""
        for message in (
            ["wide", "a", "bb"],
            ["a", "wide", "bb"],
            ["a", "bb", "wide"],
        ):
            with self.subTest(message=message):
                out = self.capture_layout(
                    self.colors.defaultmsg, message, typ="LOCAL"
                )
                lines = out.splitlines()
                self.assertEqual(len(lines), 3)
                self.assertTrue(all(len(line) == 47 for line in lines))
                self.assertTrue(lines[0].endswith("┐"))
                self.assertTrue(lines[1].endswith("│"))
                self.assertTrue(lines[2].endswith("┘"))
                self.assertEqual(out.count("2000-01-01 00:00:00"), 1)

    def test_guide_uses_header_color(self):
        """Apply and reset each standard color on every guide row."""
        for color in (
            ptc.PTColors.HEADER,
            ptc.PTColors.INFO,
            ptc.PTColors.OKGREEN,
            ptc.PTColors.WARNING,
            ptc.PTColors.FAIL,
        ):
            with self.subTest(color=color):
                raw = self.capture_output(
                    self.colors.defaultmsg,
                    ["a", "b", "c"],
                    typ="LOCAL",
                    color=color,
                )
                self.assertIn(color + "─ ─ ─┐\033[0m\n", raw)
                self.assertIn(color + "     │\033[0m\n", raw)
                self.assertTrue(raw.endswith(color + "─ ─ ─┘\033[0m\n"))

    def test_uncolored_guide(self):
        """Keep the normal foreground when no header color is selected."""
        raw = self.capture_output(
            self.colors.defaultmsg, ["a", "b", "c"], typ="LOCAL"
        )
        self.assertNotIn("\033", raw)
        self.assertIn("┐", raw)
        self.assertIn("│", raw)
        self.assertIn("┘", raw)

    def test_unicode_and_ansi_widths(self):
        """Measure wide characters and combining accents without ANSI codes."""
        out = self.capture_layout(
            self.colors.defaultmsg,
            ["\033[31m測試\033[0m", "e\u0301"],
            typ="LOCAL",
            color=ptc.PTColors.INFO,
        )
        self.assertEqual(
            out,
            "2000-01-01 00:00:00  [   LOCAL   ]  測試 ─ ─ ─┐\n"
            + " " * 36
            + "e\u0301  ─ ─ ─ ─┘\n",
        )

    def test_emoji_headers_use_display_width(self):
        """Pad emoji headers and align continuations by displayed columns."""
        for emoji in ("👩\u200d🔬", "👍🏽", "©\ufe0f"):
            cases = [
                {
                    "label": emoji,
                    "header": "[    " + emoji + "     ]",
                    "indent": 36,
                },
                {
                    "label": "123456789" + emoji,
                    "header": "[123456789" + emoji + "]",
                    "indent": 36,
                },
                {
                    "label": "REMOTE " + emoji + " CONTROLLER",
                    "header": "[REMOTE " + emoji + " CONTROLLER]",
                    "indent": 45,
                },
            ]
            for case in cases:
                for color in (None, ptc.PTColors.INFO):
                    with self.subTest(label=case["label"], color=color):
                        out = self.capture_layout(
                            self.colors.defaultmsg,
                            ["first", "second"],
                            typ=case["label"],
                            color=color,
                        )
                        self.assertEqual(
                            out,
                            "2000-01-01 00:00:00  " + case["header"]
                            + "  first  ─ ─ ─┐\n"
                            + " " * case["indent"] + "second ─ ─ ─┘\n",
                        )

    def test_emoji_guides_align_with_ascii_lines(self):
        """Align emoji and ASCII rows in terminals and unbounded streams."""
        for emoji in ("👩\u200d🔬", "👍🏽", "©\ufe0f"):
            for columns in (None, 80):
                for color in (None, ptc.PTColors.INFO):
                    with self.subTest(
                        emoji=emoji, columns=columns, color=color
                    ):
                        out = self.capture_layout(
                            self.colors.defaultmsg,
                            [emoji, "ok", "go"],
                            typ="LOCAL",
                            color=color,
                            columns=columns,
                        )
                        self.assertEqual(
                            out,
                            "2000-01-01 00:00:00  [   LOCAL   ]  "
                            + emoji + " ─ ─ ─┐\n"
                            + " " * 36 + "ok      │\n"
                            + " " * 36 + "go ─ ─ ─┘\n",
                        )

    def test_emoji_wraps_at_available_columns(self):
        """Fit two complete two-column emoji into a four-column row."""
        for emoji in ("👩\u200d🔬", "👍🏽", "©\ufe0f"):
            with self.subTest(emoji=emoji):
                out = self.capture_layout(
                    self.colors.defaultmsg,
                    [emoji * 3, "x"],
                    typ="LOCAL",
                    columns=48,
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  "
                    + emoji * 2 + " ─ ─ ─┐\n"
                    + " " * 36 + emoji + "        │\n"
                    + " " * 36 + "x  ─ ─ ─ ─┘\n",
                )

    def test_emoji_fits_without_unnecessary_fallback(self):
        """Keep the guide when exactly two message columns remain."""
        for emoji in ("👩\u200d🔬", "👍🏽", "©\ufe0f"):
            with self.subTest(emoji=emoji):
                out = self.capture_layout(
                    self.colors.defaultmsg,
                    [emoji, "x"],
                    typ="LOCAL",
                    columns=46,
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  "
                    + emoji + " ─ ─ ─┐\n"
                    + " " * 36 + "x  ─ ─ ─┘\n",
                )

    def test_emoji_styles_survive_wrapping(self):
        """Preserve message styles and the separate guide color with emoji."""
        for emoji in ("👩\u200d🔬", "👍🏽", "©\ufe0f"):
            with self.subTest(emoji=emoji):
                raw = self.capture_output(
                    self.colors.defaultmsg,
                    ["\033[31m" + emoji * 3 + "\033[0m", "x"],
                    typ="LOCAL",
                    color=ptc.PTColors.INFO,
                    columns=48,
                )
                self.assertIn(
                    "\033[31m" + emoji * 2
                    + "\033[0m \033[94m─ ─ ─┐\033[0m\n",
                    raw,
                )
                self.assertIn(
                    " " * 36 + "\033[31m" + emoji
                    + "\033[0m \033[94m       │\033[0m\n",
                    raw,
                )
                self.assertTrue(raw.endswith(
                    " " * 36 + "x \033[94m ─ ─ ─ ─┘\033[0m\n"
                ))

    def test_empty_single_line_inputs(self):
        """An empty string or list retains the single-line layout."""
        for message in ("", []):
            with self.subTest(message=message):
                out = self.capture_layout(
                    self.colors.defaultmsg, message, typ="LOCAL", columns=50
                )
                self.assertEqual(
                    out, "2000-01-01 00:00:00  [   LOCAL   ]  \n"
                )

    def test_wrap_words_and_preserve_blank_rows(self):
        """Wrap at words while keeping blank rows inside one bracket."""
        for message in (
            ["alpha beta gamma", "", "done"],
            "alpha beta gamma\r\n\r\ndone",
        ):
            with self.subTest(message=message):
                out = self.capture_layout(
                    self.colors.defaultmsg, message, typ="LOCAL", columns=52
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  alpha ─ ─ ─┐\n"
                    + " " * 36 + "beta       │\n"
                    + " " * 36 + "gamma      │\n"
                    + " " * 47 + "│\n"
                    + " " * 36 + "done  ─ ─ ─┘\n",
                )

    def test_wrapping_accounts_for_long_header(self):
        """Leave room for the complete header and closing guide."""
        out = self.capture_layout(
            self.colors.defaultmsg,
            ["Using the selected configuration.", "Done."],
            typ="REMOTE CONTROLLER",
            color=ptc.PTColors.INFO,
            columns=64,
        )
        lines = out.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith(
            "2000-01-01 00:00:00  [REMOTE CONTROLLER]  Using the "
        ))
        self.assertTrue(lines[1].startswith(" " * 42 + "selected "))
        self.assertTrue(lines[2].startswith(" " * 42 + "configuration. "))
        self.assertTrue(all(len(line) == 63 for line in lines))

    def test_all_standard_methods_wrap(self):
        """Use the terminal width through every public message method."""
        for message_function in (
            self.colors.defaultmsg,
            self.colors.headermsg,
            self.colors.infomsg,
            self.colors.okmsg,
            self.colors.warnmsg,
            self.colors.failmsg,
        ):
            with self.subTest(method=message_function.__name__):
                out = self.capture_layout(
                    message_function, ["alpha beta gamma", "done"], columns=52
                )
                lines = out.splitlines()
                self.assertEqual(len(lines), 4)
                self.assertTrue(all(len(line) < 52 for line in lines))
                self.assertTrue(lines[-1].endswith("┘"))

    def test_long_words_wrap_without_losing_text(self):
        """Split long words while preserving every letter in order."""
        out = self.capture_layout(
            self.colors.defaultmsg,
            ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "done"],
            typ="LOCAL",
            columns=50,
        )
        lines = out.splitlines()
        pieces = ["ABCDEF", "GHIJKL", "MNOPQR", "STUVWX", "YZ", "done"]
        self.assertEqual(len(lines), len(pieces))
        for index in range(len(pieces)):
            self.assertTrue(lines[index][36:].startswith(pieces[index] + " "))
        self.assertTrue(all(len(line) == 49 for line in lines))

    def test_unicode_wrap_preserves_graphemes(self):
        """Keep accents attached to their base characters when wrapping."""
        out = self.capture_layout(
            self.colors.defaultmsg,
            ["測試測試" + "e\u0301" * 4, "d"],
            typ="LOCAL",
            columns=48,
        )
        lines = out.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0][36:].startswith("測試 "))
        self.assertTrue(lines[1][36:].startswith("測試 "))
        self.assertTrue(lines[2][36:].startswith("e\u0301" * 4 + " "))
        self.assertTrue(lines[3].endswith("┘"))

    def test_styles_survive_wrap_and_do_not_color_the_guide(self):
        """Replay compound styles after wrapping and reset before guides."""
        for color in (None, ptc.PTColors.INFO):
            with self.subTest(color=color):
                raw = self.capture_output(
                    self.colors.defaultmsg,
                    ["\033[1m\033[31malpha beta\033[0m", "done"],
                    typ="LOCAL",
                    color=color,
                    columns=49,
                )
                guide_color = "" if color is None else color
                self.assertIn(
                    "\033[1m\033[31malpha\033[0m "
                    + guide_color + "─ ─ ─┐",
                    raw,
                )
                self.assertIn(
                    " " * 36 + "\033[1m\033[31mbeta\033[0m ", raw
                )
                plain = re.sub(r"\x1b\[[0-9;:]*m", "", raw)
                self.assertTrue(
                    all(len(line) == 48 for line in plain.splitlines())
                )

    def test_styles_continue_across_explicit_breaks(self):
        """Restore styles across explicit lines and honor full resets."""
        for reset in ("\033[0m", "\033[m"):
            with self.subTest(reset=reset):
                raw = self.capture_output(
                    self.colors.defaultmsg,
                    ["\033[31mfirst", "second" + reset, "third"],
                    typ="LOCAL",
                )
                self.assertIn("first\033[0m ", raw)
                self.assertIn(
                    " " * 36 + "\033[31msecond" + reset + " ", raw
                )
                self.assertIn(" " * 36 + "third ", raw)

    def test_narrow_terminal_falls_back_without_truncation(self):
        """Preserve the supplied text when the header leaves no guide space."""
        for columns in (0, 20, 44):
            with self.subTest(columns=columns):
                out = self.capture_layout(
                    self.colors.defaultmsg,
                    ["alpha", "beta"],
                    typ="LOCAL",
                    columns=columns,
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  alpha\n"
                    + " " * 36 + "beta\n",
                )

    def test_wide_grapheme_falls_back_without_splitting(self):
        """Preserve whole Unicode clusters if a cluster cannot fit."""
        for cluster in ("界", "👩\u200d🔬", "🇱🇨"):
            with self.subTest(cluster=cluster):
                out = self.capture_layout(
                    self.colors.defaultmsg,
                    [cluster, "a"],
                    typ="LOCAL",
                    columns=45,
                )
                self.assertEqual(
                    out,
                    "2000-01-01 00:00:00  [   LOCAL   ]  " + cluster + "\n"
                    + " " * 36 + "a\n",
                )

    def test_oversized_header_is_preserved(self):
        """An oversized header disables the guide without shortening text."""
        label = "H" * 70
        out = self.capture_layout(
            self.colors.defaultmsg,
            ["alpha", "beta"],
            typ=label,
            columns=60,
        )
        self.assertIn("[" + label + "]  alpha", out)
        self.assertTrue(out.endswith("beta\n"))
        self.assertNotIn("┐", out)

    def test_unsupported_controls_disable_grouping(self):
        """Avoid guessing where tabs, cursor controls, or escapes will land."""
        for columns in (None, 80):
            for control in ("\t", "\r", "\b", "\033[2J", "\x7f", "\x85"):
                with self.subTest(columns=columns, control=control):
                    message = "a" + control + "b"
                    out = self.capture_layout(
                        self.colors.defaultmsg,
                        [message, "done"],
                        typ="LOCAL",
                        columns=columns,
                    )
                    self.assertEqual(
                        out,
                        "2000-01-01 00:00:00  [   LOCAL   ]  " + message
                        + "\n" + " " * 36 + "done\n",
                    )

    def test_single_line_remains_unwrapped(self):
        """A long single-line message retains the existing output."""
        message = "x" * 100
        out = self.capture_layout(
            self.colors.defaultmsg, message, typ="LOCAL", columns=50
        )
        self.assertEqual(
            out, "2000-01-01 00:00:00  [   LOCAL   ]  " + message + "\n"
        )

    def test_buffer_preserves_supplied_line_breaks(self):
        """A redirected stream is grouped without an assumed terminal width."""
        output = io.StringIO()
        with redirect_stdout(output):
            self.colors.defaultmsg(["x" * 100, "done"], typ="LOCAL")
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("x" * 100, lines[0])
        self.assertTrue(lines[-1].endswith("┘"))

    def test_trailing_blank_row_survives_wrapping(self):
        """The final blank row closes the same group after wrapping."""
        out = self.capture_layout(
            self.colors.defaultmsg, "alpha beta\n", typ="LOCAL", columns=49
        )
        lines = out.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[-1].endswith("┘"))
        self.assertTrue(all(len(line) == 48 for line in lines))


class TestTerminalWidth(unittest.TestCase):
    """Check width detection for real terminals and redirected streams."""

    def test_terminal_uses_its_own_file_descriptor(self):
        """Read the width of the actual output stream."""
        stream = Mock()
        stream.isatty.return_value = True
        stream.fileno.return_value = 7
        with patch.object(ptc.sys, "stdout", stream):
            with patch.object(
                ptc.os,
                "get_terminal_size",
                return_value=os.terminal_size((64, 24)),
            ) as get_size:
                self.assertEqual(ptc.PTColors._output_columns(), 64)
        get_size.assert_called_once_with(7)

    def test_nonterminal_has_no_width(self):
        """Do not query terminal dimensions for files or buffers."""
        with patch.object(ptc.sys, "stdout", io.StringIO()):
            with patch.object(ptc.os, "get_terminal_size") as get_size:
                self.assertIsNone(ptc.PTColors._output_columns())
        get_size.assert_not_called()

    def test_unavailable_terminal_dimensions(self):
        """Gracefully handle custom streams and unavailable terminal sizes."""
        for failure in (AttributeError, OSError, ValueError):
            with self.subTest(failure=failure):
                stream = Mock()
                stream.isatty.return_value = True
                stream.fileno.side_effect = failure
                with patch.object(ptc.sys, "stdout", stream):
                    self.assertIsNone(ptc.PTColors._output_columns())
