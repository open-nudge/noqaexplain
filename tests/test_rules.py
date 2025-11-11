# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test noqexplain rules by running the cli."""

from __future__ import annotations

import pathlib

import pytest

from noqaexplain import _cli


@pytest.mark.parametrize(
    ("directory", "error_code"),
    (
        (pathlib.Path("tests/cases/fail/no_enoqa"), 0),
        (pathlib.Path("tests/cases/fail/short_enoqa"), 1),
        (pathlib.Path("tests/cases/pass"), None),
    ),
)
def test_cli(
    directory: pathlib.Path,
    error_code: int | None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test noqaexplain rules by running the CLI.

    Args:
        directory:
            Test directory to use as a pseudo-root of the project.
        error_code:
            Expected error code, if any.
        monkeypatch:
            Pytest fixture to change test's directory.
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).

    """
    monkeypatch.chdir(pathlib.Path.cwd() / directory)
    try:
        _cli.main(args=["check"])
    except SystemExit as e:
        if error_code is None:
            assert e.code == 0  # noqa: PT017
        else:
            assert e.code == 1  # noqa: PT017
            out, _ = capsys.readouterr()
            assert f"ENQ{error_code}" in out
