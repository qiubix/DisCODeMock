# DisCODe Test Framework

[![Build Status](https://travis-ci.org/qiubix/DisCODeTestFramework.svg?branch=master)](https://travis-ci.org/qiubix/DisCODeTestFramework)
[![Coverage Status](https://coveralls.io/repos/github/qiubix/DisCODeTestFramework/badge.svg?branch=master)](https://coveralls.io/github/qiubix/DisCODeTestFramework?branch=master)

Framework for testing DisCODe components at runtime.

## Installation
To install just run:
`python setup.py install`

If you need to install this library locally, run:
`python setup.py install --user`

## Usage
In order to use this library, you need to import `discodetestframework` package:

`>>> import discodetestframework`

`>>> tester = discodetestframework.ComponentTester()`

or:

`>>> from discodetestframework import ComponentTester`

`>>> tester = ComponentTester()`

## Running tests

To run tests for this framework:
`python setup.py test`
