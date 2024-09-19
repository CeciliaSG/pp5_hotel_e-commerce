    /* global bootstrap */
    
    
document.addEventListener("DOMContentLoaded", () => {
    const editButtons = document.querySelectorAll(".btn-edit");
    const reviewText = document.getElementById("id_body");
    const reviewForm = document.getElementById("reviewForm");
    const submitButton = document.getElementById("submitButton");

    /**
     * Initialises edit functionality for the provided edit buttons.
     * 
     * For each button in the `editButtons` collection:
     * - Retrieves the associated review's ID upon click.
     * - Fetches the content of the corresponding review.
     * - Populates the `commentText` input/textarea with the review's content for editing.
     * - Updates the submit button's text to "Update".
     * - Sets the form's action attribute to the `edit_review/{reviewId}` endpoint.
     */
    editButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            try {
                const reviewId = e.target.getAttribute("data-review-id");
                const reviewContent = document.getElementById(`review${reviewId}`).innerText;
                reviewText.value = reviewContent;
                submitButton.innerText = "Update";
                reviewForm.setAttribute("action", `edit_review/${reviewId}`);
            } catch (error) {
                alert("An error occurred while loading the review for editing. Please try again.");
            }
        });
    });

    /*
     * Initialises deletion functionality for the provided delete buttons.
     * 
     * For each button in the `deleteButtons` collection:
     * - Retrieves the associated review's ID upon click.
     * - Updates the `deleteConfirm` link's href to point to the 
     *   deletion endpoint for the specific review.
     * - Displays a confirmation modal (`deleteModal`) to prompt 
     *   the user for confirmation before deletion.
     */

    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");

    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            try {
                let reviewId = e.target.getAttribute("data-review-id");
                deleteConfirm.href = `delete_review/${reviewId}`;
                deleteModal.show();
            } catch (error) {
                alert("An error occurred while preparing the deletion. Please try again.");
            }
        });

        deleteConfirm.addEventListener('click', (e) => {
            try {
                window.location.href = deleteConfirm.href;
            } catch (error) {
                alert("Failed to delete the review. Please try again.");
            }
        });
    }
});
