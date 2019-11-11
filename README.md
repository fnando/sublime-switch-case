# Switch Case for Sublime Text

This package switches the word under the cursor between `snake_case`, `hyphen-separated`, `SCREAM_SNAKE_CASE`, `CamelCase` and `camelBack`.

Since the introduction of `hyphen-separated` case conversion, you must select the terms you want to convert beforehand.

## Installation

### Setup Package Control Repository

To install packages from this channel, just add it to Package Control. Enable the command palette and type 'Add Repository'. Then paste the following URL: https://gist.githubusercontent.com/fnando/56393d3900af55bf9e94/raw/repositories.json

### Git Clone

Clone this repository into the Sublime Text “Packages” directory, which is located where ever the “Preferences” -> “Browse Packages” option in sublime takes you.

## Usage

The default binding is `super+k, super+c`.

![SwitchCase in action](https://raw.github.com/fnando/sublime-switch-case/master/SwitchCase.gif)

You can change it by defining a new shortcut binding like the following:

```json
{ "keys": ["super+k", "super+c"], "command": "switch_case" }
```

## License

Copyright (c) 2014 Nando Vieira

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
