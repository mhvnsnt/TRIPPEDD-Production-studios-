# Evidence — mouth_candidate

Rendered frames and the measurements that produced them, committed so that
**every agent and every CI runner can see them**, not just the container that
made them. `renders/` stays gitignored; these are downscaled copies with the
source hash recorded, published by `tools/publish_evidence.py`.

| frame | source sha256[:8] | rendered |
|---|---|---|
| `01_REST_front.png` | `c549dd31` | 900x900 |
| `01_REST_mouth.png` | `5f42c9aa` | 900x900 |
| `01_REST_profile.png` | `720acdfd` | 900x900 |
| `02_OPEN_front.png` | `88e0e3c9` | 900x900 |
| `02_OPEN_mouth.png` | `cd09d6bd` | 900x900 |
| `02_OPEN_profile.png` | `1ce867a9` | 900x900 |
| `03_WIDE_front.png` | `72c9def4` | 900x900 |
| `03_WIDE_mouth.png` | `ea391ff5` | 900x900 |
| `03_WIDE_profile.png` | `0d7ccc5c` | 900x900 |
| `04_AA_front.png` | `a788acf9` | 900x900 |
| `04_AA_mouth.png` | `34275951` | 900x900 |
| `04_AA_profile.png` | `bf3b9ef3` | 900x900 |
| `05_OH_front.png` | `47140923` | 900x900 |
| `05_OH_mouth.png` | `a27910be` | 900x900 |
| `05_OH_profile.png` | `dfe30e52` | 900x900 |
| `06_EE_front.png` | `06dcce04` | 900x900 |
| `06_EE_mouth.png` | `88933305` | 900x900 |
| `06_EE_profile.png` | `f94e684b` | 900x900 |
| `07_MM_front.png` | `bff31ff6` | 900x900 |
| `07_MM_mouth.png` | `1ed146ae` | 900x900 |
| `07_MM_profile.png` | `e045ebe9` | 900x900 |
| `08_FF_front.png` | `75773ec6` | 900x900 |
| `08_FF_mouth.png` | `1ae03eeb` | 900x900 |
| `08_FF_profile.png` | `ab8e4f21` | 900x900 |
| `09_BLINK_front.png` | `1ad25169` | 900x900 |
| `09_BLINK_mouth.png` | `3b600495` | 900x900 |
| `09_BLINK_profile.png` | `7249c490` | 900x900 |
| `10_SMILE_front.png` | `0049f540` | 900x900 |
| `10_SMILE_mouth.png` | `423150d2` | 900x900 |
| `10_SMILE_profile.png` | `d940e90f` | 900x900 |

## Measured, per pose

Rays are fired at the mouth and classified by the MATERIAL each one lands on.
Material identity cannot be fooled by a hole in the wrong place; a plane test can.

| pose | jaw | lip gap (% head height) | skin | cavity | teeth | gum | tongue |
|---|---|---|---|---|---|---|---|
| 01_REST | 0° | 0.00% | 99.7 | 0.1 | 0.1 | 0.0 | 0.1 |
| 02_OPEN | 18° | 10.71% | 73.3 | 9.3 | 3.5 | 1.5 | 12.3 |
| 03_WIDE | 31° | 13.32% | 60.4 | 18.1 | 6.3 | 4.0 | 11.2 |
| 04_AA | 23° | 12.36% | 67.6 | 17.1 | 5.0 | 1.9 | 8.5 |
| 05_OH | 15° | 9.89% | 80.0 | 3.4 | 3.8 | 1.3 | 11.6 |
| 06_EE | 6° | 4.26% | 90.5 | 4.2 | 0.9 | 0.1 | 4.3 |
| 07_MM | 0° | 0.00% | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 08_FF | 5° | 3.30% | 92.1 | 3.5 | 1.3 | 0.1 | 2.9 |
| 09_BLINK | 0° | 0.00% | 99.7 | 0.1 | 0.1 | 0.0 | 0.1 |
| 10_SMILE | 4° | 2.34% | 93.9 | 2.3 | 0.8 | 0.0 | 3.0 |

## Gate

| check | result | detail |
|---|---|---|
| REST reads as a closed mouth | PASS | cavity 0.1% + tongue 0.1% of the mouth area |
| REST shows at most a hint of upper teeth | PASS | teeth 0.1% |
| OPEN parts the lips | PASS | gap 10.71% of head height vs 0.00% at rest |
| WIDE shows real teeth | PASS | teeth 6.3% |
| WIDE shows the tongue | PASS | tongue 11.2% |
| WIDE shows cavity behind them | PASS | cavity 18.1% |
| OH and EE are different mouths | PASS | OH gap 0.0834 vs EE gap 0.0359 |
| MM closes the mouth | PASS | cavity 0.0% |

**Physical gate: PASS** — 8 of 8 checks pass.

**Visual gate: PENDING.** A passing physical gate is not a passing model — these exact numbers went green on a frame whose crowns still read as separate pegs. VISUAL_FAIL outranks the measurements; PENDING is not PASS.


### 01 REST front

![01_REST_front.png](01_REST_front.png)


### 01 REST mouth

![01_REST_mouth.png](01_REST_mouth.png)


### 01 REST profile

![01_REST_profile.png](01_REST_profile.png)


### 02 OPEN front

![02_OPEN_front.png](02_OPEN_front.png)


### 02 OPEN mouth

![02_OPEN_mouth.png](02_OPEN_mouth.png)


### 02 OPEN profile

![02_OPEN_profile.png](02_OPEN_profile.png)


### 03 WIDE front

![03_WIDE_front.png](03_WIDE_front.png)


### 03 WIDE mouth

![03_WIDE_mouth.png](03_WIDE_mouth.png)


### 03 WIDE profile

![03_WIDE_profile.png](03_WIDE_profile.png)


### 04 AA front

![04_AA_front.png](04_AA_front.png)


### 04 AA mouth

![04_AA_mouth.png](04_AA_mouth.png)


### 04 AA profile

![04_AA_profile.png](04_AA_profile.png)


### 05 OH front

![05_OH_front.png](05_OH_front.png)


### 05 OH mouth

![05_OH_mouth.png](05_OH_mouth.png)


### 05 OH profile

![05_OH_profile.png](05_OH_profile.png)


### 06 EE front

![06_EE_front.png](06_EE_front.png)


### 06 EE mouth

![06_EE_mouth.png](06_EE_mouth.png)


### 06 EE profile

![06_EE_profile.png](06_EE_profile.png)


### 07 MM front

![07_MM_front.png](07_MM_front.png)


### 07 MM mouth

![07_MM_mouth.png](07_MM_mouth.png)


### 07 MM profile

![07_MM_profile.png](07_MM_profile.png)


### 08 FF front

![08_FF_front.png](08_FF_front.png)


### 08 FF mouth

![08_FF_mouth.png](08_FF_mouth.png)


### 08 FF profile

![08_FF_profile.png](08_FF_profile.png)


### 09 BLINK front

![09_BLINK_front.png](09_BLINK_front.png)


### 09 BLINK mouth

![09_BLINK_mouth.png](09_BLINK_mouth.png)


### 09 BLINK profile

![09_BLINK_profile.png](09_BLINK_profile.png)


### 10 SMILE front

![10_SMILE_front.png](10_SMILE_front.png)


### 10 SMILE mouth

![10_SMILE_mouth.png](10_SMILE_mouth.png)


### 10 SMILE profile

![10_SMILE_profile.png](10_SMILE_profile.png)

