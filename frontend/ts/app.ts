// app.ts
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#credit-score-form") as HTMLFormElement;
  const resultDiv = document.getElementById("result") as HTMLDivElement;
  
  form.addEventListener("submit", async (event) => {
      event.preventDefault();

      // Get the input values
      const salary = parseFloat((document.getElementById("salary") as HTMLInputElement).value);
      const debt = parseFloat((document.getElementById("debt") as HTMLInputElement).value);
      const savings = parseFloat((document.getElementById("savings") as HTMLInputElement).value);
      const modelChoice = (document.getElementById("model") as HTMLSelectElement).value;

      // Simple validation
      if (isNaN(salary) || isNaN(debt) || isNaN(savings)) {
          resultDiv.innerHTML = "<p class='error'>Please fill all fields with valid numbers</p>";
          resultDiv.style.display = "block";
          return;
      }

      // Show loading indicator
      resultDiv.innerHTML = "<p>Processing your request...</p>";
      resultDiv.style.display = "block";

      try {
          const response = await fetch("/submit", {
              method: "POST",
              headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
              },
              body: new URLSearchParams({
                  salary: salary.toString(),
                  debt: debt.toString(),
                  savings: savings.toString(),
                  model: modelChoice
              })
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

          const resultHtml = await response.text();
          resultDiv.innerHTML = resultHtml;
          
      } catch (error) {
          console.error("Error:", error);
          resultDiv.innerHTML = `<p class="error">Error: ${error instanceof Error ? error.message : "Unknown error"}</p>`;
      }
  });
});