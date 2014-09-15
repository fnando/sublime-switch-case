import sublime, sublime_plugin, re

def is_camelcase(text):
  return re.match("^([A-Z]+[a-z0-9]+)+$", text)

def is_snake_case(text):
  return re.match("^[a-z]+(_?[a-z0-9]+)*$", text)

def is_scream_snake_case(text):
  return re.match("^[A-Z]+(_?[A-Z0-9]+)*$", text)

def is_hyphenated(text):
  return re.match("^[a-z]+(-?[a-z0-9]+)*$", text)

def convert_to_camelcase(text):
  return "".join(map(lambda w: w[:1].upper() + w[1:].lower(), text.split("-")))

def convert_to_snake_case(text):
  return re.sub("(?<=[a-z])([A-Z])", "_\\1", text).lower()

def convert_to_scream_snake_case(text):
  return "_".join(map(lambda w: w.upper(), text.split("_")))

def convert_to_hyphenated(text):
  return re.sub("_", "-", text)

class SwitchCaseCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    word_region = self.view.word(self.view.sel()[0])
    word = self.view.substr(word_region)

    if is_snake_case(word):
      self.view.replace(edit, word_region, convert_to_hyphenated(word))
    elif is_hyphenated(word):
      self.view.replace(edit, word_region, convert_to_camelcase(word))
    elif is_camelcase(word):
      self.view.replace(edit, word_region, convert_to_scream_snake_case(convert_to_snake_case(word)))
    else:
      self.view.replace(edit, word_region, convert_to_snake_case(word))
