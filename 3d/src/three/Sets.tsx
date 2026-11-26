// Low-poly set pieces for the 3D story shorts. Everything is deterministic (seeded) and static
// unless a frame-derived value (t) is passed in.
import React, { useMemo } from "react";
import * as THREE from "three";
import { random } from "remotion";

const flat = { flatShading: true } as const;

export const Ground: React.FC<{ color: string; size?: number }> = ({
  color,
  size = 80,
}) => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
    <planeGeometry args={[size, size]} />
    <meshStandardMaterial color={color} {...flat} />
  </mesh>
);

export const Tree: React.FC<{
  pos: [number, number, number];
  s?: number;
  leaf?: string;
  blossom?: boolean;
}> = ({ pos, s = 1, leaf = "#3f9b4a", blossom }) => (
  <group position={pos} scale={s}>
    <mesh position={[0, 0.6, 0]} castShadow>
      <cylinderGeometry args={[0.12, 0.18, 1.2, 6]} />
      <meshStandardMaterial color="#7a5232" {...flat} />
    </mesh>
    <mesh position={[0, 1.6, 0]} castShadow>
      <icosahedronGeometry args={[0.85, 0]} />
      <meshStandardMaterial color={leaf} {...flat} />
    </mesh>
    {blossom &&
      [0, 1, 2, 3, 4, 5].map((i) => (
        <mesh
          key={i}
          position={[
            Math.cos(i) * 0.7,
            1.5 + Math.sin(i * 2) * 0.4,
            Math.sin(i) * 0.7,
          ]}
        >
          <icosahedronGeometry args={[0.16, 0]} />
          <meshStandardMaterial color="#f7c6d9" {...flat} />
        </mesh>
      ))}
  </group>
);

export const Flower: React.FC<{
  pos: [number, number, number];
  color: string;
  wilt?: number;
}> = ({ pos, color, wilt = 0 }) => (
  <group position={pos} rotation={[wilt * 0.9, 0, 0]}>
    <mesh position={[0, 0.2, 0]}>
      <cylinderGeometry args={[0.015, 0.015, 0.4, 4]} />
      <meshStandardMaterial color={wilt > 0.5 ? "#7d6b3a" : "#3c8c3f"} />
    </mesh>
    <mesh position={[0, 0.42, 0]}>
      <icosahedronGeometry args={[0.09, 0]} />
      <meshStandardMaterial color={wilt > 0.5 ? "#8c7a55" : color} {...flat} />
    </mesh>
  </group>
);

export const Cloud: React.FC<{ pos: [number, number, number]; s?: number }> = ({
  pos,
  s = 1,
}) => (
  <group position={pos} scale={s}>
    {[
      [0, 0, 0, 1],
      [0.9, -0.1, 0, 0.75],
      [-0.9, -0.15, 0, 0.7],
      [0.3, 0.4, 0, 0.7],
    ].map(([x, y, z, r], i) => (
      <mesh key={i} position={[x, y, z]}>
        <icosahedronGeometry args={[r, 1]} />
        <meshStandardMaterial color="#ffffff" {...flat} />
      </mesh>
    ))}
  </group>
);

export const House: React.FC<{
  pos: [number, number, number];
  wall?: string;
  roof?: string;
  rot?: number;
}> = ({ pos, wall = "#f0e2c8", roof = "#b5453a", rot = 0 }) => (
  <group position={pos} rotation={[0, rot, 0]}>
    <mesh position={[0, 0.8, 0]} castShadow>
      <boxGeometry args={[2, 1.6, 1.8]} />
      <meshStandardMaterial color={wall} {...flat} />
    </mesh>
    <mesh position={[0, 2.0, 0]} rotation={[0, Math.PI / 4, 0]} castShadow>
      <coneGeometry args={[1.6, 0.9, 4]} />
      <meshStandardMaterial color={roof} {...flat} />
    </mesh>
    <mesh position={[0, 0.5, 0.91]}>
      <boxGeometry args={[0.45, 0.9, 0.04]} />
      <meshStandardMaterial color="#6b4529" />
    </mesh>
    {[-0.6, 0.6].map((x) => (
      <mesh key={x} position={[x, 1.05, 0.91]}>
        <boxGeometry args={[0.38, 0.38, 0.04]} />
        <meshStandardMaterial color="#9fd3ec" emissive="#355" />
      </mesh>
    ))}
  </group>
);

