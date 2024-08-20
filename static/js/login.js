$(function() {
	$(".btn").click(function() {
		$(".form-signin").toggleClass("form-signin-left");
    $(".form-signup").toggleClass("form-signup-left");
    $(".frame").toggleClass("frame-long");
    $(".signup-inactive").toggleClass("signup-active");
    $(".signin-active").toggleClass("signin-inactive");
    $(".forgot").toggleClass("forgot-left");   
    $(this).removeClass("idle").addClass("active");
	});
});

// $(function() {
// 	$(".btn-signup").click(function() {
//   $(".nav").toggleClass("nav-up");
//   $(".form-signup-left").toggleClass("form-signup-down");
//   $(".success").toggleClass("success-left"); 
//   $(".frame").toggleClass("frame-short");
// 	});
// });

$(function() {
	$(".btn-signin").click(function() {
  $(".btn-animate").toggleClass("btn-animate-grow");
  $(".welcome").toggleClass("welcome-left");
  $(".cover-photo").toggleClass("cover-photo-down");
  $(".frame").toggleClass("frame-short");
  $(".profile-photo").toggleClass("profile-photo-down");
  $(".btn-goback").toggleClass("btn-goback-up");
  $(".forgot").toggleClass("forgot-fade");
	});
});


$('#submitButton').click(function(event) {
  event.preventDefault();
  var form = $('#signupForm');
  var formData = form.serialize(); 
  if (!form[0].checkValidity()) {
      $('#messageContainer').addClass("visible").text('Please fill out all required fields.');
      setTimeout(function() {
        $('#messageContainer').removeClass("visible").text("")
        }, 2000); 
      return;
  }
  $('#submitButton').prop('disabled', true);
  $('.loader').show();

  $.ajax({
      url: "/accounts/register/",
      method: 'POST',
      data: formData,
      success: function(response) {
          if (response.status === 'success') {
              $('#messageContainer').addClass("visible").text('User registered successfully!').css('color', 'green');
              setTimeout(function() {
                  window.location.href = '/accounts/login/';
              }, 2000);
          } else {
              $('#messageContainer').text('Registration failed: ' + response.message).css('color', 'red');
          }
      },
      error: function(xhr) {
          var errorMessage = 'An error occurred. Please try again.';
          if (xhr.responseJSON && xhr.responseJSON.message) {
              errorMessage = xhr.responseJSON.message;
          }
          $('#messageContainer').text(errorMessage).css('color', 'red');
      }
  });
});