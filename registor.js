// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";

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
const auth = getAuth(app);
const firstName = document.getElementById('firstName').value;
const lastName = document.getElementById('lastName').value;

// const submit = document.getElementById("submit"); // Fix this
// submit.addEventListener("click", function (event) {
//   event.preventDefault();
//   console.log("Button clicked!");
 
//   const email = document.getElementById('email').value;
//   const password = document.getElementById('password').value;

//   createUserWithEmailAndPassword(auth, email, password)
//     .then((userCredential) => {
//       // Signed up 
//       const user = userCredential.user;
//       console.log("Button clicked!");
//       alert('Creating Account Please Wait...');
//       window.location.href = 'signin.html';
//     })
//     .catch((error) => {
//       console.log("Button clicked!");
//       const errorCode = error.code;
//       const errorMessage = error.message;
//       alert('Error: ' + errorMessage);
//     });
// });

// 

const submit = document.getElementById("submit");

submit.addEventListener("click", function (event) {
    event.preventDefault();
    console.log("Submit button clicked");

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("Please fill in both email and password!");
        return;
    }

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert('Account created successfully!');
            window.location.href = 'signin.html';
        })
        .catch((error) => {
            console.error(error);
            alert(`Error: ${error.message}`);
        });
});
