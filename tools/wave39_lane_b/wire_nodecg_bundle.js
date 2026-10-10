#!/usr/bin/env node
/*
 * Wave 39 Lane B — NodeCG broadcast-graphics bundle wiring proof.
 *
 * Runs three REAL checks against the local trippedd-lowerthird bundle using
 * NodeCG's own code (nodecg@2.2.0, MIT), plus one documented environment
 * blocker (full server boot).
 *
 * 1. Bundle-manifest validation via nodecg's own bundle-parser
 *    (out/server/bundle-parser) — the same parser the server runs at boot.
 *    NOTE: hoisted cheerio@1.2.0 dropped the CJS `.default` interop that
 *    nodecg 2.2.0's compiled parser expects (it was built against
 *    cheerio 1.0.0-rc.x). The harness shims `require('cheerio').default`
 *    before the parser loads — nodecg itself is untouched.
 * 2. Extension functional test: extension.js is executed with a mock nodecg
 *    API that records Replicant registrations and log lines — proves the
 *    extension registers the `lowerThird` Replicant with the correct default
 *    and emits its load log line.
 * 3. Graphics HTML structure check: dashboard panel + graphic files exist and
 *    contain the expected Replicant wiring.
 * 4. Full server boot attempt: EXPECTED TO FAIL in this environment —
 *    nodecg 2.2.0 pins better-sqlite3@8.7.0, which ships no Node 24 (ABI 137)
 *    prebuild and cannot compile against Node 24's V8 API (CopyablePersistent
 *    et al. removed; nodecg's engines field caps at Node 20). The boot log
 *    proves the server starts and dies exactly at the TypeORM sqlite init.
 *
 * Usage: node wire_nodecg_bundle.js
 * Writes: nodecg_proof_results.json
 */
'use strict';

const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const BUNDLE_DIR = path.join(DIR, 'nodecg_bundles', 'trippedd-lowerthird');
const NODECG_DIR = path.join(DIR, 'nodecg_server', 'node_modules', 'nodecg');
const results = { checks: [], ok: true };

function check(name, fn) {
	try {
		const detail = fn();
		results.checks.push({ name, status: 'PASS', detail });
		console.log(`PASS  ${name}${detail ? ' — ' + detail : ''}`);
	} catch (err) {
		results.checks.push({ name, status: 'FAIL', detail: String(err && err.message || err) });
		results.ok = false;
		console.log(`FAIL  ${name} — ${err && err.message || err}`);
	}
}
function expect(cond, msg) { if (!cond) throw new Error(msg); }

// --- 1. bundle-parser validation -------------------------------------------
check('nodecg bundle-parser accepts trippedd-lowerthird', () => {
	// cheerio interop shim (documented above)
	const cheerio = require(path.join(DIR, 'nodecg_server', 'node_modules', 'cheerio'));
	if (cheerio && typeof cheerio.load === 'function' && !cheerio.default) {
		cheerio.default = cheerio;
	}
	const parseBundle = require(path.join(NODECG_DIR, 'out/server/bundle-parser/index.js')).default;
	const b = parseBundle(BUNDLE_DIR);
	expect(b.name === 'trippedd-lowerthird', `unexpected bundle name ${b.name}`);
	expect(b.hasExtension === true, 'extension.js not detected');
	expect(Array.isArray(b.dashboard.panels) && b.dashboard.panels.length === 1,
		'expected exactly 1 dashboard panel');
	expect(b.dashboard.panels[0].name === 'control', 'panel name mismatch');
	expect(Array.isArray(b.graphics) && b.graphics.length === 1, 'expected exactly 1 graphic');
	expect(b.graphics[0].width === 1920 && b.graphics[0].height === 1080,
		'graphic is not 1920x1080');
	return `name=${b.name} panels=${b.dashboard.panels.length} graphics=${b.graphics.length} ext=${b.hasExtension}`;
});

