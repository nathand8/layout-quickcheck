const fs = require("fs");
const traceJson = JSON.parse(
  fs.readFileSync(
    "C:/Users/William/code/school/servo/layout_trace-1.json",
    "utf-8"
  )
);

function parseJson(json) {
  const root = traceJson.post;

  const recurse = element => {
    const {
      size: { block: heightAus, inline: widthAus },
      start: { b: yAus, i: xAus }
    } = element.data.base.position;
    const values = {
      x: xAus / 60,
      y: yAus / 60,
      width: widthAus / 60,
      height: heightAus / 60
    };
    values.children = Array.from(element.data.base.children).map(child =>
      recurse(child)
    );
    return values;
  };

  return recurse(root.children[0]);
}

const parsed = parseJson(traceJson);

fs.writeFileSync(
  "C:/Users/William/code/school/servo/layout_trace-1-parsed.json",
  JSON.stringify(parsed)
);
