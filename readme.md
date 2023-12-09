# TDSR
This is a console-based screen reader.
It has been tested under macOS, Linux and FreeBSD.
It might also run on other \*nix systems, but this hasn't been tested.

## What works
* Reading output
* Reading by line, word and character
* cursor keys (waits some amount of time and speaks)

## Note
Compatibility is not guaranteed between versions.
## Requirements
* Python 3
* pyte
* speech server

## Installation on macOS
1. Install Python 3. If using [Homebrew](http://brew.sh/), `brew install python3`.
1. Clone this repository.
```git clone https://github.com/tspivey/tdsr.git```
1. cd tdsr
1. pip3 install -Ur requirements.txt
1. Assuming the repository is in ```~/tdsr```, run:
`~/tdsr/tdsr`
and it should start speaking.

## Installation on Linux

1. Install Python 3 and Speech Dispatcher.  They should be available from your package manager.
You may also need to install Speech Dispatcher's Python bindings, if they were packaged separately by your distro.
1. Follow the rest of the instructions for Mac OS X, starting with "Clone this repository".

## Terminal setup
Open Terminal preferences, under Profiles check Use Option as Meta key.
## Keys
(alt refers to the meta key.)
* alt u, i, o - read previous, current, next line
* alt j, k, l - read previous, current, next word
* alt m, comma, dot - read previous, current, next character
* alt k twice - spell current word
* alt comma twice - say current character phonetically
* alt c - config.
* alt q - quiet mode on/off. When on, text is not automatically read.
* alt r - start/end selection.
* alt v - copy mode. Press l to copy the line the review cursor is on, or s to copy the screen.

## Configuration
Once in the config menu, you can use:
* r - set rate.
* v - set volume (value between 0 and 100).
* p - toggle symbol processing.
* d - set cursor delay (in MS). The default is 20.
* l - Toggle pausing at newlines.
* s - Toggle repeated symbols
* Enter - exit, saving the configuration.

## Symbols
Symbols can be added in the configuration file (```~/.tdsr.cfg```),
under the symbols section.

The format is:
```
character code = name
```
Because of how the config system works, it's best to do this with one TDSR open, then exit and re-launch to see the changes.

## Plugins
Custom key binds and handlers can be added via the plugins and commands section of the config files
and a python module in the plugins directory that exports the following method signature:

```python
# Name: parse_output
# Parameters: an array of strings (the lines from the terminal)
# Returns: an array of strings (the things to speak)
def parse_output(lines):
    return ["a list of things to say"]
```

### Config file
In ~/.tdsr.cfg you add to the plugins and commands section to modify the shortcut and terminal command that has been run

Required: [plugins] The plugin section maps to a letter you press with alt to trigger the plugin.

Optional: [commands] The command section is a regex of the command you ran previous to triggering the plugin (this minimizes processing time)

Optional: A regex to indicate the start of your prompt line in your terminal

#### Example

To add a shortcut for alt d to trigger a plugin called my_plugin add the following under [plugins]

```
my_plugin = d
```
If you have sub folders, separate them with a dot e.g. for plugins/me/my_plugin

```
me.my_plugin = d
```

To specify a command of `echo "hi"` (which makes parsing slightly more efficient) add the following under [commands]
```
my_plugin = echo "hi"
```
Use dots for sub folders, like the plugin config. You can use a regular expression to make it more flexible, e.g. to
specify a command of `echo "hi"` or `echo "bye"`

```
my_plugin = echo "(hi|bye)"
```

The default prompt is match anything, if you use zsh you can use the following regular expression under [speech]:

```
prompt = ^➜\s{2}.+✗?
```

#### Errors

If you hear "error loading plugin" followed by an error, you can launch tdsr in debug mode

```commandline
~/tdsr --debug
```

And search the logs for "Error loading plugin" to see more details

## Repeating symbols
Symbols you would like condensed down to "42 =" instead of "= = = =" you can specify under the speech section

```
repeated_symbols_values = -_=! 
```

## License
Copyright (C) 2016, 2017  Tyler Spivey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
