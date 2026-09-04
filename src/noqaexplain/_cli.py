# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# noqa-file: PYNUDGER46

"""noqaexplain CLI entrypoint."""

from __future__ import annotations

import typing

from importlib.metadata import version

import lintkit

from noqaexplain import files
from noqaexplain._matcher import Matcher

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

lintkit.settings.name.rule = "ENQ"
lintkit.settings.name.tool = "noqaexplain"

# enoqa: Import all rules to register them (side-effect)
from noqaexplain import (  # noqa: E402
    _rule,  # noqa: F401  # pyright: ignore[reportUnusedImport]
)


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

    config = lintkit.config()
    matcher = Matcher(config)

    lintkit.registry.inject("matcher", matcher)

    lintkit.cli.main(
        version=version(name),
        files_default=files.Default(matcher, config),
        files_reader=files.Reader(matcher, config),
        names=names,
        args=args,
        description="Comply or explain - justify every ignored linting rule.",
    )
