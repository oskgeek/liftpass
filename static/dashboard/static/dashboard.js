function makeRequest(data, url) {
	var key =  $('#user-key').val();
	var secret = $('#user-secret').val();

	// if(key.length != 32 || secret.length != 32) {
	// 	return null;
	// }

	var data = $.extend({}, data, {
			'gondola-user': key,
			'gondola-time': Math.floor(Date.now()/1000),
			'gondola-url': url
		});
	
	data = JSON.stringify(data);
	
	var hash = CryptoJS.HmacSHA256(hash, secret).toString();

	var response = $.ajax({
		type: 'POST',
		url: 'http://'+$('#dashboard-address').val()+url,
		contentType: 'application/json',
		data: data,
		headers: {
			'gondola-hash': hash
		},
		async: false
	});

	if(response.status == 200) {
		response.json = JSON.parse(response.responseText);
	}

	return response;
}


function loadApplications() {
	if($('#applications').children().length > 0) {
		return;
	}

	var data = makeRequest({}, '/applications/');

	$.each(data.json.applications, function(i, e) {
		var option = $('<option>');
		$(option).text(e.name);
		$(option).attr('value', e.key);
		$('#applications').append(option);
	});	

	applicationChange();
}

function applicationChange() {
	runDashboard();
}

function runDashboard() {
	var application = $('#applications').val();

	var data = makeRequest({'gondola-application': application}, '/terminal/');

	if(data.json.log.length == 0){
		return;
	}

	$('#debug-console').empty();

	$.each(data.json.log, function(i, e) {
		if(e.length == 0)
			return;

		var entry = JSON.parse(e);
		
		var item = $('<div>');
		var pre = $('<pre>');

		var request = $('<code class="request json">'+JSON.stringify(entry.request, null, 4)+'</code>');
		var response = $('<code class="response json">'+JSON.stringify(entry.response, null, 4)+'</code>');

		$(request).appendTo(pre);
		$(response).appendTo(pre);
		$(pre).appendTo(item);

		$('#debug-console').append(item);

	});

	$('code').each(function(i,e){
		hljs.highlightBlock(e);
	});

}

function authenticate() {
	loadApplications();
}


$(document).ready(function() {

	$('#applications').change(applicationChange);

})