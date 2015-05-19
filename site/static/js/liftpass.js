$(document).ready(function() {
	var form = $('.signup form');

	form.submit(function(event) {
		$('input[name="email"]').removeClass('error');
		$('button[type="submit"]').prop('disabled', true);
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			success: function (data) {
				if(data == '0') {
					$('input[name="email"]').addClass('error');
				}else{
					form.css('display','none');
					$('.signup').append($('<p>Awesome! Look out for an e-mail from us soon.</p>'))
				}
				$('button[type="submit"]').prop('disabled', false);
			}
		});
		event.preventDefault();
	});

});	