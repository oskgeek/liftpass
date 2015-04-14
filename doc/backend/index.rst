Backend
=======

GondolaCore is divided into the following parts:

- Content
- Pricing
- Analytics
- API
- Monitoring


Content Management
------------------

- Applications 
- Metrics
- Currencies
- Goods
- Prices
- AB Testing


Pricing Engine
--------------

- JSON Engine
- Decision Tree Engine


Analytics
---------

- Processing
- Exporting


API
===

The primary way to interact with GondolaCore is via the API. Both for editing the content of applications (ex. registingering new applications, modifying goods, uploading new prices) and supplying games with new prices via the GondolaCore SDK. 

All API calls are standarized for interacting with the Backend as well as the SDK. The API follows normal REST best practices where the HTTP request method is as important as the URL itself. All parameters sent are in JSON format as part of the request body.

Minimal API JSON Content
------------------------

The minimal backend JSON call must contain: ::

	{
		'gondola-user': <32 character long user key>
		'gondola-url': <url being requested>
		'gondola-time': <UTC Unix timestamp>
	}

The minimal SDK JSON call must contain: ::

	{
		'gondola-application': <32 character long application key>
		'gondola-time': <UTC Unix timestamp>

		'player': <32 character unique player key>
		'events': [
			{
				name: <32 characters max>
				progress: <32 element array>			
				time: <UTC Unix timestamp>
				attributes: <16 element array>	
			}
			...
		]

	}

REST Calls
----------

GondolaCore authenticates all API REST requests using HMAC. HMAC fundamentally creates a unique hash (using SHA-256) of the JSON request and the application/user secret (depending if the API call is coming from a game or backend). The hash generated must be then added to the HTTP request header with the name :code:`gondola-hash`. GondolaCore will then check this hash value with the one it calculates. This process ensures that the request has come from a source that knew the application/user secret key. Any modification of the JSON body during transmission will render the request invalid. 

In more detail the HMAC authentication works as follows:

#. Add authentication fields to JSON
	* For Backend calls JSON must contain :code:`gondola-user`, :code:`gondola-url`, and :code:`gondola-time`.
	* For SDK calls JSON calls must contain :code:`gondola-application` and :code:`gondola-time`.
#. Hash is created using the application/user secret and the JSON data according to `RFC2104 <http://tools.ietf.org/html/rfc2104.html>`_.
#. Hash must be included in the HTTP header with the key named :code:`gondola-hash`.

.. IMPORTANT:: For authentication purposes the :code:`gondola-time` must be no more than 3 seconds different from that of the GondolaCore server. 

Methods
-------

Game
^^^^

