import unittest
from unittest.mock import MagicMock, patch

from tdsr.backend.mac import handle_line, transform_speech_text


class TestMacSpeech(unittest.TestCase):
	def test_angle_brackets_transformed_to_fullwidth(self):
		self.assertEqual(transform_speech_text("<"), "\uff1c")
		self.assertEqual(transform_speech_text(">"), "\uff1e")
		self.assertEqual(transform_speech_text("< and >"), "\uff1c and \uff1e")
		self.assertEqual(transform_speech_text("a < b"), "a \uff1c b")
		self.assertEqual(transform_speech_text("x > y"), "x \uff1e y")

	def test_terminal_echo_command(self):
		input_text = 'echo "< and >"'
		expected = 'echo "\uff1c and \uff1e"'
		result = transform_speech_text(input_text)
		self.assertEqual(result, expected)
		self.assertNotIn("&lt", result)
		self.assertNotIn("&gt", result)

	def test_bracketed_tag_without_html_entities(self):
		input_text = "<test>"
		expected = "\uff1ctest\uff1e"
		result = transform_speech_text(input_text)
		self.assertEqual(result, expected)
		self.assertNotIn("&lt", result)
		self.assertNotIn("&gt", result)
		self.assertIn("test", result)

	def test_ampersand_is_not_escaped(self):
		input_text = 'echo "foo & bar"'
		result = transform_speech_text(input_text)
		self.assertEqual(result, input_text)
		self.assertNotIn("&amp", result)

	def test_control_character_cleanup(self):
		self.assertEqual(transform_speech_text("[["), " ")
		self.assertEqual(transform_speech_text("\u23ce"), " ")
		self.assertEqual(transform_speech_text("[[foo\u23ce"), " foo ")

	def test_handle_line_speech_lines(self):
		self.assertEqual(handle_line(b'secho "< and >"'), 'echo "\uff1c and \uff1e"')
		self.assertEqual(handle_line(b"s<test>"), "\uff1ctest\uff1e")
		self.assertEqual(handle_line(b"l<"), "\uff1c")
		self.assertEqual(handle_line(b"l>"), "\uff1e")
		self.assertEqual(handle_line('secho "< and >"'), 'echo "\uff1c and \uff1e"')

	def test_handle_line_empty_and_control(self):
		self.assertIsNone(handle_line(b""))
		self.assertIsNone(handle_line(b"x"))
		self.assertIsNone(handle_line(b"r50"))
		self.assertIsNone(handle_line(b"v80"))
		self.assertIsNone(handle_line(b"V0"))

	def test_handle_line_avfoundation_invocation(self):
		mock_synth = MagicMock()
		mock_utterance_cls = MagicMock()
		mock_utterance_instance = MagicMock()
		mock_utterance_cls.alloc.return_value.initWithString_.return_value = mock_utterance_instance

		with patch("tdsr.backend.mac.avsynth", mock_synth), \
			 patch("tdsr.backend.mac.AVSpeechUtterance", mock_utterance_cls):
			result = handle_line(b'secho "< and >"')
			self.assertEqual(result, 'echo "\uff1c and \uff1e"')
			mock_utterance_cls.alloc.return_value.initWithString_.assert_called_once_with('echo "\uff1c and \uff1e"')
			mock_utterance_instance.setPrefersAssistiveTechnologySettings_.assert_called_once_with(True)
			mock_synth.speakUtterance_.assert_called_once_with(mock_utterance_instance)


if __name__ == "__main__":
	unittest.main()
