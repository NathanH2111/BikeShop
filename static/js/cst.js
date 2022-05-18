$(document).ready(function () {
      $('body').on('contextmenu', function (e) {
          return false;
      });
     $('body').bind('cut copy', function (e) {
         e.preventDefault();
     });

    $form = $('#custom-form'); // cache
    $form.find(':input[type="submit"]').prop('disabled', true); // disable submit btn
    $('input').keyup(function () {
        if ($('#ccn').val().trim() != '' && $('#cvv').val().trim() != '') {
            console.log('fields filled');
            console.log($('#ccn').length, $('#cvv').length);
            $form.find(':input[type="submit"]').prop('disabled', false);
        }
    });
        $('input').keydown(function () {
            if ($('#ccn').val().trim() == '' || $('#cvv').val().trim() == '') {
                console.log('some fields are empty!');
                console.log($('#ccn').length, $('#cvv').length);
                $form.find(':input[type="submit"]').prop('disabled', true);
            }
            });
});

