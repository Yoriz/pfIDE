import wx.stc

class Editor(wx.stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        super(Editor, self).__init__(*args, **kwargs)
