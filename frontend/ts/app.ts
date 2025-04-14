document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form")!;
    
    form.addEventListener("submit", (event) => {
      event.preventDefault();
  
      const salary = parseFloat((<HTMLInputElement>document.getElementById("salary")).value);
      const debt = parseFloat((<HTMLInputElement>document.getElementById("debt")).value);
      const savings = parseFloat((<HTMLInputElement>document.getElementById("savings")).value);
      const modelChoice = (<HTMLSelectElement>document.getElementById("model")).value;
  
      if (!salary || !debt || !savings) {
        alert("Please fill all fields.");
        return;
      }
  
      // Send the form data to the Flask server
      fetch("/submit", {
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
      })
      .then(response => response.text())
      .then(result => {
        document.getElementById("result")!.innerHTML = result;
      })
      .catch(error => {
        console.error("Error:", error);
      });
    });
  });
  