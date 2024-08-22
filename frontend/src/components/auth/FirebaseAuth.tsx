import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFirebaseAuth } from '../../hooks/useFirebaseAuth';
import styles from '../../styles/auth.module.css';
import { FcGoogle } from 'react-icons/fc';

const FirebaseAuth: React.FC = () => {
  const navigate = useNavigate();
  const { error, loading, handleGoogleAuth } = useFirebaseAuth();

  const handleAuth = async () => {
    const success = await handleGoogleAuth();
    if (success) {
      navigate('/explore');
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authForm}>
        <h2 className={styles.authTitle}>Welcome to Perspectives</h2>
        <button 
          onClick={handleAuth} 
          className={styles.googleButton} 
          disabled={loading}
        >
          <FcGoogle className={styles.googleIcon} />
          {loading ? 'Signing in...' : 'Continue with Google'}
        </button>
        {error && <p className={styles.error} role="alert">{error}</p>}
      </div>
    </div>
  );
};

export default FirebaseAuth;