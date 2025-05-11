document.getElementById('initiate-payment-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    const jsonData = Object.fromEntries(formData.entries()); // Convert form data to JSON

    try {
        const response = await fetch('/payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });

        if (response.ok) {
            alert('Payment submitted successfully!');
        } else {
            alert('Failed to submit payment.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while submitting the payment.');
    }
});