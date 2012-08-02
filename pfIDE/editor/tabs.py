import wx.aui
import wx
import wx.lib.agw.flatnotebook as fnb
import os.path
from pfIDE.editor import const

from pfIDE.editor.editor import Editor
from pfIDE.editor.config.config import get_config_filename

class Tab(wx.Panel):
    """
    Tab is the Panel that is eventually added to the Notebook in TabPanel
    Tab contains the editor and is really only here for sizing uses at the moment.
    Keep file code OUT of this object.
    """
    def __init__(self, parent, *args, **kwargs):
        super(Tab, self).__init__(parent,*args, **kwargs)
        self.parent = parent
        self.editor = Editor(self)
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)
        self.sizer.Add(self.editor, 1, wx.EXPAND | wx.ALL, 0)


class EditorTabPanel(wx.Panel):
    """
    The TabPanel handles the Notebook, it tries to keep it sized correctly.
    It is just for display, it should not become an API to the Notebook.
    """
    def __init__(self, *args, **kwargs):
        super(EditorTabPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.logger = wx.GetApp().logger
        self.SetSizer(self.sizer)
        self.notebook = fnb.FlatNotebook(self, agwStyle=fnb.FNB_X_ON_TAB |
                                        fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
                                        pos=(-100, -100))
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)
        self.new_tab(None) #TODO: Should open last tab

    def new_tab(self, event, tab_name="untitled"):
        """Create and add a new tab to the notebook."""
        tab = Tab(self)
        self.notebook.AddPage(tab, tab_name)
        self.current_tab = tab
        wx.CallAfter(self.notebook.SetSelection, self.notebook.GetPageCount() - 1)

    def open_tab(self, event):
        """Opens file chosen by user"""
        open_dialog = wx.FileDialog(self, "Choose a file", "", "", "*.*", wx.OPEN)
        if open_dialog.ShowModal() == wx.ID_OK:
            filename = open_dialog.GetFilename()
            dirname = open_dialog.GetDirectory()
            filepath = os.path.join(dirname, filename)
            self.open_file(filepath)
            open_dialog.Destroy()

    def edit_config(self, event):
        """Opens the user configuration in a tab"""
        self.open_file(get_config_filename())

    def open_file(self, filepath):
        """Create a tab to edit filename"""
        filename = os.path.basename(filepath)
        self.new_tab(None, tab_name=filename)
        with open(filepath,'r') as input:
            self.current_tab.editor.SetText(input.read())

    def event_manager(self, event):
        """
        Take the event code fired from the MenuBar and process it.
        """
        id = event.GetId()
        self.logger.msg("Got event with id %s" % id)
        if id == wx.ID_SAVE:
            self.logger.msg("Saving current tab.")
            if not all((self.current_tab.editor.filename, self.current_tab.editor.dirname)):
                self.logger.msg("Cannot call save on an unsaved file.")
                return
            with open(os.path.join(self.current_tab.editor.dirname, self.current_tab.editor.filename), 'w') as output:
                self.logger.msg("File handle open, trying to save.")
                output.write(self.current_tab.editor.GetTextRaw())
            self.logger.msg("File handle closed, save successful")
        elif id == wx.ID_SAVEAS:
            self.current_tab.editor.save_as()
        elif id == const.ID_RUN:
            self.current_tab.editor.run()
