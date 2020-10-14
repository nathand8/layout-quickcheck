import { choice } from './util.js';
import { generate as generateNumber } from './number.js';

const suffixes = [
  "cap",
  "ch",
  "em",
  "ex",
  "ic",
  "lh",
  "rem",
  "rlh",
  "vh",
  "vw",
  "vi",
  "vb",
  "vmin",
  "vmax",
  "px",
  "cm",
  "mm",
  "Q",
  "in",
  "pc",
  "pt",
  "mozmm",
  "",
];

function generateSuffix() {
  return choice(suffixes);
}

export function generate() {
  const number = generateNumber();
  const suffix = generateSuffix();
  return `${number}${suffix}`;
}
