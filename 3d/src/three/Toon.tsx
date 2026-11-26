// Low-poly 3D cartoon character: round white head, dot eyes, coat, hat. All motion is driven
// by props computed from useCurrentFrame() (no useFrame), as Remotion requires.
import React from "react";

export type Pose =
  | "idle"
  | "walk"
  | "shock"
  | "point"
  | "carry"
  | "wave"
  | "think"
  | "cheer"
  | "sad";

const flat = { flatShading: true } as const;

const Limb: React.FC<{
  len: number;
  r: number;
  color: string;
  rot: [number, number, number];
  pos: [number, number, number];
}> = ({ len, r, color, rot, pos }) => (
  // pivot at the top of the limb so rotations swing from the shoulder / hip
  <group position={pos} rotation={rot}>
    <mesh position={[0, -len / 2, 0]} castShadow>
      <cylinderGeometry args={[r, r * 0.9, len, 8]} />
      <meshStandardMaterial color={color} {...flat} />
    </mesh>
    <mesh position={[0, -len, 0]} castShadow>
      <sphereGeometry args={[r * 1.25, 10, 8]} />
      <meshStandardMaterial
        color={color === "#2b2f3a" ? "#1b1e26" : "#f4efe6"}
        {...flat}
      />
    </mesh>
  </group>
);

