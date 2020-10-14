import { choice } from "./util.js";

export function createGenerator(keywords) {
  const generate = () => choice(keywords);
  return generate;
}
