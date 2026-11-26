// Render every public/data/<id>.json to out/<id>-2d.mp4 with one shared bundle.
//   node render.mjs            all videos (skips finished ones)
//   node render.mjs 01-moon    just these ids
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";

const COMP = process.env.COMP || "WhatIf2D";
const DATA = process.env.DATA || "public/data";
const OUT = process.env.OUT || "out";
const SUF = process.env.SUF ?? "-2d";
const browserExecutable = "/opt/pw-browsers/chromium_headless_shell";
const ids = process.argv.slice(2).length
  ? process.argv.slice(2)
  : fs.readdirSync(DATA).filter((f) => f.endsWith(".json")).map((f) => f.replace(".json", "")).sort();

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
fs.mkdirSync(OUT, { recursive: true });
for (const id of ids) {
  const outputLocation = `${OUT}/${id}${SUF}.mp4`;
  if (fs.existsSync(outputLocation) && process.argv.length <= 2) continue;
  const inputProps = JSON.parse(fs.readFileSync(`${DATA}/${id}.json`, "utf8"));
  const composition = await selectComposition({ serveUrl, id: COMP, inputProps, browserExecutable });
  const t0 = Date.now();
  await renderMedia({
    composition, serveUrl, codec: "h264", crf: 20, inputProps, browserExecutable,
    outputLocation: outputLocation + ".part.mp4", chromiumOptions: { gl: "swangle" }, scale: Number(process.env.SCALE || 1), concurrency: 4, imageFormat: "jpeg", jpegQuality: 90,
  });
  fs.renameSync(outputLocation + ".part.mp4", outputLocation);
  console.log(`done ${id} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
