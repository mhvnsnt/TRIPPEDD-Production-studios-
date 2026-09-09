#!/usr/bin/env node

/**
 * Validate Co-Producer scene JSON without requiring a rendering application.
 * Usage: bun run show/co-producer/tools/validate-scene-data.ts <scene.json>
 */

import { readFileSync } from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("Usage: validate-scene-data.ts <scene.json>");
  process.exit(2);
}

const scene = JSON.parse(readFileSync(file, "utf8"));
const errors: string[] = [];
const required = ["schema_version", "show", "episode", "production", "assets", "shots", "presets", "validation"];
for (const key of required) if (!(key in scene)) errors.push(`Missing top-level field: ${key}`);

if (!Array.isArray(scene.shots) || scene.shots.length === 0) {
  errors.push("shots must be a non-empty array");
} else {
  let previousEnd = -Infinity;
  const ids = new Set<string>();
  for (const shot of scene.shots) {
    if (ids.has(shot.id)) errors.push(`Duplicate shot id: ${shot.id}`);
    ids.add(shot.id);
    if (!(Number.isFinite(shot.start) && Number.isFinite(shot.end) && shot.end > shot.start)) {
      errors.push(`Invalid timing: ${shot.id}`);
    }
    if (shot.start < previousEnd) errors.push(`Overlapping/out-of-order shot: ${shot.id}`);
    previousEnd = shot.end;
  }

  const maxCharacters = scene.validation?.max_characters_per_shot;
  if (Number.isFinite(maxCharacters)) {
    for (const shot of scene.shots) {
      if (!Array.isArray(shot.characters) || shot.characters.length > maxCharacters) {
        errors.push(`${shot.id} exceeds character budget`);
      }
    }
  }
}

const declaredCharacters = new Set(Object.keys(scene.assets?.characters ?? {}));
const characterIds = Array.isArray(scene.assets?.characters)
  ? new Set(scene.assets.characters)
  : declaredCharacters;
const declaredCameras = new Set(scene.presets?.camera ?? []);

for (const shot of scene.shots ?? []) {
  for (const character of shot.characters ?? []) {
    if (!characterIds.has(character)) errors.push(`${shot.id} references unknown character: ${character}`);
  }
  if (!declaredCameras.has(shot.camera)) errors.push(`${shot.id} references unknown camera preset: ${shot.camera}`);
}

if (scene.episode?.target_duration_seconds != null && Array.isArray(scene.shots) && scene.shots.length) {
  const finalEnd = scene.shots[scene.shots.length - 1].end;
  if (finalEnd > scene.episode.target_duration_seconds) {
    errors.push(`Scene runs ${finalEnd}s, beyond target ${scene.episode.target_duration_seconds}s`);
  }
}

if (errors.length) {
  console.error(`Scene validation failed (${errors.length} error${errors.length === 1 ? "" : "s"}):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Scene validation passed: ${scene.show} / ${scene.episode?.id} (${scene.shots.length} shots)`);
