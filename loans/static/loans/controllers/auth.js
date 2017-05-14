
$(document).ready(function() {

  $("#submit").click(function() {

    $.ajax({
      url: "api/v1/user/log_in",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        'email': $('#input_email').val(),
        'password': $('#input_password').val(),
      }),
      statusCode: {
        200: function(data) {
          window.location.replace("/");
        },
        302: function(data) {
          window.location.replace("/");
        },
        400: function(data) {
          $("#error-message").html("ERROR: " + data.responseText);
          $("#error-message").css("display", "block");
        },
        401: function(data) {
          $("#error-message").html("ERROR: " + data.responseText);
          $("#error-message").css("display", "block");
        }
      }
    }); // $.ajax
  });

});
