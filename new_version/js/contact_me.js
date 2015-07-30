$(function() {
  $("input,textarea").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      event.preventDefault()

      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var name, email, team, message, firstName, type;
      switch ($form[0].id) {
        case "contactForm":
        name = $("input#name").val();
        email = $("input#email").val();
        team = $("input#igemTeam").val();
        message = $("textarea#message").val();
        type = "Contact"
        firstName = name; // For Success/Failure Message
          break;
        case "reportForm":
        name = $("input#report_name").val();
        email = $("input#report_email").val();
        team = ""
        message = $("textarea#report_message").val();
        firstName = name; // For Success/Failure Message
        type = "Bug"

          break;

      }
      // Check for white space in name for Success/Fail message
      if (firstName.indexOf(' ') >= 0) {
        firstName = name.split(' ').slice(0, -1).join(' ');
      }
      window.location.href='mailto:ayekedavidr@wustl.edu?subject=Igem '+type+": "+name+": "+team+"&body="+message+"\nReply at "+email;

    },
    filter: function() {
      return $(this).is(":visible");
    },
  });
  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});
/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});
