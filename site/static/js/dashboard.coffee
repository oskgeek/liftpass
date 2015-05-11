'use strict';




DashboardController = ($scope) ->

	$('#authenticateView').show()

	$scope.userKey = localStorage.getItem('userKey')
	$scope.userSecret = localStorage.getItem('userSecret')
	$scope.serverAddress = localStorage.getItem('serverAddress')

	$scope.deleteModal = {
		title: 'Untitled delete title'
		message: 'No message'
		callback: ()->return
	}

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
			success: (json) ->
				if 'error' of json
					$scope.errorMessage(json['error'])
				else
					callback(json)
			error: (response, status, error) ->
				$scope.errorMessage("An error occured while talking to Liftpass")
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

	$scope.addApplication = () =>
		$scope.request 'POST', {'liftpass-url':'/applications/add/v1/', 'name':$scope.applicationName}, $scope.addApplicationSuccess

	$scope.addApplicationSuccess = (json) =>
		$scope.successMessage("Good <strong>#{json.name}</strong> added")
		$scope.authenticate()

	$scope.deleteApplication = () =>
		$scope.openDeleteModal('You are about to delete this application!', 'This can not be undone. All related data will be lost.', () =>
			$scope.request 'DELETE', {'liftpass-url':'/applications/delete/v1/', 'key':$scope.application.key}, $scope.deleteApplicationSuccess
			return 
		)

	$scope.deleteApplicationSuccess = () =>
		$scope.successMessage("Application successfully deleted")
		$scope.authenticate()


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
		$scope.successMessage("Good <strong>#{json.name}</strong> added")
		$scope.goodName = ''
		$scope.goods.push(json)
		$scope.$apply()

	$scope.deleteGood = (key) =>
		$scope.openDeleteModal('You are about to delete a good!', 'This can not be undone.', () =>
			$scope.request 'DELETE', {'liftpass-url':'/goods/delete/v1/', 'key':key}, $scope.deleteGoodSuccess
			return 
		)
	
	$scope.deleteGoodSuccess = (json) =>
		$scope.successMessage("Good successfully deleted")
		$scope.loadGoods($scope.application['key'])

	# -------------------------------------------------------------------------- 
	# Currency
	# --------------------------------------------------------------------------
	$scope.loadCurrency = () =>
		$scope.request 'GET', {'liftpass-url':'/currencies/list/v1/', 'key': $scope.application['key']}, $scope.loadCurrencySuccess
	
	$scope.loadCurrencySuccess = (json) =>
		$scope.toggleDashboardView('#currencyView')
		
		$.each json, (i, v) ->
			if i.indexOf('currency') != 0
				delete json[i]
		$scope.currencies = json
		$scope.$apply()

	$scope.saveCurrency = (index) =>
		k = "currency#{index}"
		$scope.request 'PUT', {'liftpass-url':'/currencies/update/v1/', 'key': $scope.application['key'], k: $scope.currencies[k]}, $scope.saveCurrencySuccess
	
	$scope.saveCurrencySuccess = (json) =>
		$scope.successMessage("Currency name change saved")
		$scope.loadCurrency()

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
		$scope.request 'PUT', {'liftpass-url':'/metrics/update/v1/', 'key': $scope.application['key'], "#{metric['name']}": metric['value']}, $scope.saveMetricSuccess

	$scope.saveMetricSuccess = (json) =>
		$scope.successMessage("Progress metric saved")
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
		$scope.request 'POST', {'liftpass-url':'/prices/add/v1/', 'key': $scope.application['key'], 'engine':$scope.priceEngine, 'path':$scope.pricePath, 'data':$scope.priceData}, $scope.addPriceSuccess

	$scope.addPriceSuccess = () =>
		$scope.successMessage("Price successfully added")
		$scope.priceEngine = ''
		$scope.pricePath = ''
		$scope.priceData = ''
		$scope.loadPrices()

	$scope.deletePrice = (price) =>
		$scope.openDeleteModal('You are about to delete a set of prices!', 'This can not be undone.', () =>
			$scope.request 'DELETE', {'liftpass-url':'/prices/delete/v1/', 'key': price['key']}, $scope.deletePriceSuccess
			return 
		)
	
	$scope.deletePriceSuccess = (json) =>
		$scope.successMessage("Price successfully deleted")
		$scope.loadPrices()

	$scope.viewPrice = (price) =>
		$scope.textModal = {
			message: if price.data then price.data else price.path
		}
		$('#textModal').modal('show')
		return

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
			'groupAPrices_key': $scope.abtest['groupAPrices_key']
			'groupBPrices_key': $scope.abtest['groupBPrices_key']
		}, $scope.saveABTestSuccess

	$scope.saveABTestSuccess = (json) ->
		$scope.successMessage("A/B test settings saved")
		$scope.loadABTestSuccess($scope.abtest)

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
		$scope.request 'GET', {'liftpass-url':'/debug/get/v1/', 'key': $scope.application['key']}, $scope.loadDebugSuccess
	
	$scope.loadDebugSuccess = (json) =>
		$scope.toggleDashboardView('#debugView')
		$scope.debugData = json

	# -------------------------------------------------------------------------- 
	# SDK
	# --------------------------------------------------------------------------	
	$scope.loadSDK = () =>
		$scope.toggleDashboardView('#sdkView')
		return


	$scope.$on("$routeChangeSuccess",(event) ->
		console.log event
		event.preventDefault();
	)


	$scope.successMessage = (message) ->
		noty({
			layout: 'bottomRight'
			text: message
			type: 'success'
			timeout: 2000
			animation: {
				open: {height: 'toggle'}
				close: {height: 'toggle'}
				easing: 'swing'
				speed: 500
			}
		})
	$scope.errorMessage = (message) ->
		noty({
			layout: 'center'
			text: message
			type: 'error'
			timeout: false
			modal: true
			animation: {
				open: {height: 'toggle'}
				close: {height: 'toggle'}
				easing: 'swing'
				speed: 500
			}
		})

	$scope.openDeleteModal = (title, message, callback) =>
		$scope.deleteModal['title'] = title
		$scope.deleteModal['message'] = message
		$scope.deleteModal['callback'] = callback
		$('#deleteModal').modal('show')

	$scope.confirmDelete = () =>
		console.log($scope.deleteModal)
		$scope.deleteModal['callback']()
		$('#deleteModal').modal('hide')

	$scope.toggleDashboardView = (view) =>

		$('.subview').hide()
		$(view).show()

	$scope.viewVisible = (name) ->
		return $("##{name}View").is(':visible') == true


app = angular.module('dashboard', [])
app.controller('DashboardController', DashboardController)

