from flask import Flask
from flask import request
import flask

import core.util.rest as rest
import core.content.content as content
import core.dashboard.terminal as terminal

import config

app = Flask(__name__, 
		static_folder='%s/static/'%config.DashboardStatic, 
		static_url_path='/static', 
		template_folder='%s/templates/'%config.DashboardStatic)


@app.route('/', methods=['GET'])
def index():

	dashboardAddress = '%s:%d'%(config.DashboardAddress, config.DashboardPort)
	apiAddress = '%s:%d'%(config.APIAddress, config.APIPort)

	return flask.render_template('index.html', dashboardAddress=dashboardAddress, apiAddress=apiAddress)


@app.route('/terminal/', methods=['GET', 'POST'])
# @rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def getLog():
	theTerminal = terminal.getTerminal()
	
	data = theTerminal.get(request.json['gondola-application'])

	return rest.successResponse({'log': data})

@app.route('/applications/', methods=['GET', 'POST'])
def applications():
	backend = content.Content()

	applications = backend.getApplications()	
	result = list(map(lambda g: g.as_dict(), applications))

	return rest.successResponse({'applications': result})



def start():
	global app
	app.run(debug=config.DashboardDebug, host=config.DashboardAddress, port=config.DashboardPort)


def getApp():
	global app
	return app