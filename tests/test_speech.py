import pytest
from unittest.mock import patch, MagicMock
from tdsr.speech import format_speech_text, normalize_text
from tdsr.backend.mac import handle_line, format_speech_text as mac_format_speech_text

def test_angle_brackets_normalized_to_words():
	assert format_speech_text("< and >") == "less than and greater than"
	assert format_speech_text("<") == "less than"
	assert format_speech_text(">") == "greater than"
	assert format_speech_text("a < b") == "a less than b"
	assert format_speech_text("x > y") == "x greater than y"

def test_terminal_echo_command():
	assert format_speech_text('echo "< and >"') == 'echo "less than and greater than"'

def test_no_html_entities_in_output():
	result = format_speech_text("< and > & test")
	assert "&lt" not in result
	assert "&gt" not in result
	assert "&amp" not in result
	assert "less than and greater than & test" == result

def test_normalize_text_alias():
	assert normalize_text("< and >") == "less than and greater than"

def test_bracket_and_return_replacement():
	assert format_speech_text("[[") == " "
	assert format_speech_text("\u23ce") == " "

def test_mac_backend_format_matches_speech():
	assert mac_format_speech_text("< and >") == format_speech_text("< and >")

def test_handle_line_pure_in_memory_no_audio():
	# Ensure avsynth is None or mocked so no audio is ever played
	with patch("tdsr.backend.mac.avsynth", None):
		assert handle_line(b"s< and >") == "less than and greater than"
		assert handle_line("s< and >") == "less than and greater than"
		assert handle_line(b"l<") == "less than"
		assert handle_line(b"l>") == "greater than"
		assert handle_line(b"shello") == "hello"
		assert handle_line(b"") is None
		assert handle_line(b"x") is None
