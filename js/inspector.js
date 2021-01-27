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

export function isPageLoaded() {

  // Wait for the document 'load' event (Attempt 3)
  // let navData = window.performance.getEntriesByType("navigation");
  // if (navData.length > 0 && navData[0].loadEventEnd > 0) {
  //   return true;
  // }
  // if (!window.onload) {
  //   window.pageIsLoaded = false;
  //   window.onload = () => {window.pageIsLoaded = true};
  // }
  // return window.pageIsLoaded;

  // Wait for one complete timeout cycle (Attempt 2)
  if (!window.pageLoadTimeout) {
    window.pageIsLoaded = false;
    window.pageLoadTimeout = setTimeout(() => {
      window.pageIsLoaded = true;
    })
  }
  return window.pageIsLoaded;

  // Wait for document state (Attempt 1)
  // return document.readyState == "complete";
}
