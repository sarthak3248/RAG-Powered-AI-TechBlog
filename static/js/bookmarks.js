const bookmarkButton = document.getElementById("bookmark-button");

if (bookmarkButton) {

    bookmarkButton.addEventListener("click", function () {

        fetch(bookmarkUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data.bookmarked) {
                bookmarkButton.innerHTML = "✅ Saved";
            } else {
                bookmarkButton.innerHTML = "🔖 Save";
            }

        });

    });

}