"""
Base class for obfuscation strategies.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from string import Template


class BaseObfuscationStrategy(ABC):  # pragma: no cover
    """
    Abstract base class for obfuscation strategies.

    Logics to handle:
        1. obfuscate method
        2. Template file containing the deobfuscation code
    """

    @abstractmethod
    def obfuscate(self, file_path: Path, **kwargs) -> bytes:
        """
        Obfuscate the given code.

        Note: Ensure you have created the template file too for deobfuscation

        Args:
            file_path: Path to the source code to obfuscate
            **kwargs: Additional arguments for the obfuscation process

        Returns:
            The obfuscated code
        """
        pass

    @property
    @abstractmethod
    def template_path(self) -> Path:
        """
        Template containing the deobfuscation code
        """
        pass

    @property
    @abstractmethod
    def template_vars(self) -> dict:
        """
        Variables to be used in the template
        """
        pass

    def get_runtime_code(self) -> str:
        """
        Get the runtime code
        """
        return generate_runtime(self.template_path, self.template_vars)

    def execute(
        self, obfuscated_code: bytes, just_return_runtime_code: bool = False, **kwargs
    ):
        """
        Execute the obfuscated code.

        Args:
            obfuscated_code: The obfuscated code to execute
            just_return_runtime_code: Returns the runtime code only without executing it (useful for generating the wrapper
                for runtime code)
        """
        execution_string = self.get_runtime_code()

        if just_return_runtime_code:
            return execution_string

        execution_string += f"\nexecute_secure_code({obfuscated_code!r}, globals())"
        return exec(execution_string, globals(), **kwargs)


def generate_runtime(template_path: Path, template_vars: dict) -> str:
    """
    Generate the runtime code needed to deobfuscate and execute the code.

    Args:
        template_path: Path to the template file
        template_vars: Dictionary of template variables

    Returns:
        The runtime code as a string
    """

    try:
        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())

        return template.safe_substitute(template_vars)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Template file not found: {template_path}") from e
