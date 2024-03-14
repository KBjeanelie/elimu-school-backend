(function($) {
  'use strict';
  $.validator.setDefaults({
    submitHandler: function() {
      alert("submitted!");
    }
  });
  $(function() {
    // validate the comment form when it is submitted
    $("#commentForm").validate({
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).parent().addClass('has-danger')
        $(element).addClass('form-control-danger')
      }
    });
    // validate signup form on keyup and submit
    $("#signupForm").validate({
      rules: {
        firstname: "required",
        lastname: "required",
        username: {
          required: true,
          minlength: 2
        },
        password: {
          required: true,
          minlength: 5
        },
        confirm_password: {
          required: true,
          minlength: 5,
          equalTo: "#password"
        },
        email: {
          required: true,
          email: true
        },
        tel: {
          required: true,
          minlength: 9
        },
        topic: {
          required: "#newsletter:checked",
          minlength: 2
        },
        agree: "required"
      },
      messages: {
        firstname: "Veuillez saisir votre prénom",
        lastname: "Veuillez saisir votre nom",
        username: {
          required: "Veuillez saisir votre nom d'utilisateur",
          minlength: "Votre nom d'utilisateur doit être composé d'au moins 2 caractères"
        },
        password: {
          required: "Veuillez fournir un mot de passe",
          minlength: "Votre mot de passe doit comporter au moins 5 caractères"
        },
        confirm_password: {
          required: "Veuillez fournir un mot de passe",
          minlength: "Votre mot de passe doit comporter au moins 5 caractères",
          equalTo: "Veuillez saisir le même mot de passe que ci-dessus"
        },
        email: "Veuillez saisir une adresse électronique valide",
        tel: "Veuillez saisir un numéro de téléphone valide",
        agree: "Please accept our policy",
        topic: "Please select at least 2 topics"
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).parent().addClass('has-danger')
        $(element).addClass('form-control-danger')
      }
    });
    // propose username by combining first- and lastname
    $("#username").focus(function() {
      var firstname = $("#firstname").val();
      var lastname = $("#lastname").val();
      if (firstname && lastname && !this.value) {
        this.value = firstname + "." + lastname;
      }
    });
    //code to hide topic selection, disable for demo
    var newsletter = $("#newsletter");
    // newsletter topics are optional, hide at first
    var inital = newsletter.is(":checked");
    var topics = $("#newsletter_topics")[inital ? "removeClass" : "addClass"]("gray");
    var topicInputs = topics.find("input").attr("disabled", !inital);
    // show when newsletter is checked
    newsletter.on("click", function() {
      topics[this.checked ? "removeClass" : "addClass"]("gray");
      topicInputs.attr("disabled", !this.checked);
    });
  });
})(jQuery);