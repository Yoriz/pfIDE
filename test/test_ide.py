import unittest

from pfIDE.editor.gui.main import IDE
from pfIDE.editor.tabs import Tab, EditorTabPanel
from pfIDE.editor.editor import Editor

class TestIde(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ide = IDE(False)
        self.ide.OnInit()

    # Test properties
    @classmethod
    def tearDownClass(self):
        self.ide.Destroy()

    def test_tab_panel(self):
        self.assertTrue(isinstance(self.ide.tab_panel, EditorTabPanel))

    def test_current_tab(self):
        self.assertTrue(isinstance(self.ide.current_tab, Tab))

    def test_current_editor(self):
        self.ide.tab_panel.new_tab("hello")
        self.assertTrue(isinstance(self.ide.current_editor, Editor))
