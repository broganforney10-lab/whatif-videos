import React from "react";
import { interpolate } from "remotion";

export type Mood = "shock" | "point" | "worried" | "think" | "excited" | "wave";

// "Blip": the channel's narrator. Mint blob, yellow antenna bulb, navy outline.
const BODY = "#5ED6B4";
const BODY_DARK = "#3BB596";
const LINE = "#16203A";
const BULB = "#FFC43D";

type Pt = [number, number];
// Hand positions (left, right) per mood, in the 600x700 character box.
const HANDS: Record<Mood, [Pt, Pt]> = {
  shock: [
    [165, 455],
    [435, 455],
  ],
  point: [
    [75, 575],
    [575, 150],
  ],
  worried: [
    [262, 610],
    [338, 610],
  ],
  think: [
    [75, 575],
    [330, 590],
  ],
  excited: [
    [30, 175],
    [570, 175],
  ],
  wave: [
    [75, 575],
    [560, 190],
  ],
};
const SHOULDER: [Pt, Pt] = [
  [118, 455],
  [482, 455],
];

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const lerpPt = (a: Pt, b: Pt, t: number): Pt => [
  lerp(a[0], b[0], t),
  lerp(a[1], b[1], t),
];

const Arm: React.FC<{ from: Pt; to: Pt; side: -1 | 1 }> = ({
  from,
  to,
  side,
}) => {
  // elbow pushed outward so arms read as bendy noodles
  const mid: Pt = [
    (from[0] + to[0]) / 2 + side * 45,
    (from[1] + to[1]) / 2 + 20,
  ];
  const d = `M ${from[0]} ${from[1]} Q ${mid[0]} ${mid[1]} ${to[0]} ${to[1]}`;
  return (
    <g>
      <path
        d={d}
        stroke={LINE}
        strokeWidth={46}
        fill="none"
        strokeLinecap="round"
      />
      <path
        d={d}
        stroke={BODY_DARK}
        strokeWidth={30}
        fill="none"
        strokeLinecap="round"
      />
      <circle
        cx={to[0]}
        cy={to[1]}
        r={30}
        fill={BODY}
        stroke={LINE}
        strokeWidth={8}
      />
    </g>
  );
};

const Mouth: React.FC<{ open: number; mood: Mood }> = ({ open, mood }) => {
  const cx = 300;
  const cy = 515;
  const talking = open > 0.06 || mood === "shock";
  if (talking) {
    const o = mood === "shock" ? Math.max(open, 0.45) : open;
    const h = 12 + o * 62;
    const w = mood === "shock" ? 44 + o * 10 : 66 - o * 8;
    return (
      <g>
        <ellipse
          cx={cx}
          cy={cy}
          rx={w}
          ry={h / 2}
          fill="#2A1630"
          stroke={LINE}
          strokeWidth={7}
        />
        {o > 0.3 && (
          <ellipse
            cx={cx}
            cy={cy + h / 2 - 12}
            rx={w * 0.55}
            ry={10}
            fill="#F07A8E"
          />
        )}
      </g>
    );
  }
  const frown = mood === "worried";
  const d = frown
    ? `M ${cx - 46} ${cy + 14} Q ${cx} ${cy - 22} ${cx + 46} ${cy + 14}`
    : mood === "think"
      ? `M ${cx - 34} ${cy + 4} Q ${cx + 10} ${cy + 16} ${cx + 44} ${cy - 8}`
      : `M ${cx - 54} ${cy - 8} Q ${cx} ${cy + 44} ${cx + 54} ${cy - 8}`;
  return (
    <path
      d={d}
      stroke={LINE}
      strokeWidth={10}
      fill="none"
      strokeLinecap="round"
    />
  );
};

const Brows: React.FC<{ mood: Mood; lift: number }> = ({ mood, lift }) => {
  // [inner y offset, outer y offset] relative to base
  const shape: Record<Mood, [number, number]> = {
    shock: [-34, -34],
    point: [0, -6],
    worried: [-22, 10],
    think: [-4, -4],
    excited: [-18, -18],
    wave: [-6, -10],
  };
  const [inner, outer] = shape[mood];
  const y = 290 - lift;
  const thinkRaise = mood === "think" ? -22 : 0;
  return (
    <g stroke={LINE} strokeWidth={13} strokeLinecap="round">
      <line x1={180} y1={y + outer} x2={262} y2={y + inner} />
      <line
        x1={338}
        y1={y + inner + thinkRaise}
        x2={420}
        y2={y + outer + thinkRaise}
      />
    </g>
  );
};

