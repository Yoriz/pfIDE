import sys
import wx
from pfIDE.editor.interpreter import StdoutTab, StdoutTabPanel
from pfIDE.editor.tabs import EditorTabPanel
from pfIDE.editor.menubar import MenuBar
from pfIDE.editor.config import config

from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor
from twisted.python import log

class MySplitter(wx.SplitterWindow):
    def __init__(self, parent, ID, log):
        wx.SplitterWindow.__init__(self, parent, ID)
        self.log = log
        wx.EVT_SPLITTER_SASH_POS_CHANGED(self, self.GetId(), self.OnSashChanged)
        wx.EVT_SPLITTER_SASH_POS_CHANGING(self, self.GetId(), self.OnSashChanging)

    def OnSashChanged(self, evt):
        self.log.WriteText("sash changed to %s\n" % str(evt.GetSashPosition()))
        # Uncomment this to not allow the change.
        #evt.SetSashPosition(-1)

    def OnSashChanging(self, evt):
        self.log.WriteText("sash changing to %s\n" % str(evt.GetSashPosition()))
        # Uncomment this to not allow the change.
        #evt.SetSashPosition(-1)

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
          - The stdout_tab_panel (containing notebook)
          - The menu bar
          - The status bar
        """
        super(IDEFrame, self).__init__(*args, **kwargs)
        self.splitter = MySplitter(self, -1, log)
        self.editor_tab_panel = EditorTabPanel(self.splitter, -1) # For the editors
        self.stdout_tab_panel = StdoutTabPanel(self.splitter, -1) # For the stdout.

        self.splitter.SetMinimumPaneSize(20)
        self.splitter.SplitHorizontally(self.editor_tab_panel, self.stdout_tab_panel, 100)
        #self.splitter.Initialize(self.editor_tab_panel)

        self.CreateStatusBar()

        self.menu_bar = MenuBar(self)
        self.SetMenuBar(self.menu_bar)

        self.SetInitialSize((800,600)) #TODO: Attach Config

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.editor_tab_panel, 1, wx.EXPAND)
        self.sizer.Add(self.stdout_tab_panel, 2, wx.EXPAND)
        self.SetSizer(self.sizer)

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        #TODO: Construct and wire up the toolbar

    def on_quit(self, event):
        self.Destroy()

class IDE(wx.App):
    """
    The application that wraps the wx.Frame and provides it to the user.
    """
    def __init__(self, *args, **kwargs):
        log.startLogging(sys.stdout)
        self.logger = log
        self.config = config.read_config()
        self.reactor = reactor
        self.reactor.registerWxApp(self)
        wx.App.__init__(self, *args, **kwargs)
        self.logger.msg("wxAPP Initialized")

    def OnInit(self):
        """
        Construct the frame, show it and finish initializing.
        """
        self.frame = IDEFrame(None)
        self.frame.Show()
        return True

    def OnExit(self):
        """
        Called when the App closes down.
        """

    @property
    def tab_panel(self):
        return self.frame.editor_tab_panel

    @property
    def current_tab(self):
        return self.tab_panel.current_tab

    @property
    def current_editor(self):
        return self.current_tab.editor
