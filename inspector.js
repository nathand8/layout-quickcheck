function loadIframe() {
  const frame = document.getElementById('inspect-frame');
  frame.onload = () => {
    console.log(outputIframeContents());
    document.getElementById('status').innerHTML = 'Ready';
  };

  const windowUrl = new URL(window.location.href);
  const testUrl = windowUrl.searchParams.get('url')
  if (testUrl !== null) {
    frame.src = testUrl
  } else {
    frame.src = "testfiles/basic.html";
  }
}

function outputIframeContents() {
  const frameBody = window.frames[0].document.body;

  const recurse = (element) => {
    const {x, y, width, height} = element.getBoundingClientRect();
    const values = {x, y, width, height};
    values.children = Array.from(element.children).map((child) => recurse(child));
    return values;
  };

  return recurse(frameBody);
}
