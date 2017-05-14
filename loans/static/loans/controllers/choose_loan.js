
$(document).ready(function() {

  $("#submit").click(function() {

    amount = $(".ws-number", $("#input_amount_area")).val().replace(',','');

    $.ajax({
      url: "/api/v1/loan/add",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        'crn': $("#input_crn").val(),
        'amount': amount,
        'deadline': $('#input_deadline').val(),
        'reason': $('#input_reason').val(),
      }),
      statusCode: {
        200: function(data) {
          window.location.replace("/apply/loan-application/4/");
        },
        400: function(data) {
          $("#error-message").html("ERROR: " + data.responseText);
          $("#error-message").css("display", "block");
        }
      }
    }); // $.ajax

  }); // #submit.click()

});
