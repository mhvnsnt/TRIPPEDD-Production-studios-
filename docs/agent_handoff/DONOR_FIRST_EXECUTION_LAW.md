# DONOR-FIRST EXECUTION LAW

## Purpose
Do not spend production turns reinventing geometry, cutters, repair chains, rigs, or anatomical parts that already exist as proven donors or open-source tools in this repository.

## HARD RULE
**DONOR / EXISTING TOOL FIRST. HAND-ROLL LAST.**

Before writing a new geometry script, cutter, remesher, repair heuristic, rig component, oral part, facial part, or bespoke workaround, the agent MUST search the repository, agent branches, existing evidence, and the approved open-source/tool bulletin for an existing implementation that already solves the problem or supplies a known-good component.

If one exists, USE IT.

A new implementation is permitted only after the existing route has been inspected and is demonstrably insufficient for the measured failure. The receipt MUST name the rejected donor/tool and the measured reason it could not be used.

## CURRENT MARS ORAL RULE
For MARS oral reconstruction, the canonical route is:

`CANONICAL_MARS` → `GNM_ORAL_DONOR` → `build_mars_oral_bridge.py` / existing oral repair chain → `survey_oral_aperture.py` → measured lip/jaw gate → visual proof.

Do NOT hand-roll a replacement mouth cutter when the repository already contains:

- `tools/character/oral_cavity.py`
- `tools/character/build_gnm_oral_donor.py`
- `tools/character/run_mars_oral_repair.sh`
- `tools/character/survey_oral_aperture.py`
- the GNM-derived oral donor assets under `assets/donor/gnm_oral/`

`oral_cavity.py` already encodes the measured-curve, closed-solid, welding, cavity-carve and aperture-validation route. `run_mars_oral_repair.sh` already provisions the donor, builds it, bridges it into MARS, and fail-closes on the aperture/protrusion survey. Reimplementing that chain by hand is forbidden unless a measured failure proves the chain itself is insufficient.

## DONOR SEARCH ORDER
1. Search the current canonical repository.
2. Search agent branches and prior commits.
3. Search the tool bulletin and open-source registry.
4. Identify the smallest known-good component that solves the failure.
5. Execute the existing pipeline on the real asset.
6. Measure the result.
7. Only then modify or extend the existing tool.

## NO TOKEN-WASTING LOOP
A failed attempt must produce a routing decision, not another handcrafted variation of the same failed mechanism. Do not write five versions of a cutter when a donor/repair chain exists. Do not repeat manual placement when measured registration or transfer tooling exists.

## OPEN-SOURCE ESCALATION
If the repository tool fails, escalate to an existing open-source project already approved by the bulletin (Blender/Rigify, GNM, PyMeshLab/MeshLab, CGAL, Open3D, Instant Meshes, libigl, facial-animation, etc.) before inventing a new algorithm. New dependencies require provenance/license/integration notes and a promotion gate.

## PROVENANCE
GNM is an Apache-2.0 open-source source, and downstream GNM-based projects document its oral/eye components and licensing. Preserve upstream attribution and third-party notices when using or redistributing derived assets.

## EXCEPTION
Hand-built geometry is allowed only when all applicable donor/tool routes have been exhausted or when the owner explicitly authorizes a bespoke implementation. The exception receipt must state:
- what was searched;
- what existing routes were tested;
- why they failed;
- what the bespoke implementation adds;
- how it will be retired if a better donor/tool is found.

## CONTINUOUS WORK
Once a donor/tool route is found, continue through execution, measurement, validation, and evidence publication without waiting for another owner prompt. If the route fails, move to the next existing route. Do not stop merely because the first tool exposed a new defect.

**Law:** The repository is a toolbox. Use the tool before forging a new tool.
