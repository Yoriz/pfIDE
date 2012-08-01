from twisted.internet.protocol import ProcessProtocol
import wx.lib.agw.flatnotebook as fnb
import wx

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
        self.frame = frame
        
    def connectionMade(self):
        self.logger.info("Connected to Python.")

    def connectionLost(self, reason):
        self.logger.warn("Connection to process lost with reason %s" % reason)
        self.frame.Newline()
        self.frame.WriteText("\n\nExited with code 0")
    
    def outReceived(self, data):
        self.logger.info("Got stdout.")
        self.frame.WriteText(data)
    
    def errReceived(self, data):
        self.logger.warn("Stderr received: %s" % data)
        self.frame.Newline()
        self.frame.BeginTextColour("Red")
        self.frame.WriteText(data)                
        
    def errConnectionLost(self):
        self.logger.warn("errConnectionLost, The child closed their stderr.")

    def processEnded(self, reason):
        self.logger.warn("processEnded, status %d" % (reason.value.exitCode,))

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
                                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
            pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)

    def run_script(self, source):
        pass

class StdoutTab(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(StdoutTab, self).__init__(*args, **kwargs)
        self.parent = parent
