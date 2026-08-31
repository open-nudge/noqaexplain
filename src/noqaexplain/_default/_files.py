# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Default file discovery mechanism."""

# noqa-file: PYNUDGER46

from __future__ import annotations

import pathlib
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from noqaexplain._matcher import Matcher


def files(
    matcher: Matcher, config: dict[str, typing.Any]
) -> Iterable[pathlib.Path]:
    """Files to lint.

    Args:
        matcher:
            The matcher to determine which files contain known noqa patterns.
        config:
            Configuration dictionary containing directory ignore settings.

    Note:
        File is yielded only if it matches one of the known
        files containing known noqa patterns.

    Yields:
        Set of files with known noqa patterns.

    """
    ignores = set(
        config.get(
            "dir_ignores", ["__pypackages__", ".venv", ".git", "__pycache__"]
        )
    ) | set(config.get("extend_dir_ignores", []))

    for path in pathlib.Path().rglob("*"):
        if (
            path.is_file()
            and ignores.isdisjoint(path.parts)
            and matcher.file(path)
        ):
            yield path.resolve()
        else:  # pragma: no cover
            pass
