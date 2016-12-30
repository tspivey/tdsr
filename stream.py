from collections import defaultdict
from pyte import control as ctrl, escape as esc
from pyte.streams import Stream

class Stream(Stream):
	def _parser_fsm(self):
		# In order to avoid getting KeyError exceptions below, we make sure
		# that these dictionaries resolve to ``"debug"``.
		basic = defaultdict(lambda: "debug", self.basic)
		escape = defaultdict(lambda: "debug", self.escape)
		sharp = defaultdict(lambda: "debug", self.sharp)
		percent = defaultdict(lambda: "debug", self.percent)
		csi = defaultdict(lambda: "debug", self.csi)

		dispatch = self.dispatch

		ESC, CSI, SP = ctrl.ESC, ctrl.CSI, ctrl.SP
		NUL_OR_DEL = [ctrl.NUL, ctrl.DEL]
		CAN_OR_SUB = [ctrl.CAN, ctrl.SUB]
		ALLOWED_IN_CSI = [ctrl.BEL, ctrl.BS, ctrl.HT, ctrl.LF, ctrl.VT,
		ctrl.FF, ctrl.CR]
		while True:
			self.state = "stream"
			char = yield
			if char == ESC:
				# Most non-VT52 commands start with a left-bracket after the
				# escape and then a stream of parameters and a command; with
				# a single notable exception -- :data:`escape.DECOM` sequence,
				# which starts with a sharp.
				#
				# .. versionchanged:: 0.4.10
				#
				#    For compatibility with Linux terminal stream also
				#    recognizes ``ESC % C`` sequences for selecting control
				#    character set. However, in the current version these
				#    are noop.
				self.state = "escape"
				char = yield
				if char == "[":
					char = CSI  # Go to CSI.
				elif char == ']':
					while True:
						char = yield
						if char == '\x07':
							break #End of OSC
				else:
					if char == "#":
						self.state = "sharp"
						dispatch(sharp[(yield)])
					if char == "%":
						self.state = "percent"
						dispatch(percent[(yield)])
					elif char in "()":
						self.state = "charset"
						dispatch("set_charset", (yield), mode=char)
					else:
						dispatch(escape[char])
					continue  # Don't go to CSI.

			if char in basic:
				dispatch(basic[char])
			elif char == CSI:
				# All parameters are unsigned, positive decimal integers, with
				# the most significant digit sent first. Any parameter greater
				# than 9999 is set to 9999. If you do not specify a value, a 0
				# value is assumed.
				#
				# .. seealso::
				#
				#    `VT102 User Guide <http://vt100.net/docs/vt102-ug/>`_
				#        For details on the formatting of escape arguments.
				#
				#    `VT220 Programmer Ref. <http://vt100.net/docs/vt220-rm/>`_
				#        For details on the characters valid for use as
				#        arguments.
				self.state = "arguments"

				params = []
				current = ""
				private = False
				while True:
					char = yield
					if char == "?":
						private = True
					elif char in ALLOWED_IN_CSI:
						dispatch(basic[char])
					elif char == SP or char == ">":
						# We don't handle secondary DA atm.
						pass
					elif char in CAN_OR_SUB:
						# If CAN or SUB is received during a sequence, the
						# current sequence is aborted; terminal displays the
						# substitute character, followed by characters in the
						# sequence received after CAN or SUB.
						dispatch("draw", char)
						break
					elif char.isdigit():
						current += char
					else:
						params.append(min(int(current or 0), 9999))

						if char == ";":
							current = ""
						else:
							if private:
								dispatch(csi[char], *params, private=True)
							else:
								dispatch(csi[char], *params)
							break  # CSI is finished.
			elif char not in NUL_OR_DEL:
				dispatch("draw", char)
