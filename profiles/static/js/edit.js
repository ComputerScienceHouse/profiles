//show edit forms 
$(function() {
	$("#edit").on('click', function () {
		$(".user-form-input").show()
		$(".user-form-value").hide()
		$("#save").show()
		$("#edit").hide()
	});
});

//show image upload on click
$(function() {
	$("#self-picture").on('click', function () {
		$("#upload-form").toggle()
	});
});

//upload form data
$(function() {
	$("#save").on('click', function (e) {

		var form_data = { 
			"name": $("#user-name").val(),
			"birthday": $("#user-birthday").val(),
			"phone": $(".user-mobile").map(function() {
				return $(this).val();
			}).get(),
			"calendar": $("#user-calendar").val(),
			"plex": $("#user-plex").val(),
			"major": $("#user-major").val(),
			"ritYear": $("#user-rityear").val(),
			"website": $("#user-homepage").val(),
			"resume": $("#user-resume").val(),
			"twitter": $("#user-twitter").val(),
			"blog": $("#user-blog").val(),
			"google": $("#user-google").val(),
			"mail": $(".user-mail").map(function() {
				return $(this).val();
			}).get(),
			"nickname": $(".user-nickname").map(function() {
				return $(this).val();
			}).get(),
			"shell": $("#user-shell").val(),
			"minor": $("#user-minor").val(),
		};

		$.ajax({
			url: '/update',
			dataType: 'json',
		    type: 'post',
		    contentType: 'application/json',
		    data: JSON.stringify(form_data),
			success: function (data, textStatus, jqXHR) {
				location.reload();
			},
			error: function(error) {
				console.log(error);
			}
		});

	});
});

//************* PROFILE PICTURE *************
//upload croppie image
$(function() {
	$("#photo-button").on('click', function (e) {
		$image_crop.croppie('result', {
			type: 'canvas',
			size: {
				width: 300,
				height: 300,
			}
		}).then(function (response) {
			console.log(response);
			$.ajax({
				url: '/upload',
				data: {
					"photo": response
				},
				method: 'POST',
				success: function (data, textStatus, jqXHR) {
					location.reload();
				},
				error: function(error) {
					console.log(error);
					location.reload();
				}
			});
		});
	});
});

//profile crop
$image_crop = $('#upload-image').croppie({
	enableExif: true,
	viewport: {
		width: 300,
		height: 300,
		type: 'square'
	},
	boundary: {
		width: 300,
		height: 300
	}
});

//update profile box
$('#images').on('change', function () { 
	var reader = new FileReader();
	reader.onload = function (e) {
		$image_crop.croppie('bind', {
			url: e.target.result
		}).then(function(){
			console.log('jQuery bind complete');
		});			
	}
	reader.readAsDataURL(this.files[0]);
});

//************* COVER PHOTO *************

$(function() {
	$("#cover-button").on('click', function (e) {
		$image_crop.croppie('result', {
			type: 'canvas',
			size: {
				width: 600,
				height: 130,
			}
		}).then(function (response) {
			console.log(response);
			$.ajax({
				url: '/upload',
				data: {
					"cover": response
				},
				method: 'POST',
				success: function (data, textStatus, jqXHR) {
					location.reload();
				},
				error: function(error) {
					console.log(error);
				}
			});
		});
	});
});

$image_crop = $('#upload-image').croppie({
	enableExif: true,
	viewport: {
		width: 300,
		height: 300,
		type: 'square'
	},
	boundary: {
		width: 300,
		height: 300
	}
});

$('#images').on('change', function () { 
	var reader = new FileReader();
	reader.onload = function (e) {
		$image_crop.croppie('bind', {
			url: e.target.result
		}).then(function(){
			console.log('jQuery bind complete');
		});			
	}
	reader.readAsDataURL(this.files[0]);
});
