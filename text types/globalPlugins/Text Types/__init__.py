# Copyright (C) Eduardo Araújo AKA Edu-MX < diaseduardo139@gmail.com
# This file is covered by the GNU General Public License.

import globalPluginHandler
import api
import textInfos
import ui

class Text:
    def __init__(self):
        self.recentText = ''
        self.recentResponse = ''
        self._symbols = '!.,@#$%¨&*()_+-=><\/";'

    def selectedText(self):
        obj=api.getCaretObject()
        try:
            info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
            if info or not info.isCollapsed:
                return info.text
        except (RuntimeError, NotImplementedError):
            return None

    def response(self, text):
        self.recentText = text
        content = text.strip()
        uppercase, lowercase, symbols, numbers = 0, 0, 0, 0
        
        for char in content:
            if char in self._symbols:
                symbols += 1
            elif char.isdigit():
                numbers += 1
            elif char.isalpha():
                if char == char.upper():
                    uppercase += 1
                elif char == char.lower():
                    lowercase += 1
        else: # end loop
            responseText = f'In the text, {len(content)} characters.\n{uppercase} Capital letters.\n{lowercase} Lowercase.\n{symbols} Symbols.\n{numbers} Numbers.'
            self.recentResponse = responseText
            return ui.message(responseText)

text = Text()
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_Char(self, gesture):
        selected = text.selectedText()
        if selected:
            if selected == text.recentText:
                ui.message(text.recentResponse)
            else:
                text.response(selected)
        else:
            ui.message('No text was selected')

    __gestures = {
        'kb:NVDA+W': 'Char'
    }