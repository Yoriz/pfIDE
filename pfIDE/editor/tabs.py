import wx.aui
import wx
import wx.lib.agw.flatnotebook as fnb

from pfIDE.editor.editor import Editor

class TabPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(TabPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.notebook = fnb.FlatNotebook(self, agwStyle=fnb.FNB_X_ON_TAB |
                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
                                        pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)


class Tab(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(Tab, self).__init__(parent,*args, **kwargs)
        self.parent = parent
        self.text_editor = Editor(self)
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)
        self.sizer.Add(self.text_editor, 1, wx.EXPAND | wx.ALL, 0)



