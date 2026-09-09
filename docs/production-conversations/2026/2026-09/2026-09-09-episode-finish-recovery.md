# EP01 Episode-Finish Recovery — 2026-09-09

## Producer direction
The episode is under a time-bound six-hour finish window. Do not treat elapsed time as proof of health; identify the actual blocker and recover the smallest failed unit.

## Evidence
The latest canonical Story Runner run was `34394290662`. Its build job `102663632361` completed with failure specifically at `Build Story Runner cut`; setup, media stack, all 12 subjectivity chunks, subjectivity assembly, Bastard terminal tag, and Node dependencies succeeded. No EP01 Story Runner artifact was present.

The current `main` source now contains the comedy-discovery fallback: when transcript evidence is empty, PySceneDetect shot-boundary regions become explicitly low-confidence `MACHINE_SUGGESTED` scene evidence rather than causing an evidence-empty stop.

## Recovery action
Only the failed Story Runner build job was rerun (`102663632361`). This preserves successful upstream work and avoids a full rerender. The rerun was accepted by GitHub. The run-job listing is temporarily empty while GitHub reconciles the new attempt, so no success is claimed until a new job and artifact are observable.

## Operating law
No blind full-run reruns. Reuse verified expensive outputs, rerun the smallest failed unit, and require observable job progress plus the canonical artifact before declaring the episode finished.
