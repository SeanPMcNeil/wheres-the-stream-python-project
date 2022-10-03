document.addEventListener('DOMContentLoaded', function () {
    M.AutoInit();
});

$(document).ready(function() {
    $('input#input_text, textarea#textarea2').characterCounter();
    M.updateTextFields();
    $('.collapsible').collapsible();
    $('.sidenav').sidenav();
});
