const predictForm = document.getElementById('predictForm');
const resultDiv = document.getElementById('result');

predictForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const data = {
        Country: document.getElementById('country').value,
        University: document.getElementById('university').value,
        Program: document.getElementById('program').value,
        Level: document.getElementById('level').value,
        Duration_Years: document.getElementById('duration_years').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = `Predicted Total Expenditure: $${result.prediction.toFixed(2)}`;
        } else {
            resultDiv.innerHTML = `Error: ${result.error}`;
        }
    } catch (error) {
        resultDiv.innerHTML = `Request failed: ${error.message}`;
    }
});
