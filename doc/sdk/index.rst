SDK
===

GondolaCore is an open source mobile pricing management platform. It manages and supplies mobile applications with unique prices and manages analytics from those applications. The mobile applications communicate with GondolaCore using an SDK which is defined below. 

Overview
========

The SDK has four primary responsibilities. Namely: 

* Collecting and managing progress metrics updated by the developer. 
* Tracking economy specific activities including purchasing of virtual good and IAP. 
* Transmitting the record of progress metrics and economy activity. Receiving of virtual good and IAP prices. 
* Supplying to the application prices for every virtual good and IAP.

The SDK is fundamentally an event based analytics SDK similar to those of MixPanel, Keen.io, Google Analytics, etc. All data is recorded in form of events which includes event names and associated attributes. However, events are not made accessible directly to the user of the SDK. In fact, to further facilitate use of the SDK strict limitations are imposed on how events are triggered and how much data is associated with the events.

The SDK has two types of triggers that generate events: updates of player progress and purchases of virtual goods and IAP. 


Design Philosophy
-----------------

The design of the SDK is based on strict, fixed sized data structures. The progress metrics recorded are referred to by index numbers. To facilitate developers macros will be supplied to the developer so that they do not have to type in mysterious index numbers when updating a metric so instead of updateMetric(12, levelsPlayed) they can type updateMetric(LEVELS_PLAYER, levelsPlayed). In general it will be expected that the SDK is have an additional file supplied by Gondola that facilitates the use of the SDK, containing helper functions and macros. In many ways the SDK specified below should be considered the the foundation for more sophisticated SDKs that can be built on top of. Similar to how C functions are very abstract, and more sophisticated C++ STL is developed on top of.

Progress Metrics
================

Updates of player progress can be considered events with a single attribute. This is the only mechanism of recording both player progress in a game and player profile. Meaning progress is also used to track device type, timezone, OS version and etc.

**Implementation Note**

* While updating progress can be seen as an event with a single attribute, when saving the updated progress the event will contain not just the value of the updated metric but also all other tracked progress metrics. 
* The SDK supports tracking of 32 progress metrics. 8 are string values and 24 are floating point metrics - stored in an array in that sequence (8 strings followed by 24 numbers).
* The user of the SDK has two primary functions of updating progress: updateProgress(progress index, progress value) and incrementProgress(progress index).
* Certain progress metrics that are hard to be recorded by the SDK user, are automatically filled when other metrics are updated. These include things like time zone, device type, OS version and etc.

**Issue**

* It is not clear how frequently events should be recorded when a progress metric is updated. Recording every progress metric update is scientifically good, but managing that much data is hard and impractical. The SDK should support different progress metric saving “strategies”.

Purchase Activity
=================

When players make a virtual good or IAP purchase, that must be recorded with the SDK using:
::
	recordPurchase(good name, good price)

This function is used for both virtual goods and IAP purchases interchangeably. When purchasing an IAP, the good price represents the amount of currency the player was rewarded (if any).

Goog price is a structure/array of 8 numbers representing the 8 virtual currencies the SDK supports. 

**Issue**

* It is often important to track the number of dollars spent by a player. It is not clear how this can be easily tracked with the SDK given that the SDK does not manage the dollar amounts for IAP, only the reward for the purchase of the IAP.

Data Transfer
=============

The SDK contains a single REST API call. The call “posts” the data recorded by the SDK and the response is a JSON file containing the price of all virtual goods and the reward for purchasing each IAP.
::
	sync() 

The user of SDK has the ability to choose where in the application the function is called. 

**Implementation Notes**

* The sync function must always submit at least one event.
* Returning JSON file is cached to ensure good prices are available at all times even when internet is not available.
* The application may be packaged with a JSON file representing prices for all goods which can be used prior to the first sync of the SDK with GondolaCore.

**Issue**

* How to ensure that prices are not modified by cheaters. How to “authenticate” prices to ensure they come from GondolaCore. 
* How to ensure that prices are not modified in the device by editing the saved JSON file.

Virtual Good Prices and IAP rewards
===================================

The SDK manages prices for all goods and IAP. 
::
	getPrice(good name)

The function returns a structure containing 8 prices representing 8 different currencies. Example is getPrice(“House”) = [100,0,0,50,0,0,0,0]. This represents the fact that a house costs say 100 wood and 50 stone, but also 0 iron, 0 gold, 0 cash, and etc.

Many games have a single currency or the developer knows the currency the good is priced as. In this case the function below returns a single integer number for the price of the good in the currency specified.
::
	getPrice(good name, currency index)

**Issue**

* How to handle requests for prices for goods that are not known by the SDK.

SDK Details
===========

Like all analytics SDKs, when the application loads an initial call initiates the SDK.
::
	init(application key)

This initial function creates if necessary all data structures and if required gives the player a unique player ID.

**Issue**

* How to initiate the SDK for players that were playing prior to the implementation of the SDK. Should the developer ignore previous players? Should the SDK mark those player and “grandfathered” players? How to handle players that play a game synced on two different devices? The progress will appear erratic to the SDK. 

Data Recording Format
=====================

The data is stored and transmitted to Gondola core in the following JSON format.

**General JSON format**

* application: application key used to identify the application. (32 character hex string)
* player: player id. (32 character unique hex string)
* events: list of events in ascending order of timestamp. The last item is the most recent event.

**Event JSON format**

* name: event name (32 characters long)
* time: UTC unix timestamp (integer with millisecond precision)
* progress: array containing all 32 progress metrics (first 8 elements must be strings, the others are floating point)
* attributes: optional array containing 16 elements (first 8 elements must be strings, the others are floating point)

**Rules**

* Purchase events have event name “purchase”, attributes[0] is the good name, and the 8 floating attribute fields represent the cost of the purchase in virtual currency (for IAP those values represent the reward for the purchase)
* All events must contain all 32 progress metrics
* Attributes are not required when updating a progress metric.



