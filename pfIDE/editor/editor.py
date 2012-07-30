import os
import os.path
import wx.stc

from pfIDE.editor.menubar import ID_OPEN, ID_SAVE, ID_SAVE_AS

faces = { 'times': 'Times',
          'mono' : 'Courier',
          'helv' : 'Helvetica',
          'other': 'new century schoolbook',
          'size' : 12,
          'size2': 10,
          }

class Editor(wx.stc.StyledTextCtrl):
    """
    The editor represents the actual StyledTextCtrl and all event handling on the Text level
    should be done here.
    """
    def __init__(self, parent, *args, **kwargs):
        super(Editor, self).__init__(parent,*args, **kwargs)
        self.load_configuration()
        self.parent = parent # The panel that contains the editor.
        self.filepath = ""
        self.indent_level = 0
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces) #set mono spacing here!
        self.set_styles()

    def load_configuration(self):
        """Apply all configuration settings"""
        config = wx.GetApp().config
        self.SetTabWidth(config.getint('editing', 'indent'))
        self.SetUseTabs(config.getboolean('editing', 'usetab'))
        #print config

    def event_manager(self, event):
        """
        Take the event code fired from the MenuBar and process it.
        """
        # event parser
        id = event.GetId()
        if id == ID_SAVE:
            pass
        elif id == ID_OPEN:
            dirname = ""
            open_dialog = wx.FileDialog(self, "Choose a file", dirname, "", "*.*", wx.OPEN)
            if open_dialog.ShowModal() == wx.ID_OK:
                filename = open_dialog.GetFilename()
                dirname = open_dialog.GetDirectory()
                with open(os.path.join(dirname, filename),'r') as input:
                    self.SetText(input.read())
                open_dialog.Destroy()


    def set_styles(self, lang='python'):
        """"""
        #INDICATOR STYLES FOR ERRORS (self.errorMark)
        self.IndicatorSetStyle(2, wx.stc.STC_INDIC_SQUIGGLE)
        self.IndicatorSetForeground(2, wx.RED)
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)

        # Python styles

        # White space
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        # Comment
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "face:%(mono)s,fore:#007F00,back:#E8FFE8,italic,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, "face:%(mono)s,fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(wx.stc.STC_P_STRING, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(wx.stc.STC_P_WORD, "face:%(mono)s,fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "face:%(mono)s,fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, "face:%(mono)s,fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, "face:%(mono)s,bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "")
        # Comment-blocks
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "face:%(mono)s,fore:#990000,back:#C0C0C0,italic,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "face:%(mono)s,fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
