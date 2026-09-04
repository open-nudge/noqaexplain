# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# noqa-file: PYNUDGER46

"""Test noqexplain rules by running the cli."""

from __future__ import annotations

import pathlib

import pytest

from noqaexplain import _cli


@pytest.mark.parametrize(
    ("directory", "names", "error_code"),
    (
        (pathlib.Path("tests/cases/fail/no_enoqa"), None, 0),
        (pathlib.Path("tests/cases/fail/short_enoqa"), None, 1),
        (pathlib.Path("tests/cases/pass"), None, None),
        (pathlib.Path("tests/cases/names"), ("ENQ1",), None),
        (pathlib.Path("tests/cases/config"), ("ENQ0",), None),
        (pathlib.Path("tests/cases/config"), ("ENQ1",), 1),
    ),
)
def test_cli(
    directory: pathlib.Path,
    names: tuple[str, ...] | None,
    error_code: int | None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test noqaexplain rules by running the CLI.

    Args:
        directory:
            Test directory to use as a pseudo-root of the project.
        names:
            Rule names to select programmatically.
        error_code:
            Expected error code, if any.
        monkeypatch:
            Pytest fixture to change test's directory.
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).

    """
    monkeypatch.chdir(pathlib.Path.cwd() / directory)
    try:
        _cli.main(args=["check"], names=names)
    except SystemExit as e:
        if error_code is None:
            assert e.code == 0  # noqa: PT017
        else:
            assert e.code == 1  # noqa: PT017
            out, _ = capsys.readouterr()
            assert f"ENQ{error_code}" in out
