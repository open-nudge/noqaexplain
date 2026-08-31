<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# noqaexplain

<!-- mkdocs remove start -->

<!-- vale off -->

<!-- pyml disable-num-lines 30 line-length-->

<p align="center">
    <em>Comply or explain - justify every ignored linting rule.</em>
</p>

<div align="center">

<a href="https://pypi.org/project/noqaexplain">![PyPI - Python Version](https://img.shields.io/pypi/v/noqaexplain?style=for-the-badge&label=release&labelColor=grey&color=blue)
</a>
<a href="https://pypi.org/project/noqaexplain">![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fopen-nudge%2Fnoqaexplain%2Fmain%2Fpyproject.toml&style=for-the-badge&label=python&labelColor=grey&color=blue)
</a>
<a href="https://opensource.org/licenses/Apache-2.0">![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)
</a>
<a>![Coverage Hardcoded](https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge)
</a>
<a href="https://scorecard.dev/viewer/?uri=github.com/open-nudge/noqaexplain">![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/open-nudge/noqaexplain?style=for-the-badge&label=OSSF)
</a>

</div>

<p align="center">
✨ <a href="#features">Features</a>
🚀 <a href="#quick-start">Quick start</a>
📚 <a href="https://open-nudge.github.io/noqaexplain">Documentation</a>
🤝 <a href="#contribute">Contribute</a>
👍 <a href="https://github.com/open-nudge/noqaexplain/blob/main/ADOPTERS.md">Adopters</a>
📜 <a href="#legal">Legal</a>
</p>
<!-- vale on -->

______________________________________________________________________

<!-- mkdocs remove end -->

## Features

__noqaexplain__ is a linter which enforces justifying every ignored linting rule
supporting __multiple formats/linters__:

- __Python__ -[`ruff`](https://github.com/astral-sh/ruff) and
    [`flake8`](https://github.com/PyCQA/flake8) `# noqa`,
    [`coveragepy`](https://github.com/nedbat/coveragepy) `# pragma: no cover`,
    and [`lintkit`](https://github.com/open-nudge/lintkit) line, span, and
    file suppressions
- __JavaScript/TypeScript__ - [`eslint`](https://github.com/eslint/eslint)
- __Rust__ - [`clippy`](https://github.com/rust-lang/rust-clippy)
- __Dockerfiles__ - [`hadolint`](https://github.com/hadolint/hadolint)
- __YAML__ - [`yamllint`](https://github.com/adrienverge/yamllint) and
    `lintkit` line, span, and file suppressions
- __TOML__ - `lintkit` line, span, and file suppressions
- __Markdown__ - [`PyMarkdown`](https://github.com/jackdewinter/pymarkdown),
    [`Vale`](https://vale.sh), and
    [`md-dead-link-check`](https://github.com/AlexanderDokuchaev/md-dead-link-check)
- __Shell__ - [`shellcheck`](https://www.shellcheck.net/)

> [!IMPORTANT]
> You can expand this list with __any__ language and linter by using
> `extend_mapping_suffix` and/or `extend_mapping_name`!
> __Feel free to open a request to add support for more linters.__

## Table of contents

- [Quick start](#quick-start)
    - [Installation](#installation)
    - [Usage](#usage)
- [Advanced](#advanced)
    - [Configuration](#configuration)
    - [Run as a pre-commit hook](#run-as-a-pre-commit-hook)
    - [Rules](#rules)

## Quick start

### Installation

> [!TIP]
> You can use your favorite package manager like
> [`uv`](https://github.com/astral-sh/uv),
> [`hatch`](https://github.com/pypa/hatch)
> or [`pdm`](https://github.com/pdm-project/pdm)
> instead of `pip`.

```sh
> pip install noqaexplain[all]
```

To install `rich` output and MCP server as well:

```sh
> pip install noqaexplain[all]
```

### Usage

To check against all files (the ones with defined mappings
from file extension to error disable comment format), run:

```sh
> noqaxplain check
```

You can pass additional arguments to `noqaexplain check`, like files
to check:

```sh
> noqaexplain check path/to/file.py maybe.rs other.yml formats.js
```

If a certain file has a line with disabled check without an explanation,
the tool will report it:

```plaintext
path/to/file.py:10:5: ENQ0 Missing explanation (enoqa) for disabled linting rule
```

to fix it, just add an explanation after the disable comment prefixed by `enq:`,
e.g.:

```python
import some_library

# enq: Disabled private access check as there is no other workaround currently.
# noqa: SLF001
some_library._private_function()
```

The same rule applies to opening span and file-wide `lintkit` directives:

```toml
# enq: Generated settings are checked separately before publication.
# noqa-file: MYLINTER1

# enq: This generated section cannot follow the repository style.
# noqa-start: MYLINTER2
generated = true
# noqa-end: MYLINTER2
```

Markdown suppressions use an HTML comment for the explanation:

```markdown
<!-- enq: Generated content cannot satisfy the line length rule. -->
<!-- pyml disable-next-line line-length -->
```

Markdown matching uses the literal comment prefixes `<!-- pyml`, `<!-- vale`,
and `<!-- md-dead-link-check`. Every matching comment needs an explanation.

## Advanced

### Configuration

You can configure noqaexplain in `pyproject.toml` (or `.noqaexplain.toml`
in the root of your project, just remove the `[tool.noqaexplain]` section),
for example:

```toml
[tool.noqaexplain]
# include rules by their complete, case-sensitive name
names = ["ENQ0"] # default: all rules included
# whether to exit after first error or all errors
end_mode = "first" # default: "all"

# Extends Python noqas mappings
# Now every # my_noqa_header: will be treated as a noqa comment
# and checked for explanations.
extend_mapping_suffix = {".py" = ["# my_noqa_header:"]}
# Target any MySuperFile.md file(s) and look for explanations
extend_mapping_name = {"MySuperFile.md" = ["# my_noqa_header:"]}
```

> [!TIP]
> Rule-specific configuration can be found in the section below.

### Run as a pre-commit hook

`noqaexplain` can be used as a pre-commit hook, to add as a plugin:

```yaml
repos:
-   repo: "https://github.com/open-nudge/noqaexplain"
    rev: ...  # select the tag or revision you want, or run `pre-commit autoupdate`
    hooks:
    -   id: "noqaexplain"
```

### Rules

> [!TIP]
> Run `noqaexplain rules` to see the list of available rules.

`noqaexplain` provides the following rules:

<!-- pyml disable-num-lines 25 line-length-->

| Name   | Description                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------- |
| `NQE0` | Ensures that all disabled linting rules have an explanation on the nearest preceding nonblank line  |
| `NQE1` | Ensures that all disabled linting rules have an associated explanation of at least <minimal length> |

and the following configurable options (in `pyproject.toml`
or `.noqaexplain.toml`):

<!-- pyml disable-num-lines 10 line-length-->

| Option                  | Description                                                                            | Affected rules | Default  |
| ----------------------- | -------------------------------------------------------------------------------------- | -------------- | -------- |
| `extend_mapping_suffix` | Additional file suffix to noqa comment(s) format mappings (dict of lists)              | __All__        | `{}`     |
| `extend_mapping_name`   | Additional file name to noqas comment(s) format mappings (dict of lists)               | __All__        | `{}`     |
| `mapping_suffix`        | File suffix to noqa comment format(s) mappings (dict of lists, __overrides default!__) | __All__        | `{}`     |
| `mapping_name`          | File name to noqa comment format(s) mappings (dict of lists, __overrides default!__)   | __All__        | `{}`     |
| `min_explain_length`    | Minimum length of explanation for disabled linting rules                               | NQE1           | 10       |
| `explain_noqa_pattern`  | String identifying explanation for disabled linting rule                               | NQE0           | `"enq:"` |

## Contribute

We welcome your contributions! Start here:

- [Code of Conduct](/CODE_OF_CONDUCT.md)
- [Contributing Guide](/CONTRIBUTING.md)
- [Roadmap](/ROADMAP.md)
- [Changelog](/CHANGELOG.md)
- [Report security vulnerabilities](/SECURITY.md)
- [Open an Issue](https://github.com/open-nudge/noqaexplain/issues)

## Legal

- This project is licensed under the _Apache 2.0 License_ - see
    the [LICENSE](/LICENSE.md) file for details.
- This project is copyrighted by _open-nudge_ - the
    appropriate copyright notice is included in each file.

<!-- mkdocs remove end -->

<!-- md-dead-link-check: on -->
