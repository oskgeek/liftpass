import config


def getTerminal():
	if config.DashboardTerminal['engine'] == 'core.terminal.local':
		import core.terminal.local as local
		return local.LocalTerminal(config.DashboardTerminal['path'])
	