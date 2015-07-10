
	
class Live
	timeDifference: (previous) ->
		current = Math.floor(Date.now())
		msPerMinute = 60 * 1000
		msPerHour = msPerMinute * 60
		msPerDay = msPerHour * 24
		msPerMonth = msPerDay * 30
		msPerYear = msPerDay * 365
		elapsed = current - previous

		if elapsed < 0
			return '<span class="text-danger">Incorrect time</span>'
		else if elapsed < msPerMinute
			return Math.round(elapsed/1000) + ' seconds ago'
		else if elapsed < msPerHour
			return Math.round(elapsed/msPerMinute) + ' minutes ago'
		else if elapsed < msPerDay 
			return Math.round(elapsed/msPerHour ) + ' hours ago'
		else if elapsed < msPerMonth
			return Math.round(elapsed/msPerDay) + ' days ago'
		else if elapsed < msPerYear
			return Math.round(elapsed/msPerMonth) + ' months ago'
		else
			return Math.round(elapsed/msPerYear ) + ' years ago'

	update: () =>
		console.log 'Updating'
		serverAddress = $('#serverAddress').val()
		appKey = $('#appKey').val()
		appSecret = $('#appSecret').val()

		data = {
			'liftpass-application': appKey,
			'liftpass-time': Math.floor(Date.now()/1000),
			'liftpass-url': '/debug-app/get/1.0/'
		}

		json = JSON.stringify(data)

		hash = CryptoJS.HmacSHA256(json, appSecret).toString();

		requestData = {'json': btoa(json)}

		response = $.ajax({
			method: 'GET',
			url: serverAddress+'/debug-app/get/1.0/',
			contentType: 'application/json',
			data: requestData,	
			crossDomain: true,
			async: true,
			headers: {
				'liftpass-hash': hash
			},
			success: (json) ->
				localStorage.setItem('appKey', $('#appKey').val())
				localStorage.setItem('appSecret', $('#appSecret').val())
				localStorage.setItem('serverAddress', serverAddress)

				window.live.updateTerminal(json)

				setTimeout(window.live.login, 5000)				
			error: (response, status, error) ->
				console.log "An error occured while talking to Liftpass"
		})

	updateTime: () =>

		$('.time').each (i, e) ->
			$(e).html window.live.timeDifference($(e).data('time'))
		

	updateTerminal: (json) =>
		$('#login').hide()
		$('#terminal').show()

		for item in json.log
			if item.length == 0 
				continue
			
			data = JSON.parse(item)
			
			time = data.request['liftpass-time']*1000
			tdTime = @timeDifference(time)
			tdIP = data.request['liftpass-ip']
			tdUser = data.request.user
			tdEvents = data.request.events.length
			
			if tdUser.length == 0
				continue

			overview = $("<tr class=\"t#{time}\" data-id=\"#{time}\"><td class=\"time\" data-time=\"#{time}\"></td><td>#{tdIP}</td><td>#{tdUser}</td><td>#{tdEvents}</td><td><button class=\"btn btn-default btn-xs\">Details</button></td></tr>")
			
			eventsTemplate = "
				<table class=\"table events\">
					<thead>
						<th>Time</th>
						<th>Name</th>
						<th colspan=\"32\">Progress</th>
					</thead>
					<tbody>
					{{#events}}
						<tr>
							<td rowspan=\"2\">{{time}}</td>
							<td rowspan=\"2\">{{name}}</td>
							{{#progress}}
								<td class=\"small\">{{.}}</td>
							{{/progress}}
						</tr>
						<tr>
							{{#attributes}}
								<td class=\"small\">{{.}}</td>
							{{/attributes}}
						</tr>
					{{/events}}
					</tbody>
				</table>
			"

			pricesTemplate = "
				<table class=\"table prices\">
					<thead>
						<tr>
							<th>Good</th>
							<th colspan=\"8\">Price</th>
						</tr>
					</thead>
					<tbody>
					{{#goods}}
						<tr>
							<td>{{name}}</td>
							{{#price}}
								<td class=\"small\">{{.}}</td>
							{{/price}}
						</tr>
					{{/goods}}
					</tbody>
				</table>
			"

			goods = {goods: ({name:k, price:data.response.goods[k]} for k of data.response.goods)}

			details = $("
				<tr class=\"details d#{time}\" style=\"display: none\">
					<td colspan=\"5\" class=\"details\">
						<p><strong>Events</strong></p>
						#{Mustache.render(eventsTemplate, data.request)}
						<p><strong>Prices</strong></p>
						#{Mustache.render(pricesTemplate, goods)}
					</td>
				</tr>")
			
			if $(".t#{time}").length == 0
				$(overview).find('button').click (event)->
					row = $(event.currentTarget).parent().parent()
					id = '.d'+$(row).data('id')
					if $(id).css('display') != 'none'
						$(id).css('display', 'none')
					else
						$(id).css('display', 'table-row')
					
				$('#terminalBody').prepend(details)
				$('#terminalBody').prepend(overview)

			@updateTime()
			

	login: () =>
		@update()


$(document).ready () ->
	$('#serverAddress').val(localStorage.getItem('serverAddress'))
	$('#appKey').val(localStorage.getItem('appKey'))
	$('#appSecret').val(localStorage.getItem('appSecret'))

	window.live = new Live()