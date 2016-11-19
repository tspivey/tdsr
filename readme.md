#TDSR
This is a console-based screen reader.
It has been tested under macOS and Linux.
(However, no Linux speech server currently exists.)

##What works
* Reading output
* Reading by line, word and character
* cursor keys (waits some amount of time and speaks)

##Note
Compatibility is not guaranteed between versions.
##Requirements
* Python 3
* pyte
* speech server

##Installation on macOS
1. Clone this repository.
```git clone https://github.com/tspivey/tdsr.git```
1. Install python3. The following instructions assume you'll be using Homebrew.
See its documentation for installation instructions.
1. brew install python3
1. pip3 install -Ur requirements.txt
1. Assuming the repository is in ```~/tdsr```, run:
```~/tdsr/tdsr```
and it should start speaking.
##Terminal setup
Open Terminal preferences, under Profiles check Use Option as Meta key.
##Keys
(alt refers to the meta key.)
* alt u, i, o - read previous, current, next line
* alt j, k, l - read previous, current, next word
* alt m, comma, dot - read previous, current, next character
* alt c - config. Once in here, r sets rate, p toggles symbol processing and enter exits.
The configuration is saved.
* alt q - quiet mode on/off. When on, text is not automatically read.
##Symbols
Symbols can be added in the configuration file (```~/.tdsr.cfg```),
under the symbols section.

The format is:
```character code = name```
Because of how the config system works, it's best to do this with one tdsr open, then exit and re-launch to see the changes.
