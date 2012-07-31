import os
import wx.stc

from pfIDE.editor.menubar import ID_SAVE, ID_SAVE_AS
from pfIDE.editor.textutils import split_comments

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
        self.filename = ""
        self.dirname = ""
        self.indent_level = 0
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces) #set mono spacing here!
        self.set_styles()

        # Handle input so smart_indent can be implemented
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def load_configuration(self):
        """Apply all configuration settings"""
        config = wx.GetApp().config
        self.SetTabWidth(config.getint('editing', 'indent'))
        self.SetIndent(config.getint('editing', 'indent'))
        self.SetUseTabs(config.getboolean('editing', 'usetab'))

    def colon_indent(self):
        self.AddText(":")

        for keyword in ["else", "elif", "except", "finally"]:
            current_line_no = self.GetCurrentLine()
            (current_line, _) = self.GetCurLine()
            #if keyword in current_line:
            if current_line.lstrip().startswith(keyword):
                previous_line_no = max([0, current_line_no - 1])
                previous_indent = self.GetLineIndentation(previous_line_no)
                new_indent = previous_indent - self.GetIndent()
                self.SetLineIndentation(current_line_no, new_indent)

    def newline_indent(self):
        """Handles smart indentation for the editor when a newline is pressed"""
        # Read settings from the config file

        # Determine how to indent
        if self.GetUseTabs():
            indent_amount = self.GetTabWidth()
            indent = "\t"
        else:
            indent_amount = self.GetIndent()
            indent = indent_amount * " "

        self.GetCurrentLine()
        cursorpos = self.GetColumn(self.GetCurrentPos())
        last_line_no = self.GetCurrentLine()
        #previous_line, cursorpos = self.GetCurLine()
        last_line = split_comments(self.GetLine(last_line_no))[0]
        indent_level = self.GetLineIndentation(last_line_no) // indent_amount

        # Should we increase or decrease the indent level
        colonpos = last_line.find(":")
        if colonpos >= 0 and cursorpos > colonpos:
            indent_level += 1
        else:
            # Unindent after certain keywords
            for token in ["return", "break", "yield", "continue", "pass", "raise", "yield"]:
                tokenpos = last_line.find(token)
                if tokenpos >= 0 and cursorpos >= tokenpos + len(token):
                    indent_level = max([indent_level - 1, 0])

        # Perform the actual smartindent
        self.NewLine()
        self.AddText(indent * indent_level)

    def on_key_down(self, event):
        key = event.GetKeyCode()
        control = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()

        if key == wx.WXK_RETURN and not control and not alt:
            self.newline_indent()
        elif shift and key == ord(';'): # ':'
            self.colon_indent()
        else:
            #print key
            #print event.GetUniChar()
            event.Skip()

    def event_manager(self, event):
        """
        Take the event code fired from the MenuBar and process it.
        """
        # event parser
        id = event.GetId()
        if id == ID_SAVE:
            if (not self.filename) or (not self.dirname):
                pass # can't save.
            with open(os.path.join(self.dirname, self.filename), 'w') as output:
                output.write(self.GetTextRaw())
        elif id == ID_SAVE_AS:
            save_dialog = wx.FileDialog(self, "Choose a file", "", "", "*.*", wx.SAVE)
            if save_dialog.ShowModal() == wx.ID_OK:
                self.filename = save_dialog.GetFilename()
                self.dirname = save_dialog.GetDirectory()
                with open(os.path.join(self.dirname, self.filename),'w') as output:
                    output.write(self.GetTextRaw())
                open(os.path.join(self.dirname, self.filename)).read()
            save_dialog.Destroy()

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
