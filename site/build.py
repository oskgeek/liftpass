import jinja2
import os 
from bs4 import BeautifulSoup
import csv
import shutil
import sass
import yaml

import jinja2_highlight


contentDir = 'content/'
outputDir = 'build/'
dataDir = 'data/'
staticDir = 'static/'

globalData = {}

for data in os.listdir(dataDir):

	name = data[0: data.find('.')]
	print('Loading:', name)

	if data.endswith('.csv'):
		globalData[name] = list(csv.reader(open('%s%s'%(dataDir, data), 'r')))
	elif data.endswith('.yml'):
		globalData[name] = yaml.safe_load(open('%s%s'%(dataDir, data), 'r'))


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), extensions=[jinja2_highlight.HighlightExtension])
env.globals = globalData

for directory, nextDir, files in os.walk(contentDir):
	
	currentDir = directory
	currentDir = currentDir.replace(contentDir, outputDir)
	
	if os.path.exists(currentDir) == False:
		os.mkdir(currentDir)


	for content in files:
		if content.endswith('.html') == False:
			continue

		print('Processing: %s/%s'%(directory, content))

		# Open page
		data = open('%s/%s'%(directory, content), 'r').read()

		
		# Render page 
		template = env.from_string(data)
		data = template.render(page="%s/%s"%(directory, content))

		# Make it pretty
		data = BeautifulSoup(data).prettify()

		# Save
		open('%s/%s'%(currentDir, content), 'w+').write(data)

for directory, nextDir, files in os.walk(staticDir):

	currentDir = '%s/%s'%(outputDir, directory)
	
	if os.path.exists(currentDir) == False:
		os.mkdir(currentDir)

	for file in files:
		print('Static:', file)
		if file.endswith('.sass'):
			data = sass.compile(string=open('%s/%s'%(directory, file), 'r').read())
			name = file
			name = name.replace('.sass', '.css')
			open('%s/%s'%(currentDir, name), 'w+').write(data)
		else:
			shutil.copy('%s/%s'%(directory, file), '%s/%s'%(currentDir, file))