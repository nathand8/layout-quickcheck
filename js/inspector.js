export function loadIframe() {
  const frame = document.getElementById("inspect-frame");
  frame.onload = () => {
    console.log(outputIframeContents());
    document.getElementById("status").innerHTML = "Ready";
  };

  const windowUrl = new URL(window.location.href);
  const testUrl = windowUrl.searchParams.get("url");
  if (testUrl !== null) {
    frame.src = testUrl;
  } else {
    frame.src = "testfiles/basic.html";
  }
}

export function outputIframeContents() {
  const frameBody = window.frames[0].document.body;

  const recurse = (element) => {
    const { x, y, width, height } = element.getBoundingClientRect();
    const values = { x, y, width, height };
    values.children = Array.from(element.children).map((child) =>
      recurse(child)
    );
    return values;
  };

  return recurse(frameBody);
}

export function loadCurrentStateFresh() {
  window.frames[0].document.documentElement.innerHTML =
    window.frames[0].document.documentElement.innerHTML;
}

export function modifyStyles(styleLog) {
  Object.entries(styleLog).forEach(([elementId, styles]) => {
    applyStyles(elementId, styles);
  });
}

export function getHtml() {
  return window.frames[0].document.documentElement.outerHTML;
}

export function applyStyles(elementId, styles) {
  const element = window.frames[0].document.getElementById(elementId);
  if (element) {
    Object.entries(styles).forEach(([styleName, styleValue]) => {
      element.style[styleName] = styleValue;
    });
  }
}
