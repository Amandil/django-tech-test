
$(document).ready(function() {

  $("#submit").click(function() {

        console.log(JSON.stringify({
          'email': $('#input_email').val(),
          'password': $('#input_password').val(),
        }));

        $.ajax({
          url: "api/v1/log_in",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify({
            'email': $('#input_email').val(),
            'password': $('#input_password').val(),
          }),
          statusCode: {
            200: function(data) {
              document.location.href="/";
            },
            400: function(data) {
              $("#error-message").html("ERROR: " + data.responseText);

            }
          }
        }); // $.ajax
  });

});
