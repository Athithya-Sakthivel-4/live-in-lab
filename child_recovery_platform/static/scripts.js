// ✅ Image Preview (Upload Page)
document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageUpload");
    const previewImage = document.getElementById("previewImage");

    if (imageInput) {
        imageInput.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    previewImage.classList.remove("d-none");
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// ✅ Live Search (Database Page)
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const children = document.querySelectorAll(".child-card");

    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            let filter = this.value.toLowerCase();
            children.forEach(child => {
                let name = child.querySelector(".card-title").innerText.toLowerCase();
                child.style.display = name.includes(filter) ? "block" : "none";
            });
        });
    }
});
