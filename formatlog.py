import sublime
import sublime_plugin
import re
from xml.dom.minidom import *
from os.path import basename
import sys

class FormatlogCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        """
        Enables or disables the 'formatlog' command.
        Command will be disabled if there are currently no text selections and current file is not 'XML' or 'Plain Text'.
        This helps clarify to the user about when the command can be executed, especially useful for UI controls.
        """
        view = self.view
        if view == None:
            return False
        syntax = view.settings().get('syntax')
        language = basename(syntax).replace('.tmLanguage', '').lower() if syntax != None else "plain text"
        return language == "xml" or language == "plain text"

    def run(self, edit):
        """
        Main plugin logic for the 'formatlog' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
                for region in view.sel():
                    if not region.empty():
                        s = view.substr(region).strip()
                        s = self.formatlog(s)
                        view.replace(edit, region, s)
        else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg).strip()
                s = self.formatlog(s)
                view.replace(edit, alltextreg, s)
        view.set_syntax_file("Packages/XML/XML.tmLanguage")

    def formatlog(self, s):
        # convert to utf-8 (makes it a bytearray and we need the b flag in re)
        s = s.encode("utf-8")
        # Strip newlines
        s = s.replace(b'\n', b'')
        s = s.replace(b'\r', b'')
        # Strip pseudo newlines
        s = s.replace(b'[\\n]', b'')
        s = s.replace(b'[\\r]', b'')
        # Remove weird one/two/three character long names
        found_reg = re.compile(b'Soap: [<|>]{2} "\w{0,3}"', re.DOTALL)
        s = re.sub(found_reg, b'Soap: << ""', s)
        # Remove soap code
        found_reg = re.compile(b'"?([a-zA-Z0-9\:\,\s\.]*)(\[[a-zA-Z0-9]+\])?[ |]?Soap: [<|>]{2} "', re.DOTALL)
        s = re.sub(found_reg, b'',s)
        # XML Header
        xmlheader = re.compile(b"<\?.*\?>").match(s)
        # convert to plain string without indents and spaces
        s = re.compile(b'>\s+([^\s])', re.DOTALL).sub(b'>\g<1>', s)
        # replace tags to convince minidom process cdata as text
        s = s.replace(b'<![CDATA[', b'%CDATAESTART%').replace(b']]>', b'%CDATAEEND%')
        # Ends with a quotation mark? Remove it
        if s.endswith(b'"'):
            s = s[:-1]
        # Starts with a quotation mark? Remove it
        if s.startswith(b'"'):
            s = s[1:]
        # Doesn't end with a bracket (>)? Add it
        if not s.endswith(b'>'):
            s += b'>'
        # Doesn't start with a bracket(<)? Add it
        if not s.startswith(b'<'):
            s = b'<' + s
        # Check if a namespace is used and see if a namespace declaration is given
        namespace = re.compile(b'\w*:\w*')
        if namespace.search(s) is not None:
            # Check if namespace (xmlns) is defined
            namespace = re.compile(b'xmlns:\w*=')
            if namespace.search(s) is None:
                # Add a fallback namespace
                fallbackNamespace = b' xmlns:soap="http://www.w3.org/2001/12/soap-envelope"'
                index = s.index(b":")
                # First part until the :
                firstPart = s[0:index]
                # Second part with :
                lastPart = s[index:]
                # Now find the first >
                index = lastPart.index(b">")
                # Add the fallback right beforethe >
                middlePart = lastPart[0:index] + fallbackNamespace
                # Update the lastpart
                lastPart = lastPart[index:]
                # Restructure s with firstPart, middlePart (with NS) and lastPart
                s = firstPart + middlePart + lastPart
        try:
            s = parseString(s).toprettyxml()
        except Exception as e:
            sublime.error_message(str(e))
            return s.decode("utf-8")
        # remove line breaks
        s = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL).sub('>\g<1></', s)
        # restore cdata
        s = s.replace('%CDATAESTART%', '<![CDATA[').replace('%CDATAEEND%', ']]>')
        # remove xml header
        s = s.replace("<?xml version=\"1.0\" ?>", "").strip()
        if xmlheader:
                s = xmlheader.group().decode("utf-8") + "\n" + s
        return s
