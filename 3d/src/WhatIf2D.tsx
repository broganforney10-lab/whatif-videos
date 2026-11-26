import React, { useEffect, useState } from "react";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  continueRender,
  delayRender,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Character, Mood } from "./Character";

export type Scene = {
  from: number;
  dur: number;
  kicker: string;
  headline: string;
  sub: string;
  mood: Mood;
};
export type Word = { w: string; start: number; end: number };
export type VideoData = {
  id: string;
  emoji: string;
  subject: string;
  durationInFrames: number;
  audio: string;
  scenes: Scene[];
  words: Word[];
  mouth: number[];
};

const ACCENT = "#FFC43D";
const W = 1080;
const H = 1920;
const GROUND_Y = 1585;

const fonts = Promise.all([
  loadFont({
    family: "InterDisplay",
    url: staticFile("fonts/InterDisplay-Black.otf"),
    weight: "900",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("fonts/Inter-ExtraBold.otf"),
    weight: "800",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("fonts/Inter-Bold.otf"),
    weight: "700",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("fonts/Inter-SemiBold.otf"),
    weight: "600",
  }),
]);

const useFonts = () => {
  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => {
    fonts
      .then(() => continueRender(handle))
      .catch((e) => {
        console.error(e);
        continueRender(handle);
      });
  }, [handle]);
};

const Sky: React.FC<{ frame: number }> = ({ frame }) => (
  <AbsoluteFill
    style={{
      background:
        "linear-gradient(180deg, #070C1E 0%, #12204A 55%, #1C3266 100%)",
    }}
  >
    <svg width={W} height={H} style={{ position: "absolute" }}>
      {new Array(70).fill(0).map((_, i) => {
        const x = random(`sx${i}`) * W;
        const y = random(`sy${i}`) * 1250;
        const r = 1.5 + random(`sr${i}`) * 3;
        const tw =
          0.35 +
          0.65 * Math.abs(Math.sin(frame / (14 + random(`st${i}`) * 30) + i));
        return (
          <circle
            key={i}
            cx={x}
            cy={y}
            r={r}
            fill="#DDE6FF"
            opacity={tw * 0.8}
          />
        );
      })}
      {/* rolling hill the narrator stands on */}
      <path
        d={`M 0 ${GROUND_Y - 10} Q 270 ${GROUND_Y - 60} 540 ${GROUND_Y - 30} T 1080 ${GROUND_Y - 20} L 1080 1920 L 0 1920 Z`}
        fill="#16294F"
      />
      <path
        d={`M 0 ${GROUND_Y - 10} Q 270 ${GROUND_Y - 60} 540 ${GROUND_Y - 30} T 1080 ${GROUND_Y - 20}`}
        stroke="#2D4C85"
        strokeWidth={8}
        fill="none"
      />
      {new Array(9).fill(0).map((_, i) => {
        const x = 60 + i * 120 + random(`gx${i}`) * 40;
        const y = GROUND_Y + 60 + random(`gy${i}`) * 180;
        return (
          <path
            key={i}
            d={`M ${x} ${y} l 8 -22 l 8 22 l 8 -16 l 6 16`}
            stroke="#24406F"
            strokeWidth={5}
            fill="none"
            strokeLinecap="round"
          />
        );
      })}
    </svg>
  </AbsoluteFill>
);

const headlineSize = (t: string) => {
  const longest = Math.max(...t.split(" ").map((w) => w.length));
  const byWord = Math.floor(900 / (longest * 0.62));
  const byTotal = t.length > 16 ? 112 : t.length > 10 ? 136 : 168;
  return Math.max(84, Math.min(byWord, byTotal));
};

const SceneText: React.FC<{ scene: Scene; local: number }> = ({
  scene,
  local,
}) => {
  const { fps } = useVideoConfig();
  const inK = spring({ frame: local, fps, config: { damping: 16, mass: 0.6 } });
  const inH = spring({
    frame: local - 4,
    fps,
    config: { damping: 12, mass: 0.7 },
  });
  const inS = spring({ frame: local - 10, fps, config: { damping: 18 } });
  const out = interpolate(local, [scene.dur - 7, scene.dur], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        position: "absolute",
        top: 190,
        left: 80,
        right: 80,
        textAlign: "center",
        opacity: out,
      }}
    >
      <div
        style={{
          fontFamily: "Inter",
          fontWeight: 800,
          fontSize: 46,
          letterSpacing: 2,
          color: ACCENT,
          opacity: inK,
          transform: `translateY(${(1 - inK) * 30}px)`,
        }}
      >
        {scene.kicker}
      </div>
      <div
        style={{
          fontFamily: "InterDisplay",
          fontWeight: 900,
          fontSize: headlineSize(scene.headline),
          lineHeight: 1.0,
          color: "#fff",
          marginTop: 22,
          transform: `scale(${0.6 + 0.4 * inH}) rotate(${(1 - inH) * -4}deg)`,
          opacity: Math.min(1, inH * 1.5),
          textShadow: "0 8px 0 rgba(0,0,0,0.25)",
        }}
      >
        {scene.headline}
      </div>
      {scene.sub && (
        <div
          style={{
            fontFamily: "Inter",
            fontWeight: 600,
            fontSize: 48,
            lineHeight: 1.25,
            color: "#D2DCEB",
            marginTop: 28,
            opacity: inS,
            transform: `translateY(${(1 - inS) * 24}px)`,
          }}
        >
          {scene.sub}
        </div>
      )}
    </div>
  );
};

