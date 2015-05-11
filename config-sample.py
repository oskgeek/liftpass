import sys
import os

# ------------------------------------------------------------------------------
# User Authentication - Liftpass is a single user application (for now)
# ------------------------------------------------------------------------------
UserKey = b'$UserKey'
UserSecret = b'$UserSecret'

# ------------------------------------------------------------------------------
# Paths 
# ------------------------------------------------------------------------------
BasePath = os.path.abspath('./')
sys.path.append(BasePath)

# Where application data is stored
DataPath = os.path.join(BasePath,'data/')

# ------------------------------------------------------------------------------
# Analytics Storage - Where SDK updates are stored before being processed
# ------------------------------------------------------------------------------
AnalyticsStorage = {
	'engine': 'core.storage.filesystem',
	'path': os.path.join(DataPath, 'analytics/')
}

# ------------------------------------------------------------------------------
# Content Database - Where application content and settings are stored
# ------------------------------------------------------------------------------
ContentDatabase = {
	'address': 'sqlite:///%s/content.db'%DataPath,
	'debug': False
}

# ------------------------------------------------------------------------------
# Monitoring  - records server activity and performance (not yet supported)
# ------------------------------------------------------------------------------
MonitorEngine = None

# ------------------------------------------------------------------------------
# Debug Terminal - caches user updates for debuging
# ------------------------------------------------------------------------------
DashboardTerminal = {
	'engine': 'core.terminal.local',
	'path': os.path.join(DataPath, 'terminal/')
}

# ------------------------------------------------------------------------------
# API Interface Service
# ------------------------------------------------------------------------------
APIServer = {
	'address': '127.0.0.1',
	'port': 9090,
	'debug': True,
	'cors': True
}
