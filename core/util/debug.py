import blessings 
import sys

terminal = blessings.Terminal()

def log(text):
	print(terminal.bold+'[Log] '+terminal.normal+text, file=sys.stderr)

def error(text):
	print(terminal.bold+terminal.red+'[Log] '+terminal.normal+terminal.white+text, file=sys.stderr)