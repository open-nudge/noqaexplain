# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Default file discovery mechanism."""

# noqa-file: PYNUDGER46

from __future__ import annotations

import pathlib
import typing

import lintkit

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from noqaexplain._matcher import Matcher


class Default(lintkit.cli.files.default.Base):
    """Provide default files to lint."""

    def __init__(self, matcher: Matcher, config: dict[str, typing.Any]) -> None:
        """Configure default file discovery.

        Args:
            matcher:
                The matcher used to identify files with known noqa patterns.
            config:
                Configuration dictionary with directory ignore settings.

        """
        self.matcher: Matcher = matcher
        self.config: dict[str, typing.Any] = config

    @typing.override
    def __call__(self) -> Iterable[pathlib.Path]:
        """Provide resolved files containing known noqa patterns.

        Yields:
            Resolved files containing known noqa patterns.

        """
        ignores = _ignores(self.config)

        for path in pathlib.Path().rglob("*"):
            if (  # pragma: no branch
                path.is_file()
                and ignores.isdisjoint(path.parts)
                and self.matcher.file(path)
            ):
                yield path.resolve()


class Reader(lintkit.cli.files.reader.Base):
    """Recursively expand file and directory arguments."""

    def __init__(self, matcher: Matcher, config: dict[str, typing.Any]) -> None:
        """Configure recursive file argument reading.

        Args:
            matcher:
                The matcher used to identify files with known noqa patterns.
            config:
                Configuration dictionary with directory ignore settings.

        """
        self.matcher: Matcher = matcher
        self.config: dict[str, typing.Any] = config

    @typing.override
    def __call__(
        self, paths: Iterable[str | pathlib.Path]
    ) -> Iterable[str | pathlib.Path]:
        """Yield resolved files from explicit and directory arguments.

        Args:
            paths:
                File or directory arguments.

        Yields:
            Resolved, first-seen file paths without canonical duplicates.

        """
        ignores = _ignores(self.config)
        seen: set[pathlib.Path] = set()

        for value in paths:
            path = pathlib.Path(value).resolve()
            directory = path.is_dir()
            candidates = path.rglob("*") if directory else (path,)
            for candidate in candidates:
                resolved = candidate.resolve()
                if (
                    resolved not in seen
                    and (  # pragma: no branch
                        not directory
                        or (
                            resolved.is_file()
                            and ignores.isdisjoint(resolved.parts[:-1])
                            and self.matcher.file(resolved)
                        )
                    )
                ):
                    seen.add(resolved)
                    yield resolved


def _ignores(config: dict[str, typing.Any]) -> set[str]:
    """Return a set of directory names to ignore.

    Args:
        config:
            Configuration dictionary containing directory ignore settings.

    Returns:
        Set of directory names to ignore.

    """
    return set(
        config.get(
            "dir_ignores",
            ["__pypackages__", ".venv", ".git", "__pycache__"],
        )
    ) | set(config.get("extend_dir_ignores", []))
