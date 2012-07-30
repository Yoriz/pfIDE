import wx.aui
import wx
import wx.lib.agw.flatnotebook as fnb

from .editor import Editor

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


class TabPanel(wx.Panel):
    """
    The TabPanel handles the Notebook, it tries to keep it sized correctly.
    It is just for display, it should not become an API to the Notebook.
    """
    def __init__(self, *args, **kwargs):
        super(TabPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.notebook = fnb.FlatNotebook(self, agwStyle=fnb.FNB_X_ON_TAB |
                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
                                        pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)
        self.current_tab = None

    def new_tab(self):
        """Create and add a new tab to the notebook."""
        tab = Tab(self)
        self.notebook.AddPage(tab, "untitled")
        self.current_tab = tab
        wx.CallAfter(self.notebook.SetSelection, self.notebook.GetPageCount() - 1)