**POST /games/add/v1/**

* Arguments
	* name - Name of new application
* Response
	* name - Name of new application
	* key - Application key
	* secret - Application secret
	* created - Timestamp when application was created



**GET /games/list/v1/**

* Arguments
* Response 
	* games - List of applications
		* name - Name of the application
		* key - Application key
		* secret - Application secret
		* created - Timestamp when application was created

**DELETE /games/delete/v1/**

* Arguments 
	* key - Application key
* Response 
	* deleted - Number of applications deleted

**GET /games/get/v1/**

* Arguments 
	* key - Application key
* Response
 	* name - Name of application
	* key - Application key
	* secret - Application secret
	* created - Timestamp when application was created

**PUT /games/update/v1/**

* Arguments
	* key - Application key
	* name - Application name (optional)
* Response
 	* name - Name of application
	* key - Application key
	* secret - Application secret
	* created - Timestamp when application was created

**GET /currencies/get/v1/**

* Arguments
	* key - Application key
* Response 
	* currency1 - Name of the 1st currency
	* currency2 - Name of the 2nd currency
	* currency3 - Name of the 3rd currency
	* currency4 - Name of the 4th currency
	* currency5 - Name of the 5th currency
	* currency6 - Name of the 6th currency
	* currency7 - Name of the 7th currency
	* currency8 - Name of the 8th currency

**PUT /currencies/update/v1/**

* Arguments
	* key - Application key
	* currency1 - Name of the 1st currency (optional)
	* currency2 - Name of the 2nd currency (optional)
	* currency3 - Name of the 3rd currency (optional)
	* currency4 - Name of the 4th currency (optional)
	* currency5 - Name of the 5th currency (optional)
	* currency6 - Name of the 6th currency (optional)
	* currency7 - Name of the 7th currency (optional)
	* currency8 - Name of the 8th currency (optional)
* Response 
	* currency1 - Name of the 1st currency
	* currency2 - Name of the 2nd currency
	* currency3 - Name of the 3rd currency
	* currency4 - Name of the 4th currency
	* currency5 - Name of the 5th currency
	* currency6 - Name of the 6th currency
	* currency7 - Name of the 7th currency
	* currency8 - Name of the 8th currency

**POST /goods/add/v1/**

* Arguments
	* key - Application key
	* name - Name of the good
* Response
	* key - Good key
	* name - Name of the good
	* created - Timestamp of when good was created

**GET /goods/get/v1/**

* Arguments
	* key - Good key
* Response 
	* key - Good key
	* name - Name of the good
	* created - Timestamp of when good was created

**GET /goods/list/v1/**

* Arguments
	* key - Application key
* Response 
	* goods - List of goods for the application
		* key - Good key
		* name - Name of the good
		* created - Timestamp of when good was created

**DELETE /goods/delete/v1/**

* Arguments
	* key - Good key
* Response 
	* deleted - Number of goods deleted

**PUT /goods/update/v1/**

* Arguments
	* key - Good key
	* name - Good name (optional)
* Response
	* key - Good key
	* name - Name of the good
	* created - Timestamp of when good was created

**GET /abtest/get/v1/**

* Arguments
	* key - Application key
* Response
	* key - Application key
	* countryWhiteList - List of countries that can participate in dynamic pricing
	* countryBlackList - List of countries not participating in dynamic pricing
	* modulus - Modulus to apply to user IDs
	* modulusLimit - Modulus limit of users that qualify for dynamic pricing
	* dynamicPrices_key - Prices key being used for dynamic pricing
	* staticPrices_key - Prices key being used for static pricing

**PUT /abtest/update/v1/**

* Arguments
	* key - Application key
	* countryWhiteList - List of countries that can participate in dynamic pricing (optional)
	* countryBlackList - List of countries not participating in dynamic pricing (optional)
	* modulus - Modulus to apply to user IDs (optional)
	* modulusLimit - Modulus limit of users that qualify for dynamic pricing (optional)
	* dynamicPrices_key - Prices key being used for dynamic pricing (optional)
	* staticPrices_key - Prices key being used for static pricing (optional)
* Response 
	* countryWhiteList - List of countries that can participate in dynamic pricing
	* countryBlackList - List of countries not participating in dynamic pricing
	* modulus - Modulus to apply to user IDs
	* modulusLimit - Modulus limit of users that qualify for dynamic pricing
	* dynamicPrices_key - Prices key being used for dynamic pricing
	* staticPrices_key - Prices key being used for static pricing

**GET /metrics/get/v1/**

* Arguments
	* key - Application key
* Response
	* key - Application key
	* str1-str8 - Name of string metrics
	* num1-num24 - Name of numberic metrics

**PUT /metrics/update/v1/**

* Arguments 
	* key - Application key
	* str1-str8 - Name of string metrics (optional)
	* num1-num24 - Name of numberic metrics (optional)
* Response
	* key - Application key
	* str1-str8 - Name of string metrics
	* num1-num24 - Name of numberic metrics

**GET /prices/list/v1/**

* Arguments
	* key - Application key
* Response 
	* prices - List of prices for the application
		* key - Application key
		* price_key - Prices key
		* engine - Name of pricing engine 
		* path - Path where prices is stored
		* data - Data for prices if stored
		* created - Timestamp of when price was created

**GET /prices/get/v1/**

* Arguments
	* key - Prices key
* Response
	* key - Application key
	* price_key - Prices key
	* engine - Name of pricing engine 
	* path - Path where prices is stored
	* data - Data for prices if stored
	* created - Timestamp of when price was created

**DELETE /prices/delete/v1/**

* Arguments
	* key - Prices key
* Response
	* deleted - Number of prices deleted

**POST /prices/add/v1/**

* Arguments
	* key - Application key
	* engine - Name of pricing engine 
	* path - Path where prices is stored
	* data - Data for prices if stored
* Response
	* key - Application key
	* price_key - Prices key
	* engine - Name of pricing engine 
	* path - Path where prices is stored
	* data - Data for prices if stored
	* created - Timestamp of when price was created

**POST /update/v1/**

* Arguments
	* player - Player unique ID
	* events - Ordered list of events (ascing timestamp)
		* name: Name of the event
		* progress: Array of the 32 progress metrics (optional)
		* time: Timestamp of when the event was triggered 
		* attributes: Array of the 16 event attributes (optiona)
* Response
	* goods - Dictionary of goods names and prices (good name=>price array)


Monitoring
----------

- Segment.io