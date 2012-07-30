import wx.stc

class Editor(wx.stc.StyledTextCtrl):
    """
    The editor represents the actual StyledTextCtrl and all event handling on the Text level
    should be done here.
    """
    def __init__(self, *args, **kwargs):
        super(Editor, self).__init__(*args, **kwargs)

    def event_manager(self, event):
        print event.GetId()