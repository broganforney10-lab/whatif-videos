// 3D cartoon-story Short: every shot has its own set, character action and camera move.
// Shot list comes from public/story/<id>.json; voice, lip-sync and word timings from public/data/<id>.json.
import React, { useEffect, useLayoutEffect, useState } from "react";
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
import {
  Cloud,
  Emoji,
  Flower,
  Ground,
  Hive,
  House,
  Poof,
  Shelf,
  Tree,
} from "./Sets";

type V3 = [number, number, number];
export type Prop3D = {
  ch: string;
  pos: V3;
  s?: number;
  anim?: "buzz" | "float" | "poof" | "shrink" | "grow" | "flyaway" | "rise";
};
export type Shot = {
  from: number;
  dur: number; // frames
  set: "meadow" | "orchard" | "store" | "wheat" | "town" | "beach" | "night" | "snow" | "home";
  pose: Pose;
  pose2?: Pose;
  poseAt?: number; // switch to pose2 at poseAt (0..1 of the shot)
  walk?: [[number, number], [number, number]]; // x,z start -> end
  heading?: number;
  cam: { from: V3; to: V3; look: V3; lookTo?: V3; fov?: number };
  props?: Prop3D[];
  fill?: [number, number]; // store shelf fill, start -> end
  wilt?: [number, number]; // meadow wilt, start -> end
  hat?: "top" | "cap" | "none" | "straw";
  coat?: string;
  held?: string; // emoji held in hand
};
export type StoryData = {
  id: string;
  durationInFrames: number;
  audio: string;
  shots: Shot[];
  words: { w: string; start: number; end: number }[];
  mouth: number[];
};

const fonts = loadFont({
  family: "InterDisplay",
  url: staticFile("fonts/InterDisplay-Black.otf"),
  weight: "900",
});

const useAssetsReady = () => {
  const [h] = useState(() => delayRender("fonts+emoji"));
  useEffect(() => {
    Promise.all([fonts, document.fonts.load('200px "Noto Color Emoji"', "🐝")])
      .catch(() => null)
      .then(() => continueRender(h));
  }, [h]);
};

const ease = Easing.bezier(0.45, 0, 0.25, 1);
const lerp3 = (a: V3, b: V3, k: number): V3 => [
  a[0] + (b[0] - a[0]) * k,
  a[1] + (b[1] - a[1]) * k,
  a[2] + (b[2] - a[2]) * k,
];

const CameraRig: React.FC<{ pos: V3; look: V3; fov: number }> = ({
  pos,
  look,
  fov,
}) => {
  const camera = useThree((s) => s.camera) as import("three").PerspectiveCamera;
  useLayoutEffect(() => {
    camera.position.set(...pos);
    camera.fov = fov;
    camera.lookAt(...look);
    camera.updateProjectionMatrix();
  }, [camera, pos, look, fov]);
  return null;
};

const SKY: Record<Shot["set"], [string, string]> = {
  meadow: ["#8fd3ff", "#cfefff"],
  orchard: ["#9fd8ff", "#e6f6ff"],
  store: ["#f3efe6", "#f3efe6"],
  wheat: ["#ffd8a8", "#fff1d6"],
  town: ["#94cdf7", "#dff2ff"],
  beach: ["#7cc8f5", "#d4f1ff"],
  night: ["#0b1030", "#2a2f5c"],
  snow: ["#b9dcf5", "#eef7ff"],
  home: ["#f4e7d3", "#f4e7d3"],
};

