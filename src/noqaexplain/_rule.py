# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# enq: lintkit related errors, should be fixed upstream
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false, reportUnknownArgumentType=false

"""Explain NoQA rules/checks."""

from __future__ import annotations

import abc
import typing

import lintkit

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from noqaexplain._match import Matcher


class _Values(
    lintkit.loader.File, lintkit.rule.Node, lintkit.check.Check, abc.ABC
):
    """Shared base class generating noqa values to verify."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Generate noqa related values.

        Note:
            Line __above__ noqa comment is yielded as that's
            where the noqa explanation should be placed.

        Yields:
            Values to be checked.

        """
        matcher: Matcher = self.matcher

        if patterns := matcher.file(self.file):
            for row, line in enumerate(self._lines):
                if (column := matcher.line(line, patterns)) is not None:
                    # Edge case matching 0-th line which could be disabled
                    # by placing enq at the end, not worth checking I think
                    yield lintkit.Value(
                        self._lines[row - 1],  # pyright: ignore[reportOptionalSubscript]
                        lintkit.Pointer(row),
                        lintkit.Pointer(column),
                    )
        else:  # pragma: no cover
            pass


class NoExplain(_Values, code=0):
    """Check for missing noqa explanation."""

    def check(self, value: lintkit.Value[str]) -> bool:
        """Check if noqa explanation is missing.

        Args:
            value: Value to be checked (line above noqa comment).

        Returns:
            True if explanation is missing, False otherwise.

        """
        return self.config.get("explain_noqa_pattern", "enq:") not in value

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
            "explanation one line above them, starting with "
            f"'{self.config.get('explain_noqa_pattern', 'enq:')}'."
        )


class NoExplainShort(_Values, code=1):
    """Check for too short noqa explanation."""

    def check(self, value: lintkit.Value[str]) -> bool:
        """Check if noqa explanation is too short.

        Note:
            Length can be configured via `min_explain_length`
            config option.

        Args:
            value: Value to be checked (line above noqa comment).

        Returns:
            True if explanation is too short, False otherwise.

        """
        if self.config.get("explain_noqa_pattern", "enq:") in value:
            self._explanation_length: int = len(
                value.split(self.config.get("explain_noqa_pattern", "enq:"))[
                    1
                ].strip()
            )
            return self._explanation_length < self.config.get(
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
            f"{self.config.get('min_explain_length', 10)} chars)."
        )

    def description(self) -> str:
        """Return rule description.

        Returns:
            Rule description.

        """
        return (
            "Ensures that all disabled linting rules have an associated "
            "explanation with the length of at least "
            f"'{self.config.get('explain_noqa_pattern', 'enq:')}', "
            "and that the explanation is of sufficient length."
        )
