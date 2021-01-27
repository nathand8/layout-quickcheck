export function outputElementDimensions() {

  const recurse = (element) => {
    const { x, y, width, height } = element.getBoundingClientRect();
    const values = { x, y, width, height };
    values.children = Array.from(element.children).map((child) =>
      recurse(child)
    );
    return values;
  };

  return recurse(document.body);
}

export function loadCurrentStateFresh() {
  document.documentElement.innerHTML = document.documentElement.innerHTML;
}

export function modifyStyles(styleLog) {
  Object.entries(styleLog).forEach(([elementId, styles]) => {
    applyStyles(elementId, styles);
  });
}

export function applyStyles(elementId, styles) {
  const element = document.getElementById(elementId);
  if (element) {
    Object.entries(styles).forEach(([styleName, styleValue]) => {
      element.style[styleName] = styleValue;
    });
  }
}
