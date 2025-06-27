#!/usr/bin/env python3
#Copyright (C) 2016, 2017  Tyler Spivey
#See the license in COPYING.txt
from Foundation import (
	NSObject, NSFileHandle, NSNotificationCenter,
	NSFileHandleReadCompletionNotification, NSFileHandleNotificationDataItem,
)
from AVFoundation import AVSpeechSynthesizer, AVSpeechUtterance, AVSpeechBoundaryImmediate, AVSpeechSynthesisVoice
from PyObjCTools import AppHelper
from objc import python_method
import threading

rate = None
volume = None
voice_idx = None
voices = AVSpeechSynthesisVoice.speechVoices()
avsynth = AVSpeechSynthesizer.new()

class FileObserver(NSObject):
	def initWithFileDescriptor_readCallback_errorCallback_(self,
	fileDescriptor, readCallback, errorCallback):
		self = self.init()
		self.readCallback = readCallback
		self.errorCallback = errorCallback
		self.fileHandle = NSFileHandle.alloc().initWithFileDescriptor_(
		fileDescriptor)
		self.nc = NSNotificationCenter.defaultCenter()
		self.nc.addObserver_selector_name_object_(
		self,
		'fileHandleReadCompleted:',
		NSFileHandleReadCompletionNotification,
		self.fileHandle)
		self.fileHandle.readInBackgroundAndNotify()
		return self

	def fileHandleReadCompleted_(self, aNotification):
		ui = aNotification.userInfo()
		newData = ui.objectForKey_(NSFileHandleNotificationDataItem)
		if newData is None:
			if self.errorCallback is not None:
				self.errorCallback(self, ui.objectForKey_(NSFileHandleError))
			self.close()
		else:
			self.fileHandle.readInBackgroundAndNotify()
			if self.readCallback is not None:
				self.readCallback(self, bytes(newData))

	def close(self):
		self.nc.removeObserver_(self)
		if self.fileHandle is not None:
			self.fileHandle.closeFile()
			self.fileHandle = None
		# break cycles in case these functions are closed over
		# an instance of us
		self.readCallback = None
		self.errorCallback = None

	def __del__(self):
		# Without this, if a notification fires after we are GC'ed
		# then the app will crash because NSNotificationCenter
		# doesn't retain observers.  In this example, it doesn't
		# matter, but it's worth pointing out.
		self.close()

def prompt():
	sys.stdout.write("write something: ")
	sys.stdout.flush()

def gotLine(observer, line):
	if not line:
		AppHelper.stopEventLoop()
		return
	line = line.strip(b'\n')
	for l in line.split(b'\n'):
		handle_line(l)



def handle_line(line):
	global rate, volume, voice_idx
	line = line.decode('utf-8', 'replace')
	if line[0] == u"s" or line[0] == "l":
		l = line[1:].replace('[[', ' ')
		l = l.replace(u'\u23ce', ' ')
		u = AVSpeechUtterance.alloc().initWithString_(l)
		u.setPrefersAssistiveTechnologySettings_(True)
		if rate is not None:
			u.setRate_(rate)
		if volume is not None:
			u.setVolume_(volume)
		if voice_idx is not None:
			u.setVoice_(voices[voice_idx])
		avsynth.speakUtterance_(u)
	elif line[0] == u"x":
		avsynth.stopSpeakingAtBoundary_(AVSpeechBoundaryImmediate)
	elif line[0] == u"r":
		rate = float(line[1:])/100
	elif line[0] == u"v":
		volume = int(line[1:]) / 100.0
	elif line[0] == "V":
		voice_idx = int(line[1:])
		if voice_idx >= len(voices):
			voice_idx = None

def gotError(observer, err):
	print("error:", err)
	AppHelper.stopEventLoop()


def main():
	import sys
	observer = FileObserver.alloc().initWithFileDescriptor_readCallback_errorCallback_(
	sys.stdin.fileno(), gotLine, gotError)
	AppHelper.runConsoleEventLoop(installInterrupt=True)

if __name__ == '__main__':
	main()
	