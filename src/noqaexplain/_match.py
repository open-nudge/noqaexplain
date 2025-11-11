# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module to match file and its line within file against noqa pattern(s)."""

from __future__ import annotations

import collections
import dataclasses
import typing

from noqaexplain import _default

if typing.TYPE_CHECKING:
    import pathlib


@typing.final
@dataclasses.dataclass
class Matcher:
    """Match file and its line against noqa patterns.

    Note:
        See `_rule.Values` for an example usage.

    """

    config: dict[str, typing.Any]
    suffix_mapping: dict[str, list[str]] = dataclasses.field(init=False)
    name_mapping: dict[str, list[str]] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Initialize mappings.

        Note:
            Mappings can be provided (and extended) via configuration.

        """
        self.suffix_mapping = self._full_mapping("suffix")
        self.name_mapping = self._full_mapping("name")

    def _full_mapping(self, name: str) -> dict[str, list[str]]:
        """Get full mapping for given name (suffix or name).

        Args:
            name:
                Name of the mapping to retrieve.
                Either 'suffix' or 'name'.

        Returns:
            Full mapping for given name.

        """
        mapping: collections.defaultdict[str, list[str]] = (
            collections.defaultdict(
                list,
                self.config.get(
                    f"{name}_mapping", getattr(_default, f"{name}_mapping")()
                ),
            )
        )
        for extension, noqas in self.config.get(
            f"extend_{name}_mapping", {}
        ).items():
            mapping[extension].extend(noqas)  # pragma: no cover

        return mapping

    def file(self, path: pathlib.Path) -> list[str]:
        """Match `path` against suffixes and names.

        Warning:
            Name patterns have higher priority and might override
            suffix patterns.

        Args:
            path:
                Path to be matched.

        Returns:
            List (possibly empty) of matching patterns.

        """
        suffix_patterns = self.suffix_mapping.get(path.suffix, [])
        suffix_patterns.extend(self.name_mapping.get(path.name, []))
        return suffix_patterns

    def line(self, line: str, patterns: list[str]) -> int | None:
        """Match `line` against known patterns.

        Note:
            `patterns` are expected to be provided from `file()` method.

        Args:
            line:
                Line to be matched.
            patterns:
                Patterns to match against.

        Returns:
            Index of the last matching pattern, or None if no match.

        """
        for pattern in patterns:
            if (index := line.find(pattern)) != -1:
                return index
        return None
