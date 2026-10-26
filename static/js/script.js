// CleanCity AI - Shared JavaScript

document.addEventListener("DOMContentLoaded", function () {
    console.log("CleanCity AI loaded successfully.");

    // Confirm before deleting an item
    document.querySelectorAll(".delete-btn").forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = confirm(
                "Are you sure you want to delete this item?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // Preview uploaded images
    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("imagePreview");

    if (imageInput && imagePreview) {
        imageInput.addEventListener("change", function () {
            const file = this.files && this.files[0];

            if (!file) {
                imagePreview.src = "";
                imagePreview.style.display = "none";
                return;
            }

            if (!file.type.startsWith("image/")) {
                alert("Please select a valid image file.");
                this.value = "";
                imagePreview.style.display = "none";
                return;
            }

            imagePreview.src = URL.createObjectURL(file);
            imagePreview.style.display = "block";
        });
    }

    // Automatically dismiss success messages
    document.querySelectorAll("[data-auto-dismiss]").forEach(function (alertBox) {
        setTimeout(function () {
            alertBox.style.display = "none";
        }, 5000);
    });

    // Update the displayed file name
    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");

    if (fileInput && fileName) {
        fileInput.addEventListener("change", function () {
            fileName.textContent =
                this.files.length > 0
                    ? this.files[0].name
                    : "No file selected";
        });
    }
});