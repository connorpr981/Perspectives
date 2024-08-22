import React, { useEffect, useCallback } from 'react';
import { SavedPath, PathType } from '../../types/pathBased';
import styles from '../../styles/pathBased.module.css';
import { KEYBOARD_SHORTCUTS } from '../../constants/keyboardShortcuts';
import { FaSave, FaPlay, FaBars, FaTimes } from 'react-icons/fa';

interface SavedPathsPanelProps {
  savedPaths: SavedPath[];
  loadSavedPath: (savedPath: SavedPath) => void;
  onSavePath: () => void;
  isFullPathSelected: boolean;
  draftPath: PathType | null;
  onResumeDraft: () => void;
  onToggleSidePane: () => void;
  toggleButtonRef: React.RefObject<HTMLButtonElement>;
  highlightedSavedPathId: string | null;
  isSidePaneExpanded: boolean;
}

export const SavedPathsPanel: React.FC<SavedPathsPanelProps> = ({
  savedPaths,
  loadSavedPath,
  onSavePath,
  isFullPathSelected,
  draftPath,
  onResumeDraft,
  onToggleSidePane,
  toggleButtonRef,
  highlightedSavedPathId,
  isSidePaneExpanded
}) => {
  const handleKeyPress = useCallback((e: KeyboardEvent) => {
    if (e.key === KEYBOARD_SHORTCUTS.SAVE_PATH && isFullPathSelected) {
      e.preventDefault();
      onSavePath();
    }
  }, [isFullPathSelected, onSavePath]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  const handleSavePath = () => {
    onSavePath();
    if (draftPath) {
      onResumeDraft();
    }
  };

  return (
    <footer className={styles.savedPathsPanel}>
      <button 
        ref={toggleButtonRef}
        className={styles.sidePaneToggle}
        onClick={onToggleSidePane}
        title={isSidePaneExpanded ? "Close Side Pane" : "Open Side Pane"}
      >
        {isSidePaneExpanded ? (
          <FaTimes data-testid="close-icon" />
        ) : (
          <FaBars data-testid="open-icon" />
        )}
      </button>
      <div className={styles.savedPathsContainer}>
        {savedPaths.map((savedPath, index) => (
          <button 
            key={savedPath.id} 
            onClick={() => loadSavedPath(savedPath)}
            className={`${styles.pathButton} ${savedPath.id === highlightedSavedPathId ? styles.highlightedPath : ''}`}
            title={`Load Path ${index + 1}`}
          >
            Path {index + 1}
          </button>
        ))}
      </div>
      {draftPath && (
        <button 
          onClick={onResumeDraft}
          className={styles.resumePathButton}
          title="Resume Draft Path"
        >
          <FaPlay data-testid="resume-icon" />
        </button>
      )}
      <button 
        className={styles.savePathButton} 
        onClick={handleSavePath}
        disabled={!isFullPathSelected}
        title={isFullPathSelected ? "Save Current Path" : "Complete path to save"}
      >
        <FaSave data-testid="save-icon" />
      </button>
    </footer>
  );
};