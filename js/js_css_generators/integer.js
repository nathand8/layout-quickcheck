import { choice, randInt } from "./util.js";

const MAX_NUMBER = 2000;

const prefixes = ["", "+", "-"];

function generate_prefix() {
  return choice(prefixes);
}

export function generate() {
  const prefix = generate_prefix();
  const number = randInt(MAX_NUMBER);
  return `${prefix}${number}`;
}
