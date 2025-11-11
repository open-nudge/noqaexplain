# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0
"""Dummy module."""

from __future__ import annotations


# enq: this function should have specified the type
def foo(b) -> int:  # noqa: ANN001 # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Dummy function that adds 1 to the input integer."""
    return b + 1
