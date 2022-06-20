#!/usr/bin/env python3
import termios
import tty

from tdsr.tdsr import main as tdsr_main


def main():
    old = termios.tcgetattr(0)
    try:
        tty.setraw(0)
        tdsr_main(old)
    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, old)


if __name__ == "__main___":
    main()
