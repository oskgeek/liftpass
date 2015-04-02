PriceStore
	Responsible for storing, loading, and fetching prices for every player
	
	load() -- load prices from database to memory
	test() -- test prices are working
	get() -- get prices for player

	== REST functions ==
	uploadPrices()
	listPrices()
	setActivePricesVersion()
	getActivePricesVersion()

ABControl
	Figures out what set of prices a player should see

	== Internal functions ==
	load() -- load A/B testing data to memory
	check() -- check if player is part of dynamic pricing 

	== REST functions ==
	addActiveCountry()
	removeActiveCountry()
	listActiveCountries()
	addActiveDevice()
	removeActiveDevice()
	listActiveDevices()
	setDefaultPriceVersion()
	getDefaultPriceVersion()
	setModulo()
	getModulo()


Analytics
	Takes player updates and stores it for later analyzing


Worker
	Interface with game SDK

Manager
	Interface with developer using REST/Dashboard


Core 
	- Database credentials
	- S3 credentials


================================================================================

updateProgress(name, value)
increaseProgress(name, amount)
purchase(name, price, currency)
getPrice(name, currency)

Progress = {progress_id, value}
Events = {name, time, attributes, progress}






================================================================================





purchaseVirtualGood(name, amount, amount, ...)
purchaseIAP(name, currency, amount)
sessionBegin()
sessionEnd()

event(name, attribute, attribute, ...)

updateProgress(metric, amount)
increaseProgress(metric, amount)


================================================================================




================================================================================
SDK 
================================================================================

GondolaCore SDK has 4 primary tasks:
1. Collecting and managing progress metrics updated by the developer.
2. Tracking economy specific activities including purchasing of virtual good and IAP.
3. Transmitting the record of progress metrics and economy activity. Receiving of virtual good and IAP prices.
4. Supplying to the game developer prices for every virtual good and IAP.


The SDK operates under a strict set of constraints. Namely:
- The developer can track up to 32 progress metrics. 8 strings and 24 floating point metrics.
- Virtual goods and IAP can have up to 8 simultaneous prices. 
- The player can earn and spend in 8 currencies.

The SDK manages all progress metrics and economy activities in the same event based format. An event has the following fields:
- game key
- player key
- time
- progress strings 8 
- progress flaots 24
- event name
- event attribute strings 8
- event attribute floats 8

For convenience and flexibility the SDK is devised around pipes that direct certain progress metrics and economic activity to the right places.
The 32 progress metrics are given developer friendly names that map to index values 0-31. 

#define GC_LEVELS_PLAYED 9

gcUpdateMetric(GC_LEVELS_PLAYED, levelsPlayed);
...or alternatively 
gcIncrementMetric(GC_LEVELS_PLAYED);

Some progress metrics are easier to filled automatically by the SDK. This includes: device name, country, language, time zone, and etc. For those pipes from the developer friendly names are mapped to SDK specific pipes. 

#define GC_COUNTRY	1
#define GC_INTERNAL_COUNTRY	GC_COUNTRY

Now every time the SDK updates any progress metric, country will automatically be set to the correct progress metric. 

To check everything is working progress can be fetched also.
gcGetMetric(GC_LEVELS_PLAYED)

When a player makes a purchase (either of virtual good or IAP) the following function exists:

GCPrices price = gcGetGoodPrice(goodName)

gcPurchase(goodName, price)

Internally by default only two event types are generated. The most common is the Update event that is triggered right before the request for new prices is submitted. It has no special attributes only the current progress metrics.
The second event is the Purchase event that is triggered every time the gcPurchase function is called. It includes the name of the good purchased and the 8 possible prices the good has.




