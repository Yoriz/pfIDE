import wx

class MenuBar(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.file = wx.Menu()
        self.file.Append(101, "Exit", "Exits the Application")
        self.Bind(wx.EVT_MENU, self.on_quit, id=101)

        self.edit = wx.Menu()
        self.deploy = wx.Menu()
        self.Append(self.file, "File")

    def on_quit(self):
        self.Close()

