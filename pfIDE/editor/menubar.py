import wx

ID_OPEN = 5000
ID_SAVE = 5003
ID_SAVE_AS = 5004

class MenuBar(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.parent = parent
        self.file = wx.Menu()
        self.new_tab_event = self.file.Append(wx.ID_NEW, "New", "Create a new tab for editing")
        self.open_tab_event = self.file.Append(wx.ID_OPEN, "Open", "Open a file")
        self.save_tab_event = self.file.Append(wx.ID_SAVE, "Save", "Save the current tab.")
        self.save_as_tab_event = self.file.Append(wx.ID_SAVEAS, "Save as", "Save the current tab as")
        self.quit_event = self.file.Append(wx.ID_EXIT, "Exit", "Exits the Application")
        self.Append(self.file, "File")

        self.parent.Bind(wx.EVT_MENU, self.parent.on_quit, self.quit_event)
        self.parent.Bind(wx.EVT_MENU, self.parent.tab_panel.new_tab, self.new_tab_event)

        def bind_to_editor(event):
            self.parent.Bind(wx.EVT_MENU, self.parent.tab_panel.current_tab.editor.event_manager, event)
        for event in [self.save_as_tab_event, self.save_tab_event, self.open_tab_event]:
            bind_to_editor(event)
