# TDSR
This is a console-based screen reader.
It has been tested under macOS and Linux.
It might also run on FreeBSD and other *nix systems, but this hasn't been tested.

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
* Enter - exit, saving the configuration.

## Symbols
Symbols can be added in the configuration file (```~/.tdsr.cfg```),
under the symbols section.

The format is:
```
character code = name
```
Because of how the config system works, it's best to do this with one TDSR open, then exit and re-launch to see the changes.