export const Toon: React.FC<{
  t: number; // seconds into the current shot (drives walk cycle, blinks, gestures)
  pose: Pose;
  mouth: number; // 0..1 lip-sync
  coat?: string;
  hat?: "top" | "cap" | "none" | "straw";
  position?: [number, number, number];
  heading?: number; // radians, 0 = facing camera (+z)
  scale?: number;
  prop?: React.ReactNode; // something held in front (box, sign, brush)
}> = ({
  t,
  pose,
  mouth,
  coat = "#c8352e",
  hat = "top",
  position = [0, 0, 0],
  heading = 0,
  scale = 1,
  prop,
}) => {
  const walking = pose === "walk";
  const cyc = Math.sin(t * 9);
  const legSwing = walking ? cyc * 0.55 : 0;
  const bob = walking
    ? Math.abs(Math.cos(t * 9)) * 0.06
    : Math.sin(t * 2.2) * 0.015;
  const shockJump =
    pose === "shock"
      ? Math.max(0, Math.sin(Math.min(t, 0.5) * Math.PI * 2)) * 0.18
      : 0;
  const cheerJump = pose === "cheer" ? Math.abs(Math.sin(t * 6)) * 0.22 : 0;

  // arm rotations [x, y, z] for (left, right); z swings the arm out sideways, x forward
  let la: [number, number, number] = [walking ? -legSwing : 0, 0, 0.12];
  let ra: [number, number, number] = [walking ? legSwing : 0, 0, -0.12];
  if (pose === "shock") {
    la = [0, 0, 2.5];
    ra = [0, 0, -2.5];
  }
  if (pose === "point") {
    ra = [0, 0, -2.2 + Math.sin(t * 3) * 0.08];
  }
  if (pose === "carry") {
    la = [-1.25, 0, 0.25];
    ra = [-1.25, 0, -0.25];
  }
  if (pose === "wave") {
    ra = [0, 0, -2.6 + Math.sin(t * 10) * 0.35];
  }
  if (pose === "think") {
    ra = [-2.1, 0, 0.55];
  }
  if (pose === "cheer") {
    la = [0, 0, 2.7];
    ra = [0, 0, -2.7];
  }
  if (pose === "sad") {
    la = [0.1, 0, 0.05];
    ra = [0.1, 0, -0.05];
  }

  const headTilt =
    pose === "sad" ? 0.25 : pose === "think" ? -0.15 : Math.sin(t * 1.7) * 0.05;
  const blink = (t * 30 + 11) % 95 < 4;
  const eyeH = blink ? 0.01 : pose === "shock" ? 0.085 : 0.065;
  const mouthOpen = pose === "shock" ? Math.max(0.5, mouth) : mouth;

  return (
    <group
      position={[
        position[0],
        position[1] + bob + shockJump + cheerJump,
        position[2],
      ]}
      rotation={[0, heading, 0]}
      scale={scale}
    >
      {/* legs */}
      <Limb
        len={0.55}
        r={0.075}
        color="#2b2f3a"
        rot={[legSwing, 0, 0]}
        pos={[-0.13, 0.58, 0]}
      />
      <Limb
        len={0.55}
        r={0.075}
        color="#2b2f3a"
        rot={[-legSwing, 0, 0]}
        pos={[0.13, 0.58, 0]}
      />
      {/* coat body */}
      <mesh position={[0, 0.9, 0]} castShadow>
        <cylinderGeometry args={[0.24, 0.32, 0.72, 10]} />
        <meshStandardMaterial color={coat} {...flat} />
      </mesh>
      {[0.98, 0.86, 0.74].map((y) => (
        <mesh key={y} position={[0, y, 0.27]}>
          <sphereGeometry args={[0.025, 6, 6]} />
          <meshStandardMaterial color="#f2c14e" />
        </mesh>
      ))}
      {/* arms */}
      <Limb len={0.5} r={0.06} color={coat} rot={la} pos={[-0.3, 1.18, 0]} />
      <Limb len={0.5} r={0.06} color={coat} rot={ra} pos={[0.3, 1.18, 0]} />
      {prop && <group position={[0, 0.95, 0.45]}>{prop}</group>}
      {/* head */}
      <group position={[0, 1.62, 0]} rotation={[headTilt, 0, 0]}>
        <mesh castShadow>
          <sphereGeometry args={[0.36, 20, 16]} />
          <meshStandardMaterial color="#fbf8f2" roughness={0.6} />
        </mesh>
        {/* eyes: white ball, big dark pupil, shine dot; squash vertically to blink */}
        {[-0.12, 0.12].map((x) => (
          <group
            key={x}
            position={[x, 0.06, 0.29]}
            scale={[1, eyeH / 0.065, 1]}
          >
            <mesh>
              <sphereGeometry args={[0.085, 14, 10]} />
              <meshStandardMaterial color="#ffffff" />
            </mesh>
            <mesh position={[0, -0.005, 0.055]}>
              <sphereGeometry args={[0.048, 12, 10]} />
              <meshStandardMaterial color="#14110f" />
            </mesh>
            <mesh position={[0.018, 0.022, 0.095]}>
              <sphereGeometry args={[0.014, 8, 6]} />
              <meshBasicMaterial color="#ffffff" />
            </mesh>
          </group>
        ))}
        {/* nose + rosy cheeks */}
        <mesh position={[0, -0.04, 0.36]}>
          <sphereGeometry args={[0.035, 10, 8]} />
          <meshStandardMaterial color="#f2c7b0" />
        </mesh>
        {[-0.21, 0.21].map((x) => (
          <mesh key={x} position={[x, -0.07, 0.28]} scale={[1, 0.6, 0.4]}>
            <sphereGeometry args={[0.06, 10, 8]} />
            <meshStandardMaterial color="#ff9aa8" transparent opacity={0.7} />
          </mesh>
        ))}
        {/* brows */}
        {[-1, 1].map((s) => (
          <mesh
            key={s}
            position={[s * 0.12, 0.17 + (pose === "shock" ? 0.04 : 0), 0.32]}
            rotation={[
              0,
              0,
              s * (pose === "sad" ? 0.35 : pose === "think" ? -0.2 : 0),
            ]}
          >
            <boxGeometry args={[0.11, 0.022, 0.02]} />
            <meshStandardMaterial color="#222" />
          </mesh>
        ))}
        {/* mouth: opens with the voice; when quiet it's a smile (or a frown when sad) */}
        {mouthOpen > 0.08 ? (
          <group position={[0, -0.15, 0.31]}>
            <mesh scale={[1, 0.3 + mouthOpen * 1.4, 0.5]}>
              <sphereGeometry args={[0.075, 14, 10]} />
              <meshStandardMaterial color="#5a1a24" />
            </mesh>
            {mouthOpen > 0.35 && (
              <mesh
                position={[0, -0.03 - mouthOpen * 0.02, 0.02]}
                scale={[1, 0.5, 0.4]}
              >
                <sphereGeometry args={[0.045, 10, 8]} />
                <meshStandardMaterial color="#ef7b8c" />
              </mesh>
            )}
          </group>
        ) : (
          <mesh
            position={[0, pose === "sad" ? -0.19 : -0.12, 0.31]}
            rotation={[0, 0, pose === "sad" ? 0 : Math.PI]}
          >
            <torusGeometry args={[0.07, 0.014, 6, 12, Math.PI]} />
            <meshStandardMaterial color="#3a1420" />
          </mesh>
        )}
        {/* hat */}
        {hat === "top" && (
          <group position={[0, 0.3, 0]}>
            <mesh>
              <cylinderGeometry args={[0.36, 0.36, 0.03, 16]} />
              <meshStandardMaterial color="#14161c" />
            </mesh>
            <mesh position={[0, 0.2, 0]}>
              <cylinderGeometry args={[0.23, 0.23, 0.4, 16]} />
              <meshStandardMaterial color="#14161c" />
            </mesh>
          </group>
        )}
        {hat === "cap" && (
          <group position={[0, 0.2, 0]}>
            <mesh>
              <sphereGeometry
                args={[0.33, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2]}
              />
              <meshStandardMaterial color="#20345c" />
            </mesh>
            <mesh position={[0, 0, 0.3]}>
              <boxGeometry args={[0.36, 0.03, 0.22]} />
              <meshStandardMaterial color="#20345c" />
            </mesh>
          </group>
        )}
        {hat === "straw" && (
          <group position={[0, 0.26, 0]}>
            <mesh>
              <cylinderGeometry args={[0.55, 0.55, 0.03, 16]} />
              <meshStandardMaterial color="#d9b45a" {...flat} />
            </mesh>
            <mesh position={[0, 0.1, 0]}>
              <cylinderGeometry args={[0.24, 0.28, 0.2, 12]} />
              <meshStandardMaterial color="#d9b45a" {...flat} />
            </mesh>
          </group>
        )}
      </group>
    </group>
  );
};
