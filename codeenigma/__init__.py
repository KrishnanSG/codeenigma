from importlib.metadata import PackageNotFoundError, version

try:
    import tomllib

    with open("pyproject.toml", "rb") as f:
        content = tomllib.load(f)
        __version__ = content["tool"]["poetry"]["version"]
except FileNotFoundError:
    try:
        __version__ = version("codeenigma")
    except PackageNotFoundError:
        __version__ = "undefined"
