import { useCallback, useRef, useEffect } from 'react';
import { PathType } from '../types/pathBased';

export const useColumnScroll = (
  config: { columns: { title: string }[] },
  path: PathType,
  columnsWrapperRef: React.RefObject<HTMLDivElement>
) => {
  const activeColumnIndex = path.length - 1;
  const previousActiveColumnIndex = useRef(activeColumnIndex);

  const scrollToActiveColumn = useCallback(() => {
    if (columnsWrapperRef.current) {
      const wrapper = columnsWrapperRef.current;
      const columns = Array.from(wrapper.children) as HTMLElement[];
      const activeColumn = columns[activeColumnIndex];
      
      if (activeColumn) {
        const isMovingForward = activeColumnIndex > previousActiveColumnIndex.current;
        const shouldScroll = isMovingForward 
          ? activeColumnIndex >= 2 && activeColumnIndex <= config.columns.length - 2
          : activeColumnIndex >= 1 && activeColumnIndex <= config.columns.length - 2;

        if (shouldScroll) {
          const scrollLeft = activeColumn.offsetLeft - (wrapper.clientWidth - activeColumn.offsetWidth) / 2;
          wrapper.scrollTo({
            left: scrollLeft,
            behavior: 'smooth'
          });
        }
      }
    }
    previousActiveColumnIndex.current = activeColumnIndex;
  }, [activeColumnIndex, config.columns.length, columnsWrapperRef]);

  useEffect(() => {
    scrollToActiveColumn();
  }, [scrollToActiveColumn]);

  const scrollColumnIntoView = useCallback((columnRef: React.RefObject<HTMLDivElement>, columnIndex: number) => {
    if (columnsWrapperRef.current && columnRef.current) {
      const wrapper = columnsWrapperRef.current;
      const isMovingForward = columnIndex > previousActiveColumnIndex.current;
      const shouldScroll = isMovingForward 
        ? columnIndex >= 2 && columnIndex <= config.columns.length - 2
        : columnIndex >= 1 && columnIndex <= config.columns.length - 2;

      if (shouldScroll) {
        const scrollLeft = columnRef.current.offsetLeft - (wrapper.clientWidth - columnRef.current.offsetWidth) / 2;
        wrapper.scrollTo({
          left: scrollLeft,
          behavior: 'smooth'
        });
      }
    }
    previousActiveColumnIndex.current = columnIndex;
  }, [config.columns.length, columnsWrapperRef]);

  return {
    activeColumnIndex,
    scrollToActiveColumn,
    scrollColumnIntoView,
  };
};