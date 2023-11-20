// Add an event listener for the file input change event
$('#resume').on('change', function() {
    // Get the name of the file
    var fileName = $(this).val().split('\\').pop();
    // Update the label with the file name
    $('.custom-file-label').text(fileName);
    });