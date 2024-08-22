import { useState } from 'react';
import { auth } from '../services/firebase';
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

export const useFirebaseAuth = () => {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleGoogleAuth = async (): Promise<boolean> => {
    setError(null);
    setLoading(true);

    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      return true;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    } finally {
      setLoading(false);
    }
  };

  const getErrorMessage = (error: unknown): string => {
    if (error instanceof Error) {
      if (error.message.includes('auth/popup-closed-by-user')) {
        return 'Sign-in cancelled. Please try again.';
      }
      return error.message;
    }
    return 'An unexpected error occurred. Please try again.';
  };

  return { error, loading, handleGoogleAuth };
};