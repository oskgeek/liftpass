from setuptools import setup, Command
import os
import string
import uuid

class ConfigureCommand(Command):
	description = 'Create basic Liftpass config.py file'
	user_options = []

	def initialize_options(self):
		pass
	def finalize_options(self):
		pass

	def run(self):

		if os.path.exists('config.py'):
			print('A config.py file already exists! If you want to create a new file, delete the current one first.')
			return 
			
		config = open('config-sample.py', 'r').read()

		userKey = uuid.uuid4().hex.replace('-', '')
		userSecret = uuid.uuid4().hex.replace('-', '')

		config = string.Template(config).substitute({
			'UserKey': userKey,
			'UserSecret': userSecret
		})

		if os.path.exists('config.py') == False:
			print('Generating config.py')
			open('config.py', 'w+').write(config)
		
	
		if os.path.exists('data') == False:
			print('Creating data/ directory')
			os.mkdir('data')
		if os.path.exists('data/analytics') == False:
			print('Creating data/analytics directory')
			os.mkdir('data/analytics')
		if os.path.exists('data/terminal') == False:
			print('Creating data/terminal directory')
			os.mkdir('data/terminal')
		if os.path.exists('tmp') == False:
			print('Creating tmp/ directory')
			os.mkdir('tmp')

setup(
	name = 'liftpass',
	version = '1.0',
	url = 'http://openliftpass.org',
	install_requires = [
		'markdown',
		'jinja2',
		'flask',
		'sqlalchemy',
		'blessings',
		'requests',
		'beautifulsoup4',
		'pyyaml',
		'libsass',
		'jinja2_highlight',

	], 
	cmdclass = {
		'config': ConfigureCommand
	}
)

