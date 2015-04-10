import sys
import os

#
# Update import path
#

BasePath = os.path.abspath('./')
DataPath = BasePath+'/data/'
sys.path.append(BasePath)

#
# Storage Buffer
#

StorageEngine = 'engine.storage.Filesystem'
StoragePath = 'tmp/'

#
# Content Database
#

ContentAddress = 'sqlite:///%s/content.db'%DataPath
ContentUsername = None
ContentPassword = None
ContentPort = None
ContentDatabase = None
ContentDebug = False

#
# Analytics 
#

analyticsEngine = None 
analyticsUsername = None
analyticsPassword = None
analyticsPort = None
analyticsDatabase = None

#
# Monitoring
#

MonitorEngine = 'engine.monitoring.SimpleMonitoring'
MonitorAddress =  '%s/monitoring'%DataPath
MonitorUsername = None
MonitorPassword = None
MonitorPort = None
MonitorDatabase = None
MonitorDebug = False

#
# User Authentication
#

UserKey = b'Kc61Fdmv9q2xiH2MNIhQM70U9N6Z1wqu'
UserSecret = b'8vM9o1fPN4mVG3VIPzy4ON9iXODYKxtt'

#
# SDK Interface Service
#

SDKAddress = '127.0.0.1'
SDKPort = 8080
SDKDebug = True

#
# API Interface Service
#

APIAddress = '127.0.0.1'
APIPort = 9090
APIDebug = True

#
# Dashboard Service
#

port = 7070