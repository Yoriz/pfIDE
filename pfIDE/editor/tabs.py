import wx.aui
import wx
import wx.lib.agw.flatnotebook as fnb
import os.path

from pfIDE.editor.editor import Editor

class Tab(wx.Panel):
    """
    Tab is the Panel that is eventually added to the Notebook in TabPanel
    Tab contains the editor and is really only here for sizing uses at the moment.
    Keep file code OUT of this object.
    """
    def __init__(self, parent, *args, **kwargs):
        super(Tab, self).__init__(parent,*args, **kwargs)
        self.parent = parent
        self.editor = Editor(self)
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)
        self.sizer.Add(self.editor, 1, wx.EXPAND | wx.ALL, 0)


class EditorTabPanel(wx.Panel):
    """
    The TabPanel handles the Notebook, it tries to keep it sized correctly.
    It is just for display, it should not become an API to the Notebook.
    """
    def __init__(self, *args, **kwargs):
        super(EditorTabPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.notebook = fnb.FlatNotebook(self, agwStyle=fnb.FNB_X_ON_TAB |
                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
                                        pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)
        self.new_tab(None) #TODO: Should open last tab

    def new_tab(self, event, tab_name="untitled"):
        """Create and add a new tab to the notebook."""
        tab = Tab(self)
        self.notebook.AddPage(tab, tab_name)
        self.current_tab = tab
        wx.CallAfter(self.notebook.SetSelection, self.notebook.GetPageCount() - 1)

    def open_tab(self, event):
        open_dialog = wx.FileDialog(self, "Choose a file", "", "", "*.*", wx.OPEN)
        if open_dialog.ShowModal() == wx.ID_OK:
            filename = open_dialog.GetFilename()
            dirname = open_dialog.GetDirectory()
            self.new_tab(None, tab_name=filename)
            with open(os.path.join(dirname, filename),'r') as input:
                self.current_tab.editor.SetText(input.read())
            open_dialog.Destroy()