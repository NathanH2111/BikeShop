

$(document).ready(function () {
          $('body').on('contextmenu', function (e) {
              return false;
          });
     $('body').bind('cut copy', function (e) {
         e.preventDefault();
     });
        $form = $('#login'); // cache
        $form.find(':input[type="submit"]').prop('disabled', true); // disable submit btn
        $('input').keyup(function () {
            if (
                $('#Password').val().trim() != '' && $('#Username').val().trim() != ''
            ) {
                console.log('fields filled');
                console.log($('#ccn').length, $('#cvv').length);
                $form.find(':input[type="submit"]').prop('disabled', false);
            }
        });
        $('input').keydown(function () {
            if ($('#Password').val().trim() == '' || $('#Username').val().trim() == '') {
                console.log('some fields are empty!');
                console.log($('#ccn').length, $('#cvv').length);
                $form.find(':input[type="submit"]').prop('disabled', true);
            }
        });
    });
