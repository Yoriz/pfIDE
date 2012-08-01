import unittest

from pfIDE.editor.autocomplete import CodeCompletion

class TestCodeCompletion(unittest.TestCase):
    def setUp(self):
        self.autocomplete = CodeCompletion()
        import math
        self.autocomplete.add_module(math)

    # Test properties
    def tearDown(self):
        pass

    def test_suggest(self):
        suggestions = self.autocomplete.suggest("m")
        self.assertIn("math", suggestions)

    def test_suggest2(self):
        suggestions = self.autocomplete.suggest("s")
        self.assertIn("sin", suggestions)
        # TODO: maybe it should only suggest "sin" if I enter math.sin

    def test_clear(self):
        for char in "math":
            self.autocomplete.update_key(char)
        suggestions = self.autocomplete.suggest()
        self.assertIn("math", suggestions)

