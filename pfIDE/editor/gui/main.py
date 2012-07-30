import wx
from pfIDE.editor.tabs import TabPanel, Tab
from pfIDE.editor.menubar import MenuBar

class IDEFrame(wx.Frame):
    """
    The actual frame that handles all the wx.Panels other elements.
    If it gets displayed eventually it will end up here.
    This wx.Frame is also the Parent or eventual grand-daddy of all other wx elements.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the wx.Frame and construct the following elements;
          - The tab_panel (containing notebook)
          - The menu bar
          - The status bar
        """
        super(IDEFrame, self).__init__(*args, **kwargs)
        self.tab_panel = TabPanel(self)
        self.menu_bar = MenuBar(self)
        self.SetMenuBar(self.menu_bar)

        self.CreateStatusBar()

        self.SetInitialSize((800,600)) #TODO: Attach Config

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.tab_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        # for testing
        self.tab_panel.notebook.AddPage(Tab(self.tab_panel), "untitled")

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        #TODO: Construct and wire up the toolbar

    def on_quit(self, event):
        print "Called."
        self.Destroy()

class IDE(wx.App):
    """
    The application that wraps the wx.Frame and provides it to the user.
    """
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        """
        Construct the frame, show it and finish initializing.
        """
        self.frame = IDEFrame(None)
        self.frame.Show()
        return True
