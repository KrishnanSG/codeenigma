from datetime import datetime
from pathlib import Path
from string import Template

import rich

from codeenigma.extensions.base import IExtension


class ExpiryExtension(IExtension):
    """
    Extension to add code expiry verification to the runtime.

    This extension adds expiry verification to the runtime code, ensuring that the code
    can only be executed before the specified expiry date.
    """

    def __init__(self, expiry_date: datetime):
        self.expiry_date = expiry_date

    def get_code(self) -> str:
        """
        Returns the code for the extension that adds expiry verification.
        """
        rich.print(
            f"[bold blue]Adding expiry verification. The runtime will expire on: {self.expiry_date.strftime('%B %d, %Y %I:%M %p')}[/bold blue]"
        )
        with open(
            Path(__file__).parent / "expiry_code.py.template", encoding="utf-8"
        ) as f:
            expiry_check = Template(f.read())

        return expiry_check.safe_substitute({"expiry_date": repr(self.expiry_date)})
