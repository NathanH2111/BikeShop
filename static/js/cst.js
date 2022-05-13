$(document).ready(function () {
    $('#ccn').mask('9999-9999-9999-9999');

    $form = $('#custom-form'); // cache
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
