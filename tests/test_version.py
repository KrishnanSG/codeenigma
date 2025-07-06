from unittest import TestCase


class TestVersion(TestCase):  # pragma: no cover
    def test_version(self):
        from codeenigma import __version__

        self.assertIsNotNone(__version__)
