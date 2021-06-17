# Contributing to ARgorithm

![+1](https://github.githubassets.com/images/icons/emoji/unicode/1f44d.png)![tada](https://github.githubassets.com/images/icons/emoji/unicode/1f389.png) First off, thanks for taking the time to contribute! ![tada](https://github.githubassets.com/images/icons/emoji/unicode/1f389.png)![+1](https://github.githubassets.com/images/icons/emoji/unicode/1f44d.png)

The following is a set of guidelines for contributing to ARgorithm Toolkit, which are hosted in the ARgorithm Organization on GitHub. These are mostly guidelines, not rules. Use your best  judgment, and feel free to propose changes to this document in a pull  request.

**Table of contents**

- [Code of Conduct](#code-of-conduct)
- [How do I contribute](#how-can-I-contribute)
- [About ARgorithm](#about-argorithm)
- [Getting started](#getting-started)
- [Issues](#creating-issues)
- [Pull requests](#creating-pull-requests)
- [Contact](#contact)

## Code of conduct

You can read the code of conduct [here](https://github.com/ARgorithm/toolkit/blob/master/CODE_OF_CONDUCT.md)

## How can I contribute

We love your input! There are many ways to be contributor to our project:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## About ARgorithm

You can read more about our project [here](https://argorithm.github.io/)

You can read more about the internal workings of ARgorithm in the [wiki](https://github.com/ARgorithm/toolkit/wiki)

## Getting Started

### Prerequisites

- Python Programming and Packaging
- YAML
- JSON schema
- Testing using PyTest
- Python documentation using mkdocs
- Docker

### Environment setup

For the toolkit, we use a Makefile to make the process simpler

```makefile
init:
	pip install -r requirements.txt
	python setup.py install
	
clean:
	rm -rf ARgorithmToolkit.egg-info/ build/ dist/

lint:
	pylint ARgorithmToolkit
	pylint tests/

test:
	pytest tests

server:
	docker build . -t argorithm-server:local
	docker run --rm -p 80:80 argorithm-server:local

verify:
	python schema.py

dist:
	python setup.py sdist
	python setup.py bdist_wheel

deploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload dist/*

testdeploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload --repository testpypi dist/*

```

Here is a description of commands

| Make command | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| `init`       | Sets up the environment with the requirements                |
| `clean`      | Cleans the build files                                       |
| `lint`       | lints the code files according to repositories `.pylintrc` file |
| `test`       | runs the tests written in the `test/` directory using Pytest |
| `server`     | Starts a local instance of server with which uses your instance of `ARgorithmToolkit ` for server testing |
| `verify`     | Checks if  code is up to date with designs written in`designs/` |
| `dist`       | Creates the python build package for deployment              |

Documentation has its own makefile to use. When making changes to the md files in `docs/docs/` or `mkdocs.yml` or whenever you want to see how the documentation builds as, do the following  

```bash
user@os :toolkit$ cd docs/
user@os :toolkit/docs$ make serve
```

**Writing designs**

Writing designs forms a critical part of our application thus please use the schema provided when writing the `.design.yml` file.
Create an issue for feature request where you suggest an design and get involved with maintainers on the discord server.

**Writing examples**

The examples in the `examples/` directory are for users to understand how ARgorithms can be created. If adding more examples, please ensure the code is readable and visualises some popular algorithm for convenience.

## Creating Issues

Issues are divided into 3 types for simplicity

1. Bug Report ([template](https://github.com/ARgorithm/toolkit/blob/master/.github/ISSUE_TEMPLATE/bug_report.md))
2. Feature Request ([template](https://github.com/ARgorithm/toolkit/blob/master/.github/ISSUE_TEMPLATE/feature_request.md))
3. Question ([template](https://github.com/ARgorithm/toolkit/blob/master/.github/ISSUE_TEMPLATE/question.md))

### Bug report

Before submitting a bug report, [check for similar bug reports](https://github.com/ARgorithm/toolkit/issues?q=is%3Aissue+label%3Abug)

Explain the problem and include additional details to help maintainers reproduce the problem:

- **Use the bug report template**
- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you used ARgorithm, e.g. which command exactly you used in the terminal. When listing steps, **don't just say what you did, but explain how you did it**.
- **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets,  which you use in those examples. If you're providing snippets in the  issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why.**
- **Include screenshots and animated GIFs** which show  you following the described steps and clearly demonstrate the problem.  If you use the keyboard while following the steps, **record the GIF with the [Keybinding Resolver](https://github.com/atom/keybinding-resolver) shown**. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
- **If you're reporting that ARgorithm crashed**, include a crash report with a stack trace.
- **If the problem is related to performance or memory**, include a [CPU profile capture](https://flight-manual.atom.io/hacking-atom/sections/debugging/#diagnose-runtime-performance) with your report.
- **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

- **Did the problem start happening recently** (e.g. after updating to a new version of ARgorithm) or was this always a problem?
- If the problem started happening recently, **can you reproduce the problem in an older version of ARgorithm?** What's the most recent version in which the problem doesn't happen?
- **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.
- If the problem is related to working with files (e.g. opening and editing files), **does the problem happen for all files or only some?**

Include details about your configuration and environment:

- **Which version of ARgorithm are you using?** You can get that by using your python package manager
- **What's the name and version of the OS you're using**?
- **Are you running ARgorithm in a virtual machine?** If so, which VM software are you using and which operating systems and versions are used for the host and the guest?
- **Which packages do you have installed?** You can get that list by running `pip list`.

### Feature request

Before creating enhancement suggestions, please check for [similar already existing requests](https://github.com/ARgorithm/toolkit/issues?q=is%3Aissue+label%3Aenhancement+) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please include as many details as possible. Fill in the template, including the steps that you imagine you would take if the feature you're requesting existed.

- **Use the feature request template**
- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
- **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of Atom which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
- **Explain why this enhancement would be useful** to most ARgorithm users

### Question

Question issues are so that users to ask how to use different features of ARgorithm toolkit

Before creating question issues check for [existing questions](is:issue label:"question" ). Keep the following in mind when creating question issues:

- **Use the question template**
- **Use a clear and descriptive title** for the issue to identify the question
- **Provide a explanation of what you want to do**. Include examples, input/output descriptions etc.
- **Describe your system** to understand your environment better

> You may later mention this question in the discord help channel to get better insights about your problem as well

**Issue tags**

These extra tags can help maintainers and contributors to better resolve issues 

| Tag             | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `documentation` | if changes in documentation are made                         |
| `structure`     | if support for more template class has been added or previous template classes have been fixed |
| `cli`           | if command line interface has been improved                  |
| `base`          | if changes are made in the way intermediate data is generated or structures and states are handled |

## Creating Pull requests

All pull requests should be linked to an issue pertaining to a bug or a feature enhancement, This is important as it prevents duplication of work. Early contributors can find issues to work on that have the [good first issue](https://github.com/ARgorithm/toolkit/issues?q=is%3Aissue+label%3A%22good+first+issue%22+) tag.

We request you to use the [Pull request template](https://github.com/ARgorithm/toolkit/blob/master/.github/PULL_REQUEST_TEMPLATE.md) to

- Maintain ARgorithm Toolkit's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible ARgorithm
- Enable a sustainable system for maintainers to review contributions

## Contact

**Current Maintainers**

- [TheForeverLost](https://github.com/TheForeverLost)
- [YatharthMathur](https://github.com/yatharthmathur)
- [Vin-dictive](https://github.com/Vin-dictive)
- [UtkG07](https://github.com/UtkG07)

Join our discord server to get in touch with us and fellow contributors

[![Discord Server](https://img.shields.io/discord/854962642790383648.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge)](https://discord.gg/W7QPh35snP)
