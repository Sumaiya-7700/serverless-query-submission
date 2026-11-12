// Configuration: Replace with your actual API Gateway Invoke URL once deployed
const API_URL = "https://krg98rpskb.execute-api.ap-south-1.amazonaws.com/contact"; 

document.addEventListener("DOMContentLoaded", () => {
    const contactForm = document.getElementById("contactForm");
    const submitBtn = document.getElementById("submitBtn");
    const spinner = document.getElementById("spinner");
    const btnText = submitBtn.querySelector(".btn-text");
    const successModal = document.getElementById("successModal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    contactForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Gather form data
        const formData = {
            name: document.getElementById("name").value.trim(),
            email: document.getElementById("email").value.trim(),
            mobileno: document.getElementById("mobileno").value.trim(),
            address: document.getElementById("address").value.trim(),
            query: document.getElementById("query").value.trim()
        };

        // Client-side validation check
        if (!formData.name || !formData.email || !formData.mobileno || !formData.query) {
            alert("Please fill in all required fields.");
            return;
        }

        // Disable button & show spinner
        submitBtn.disabled = true;
        btnText.textContent = "Sending Query...";
        spinner.style.display = "inline-block";

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                // Show success modal popup
                successModal.style.display = "flex";
                contactForm.reset();
            } else {
                alert("Error: " + (result.error || "Unable to send query. Please try again."));
            }
        } catch (error) {
            console.error("Network Error:", error);
            alert("Network connection error. Please check your API URL or internet connection.");
        } finally {
            // Restore button state
            submitBtn.disabled = false;
            btnText.textContent = "Send Query";
            spinner.style.display = "none";
        }
    });

    // Close modal event
    closeModalBtn.addEventListener("click", () => {
        successModal.style.display = "none";
    });

    // Close modal when clicking outside content
    window.addEventListener("click", (e) => {
        if (e.target === successModal) {
            successModal.style.display = "none";
        }
    });
});
