from abc import ABC, abstractmethod
from pathlib import Path

from codeenigma.bundler import IBundler
from codeenigma.strategies.base import BaseObfuscationStrategy


class IRuntimeBuilder(ABC):
    """
    Interface for runtime builder

    Logics to handle:
        1. Call the obfuscation strategy to get the runtime code
        2. Build the runtime
    """

    def __init__(self, strategy: BaseObfuscationStrategy, bundler: IBundler):
        self.strategy = strategy
        self.bundler = bundler

    @abstractmethod
    def build(self, output_dir: Path):
        pass
