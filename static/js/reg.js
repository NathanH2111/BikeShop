$(document).ready(function () {
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
    $form.find(':input').change(function () {
        // monitor all inputs for changes
        var disable = false;
        $form
            .find(':input')
            .not('[type="submit"]')
            .each(function (i, el) {
                // test all inputs for values
                if ($.trim(el.value) === '') {
                    disable = true; // disable submit if any of them are still blank
                }
            });
        $form.find(':input[type="submit"]').prop('disabled', disable);
    });
});
