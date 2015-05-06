import sys
import os

#
# Update import path
#

BasePath = os.path.abspath('./')
DataPath = BasePath+'/data/'
StaticPath = BasePath+'/static/'
sys.path.append(BasePath)

#
# Analytics Storage
#

AnalyticsStorage = {
	'engine': 'core.storage.filesystem',
	'path': BasePath+'/tmp/'
}

#
# Content Database
#

ContentAddress = 'sqlite:///%s/content.db'%DataPath
ContentDebug = False

#
# Monitoring
#

MonitorEngine = 'core.monitoring.SimpleMonitoring'
MonitorAddress =  '%s/monitoring'%DataPath
MonitorDebug = False

#
# User Authentication
#

UserKey = b'$UserKey'
UserSecret = b'$UserSecret'


# 
# Dashboard 
#
DashboardAddress = '127.0.0.1'
DashboardPort = 8080
DashboardDebug = True
DashboardStatic = '%s/dashboard/'%StaticPath
DashboardTerminal = {
	'engine': 'core.dashboard.terminal.local',
	'path': '%s/terminal/'%DataPath
}

#
# API Interface Service
#

APIAddress = '127.0.0.1'
APIPort = 9090
APIDebug = True