import sublime, sublime_plugin, re
from . import utils

class SwitchCaseCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    for sel in self.view.sel():
      word_region = self.view.word(sel)
      word = self.view.substr(word_region)

      if kwargs["type"] == "alternate":
        result = utils.alternate(word)
      else:
        result = utils.convert(word, kwargs["type"])

      self.view.replace(edit, word_region, result)
