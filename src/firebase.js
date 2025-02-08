// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAVuHJSx73ahoE3iChdEU1MnaBGfr1crQA",
  authDomain: "tides-4e9cd.firebaseapp.com",
  projectId: "tides-4e9cd",
  storageBucket: "tides-4e9cd.firebasestorage.app",
  messagingSenderId: "770702608278",
  appId: "1:770702608278:web:e09b7111dfed0961487fb7",
  measurementId: "G-VDSLQV9XB6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
export const responsesCollection = collection(db, "responses");
