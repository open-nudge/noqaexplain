# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# noqa-file: PYNUDGER46

"""noqaexplain CLI entrypoint."""

from __future__ import annotations

import pathlib
import typing

from importlib.metadata import version

import lintkit
import loadfig

from noqaexplain._match import Matcher

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

lintkit.settings.name = "ENQ"

# enoqa: Import all rules to register them (side-effect)
from noqaexplain import (  # noqa: E402
    _rule,  # noqa: F401  # pyright: ignore[reportUnusedImport]
)


def _files_default(
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


def main(
    args: list[str] | None = None,
    names: Iterable[str] | None = None,
) -> None:
    """Run the CLI.

    Note:
        Arguments are used for testing purposes only.

    Args:
        args:
            CLI arguments, defaults to sys.argv[1:].
        names:
            Complete, case-sensitive rule names to include, such as ``ENQ0``.

    """
    name = "noqaexplain"

    config = loadfig.config(name)
    matcher = Matcher(config)

    lintkit.registry.inject("config", config)
    lintkit.registry.inject("matcher", matcher)

    if names is None:  # pragma: no cover
        names = config.get("names")

    lintkit.cli.main(
        version=version(name),
        files_default=_files_default(matcher, config),
        names=names,
        end_mode=config.get("end_mode", "all"),
        args=args,
        description="Comply or explain - justify every ignored linting rule.",
    )
