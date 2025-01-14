document
  .getElementById("loanForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
      features: [
        parseFloat(formData.get("salary")),
        parseFloat(formData.get("loan_amount")),
        parseFloat(formData.get("age")),
        parseFloat(formData.get("interest_rate")),
        parseFloat(formData.get("remaining_term")),
        parseFloat(formData.get("outstanding_balance")),
      ],
    };

    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    const prediction = result.prediction;
    const confidence = result.confidence;
    alert(`Prediction: ${prediction} (Confidence: ${confidence.toFixed(2)}%)`);
  });
document.getElementById("loanForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const salary = document.getElementById("salary").value;
  if (salary <= 0) {
    alert("Salary must be greater than 0.");
    return;
  }
  // Add more validation rules here
  alert("Form submitted successfully!");
});