export const Hive: React.FC<{ pos: [number, number, number] }> = ({ pos }) => (
  <group position={pos}>
    <mesh position={[0, 0.5, 0]}>
      <boxGeometry args={[0.1, 1, 0.1]} />
      <meshStandardMaterial color="#6b4529" />
    </mesh>
    {[0, 1, 2].map((i) => (
      <mesh key={i} position={[0, 1.15 + i * 0.32, 0]} castShadow>
        <boxGeometry args={[0.9 - i * 0.04, 0.3, 0.7]} />
        <meshStandardMaterial color={i % 2 ? "#e9c46a" : "#f4d98b"} {...flat} />
      </mesh>
    ))}
    <mesh position={[0, 2.12, 0]}>
      <boxGeometry args={[1.0, 0.08, 0.8]} />
      <meshStandardMaterial color="#8a5a33" />
    </mesh>
  </group>
);

export const Shelf: React.FC<{
  pos: [number, number, number];
  fill: number;
  seed: string;
  rot?: number;
}> = ({ pos, fill, seed, rot = 0 }) => {
  const colors = [
    "#e63946",
    "#f4a261",
    "#2a9d8f",
    "#e9c46a",
    "#8ab17d",
    "#d62828",
    "#6a994e",
  ];
  return (
    <group position={pos} rotation={[0, rot, 0]}>
      <mesh position={[0, 1.1, -0.25]}>
        <boxGeometry args={[3, 2.2, 0.1]} />
        <meshStandardMaterial color="#d8dde6" />
      </mesh>
      {[0.25, 0.85, 1.45, 2.05].map((y, row) => (
        <group key={y}>
          <mesh position={[0, y, 0]}>
            <boxGeometry args={[3, 0.06, 0.55]} />
            <meshStandardMaterial color="#aeb6c2" />
          </mesh>
          {new Array(9).fill(0).map((_, i) => {
            const keep = random(`${seed}${row}${i}`) < fill;
            if (!keep) return null;
            return (
              <mesh
                key={i}
                position={[-1.3 + i * 0.33, y + 0.17, 0]}
                castShadow
              >
                <sphereGeometry args={[0.13, 7, 6]} />
                <meshStandardMaterial
                  color={colors[(row * 3 + i) % colors.length]}
                  {...flat}
                />
              </mesh>
            );
          })}
        </group>
      ))}
    </group>
  );
};

// Emoji on a camera-facing plane. Gives every topic its own recognisable prop cheaply.
const texCache = new Map<string, THREE.CanvasTexture>();
export const emojiTexture = (ch: string) => {
  if (texCache.has(ch)) return texCache.get(ch)!;
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d")!;
  g.font = '200px "Noto Color Emoji"';
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText(ch, 128, 140);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  texCache.set(ch, t);
  return t;
};

export const Emoji: React.FC<{
  ch: string;
  pos: [number, number, number];
  s?: number;
  opacity?: number;
  spin?: number;
}> = ({ ch, pos, s = 1, opacity = 1, spin = 0 }) => {
  const tex = useMemo(() => emojiTexture(ch), [ch]);
  return (
    <sprite position={pos} scale={[s, s, s]} material-rotation={spin}>
      <spriteMaterial
        map={tex}
        transparent
        opacity={opacity}
        depthWrite={false}
      />
    </sprite>
  );
};

// A little puff of white spheres expanding from a point (for things vanishing).
export const Poof: React.FC<{ pos: [number, number, number]; k: number }> = ({
  pos,
  k,
}) => {
  if (k <= 0 || k >= 1) return null;
  return (
    <group position={pos}>
      {new Array(10).fill(0).map((_, i) => {
        const a = (i / 10) * Math.PI * 2;
        const d = k * 0.9;
        return (
          <mesh
            key={i}
            position={[
              Math.cos(a) * d,
              Math.sin(a * 1.3) * d * 0.6,
              Math.sin(a) * d,
            ]}
            scale={1 - k}
          >
            <icosahedronGeometry args={[0.18, 0]} />
            <meshStandardMaterial
              color="#ffffff"
              transparent
              opacity={1 - k}
              {...flat}
            />
          </mesh>
        );
      })}
    </group>
  );
};