const SetPiece: React.FC<{ shot: Shot; k: number; t: number }> = ({
  shot,
  k,
  t,
}) => {
  const wilt = shot.wilt ? shot.wilt[0] + (shot.wilt[1] - shot.wilt[0]) * k : 0;
  switch (shot.set) {
    case "meadow":
      return (
        <>
          <Ground color={wilt > 0.5 ? "#a8a060" : "#7cc56a"} />
          {new Array(70).fill(0).map((_, i) => (
            <Flower
              key={i}
              pos={[
                (random(`fx${i}`) - 0.5) * 16,
                0,
                (random(`fz${i}`) - 0.6) * 14,
              ]}
              color={["#ff6b9a", "#ffd23f", "#f8f8ff", "#b388ff"][i % 4]}
              wilt={wilt}
            />
          ))}
          <Hive pos={[2.2, 0, -1.5]} />
          {[
            [-5, -6],
            [5, -8],
            [-8, -3],
            [8, -4],
            [0, -11],
          ].map(([x, z], i) => (
            <Tree key={i} pos={[x, 0, z]} s={1.4} />
          ))}
          <Cloud pos={[-4, 7, -14]} s={1.6} />
          <Cloud pos={[6, 8, -16]} s={1.3} />
        </>
      );
    case "orchard":
      return (
        <>
          <Ground color="#86c36d" />
          {new Array(5)
            .fill(0)
            .flatMap((_, r) =>
              new Array(6)
                .fill(0)
                .map((__, c) => (
                  <Tree
                    key={`${r}${c}`}
                    pos={[-6 + c * 2.4, 0, -2 - r * 3]}
                    s={1.1}
                    leaf="#5aa557"
                    blossom
                  />
                )),
            )}
          <Cloud pos={[3, 7, -18]} s={1.5} />
        </>
      );
    case "store": {
      const fill = shot.fill
        ? shot.fill[0] + (shot.fill[1] - shot.fill[0]) * k
        : 1;
      return (
        <>
          <Ground color="#e9e4da" />
          <Shelf pos={[-2.3, 0, -2]} fill={fill} seed="a" rot={0.35} />
          <Shelf pos={[2.3, 0, -2]} fill={fill} seed="b" rot={-0.35} />
          <Shelf pos={[0, 0, -4.5]} fill={fill} seed="c" />
        </>
      );
    }
    case "wheat":
      return (
        <>
          <Ground color="#d9b95c" />
          {new Array(260).fill(0).map((_, i) => {
            const x = (random(`wx${i}`) - 0.5) * 18,
              z = (random(`wz${i}`) - 0.7) * 16;
            const sway = Math.sin(t * 2 + x * 0.6) * 0.12;
            return (
              <mesh key={i} position={[x, 0.45, z]} rotation={[0, 0, sway]}>
                <cylinderGeometry args={[0.03, 0.02, 0.9, 4]} />
                <meshStandardMaterial color="#e8c766" flatShading />
              </mesh>
            );
          })}
          <House pos={[-5, 0, -9]} wall="#e6d2b0" roof="#a8442f" rot={0.4} />
          <Cloud pos={[2, 7, -16]} s={1.5} />
        </>
      );
    case "town":
      return (
        <>
          <Ground color="#8fbf6e" />
          <mesh position={[0, 0.01, -2]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[40, 3]} />
            <meshStandardMaterial color="#5b5f66" />
          </mesh>
          {[-6, -3, 3, 6].map((x, i) => (
            <House
              key={x}
              pos={[x, 0, -6]}
              wall={["#f0e2c8", "#dfe9f5", "#f5d9d0", "#e3f0d8"][i]}
            />
          ))}
          {/* market stall */}
          <group position={[0, 0, -0.5]}>
            <mesh position={[0, 0.5, 0]}>
              <boxGeometry args={[2.4, 1, 0.9]} />
              <meshStandardMaterial color="#b07a4a" flatShading />
            </mesh>
            <mesh position={[0, 2.1, 0]} rotation={[0.25, 0, 0]}>
              <boxGeometry args={[2.8, 0.08, 1.4]} />
              <meshStandardMaterial color="#e63946" />
            </mesh>
            {[-1.1, 1.1].map((x) => (
              <mesh key={x} position={[x, 1.3, 0.35]}>
                <cylinderGeometry args={[0.04, 0.04, 1.6, 6]} />
                <meshStandardMaterial color="#6b4529" />
              </mesh>
            ))}
          </group>
          <Cloud pos={[-3, 7, -16]} s={1.4} />
        </>
      );
    case "beach":
      return (
        <>
          <Ground color="#f1d79a" />
          <mesh position={[0, 0.03, -9]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[80, 14]} />
            <meshStandardMaterial color="#2fa7c9" flatShading />
          </mesh>
          {new Array(14).fill(0).map((_, i) => (
            <mesh key={i} position={[(random(`bw${i}`) - 0.5) * 20, 0.06, -3 - random(`bz${i}`) * 10]} rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[1.4, 0.06]} />
              <meshBasicMaterial color="#e8fbff" transparent opacity={0.5 + 0.5 * Math.sin(t * 2 + i)} />
            </mesh>
          ))}
          {[[-4, -1], [4.5, -2.5], [-6, -4]].map(([x, z], i) => (
            <group key={i} position={[x, 0, z]}>
              <mesh position={[0, 1.4, 0]} rotation={[0, 0, 0.12]}><cylinderGeometry args={[0.1, 0.16, 2.8, 6]} /><meshStandardMaterial color="#8a6239" flatShading /></mesh>
              {[0, 1, 2, 3, 4].map((j) => (
                <mesh key={j} position={[Math.cos(j * 1.26) * 0.7 + 0.15, 2.8, Math.sin(j * 1.26) * 0.7]} rotation={[Math.sin(j * 1.26) * 0.6, j * 1.26, -Math.cos(j * 1.26) * 0.6]}>
                  <boxGeometry args={[1.5, 0.05, 0.35]} /><meshStandardMaterial color="#3e9a4a" flatShading />
                </mesh>
              ))}
            </group>
          ))}
          <Cloud pos={[2, 7, -18]} s={1.5} />
        </>
      );
    case "night":
      return (
        <>
          <Ground color="#2b3350" />
          {new Array(60).fill(0).map((_, i) => (
            <mesh key={i} position={[(random(`sx${i}`) - 0.5) * 40, 4 + random(`sy${i}`) * 14, -18 - random(`sz${i}`) * 6]}>
              <sphereGeometry args={[0.06 + random(`ss${i}`) * 0.06, 4, 4]} />
              <meshBasicMaterial color="#ffffff" transparent opacity={0.5 + 0.5 * Math.abs(Math.sin(t * 2 + i))} />
            </mesh>
          ))}
          {[-6, 6].map((x, i) => <House key={x} pos={[x, 0, -7]} wall={["#4a5578", "#5a4f78"][i]} roof="#2b2440" />)}
          <Tree pos={[-3, 0, -5]} s={1.3} leaf="#24543a" />
          <Tree pos={[3.5, 0, -6]} s={1.2} leaf="#24543a" />
        </>
      );
    case "snow":
      return (
        <>
          <Ground color="#f4f9ff" />
          {new Array(16).fill(0).map((_, i) => (
            <mesh key={i} position={[(random(`ix${i}`) - 0.5) * 18, 0.4 + random(`iy${i}`) * 0.6, -3 - random(`iz${i}`) * 10]} rotation={[0, random(`ir${i}`) * 3, 0]}>
              <boxGeometry args={[1 + random(`iw${i}`), 0.8 + random(`ih${i}`) * 1.4, 1]} />
              <meshStandardMaterial color="#bfe4ff" transparent opacity={0.9} flatShading />
            </mesh>
          ))}
          {[[-6, -9], [5, -11]].map(([x, z], i) => (
            <mesh key={i} position={[x, 2.5, z]}><coneGeometry args={[3, 5, 5]} /><meshStandardMaterial color="#e6f2ff" flatShading /></mesh>
          ))}
          {new Array(40).fill(0).map((_, i) => (
            <mesh key={`f${i}`} position={[(random(`fx${i}`) - 0.5) * 12, ((random(`fy${i}`) * 6 - t * 0.8) % 6 + 6) % 6, (random(`fz${i}`) - 0.5) * 8]}>
              <sphereGeometry args={[0.04, 4, 4]} /><meshBasicMaterial color="#ffffff" />
            </mesh>
          ))}
        </>
      );
    case "home":
      return (
        <>
          <Ground color="#c99a6b" />
          <mesh position={[0, 2, -3]}><boxGeometry args={[14, 4, 0.2]} /><meshStandardMaterial color="#f3e3c7" /></mesh>
          <mesh position={[-5, 2, 0]}><boxGeometry args={[0.2, 4, 8]} /><meshStandardMaterial color="#ecd7b4" /></mesh>
          <mesh position={[1.5, 2.2, -2.88]}><boxGeometry args={[1.6, 1.1, 0.04]} /><meshStandardMaterial color="#9fd3ec" emissive="#355" /></mesh>
          <group position={[-2.2, 0, -2]}>
            <mesh position={[0, 0.4, 0]}><boxGeometry args={[2.2, 0.5, 0.9]} /><meshStandardMaterial color="#4f7cac" flatShading /></mesh>
            <mesh position={[0, 0.85, -0.35]}><boxGeometry args={[2.2, 0.6, 0.2]} /><meshStandardMaterial color="#4f7cac" flatShading /></mesh>
          </group>
          <group position={[2.2, 0, -1.2]}>
            <mesh position={[0, 0.75, 0]}><boxGeometry args={[1.4, 0.06, 0.8]} /><meshStandardMaterial color="#8a5a33" /></mesh>
            {[[-0.6, -0.3], [0.6, -0.3], [-0.6, 0.3], [0.6, 0.3]].map(([x, z], i) => (
              <mesh key={i} position={[x, 0.37, z]}><boxGeometry args={[0.06, 0.74, 0.06]} /><meshStandardMaterial color="#6b4529" /></mesh>
            ))}
          </group>
          <mesh position={[-4, 1.6, -2.6]}><cylinderGeometry args={[0.03, 0.03, 3.2, 6]} /><meshStandardMaterial color="#333" /></mesh>
          <mesh position={[-4, 3.2, -2.6]}><coneGeometry args={[0.35, 0.4, 10, 1, true]} /><meshStandardMaterial color="#f6d365" emissive="#a07000" side={2} /></mesh>
        </>
      );
  }
};

