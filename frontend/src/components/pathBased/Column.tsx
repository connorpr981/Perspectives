import React from 'react';
import styles from '../../styles/pathBased.module.css';

interface ColumnProps {
  children: React.ReactNode;
  className?: string;
}

export const Column = React.forwardRef<HTMLDivElement, ColumnProps>(
  ({ children, className }, ref) => (
    <div className={`${styles.column} ${className || ''}`} ref={ref}>
      <div className={styles.activeColumnIndicator} />
      {children}
    </div>
  )
);