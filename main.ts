// Entry runner for make.fun news-image-20261124.
// Reads the drawn front page (entry.png, produced by draw.py in this repo)
// and copies it to /output/entry.png. Node 22 standard library only.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const out = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`missing ${src} — run: python3 draw.py`);
  process.exit(1);
}

const buf = readFileSync(src);

// Verify it is a PNG and read its dimensions from the IHDR chunk.
if (buf.length < 33 || buf.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
  console.error("entry.png is not a PNG file");
  process.exit(1);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png is ${width}x${height}, expected 1024x1024`);
  process.exit(1);
}

if (buf.length > 1024 * 1024) {
  console.error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
  process.exit(1);
}
const sha256 = createHash("sha256").update(buf).digest("hex");

mkdirSync(outDir, { recursive: true });
writeFileSync(out, buf);
console.log(`wrote ${out} (${buf.length} bytes, ${width}x${height})`);
console.log(`sha256: ${sha256}`);
