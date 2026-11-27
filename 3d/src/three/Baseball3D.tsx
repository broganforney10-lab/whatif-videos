// "Baseball What Ifs" 3D Short. One JSON (public/bb/<id>.json) holds shots, scenes, words, mouth and audio.
// Ballpark + Moon sets, a real 3D ball with seams and a motion trail, a swinging bat, a jumbotron that shows
// each scene's number, a broadcast-style stat graphic and word-by-word captions. Hard cuts, no dip to black.
import React, { useEffect, useLayoutEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import {
  AbsoluteFill,
  continueRender,
  delayRender,
  Easing,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Pose, Toon } from "./Toon";
import { Emoji, Poof } from "./Sets";

type V3 = [number, number, number];
type Prop3D = { ch: string; pos: V3; s?: number; anim?: "float" | "grow" | "pop" | "rise" | "burst" };
type Flight = { from: V3; to: V3; arc?: number; t0: number; t1: number; spin?: boolean; trail?: number; r?: number };
type Actor = {
  pos: V3;
  heading?: number;
  pose: Pose;
  pose2?: Pose;
  poseAt?: number;
  hat?: "cap" | "helmet" | "space" | "none";
  jersey?: string;
  bat?: { a0: number; a1: number; t0: number; t1: number } | "rest";
  run?: [V3, V3];
  talk?: boolean;
};
export type BBShot = {
  from: number;
  dur: number;
  set: "park" | "moon";
  cam: { from: V3; to: V3; look: V3; lookTo?: V3; fov?: number; follow?: boolean };
  actors: Actor[];
  ball?: Flight;
  props?: Prop3D[];
  board?: string; // jumbotron text
  crowd?: number; // 0..1 how hard the crowd bounces
  night?: boolean;
  shake?: number; // camera shake at ball contact time (0..1 of shot)
};
type Scene = { from: number; dur: number; kicker: string; headline: string; sub: string };
export type BBData = {
  id: string;
  durationInFrames: number;
  audio: string;
  shots: BBShot[];
  scenes: Scene[];
  words: { w: string; start: number; end: number }[];
  mouth: number[];
  clean?: boolean;
};

const fonts = loadFont({ family: "InterDisplay", url: staticFile("fonts/InterDisplay-Black.otf"), weight: "900" });
const useAssetsReady = () => {
  const [h] = useState(() => delayRender("fonts+emoji"));
  useEffect(() => {
    Promise.all([fonts, document.fonts.load('200px "Noto Color Emoji"', "⚾")])
      .catch(() => null)
      .then(() => continueRender(h));
  }, [h]);
};

const ease = Easing.bezier(0.45, 0, 0.25, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp3 = (a: V3, b: V3, k: number): V3 => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];

const CameraRig: React.FC<{ pos: V3; look: V3; fov: number }> = ({ pos, look, fov }) => {
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  useLayoutEffect(() => {
    camera.position.set(...pos);
    camera.fov = fov;
    camera.near = 0.1;
    camera.far = 400;
    camera.lookAt(...look);
    camera.updateProjectionMatrix();
  }, [camera, pos, look, fov]);
  return null;
};

// ---------- field geometry ----------
// Home plate at z=+4. Mound 9.4 units toward center field. Bases 14 units apart.
export const HOME: V3 = [0, 0, 4];
const D = 14 / Math.SQRT2;
const BASES: V3[] = [[D, 0, 4 - D], [0, 0, 4 - 2 * D], [-D, 0, 4 - D]];
export const MOUND: V3 = [0, 0, 4 - 9.4];
const WALL_R = 34;

const Flat: React.FC<{ y?: number; pos?: [number, number]; rot?: number; w: number; h: number; color: string; shape?: "circle" }> = ({
  y = 0.01, pos = [0, 0], rot = 0, w, h, color, shape,
}) => (
  <mesh position={[pos[0], y, pos[1]]} rotation={[-Math.PI / 2, 0, rot]} receiveShadow>
    {shape === "circle" ? <circleGeometry args={[w, 48]} /> : <planeGeometry args={[w, h]} />}
    <meshStandardMaterial color={color} roughness={0.95} />
  </mesh>
);

const textTex = (text: string, w = 1024, h = 512, bg = "#0b0f1a", fg = "#ffd23f") => {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const g = c.getContext("2d")!;
  g.fillStyle = bg;
  g.fillRect(0, 0, w, h);
  // LED dot grid
  g.fillStyle = "rgba(255,255,255,0.04)";
  for (let x = 0; x < w; x += 8) for (let y = 0; y < h; y += 8) g.fillRect(x, y, 3, 3);
  g.fillStyle = fg;
  g.textAlign = "center";
  g.textBaseline = "middle";
  let size = 230;
  g.font = `900 ${size}px InterDisplay`;
  while (g.measureText(text).width > w * 0.9 && size > 60) {
    size -= 8;
    g.font = `900 ${size}px InterDisplay`;
  }
  g.shadowColor = fg;
  g.shadowBlur = 30;
  g.fillText(text, w / 2, h / 2 + 10);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
};

const Jumbotron: React.FC<{ text: string; pos: V3; s?: number }> = ({ text, pos, s = 1 }) => {
  const tex = useMemo(() => textTex(text), [text]);
  return (
    <group position={pos} scale={s}>
      <mesh position={[0, 0, -0.3]} castShadow>
        <boxGeometry args={[13, 7, 0.5]} />
        <meshStandardMaterial color="#1b2433" metalness={0.4} roughness={0.5} />
      </mesh>
      <mesh position={[0, 0, 0]}>
        <planeGeometry args={[12, 6]} />
        <meshBasicMaterial map={tex} toneMapped={false} />
      </mesh>
      {[-4, 4].map((x) => (
        <mesh key={x} position={[x, -7, -0.3]}>
          <boxGeometry args={[0.6, 8, 0.6]} />
          <meshStandardMaterial color="#2c3646" />
        </mesh>
      ))}
    </group>
  );
};

const LightTower: React.FC<{ pos: V3; on: boolean }> = ({ pos, on }) => (
  <group position={pos}>
    <mesh position={[0, 9, 0]}>
      <cylinderGeometry args={[0.25, 0.4, 18, 8]} />
      <meshStandardMaterial color="#8a93a3" metalness={0.5} roughness={0.4} />
    </mesh>
    <mesh position={[0, 18.5, 0]} rotation={[0, Math.atan2(-pos[0], -pos[2] + 4), 0]}>
      <boxGeometry args={[4.4, 2.6, 0.4]} />
      <meshStandardMaterial color="#f8f6e8" emissive={on ? "#fff6d0" : "#555"} emissiveIntensity={on ? 2.2 : 0.2} toneMapped={false} />
    </mesh>
  </group>
);

const Stands: React.FC<{ t: number; crowd: number }> = ({ t, crowd }) => {
  const fans = useMemo(() => {
    const out: { p: V3; c: string; ph: number }[] = [];
    const cols = ["#d23c3c", "#2d5fa8", "#f3f3f3", "#f2c14e", "#2f8f5b", "#1d1f27", "#e87b2e"];
    for (let row = 0; row < 7; row++) {
      const r = WALL_R + 2.5 + row * 1.6;
      for (let i = 0; i < 70; i++) {
        const a = -Math.PI * 0.78 + (i / 69) * Math.PI * 1.56 + (row % 2) * 0.01;
        out.push({
          p: [Math.sin(a) * r, 2.6 + row * 1.15, 4 - Math.cos(a) * r],
          c: cols[Math.floor(random(`fan${row}-${i}`) * cols.length)],
          ph: random(`ph${row}-${i}`) * 6,
        });
      }
    }
    return out;
  }, []);
  return (
    <group>
      {/* tiers */}
      {new Array(7).fill(0).map((_, row) => {
        const r = WALL_R + 2.5 + row * 1.6;
        return (
          <mesh key={row} position={[0, 1.6 + row * 1.15, 4]} rotation={[0, Math.PI, 0]}>
            <cylinderGeometry args={[r + 0.8, r + 0.8, 1.15, 64, 1, true, -Math.PI * 0.8, Math.PI * 1.6]} />
            <meshStandardMaterial color={row % 2 ? "#3b4352" : "#454e60"} side={THREE.DoubleSide} />
          </mesh>
        );
      })}
      {fans.map((f, i) => (
        <mesh key={i} position={[f.p[0], f.p[1] + Math.max(0, Math.sin(t * 9 + f.ph)) * 0.35 * crowd, f.p[2]]}>
          <boxGeometry args={[0.55, 0.8, 0.4]} />
          <meshStandardMaterial color={f.c} />
        </mesh>
      ))}
    </group>
  );
};

const Ballpark: React.FC<{ t: number; crowd: number; night: boolean; board?: string }> = ({ t, crowd, night, board }) => {
  const stripes = 16;
  return (
    <>
      {/* outer grass with mowing stripes */}
      <Flat w={WALL_R + 1} h={0} color="#3f9b45" shape="circle" pos={[0, 4]} y={0} />
      {new Array(stripes).fill(0).map((_, i) => (
        <Flat key={i} y={0.004} pos={[-WALL_R + (i + 0.5) * ((2 * WALL_R) / stripes), 4 - WALL_R / 2]} w={(2 * WALL_R) / stripes} h={WALL_R + 2}
          color={i % 2 ? "#3a9341" : "#47a64d"} />
      ))}
      {/* infield dirt: big circle cut, then diamond of grass */}
      <Flat w={13} h={0} shape="circle" color="#b9814f" pos={[0, 4 - D]} y={0.008} />
      <Flat w={D * 1.42 - 1.5} h={D * 1.42 - 1.5} rot={Math.PI / 4} pos={[0, 4 - D]} y={0.012} color="#4aa652" />
      <Flat w={2.6} h={0} shape="circle" color="#b9814f" pos={[0, 4]} y={0.014} />
      {/* mound */}
      <mesh position={[MOUND[0], 0.12, MOUND[2]]} receiveShadow castShadow>
        <cylinderGeometry args={[1.3, 1.9, 0.26, 32]} />
        <meshStandardMaterial color="#b9814f" roughness={1} />
      </mesh>
      <mesh position={[MOUND[0], 0.27, MOUND[2]]}>
        <boxGeometry args={[0.6, 0.04, 0.15]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* chalk lines */}
      {[1, -1].map((s) => (
        <mesh key={s} position={[(s * WALL_R) / 2 / Math.SQRT2, 0.02, 4 - WALL_R / 2 / Math.SQRT2]} rotation={[-Math.PI / 2, 0, s * Math.PI / 4]}>
          <planeGeometry args={[0.08, WALL_R]} />
          <meshBasicMaterial color="#ffffff" />
        </mesh>
      ))}
      {/* bases + plate */}
      {BASES.map((b, i) => (
        <mesh key={i} position={[b[0], 0.06, b[2]]} rotation={[0, Math.PI / 4, 0]} castShadow>
          <boxGeometry args={[0.5, 0.1, 0.5]} />
          <meshStandardMaterial color="#ffffff" />
        </mesh>
      ))}
      <mesh position={[0, 0.03, 4]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.35, 5]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>
      {/* batter boxes */}
      {[-0.9, 0.9].map((x) => (
        <mesh key={x} position={[x, 0.02, 4]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[0.55, 0.6, 4, 1]} />
          <meshBasicMaterial color="#ffffff" />
        </mesh>
      ))}
      {/* outfield wall + yellow top line */}
      <mesh position={[0, 1.4, 4]} rotation={[0, Math.PI, 0]}>
        <cylinderGeometry args={[WALL_R, WALL_R, 2.8, 96, 1, true, -Math.PI * 0.75, Math.PI * 1.5]} />
        <meshStandardMaterial color="#1f5a3a" side={THREE.DoubleSide} />
      </mesh>
      <mesh position={[0, 2.82, 4]} rotation={[0, Math.PI, 0]}>
        <cylinderGeometry args={[WALL_R + 0.05, WALL_R + 0.05, 0.12, 96, 1, true, -Math.PI * 0.75, Math.PI * 1.5]} />
        <meshBasicMaterial color="#f2c14e" side={THREE.DoubleSide} />
      </mesh>
      <Stands t={t} crowd={crowd} />
      <Jumbotron text={board ?? "⚾"} pos={[0, 15, 4 - WALL_R - 14]} s={1.3} />
      {[[-26, -24], [26, -24], [-34, 6], [34, 6]].map(([x, z], i) => (
        <LightTower key={i} pos={[x, 0, z]} on={night} />
      ))}
      {/* skyline far away */}
      {new Array(18).fill(0).map((_, i) => (
        <mesh key={i} position={[-90 + i * 10.5, 6 + random(`bh${i}`) * 10, -110]}>
          <boxGeometry args={[8, 12 + random(`bh${i}`) * 20, 6]} />
          <meshStandardMaterial color={night ? "#1c2340" : "#9fb3c8"} emissive={night ? "#2a3560" : "#000"} />
        </mesh>
      ))}
    </>
  );
};

const MoonSet: React.FC<{ board?: string }> = () => {
  const craters = useMemo(
    () => new Array(40).fill(0).map((_, i) => ({
      x: (random(`cx${i}`) - 0.5) * 120, z: 6 - random(`cz${i}`) * 140, r: 0.8 + random(`cr${i}`) * 4,
    })),
    [],
  );
  const stars = useMemo(
    () => new Array(260).fill(0).map((_, i) => {
      const a = random(`sa${i}`) * Math.PI * 2, e = 0.05 + random(`se${i}`) * 1.3;
      return [Math.cos(a) * Math.cos(e) * 180, Math.sin(e) * 180, Math.sin(a) * Math.cos(e) * 180] as V3;
    }),
    [],
  );
  return (
    <>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[3000, 3000, 1, 1]} />
        <meshStandardMaterial color="#9a9a9e" roughness={1} />
      </mesh>
      {craters.map((c, i) => (
        <group key={i} position={[c.x, 0, c.z]}>
          <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[c.r * 0.82, c.r, 28]} />
            <meshStandardMaterial color="#b5b5b9" />
          </mesh>
          <mesh position={[0, 0.015, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <circleGeometry args={[c.r * 0.82, 28]} />
            <meshStandardMaterial color="#7d7d82" />
          </mesh>
        </group>
      ))}
      {/* tiny chalk diamond so you know it's baseball */}
      {[[0, 4], [D, 4 - D], [0, 4 - 2 * D], [-D, 4 - D]].map(([x, z], i) => (
        <mesh key={i} position={[x, 0.06, z]} rotation={[0, Math.PI / 4, 0]}>
          <boxGeometry args={[0.5, 0.1, 0.5]} />
          <meshStandardMaterial color="#ffffff" />
        </mesh>
      ))}
      {stars.map((p, i) => (
        <mesh key={i} position={p}>
          <sphereGeometry args={[0.25 + random(`st${i}`) * 0.3, 4, 4]} />
          <meshBasicMaterial color="#ffffff" fog={false} />
        </mesh>
      ))}
      {/* Earth */}
      <group position={[45, 38, -130]}>
        <mesh>
          <sphereGeometry args={[11, 40, 30]} />
          <meshStandardMaterial color="#2f6fd6" emissive="#173a80" emissiveIntensity={0.6} fog={false} />
        </mesh>
        {[[3, 4, 2], [-5, -2, 4], [1, -6, 3]].map(([x, y, r], i) => (
          <mesh key={i} position={[x, y, 9.4]}>
            <sphereGeometry args={[r, 12, 10]} />
            <meshStandardMaterial color="#3e9a4a" emissive="#1d4a22" emissiveIntensity={0.5} fog={false} />
          </mesh>
        ))}
      </group>
    </>
  );
};

// ---------- ball, bat ----------
const Ball: React.FC<{ pos: V3; r?: number; spin?: number }> = ({ pos, r = 0.16, spin = 0 }) => (
  <group position={pos} rotation={[spin, spin * 0.7, 0]}>
    <mesh castShadow>
      <sphereGeometry args={[r, 24, 18]} />
      <meshStandardMaterial color="#fbfaf5" roughness={0.55} />
    </mesh>
    {[0, Math.PI].map((a) => (
      <mesh key={a} rotation={[Math.PI / 2, a, 0.6]}>
        <torusGeometry args={[r * 0.82, r * 0.07, 6, 28, Math.PI * 1.15]} />
        <meshStandardMaterial color="#d22a2a" />
      </mesh>
    ))}
  </group>
);

const flightPos = (f: Flight, k: number): V3 => {
  const p = lerp3(f.from, f.to, k);
  p[1] += (f.arc ?? 0) * 4 * k * (1 - k);
  return p;
};

const BallFlight: React.FC<{ f: Flight; k: number; t: number }> = ({ f, k, t }) => {
  if (k < f.t0) return null;
  const q = Math.min(1, (k - f.t0) / (f.t1 - f.t0));
  const trail = f.trail ?? 10;
  const pts = new Array(trail).fill(0).map((_, i) => Math.max(0, q - (i + 1) * 0.018));
  return (
    <group>
      <Ball pos={flightPos(f, q)} spin={f.spin === false ? 0 : t * 30} r={f.r ?? 0.17} />
      {q < 1 &&
        pts.map((qq, i) => (
          <mesh key={i} position={flightPos(f, qq)}>
            <sphereGeometry args={[(f.r ?? 0.17) * 0.9 * (1 - i / trail), 10, 8]} />
            <meshBasicMaterial color="#ffffff" transparent opacity={0.45 * (1 - i / trail)} depthWrite={false} />
          </mesh>
        ))}
    </group>
  );
};

// Bat held at the chest; rotates around the body's vertical axis for a swing.
const Bat: React.FC<{ angle: number; tilt?: number }> = ({ angle, tilt = 0.35 }) => (
  <group rotation={[0, angle, 0]} position={[0, 0.05, -0.35]}>
    <group rotation={[0, 0, tilt]}>
      <mesh position={[0.62, 0, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
        <cylinderGeometry args={[0.075, 0.035, 1.15, 12]} />
        <meshStandardMaterial color="#c8925a" roughness={0.45} />
      </mesh>
      <mesh position={[0.03, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.05, 0.05, 0.08, 10]} />
        <meshStandardMaterial color="#2b1d12" />
      </mesh>
    </group>
  </group>
);

// ---------- props ----------
const PropAnim: React.FC<{ p: Prop3D; k: number; t: number; i: number }> = ({ p, k, t, i }) => {
  let pos: V3 = p.pos, s = p.s ?? 0.8, op = 1;
  if (p.anim === "float") pos = [p.pos[0], p.pos[1] + Math.sin(t * 2.2 + i) * 0.15, p.pos[2]];
  if (p.anim === "grow") s *= interpolate(k, [0, 0.3], [0.1, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  if (p.anim === "pop") {
    const a = interpolate(k, [0.45, 0.6], [0, 1], clamp);
    if (a <= 0) return null;
    s *= interpolate(a, [0, 1], [0.2, 1], { easing: Easing.out(Easing.back(3)) });
  }
  if (p.anim === "rise") { pos = [p.pos[0], p.pos[1] + k * 1.4, p.pos[2]]; op = 1 - k * 0.5; }
  if (p.anim === "burst") {
    const a = interpolate(k, [0.5, 0.9], [0, 1], clamp);
    if (a <= 0) return null;
    return <Poof pos={p.pos} k={a} />;
  }
  return <Emoji ch={p.ch} pos={pos} s={s} opacity={op} />;
};

// ---------- 2D overlays ----------
const StatGraphic: React.FC<{ sc: Scene; t: number; first: boolean }> = ({ sc, t, first }) => {
  const inK = interpolate(t, [0, 0.35], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const hl = sc.headline;
  const big = hl.length <= 12;
  return (
    <div style={{ position: "absolute", top: first ? 250 : 210, left: 0, width: "100%", display: "flex", flexDirection: "column", alignItems: "center",
      transform: `translateY(${(1 - inK) * -40}px)`, opacity: inK, fontFamily: "InterDisplay", fontWeight: 900 }}>
      <div style={{ background: "#f2c14e", color: "#0e1628", fontSize: 40, padding: "10px 26px", borderRadius: 10, letterSpacing: 1.5,
        boxShadow: "0 8px 24px rgba(0,0,0,0.35)", maxWidth: 940, textAlign: "center" }}>
        {sc.kicker}
      </div>
      <div style={{ marginTop: 16, background: "linear-gradient(#13213f, #0b1429)", color: "#fff", fontSize: big ? 128 : 92, lineHeight: 1.02,
        padding: "16px 44px 22px", borderRadius: 22, border: "5px solid #f2c14e", boxShadow: "0 18px 40px rgba(0,0,0,0.45)", textAlign: "center",
        maxWidth: 980, letterSpacing: -2 }}>
        {hl}
      </div>
    </div>
  );
};

const Captions: React.FC<{ words: BBData["words"]; t: number }> = ({ words, t }) => {
  const i = words.findIndex((w, j) => t >= w.start && t < (words[j + 1]?.start ?? w.end + 0.4));
  if (i < 0) return null;
  const w = words[i].w;
  const pop = interpolate(t - words[i].start, [0, 0.08], [0.78, 1], { extrapolateRight: "clamp" });
  const key = /\d|%/.test(w) || w.length >= 8;
  return (
    <div style={{ position: "absolute", top: 1360, width: "100%", textAlign: "center", fontFamily: "InterDisplay", fontWeight: 900,
      fontSize: 100, color: key ? "#FFD23F" : "#fff", WebkitTextStroke: "16px #0b0f1a", paintOrder: "stroke fill",
      transform: `scale(${pop})`, letterSpacing: -1, textTransform: "uppercase" }}>
      {w.replace(/[.,!?]$/, "")}
    </div>
  );
};

// ---------- main ----------
export const Baseball3D: React.FC<BBData> = (d) => {
  useAssetsReady();
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const shot = d.shots.find((s) => frame >= s.from && frame < s.from + s.dur) ?? d.shots[d.shots.length - 1];
  const local = frame - shot.from;
  const t = local / fps;
  const k = Math.min(1, local / shot.dur);
  const ek = ease(k);
  let cam = lerp3(shot.cam.from, shot.cam.to, ek);
  if (shot.shake !== undefined) {
    const s = Math.max(0, 1 - Math.abs(k - shot.shake) * 9) * 0.12;
    cam = [cam[0] + Math.sin(frame * 3.1) * s, cam[1] + Math.cos(frame * 2.7) * s, cam[2]];
  }
  let look = lerp3(shot.cam.look, shot.cam.lookTo ?? shot.cam.look, ek);
  if (shot.cam.follow && shot.ball) {
    const f = shot.ball;
    const q = Math.max(0, Math.min(1, (k - f.t0) / (f.t1 - f.t0)));
    const bp = flightPos(f, q);
    cam = [bp[0] + cam[0], bp[1] + cam[1], bp[2] + cam[2]];
    look = [bp[0] + look[0], bp[1] + look[1], bp[2] + look[2]];
  }
  const sc = d.scenes.find((s) => frame >= s.from && frame < s.from + s.dur) ?? d.scenes[d.scenes.length - 1];
  const scIdx = d.scenes.indexOf(sc);
  const moon = shot.set === "moon";
  const night = moon || !!shot.night;
  const sky = moon ? "linear-gradient(#000004, #05060c)" : night ? "linear-gradient(#0a1230, #24305e 70%, #3b3f6e)" : "linear-gradient(#4fa3e8, #a9d6f7 60%, #e7f3fb)";
  const mouth = d.mouth[Math.min(frame, d.mouth.length - 1)] ?? 0;
  const fogCol = moon ? "#05060c" : night ? "#24305e" : "#bfe0f7";
  const showStat = scIdx > 0 && scIdx < d.scenes.length - 1 && sc.headline.length > 0;

  return (
    <AbsoluteFill style={{ background: sky }}>
      <ThreeCanvas width={width} height={height} shadows gl={{ antialias: true, preserveDrawingBuffer: true, toneMapping: THREE.ACESFilmicToneMapping }}>
        <CameraRig pos={cam} look={look} fov={shot.cam.fov ?? 45} />
        <fog attach="fog" args={[fogCol, moon ? 70 : 60, moon ? 300 : 160]} />
        <hemisphereLight args={[moon ? "#8c96b8" : night ? "#9fb0ff" : "#ffffff", moon ? "#222" : "#4a6a3a", moon ? 0.35 : night ? 0.55 : 0.85]} />
        <directionalLight position={moon ? [30, 25, 20] : [14, 22, 12]} intensity={moon ? 2.4 : night ? 1.2 : 1.7} color={night && !moon ? "#fff1d6" : "#ffffff"}
          castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-20} shadow-camera-right={20} shadow-camera-top={20} shadow-camera-bottom={-20} shadow-bias={-0.0004} />
        <directionalLight position={[-10, 6, -14]} intensity={moon ? 0.2 : 0.6} color={night ? "#8fb2ff" : "#ffe6c0"} />
        {moon ? <MoonSet /> : <Ballpark t={t} crowd={shot.crowd ?? 0.25} night={night} board={shot.board} />}
        {shot.actors.map((a, i) => {
          const pos = a.run ? lerp3(a.run[0], a.run[1], ek) : a.pos;
          const heading = a.run ? Math.atan2(a.run[1][0] - a.run[0][0], a.run[1][2] - a.run[0][2]) : (a.heading ?? 0);
          const pose = a.run ? "walk" : a.pose2 && k >= (a.poseAt ?? 0.5) ? a.pose2 : a.pose;
          let bat: React.ReactNode;
          if (a.bat === "rest") bat = <Bat angle={-1.9} tilt={1.0} />;
          else if (a.bat) {
            const q = interpolate(k, [a.bat.t0, a.bat.t1], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
            bat = <Bat angle={a.bat.a0 + (a.bat.a1 - a.bat.a0) * q} tilt={0.35 - q * 0.25} />;
          }
          return (
            <Toon key={i} t={a.run ? t * 1.6 : t} pose={pose} mouth={a.talk === false ? 0 : mouth} position={pos} heading={heading}
              hat={a.hat ?? "cap"} capColor="#c8352e" coat={a.jersey ?? "#1d2f5c"} prop={bat} />
          );
        })}
        {shot.ball && <BallFlight f={shot.ball} k={k} t={t} />}
        {(shot.props ?? []).map((p, i) => <PropAnim key={i} p={p} k={k} t={t} i={i} />)}
      </ThreeCanvas>
      {/* vignette for a filmic look */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%)" }} />
      {!d.clean && showStat && <StatGraphic sc={sc} t={(frame - sc.from) / fps} first={false} />}
      {!d.clean && scIdx === 0 && <StatGraphic sc={sc} t={frame / fps} first />}
      {!d.clean && <Captions words={d.words} t={frame / fps} />}
      <Audio src={staticFile(d.audio)} />
    </AbsoluteFill>
  );
};
