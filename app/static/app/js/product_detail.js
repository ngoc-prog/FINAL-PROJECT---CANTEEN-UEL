document.addEventListener("DOMContentLoaded", function () {
    // Quantity control functionality
    const quantityInput = document.getElementById("quantity");
    const minusButton = document.getElementById("button-minus");
    const plusButton = document.getElementById("button-plus");

    if (quantityInput && minusButton && plusButton) {
        function updateQuantity(change) {
            let currentValue = parseInt(quantityInput.value) || 1;
            let newValue = currentValue + change;

            if (newValue < 1) {
                newValue = 1;
            }

            quantityInput.value = newValue;
            updateTotalPrice();
        }

        plusButton.addEventListener("click", function () {
            updateQuantity(1);
        });

        minusButton.addEventListener("click", function () {
            updateQuantity(-1);
        });

        quantityInput.addEventListener("input", function () {
            let value = parseInt(quantityInput.value);
            if (isNaN(value) || value < 1) {
                quantityInput.value = 1;
            }
            updateTotalPrice();
        });
    }

    // Price calculation functionality
    function updateTotalPrice() {
        const basePrice = parseFloat(document.getElementById("product-price").dataset.basePrice) || 0;
        const sizeModifier = parseFloat(document.querySelector("input[name='size']:checked").dataset.priceModifier) || 0;
        const quantity = parseInt(quantityInput.value) || 1;
        const totalPrice = (basePrice + sizeModifier) * quantity;

        document.getElementById("product-price").textContent = totalPrice.toLocaleString("vi-VN") + " VND";
    }

    document.querySelectorAll(".size-option").forEach(option => {
        option.addEventListener("change", updateTotalPrice);
    });

    updateTotalPrice();

    // Feedback form submission with AJAX
    const feedbackForm = document.getElementById("feedback-form");
    
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const formData = new FormData(feedbackForm);
            const url = feedbackForm.getAttribute("action");
            
            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                credentials: "same-origin",
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // Create new feedback element
                    const newFeedback = document.createElement("div");
                    newFeedback.classList.add("card", "mt-3");
                    
                    // Format date nicely
                    const date = new Date();
                    const formattedDate = `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
                    
                    // Create stars HTML
                    let starsHtml = '';
                    for (let i = 1; i <= 5; i++) {
                        if (i <= data.rating) {
                            starsHtml += '<i class="fa fa-star"></i>';
                        } else {
                            starsHtml += '<i class="far fa-star"></i>';
                        }
                    }
                    
                    // Populate feedback HTML
                    newFeedback.innerHTML = `
                        <div class="card-body">
                            <h5 class="card-title">${data.username}</h5>
                            <p class="card-text">${data.comment}</p>
                            <p class="text-warning">${starsHtml}</p>
                            <small class="text-muted">${formattedDate}</small>
                        </div>
                    `;
                    
                    // Add the new feedback to the top of the list
                    const feedbackList = document.getElementById("feedback-list");
                    
                    // If there's an alert saying "no feedback yet", remove it
                    const noFeedbackAlert = feedbackList.querySelector(".alert");
                    if (noFeedbackAlert) {
                        noFeedbackAlert.remove();
                    }
                    
                    // Add new feedback at the top
                    feedbackList.insertBefore(newFeedback, feedbackList.firstChild);
                    
                    // Reset the form
                    feedbackForm.reset();
                    
                    // Show success message
                    const successAlert = document.createElement("div");
                    successAlert.classList.add("alert", "alert-success", "mt-3");
                    successAlert.textContent = "Đánh giá của bạn đã được gửi thành công!";
                    feedbackForm.insertAdjacentElement("beforebegin", successAlert);
                    
                    // Remove success message after 3 seconds
                    setTimeout(() => {
                        successAlert.remove();
                    }, 3000);
                } else {
                    // Show error message
                    const errorAlert = document.createElement("div");
                    errorAlert.classList.add("alert", "alert-danger", "mt-3");
                    errorAlert.textContent = data.message || "Đã xảy ra lỗi khi gửi đánh giá.";
                    feedbackForm.insertAdjacentElement("beforebegin", errorAlert);
                    
                    // Remove error message after 3 seconds
                    setTimeout(() => {
                        errorAlert.remove();
                    }, 3000);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                // Show error message
                const errorAlert = document.createElement("div");
                errorAlert.classList.add("alert", "alert-danger", "mt-3");
                errorAlert.textContent = "Đã xảy ra lỗi khi gửi đánh giá.";
                feedbackForm.insertAdjacentElement("beforebegin", errorAlert);
                
                // Remove error message after 3 seconds
                setTimeout(() => {
                    errorAlert.remove();
                }, 3000);
            });
        });
    }
});