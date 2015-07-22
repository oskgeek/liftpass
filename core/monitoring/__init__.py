from core.monitoring.base import Monitor
from core.monitoring.cloudwatch import CloudWatch
from core.monitoring.statsd import StatsD
import config


def getMonitor():
	if config.MonitorEngine == None:
		return Monitor(config.MonitorEngine)

	elif config.MonitorEngine['engine'] == 'core.monitoring.base':
		return Monitor(config.MonitorEngine)

	elif config.MonitorEngine['engine'] == 'core.monitoring.cloudwatch':
		return CloudWatch(config.MonitorEngine)

	elif config.MonitorEngine['engine'] == 'core.monitoring.statsd':
		return StatsD(config.MonitorEngine)
