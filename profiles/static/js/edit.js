$(function() {
	$("#edit").on('click', function () {
		$(".user-form-input").show()
		$(".user-form-value").hide()
		$("#save").show()
		$("#edit").hide()
	});
});

$(function() {
	$("#self-picture").on('click', function () {
		$("#upload-form").toggle()
	});
});

$(function() {
	$("#save").on('click', function (e) {

		var form_data = { 
			"name": $("#user-name").val(),
			"birthday": $("#user-birthday").val(),
			"phone": $("#user-mobile").val(),
			"plex": $("#user-plex").val(),
			"major": $("#user-major").val(),
			"ritYear": $("#user-rityear").val(),
			"website": $("#user-homepage").val(),
			"resume": $("#user-resume").val(),
			"github": $("#user-github").val(),
			"twitter": $("#user-twitter").val(),
			"blog": $("#user-blog").val(),
			"google": $("#user-google").val(),
			"mail": $("#user-mail").val(),
			"nickname": $("#user-nickname").val(),
			"shell": $("#user-shell").val(),
			"minor": $("#user-minor").val(),
		};

		$.ajax({
			url: '/update',
			data: form_data,
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

$(function() {
	$("#photo-button").on('click', function (e) {
		$image_crop.croppie('result', {
			type: 'canvas',
			size: 'viewport'
		}).then(function (response) {
			$.ajax({
				url: '/upload',
				data: {
					"photo": response
				},
				method: 'POST',
				success: function (data, textStatus, jqXHR) {
				      
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
