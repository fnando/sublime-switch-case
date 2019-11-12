import re

def convert(text, case):
  words = to_words(text)

  if case == "hyphenated":
    return "-".join(words)
  elif case == "snake":
    return "_".join(words)
  elif case == "scream_snake":
    return "_".join(map(lambda word: word.upper(), words))
  elif case == "dot":
    return ".".join(words)
  elif case == "space":
    return " ".join(words)
  elif case == "camel":
    return "".join(map(lambda word: word.title(), words))
  elif case == "camel_back":
    result = "".join(map(lambda word: word.title(), words))
    return result[:1].lower() + result[1:]
  elif case == "slash":
    return "/".join(words)
  elif case == "backslash":
    return "\\".join(words)
  elif case == "lower":
    return words[0].lower()
  elif case == "upper":
    return words[0].upper()
  elif case == "title":
    return words[0].title()
  else:
    return text

def to_words(text):
  if re.match(r"^([a-zA-Z][a-z0-9]*|[A-Z]+[A-Z0-9]*)$", text):
    words = [text]
  elif re.match(r"^[a-zA-Z][a-z0-9]*([A-Z][A-Za-z0-9]+)+$", text):
    text = re.sub(r"([A-Z]+|[0-9]+)", "__SWITCH_CASE_SEPARATOR__\\1", text[:1].lower() + text[1:])
    words = re.split(r"__SWITCH_CASE_SEPARATOR__", text)
  elif re.match(r"^[a-z]+[a-z0-9]*([-_. /\\]+[a-z0-9]+)*$", text, flags=re.IGNORECASE):
    words = re.split(r"[-_. /\\]+", text)
  else:
    words = [text]

  return list(map(lambda word: word.lower(), words))

matchers_multiple_words = [
  {"name": "snake", "match": lambda text: re.match(r"^[a-z]+(_[a-z0-9]+)+$", text)},
  {"name": "scream_snake", "match": lambda text: re.match(r"^[A-Z]+(_[A-Z0-9]+)+$", text)},
  {"name": "camel", "match": lambda text: re.match(r"^[A-Z]+[a-z0-9]*([A-Z]+[a-z0-9]+)+$", text)},
  {"name": "camel_back", "match": lambda text: re.match(r"^[a-z]+[a-z0-9]*([A-Z]+[a-z0-9]+)+$", text)},
  {"name": "hyphenated", "match": lambda text: re.match(r"^[a-z]+(-[a-z0-9]+)+$", text, flags=re.IGNORECASE)},
  {"name": "dot", "match": lambda text: re.match(r"^[a-z]+(\.[a-z0-9]+)+$", text, flags=re.IGNORECASE)},
  {"name": "space", "match": lambda text: re.match(r"^[a-z]+( [a-z0-9]+)+$", text, flags=re.IGNORECASE)},
  {"name": "slash", "match": lambda text: re.match(r"^[a-z]+(/[a-z0-9]+)+$", text, flags=re.IGNORECASE)},
  {"name": "backslash", "match": lambda text: re.match(r"^[a-z]+(\\[a-z0-9]+)+$", text, flags=re.IGNORECASE)}
]

matchers_single_word = [
  {"name": "lower", "match": lambda text: re.match(r"^[a-z][a-z0-9]*$", text)},
  {"name": "upper", "match": lambda text: re.match(r"^[A-Z][A-Z0-9]*$", text)},
  {"name": "title", "match": lambda text: re.match(r"^[A-Z][a-z0-9]*$", text)}
]

def alternate(text):
  words = to_words(text)
  matchers = matchers_multiple_words if len(words) > 1 else matchers_single_word
  current_matcher = next(matcher for matcher in matchers if matcher["match"](text))

  if current_matcher:
    index = matchers.index(current_matcher) + 1
    next_matcher = matchers[index if index < len(matchers) else 0]
  else:
    next_matcher = matchers[0]

  return convert(text, next_matcher["name"])

