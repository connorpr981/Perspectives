export const scrollItemToCenter = (element: HTMLElement | null, container: HTMLElement | null) => {
  if (!element || !container) return;

  const containerRect = container.getBoundingClientRect();
  const elementRect = element.getBoundingClientRect();

  const elementCenter = elementRect.top + elementRect.height / 2 - containerRect.top;
  const containerCenter = containerRect.height / 2;
  const centerOffset = elementCenter - containerCenter;

  const newScrollTop = container.scrollTop + centerOffset;

  if (typeof container.scrollTo === 'function') {
    container.scrollTo({
      top: newScrollTop,
      behavior: 'smooth'
    });
  } else {
    // Fallback for environments where scrollTo is not available
    container.scrollTop = newScrollTop;
  }
};