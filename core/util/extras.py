import datetime

def keysInDict(dictionary, keys):
	return all(map(lambda k: k in dictionary, keys))


def datetimeStamp():
	return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')