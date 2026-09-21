const organizeForm = document.querySelector(
    'form[action="/organize"]'
);

const organizeLoading = document.getElementById(
    "organizeLoading"
);

if (organizeForm && organizeLoading) {

    organizeForm.addEventListener(
        "submit",
        function () {

            organizeLoading.style.display = "flex";

            const organizeButton =
                organizeForm.querySelector(
                    'button[type="submit"]'
                );

            if (organizeButton) {

                organizeButton.disabled = true;

                organizeButton.innerHTML =
                    "Organizing...";
            }
        }
    );
}