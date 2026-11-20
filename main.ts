// news-image-20261120 — a program/v1 entry for make.fun.
//
// The entry is one front-page image summing up Friday 20 November 2026's
// world news. The image was drawn in advance by draw.py in this repository
// (vector shapes and system fonts, no photograph) and is shipped here as
// entry.png. This program only delivers that image to the grader's output
// directory: it reads the bundled PNG and writes the exact same bytes to
// <output>/entry.png, so every run produces byte-identical output.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const image = readFileSync(join(here, "entry.png"));

// Guard: only ever deliver a real PNG. The first eight bytes of a PNG file
// are a fixed signature; anything else means the bundled image is corrupt.
const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!image.subarray(0, 8).equals(pngSignature)) {
  throw new Error("entry.png is not a valid PNG file");
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
writeFileSync(target, image);

// Confirm the write landed whole: the grader gates on a complete PNG of
// at most 1 MiB, and this program must write identical bytes on every run.
if (readFileSync(target).length !== image.length) {
  throw new Error("entry.png was not written completely");
}
