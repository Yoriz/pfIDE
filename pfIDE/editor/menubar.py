import wx

ID_QUIT = wx.NewId()



class MenuBar(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.parent = parent
        self.file = wx.Menu()
        self.new_tab_event = self.file.Append(wx.ID_NEW, "New Tab", "Opens a new tab for editing")
        self.quit_event = self.file.Append(wx.ID_EXIT, "Exit", "Exits the Application")
        self.Append(self.file, "File")

        self.Bind(wx.EVT_MENU, self.parent.on_quit, self.quit_event)
        self.Bind(wx.EVT_MENU, self.parent.tab_panel.new_tab, self.new_tab_event)

    def on_quit(self):
        self.parent.Close() # wx.Frame in this case
