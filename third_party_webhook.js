$('input[type="checkbox"]').on('change', function() {
    $('input[type="checkbox"]').not(this).prop('checked', false);
    document.getElementById("save-webhook").disabled=false;
 });
document.getElementById("save-webhook").disabled=true;