// --- 2. extension functional test -------------------------------------------
check('extension.js registers lowerThird Replicant', () => {
	const logs = [];
	const replicants = {};
	const mockNodecg = {
		log: { info: (m) => logs.push(String(m)) },
		Replicant: (name, opts) => {
			const rep = {
				name,
				value: opts && opts.defaultValue,
				_listeners: [],
				on: (ev, cb) => { rep._listeners.push([ev, cb]); },
			};
			replicants[name] = rep;
			return rep;
		},
	};
	const ext = require(path.join(BUNDLE_DIR, 'extension.js'));
	ext(mockNodecg);
	expect(logs.some((l) => l.includes('trippedd-lowerthird extension loaded')),
		'load log line missing');
	expect(replicants.lowerThird, 'lowerThird Replicant not registered');
	expect(replicants.lowerThird.value.name === 'ASHES', 'default name mismatch');
	expect(replicants.lowerThird.value.title === 'TRIPPEDD STATION IDENT', 'default title mismatch');
	// simulate a dashboard push through the replicant
	replicants.lowerThird.value = { name: 'TEST', title: 'PROOF' };
	replicants.lowerThird._listeners.forEach(([ev, cb]) => ev === 'change' && cb(replicants.lowerThird.value));
	expect(logs.some((l) => l.includes('TEST')), 'change handler did not log update');
	return `log lines=${logs.length} replicants=${Object.keys(replicants).join(',')}`;
});

// --- 3. graphics/dashboard HTML structure -------------------------------------
check('dashboard panel + graphic HTML wired to replicant', () => {
	const cheerio = require(path.join(DIR, 'nodecg_server', 'node_modules', 'cheerio'));
	const panel = fs.readFileSync(path.join(BUNDLE_DIR, 'dashboard', 'panel.html'), 'utf8');
	const gfx = fs.readFileSync(path.join(BUNDLE_DIR, 'graphics', 'lowerthird.html'), 'utf8');
	const $p = cheerio.load(panel);
	expect($p('#push').length === 1, 'dashboard push button missing');
	expect(panel.includes("Replicant('lowerThird')"), 'panel does not use lowerThird replicant');
	const $g = cheerio.load(gfx);
	expect($g('#lt').length === 1 && $g('#name').length === 1 && $g('#title').length === 1,
		'graphic lower-third elements missing');
	expect(gfx.includes("Replicant('lowerThird')"), 'graphic does not use lowerThird replicant');
	return 'panel: #push + replicant write; graphic: #lt/#name/#title + replicant read';
});

// --- 4. full server boot (expected environment failure, documented) ------------
check('full server boot attempt (documents blocker)', () => {
	const { execFileSync } = require('child_process');
	let out = '';
	try {
		execFileSync('node', [path.join(NODECG_DIR, 'index.js')], {
			cwd: path.join(DIR, 'nodecg_server'),
			timeout: 45000,
			stdio: ['ignore', 'pipe', 'pipe'],
			env: { ...process.env, FORCE_COLOR: '0' },
		});
		throw new Error('server booted unexpectedly — blocker not reproduced');
	} catch (err) {
		out = String((err.stdout || '') + (err.stderr || ''));
	}
	fs.writeFileSync(path.join(DIR, 'nodecg_boot_attempt.log'), out);
	const started = out.includes('Starting NodeCG 2.2.0');
	const diedAtSqlite = out.includes('Could not locate the bindings file') &&
		out.includes('better-sqlite3');
	expect(started, 'server did not even start — different failure than expected');
	expect(diedAtSqlite, 'server failed somewhere other than the better-sqlite3 init');
	return 'server starts, then dies at TypeORM better-sqlite3 init (no Node 24 binding) — see nodecg_boot_attempt.log';
});

fs.writeFileSync(path.join(DIR, 'nodecg_proof_results.json'), JSON.stringify(results, null, 2));
console.log(`\n${results.checks.filter((c) => c.status === 'PASS').length}/${results.checks.length} checks passed`);
process.exit(results.ok ? 0 : 1);
