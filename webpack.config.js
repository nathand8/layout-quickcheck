const path = require("path");

module.exports = {
  entry: "./js/inspector.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "jsdist"),
    library: "inspectorTools",
  },
  mode: 'development',
};
