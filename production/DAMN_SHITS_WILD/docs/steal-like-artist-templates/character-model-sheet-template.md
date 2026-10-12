# CHARACTER MODEL SHEET TEMPLATE

**Show:** [Show name]
**Character:** [Character name / alias]
**Date created:** [YYYY-MM-DD]
**Version:** [v1, v2...]
**Status:** [draft / approved / locked]

> Fill this out completely before building the character's rig (mouths, eyes, hands).
> The model sheet is law — if the rig doesn't match the sheet, the rig is wrong.

---

## 1. TURNAROUND

Four views at the same scale, same pose (neutral standing):

| View | Description | File |
|------|-------------|------|
| Front | Facing camera, arms at sides | `turnaround-front.png` |
| 3/4 | Three-quarter turn, facing slightly right | `turnaround-34.png` |
| Side | Full profile, facing right | `turnaround-side.png` |
| Back | Facing away | `turnaround-back.png` |

**Proportions:**
- Height in heads: [e.g., 6.5 heads]
- Shoulder width: [relative to head]
- Notable proportions: [long arms, short legs, big head, etc.]

---

## 2. EXPRESSION SHEET

| Expression | Description | File |
|------------|-------------|------|
| Neutral | Default resting face | `expr-neutral.png` |
| Happy | | `expr-happy.png` |
| Angry | | `expr-angry.png` |
| Sad | | `expr-sad.png` |
| Surprised | | `expr-surprised.png` |
| Scared | | `expr-scared.png` |
| Smug / confident | | `expr-smug.png` |
| Disgusted | | `expr-disgusted.png` |

Add or remove rows per character. Minimum 6.

---

## 3. MOUTH CHART (Preston Blair)

| Viseme | Sounds | Description for THIS character | File |
|--------|--------|-------------------------------|------|
| Closed / Rest | silence | | `viseme-closed.png` |
| Ah | ah, eye, hat | | `viseme-ah.png` |
| Ee | egg, eat, tree | | `viseme-ee.png` |
| Oh | oh, goat, hot | | `viseme-oh.png` |
| Oo | oo, you | | `viseme-oo.png` |
| M/B/P | m, b, p | Lips pressed — non-negotiable | `viseme-mbp.png` |
| F/V | f, v | | `viseme-fv.png` |
| L | l, t, d, n, th | | `viseme-l.png` |
| Hiss | s, k, g, z | | `viseme-hiss.png` |
| W | w, q | | `viseme-w.png` |

Add character-specific bonus shapes (snarl, grin, etc.) as needed.

---

## 4. EYE EXPRESSIONS

**Eye style:** [visible eyes with pupils / shrouded glints / visor / other — describe]

| Expression | Description | File |
|------------|-------------|------|
| Neutral | | `eyes-neutral.png` |
| Blink | | `eyes-blink.png` |
| Happy | | `eyes-happy.png` |
| Angry | | `eyes-angry.png` |
| Sad | | `eyes-sad.png` |
| Surprised | | `eyes-surprised.png` |

---

## 5. HAND POSES

**Finger count:** [4 / 5 — verify from episode frames, not assumptions]
**Skin tone:** [hex, sampled from reference]

| Pose | Use for | File |
|------|---------|------|
| Open palm | Gesturing, presenting | `hand-open-palm.png` |
| Fist | Emphasis, anger | `hand-fist.png` |
| Pointing | Directing attention | `hand-pointing.png` |
| Gripping | Holding objects | `hand-gripping.png` |
| Thumbs up | Approval | `hand-thumbs-up.png` |
| Relaxed | Idle | `hand-relaxed.png` |
| Counting | Numbers, listing | `hand-counting.png` |
| Beckoning | "Come here" | `hand-beckoning.png` |
| Holding | Pinch grip for props | `hand-holding.png` |
| Shaka | Casual greeting | `hand-shaka.png` |

---

## 6. COLOR MODEL

| Area | Hex | Notes |
|------|-----|-------|
| Skin | | Never lighten from this value |
| Teeth | | |
| Grill / gold | | Note if it varies by shot |
| Primary clothing | | |
| Trim / accent | | |
| Eyes / glints | | |
| Hair | | |
| Accessories | | |

---

## 7. SCALE REFERENCE

| Compared to | Relative height | Notes |
|-------------|----------------|-------|
| [Character B] | | |
| [Character C] | | |
| Door frame | | |
| [Common prop] | | |

---

## 8. CHARACTER NOTES

Character-specific quirks that aren't obvious from drawings:

- [Design features that must be preserved]
- [Variations that are intentional, not errors]
- [Things the AI will try to "fix" that it must NOT fix]
- [Shroud/hood rules, if applicable]
- [Anything the owner has specifically flagged]

---

## 9. LIKENESS CHECKLIST

Before any asset enters the pipeline:

- [ ] Proportions match turnaround
- [ ] Skin tone matches color model (numeric check, not eyeball)
- [ ] Distinctive features present (teeth shape, scars, accessories, etc.)
- [ ] Style matches show (line weight, shading, outlines)
- [ ] No whitewashing, no color drift
- [ ] Visually verified by human eyes, not just filename

---

*Template version: 2026-10-10. Based on the Ashes rig build.*
