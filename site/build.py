import jinja2
import os 
import sys
from bs4 import BeautifulSoup
import csv
import shutil
import dbm
import sass
import yaml
import coffeescript
import jinja2_highlight


contentDir = 'content/'
outputDir = 'build/'
dataDir = 'data/'
staticDir = 'static/'


class Build:

	def __init__(self, cache=True):
		self.globalData = {}
		self.env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), extensions=[jinja2_highlight.HighlightExtension])
		self.env.globals = self.globalData
		if cache:
			self.cache = dbm.open('.cache', 'c')
		else:
			self.cache = dbm.open('.cache', 'n')

	def __del__(self):
		self.cache.close()


	def buildAll(self):
		self.loadData()
		self.renderContent()
		self.compileStatic()

	# --------------------------------------------------------------------------
	# 1) Load data 
	# --------------------------------------------------------------------------
	def loadData(self):
		for data in os.listdir(dataDir):
			name = data[0: data.find('.')]
			print('Loading:', name)

			if data.endswith('.csv'):
				self.globalData[name] = list(csv.reader(open('%s%s'%(dataDir, data), 'r')))
			elif data.endswith('.yml'):
				self.globalData[name] = yaml.safe_load(open('%s%s'%(dataDir, data), 'r'))
	# --------------------------------------------------------------------------
	# 2) Render content 
	# --------------------------------------------------------------------------
	def renderContent(self):
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
				template = self.env.from_string(data)
				data = template.render(page="%s/%s"%(directory, content))

				# Make it pretty
				data = BeautifulSoup(data).prettify()

				# Save
				open('%s/%s'%(currentDir, content), 'w+').write(data)

	# --------------------------------------------------------------------------
	# 3) Compile static data
	# --------------------------------------------------------------------------
	def compileStatic(self):	
		for directory, nextDir, files in os.walk(staticDir):

			# Skip hidden directories
			if '/.' in directory:
				continue

			currentDir = '%s/%s'%(outputDir, directory)
			
			if os.path.exists(currentDir) == False:
				os.mkdir(currentDir)

			for file in files:
				# Skip hidden files
				if file[0] == '.':
					continue

				source = '%s/%s'%(directory, file)
				
				if file.endswith('.sass'):
					name = file
					name = name.replace('.sass', '.css')
					if self.shouldCompile(source, destination):
						print('Compiling:', source)
						data = sass.compile(string=open(source, 'r').read())
						open(destination, 'w+').write(data)
				elif file.endswith('.coffee'):
					name = file.replace('.coffee', '.js')
					destination = '%s/%s'%(currentDir, name)
					if self.shouldCompile(source, destination):
						print('Compiling:', source)
						data = coffeescript.compile(open(source, 'r').read())
						open(destination, 'w+').write(data)
				else:
					destination = '%s/%s'%(currentDir, file)
					if self.shouldCompile(source, destination):
						print('Copying:', source)
						shutil.copy(source, destination)

	def shouldCompile(self, source, destination):
		res = False
		lastModified = ('%d'%os.stat(source).st_mtime).encode('utf-8')

		if source not in self.cache or os.path.exists(destination) == False:
			res = True
		else:
			res = self.cache[source] != lastModified

		self.cache[source] = lastModified

		return res


if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		Build().buildAll()
	else:
		cache = not('--force' in sys.argv)
		Build(cache=cache).buildAll()