import blessings 
import sys
import io 
import traceback 
import datetime

terminal = blessings.Terminal()

def log(text):
	print('%s %s'%(datetime.datetime.now(), text))

def error(text):
	print(text, file=sys.stderr)

def stacktrace(exception):
	error('-'*60)
	print(datetime.datetime.now())
	error(str(exception))
	stream = io.StringIO()
	traceback.print_exc(file=stream)
	for line in stream.getvalue().split('\n'):
		error(line)
	error('-'*60)
