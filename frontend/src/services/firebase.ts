import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signOut, setPersistence, browserLocalPersistence } from "firebase/auth";
import { getFirestore, connectFirestoreEmulator } from "firebase/firestore";
import { getAnalytics, isSupported } from "firebase/analytics";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
setPersistence(auth, browserLocalPersistence);
export const firestore = getFirestore(app);

// Connect to Firestore emulator
if (process.env.NODE_ENV === 'development') {
  connectFirestoreEmulator(firestore, 'localhost', 8080);
  console.log('Connected to Firestore emulator');
}

// Conditionally initialize analytics
export const analytics = process.env.NODE_ENV === 'production' 
  ? isSupported().then(() => getAnalytics(app)) 
  : null;

export const googleProvider = new GoogleAuthProvider();

export const logOut = () => signOut(auth);

export const initializeFirebase = () => {
  console.log("Firebase has been initialized");
};