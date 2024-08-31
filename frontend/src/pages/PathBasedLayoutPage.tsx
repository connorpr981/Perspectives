import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  PathSelectableColumn, 
  SavedPathsPanel, 
  SidePane 
} from '../components/pathBased';
import { LayoutConfig, ItemType } from '../types/pathBased';
import layoutStyles from '../styles/layout.module.css';
import styles from '../styles/pathBased.module.css';
import { fetchTranscriptData } from '../services/firestoreService';
import { transformTranscriptData } from '../utils/dataTransformers';
import { useColumnScroll } from '../hooks/useColumnScroll';
import { usePathNavigation } from '../hooks/usePathNavigation';
import { useLoading } from '../context/LoadingContext';
import { useTheme } from '../hooks/useTheme';
import { KEYBOARD_SHORTCUTS } from '../constants/keyboardShortcuts';
import { useTranscript } from '../context/TranscriptContext';
import LoadingSpinner from '../components/LoadingSpinner';

const defaultLayoutConfig: LayoutConfig = {
  columns: [
    { title: 'Sections' },
    { title: 'Turns' },
    { title: 'Questions' },
    { title: 'Perspectives' },
  ]
};

const PathBasedLayoutPage: React.FC = () => {
  const { transcriptId } = useTranscript();
  const { isLoading, setIsLoading } = useLoading();
  const [config] = useState<LayoutConfig>(defaultLayoutConfig);
  const [rootItem, setRootItem] = useState<ItemType | null>(null);
  const [isSidePaneExpanded, setIsSidePaneExpanded] = useState(false);
  const columnsWrapperRef = useRef<HTMLDivElement>(null);
  const toggleButtonRef = useRef<HTMLButtonElement>(null);
  const { theme, toggleTheme } = useTheme();
  const [fetchError, setFetchError] = useState<string | null>(null);

  const {
    path,
    getItemsForColumn,
    savedPaths,
    loadSavedPath,
    savePath,
    draftPath,
    resumeDraftPath,
    handleSelect,
    highlightedSavedPathId
  } = usePathNavigation(config, rootItem, columnsWrapperRef);

  const { activeColumnIndex, scrollToActiveColumn, scrollColumnIntoView } = useColumnScroll(config, path, columnsWrapperRef);

  useEffect(() => {
    scrollToActiveColumn();
  }, [scrollToActiveColumn]);

  useEffect(() => {
    let isMounted = true;

    const fetchTranscript = async () => {
      if (transcriptId) {
        setIsLoading(true);
        setFetchError(null);
        try {
          console.log('Fetching transcript with ID:', transcriptId);
          const data = await fetchTranscriptData(transcriptId);
          console.log('Fetched data:', data);
          const processedData = transformTranscriptData(data);
          console.log('Processed data:', processedData);
          if (isMounted) {
            setRootItem(processedData);
          }
        } catch (error) {
          console.error("Error fetching transcript:", error);
          // if (isMounted) {
          //   setFetchError("Failed to load transcript. Please try again.");
          // }
        } finally {
          if (isMounted) {
            setIsLoading(false);
          }
        }
      } else {
        // If there's no transcriptId, just set loading to false
        setIsLoading(false);
      }
    };

    fetchTranscript();

    return () => {
      isMounted = false;
    };
  }, [transcriptId, setIsLoading]);

  const toggleSidePane = useCallback(() => {
    setIsSidePaneExpanded(prev => !prev);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        toggleSidePane();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [toggleSidePane]);

  useEffect(() => {
    const preventArrowKeyDefault = (e: KeyboardEvent) => {
      if ([KEYBOARD_SHORTCUTS.NAVIGATE_UP, KEYBOARD_SHORTCUTS.NAVIGATE_DOWN, KEYBOARD_SHORTCUTS.NAVIGATE_LEFT, KEYBOARD_SHORTCUTS.NAVIGATE_RIGHT].includes(e.key)) {
        e.preventDefault();
      }
    };

    window.addEventListener('keydown', preventArrowKeyDefault);

    return () => {
      window.removeEventListener('keydown', preventArrowKeyDefault);
    };
  }, []);

  return (
    <div className={layoutStyles.layout}>
      <header className={layoutStyles.header}>
        <h1>Perspectives</h1>
      </header>
      <div className={layoutStyles.mainLayout}>
        <SidePane
          isExpanded={isSidePaneExpanded}
          onClose={toggleSidePane}
          theme={theme}
          toggleTheme={toggleTheme}
        />
        {isSidePaneExpanded && <div className={layoutStyles.overlay} onClick={toggleSidePane} />}
        <div className={layoutStyles.mainContentWrapper}>
          {isLoading ? (
            <LoadingSpinner />
          ) : fetchError ? (
            <div className={styles.errorMessage}>{fetchError}</div>
          ) : (
            <div className={layoutStyles.columnsWrapper} ref={columnsWrapperRef}>
              <div className={`${layoutStyles.columnsContainer} ${styles.columnsContainer}`}>
                {config.columns.map((columnConfig, colIndex) => (
                  <PathSelectableColumn
                    key={colIndex}
                    config={columnConfig}
                    items={getItemsForColumn(colIndex)}
                    onSelect={handleSelect}
                    path={path}
                    columnIndex={colIndex}
                    isActive={colIndex === activeColumnIndex}
                    scrollColumnIntoView={scrollColumnIntoView}
                    observe={() => {}}
                    activeColumnIndex={activeColumnIndex}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
        <div className={layoutStyles.savedPathsPanelWrapper}>
          <SavedPathsPanel
            savedPaths={savedPaths}
            loadSavedPath={loadSavedPath}
            onSavePath={savePath}
            isFullPathSelected={path.length === config.columns.length}
            draftPath={draftPath}
            onResumeDraft={resumeDraftPath}
            onToggleSidePane={toggleSidePane}
            toggleButtonRef={toggleButtonRef}
            highlightedSavedPathId={highlightedSavedPathId}
            isSidePaneExpanded={isSidePaneExpanded}
          />
        </div>
      </div>
    </div>
  );
};

export default PathBasedLayoutPage;