/**
 * TRIPPEDD visual storytelling law: the audience can enter a character's
 * subjective reality without requiring the character to acknowledge it.
 *
 * This is a production rule, not a one-off EP01 effect. Generated/animated/3D
 * material is justified when it communicates subjective experience or an
 * editorial joke that cannot be represented faithfully by the source camera.
 */

export type VisualRealityMode =
  | 'LIVE_ACTION'
  | 'VISUAL_DISTORTION'
  | 'ANIMATION'
  | 'THREE_D'
  | 'BLENDER_CG'
  | 'IMPOSSIBLE_WORLD'
  | 'LIVE_ACTION_RETURN';

export interface SubjectivityTransition {
  id: string;
  from: VisualRealityMode;
  to: VisualRealityMode;
  trigger: string;
  audiencePurpose: string;
  characterAcknowledges: boolean;
  sourceTruthRequired: boolean;
  generatedMaterialAllowed: boolean;
}

export interface SubjectivitySequencePlan {
  id: string;
  name: string;
  rule: string;
  modes: VisualRealityMode[];
  transitions: SubjectivityTransition[];
  characterAcknowledges: boolean;
  returnToReality: string;
  comedyPrinciple: string;
}

export const REALITY_SUBJECTIVITY_RULE =
  'When a character becomes altered, production language may change with the character\'s subjective experience. The audience may see an enormous impossible reality while the character remains mundane, dismissive, or unaware. The mismatch is the joke.';

export const SUBJECTIVITY_MODES: VisualRealityMode[] = [
  'LIVE_ACTION',
  'VISUAL_DISTORTION',
  'ANIMATION',
  'THREE_D',
  'BLENDER_CG',
  'IMPOSSIBLE_WORLD',
  'LIVE_ACTION_RETURN',
];

export function createSubjectivitySequence(input: {
  id: string;
  name: string;
  trigger: string;
  characterAcknowledges?: boolean;
}): SubjectivitySequencePlan {
  const characterAcknowledges = input.characterAcknowledges ?? false;
  const modes = SUBJECTIVITY_MODES;
  const transitions: SubjectivityTransition[] = modes.slice(0, -1).map((from, index) => {
    const to = modes[index + 1];
    return {
      id: `${input.id}-${from.toLowerCase()}-to-${to.toLowerCase()}`,
      from,
      to,
      trigger: input.trigger,
      audiencePurpose:
        to === 'LIVE_ACTION_RETURN'
          ? 'Make the return to mundane reality feel intentionally anticlimactic.'
          : 'Escalate access to the character\'s subjective experience without replacing source truth.',
      characterAcknowledges,
      sourceTruthRequired: from === 'LIVE_ACTION' || to === 'LIVE_ACTION_RETURN',
      generatedMaterialAllowed: from !== 'LIVE_ACTION_RETURN' && to !== 'LIVE_ACTION',
    };
  });

  return {
    id: input.id,
    name: input.name,
    rule: REALITY_SUBJECTIVITY_RULE,
    modes,
    transitions,
    characterAcknowledges,
    returnToReality: 'Return to live action without requiring the character to validate what the audience just saw.',
    comedyPrinciple: 'The spectacle can be enormous; the character response can be completely ordinary.',
  };
}

export const EP01_LOST_ACID_SUBJECTIVITY = createSubjectivitySequence({
  id: 'ep01-lost-acid-subjectivity',
  name: 'The Shumafied Experience',
  trigger: 'The character believes the shroomified attempt finally kicked in.',
  characterAcknowledges: false,
});
