import React, { useState, useEffect } from 'react';
import { ItemType } from '../../types/pathBased';
import ReactMarkdown from 'react-markdown';
import styles from '../../styles/pathBased.module.css';

interface ItemProps {
  item: ItemType;
  isSelected: boolean;
  isExpanded: boolean;
  onClick: () => void;
}

export const Item = React.forwardRef<HTMLDivElement, ItemProps>(({ item, isSelected, isExpanded, onClick }, ref) => {
  const [isAnimated, setIsAnimated] = useState(false);

  useEffect(() => {
    if (isSelected) {
      setIsAnimated(true);
      const timer = setTimeout(() => setIsAnimated(false), 300); // Duration of the animation
      return () => clearTimeout(timer);
    }
  }, [isSelected]);

  return (
    <div
      ref={ref}
      className={`${styles.item} 
                  ${isSelected ? styles.itemSelected : ''} 
                  ${isExpanded && item.content.length > 0 ? styles.itemExpanded : ''}
                  ${isAnimated ? styles.itemAnimated : ''}`}
      onClick={onClick}
    >
      <h3 className={styles.itemTitle}>{item.title}</h3>
      {item.subtitle && <p className={styles.itemSubtitle}>{item.subtitle}</p>}
      {isExpanded && item.content.length > 0 && (
        <div className={styles.itemContent}>
          {item.content.map((section, index) => (
            <div key={index} className={styles.contentSection}>
              <h4 className={styles.contentSectionLabel}>{section.label}</h4>
              <div className={styles.contentSectionContent}>
                {section.type === 'markdown' ? (
                  <ReactMarkdown
                    components={{
                      a: ({ node, children, ...props }) => (
                        <a target="_blank" rel="noopener noreferrer" {...props}>
                          {children}
                        </a>
                      )
                    }}
                  >
                    {section.value}
                  </ReactMarkdown>
                ) : (
                  <p>{section.value}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
});

Item.displayName = 'Item';