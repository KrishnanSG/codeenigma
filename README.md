# CodeEnigma

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

CodeEnigma is a Python package for lightweight code obfuscation using AES-256 encryption and Base64 encoding. It helps protect your Python code from prying eyes while preserving full functionality.

## 🔒 Why CodeEnigma?
After searching extensively for a free and open-source Python obfuscation tool, I realized that most available options were either paid, closed-source, or opaque in how they worked. I wasn't comfortable letting a black-box tool encrypt my production code without knowing exactly what it was doing — especially when it had access to sensitive logic.

So I built **CodeEnigma** — a transparent, self-contained solution that gives you full control over the obfuscation process, with no hidden logic and no external servers involved.

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