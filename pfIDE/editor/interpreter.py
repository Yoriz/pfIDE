from twisted.internet.protocol import ProcessProtocol
import wx

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

class StdoutPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(StdoutPanel, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.process = PythonProcessProtocol(self)
