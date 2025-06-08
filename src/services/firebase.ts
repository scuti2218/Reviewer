// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  indexedDBLocalPersistence,
} from "firebase/auth";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getDatabase } from "firebase/database";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDjmX30TLR9T_IQTVeKb05X1Rf0G_Ccl0Q",
  authDomain: "reviewer-fdc2a.firebaseapp.com",
  projectId: "reviewer-fdc2a",
  storageBucket: "reviewer-fdc2a.firebasestorage.app",
  messagingSenderId: "84575196797",
  appId: "1:84575196797:web:b7a30f99b5d297dc3e4314",
  measurementId: "G-99S428W862",
  databaseURL:
    "https://reviewer-fdc2a-default-rtdb.asia-southeast1.firebasedatabase.app",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
auth.setPersistence(indexedDBLocalPersistence);
const provider = new GoogleAuthProvider();
const db = getFirestore(app);
const rdb = getDatabase(app);

export { analytics, auth, provider, db, rdb };