if __name__ == "__main__":
  import unittest

  class TestStringMethods(unittest.TestCase):
    def test_convert_to_words(self):
      self.assertEqual(to_words("this-is-hyphenated-1234"), ["this", "is", "hyphenated", "1234"])
      self.assertEqual(to_words("this"), ["this"])
      self.assertEqual(to_words("This"), ["this"])
      self.assertEqual(to_words("1234"), ["1234"])
      self.assertEqual(to_words("this is spaced 1234"), ["this", "is", "spaced", "1234"])
      self.assertEqual(to_words("this    is  spaced   1234"), ["this", "is", "spaced", "1234"])
      self.assertEqual(to_words("THIS-IS-HYPHENATED-1234"), ["this", "is", "hyphenated", "1234"])
      self.assertEqual(to_words("this_is_snake_case_1234"), ["this", "is", "snake", "case", "1234"])
      self.assertEqual(to_words("THIS_IS_SCREAM_SNAKE_CASE_1234"), ["this", "is", "scream", "snake", "case", "1234"])
      self.assertEqual(to_words("this.is.dot.case.1234"), ["this", "is", "dot", "case", "1234"])
      self.assertEqual(to_words("THIS.IS.DOT.CASE.1234"), ["this", "is", "dot", "case", "1234"])
      self.assertEqual(to_words("ThisIsCamelCase1234"), ["this", "is", "camel", "case", "1234"])
      self.assertEqual(to_words("thisIsCamelBackCase1234"), ["this", "is", "camel", "back", "case", "1234"])
      self.assertEqual(to_words("getURL"), ["get", "url"])

    def test_convert_to_hyphenated(self):
      self.assertEqual(convert("multiple-words-1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multiple_words_1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multipleWords1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("MultipleWords1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multiple words 1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multiple.words.1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multiple/words/1234", "hyphenated"), "multiple-words-1234")
      self.assertEqual(convert("multiple\\words\\1234", "hyphenated"), "multiple-words-1234")

    def test_convert_to_snake_case(self):
      self.assertEqual(convert("multiple-words-1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multiple_words_1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multipleWords1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("MultipleWords1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multiple words 1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multiple.words.1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multiple/words/1234", "snake"), "multiple_words_1234")
      self.assertEqual(convert("multiple\\words\\1234", "snake"), "multiple_words_1234")

    def test_convert_to_scream_snake_case(self):
      self.assertEqual(convert("multiple-words-1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multiple_words_1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multipleWords1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("MultipleWords1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multiple words 1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multiple.words.1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multiple/words/1234", "scream_snake"), "MULTIPLE_WORDS_1234")
      self.assertEqual(convert("multiple\\words\\1234", "scream_snake"), "MULTIPLE_WORDS_1234")

    def test_convert_to_dot_case(self):
      self.assertEqual(convert("multiple-words-1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multiple_words_1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multipleWords1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("MultipleWords1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multiple words 1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multiple.words.1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multiple/words/1234", "dot"), "multiple.words.1234")
      self.assertEqual(convert("multiple\\words\\1234", "dot"), "multiple.words.1234")

    def test_convert_to_space_case(self):
      self.assertEqual(convert("multiple-words-1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multiple_words_1234", "space"), "multiple words 1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multipleWords1234", "space"), "multiple words 1234")
      self.assertEqual(convert("MultipleWords1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multiple words 1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multiple.words.1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multiple/words/1234", "space"), "multiple words 1234")
      self.assertEqual(convert("multiple\\words\\1234", "space"), "multiple words 1234")

    def test_convert_to_camel_case(self):
      self.assertEqual(convert("multiple-words-1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multiple_words_1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multipleWords1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("MultipleWords1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multiple words 1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multiple.words.1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multiple/words/1234", "camel"), "MultipleWords1234")
      self.assertEqual(convert("multiple\\words\\1234", "camel"), "MultipleWords1234")

    def test_convert_to_camel_back_case(self):
      self.assertEqual(convert("multiple-words-1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multiple_words_1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multipleWords1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("MultipleWords1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multiple words 1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multiple.words.1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multiple/words/1234", "camel_back"), "multipleWords1234")
      self.assertEqual(convert("multiple\\words\\1234", "camel_back"), "multipleWords1234")

    def test_convert_to_slash_case(self):
      self.assertEqual(convert("multiple-words-1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multiple_words_1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multipleWords1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("MultipleWords1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multiple words 1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multiple.words.1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multiple/words/1234", "slash"), "multiple/words/1234")
      self.assertEqual(convert("multiple\\words\\1234", "slash"), "multiple/words/1234")

    def test_convert_to_backslash_case(self):
      self.assertEqual(convert("multiple-words-1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multiple_words_1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("MULTIPLE_WORDS_1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multipleWords1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("MultipleWords1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multiple words 1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multiple.words.1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multiple/words/1234", "backslash"), "multiple\\words\\1234")
      self.assertEqual(convert("multiple\\words\\1234", "backslash"), "multiple\\words\\1234")

    def test_alternate(self):
      result = alternate("multiple-words-1234")
      self.assertEqual(result, "multiple.words.1234")

      result = alternate(result)
      self.assertEqual(result, "multiple words 1234")

      result = alternate(result)
      self.assertEqual(result, "multiple/words/1234")

      result = alternate(result)
      self.assertEqual(result, "multiple\\words\\1234")

      result = alternate(result)
      self.assertEqual(result, "multiple_words_1234")

      result = alternate(result)
      self.assertEqual(result, "MULTIPLE_WORDS_1234")

      result = alternate(result)
      self.assertEqual(result, "MultipleWords1234")

      result = alternate(result)
      self.assertEqual(result, "multipleWords1234")

      result = alternate(result)
      self.assertEqual(result, "multiple-words-1234")

    def test_alternate_one_word(self):
      result = alternate("word")
      self.assertEqual(result, "WORD")

      result = alternate(result)
      self.assertEqual(result, "Word")

      result = alternate(result)
      self.assertEqual(result, "word")

  unittest.main()