export const Character: React.FC<{
  mood: Mood;
  prevMood: Mood;
  sceneFrame: number; // frames since this scene started
  frame: number; // global frame
  mouth: number; // 0..1 loudness of the voice right now
}> = ({ mood, prevMood, sceneFrame, frame, mouth }) => {
  // pose blends from the previous scene's pose over 9 frames
  const blend = interpolate(sceneFrame, [0, 9], [0, 1], {
    extrapolateRight: "clamp",
  });
  const ease = 1 - Math.pow(1 - blend, 3);
  let lh = lerpPt(HANDS[prevMood][0], HANDS[mood][0], ease);
  let rh = lerpPt(HANDS[prevMood][1], HANDS[mood][1], ease);

  // little secondary motion per mood
  if (mood === "wave")
    rh = [
      rh[0] + Math.sin(frame / 3.2) * 38,
      rh[1] + Math.cos(frame / 3.2) * 10,
    ];
  if (mood === "excited") {
    lh = [lh[0], lh[1] + Math.sin(frame / 3) * 18];
    rh = [rh[0], rh[1] + Math.sin(frame / 3 + 1.4) * 18];
  }
  if (mood === "point") rh = [rh[0], rh[1] + Math.sin(frame / 7) * 8];

  // body: idle bob, hop on each new scene, shiver when worried, bounce when excited
  const hop = sceneFrame < 14 ? Math.sin((sceneFrame / 14) * Math.PI) * 46 : 0;
  const bob = Math.sin(frame / 11) * 7 + mouth * 6;
  const bounce = mood === "excited" ? Math.abs(Math.sin(frame / 5)) * 26 : 0;
  const shiver = mood === "worried" ? Math.sin(frame * 2.1) * 2.5 : 0;
  const squash = 1 + Math.sin(frame / 11) * 0.015 - (sceneFrame < 4 ? 0.05 : 0);
  const shockJump =
    mood === "shock" && sceneFrame < 20
      ? 1 + 0.06 * Math.sin((sceneFrame / 20) * Math.PI)
      : 1;

  // eyes: blink every ~3.3 s, look up toward the text when a scene starts
  const cycle = (frame + 17) % 101;
  const blink = cycle < 5 ? Math.abs(cycle - 2.5) / 2.5 : 1;
  const lookUp = interpolate(sceneFrame, [0, 6, 34, 44], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lookX = mood === "think" ? 16 : mood === "point" ? 10 * lookUp : 0;
  const lookY = mood === "think" ? -20 : -18 * lookUp + 4;
  const pupil = mood === "shock" ? 15 : 24;
  const eyeRy = 64 * blink * (mood === "shock" ? 1.12 : 1);

  const antennaSwing =
    Math.sin(frame / 9) * 6 + (sceneFrame < 14 ? Math.sin(sceneFrame) * 10 : 0);
  const glow = 0.55 + 0.45 * Math.sin(frame / 6);

  return (
    <svg
      width={600}
      height={700}
      viewBox="0 0 600 700"
      style={{ overflow: "visible" }}
    >
      {/* shadow */}
      <ellipse
        cx={300}
        cy={680}
        rx={190 - (hop + bounce) * 0.8}
        ry={22}
        fill="#000"
        opacity={0.28}
      />
      <g transform={`translate(${shiver}, ${-hop - bob - bounce})`}>
        {/* feet */}
        <ellipse
          cx={220}
          cy={655}
          rx={58}
          ry={28}
          fill={BODY_DARK}
          stroke={LINE}
          strokeWidth={9}
        />
        <ellipse
          cx={380}
          cy={655}
          rx={58}
          ry={28}
          fill={BODY_DARK}
          stroke={LINE}
          strokeWidth={9}
        />
        <g
          transform={`translate(300 650) scale(${shockJump / squash} ${squash * shockJump}) translate(-300 -650)`}
        >
          {/* antenna */}
          <g transform={`rotate(${antennaSwing} 300 222)`}>
            <path
              d="M 300 222 Q 290 175 300 132"
              stroke={LINE}
              strokeWidth={22}
              fill="none"
              strokeLinecap="round"
            />
            <path
              d="M 300 222 Q 290 175 300 132"
              stroke={BODY_DARK}
              strokeWidth={10}
              fill="none"
              strokeLinecap="round"
            />
            <circle
              cx={300}
              cy={118}
              r={44}
              fill={BULB}
              opacity={0.18 * glow}
            />
            <circle
              cx={300}
              cy={118}
              r={26}
              fill={BULB}
              stroke={LINE}
              strokeWidth={8}
            />
          </g>
          {/* body */}
          <path
            d="M 300 222 C 450 222 520 330 515 450 C 510 580 420 650 300 650 C 180 650 90 580 85 450 C 80 330 150 222 300 222 Z"
            fill={BODY}
            stroke={LINE}
            strokeWidth={10}
          />
          <ellipse
            cx={300}
            cy={560}
            rx={150}
            ry={70}
            fill="#7FE3C6"
            opacity={0.6}
          />
          <ellipse
            cx={205}
            cy={300}
            rx={40}
            ry={22}
            fill="#fff"
            opacity={0.35}
            transform="rotate(-25 205 300)"
          />
          {/* cheeks */}
          <ellipse
            cx={168}
            cy={470}
            rx={34}
            ry={20}
            fill="#FF8FA3"
            opacity={0.55}
          />
          <ellipse
            cx={432}
            cy={470}
            rx={34}
            ry={20}
            fill="#FF8FA3"
            opacity={0.55}
          />
          {/* eyes */}
          {[225, 375].map((x) => (
            <g key={x}>
              <ellipse
                cx={x}
                cy={385}
                rx={52}
                ry={Math.max(4, eyeRy)}
                fill="#fff"
                stroke={LINE}
                strokeWidth={8}
              />
              {blink > 0.35 && (
                <>
                  <circle
                    cx={x + lookX}
                    cy={392 + lookY}
                    r={pupil}
                    fill={LINE}
                  />
                  <circle
                    cx={x + lookX + 8}
                    cy={384 + lookY}
                    r={7}
                    fill="#fff"
                  />
                </>
              )}
            </g>
          ))}
          <Brows mood={mood} lift={mood === "shock" ? 8 : 0} />
          <Mouth open={mouth} mood={mood} />
        </g>
        <Arm from={SHOULDER[0]} to={lh} side={-1} />
        <Arm from={SHOULDER[1]} to={rh} side={1} />
      </g>
    </svg>
  );
};
