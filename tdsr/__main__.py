#!/usr/bin/env python3
import os
import termios
import tty

from tdsr.tdsr import FOCUS_REPORTING_OFF, main as tdsr_main


def main():
    old = termios.tcgetattr(0)
    try:
        tty.setraw(0)
        tdsr_main(old)
    finally:
        os.write(1, FOCUS_REPORTING_OFF)
        termios.tcsetattr(0, termios.TCSADRAIN, old)


if __name__ == "__main__":
    main()
