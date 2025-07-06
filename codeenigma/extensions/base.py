from abc import ABC, abstractmethod


class IExtension(ABC):  # pragma: no cover
    """
    Interface for extensions to the runtime code.

    They are used to add additional functionality to the runtime code. They will be used in the runtime builder to prepare the final runtime.
    Extensions can add additional functions or the functions created can be called to either prepare or verify.

    Typical usage:
        * License verification
        * Expiry verification
        * Machine ID verification
        * Enforcing file or module level restrictions
    """

    @abstractmethod
    def get_code(self, **kwargs) -> str:
        """
        Returns the code for the extension
        """
        pass
