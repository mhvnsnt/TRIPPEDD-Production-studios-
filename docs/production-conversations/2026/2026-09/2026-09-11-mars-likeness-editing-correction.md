# 2026-09-11 — Mars likeness-preserving image-editing correction

## Status

**SHOWRUNNER LOCK / PRODUCTION RECORD**

This record belongs to **TRIPPEDD Production Studios**. It is not a God Mode OS record and must not be written into the God Mode OS repository.

## Showrunner instruction

The user explicitly corrected the image-production workflow:

> Unless I explicitly ask for a completely new character image, do not generate a new character image or a different likeness. Use the image I shared and perform edits on that image, like Photoshop-style editing.

The supplied photograph/image is the identity authority. The task is an **edit of the supplied image**, not a text-to-image reinterpretation of the person.

## Non-negotiable likeness rules

- Preserve the user's exact identity and likeness.
- Preserve the supplied image's exact viewing angle/orientation.
- Preserve facial structure, proportions, beard, dreadlocks/loc arrangement, silhouette, pose, and visible head/neck geometry.
- Do not reconstruct or redesign the face.
- Do not beautify, reinterpret, stylize into a different person, or substitute a generated character.
- Do not invent facial features that are hidden or absent in the source.
- Do not change the direction the head is facing.
- Do not use an earlier incorrectly generated Mars image as the identity source.
- If the result changes likeness, it is **INVALID** and must not become a canonical asset.
- A completely new character image is permitted only when the user explicitly requests one.

## Correct operation

**SOURCE IMAGE → preserve identity/geometry → deterministic or Photoshop-style edit/composite/grade → inspect → compare → iterate**

Not:

**SOURCE IMAGE → describe person to image model → regenerate a new Mars character**

The user's requested workflow is the former.

## Mars treatment layers to preserve

The desired upgrades are treatment changes applied to the supplied source, including where appropriate:

- saturated cobalt/electric-blue treatment
- cyan/blue rim light
- indigo/violet/magenta information in darker hair areas
- richer colorful diffraction/sparkle stars
- black/near-black space background treatment where it is part of the approved composition
- solid glowing white eyes only where consistent with the source/angle and explicitly intended
- consistent forehead sigil only when the source geometry actually permits it
- crunchy/painterly facial and hair detail
- retro-digital / early-CD-ROM character treatment

These are **treatment layers**, not permission to regenerate the person.

## Tonnō dependency

The approved Mars treatment previously established that the Tonnō pass is a key creative stage and must not be silently removed.

Canonical Tonnō sequence:

1. center 4:3 crop
2. nearest-neighbor shrink to 640×480
3. 256-color median-cut quantization
4. Floyd–Steinberg dithering

The Tonnō stage should remain available when reproducing/upgrading the approved look.

## What went wrong in this conversation

The user supplied a specific Mars photograph and asked for the missing treatment upgrades without altering likeness.

An image-generation attempt was incorrectly made as a new portrait rather than an edit of the supplied image. The returned generation metadata showed:

- `edit_op: null`
- `parent_gen_id: null`

The generated result also changed the viewing presentation and likeness rather than preserving the supplied photograph.

The user rejected that result and clarified that the supplied photograph—not the generated replacement—is the source of truth.

The subsequent image-generation attempt errored, so no successful corrected edit was produced in that attempt.

## Source-image handling

The last supplied photograph in this conversation is the authoritative source for the pending edit. It is a right-facing/profile Mars treatment image with the user's real photographed head/neck and dreadlocks.

For the next edit attempt:

- use that exact uploaded image as the edit target;
- do not substitute the prior generated portrait;
- do not generate a new person;
- preserve the exact angle;
- apply only the requested treatment upgrades;
- work **one angle at a time**;
- stop after one angle and wait for the user's approval before moving to the next angle.

The user identified three additional/source angles for sequential treatment: **left angle, right angle, and back-of-head angle**. Do not batch-generate all three.

## Approved reference / quality target

The highest-quality approved Mars treatment remains the visual target for **lighting, color, star treatment, saturation, and texture**, while the supplied photograph remains the identity target.

The important distinction is:

**approved image = treatment reference**

**supplied photograph = likeness/geometry source**

Never reverse those roles.

## Production-agent behavior rule

Before any image-generation call, the agent must classify the requested operation:

- **EDIT** — supplied image exists and user asks to preserve/edit it → edit the supplied image.
- **NEW CHARACTER** — user explicitly asks for a completely new character image → generation is allowed.
- **AMBIGUOUS** — do not assume NEW CHARACTER; preserve the supplied source and clarify if necessary.

The agent must not silently convert EDIT into NEW CHARACTER.

## Conversation continuity

This record is a reconstructed production record of the decisions and corrections from the 2026-09-11 conversation. It is not claimed to be a verbatim transcript.

The governing production principle is:

> **Likeness outranks style. The supplied image is the identity authority.**

