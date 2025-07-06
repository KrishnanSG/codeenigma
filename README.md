![Image](https://raw.githubusercontent.com/KrishnanSG/codeenigma/main/static/logo.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/codeenigma)](https://pypi.org/project/codeenigma/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CodeFactor](https://www.codefactor.io/repository/github/krishnansg/codeenigma/badge)](https://www.codefactor.io/repository/github/krishnansg/codeenigma)
[![Downloads](https://static.pepy.tech/badge/codeenigma)](https://pepy.tech/project/codeenigma)
[![CI](https://github.com/KrishnanSG/codeenigma/actions/workflows/main.yml/badge.svg)](https://github.com/KrishnanSG/codeenigma/actions)
[![Coverage](https://raw.githubusercontent.com/KrishnanSG/codeenigma/python-coverage-comment-action-data/badge.svg)](https://github.com/KrishnanSG/codeenigma/actions/workflows/python-coverage-comment-action-data.yml)

A lightweight, open-source tool for Python code obfuscation. CodeEnigma helps protect your logic from reverse engineering and unauthorized access, making it secure to distribute your Python applications.

## 🔒 Why CodeEnigma?
After searching extensively for a free and open-source Python obfuscation tool, I realized that most available options were either paid, closed-source, or opaque in how they worked. I wasn't comfortable letting a black-box tool obfuscate my production code without knowing exactly what it was doing — especially when it had access to sensitive logic.

So I built **CodeEnigma** — a transparent, self-contained solution that gives you full control over the obfuscation process, with no hidden logic and no external servers involved. 

This project is inspired by [PyArmor](https://pyarmor.dashingsoft.com/) but with a different approach.

## High Level Architecture

![Image](https://raw.githubusercontent.com/KrishnanSG/codeenigma/main/static/CodeEnigma.HLD.svg)

The working principle of CodeEnigma is simple:
1. The user provides the path to the Python module to obfuscate.
2. CodeEnigma reads the module's source code.
3. An AES-256 key is generated using a secure random number generator and set in `private.py`
4. Obfuscation runs file by file running the following steps:
   * 4.1. Compile using `compile(code, str(file_path), "exec")` 
   * 4.2. Compress the byte code using `zlib.compress(compiled_code)`
   * 4.3. Encode the compressed byte code using `base64.b64encode(compressed_code)`
   * 4.4. Encrypt the encoded byte code using `AESGCM(SECRET_KEY).encrypt(NONCE, obfuscated, associated_data=None)`
   _[refer for more details](codeenigma/core.py)_:
5. CodeEnigma creates a new module with the obfuscated code.
6. A codeenigma_runtime.pyx file is created with the deobfuscation logic to decrypt and execute the obfuscated code.
7. The runtime is compiled to a Python extension module using Cython. Also generates a codeenigma_runtime.whl file for distribution.
8. End of process, the obfuscated module is ready to be distributed as wheel files.

## Features

- 🔒 Strong encryption using AES-256
- 🔄 Simple API for obfuscating any python module
- 🔑 Secure and dynamic key generation
- 🛠️ Command-line interface for easy integration into build processes
- 📦 Lightweight and dependency-minimal

## Installation

Using Poetry:

```bash
poetry add codeenigma
```

Using pip:

```bash
pip install codeenigma
```

## Usage

CodeEnigma comes with a user-friendly command-line interface powered by Typer. The CLI provides helpful prompts and rich output.

### Basic Usage

To obfuscate a Python module:

```bash
codeenigma obfuscate /path/to/your/module
```

### Command Line Options

- `--expiration`, `-e`: Set an expiration date for the obfuscated code (YYYY-MM-DD)
- `--output`, `-o`, `--dist`: Specify output directory (default: 'dist')
- `--verbose`, `-v`: Show detailed output

#### Examples

Obfuscate with an expiration date:

> _The following example will obfuscate the module and set the expiration date to December 31, 2025, at 23:59:59+0530 (IST)._
```bash
codeenigma obfuscate /path/to/your/module -e "2025-12-31 23:59:59+0530"
```

Specify custom output directory:
```bash
codeenigma obfuscate /path/to/your/module -o custom_output
```

### Version Information

To check the installed version:
```bash
codeenigma version
```

## Contributing

Contributions are welcome! This is a complete free and open-source project. If you have any suggestions or find any bugs, please open an [issue](https://github.com/KrishnanSG/CodeEnigma/issues/new).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ using Python
- Uses [cryptography](https://cryptography.io/) for secure encryption
- Uses [Cython](https://cython.org/) for compiling the runtime
- Logo Credits, Claude 🫡