# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Default values in case no configuration is provided."""

from __future__ import annotations


def suffix_mapping() -> dict[str, list[str]]:
    """Default suffix (file extension) to noqa ignore patterns mapping.

    Note:
        This list is not exhaustive and can be extended via configuration
        (`extend_suffix_mapping` config option).

    Returns:
        Suffix (file extension) to noqa ignore patterns mapping.

    """
    suffix_mapping = {
        # Python
        ".py": [
            "# noqa: ignore",
            "# ruff: noqa",
            "# flake8: noqa",
            "# pyright: ignore",
            "# type: ignore",
            "# pragma: no",  # pragma: no cover/branch
        ],
        # JavaScript
        ".js": ["// eslint-disable-next-line", "// @ts-ignore"],
        # Rust
        ".rs": ["#[allow(clippy"],
        # YAML
        ".yml": ["# zizmor: ignore", "# yamllint disable"],
        # Shell
        ".sh": ["# shellcheck disable="],
        # Dockerfile
        ".Dockerfile": ["# hadolint ignore", "# hadolint global ignore"],
    }

    suffix_mapping[".ts"] = suffix_mapping[".tsx"] = suffix_mapping[".jsx"] = (
        suffix_mapping[".js"]
    )
    suffix_mapping[".yaml"] = suffix_mapping[".yml"]
    suffix_mapping[".dockerfile"] = suffix_mapping[".Dockerfile"]

    return suffix_mapping


def name_mapping() -> dict[str, list[str]]:
    """Default filename to noqa ignore patterns mapping.

    Note:
        This function can be used for specific filenames (e.g. Dockerfile)
        instead of matching by file extension.

    Args:
        suffix_mapping:
            Suffix mapping to reuse patterns from.

    Returns:
        Filename to noqa ignore patterns mapping.

    """
    return {
        "Dockerfile": ["# hadolint ignore", "# hadolint global ignore"],
    }
