# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests of the package."""

from __future__ import annotations

import noqaexplain

from noqaexplain import _cli


def test_version() -> None:
    """Smoke test package version."""
    # nosemgrep
    assert noqaexplain.__version__ != ""


def test_rules() -> None:
    """Smoke tests rules have descriptions."""
    try:
        _cli.main(args=["rules"])
    except SystemExit as e:
        # nosemgrep
        assert e.code == 0  # noqa: PT017
