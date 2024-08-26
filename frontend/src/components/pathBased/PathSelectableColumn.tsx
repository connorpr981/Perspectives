import React, { useRef, useEffect } from 'react';
import { Column } from './Column';
import { Item } from './Item';
import { ItemType, ColumnConfig, PathType } from '../../types/pathBased';
import styles from '../../styles/pathBased.module.css';
import { scrollItemToCenter } from '../../utils/scrollHelpers';

interface PathSelectableColumnProps {
  items: ItemType[];
  onSelect: (columnIndex: number, itemIndex: number) => void;
  path: PathType;
  columnIndex: number;
  config: ColumnConfig;
  observe: (element: Element | null) => void;
  isActive: boolean;
  scrollColumnIntoView: (columnRef: React.RefObject<HTMLDivElement>, columnIndex: number) => void;
  activeColumnIndex: number;
}

export const PathSelectableColumn: React.FC<PathSelectableColumnProps> = ({
  items,
  onSelect,
  path,
  columnIndex,
  config,
  observe,
  isActive,
  scrollColumnIntoView,
  activeColumnIndex
}) => {
  const columnRef = useRef<HTMLDivElement>(null);
  const itemsWrapperRef = useRef<HTMLDivElement>(null);
  const itemRefs = useRef<(HTMLDivElement | null)[]>([]);

  const hasSelectedItem = path[columnIndex] !== undefined;

  useEffect(() => {
    observe(columnRef.current);
  }, [observe]);

  useEffect(() => {
    if (isActive && columnRef.current) {
      scrollColumnIntoView(columnRef, columnIndex);
    }
  }, [isActive, scrollColumnIntoView, columnIndex]);

  useEffect(() => {
    const selectedItemIndex = path[columnIndex];
    if (selectedItemIndex !== undefined) {
      const selectedItem = itemRefs.current[selectedItemIndex];
      if (selectedItem && itemsWrapperRef.current) {
        setTimeout(() => {
          scrollItemToCenter(selectedItem, itemsWrapperRef.current);
          selectedItem.classList.add(styles.itemTransition);
        });
      }
    }
  }, [path, columnIndex]);

  useEffect(() => {
    if (columnIndex > activeColumnIndex && itemsWrapperRef.current) {
      itemsWrapperRef.current.scrollTop = 0;
    }
  }, [activeColumnIndex, columnIndex]);

  // Group items by section
  const groupedItems = items.reduce((acc, item) => {
    let section = item.section || 'Other';
    if (config.title === 'Tags') {
      section = 'Tidbits';
    }
    if (!acc[section]) {
      acc[section] = [];
    }
    acc[section].push(item);
    return acc;
  }, {} as Record<string, ItemType[]>);

  return (
    <Column 
      ref={columnRef} 
      className={`${isActive ? styles.activeColumn : ''} ${hasSelectedItem ? styles.hasSelectedItem : ''}`}
    >
      <div className={styles.itemsWrapper} ref={itemsWrapperRef}>
        <div className={styles.itemsContainer}>
          {Object.entries(groupedItems).map(([section, sectionItems], sectionIndex) => (
            <div key={section} className={styles.section}>
              <h3 className={styles.sectionTitle}>{section}</h3>
              {sectionItems.map((item, index) => (
                <Item
                  key={`${sectionIndex}-${index}`}
                  ref={el => itemRefs.current[items.indexOf(item)] = el}
                  item={item}
                  isSelected={path[columnIndex] === items.indexOf(item)}
                  isExpanded={path[columnIndex] === items.indexOf(item)}
                  onClick={() => onSelect(columnIndex, items.indexOf(item))}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    </Column>
  );
};