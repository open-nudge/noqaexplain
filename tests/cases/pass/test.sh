#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Example mini shell script to demonstrate basic shell functionalities

# enq: it should not be explained
# shellcheck disable=SC2034,SC2154,SC3011,SC3045
IFS=',' read -r -a skip_array <<< "${skip_files}"
