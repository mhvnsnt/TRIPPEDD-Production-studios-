/**
 * The creator's remembered material, as story-planning input ONLY.
 *
 * Everything in here is HUMAN_DIRECTION: it is what the creator said they shot
 * or wanted, not a claim that footage exists. Each beat carries cues used to go
 * looking for it in real evidence. A beat that finds nothing stays NOT_FOUND —
 * it never becomes an editorial event, and the motel clerk never gets invented.
 */
import type { StoryBeat } from './types';

function beat(
  id: string, thread: string, title: string, description: string,
  mentionStrength: StoryBeat['mentionStrength'],
  cues: StoryBeat['cues']
): StoryBeat {
  return { id, thread, title, description, mentionStrength, cues, evidenceClass: 'HUMAN_DIRECTION' };
}

/**
 * Seeded from the creator's own description of the Walk material. Strength is
 * recorded as given: beats described in passing are PARTIAL and must not be
 * treated as firmly as the ones named outright.
 */
export const WALK_STORY_BEATS: StoryBeat[] = [
  beat('walk.motel_chilling', 'WALK', 'Motel chilling',
    'Hanging out at the motel before the walk begins.', 'EXPLICIT',
    { dialogue: ['motel', 'room', 'chill', 'chilling'], entities: ['motel'] }),

  beat('walk.motel_clerk', 'WALK', 'Motel clerk',
    'Interaction with the motel clerk. Mentioned only in passing — the extent of any recorded material is unknown.',
    'PARTIAL',
    { dialogue: ['clerk', 'front desk', 'check in', 'checkout', 'room key', 'office'],
      onScreenText: ['office', 'motel', 'vacancy'], entities: ['clerk'] }),

  beat('walk.shumafied_pack', 'WALK', 'Shumafied pack/device bit',
    'The bit involving the Shumafied pack/device.', 'EXPLICIT',
    { dialogue: ['shumafied', 'shuma', 'pack', 'device'], entities: ['shumafied'] }),

  beat('walk.cigar_walk', 'WALK', 'Walking for cigars',
    'Walking out to get cigars.', 'EXPLICIT',
    { dialogue: ['cigar', 'cigars', 'store', 'walk', 'swisher', 'black'], entities: ['cigars'] }),

  beat('walk.bag_interruption', 'WALK', 'Bag-related interruption',
    'The walk is interrupted by something involving the bag.', 'EXPLICIT',
    { dialogue: ['bag', 'my bag', 'give it back', 'took my'], entities: ['bag'] }),

  beat('walk.cigar_trip', 'WALK', 'Cigar trip',
    'The trip itself to get the cigars.', 'EXPLICIT',
    { dialogue: ['cigar', 'store', 'gas station', 'corner store'], entities: ['cigars'] }),

  beat('walk.joe_encounter', 'WALK', 'Joe encounter',
    'Encountering Joe during the walk.', 'EXPLICIT',
    { dialogue: ['joe', 'hey joe', "what's your name"], entities: ['joe'] }),

  beat('walk.bag_return_argument', 'WALK', 'Recorded bag-return interaction/argument',
    'The recorded interaction/argument about returning the bag.', 'EXPLICIT',
    { dialogue: ['bag', 'give it back', 'my bag', 'argue', 'arguing', 'give me'], entities: ['bag'] }),

  beat('walk.phone_number_exchange', 'WALK', 'Phone-number exchange',
    'Exchanging phone numbers.', 'EXPLICIT',
    { dialogue: ['number', 'phone', 'text me', 'call me', 'digits'], entities: ['phone'] }),

  beat('walk.smoking_hanging', 'WALK', 'Smoking / hanging out',
    'Smoking and hanging out.', 'EXPLICIT',
    { dialogue: ['smoke', 'smoking', 'light', 'lighter', 'hit this'], entities: ['smoking'] }),

  beat('walk.tyneshia_drinking', 'WALK', 'Tyneshia drinking',
    'Tyneshia drinking.', 'EXPLICIT',
    { dialogue: ['tyneshia', 'drink', 'drinking', 'bottle', 'cup'], entities: ['tyneshia'] }),

  beat('walk.mini_scenes', 'WALK', 'Other recorded mini-scenes / arguments',
    'Assorted other recorded mini-scenes and arguments. Not individually specified.',
    'PARTIAL', { dialogue: ['argue', 'arguing', 'shut up', 'stop it'] }),
];

export const JOE_STORY_BEATS: StoryBeat[] = [
  beat('joe.prayer', 'JOE', 'Prayer',
    'Joe praying.', 'EXPLICIT',
    { dialogue: ['pray', 'prayer', 'lord', 'god', 'amen', 'bless'], entities: ['joe'] }),

  beat('joe.tic_tacs', 'JOE', 'Tic Tacs',
    'The Tic Tacs bit.', 'EXPLICIT',
    { dialogue: ['tic tac', 'tic tacs', 'mint', 'mints'], entities: ['joe'] }),

  beat('joe.names_intros', 'JOE', 'Names / intros',
    'Names and introductions.', 'EXPLICIT',
    { dialogue: ['my name', "what's your name", 'nice to meet', "i'm joe", 'call me'], entities: ['joe'] }),

  beat('joe.disappearing', 'JOE', 'Disappearing / reappearing behaviour',
    'Joe disappearing and reappearing.', 'EXPLICIT',
    { dialogue: ['where did he go', "he's gone", 'he came back', 'where you been'], entities: ['joe'] }),

  beat('joe.bag_waiting', 'JOE', 'Later bag-related waiting/arrival context',
    'The later context of waiting for/arriving with the bag.', 'PARTIAL',
    { dialogue: ['waiting', 'wait here', "he's coming", 'bag'], entities: ['joe', 'bag'] }),
];

export const DEFAULT_STORY_INVENTORY: StoryBeat[] = [...WALK_STORY_BEATS, ...JOE_STORY_BEATS];

export function beatsByThread(beats: StoryBeat[] = DEFAULT_STORY_INVENTORY): Record<string, StoryBeat[]> {
  const out: Record<string, StoryBeat[]> = {};
  for (const b of beats) (out[b.thread] ??= []).push(b);
  return out;
}
