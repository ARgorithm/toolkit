![Schema Up to date](https://github.com/ARgorithm/Toolkit/workflows/Schema%20Up%20to%20date/badge.svg) ![Tests](https://github.com/ARgorithm/Toolkit/workflows/Tests/badge.svg)
# ToolKit
Toolkit Package to use to generate your custom algorithms for AR representation

The package is designed to provide an STL like feature to various data structures and algorithms to support state generation for ARgorithm Unity Application to utilise while rendering an algorithm.

### Usage

The repository has a make file for all its major functions :

```bash
$ make init
```
will install all your dependencies

```bash
$ make test
```
Will run tests on code

```bash
$ make dist
```
will create python dist package for pip. This should only be used when package is up for new release

```bash
$ make testdeploy
```
test deployment of built distribution

```bash
$ make deploy
```
deploy package to PyPip. Required setup of PyPip before that

### Contributing Guidelines

1. **ARgorithmToolkit** is the main package that contains all the functionality for the use case
2. **tests** contains tests created for **ARgorithmToolkit** . These tests are designed for Pytest
3. **schemas** contains schemas for the design each individual data structure