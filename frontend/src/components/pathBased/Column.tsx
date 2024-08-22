import React from 'react';
import styles from '../../styles/pathBased.module.css';

interface ColumnProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export const Column = React.forwardRef<HTMLDivElement, ColumnProps>(
  ({ children, title, className }, ref) => (
    <div className={`${styles.column} ${className || ''}`} ref={ref}>
      <div className={styles.activeColumnIndicator} />
      <div className={styles.columnHeader}>
        <h2 className={styles.columnTitle}>{title}</h2>
      </div>
      {children}
    </div>
  )
);