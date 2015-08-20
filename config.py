import sys
import os

# ------------------------------------------------------------------------------
# User Authentication - Liftpass is a single user application (for now)
# ------------------------------------------------------------------------------
UserKey = b'd759214482924d10ac159b794e9424e7'
UserSecret = b'4bf5d2c68e444ecab4d50adf8590544c'

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
	'path': os.path.join(DataPath, 'analytics/'),
	'update': 600,
}

# ------------------------------------------------------------------------------
# Content Database - Where application content and settings are stored
# ------------------------------------------------------------------------------
ContentDatabase = {
	'address': 'sqlite:///%s/content.db'%DataPath,
	'debug': False
}

# ------------------------------------------------------------------------------
# Pricing Engine - Where data for prices are stored
# ------------------------------------------------------------------------------
PricingStorage = {
	'engine': 'core.storage.filesystem',
	'path': os.path.join(DataPath, 'prices/')
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
	'cors': True
}
