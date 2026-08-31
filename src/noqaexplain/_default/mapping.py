# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Default values in case no configuration is provided."""

from __future__ import annotations

_LINTKIT = ["# noqa:", "# noqa-start:", "# noqa-file:"]

type NoqaComments = list[str]


def suffix() -> dict[str, NoqaComments]:
    """Default mapping from suffixes to noqa ignore patterns.

    Note:
        This list is not exhaustive and can be extended via configuration
        (`extend_mapping_suffix` config option).

    Returns:
        Mapping from suffixes (file extensions) to noqa ignore patterns.

    """
    mapping_suffix = {
        # Python
        ".py": [
            *_LINTKIT,
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
        ".yml": [*_LINTKIT, "# zizmor: ignore", "# yamllint disable"],
        # TOML
        ".toml": [*_LINTKIT],
        # Markdown
        ".md": ["<!-- pyml", "<!-- vale", "<!-- md-dead-link-check"],
        # Shell
        ".sh": ["# shellcheck disable="],
        # Dockerfile
        ".Dockerfile": ["# hadolint ignore", "# hadolint global ignore"],
    }

    mapping_suffix[".ts"] = mapping_suffix[".tsx"] = mapping_suffix[".jsx"] = (
        mapping_suffix[".js"]
    )
    mapping_suffix[".yaml"] = mapping_suffix[".yml"]
    mapping_suffix[".markdown"] = mapping_suffix[".md"]
    mapping_suffix[".dockerfile"] = mapping_suffix[".Dockerfile"]

    return mapping_suffix


def name() -> dict[str, NoqaComments]:
    """Default mapping from filenames to noqa ignore patterns.

    Note:
        This function can be used for specific filenames (e.g. Dockerfile)
        instead of matching by file extension.

    Returns:
        Mapping from filenames to noqa ignore patterns.

    """
    return {
        "Dockerfile": ["# hadolint ignore", "# hadolint global ignore"],
    }