const PropAnim: React.FC<{ p: Prop3D; k: number; t: number; i: number }> = ({
  p,
  k,
  t,
  i,
}) => {
  let pos: V3 = p.pos,
    s = p.s ?? 0.8,
    op = 1;
  switch (p.anim) {
    case "buzz":
      pos = [
        p.pos[0] + Math.sin(t * 5 + i) * 0.5,
        p.pos[1] + Math.sin(t * 7 + i * 2) * 0.25,
        p.pos[2] + Math.cos(t * 4 + i) * 0.4,
      ];
      break;
    case "float":
      pos = [p.pos[0], p.pos[1] + Math.sin(t * 2 + i) * 0.15, p.pos[2]];
      break;
    case "poof": {
      const pk = interpolate(k, [0.35, 0.5], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      pos = [
        p.pos[0] + Math.sin(t * 5 + i) * 0.4,
        p.pos[1] + Math.sin(t * 7 + i) * 0.2,
        p.pos[2],
      ];
      s *= 1 - pk;
      if (pk >= 1)
        return (
          <Poof
            pos={p.pos}
            k={interpolate(k, [0.5, 0.8], [0, 1], {
              extrapolateRight: "clamp",
            })}
          />
        );
      break;
    }
    case "shrink":
      s *= interpolate(k, [0.2, 0.9], [1, 0.35], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      break;
    case "grow":
      s *= interpolate(k, [0, 0.4], [0.2, 1], {
        extrapolateRight: "clamp",
        easing: Easing.out(Easing.back(2)),
      });
      break;
    case "flyaway":
      pos = [p.pos[0] + k * 6, p.pos[1] + k * 4, p.pos[2] - k * 3];
      op = 1 - k * 0.6;
      break;
    case "rise":
      pos = [p.pos[0], p.pos[1] + k * 1.5, p.pos[2]];
      break;
  }
  return <Emoji ch={p.ch} pos={pos} s={s} opacity={op} />;
};

const Captions: React.FC<{ words: StoryData["words"]; t: number }> = ({
  words,
  t,
}) => {
  // one word at a time, like the reference style; numbers / key words in yellow
  const i = words.findIndex(
    (w, j) => t >= w.start && t < (words[j + 1]?.start ?? w.end + 0.4),
  );
  if (i < 0) return null;
  const w = words[i].w;
  const pop = interpolate(t - words[i].start, [0, 0.08], [0.8, 1], {
    extrapolateRight: "clamp",
  });
  const key = /\d|%/.test(w) || w.length >= 9;
  return (
    <div
      style={{
        position: "absolute",
        top: 1330,
        width: "100%",
        textAlign: "center",
        fontFamily: "InterDisplay",
        fontWeight: 900,
        fontSize: 92,
        color: key ? "#FFD23F" : "#fff",
        WebkitTextStroke: "14px #111",
        paintOrder: "stroke fill",
        transform: `scale(${pop})`,
        letterSpacing: -1,
      }}
    >
      {w.replace(/[.,!?]$/, "")}
    </div>
  );
};

export const Story3D: React.FC<StoryData> = (d) => {
  useAssetsReady();
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const shot =
    d.shots.find((s) => frame >= s.from && frame < s.from + s.dur) ??
    d.shots[d.shots.length - 1];
  const local = frame - shot.from;
  const t = local / fps;
  const k = Math.min(1, local / shot.dur);
  const ek = ease(k);
  const cam = lerp3(shot.cam.from, shot.cam.to, ek);
  const look = lerp3(shot.cam.look, shot.cam.lookTo ?? shot.cam.look, ek);
  const walk = shot.walk;
  const pos: V3 = walk
    ? [
        walk[0][0] + (walk[1][0] - walk[0][0]) * ek,
        0,
        walk[0][1] + (walk[1][1] - walk[0][1]) * ek,
      ]
    : [0, 0, 0];
  const heading = walk
    ? Math.atan2(walk[1][0] - walk[0][0], walk[1][1] - walk[0][1])
    : (shot.heading ?? 0);
  const pose = shot.pose2 && k >= (shot.poseAt ?? 0.5) ? shot.pose2 : shot.pose;
  const mouth = d.mouth[Math.min(frame, d.mouth.length - 1)] ?? 0;
  const fade = interpolate(local, [0, 4], [0, 1], {
    extrapolateRight: "clamp",
  });
  const [top, bottom] = SKY[shot.set];

  return (
    <AbsoluteFill style={{ background: `linear-gradient(${top}, ${bottom})` }}>
      <ThreeCanvas
        width={width}
        height={height}
        shadows
        gl={{ antialias: true, preserveDrawingBuffer: true }}
      >
        <CameraRig pos={cam} look={look} fov={shot.cam.fov ?? 45} />
        <fog attach="fog" args={[bottom, 14, 40]} />
        <hemisphereLight args={["#ffffff", "#8a7a5a", 0.9]} />
        <directionalLight
          position={[6, 10, 6]}
          intensity={1.5}
          castShadow
          shadow-mapSize={[1024, 1024]}
          shadow-camera-left={-10}
          shadow-camera-right={10}
          shadow-camera-top={10}
          shadow-camera-bottom={-10}
        />
        <SetPiece shot={shot} k={k} t={t} />
        <Toon
          t={t}
          pose={walk && pose === shot.pose ? "walk" : pose}
          mouth={mouth}
          position={pos}
          heading={walk ? heading : (shot.heading ?? 0)}
          hat={shot.hat ?? "straw"}
          coat={shot.coat ?? "#c8352e"}
          prop={
            shot.held ? (
              <Emoji ch={shot.held} pos={[0, 0.1, 0]} s={0.55} />
            ) : undefined
          }
        />
        {(shot.props ?? []).map((p, i) => (
          <PropAnim key={i} p={p} k={k} t={t} i={i} />
        ))}
      </ThreeCanvas>
      <AbsoluteFill style={{ background: "#000", opacity: 1 - fade }} />
      <Captions words={d.words} t={frame / fps} />
      <Audio src={staticFile(d.audio)} />
    </AbsoluteFill>
  );
};
