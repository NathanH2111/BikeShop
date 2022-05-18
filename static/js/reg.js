$(document).ready(function () {
      $('body').on('contextmenu', function (e) {
          return false;
      });
     $('body').bind('cut copy', function (e) {
         e.preventDefault();
     });
    var strength = {
        0: 'Worst',
        1: 'Bad',
        2: 'Weak',
        3: 'Good',
        4: 'Strong',
    };
    var password = document.getElementById('password');
    var meter = document.getElementById('password-strength-meter');
    var text = document.getElementById('password-strength-text');

    password.addEventListener('input', function () {
        var val = password.value;
        var result = zxcvbn(val);
        // Update the password strength meter
        meter.value = result.score;
        // Update the text indicator
        if (val !== '') {
            text.innerHTML = 'Strength: ' + strength[result.score];
            console.log(strength);
        } else {
            text.innerHTML = '';
        }
    });
    $form = $('#rgstr'); // cache
    $form.find(':input[type="submit"]').prop('disabled', true); // disable submit btn
        $form.find(':input[type="submit"]').prop('disabled', true); // disable submit btn
        $('input').keyup(function () {
            if (
                $('#eml').val().trim() != '' && $('#adr').val().trim() != '' && $('#password').val().trim() != ''
            ) {
                console.log('fields filled');
                console.log($('#ccn').length, $('#cvv').length);
                $form.find(':input[type="submit"]').prop('disabled', false);
            }
        });
        $('input').keydown(function () {
            if ($('#eml').val().trim() == '' || $('#adr').val().trim() == '' || $('#password').val().trim() == '') {
                console.log('some fields are empty!');
                console.log($('#ccn').length, $('#cvv').length);
                $form.find(':input[type="submit"]').prop('disabled', true);
            }
        });
});
