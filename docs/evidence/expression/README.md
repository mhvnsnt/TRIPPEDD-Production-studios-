# Evidence — expression

Rendered frames and the measurements that produced them, committed so that
**every agent and every CI runner can see them**, not just the container that
made them. `renders/` stays gitignored; these are downscaled copies with the
source hash recorded, published by `tools/publish_evidence.py`.

| frame | source sha256[:8] | rendered |
|---|---|---|
| `01_REST_front.png` | `e7babdc0` | 900x900 |
| `01_REST_profile.png` | `0d619db8` | 900x900 |
| `02_BLINK_front.png` | `33f887d0` | 900x900 |
| `02_BLINK_profile.png` | `dc50ce6e` | 900x900 |
| `03_BLINK_L_ONLY_front.png` | `ed3c1f5a` | 900x900 |
| `03_BLINK_L_ONLY_profile.png` | `4b77f9c8` | 900x900 |
| `04_SMILE_front.png` | `6dcb2d9a` | 900x900 |
| `04_SMILE_profile.png` | `f95b2f78` | 900x900 |
| `05_NOSTRIL_FLARE_front.png` | `919e5f71` | 900x900 |
| `05_NOSTRIL_FLARE_profile.png` | `e992a1b0` | 900x900 |
| `06_BROW_UP_front.png` | `bf1cc149` | 900x900 |
| `06_BROW_UP_profile.png` | `c90a09fc` | 900x900 |
| `07_BROW_DOWN_front.png` | `5ed82f26` | 900x900 |
| `07_BROW_DOWN_profile.png` | `de8febc1` | 900x900 |
| `08_CHEEK_PUFF_front.png` | `9a35cf1d` | 900x900 |
| `08_CHEEK_PUFF_profile.png` | `21914886` | 900x900 |
| `09_PUCKER_front.png` | `ee450cec` | 900x900 |
| `09_PUCKER_profile.png` | `998272ce` | 900x900 |
| `10_JAW_OPEN_front.png` | `3af2bcdd` | 900x900 |
| `10_JAW_OPEN_profile.png` | `c01544e7` | 900x900 |
| `11_SQUINT_front.png` | `87b2fbbb` | 900x900 |
| `11_SQUINT_profile.png` | `f8fbe9c9` | 900x900 |
| `12_DISGUST_front.png` | `afe170b2` | 900x900 |
| `12_DISGUST_profile.png` | `ff95add4` | 900x900 |

## Measured, per pose

Rays are fired at the mouth and classified by the MATERIAL each one lands on.
Material identity cannot be fooled by a hole in the wrong place; a plane test can.

| pose | jaw | lip gap (% head height) | skin | cavity | teeth | gum | tongue |
|---|---|---|---|---|---|---|---|
| 01_REST | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 02_BLINK | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 03_BLINK_L_ONLY | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 04_SMILE | 3° | 2.61% | 93.6 | 6.0 | 0.4 | 0.0 | 0.0 |
| 05_NOSTRIL_FLARE | 0° | 0.14% | 97.6 | 1.9 | 0.0 | 0.6 | 0.0 |
| 06_BROW_UP | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 07_BROW_DOWN | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 08_CHEEK_PUFF | 0° | 0.00% | 97.4 | 2.6 | 0.0 | 0.0 | 0.0 |
| 09_PUCKER | 0° | 0.00% | 97.8 | 2.2 | 0.0 | 0.0 | 0.0 |
| 10_JAW_OPEN | 0° | 0.14% | 95.4 | 3.4 | 0.0 | 1.3 | 0.0 |
| 11_SQUINT | 0° | 0.00% | 97.7 | 2.1 | 0.1 | 0.0 | 0.1 |
| 12_DISGUST | 0° | 0.00% | 97.5 | 2.5 | 0.0 | 0.0 | 0.0 |

## Gate

