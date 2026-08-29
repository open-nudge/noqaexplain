# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# noqa-file: PYNUDGER46

"""Placeholder module."""

from __future__ import annotations


def foo(b) -> int:  # noqa: ANN001 # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Placeholder function that adds 1 to the input integer.

    Args:
        b: The input integer to increment.

    Returns:
        The input integer plus one.
    """
    return b + 1
