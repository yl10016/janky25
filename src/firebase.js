// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC-3Mqf2dWK84Zw5cvdOKD25v_UT14B8Nw",
  authDomain: "ebbandecho-dfc67.firebaseapp.com",
  projectId: "ebbandecho-dfc67",
  storageBucket: "ebbandecho-dfc67.firebasestorage.app",
  messagingSenderId: "447048550825",
  appId: "1:447048550825:web:4d0f30729c6a85aec41cb8",
  measurementId: "G-DWF1T7QK4H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
export const responsesCollection = collection(db, "responses");