| check | result | detail |
|---|---|---|
| 02_BLINK reaches the screen | PASS | pixel delta 0.03441 inside the region it moves (0.00266 over the whole frame) |
| 03_BLINK_L_ONLY reaches the screen | PASS | pixel delta 0.03432 inside the region it moves (0.00110 over the whole frame) |
| 04_SMILE reaches the screen | PASS | pixel delta 0.04392 inside the region it moves (0.02383 over the whole frame) |
| 05_NOSTRIL_FLARE reaches the screen | PASS | pixel delta 0.04361 inside the region it moves (0.02468 over the whole frame) |
| 06_BROW_UP reaches the screen | PASS | pixel delta 0.02174 inside the region it moves (0.01214 over the whole frame) |
| 07_BROW_DOWN reaches the screen | PASS | pixel delta 0.01764 inside the region it moves (0.00694 over the whole frame) |
| 08_CHEEK_PUFF reaches the screen | PASS | pixel delta 0.05026 inside the region it moves (0.01940 over the whole frame) |
| 09_PUCKER reaches the screen | PASS | pixel delta 0.04216 inside the region it moves (0.01571 over the whole frame) |
| 10_JAW_OPEN reaches the screen | PASS | pixel delta 0.05896 inside the region it moves (0.02949 over the whole frame) |
| 11_SQUINT reaches the screen | PASS | pixel delta 0.00951 inside the region it moves (0.00399 over the whole frame) |
| 12_DISGUST reaches the screen | PASS | pixel delta 0.04132 inside the region it moves (0.02499 over the whole frame) |
| blink_L closes, not opens (geometry) | PASS | blink_L travels +1.05 of the eye's own opening (occlusion 0%, which is NOT the verdict) |
| blink_R closes, not opens (geometry) | PASS | blink_R travels +1.07 of the eye's own opening (occlusion 100%, which is NOT the verdict) |
| one lid moves about half of what two lids move | PASS | one lid 0.00110 vs both 0.00266 = 41% of the two-lid change |
| the FACS jaw shape parts the lips on its own | PASS | gap 0.14% of head height vs 0.00% at rest -- skin only; the jaw BONE is what carries the lower arch, and driving it from this shape is not wired yet |
| a compound is not just its largest part | PASS | disgust vs sneer-alone differ by 0.01427 across the frame |

**Physical gate: PASS** — 16 of 16 checks pass.

**Visual gate: FAIL.** A passing physical gate is not a passing model — these exact numbers went green on a frame whose crowns still read as separate pegs. VISUAL_FAIL outranks the measurements; PENDING is not PASS.


### 01 REST front

![01_REST_front.png](01_REST_front.png)


### 01 REST profile

![01_REST_profile.png](01_REST_profile.png)


### 02 BLINK front

![02_BLINK_front.png](02_BLINK_front.png)


### 02 BLINK profile

![02_BLINK_profile.png](02_BLINK_profile.png)


### 03 BLINK L ONLY front

![03_BLINK_L_ONLY_front.png](03_BLINK_L_ONLY_front.png)


### 03 BLINK L ONLY profile

![03_BLINK_L_ONLY_profile.png](03_BLINK_L_ONLY_profile.png)


### 04 SMILE front

![04_SMILE_front.png](04_SMILE_front.png)


### 04 SMILE profile

![04_SMILE_profile.png](04_SMILE_profile.png)


### 05 NOSTRIL FLARE front

![05_NOSTRIL_FLARE_front.png](05_NOSTRIL_FLARE_front.png)


### 05 NOSTRIL FLARE profile

![05_NOSTRIL_FLARE_profile.png](05_NOSTRIL_FLARE_profile.png)


### 06 BROW UP front

![06_BROW_UP_front.png](06_BROW_UP_front.png)


### 06 BROW UP profile

![06_BROW_UP_profile.png](06_BROW_UP_profile.png)


### 07 BROW DOWN front

![07_BROW_DOWN_front.png](07_BROW_DOWN_front.png)


### 07 BROW DOWN profile

![07_BROW_DOWN_profile.png](07_BROW_DOWN_profile.png)


### 08 CHEEK PUFF front

![08_CHEEK_PUFF_front.png](08_CHEEK_PUFF_front.png)


### 08 CHEEK PUFF profile

![08_CHEEK_PUFF_profile.png](08_CHEEK_PUFF_profile.png)


### 09 PUCKER front

![09_PUCKER_front.png](09_PUCKER_front.png)


### 09 PUCKER profile

![09_PUCKER_profile.png](09_PUCKER_profile.png)


### 10 JAW OPEN front

![10_JAW_OPEN_front.png](10_JAW_OPEN_front.png)


### 10 JAW OPEN profile

![10_JAW_OPEN_profile.png](10_JAW_OPEN_profile.png)


### 11 SQUINT front

![11_SQUINT_front.png](11_SQUINT_front.png)


### 11 SQUINT profile

![11_SQUINT_profile.png](11_SQUINT_profile.png)


### 12 DISGUST front

![12_DISGUST_front.png](12_DISGUST_front.png)


### 12 DISGUST profile

![12_DISGUST_profile.png](12_DISGUST_profile.png)

