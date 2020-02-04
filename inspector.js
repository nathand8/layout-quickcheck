function loadIframe() {
  const frame = document.getElementById('inspect-frame');
  frame.onload = () => { console.log(outputIframeContents())};
  frame.src = "testfiles/test1.html";
}

function outputIframeContents() {
  const frameBody = window.frames[0].document.body;

  const recurse = (element) => {
    const tag = element.tagName;
    const {x, y, width, height} = element.getBoundingClientRect();
    const values = {x, y, width, height, tag};
    values.children = Array.from(element.children).map((child) => recurse(child, {}));
    return values;
  };

  return recurse(frameBody);
}
