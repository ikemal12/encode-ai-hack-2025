// app.ts
import { firebaseConfig } from '../firebase-config'; 
import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { getFirestore, collection, addDoc } from "firebase/firestore";

// Initialize Firebase with the imported config
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Your existing DOMContentLoaded function
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

  // Example of Firebase Auth: Sign Up New User
  const signUpButton = document.querySelector("#sign-up-button") as HTMLButtonElement;
  signUpButton?.addEventListener("click", async () => {
    const email = (document.querySelector("#email") as HTMLInputElement).value;
    const password = (document.querySelector("#password") as HTMLInputElement).value;
    
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log("User created:", userCredential.user);
    } catch (error) {
      console.error("Error signing up:", error);
    }
  });

  // Example of Firebase Auth: Login User
  const loginButton = document.querySelector("#login-button") as HTMLButtonElement;
  loginButton?.addEventListener("click", async () => {
    const email = (document.querySelector("#email") as HTMLInputElement).value;
    const password = (document.querySelector("#password") as HTMLInputElement).value;

    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      console.log("User logged in:", userCredential.user);
    } catch (error) {
      console.error("Error logging in:", error);
    }
  });

  // Save Estimate/Query to Firestore
  const saveEstimate = async (userId: string, estimateData: any) => {
    try {
      const docRef = await addDoc(collection(db, "estimates"), {
        userId: userId,
        estimateData: estimateData,
        timestamp: new Date()
      });
      console.log("Document written with ID: ", docRef.id);
    } catch (e) {
      console.error("Error adding document: ", e);
    }
  };
});