// The topic's emoji: shown in the hook, then it "poofs" away. Later scenes keep a faded ghost of it.
const Prop: React.FC<{ emoji: string; frame: number; hookDur: number }> = ({
  emoji,
  frame,
  hookDur,
}) => {
  const poofAt = Math.min(66, hookDur - 30);
  const x = 175;
  const y = 1095;
  const float = Math.sin(frame / 13) * 14;
  if (frame < poofAt + 18) {
    const grow = interpolate(frame, [0, 12], [0, 1], {
      extrapolateRight: "clamp",
    });
    const pop = interpolate(
      frame,
      [poofAt, poofAt + 5, poofAt + 10],
      [1, 1.35, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
    );
    const k = Math.max(0, frame - poofAt);
    return (
      <div
        style={{
          position: "absolute",
          left: x - 110,
          top: y - 110 + float,
          width: 220,
          height: 220,
        }}
      >
        <div
          style={{
            fontFamily: "Noto Color Emoji",
            fontSize: 170,
            lineHeight: "220px",
            textAlign: "center",
            transform: `scale(${grow * pop})`,
          }}
        >
          {emoji}
        </div>
        {frame >= poofAt &&
          new Array(12).fill(0).map((_, i) => {
            const a = (i / 12) * Math.PI * 2;
            const d = k * 9;
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 110 + Math.cos(a) * d - 22,
                  top: 110 + Math.sin(a) * d - 22,
                  width: 44,
                  height: 44,
                  borderRadius: 22,
                  background: "#E8EEFF",
                  opacity: Math.max(0, 1 - k / 18),
                  transform: `scale(${1 - k / 24})`,
                }}
              />
            );
          })}
      </div>
    );
  }
  return (
    <div
      style={{
        position: "absolute",
        left: x - 90,
        top: y - 90 + float,
        width: 180,
        height: 180,
        borderRadius: 90,
        border: "6px dashed rgba(200,215,255,0.35)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          fontFamily: "Noto Color Emoji",
          fontSize: 110,
          opacity: 0.18,
          filter: "grayscale(1)",
        }}
      >
        {emoji}
      </div>
    </div>
  );
};

const WORDS_PER_CAPTION = 3;

const Captions: React.FC<{ words: Word[]; t: number; sceneEnds: number[] }> = ({
  words,
  t,
}) => {
  // group into short chunks, breaking after punctuation
  const chunks: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length === WORDS_PER_CAPTION || /[.,?!:;]$/.test(w.w)) {
      chunks.push(cur);
      cur = [];
    }
  }
  if (cur.length) chunks.push(cur);
  const idx = chunks.findIndex((c, i) => {
    const end =
      i + 1 < chunks.length
        ? Math.min(chunks[i + 1][0].start, c[c.length - 1].end + 0.6)
        : c[c.length - 1].end + 0.6;
    return t >= c[0].start && t < end;
  });
  if (idx < 0) return null;
  const chunk = chunks[idx];
  const active = chunk.reduce((a, w, i) => (w.start <= t ? i : a), -1);
  const pop = interpolate(t - chunk[0].start, [0, 0.12], [0.85, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const len = chunk.map((w) => w.w).join(" ").length;
  return (
    <div
      style={{
        position: "absolute",
        top: 1660,
        left: 70,
        right: 70,
        textAlign: "center",
        fontFamily: "InterDisplay",
        fontWeight: 900,
        fontSize: len > 20 ? 66 : 80,
        transform: `scale(${pop})`,
        WebkitTextStroke: "12px #0A0F1F",
        paintOrder: "stroke fill",
      }}
    >
      {chunk.map((w, i) => (
        <span
          key={i}
          style={{
            color: i === active ? ACCENT : "#fff",
            marginRight: i < chunk.length - 1 ? 18 : 0,
          }}
        >
          {w.w}
        </span>
      ))}
    </div>
  );
};

export const WhatIf2D: React.FC<VideoData> = (data) => {
  useFonts();
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const si = Math.max(
    0,
    data.scenes.findIndex((s) => frame >= s.from && frame < s.from + s.dur),
  );
  const scene = data.scenes[si];
  const prev = data.scenes[Math.max(0, si - 1)];
  const local = frame - scene.from;
  const mouth = data.mouth[Math.min(frame, data.mouth.length - 1)] ?? 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#070C1E", overflow: "hidden" }}>
      <Sky frame={frame} />
      <SceneText scene={scene} local={local} />
      <Prop emoji={data.emoji} frame={frame} hookDur={data.scenes[0].dur} />
      <div
        style={{
          position: "absolute",
          left: (W - 600) / 2 + 60,
          top: GROUND_Y - 690,
          transform: "scale(1.22)",
          transformOrigin: "50% 98%",
        }}
      >
        <Character
          mood={scene.mood}
          prevMood={si === 0 ? scene.mood : prev.mood}
          sceneFrame={local}
          frame={frame}
          mouth={mouth}
        />
      </div>
      <Captions
        words={data.words}
        t={t}
        sceneEnds={data.scenes.map((s) => (s.from + s.dur) / fps)}
      />
      <div
        style={{
          position: "absolute",
          bottom: 52,
          width: "100%",
          textAlign: "center",
          fontFamily: "Inter",
          fontWeight: 700,
          fontSize: 36,
          color: "#8FA3C8",
        }}
      >
        @whatifitvanished
      </div>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: 12,
          width: `${(frame / durationInFrames) * 100}%`,
          background: ACCENT,
        }}
      />
      <Audio src={staticFile(data.audio)} />
    </AbsoluteFill>
  );
};
