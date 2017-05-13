
$(document).ready(function() {

  $("#submit").click(function() {

    $.ajax({
      url: "api/v1/register",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(JSON.stringify({
        'crn': $("#input_crn").val(),
        'business_name': $('#input_name').val(),
        'sector': $('#input_sector').val(),
        'address_1': $('#input_address_1').val(),
        'address_2': $('#input_address_2').val(),
        'city': $('#input_city').val(),
        'postcode': $('#input_postcode').val(),
      })),
      statusCode: {
        200: function(data) {
          document.location.replace("apply/loan-application/3/" + $("#input_crn").val());
        },
        400: function(data) {
          $("#error-message").html("ERROR: " + data.responseText);
          $("#error-message").css("display", "");
        }
      }
    }); // $.ajax

  }); // #submit.click()

});
