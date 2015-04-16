import config


def getTerminal():
	if config.DashboardTerminal['engine'] == 'core.dashboard.terminal.local':
		import core.dashboard.terminal.local as local
		return local.LocalTerminal(config.DashboardTerminal['path'])
	