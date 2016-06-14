# DisCODe runner

[![Build Status](https://travis-ci.org/qiubix/DisCODeRunner.svg?branch=master)](https://travis-ci.org/qiubix/DisCODeRunner)
[![Coverage Status](https://coveralls.io/repos/github/qiubix/DisCODeRunner/badge.svg?branch=master)](https://coveralls.io/github/qiubix/DisCODeRunner?branch=master)

Framework for testing DisCODe components at runtime.

## Installation
To install just run:
`python setup.py install`

If you need to install this library locally, run:
`python setup.py install --user`

## Usage
In order to use this library, you need to import `discoderunner` package:

`>>> import discoderunner`

`>>> tester = discoderunner.ComponentTester()`

or:

`>>> from discoderunner import ComponentTester`

`>>> tester = ComponentTester()`

