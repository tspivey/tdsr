#TDSR
This is a console-based screen reader.
It has been tested under Linux and Mac OS.

##What works
* Reading output
* Reading by line and character
* cursor keys (waits some amount of time and speaks)
##What doesn't work
* Reading by word
* Configuration
##Requirements
* Python 3
* Emacspeak speech server
Currently it's hardcoded to run ```~/mac```.

To install some required Python libraries, run:
```pip3 install -r requirements.txt```
