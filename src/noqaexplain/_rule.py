# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# enq: lintkit related errors, should be fixed upstream
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false, reportUnknownArgumentType=false

# enq: too small module to split it further semantically currently
# noqa-file: PYNUDGER43

"""Explain NoQA rules/checks."""

from __future__ import annotations

import abc
import typing

import lintkit

if typing.TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from noqaexplain._matcher import Matcher


class _Values(
    lintkit.loader.File, lintkit.rule.Node, lintkit.check.Check, abc.ABC
):
    """Shared base class generating noqa values to verify."""

    def values(self) -> Iterable[lintkit.Value[str]]:  # noqa: PYNUDGER45
        """Generate noqa related values.

        Note:
            The nearest preceding nonblank line is yielded as that's
            where the noqa explanation should be placed.

        Yields:
            Values to be checked.

        """
        matcher: Matcher = self.matcher

        if patterns := matcher.file(self.file):  # pragma: no branch
            for row, line in enumerate(self._lines):
                if (column := matcher.line(line, patterns)) is not None:
                    yield lintkit.Value(
                        _preceding_explanation(self._lines, row),
                        lintkit.Pointer(row),
                        lintkit.Pointer(column),
                    )


class NoExplain(_Values, code=0):
    """Check for missing noqa explanation."""

    def check(self, value: lintkit.Value[str]) -> bool:
        """Check if noqa explanation is missing.

        Args:
            value: Value to be checked (nearest preceding nonblank line).

        Returns:
            True if explanation is missing, False otherwise.

        """
        return (
            self.matcher.config.get("explain_noqa_pattern", "enq:") not in value
        )

    def message(self, _: lintkit.Value[str]) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Display error message in case of rule violation.

        Args:
            value:
                Value which violated the rule.

        Returns:
            Message describing rule violation.

        """
        return "Missing explanation (enq) for disabled linting rule."

    def description(self) -> str:
        """Return rule description.

        Returns:
            Rule description.

        """
        return (
            "Ensures that all disabled linting rules have an associated "
            "explanation on the nearest preceding nonblank line, "
            "starting with "
            f"'{self.matcher.config.get('explain_noqa_pattern', 'enq:')}'."
        )


class NoExplainShort(_Values, code=1):
    """Check for too short noqa explanation."""

    def check(self, value: lintkit.Value[str]) -> bool:
        """Check if noqa explanation is too short.

        Note:
            Length can be configured via `min_explain_length`
            config option.

        Args:
            value: Value to be checked (nearest preceding nonblank line).

        Returns:
            True if explanation is too short, False otherwise.

        """
        pattern = self.matcher.config.get("explain_noqa_pattern", "enq:")
        if pattern in value:
            self._explanation_length: int = len(value.split(pattern)[1].strip())
            return self._explanation_length < self.config(
                "min_explain_length", 10
            )

        return False

    def message(self, _: lintkit.Value[str]) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Display error message in case of rule violation.

        Args:
            value:
                Value which violated the rule.

        Returns:
            Message describing rule violation.

        """
        explanation_length = self._explanation_length
        self._explanation_length = None  # reset for next use

        return (
            "Noqa explanation (enq) too short "
            f"(got {explanation_length} chars, minimum is "
            f"{self.config('min_explain_length', 10)} chars)."
        )

    def description(self) -> str:
        """Return rule description.

        Returns:
            Rule description.

        """
        return (
            "Ensures that all disabled linting rules have an associated "
            "explanation with the length of at least "
            f"'{self.matcher.config.get('explain_noqa_pattern', 'enq:')}', "
            "and that the explanation is of sufficient length."
        )


def _preceding_explanation(lines: Sequence[str], row: int) -> str:
    """Find the nearest preceding nonblank line.

    Args:
        lines: Lines to search.
        row: Row before which to search.

    Returns:
        Nearest preceding nonblank line, or an empty string if none exists.

    """
    for preceding_line in reversed(lines[:row]):
        if preceding_line.strip():
            return preceding_line
    return ""  # noqa: PYNUDGER30  # pragma: no cover
