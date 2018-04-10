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


			var photo = $("#photo").val();
			$.ajax({
				url: '/upload',
				data: {
					"photo": photo
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
