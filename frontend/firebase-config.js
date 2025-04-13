// Import the necessary functions from the Firebase SDK
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your Firebase configuration object
export const firebaseConfig = {
  apiKey: "AIzaSyAJBubAYLVzcpMgJRkc4lPf6MXa4Zw-U00",
  authDomain: "encode-ai-hack-2025.firebaseapp.com",
  projectId: "encode-ai-hack-2025",
  storageBucket: "encode-ai-hack-2025.firebasestorage.app",
  messagingSenderId: "752008023974",
  appId: "1:752008023974:web:56bed81533b00a475f8967",
  measurementId: "G-1JF3D4ZN4L"
};

// Initialize Firebase and Firebase services
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Auth and Firestore
const auth = getAuth(app);
const db = getFirestore(app);

export { app, analytics, auth, db };
