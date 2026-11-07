import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import TestCase

from typer.testing import CliRunner

from codeenigma.cli import app
from codeenigma.extensions import ExpiryExtension


class TestCodeEnigmaCLI(TestCase):  # pragma: no cover
    def setUp(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(app, ["version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CodeEnigma CLI v", result.output)

    def test_obfuscate(self):
        # First run the example module to get expected output
        # Get the path to the example module
        example_module_path = (
            Path(__file__).parent / "example_module" / "example_module"
        )

        # # Now test the obfuscation
        result = self.runner.invoke(
            app, ["obfuscate", str(example_module_path), "-o", "tests/cedist"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Obfuscation completed successfully", result.output)

        out_path = Path(__file__).parent / "cedist" / "example_module" / "main.py"
        cedist_path = str((Path(__file__).parent / "cedist").absolute())
        env = os.environ.copy()
        env["PYTHONPATH"] = cedist_path + os.pathsep + env.get("PYTHONPATH", "")

        result = subprocess.run(
            ["python", str(out_path)],
            capture_output=True,
            cwd=str(Path(__file__).parent / "cedist"),
            text=True,
            env=env,
        )

        # Check that the output contains expected strings
        self.assertIn("Hello World!", result.stdout)
        self.assertIn("This is a test", result.stdout)
        self.assertIn("Hello, World!", result.stdout)
        self.assertIn("55", result.stdout)
        self.assertIn("3", result.stdout)
        self.assertIn("6", result.stdout)

    def test_obfuscate_with_expiration(self):
        example_module_path = (
            Path(__file__).parent / "example_module" / "example_module"
        )

        expiration_date = str((datetime.now(UTC) + timedelta(days=1)).isoformat())

        result = self.runner.invoke(
            app,
            [
                "obfuscate",
                str(example_module_path),
                "-e",
                expiration_date,
                "-o",
                "tests/cedist2",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        out_path = Path(__file__).parent / "cedist2" / "example_module" / "main.py"
        cedist_path = str((Path(__file__).parent / "cedist2").absolute())
        env = os.environ.copy()
        env["PYTHONPATH"] = cedist_path + os.pathsep + env.get("PYTHONPATH", "")

        result = subprocess.run(
            [sys.executable, str(out_path)],
            capture_output=True,
            cwd=str(Path(__file__).parent / "cedist2"),
            text=True,
            env=env,
        )

        self.assertNotIn("Code expired on", result.stdout)
        self.assertIn("Hello, World!", result.stdout)
        self.assertIn("55", result.stdout)
        self.assertIn("3", result.stdout)
        self.assertIn("6", result.stdout)

    def test_expiry_extension_blocks_expired_code(self):
        expiry_extension = ExpiryExtension(datetime.now(UTC) - timedelta(seconds=1))

        with self.assertRaises(SystemExit) as context:
            exec(expiry_extension.get_code(), {})

        self.assertEqual(context.exception.code, 1)
