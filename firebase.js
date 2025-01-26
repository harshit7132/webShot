// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore"; // 🔥 Firestore imports

// Your web app's Firebase configuration 
const firebaseConfig = {
  apiKey: "AIzaSyAT53j_k9Alzr7O2HDmeQ8_tfZTdQnde48",
  authDomain: "webshot-c0c2a.firebaseapp.com",
  databaseURL: "https://webshot-c0c2a-default-rtdb.firebaseio.com",
  projectId: "webshot-c0c2a",
  storageBucket: "webshot-c0c2a.firebasestorage.app",
  messagingSenderId: "917217158557",
  appId: "1:917217158557:web:4715f7e0bf7208cf79bb74",
  measurementId: "G-E8JJ3NZ6KE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase Auth
const auth = getAuth(app);

// 🔥 Initialize Firestore
const db = getFirestore(app); // Firestore instance

// 🛠️ Sign Up Function with Firestore Data
export const signUpWithEmailPassword = async (firstName, lastName, email, password) => {
  try {
    // Create user in Firebase Authentication
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // 🛠️ Add User Data to Firestore (Store user's name, email, and UID)
    await setDoc(doc(db, 'users', user.uid), {
      firstName: firstName,
      lastName: lastName,
      email: email,
      password: password,
      uid: user.uid,
      createdAt: new Date().toISOString()
    });

    console.log('User Signed Up and Data Saved:', user);
    alert('User Signed Up Successfully');
    return user;
  } catch (error) {
    console.error('Error Signing Up:', error.message);
    alert(`Error: ${error.message}`);
    throw error;
  }
};

// 🛠️ Login Function
export const loginWithEmailPassword = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    console.log('User Logged In:', user);
    alert('User Logged In Successfully');
    return user;
  } catch (error) {
    console.error('Error Logging In:', error.message);
    alert(`Error: ${error.message}`);
    throw error;
  }
};

// Export the app, auth, analytics, and db for use throughout the project
export { app, analytics, auth, db };
