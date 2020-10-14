import { styleData } from "./js_css_generators/styleData.js";
import { choice } from "./js_css_generators/util.js";
import { generate as generateLength } from "./js_css_generators/length.js";
import { createGenerator as createKeywordGenerator } from "./js_css_generators/keyword.js";

const STYLE_PROBABILITY = 0.01;

function typeToGenerator(typedomType, currentStyle) {
  switch (typedomType) {
    case "Length":
      return generateLength;
    case "Keyword":
      return createKeywordGenerator(currentStyle.keywords);
  }
}

function isSupportedType(currentStyle) {
  return function (typedomType) {
    if (typedomType === "Length") {
      return true;
    } else if (typedomType === "Keyword") {
      return Object.keys(currentStyle).includes("keywords");
    } else {
      return false;
    }
  };
}

export function generateStyles() {
  return styleData.data.reduce((acc, currentStyle) => {
    if (Math.random() <= STYLE_PROBABILITY) {
      const typedomTypes = (currentStyle.typedom_types || []).filter(
        isSupportedType(currentStyle)
      );
      if (typedomTypes.length > 0) {
        const typeChoice = choice(typedomTypes);
        const generator = typeToGenerator(typeChoice, currentStyle);
        acc[currentStyle.name] = generator();
      }
    }
    return acc;
  }, {});
}
