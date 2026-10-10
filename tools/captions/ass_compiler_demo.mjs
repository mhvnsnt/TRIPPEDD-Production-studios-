// ass_compiler_demo.mjs — parse ASS -> JSON AST; compile -> render-ready data.
// (ass-compiler, MIT: https://github.com/weizhenye/ass-compiler)
//   parse(text)   -> structured JSON AST (info, styles, events)
//   compile(text) -> render-ready object (resolved styles, timed dialogues)
// npm i ass-compiler ; node ass_compiler_demo.mjs in.ass outdir
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { parse, compile } from "ass-compiler";

const [inFile, outDir] = process.argv.slice(2);
mkdirSync(outDir, { recursive: true });

const assText = readFileSync(inFile, "utf8");

const ast = parse(assText);
writeFileSync(`${outDir}/parsed.json`, JSON.stringify(ast, null, 2));

const compiled = compile(assText);
writeFileSync(`${outDir}/compiled.json`,
              JSON.stringify(compiled.dialogues, null, 2));

const names = Object.keys(compiled.styles ?? {});
console.log(`AST: ${ast.events.dialogue.length} dialogues, ` +
            `styles: ${Object.keys(ast.styles.style).join(", ")}`);
console.log(`compiled: ${compiled.dialogues.length} dialogues, ` +
            `resolved styles: ${names.join(", ")}, ` +
            `playres ${compiled.width}x${compiled.height}`);
const d0 = compiled.dialogues[0];
console.log(`cue0: start=${d0.start}ms end=${d0.end}ms ` +
            `style=${d0.style?.name ?? "?"} slices=${d0.slices?.length ?? "?"}`);
