// node stills.mjs <id> [frames...]  -> stills/<id>-<frame>.jpg (default: middle of every shot)
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";

const [id, ...fr] = process.argv.slice(2);
const inputProps = JSON.parse(fs.readFileSync(`public/bb/${id}.json`, "utf8"));
if (process.env.CLEAN) inputProps.clean = true;
const frames = fr.length ? fr.map(Number) : inputProps.shots.map((s) => s.from + Math.floor(s.dur * 0.6));
const browserExecutable = "/opt/pw-browsers/chromium_headless_shell";
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const composition = await selectComposition({ serveUrl, id: "Baseball3D", inputProps, browserExecutable });
fs.mkdirSync("stills", { recursive: true });
for (const frame of frames) {
  await renderStill({ composition, serveUrl, inputProps, frame, browserExecutable, output: process.env.CLEAN ? `stills/clean-${id}.jpg` : `stills/${id}-${frame}.jpg`,
    imageFormat: "jpeg", jpegQuality: 80, scale: Number(process.env.SCALE || 0.5), chromiumOptions: { gl: "swangle" } });
  console.log("still", frame);
}
