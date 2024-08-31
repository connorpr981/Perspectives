import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/layout.module.css';
import { useAuth } from '../hooks/useAuth';

const LandingPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className={`${styles.layout} ${styles.landingPage}`}>
      <main className={styles.landingContent}>
        <h1 className={styles.landingTitle}>Welcome to Perspectives</h1>
        <p className={styles.landingDescription}>Explore depth-wise.</p>
        {user ? (
          <Link to="/explore" className={styles.landingButton}>
            Start Exploring
          </Link>
        ) : (
          <Link to="/login" className={styles.landingButton}>
            Login / Sign Up
          </Link>
        )}
      </main>
    </div>
  );
};

export default LandingPage;