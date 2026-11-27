import { CalculateMetadataFunction, Composition, staticFile } from "remotion";
import { VideoData, WhatIf2D } from "./WhatIf2D";
import { Story3D, StoryData } from "./three/Story3D";
import { Baseball3D, BBData } from "./three/Baseball3D";

const bbMetadata: CalculateMetadataFunction<BBData | { id: string }> = async ({ props }) => {
  const data: BBData = "shots" in props ? props : await (await fetch(staticFile(`bb/${props.id}.json`))).json();
  return { durationInFrames: data.durationInFrames, props: data };
};

const storyMetadata: CalculateMetadataFunction<
  StoryData | { id: string }
> = async ({ props }) => {
  const data: StoryData =
    "shots" in props
      ? props
      : await (await fetch(staticFile(`story/${props.id}.json`))).json();
  return { durationInFrames: data.durationInFrames, props: data };
};

// Props are one public/data/<id>.json file (see prep.py). In Studio, edit `id` to preview another video.
type Props = VideoData | { id: string };

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const data: VideoData =
    "scenes" in props
      ? props
      : await (await fetch(staticFile(`data/${props.id}.json`))).json();
  return { durationInFrames: data.durationInFrames, props: data };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="WhatIf2D"
        component={WhatIf2D as unknown as React.FC<Props>}
        durationInFrames={1215}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ id: "01-moon" }}
        calculateMetadata={calculateMetadata}
      />
      <Composition
        id="Story3D"
        component={Story3D as unknown as React.FC<StoryData | { id: string }>}
        durationInFrames={1215}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ id: "02-bees" }}
        calculateMetadata={storyMetadata}
      />
      <Composition
        id="Baseball3D"
        component={Baseball3D as unknown as React.FC<BBData | { id: string }>}
        durationInFrames={1215}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ id: "01-moon" }}
        calculateMetadata={bbMetadata}
      />
    </>
  );
};
