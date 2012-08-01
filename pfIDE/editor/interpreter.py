from twisted.internet.protocol import ProcessProtocol
import wx.lib.agw.flatnotebook as fnb
import wx
from wx.richtext import RichTextCtrl

ENABLED = True
import version
if version.is_windows():
    try:
        import win32api
    except ImportError:
        ENABLED = False
        win32api = None

class PythonProcessProtocol(ProcessProtocol):       
    def __init__(self, frame):
        self.logger = wx.GetApp().logger
        self.console = frame.console
        
    def connectionMade(self):
        self.logger.msg("Connected to Python.")

    def connectionLost(self, reason):
        self.logger.err("Connection to process lost with reason %s" % reason)
        self.console.Newline()
        self.console.WriteText("\n\nExited with code 0")
    
    def outReceived(self, data):
        self.logger.msg("Got stdout.")
        self.console.WriteText(data)
    
    def errReceived(self, data):
        self.logger.err("Stderr received: %s" % data)
        self.console.Newline()
        self.console.BeginTextColour("Red")
        self.console.WriteText(data)
        
    def errConnectionLost(self):
        self.logger.msg("The process closed their stderr.")

    def processEnded(self, reason):
        self.logger.msg("Process ended with status %d" % (reason.value.exitCode,))

class StdoutTabPanel(wx.Panel):
    """
    The TabPanel handles the Notebook, it tries to keep it sized correctly.
    It is just for display, it should not become an API to the Notebook.
    """
    def __init__(self, *args, **kwargs):
        super(StdoutTabPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.notebook = fnb.FlatNotebook(self, agwStyle=fnb.FNB_X_ON_TAB |
                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8, pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)

    def run_script(self, args):
        reactor = wx.GetApp().reactor
        panel = StdoutTab(self)
        self.notebook.AddPage(panel, "Python Interpreter.",select=True)
        reactor.spawnProcess(PythonProcessProtocol(panel), version.get_python_exe(), args)

class StdoutTab(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(StdoutTab, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_rich_text_ctrl()

        self.SetSizer(self.sizer)
        self.Layout()

    def _create_rich_text_ctrl(self):
        """Creates the textbox for the console"""
        self.console = RichTextCtrl(self, style=wx.TE_READONLY)
        monospace_font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,
            False, u"Monospace")
        self.console.SetFont(monospace_font)
        self.sizer.Add(self.console, 1, wx.EXPAND | wx.ALL, 1)
