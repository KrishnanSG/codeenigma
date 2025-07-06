# pragma: no cover
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("codeenigma")
except PackageNotFoundError:
    try:
        import tomllib

        with open("pyproject.toml", "rb") as f:
            content = tomllib.load(f)
            __version__ = content["tool"]["poetry"]["version"]
    except FileNotFoundError:
        __version__ = "undefined"

__all__ = ["__version__"]
