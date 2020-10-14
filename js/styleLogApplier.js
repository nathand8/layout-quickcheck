export function applyStyles(elementId, styles) {
  const element = window.frames[0].document.getElementById(elementId);
  Object.entries(styles).forEach(([styleName, styleValue]) => {
    element.style[styleName] = styleValue;
  });
}
