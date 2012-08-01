import unittest

from pfIDE.editor.gui.main import IDE

class TestEditor(unittest.TestCase):
    def setUp(self):
        self.ide = IDE(False)
        self.ide.OnInit()

        # An editor to test with
        self.ide.tab_panel.new_tab("hello")
        self.editor = self.ide.editor

    def test_indent(self):
        old_indent = self.editor.GetLineIndentation(0)
        self.editor.AddText("if:")
        self.editor.newline_indent()
        new_indent = self.editor.GetLineIndentation(1)
        self.assertEqual(old_indent + self.editor.GetIndent(), new_indent)

