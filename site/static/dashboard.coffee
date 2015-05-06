'use strict';




DashboardController = ($scope) ->
	
	$('#authenticateView').show()

	$scope.userKey = localStorage.getItem('userKey')
	$scope.userSecret = localStorage.getItem('userSecret')
	$scope.serverAddress = localStorage.getItem('serverAddress')

	$scope.saveCredentials = () ->
		localStorage.setItem('userKey', $scope.userKey)
		localStorage.setItem('userSecret', $scope.userSecret)
		localStorage.setItem('serverAddress', $scope.serverAddress)

	$scope.request = (method, data, callback) ->

		if $scope.userKey.length < 32 or $scope.userSecret.length < 32 or $scope.serverAddress < 10
			return

		$scope.saveCredentials()

		data = $.extend({}, data, {
			'liftpass-user': $scope.userKey,
			'liftpass-time': Math.floor(Date.now()/1000),
			'liftpass-url': data['liftpass-url']
		})
		
		json = JSON.stringify(data)
		
		hash = CryptoJS.HmacSHA256(json, $scope.userSecret).toString();
		
		if method == 'GET'
			requestData = {'json': btoa(json)}
		else
			requestData = json

		response = $.ajax({
			method: method,
			url: $scope.serverAddress+data['liftpass-url'],
			contentType: 'application/json',
			data: requestData,	
			crossDomain: true,
			async: true,
			headers: {
				'liftpass-hash': hash
			},
			success: callback
		})
			


	$scope.authenticate = () =>
		$scope.request	'GET', {'liftpass-url':'/applications/list/v1/'}, $scope.authenticateSuccess

	
	$scope.authenticateSuccess = (json) => 
		$('#authenticateView').hide()
		$('.view').hide()
		$('#applicationsView').show()

		$scope.applications = json['applications']
		$scope.$apply()

	$scope.loadApplication = (applicationKey) =>
		$scope.request 'GET', {'liftpass-url':'/applications/get/v1/', 'key': applicationKey}, $scope.loadApplicationSuccess

	$scope.loadApplicationSuccess = (json) =>
		$('#applicationsView').hide()
		$('#dashboardView').show()

		$scope.application = json
		$scope.$apply()


	# -------------------------------------------------------------------------- 
	# Goods
	# --------------------------------------------------------------------------
	$scope.loadGoods = () =>
		$scope.request 'GET', {'liftpass-url':'/goods/list/v1/', 'key': $scope.application['key']}, $scope.loadGoodsSuccess

	$scope.loadGoodsSuccess = (json) =>
		$scope.toggleDashboardView('#goodsView')

		$scope.goods = json['goods']
		$scope.$apply()

	$scope.addGood = () =>
		$scope.request 'POST', {'liftpass-url':'/goods/add/v1/', 'key':$scope.application['key'], 'name':$scope.goodName}, $scope.addGoodSuccess

	$scope.addGoodSuccess = (json) =>
		$scope.goodName = ''
		$scope.goods.push(json)
		$scope.$apply()

	$scope.deleteGood = (key) =>
		$scope.request 'DELETE', {'liftpass-url':'/goods/delete/v1/', 'key':key}, $scope.deleteGoodSuccess
	
	$scope.deleteGoodSuccess = (json) =>
		$scope.loadGoods($scope.application['key'])

	# -------------------------------------------------------------------------- 
	# Currency
	# --------------------------------------------------------------------------
	$scope.loadCurrency = () =>
		$scope.request 'GET', {'liftpass-url':'/currencies/get/v1/', 'key': $scope.application['key']}, $scope.loadCurrencySuccess
	
	$scope.loadCurrencySuccess = (json) =>
		$scope.toggleDashboardView('#currencyView')
		
		$.each json, (i, v) ->
			if i.indexOf('currency') != 0
				delete json[i]
		$scope.currencies = json
		$scope.$apply()

	$scope.saveCurrency = (index) =>
		k = "currency#{index}"
		$scope.request 'PUT', {'liftpass-url':'/currencies/update/v1/', 'key': $scope.application['key'], k: $scope.currencies[k]}, $scope.loadCurrency

	# -------------------------------------------------------------------------- 
	# Metrics
	# --------------------------------------------------------------------------
	$scope.loadMetrics = () =>
		$scope.request 'GET', {'liftpass-url':'/metrics/get/v1/', 'key': $scope.application['key']}, $scope.loadMetricsSuccess
	
	$scope.loadMetricsSuccess = (json) =>
		$scope.toggleDashboardView('#metricsView')
		
		data = $.map json, (i, v) -> {
			'value': i, 
			'name': v, 
			'index': if v.indexOf('String') != -1 then parseInt(v.slice(12)) else (parseInt(v.slice(12))+12)
		}

		data = data.filter (v) -> v['name'].indexOf('metric') != -1

		$scope.metrics = data

		$scope.$apply()

	$scope.saveMetric= (metric) =>
		console.log metric
		$scope.request 'PUT', {'liftpass-url':'/metrics/update/v1/', 'key': $scope.application['key'], "#{metric['name']}": metric['value']}, $scope.saveMetricSuccess

	$scope.saveMetricSuccess = (json) =>
		return
		

	# -------------------------------------------------------------------------- 
	# Prices
	# --------------------------------------------------------------------------
	$scope.loadPrices = () =>
		$scope.request 'GET', {'liftpass-url':'/prices/list/v1/', 'key': $scope.application['key']}, $scope.loadPricesSuccess

	$scope.loadPricesSuccess = (json) =>
		$scope.toggleDashboardView('#pricesView')
		$scope.prices = json['prices']
		$scope.$apply()

	$scope.addPrice = () =>
		$scope.request 'POST', {'liftpass-url':'/prices/add/v1/', 'key': $scope.application['key'], 'engine':$scope.priceEngine, 'path':$scope.priceEngine, 'data':$scope.priceData}, $scope.addPriceSuccess

	$scope.addPriceSuccess = () =>
		$scope.priceEngine = ''
		$scope.pricePath = ''
		$scope.priceData = ''
		$scope.loadPrices()

	$scope.deletePrice = (price) =>
		$scope.request 'DELETE', {'liftpass-url':'/prices/delete/v1/', 'key': price['key']}, $scope.deletePriceSuccess
	$scope.deletePriceSuccess = (json) =>
		$scope.loadPrices()

	# -------------------------------------------------------------------------- 
	# Prices
	# --------------------------------------------------------------------------
	
	$scope.loadABTest = () =>
		$scope.request 'GET', {'liftpass-url':'/abtest/get/v1/', 'key': $scope.application['key']}, $scope.loadABTestSuccess

	$scope.loadABTestSuccess = (json) =>
		$scope.toggleDashboardView('#abtestView')
		$scope.abtest = json
		$scope.$apply()

	$scope.saveABTest = () =>
		$scope.request 'PUT', {
			'liftpass-url':'/abtest/update/v1/', 
			'key': $scope.application['key'],
			'countryWhiteList': $scope.abtest['countryWhiteList'],
			'countryBlackList': $scope.abtest['countryBlackList'],
			'modulus': $scope.abtest['modulus'],
			'modulusLimit': $scope.abtest['modulusLimit'],
			'dynamicPrices_key': $scope.abtest['dynamicPrices_key']
			'staticPrices_key': $scope.abtest['staticPrices_key']
		}, $scope.loadABTestSuccess

	# -------------------------------------------------------------------------- 
	# Analytics
	# --------------------------------------------------------------------------
	$scope.loadAnalytics = () =>
		$scope.toggleDashboardView('#analyticsView')
		return

	# -------------------------------------------------------------------------- 
	# Debug
	# --------------------------------------------------------------------------	
	$scope.loadDebug = () =>
		$scope.toggleDashboardView('#debugView')
		return

	# -------------------------------------------------------------------------- 
	# SDK
	# --------------------------------------------------------------------------	
	$scope.loadSDK = () =>
		$scope.toggleDashboardView('#sdkView')
		return







	$scope.toggleDashboardView = (view) ->
		$('.subview').hide()
		$(view).show()

	$scope.viewVisible = (name) ->
		return $("##{name}View").is(':visible') == true




angular.module('dashboard', []).controller('DashboardController', DashboardController)







