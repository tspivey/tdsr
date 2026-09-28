#Copyright (C) 2016, 2017  Tyler Spivey
#See the license in COPYING.txt

def format_speech_text(text):
	"""Format text for speech synthesis, replacing characters that cause issues with screen readers.

	Ensures '<' and '>' are formatted as 'less than' and 'greater than'
	rather than being vocalized as HTML entity names.
	"""
	text = text.replace('[[', ' ')
	text = text.replace('\u23ce', ' ')
	text = text.replace('<', 'less than').replace('>', 'greater than')
	return text

normalize_text = format_speech_text
