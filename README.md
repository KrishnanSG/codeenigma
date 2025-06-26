# PyCodeEnigma

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A Python package for code obfuscation using AES-256 and Base64 encryption. PyCodeEnigma helps protect your Python code by encrypting it while maintaining its functionality.

## Features

- 🔒 Strong encryption using AES-256
- 🔄 Simple API for obfuscating and deobfuscating code
- 🔑 Secure key generation and management
- 🛠️ Command-line interface for easy integration into build processes
- 📦 Lightweight and dependency-minimal

## Installation

Using Poetry:

```bash
poetry add pycodeenigma
```

Using pip:

```bash
pip install pycodeenigma
```

## Usage

### Basic Usage

```python
from pycodeenigma import (
    generate_key,
    obfuscate_code,
    deobfuscate_code,
    save_key,
    load_key
)

# Generate a secure key
password = b"your-strong-password"
key = generate_key(password)

# Save the key for later use
save_key(key, "secret.key")

# Later, load the key
key = load_key("secret.key")


# Your Python code
code = """
def hello():
    print("Hello, World!")
"""

# Obfuscate the code
obfuscated = obfuscate_code(code, key)
print(f"Obfuscated code: {obfuscated}")

# Deobfuscate the code
deobfuscated = deobfuscate_code(obfuscated, key)
print(f"Deobfuscated code: {deobfuscated}")
```

### Command Line Interface

PyCodeEnigma comes with a user-friendly command-line interface powered by Typer. The CLI provides helpful prompts and rich output.

#### Generate a new encryption key

```bash
pycodeenigma generate-key --password "your-strong-password" --output secret.key
```

You'll be prompted to enter the password if not provided:

```bash
pycodeenigma generate-key --output secret.key
```

#### Obfuscate a Python file

```bash
pycodeenigma obfuscate my_script.py --key secret.key --output obfuscated_script.py
```

With optional author metadata:

```bash
pycodeenigma obfuscate my_script.py --key secret.key --author "John Doe" --output obfuscated_script.py
```

#### Deobfuscate a file

```bash
pycodeenigma deobfuscate obfuscated_script.py --key secret.key --output deobfuscated_script.py
```

#### Using stdin/stdout

You can use `-` for stdin/stdout:

```bash
# Obfuscate from stdin to stdout
cat script.py | pycodeenigma obfuscate - --key secret.key

# Deobfuscate from stdin to file
cat obfuscated.py | pycodeenigma deobfuscate - --key secret.key --output deobfuscated.py
```

#### Getting Help

For a list of all available commands and options:

```bash
pycodeenigma --help
```

For help on a specific command:

```bash
pycodeenigma obfuscate --help
pycodeenigma deobfuscate --help
pycodeenigma generate-key --help
```

## Security Notes

- The security of your obfuscated code depends on keeping the encryption key secure.
- Obfuscation is not a substitute for proper security practices.
- Always use strong, unique passwords for key generation.
- Keep your encryption keys secure and never commit them to version control.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ using Python
- Uses [cryptography](https://cryptography.io/) for secure encryption