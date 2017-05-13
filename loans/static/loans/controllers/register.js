
$(document).ready(function() {

  $("#submit").click(function() {

    console.log(JSON.stringify({
      'first_name': $("#input_first_name").val(),
      'last_name': $('#input_last_name').val(),
      'email': $('#input_email').val(),
      'password': $('#input_password').val(),
      'telephone_number': $('#input_phone_number').val()
    }));

    $.ajax({
      url: "api/v1/register",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        'first_name': $("#input_first_name").val(),
        'last_name': $('#input_last_name').val(),
        'email': $('#input_email').val(),
        'password': $('#input_password').val(),
        'telephone_number': $('#input_phone_number').val()
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

  }); // #submit.click()

});
