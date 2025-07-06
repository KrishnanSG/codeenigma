from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

from codeenigma.bundler import IBundler
from codeenigma.extensions.base import IExtension
from codeenigma.strategies.base import BaseObfuscationStrategy


class IRuntimeBuilder(ABC):  # pragma: no cover
    """
    Interface for runtime builder

    Logics to handle:
        1. Call the obfuscation strategy to get the runtime code
        2. Call extensions to append additional code (the runtimes can decide whether to append or not)
        3. Build the runtime
    """

    def __init__(
        self,
        strategy: BaseObfuscationStrategy,
        bundler: IBundler,
        extensions: Optional[Sequence[IExtension]] = None,
    ):
        self.strategy = strategy
        self.bundler = bundler
        self.extensions = extensions

    @abstractmethod
    def build(self, output_dir: Path):
        pass
