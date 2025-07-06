import os
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import TestCase

from typer.testing import CliRunner

from codeenigma.cli import app


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

        expiration_date = str((datetime.now(UTC) + timedelta(seconds=5)).isoformat())

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

        self.assertIn("Hello, World!", result.stdout)
        self.assertIn("55", result.stdout)
        self.assertIn("3", result.stdout)
        self.assertIn("6", result.stdout)

        # Check for code expiration
        time.sleep(6)
        result = subprocess.run(
            [sys.executable, str(out_path)],
            capture_output=True,
            cwd=str(Path(__file__).parent / "cedist2"),
            text=True,
            env=env,
        )
        self.assertIn("Code expired on", result.stdout)
        self.assertEqual(result.returncode, 1)
