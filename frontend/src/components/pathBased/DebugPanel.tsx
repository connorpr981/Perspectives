import React, { useState } from 'react';
import { PathType, ItemType } from '../../types/pathBased';
import styles from '../../styles/pathBased.module.css';

interface DebugPanelProps {
  path: PathType;
  items: ItemType;
}

export const DebugPanel: React.FC<DebugPanelProps> = ({ path, items }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={styles.debugPanel}>
      <h3 className={styles.debugTitle}>Debug Info</h3>
      <p>Current Path: {JSON.stringify(path)}</p>
      <button onClick={() => setExpanded(!expanded)}>
        {expanded ? 'Hide' : 'Show'} Items Structure
      </button>
      {expanded && (
        <pre className={styles.itemsJson} data-testid="items-json">
          {JSON.stringify(items, null, 2)}
        </pre>
      )}
    </div>
  );
};