import { useState, useEffect, useCallback } from 'react';
import { PathType } from '../types/pathBased';

export const useColumnVisibility = (
  path: PathType,
  totalColumns: number,
  columnsWrapperRef: React.RefObject<HTMLDivElement>
) => {
  const [visibleColumns, setVisibleColumns] = useState<number[]>([]);

  const updateVisibleColumns = useCallback(() => {
    if (!columnsWrapperRef.current) return;

    const wrapperWidth = columnsWrapperRef.current.offsetWidth;
    const columnWidth = (columnsWrapperRef.current.children[0] as HTMLElement)?.offsetWidth || 0;
    const maxVisibleColumns = Math.floor(wrapperWidth / columnWidth);

    let newVisibleColumns: number[] = [];

    // Always show the first column
    newVisibleColumns.push(0);

    // Add columns from the current path
    for (let i = 1; i < path.length; i++) {
      newVisibleColumns.push(i);
    }

    // Add the next column if there's space
    if (path.length < totalColumns) {
      newVisibleColumns.push(path.length);
    }

    // If we have more columns than can fit, prioritize showing the active column
    if (newVisibleColumns.length > maxVisibleColumns) {
      const activeColumnIndex = path.length - 1;
      const start = Math.max(0, activeColumnIndex - Math.floor(maxVisibleColumns / 2));
      newVisibleColumns = newVisibleColumns.slice(start, start + maxVisibleColumns);
    }

    setVisibleColumns(newVisibleColumns);
  }, [path, totalColumns, columnsWrapperRef]);

  useEffect(() => {
    updateVisibleColumns();
    window.addEventListener('resize', updateVisibleColumns);
    return () => window.removeEventListener('resize', updateVisibleColumns);
  }, [updateVisibleColumns]);

  return visibleColumns;
};
