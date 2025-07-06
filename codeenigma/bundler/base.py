from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class IBundler(ABC):  # pragma: no cover
    """
    Interface for bundling modules into a wheels/extensions.
    """

    @abstractmethod
    def create_wheel(
        self, module_path: Path, output_dir: Optional[Path] = None, **kwargs
    ) -> Path:
        pass

    @abstractmethod
    def create_extension(
        self, module_path: Path, output_dir: Optional[Path] = None, **kwargs
    ) -> Path:
        pass
