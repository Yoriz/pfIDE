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
        """Test autocompletion module name"""
        suggestions = self.autocomplete.suggest("m")
        self.assertIn("math", suggestions)

    def test_suggest2(self):
        """Test autocompleting function name"""
        suggestions = self.autocomplete.suggest("s")
        self.assertIn("sin", suggestions)

    def test_suggest3(self):
        """Only autocomplete incomplete keywords"""
        suggestions = self.autocomplete.suggest("sin")
        self.assertNotIn("sin", suggestions)

    def test_case_insensitive(self):
        """Test whether autocomplete is case sensitive"""
        suggestions = self.autocomplete.suggest("MaT")
        self.assertIn("math", suggestions)

    def test_interactive(self):
        """A more interative unit test"""
        for char in "mat":
            self.autocomplete.update_key(char)
        suggestions = self.autocomplete.suggest()
        self.assertIn("math", suggestions)

    def test_back(self):
        """Removing chars"""
        for char in "matXX":
            self.autocomplete.update_key(char)
        self.autocomplete.back()
        self.autocomplete.back()
        suggestions = self.autocomplete.suggest()
        self.assertIn("math", suggestions)

    def test_clear(self):
        for char in "mathematicals":
            self.autocomplete.update_key(char)
        self.clear()
        suggestions = self.autocomplete.suggest()
        self.assertIn("math", suggestions)

