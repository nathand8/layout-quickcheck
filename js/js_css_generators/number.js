import { choice } from "./util.js";
import { generate as generateInteger } from "./integer.js";

const number_generators = [generateInteger];

function pick_generator() {
  return choice(number_generators);
}

export function generate() {
  const generator = pick_generator();
  return generator();
}
