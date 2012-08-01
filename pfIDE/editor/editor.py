import os
import wx.stc
from pfIDE.editor import const

from pfIDE.editor.textutils import split_comments

from autocomplete import CodeCompletion

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
        self.autocomp = CodeCompletion()

        # Handle input so smart_indent can be implemented
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        # Handle character input for AutoComp
        self.Bind(wx.EVT_CHAR, self.on_evt_char)

    def load_configuration(self):
        """Apply all configuration settings"""
        config = wx.GetApp().config
        self.SetTabWidth(config.getint('editing', 'indent'))
        self.SetIndent(config.getint('editing', 'indent'))
        self.SetUseTabs(config.getboolean('editing', 'usetab'))

    def colon_indent(self):

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
        if 0 <= colonpos < cursorpos:
            indent_level += 1
        else:
            # Unindent after certain keywords
            for token in ["return", "break", "yield", "continue", "pass", "raise"]:
                tokenpos = last_line.find(token)
                if tokenpos >= 0 and cursorpos >= tokenpos + len(token):
                    indent_level = max([indent_level - 1, 0])

        # Perform the actual smartindent
        self.NewLine()
        self.AddText(indent * indent_level)

    def on_key_down(self, event):
        """This function should only handle key presses which cannot be
        handled by on_evt_char.
        Eg, newline, backspace.
        """
        key = event.GetKeyCode()
        control = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()

        # If the AutoComplete menu is showing, hitting return merely
        # closes it and autocompletes; we shouldn't indent in this case.
        autocomp_showing = self.AutoCompActive()

        if key == wx.WXK_RETURN and not control and not alt and not autocomp_showing:
            # order of these calls is important
            self.code_complete(event)
            event.Skip(False)   # prevent character from being printed
                                # other than in newline_indent()
            self.newline_indent()
        elif key == wx.WXK_BACK and not control and not alt:
            self.code_complete(event)
        else:
            event.Skip()

    def on_evt_char(self, event):
        """This should handle most key presses, as the event passed to this
        function allows us to more accurately determine what the character is.
        """
        key = event.GetKeyCode()
        char = chr(event.GetUniChar())
        ctrl = event.ControlDown()
        alt = event.AltDown()
        autocomp_showing = self.AutoCompActive()

        if char == ':':
            self.colon_indent()

        self.code_complete(event)

    def event_manager(self, event):
        """
        Take the event code fired from the MenuBar and process it.
        """
        # event parser
        id = event.GetId()
        if id == wx.ID_SAVE:
            if (not self.filename) or (not self.dirname):
                pass # can't save.
            with open(os.path.join(self.dirname, self.filename), 'w') as output:
                output.write(self.GetTextRaw())
        elif id == wx.ID_SAVEAS:
            save_dialog = wx.FileDialog(self, "Choose a file", "", "", "*.*", wx.SAVE)
            if save_dialog.ShowModal() == wx.ID_OK:
                self.filename = save_dialog.GetFilename()
                self.dirname = save_dialog.GetDirectory()
                with open(os.path.join(self.dirname, self.filename),'w') as output:
                    output.write(self.GetTextRaw())
                open(os.path.join(self.dirname, self.filename)).read()
            save_dialog.Destroy()

            # Ugh. Hack
            root = wx.GetApp().frame
            root.tab_panel.notebook.SetPageText(root.tab_panel.notebook.GetSelection()-1, self.filename)

        elif id == const.ID_RUN:
            reactor = wx.GetApp().reactor
            # is the current file saved?
            if not any((self.dirname, self.filename)):
                pass

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

    def code_complete(self, event):
        """TODO:
        - Properly handle uppercase; the current implementation ignores
          caps lock.
        """
        if event.GetKeyCode() == wx.WXK_BACK:
            self.autocomp.back()
        else:
            try:
                # this isn't perfect, doesn't handle caps lock
                #if event.ShiftDown():
                #    ch = chr(event.GetUniChar())
                #else:
                #    ch = chr(event.GetUniChar()).lower()
                ch = chr(event.GetUniChar())
                self.autocomp.update_key(ch)
            except ValueError:
                self.autocomp.clear()
                return
        choices = list(self.autocomp.suggest())
        if choices:
            choices.sort()
            self.AutoCompShow(self.autocomp.len_entered-1, ' '.join(choices))
        # Skip the event so the character will be printed.
        event.Skip()
