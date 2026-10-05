document.addEventListener("DOMContentLoaded", function () {

    var forms = document.querySelectorAll(".delete-form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            var answer = confirm("Are you sure you want to delete this record?");

            if (!answer) {
                event.preventDefault();
            }
        });
    });

});
