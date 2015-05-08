import blessings 
import sys
import io 
import traceback 

terminal = blessings.Terminal()

def log(text):
	print(terminal.bold+'[Log] '+terminal.normal+text)

def error(text):
	print(terminal.bold+terminal.red+'[Log] '+terminal.normal+terminal.white+text, file=sys.stderr)

def stacktrace(exception):
	error('-'*60)
	error(str(exception))
	stream = io.StringIO()
	traceback.print_exc(file=stream)
	for line in stream.getvalue().split('\n'):
		error(line)
	error('-'*60)