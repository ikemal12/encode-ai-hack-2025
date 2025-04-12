document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#credit-score-form")!;
    const resultDiv = document.getElementById("result")!;
    
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
  
      // Get the input values
      const salary = parseFloat((<HTMLInputElement>document.getElementById("salary")).value);
      const debt = parseFloat((<HTMLInputElement>document.getElementById("debt")).value);
      const savings = parseFloat((<HTMLInputElement>document.getElementById("savings")).value);
      const modelChoice = (<HTMLSelectElement>document.getElementById("model")).value;
  
      // Simple validation to check if fields are filled
      if (!salary || !debt || !savings) {
        alert("Please fill all fields.");
        return;
      }
  
      // Show loading indicator (you can replace with a spinner or loading text)
      resultDiv.innerHTML = "Estimating your credit score...";
      resultDiv.style.display = "block";
  
      // Send the data to the backend (Flask API)
      try {
        const response = await fetch("/submit", {
          method: "POST",
          body: new URLSearchParams({
            salary: salary.toString(),
            debt: debt.toString(),
            savings: savings.toString(),
            model: modelChoice
          }),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          }
        });
  
        if (!response.ok) {
          throw new Error("Failed to get response from the server.");
        }
  
        const result = await response.text();
        
        // Display the result
        resultDiv.innerHTML = `Your estimated credit score is: ${result}`;
        resultDiv.style.backgroundColor = "#dff0d8";  // Green background for success
  
      } catch (error) {
        // Handle any errors
        resultDiv.innerHTML = "Sorry, there was an error estimating your credit score.";
        resultDiv.style.backgroundColor = "#f2dede";  // Red background for error
      }
    });
  });
  