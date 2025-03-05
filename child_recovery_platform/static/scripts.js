document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("preview");
    const resultDiv = document.getElementById("result");

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.classList.remove("d-none");
            };
            reader.readAsDataURL(file);
        }
    });

    document.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();
        resultDiv.textContent = "Processing...";
        resultDiv.classList.remove("d-none");

        const formData = new FormData(this);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            resultDiv.textContent = data;
            resultDiv.classList.add("alert-success");
        })
        .catch(error => {
            resultDiv.textContent = "Error processing image.";
            resultDiv.classList.add("alert-danger");
        });
    });
});
