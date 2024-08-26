import { useState, useCallback, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ItemType, PathType, SavedPath, LayoutConfig } from '../types/pathBased';
import { KEYBOARD_SHORTCUTS } from '../constants/keyboardShortcuts';

export const usePathNavigation = (
  config: LayoutConfig,
  rootItem: ItemType | null,
  columnsWrapperRef: React.RefObject<HTMLDivElement>
) => {
  const [path, setPath] = useState<PathType>([]);
  const [items, setItems] = useState<ItemType | null>(null);
  const [savedPaths, setSavedPaths] = useState<SavedPath[]>([]);
  const [draftPath, setDraftPath] = useState<PathType | null>(null);
  const [lastLoadedSavedPath, setLastLoadedSavedPath] = useState<PathType | null>(null);
  const [highlightedSavedPathId, setHighlightedSavedPathId] = useState<string | null>(null);

  useEffect(() => {
    if (rootItem) {
      setItems(rootItem);
    }
  }, [rootItem]);

  const getItemsForColumn = useCallback((columnIndex: number): ItemType[] => {
    if (!items) return [];
    let currentItems = items;
    for (let i = 0; i < columnIndex; i++) {
      if (path[i] === undefined || !currentItems.children) return [];
      currentItems = currentItems.children[path[i]];
    }
    return currentItems.children || [];
  }, [path, items]);

  const resumeDraftPath = useCallback(() => {
    if (draftPath) {
      setPath(draftPath);
      setDraftPath(null);
      setLastLoadedSavedPath(null);
    }
  }, [draftPath]);

  const savePathAndReset = useCallback(() => {
    setSavedPaths(prev => [...prev, { id: uuidv4(), path: [...path] }]);
    setPath([0]);
    if (columnsWrapperRef.current) {
      columnsWrapperRef.current.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
    }
    if (draftPath) {
      resumeDraftPath();
    }
  }, [path, columnsWrapperRef, draftPath, resumeDraftPath]);

  const handleSelect = useCallback((columnIndex: number, itemIndex: number) => {
    setPath(prevPath => {
      const newPath = prevPath.slice(0, columnIndex + 1);
      newPath[columnIndex] = itemIndex;
      return newPath;
    });
  }, []);

  const handleKeyNavigation = useCallback((e: KeyboardEvent) => {
    if ([KEYBOARD_SHORTCUTS.NAVIGATE_UP, KEYBOARD_SHORTCUTS.NAVIGATE_DOWN, KEYBOARD_SHORTCUTS.NAVIGATE_LEFT, KEYBOARD_SHORTCUTS.NAVIGATE_RIGHT].includes(e.key)) {
      e.preventDefault();
      e.stopPropagation();
      setPath(prevPath => {
        const newPath = [...prevPath];
        const currentColumn = newPath.length - 1;
        const currentItem = newPath[currentColumn] || 0;
        const currentColumnItems = getItemsForColumn(currentColumn);

        switch (e.key) {
          case KEYBOARD_SHORTCUTS.NAVIGATE_UP:
            newPath[currentColumn] = (currentItem - 1 + currentColumnItems.length) % currentColumnItems.length;
            break;
          case KEYBOARD_SHORTCUTS.NAVIGATE_DOWN:
            newPath[currentColumn] = (currentItem + 1) % currentColumnItems.length;
            break;
          case KEYBOARD_SHORTCUTS.NAVIGATE_LEFT:
            if (currentColumn > 0) newPath.pop();
            break;
          case KEYBOARD_SHORTCUTS.NAVIGATE_RIGHT:
            if (currentColumn < config.columns.length - 1) {
              const currentItem = currentColumnItems[newPath[currentColumn]];
              if (currentItem && currentItem.children && currentItem.children.length > 0) {
                newPath.push(0);
              }
            }
            break;
        }
        return newPath;
      });
    }
  }, [config.columns.length, getItemsForColumn]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyNavigation);
    return () => window.removeEventListener('keydown', handleKeyNavigation);
  }, [handleKeyNavigation]);

  const loadSavedPath = useCallback((savedPath: SavedPath) => {
    if (JSON.stringify(path) !== JSON.stringify(lastLoadedSavedPath)) {
      setDraftPath(path);
    }
    setPath(savedPath.path);
    setLastLoadedSavedPath(savedPath.path);
    setHighlightedSavedPathId(savedPath.id);
  }, [path, lastLoadedSavedPath]);

  useEffect(() => {
    if (JSON.stringify(path) !== JSON.stringify(lastLoadedSavedPath)) {
      setHighlightedSavedPathId(null);
    }
  }, [path, lastLoadedSavedPath]);

  return {
    path,
    setPath,
    items,
    handleSelect,
    getItemsForColumn,
    savedPaths,
    loadSavedPath,
    savePath: savePathAndReset,
    draftPath,
    resumeDraftPath,
    highlightedSavedPathId
  };
};