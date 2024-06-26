document.addEventListener("DOMContentLoaded", function() {
    const titleInput = document.getElementById("title");
    const contentInput = document.getElementById("content");

    const titleRegex = /^[a-zA-Z0-9\s]+$/;
    const contentRegex = /^.{1,500}$/;

    titleInput.addEventListener("input", function() {
        if (!titleRegex.test(titleInput.value)) {
            titleInput.setCustomValidity("Title must contain only letters, numbers, and spaces");
        } else {
            titleInput.setCustomValidity("");
        }
    });

    contentInput.addEventListener("input", function() {
        if (!contentRegex.test(contentInput.value)) {
            contentInput.setCustomValidity("Content must be between 1 and 500 characters");
        } else {
            contentInput.setCustomValidity("");
        }
    });
});
