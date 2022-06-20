#!/usr/bin/env python3
#Copyright (C) 2016, 2017  Tyler Spivey
#See the license in COPYING.txt
import io
import sys
import speechd.client

def check_range(synth, value, low, high, name):
	if value >= low and value <= high:
		return True
	synth.speak('Bogus value for {0}: {1}.  Value must be in the range {2} to {3}'.format(name, value, low, high))
	return False

def main():
	input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
	synth = speechd.client.SSIPClient('tdsr')
	line = input_stream.readline()
	while line:
		line = line.strip('\n')
		if line[0] == u"s":
			synth.speak(line[1:])
		elif line[0] == u"l":
			# TODO capitals.  Do pitchrise here, or just
			# let it be Speech Dispatcher's problem?
			synth.char(line[1:])
		elif line[0] == u"x":
			synth.cancel()
		elif line[0] == u"r":
			rate = int(line[1:])
			if check_range(synth, rate, 0, 100, 'rate'):
				synth.set_rate(-100 + rate * 2)
		elif line[0] == u"v":
			volume = int(line[1:])
			if check_range(synth, volume, 0, 100, 'volume'):
				synth.set_volume(-100 + volume * 2)
		line = input_stream.readline()
	synth.close()

if __name__ == '__main__':
	main()
