from unittest import TestCase


class TestOcGull(TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
