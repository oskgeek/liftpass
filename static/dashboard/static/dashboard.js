function saveCredentials() {
	localStorage.setItem('user-key', $('#user-key').val());
	localStorage.setItem('user-secret', $('#user-secret').val());
}

function tryLoadingCredentials() {
	$('#user-key').val(localStorage.getItem('user-key'));
	$('#user-secret').val(localStorage.getItem('user-secret'));
}

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
	
	var hash = CryptoJS.HmacSHA256(data, secret).toString();

	var response = $.ajax({
		type: 'POST',
		url: url,
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
	
	if(data.json.applications.length>0) {
		saveCredentials();
	}

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

	$('#debug-console').empty();

	if(data.json.log.length == 0){
		$('#debug-console').append($('<p class="bg-warning">This application has no logs.</p>'));
		return;
	}

	

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
	tryLoadingCredentials();
	$('#applications').change(applicationChange);

})
