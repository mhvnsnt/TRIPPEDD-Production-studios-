#!/usr/bin/env node
/* osmd_render.cjs — render a MusicXML score (from the OpenScore Lieder pull)
 * to SVG via OpenSheetMusicDisplay, headless under jsdom.
 * Usage: node osmd_render.cjs <score.musicxml> <out.svg>
 */
const fs = require("fs");
const { JSDOM } = require("jsdom");

const [xmlPath, outPath] = process.argv.slice(2);
if (!xmlPath || !outPath) {
    console.error("usage: node osmd_render.cjs <score.musicxml> <out.svg>");
    process.exit(2);
}

// OSMD needs a DOM *before* it is required (same lesson as Lane A's VexFlow).
const dom = new JSDOM(`<!DOCTYPE html><html><body><div id="osmd"></div></body></html>`);
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;
global.HTMLElement = dom.window.HTMLElement;
global.Element = dom.window.Element;
global.Node = dom.window.Node;
global.SVGElement = dom.window.SVGElement;
global.getComputedStyle = dom.window.getComputedStyle.bind(dom.window);
global.XMLSerializer = dom.window.XMLSerializer;
global.DOMParser = dom.window.DOMParser;

const { OpenSheetMusicDisplay } = require("opensheetmusicdisplay");

(async () => {
    const xml = fs.readFileSync(xmlPath, "utf8");
    const container = document.getElementById("osmd");
    // jsdom has no layout engine: stub the geometry OSMD reads for autoResize.
    container.style.width = "1200px";
    Object.defineProperty(container, "clientWidth", { get: () => 1200 });
    Object.defineProperty(container, "offsetWidth", { get: () => 1200 });
    container.getBoundingClientRect = () => ({
        width: 1200, height: 800, top: 0, left: 0, right: 1200, bottom: 800,
        x: 0, y: 0, toJSON: () => ({}),
    });
    const osmd = new OpenSheetMusicDisplay(container, {
        autoResize: false,
        pageFormat: "A4_P", // headless: fixed page, no layout engine
    });
    await osmd.load(xml);
    osmd.render();
    const svg = container.innerHTML;
    fs.writeFileSync(outPath, svg);
    const staves = (svg.match(/<g[^>]*class="[^"]*vf-stave[^"]*"/g) || []).length;
    const notes = (svg.match(/class="[^"]*vf-stavenote[^"]*"/g) || []).length;
    console.log(JSON.stringify({
        input: xmlPath, output: outPath,
        svg_bytes: svg.length,
        stavenote_groups: notes,
        stave_groups: staves,
    }));
})().catch((e) => { console.error("OSMD render failed:", e.message); process.exit(1); });
