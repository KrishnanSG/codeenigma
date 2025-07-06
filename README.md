# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/KrishnanSG/codeenigma/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------- | -------: | -------: | ------: | --------: |
| codeenigma/bundler/base.py           |        3 |        0 |    100% |           |
| codeenigma/bundler/poetry.py         |       56 |       11 |     80% |25, 34-35, 66, 71, 82-85, 97-99 |
| codeenigma/bundler/standard.py       |        7 |        0 |    100% |           |
| codeenigma/cli.py                    |       58 |       16 |     72% |70-73, 76-79, 84-88, 91-94, 110, 114-121, 131 |
| codeenigma/extensions/base.py        |        1 |        0 |    100% |           |
| codeenigma/extensions/expiry.py      |       13 |        0 |    100% |           |
| codeenigma/orchestrator.py           |       60 |       11 |     82% |75-77, 83-84, 95-101, 117, 120-121 |
| codeenigma/private.py                |        4 |        0 |    100% |           |
| codeenigma/runtime/base.py           |        7 |        0 |    100% |           |
| codeenigma/runtime/cython/builder.py |       65 |        2 |     97% |   101-102 |
| codeenigma/strategies/base.py        |       10 |        2 |     80% |     94-95 |
| codeenigma/strategies/encryption.py  |       25 |        0 |    100% |           |
|                            **TOTAL** |  **309** |   **42** | **86%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/KrishnanSG/codeenigma/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/KrishnanSG/codeenigma/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/KrishnanSG/codeenigma/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/KrishnanSG/codeenigma/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FKrishnanSG%2Fcodeenigma%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/KrishnanSG/codeenigma/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.