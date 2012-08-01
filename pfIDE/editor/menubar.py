import wx
import const

class MenuBar(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.parent = parent

        self.file = wx.Menu()
        self.new_tab_event = self.file.Append(wx.ID_NEW, "New", "Create a new tab for editing.")
        self.open_tab_event = self.file.Append(wx.ID_OPEN, "Open", "Open a file.")
        self.save_tab_event = self.file.Append(wx.ID_SAVE, "Save", "Save the current tab.")
        self.save_as_tab_event = self.file.Append(wx.ID_SAVEAS, "Save as", "Save the current tab as.")
        self.quit_event = self.file.Append(wx.ID_EXIT, "Exit", "Exits the Application.")
        self.Append(self.file, "&File")

        self.run = wx.Menu()
        self.run_script_event = self.run.Append(const.ID_RUN, "Run Script", "Run the current script.")
        self.Append(self.run, "&Run")

        # quit is bound to IDEFrame
        self.parent.Bind(wx.EVT_MENU, self.parent.on_quit, self.quit_event)

        # new tab and open are bound to TabPanel which manages notebook
        self.parent.Bind(wx.EVT_MENU, self.parent.editor_tab_panel.new_tab, self.new_tab_event)
        self.parent.Bind(wx.EVT_MENU,self.parent.editor_tab_panel.open_tab, self.open_tab_event)

        # These changes relate directly to the editors, they are bound there.
        def bind_to_editor(event):
            self.parent.Bind(wx.EVT_MENU, self.parent.editor_tab_panel.current_tab.editor.event_manager, event)
        for event in [self.save_as_tab_event, self.save_tab_event, self.run_script_event]:
            bind_to_editor(event)

