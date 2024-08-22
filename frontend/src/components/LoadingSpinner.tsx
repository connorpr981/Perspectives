import React from 'react';
import styles from '../styles/loadingSpinner.module.css';

const LoadingSpinner: React.FC = () => (
  <div className={styles.spinnerOverlay}>
    <div className={styles.spinner}></div>
  </div>
);

export default LoadingSpinner;