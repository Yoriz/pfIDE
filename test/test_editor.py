import unittest

from pfIDE.editor.gui.main import IDE

class TestEditor(unittest.TestCase):
    def setUp(self):
        self.ide = IDE(False)
        self.ide.OnInit()

        # An editor to test with
        self.ide.tab_panel.new_tab("hello")
        self.editor = self.ide.current_editor

    def tearDown(self):
        self.ide.Destroy()

    def test_if_indent(self):
        """Test if statement indent"""
        old_indent = self.editor.GetLineIndentation(0)
        self.editor.AddText("if True:")
        self.editor.newline_indent()

        new_indent = self.editor.GetLineIndentation(1)
        self.assertEqual(old_indent + self.editor.GetIndent(), new_indent)

    def test_return_indent(self):
        """Test return statement"""
        self.editor.AddText("if True:")
        self.editor.newline_indent()
        self.editor.AddText("return")

        old_indent = self.editor.GetLineIndentation(1)
        self.editor.newline_indent()
        new_indent = self.editor.GetLineIndentation(2)
        self.assertEqual(old_indent - self.editor.GetIndent(), new_indent)

    def test_false_return_indent(self):
        """Test return statement"""
        self.editor.AddText("if True:")
        self.editor.newline_indent()
        self.editor.AddText("print 'return'")

        old_indent = self.editor.GetLineIndentation(1)
        self.editor.newline_indent()
        new_indent = self.editor.GetLineIndentation(2)
        self.assertEqual(old_indent, new_indent)

    def test_colon_indent(self):
        self.editor.AddText("if:")
        self.editor.newline_indent()

        old_indent = self.editor.GetLineIndentation(1)
        self.editor.AddText("else")
        self.editor.colon_indent()

        new_indent = self.editor.GetLineIndentation(2)
        self.assertEqual(old_indent - self.editor.GetIndent(), new_indent)
