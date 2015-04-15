import datetime

def keysInDict(dictionary, keys):
	return all(map(lambda k: k in dictionary, keys))


def datetimeStamp():
	return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

def unixTimestamp():
	d = datetime.datetime.utcnow()
	epoch = datetime.datetime(1970,1,1)
	t = (d - epoch).total_seconds()
	return int(t)