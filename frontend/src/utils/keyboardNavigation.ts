import { PathType } from '../types/pathBased';

export const handleKeyNavigation = (
  e: KeyboardEvent,
  path: PathType,
  totalColumns: number,
  getItemsForColumn: (columnIndex: number) => any[],
  setPath: (newPath: PathType) => void,
  savePath: () => void
) => {
  if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter"].includes(e.key)) {
    e.preventDefault();
    const newPath = [...path];
    const currentColumn = newPath.length - 1;
    const currentItem = newPath[currentColumn] || 0;
    const currentColumnItems = getItemsForColumn(currentColumn) || [];

    let shouldUpdatePath = false;

    switch (e.key) {
      case "ArrowUp":
        if (currentColumnItems.length > 0) {
          newPath[currentColumn] = (currentItem - 1 + currentColumnItems.length) % currentColumnItems.length;
          shouldUpdatePath = true;
        }
        break;
      case "ArrowDown":
        if (currentColumnItems.length > 0) {
          newPath[currentColumn] = (currentItem + 1) % currentColumnItems.length;
          shouldUpdatePath = true;
        }
        break;
      case "ArrowLeft":
        if (currentColumn > 0) {
          newPath.pop();
          shouldUpdatePath = true;
        }
        break;
      case "ArrowRight":
        if (currentColumn < totalColumns - 1 && path.length < totalColumns) {
          const nextColumnItems = getItemsForColumn(currentColumn + 1) || [];
          if (nextColumnItems.length > 0) {
            newPath.push(0);
            shouldUpdatePath = true;
          }
        }
        break;
      case "Enter":
        if (path.length === totalColumns) {
          savePath();
          return;
        }
        break;
    }
    if (shouldUpdatePath) {
      setPath(newPath);
    }
  }
};