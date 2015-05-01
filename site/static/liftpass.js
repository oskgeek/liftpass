// function stretchAndCenter() {

// 	$('.stetch-and-center').each(function(index, element) {

// 		var parentHeight = $(element).parent().height();
		
// 		var childHeight = $(element).children().outerHeight();


// 		if($(window).width()>=768) {
// 			$(element).height(parentHeight);
// 		}else{
// 			$(element).height(childHeight);
// 		}
// 		console.log(parentHeight, childHeight);
// 		$(element).children().each(function(i, e){
// 			$(e).css('top', parentHeight-childHeight)
// 				.css('width', $(element).width())
// 				.css('position', 'absolute');
// 		});
// 	});

// }

// $(window).resize(stretchAndCenter);
// $(document).ready(stretchAndCenter);