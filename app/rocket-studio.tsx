'use client';

import { useMemo, useState } from 'react';

type RenderPass = 'Beauty' | 'Diffuse' | 'Specular' | 'Shadow' | 'AO' | 'Depth' | 'Normal' | 'Mist';
type Engine = 'CYCLES' | 'EEVEE' | 'WORKBENCH';

type Node = { id: string; x: number; y: number; label: string; color: string };

const renderPasses: RenderPass[] = ['Beauty', 'Diffuse', 'Specular', 'Shadow', 'AO', 'Depth', 'Normal', 'Mist'];
const engines: Engine[] = ['CYCLES', 'EEVEE', 'WORKBENCH'];

const effects = [
  ['Glow', 0.55], ['Bloom', 0.35], ['Lens Flare', 0.2], ['Chromatic Aberration', 0.08],
  ['Vignette', 0.3], ['Film Grain', 0.12], ['Depth Blur', 0.18], ['Motion Blur', 0.25],
  ['Color Grade', 0.5], ['LUT', 0.4], ['Sharpen', 0.35], ['Halation', 0.15],
] as const;

const initialNodes: Node[] = [
  { id: 'render', x: 30, y: 100, label: 'Render Layer', color: '#31DFFF' },
  { id: 'balance', x: 220, y: 60, label: 'Color Balance', color: '#9b7cff' },
  { id: 'glare', x: 220, y: 180, label: 'Glare', color: '#ffb347' },
  { id: 'mix', x: 430, y: 120, label: 'Mix', color: '#5eead4' },
  { id: 'lens', x: 620, y: 70, label: 'Lens Distort', color: '#f472b6' },
  { id: 'composite', x: 810, y: 120, label: 'Composite', color: '#4000FF' },
];

function Slider({ label, value, min, max, step = 0.01, onChange }: { label: string; value: number; min: number; max: number; step?: number; onChange: (v: number) => void }) {
  return <label className="slider"><span>{label}<b>{value.toFixed(step < 0.1 ? 2 : 0)}</b></span><input type="range" min={min} max={max} step={step} value={value} onChange={e => onChange(Number(e.target.value))} /></label>;
}

function Viewport({ exposure, gamma, pass, engine }: { exposure: number; gamma: number; pass: RenderPass; engine: Engine }) {
  return <div className="viewport">
    <div className="scanline" />
    <div className="mars-orb"><div className="mars-highlight" /><div className="mars-shadow" /><div className="mars-ring" /></div>
    <div className="viewport-grid" />
    <div className="viewport-label">MARS / REAL-TIME PREVIEW SURFACE</div>
    <div className="viewport-stats">ENGINE {engine} · PASS {pass.toUpperCase()} · EXP {exposure.toFixed(2)} · GAMMA {gamma.toFixed(2)}</div>
    <div className="viewport-truth">PREVIEW VISUALIZATION · AUTHORITATIVE PIXELS: UNAVAILABLE</div>
  </div>;
}

export function RocketStudio() {
  const [workspace, setWorkspace] = useState<'render' | 'comp'>('render');
  const [pass, setPass] = useState<RenderPass>('Beauty');
  const [engine, setEngine] = useState<Engine>('EEVEE');
  const [resolution, setResolution] = useState(50);
  const [samples, setSamples] = useState(64);
  const [exposure, setExposure] = useState(0);
  const [gamma, setGamma] = useState(1);
  const [camera, setCamera] = useState('PERSP');
  const [renderState, setRenderState] = useState('IDLE');
  const [nodes, setNodes] = useState(initialNodes);
  const [selectedNode, setSelectedNode] = useState('render');
  const [selectedEffect, setSelectedEffect] = useState('Glow');
  const [effectValues, setEffectValues] = useState<Record<string, number>>(() => Object.fromEntries(effects.map(([name, value]) => [name, value])));
  const [layers, setLayers] = useState(['Final Composite', 'Lens Distort', 'Color Grade', 'Glare', 'Render Layer', 'Original Plate']);

  const selectedEffectValue = effectValues[selectedEffect] ?? 0;
  const selectedNodeData = useMemo(() => nodes.find(n => n.id === selectedNode) ?? nodes[0], [nodes, selectedNode]);

  const startFrameRender = () => {
    setRenderState('QUEUED');
    window.setTimeout(() => setRenderState('RUNNING'), 300);
    window.setTimeout(() => setRenderState('AWAITING_RENDER_WORKER'), 1600);
  };

  const moveNode = (id: string, dx: number, dy: number) => setNodes(current => current.map(node => node.id === id ? { ...node, x: Math.max(10, node.x + dx), y: Math.max(20, node.y + dy) } : node));

  return <main className="rocket-shell">
    <header className="rocket-header"><div><span>TRIPPEDD / GOD MOLECULE</span><strong>ROCKET PRODUCTION WORKSTATION</strong></div><div className="header-status"><i /> HUMAN VISUAL AUTHORITY · ACTIVE</div></header>
    <div className="workspace-tabs"><button className={workspace === 'render' ? 'active' : ''} onClick={() => setWorkspace('render')}>🎥 RT RENDER</button><button className={workspace === 'comp' ? 'active' : ''} onClick={() => setWorkspace('comp')}>✦ COMPOSITING / VFX</button></div>

    {workspace === 'render' ? <section className="workspace">
      <aside className="control-panel">
        <div className="panel-title">REAL-TIME RENDER PREVIEW</div>
        <div className="truth-card"><b>RENDER AUTHORITY</b><span>Viewport is an interactive control surface. No authoritative frame is claimed until a real render worker returns bytes + provenance.</span></div>
        <label className="field">RENDER PASS<select value={pass} onChange={e => setPass(e.target.value as RenderPass)}>{renderPasses.map(p => <option key={p}>{p}</option>)}</select></label>
        <label className="field">ENGINE<select value={engine} onChange={e => setEngine(e.target.value as Engine)}>{engines.map(e => <option key={e}>{e}</option>)}</select></label>
        <Slider label="Resolution %" value={resolution} min={10} max={100} step={10} onChange={setResolution} />
        <Slider label="Samples" value={samples} min={8} max={512} step={8} onChange={setSamples} />
        <Slider label="Exposure" value={exposure} min={-4} max={4} onChange={setExposure} />
        <Slider label="Gamma" value={gamma} min={0.5} max={2} onChange={setGamma} />
        <div className="field"><span>CAMERA</span><div className="camera-grid">{['FRONT', 'SIDE', 'TOP', 'PERSP', 'CLOSE'].map(c => <button key={c} className={camera === c ? 'selected' : ''} onClick={() => setCamera(c)}>{c}</button>)}</div></div>
        <div className="camera-advanced"><Slider label="Focal length" value={50} min={18} max={120} step={1} onChange={() => {}} /><Slider label="Aperture" value={2.8} min={0.7} max={16} step={0.1} onChange={() => {}} /></div>
        <button className="primary" onClick={startFrameRender}>RENDER FRAME → {renderState}</button>
      </aside>
      <div className="render-main"><Viewport exposure={exposure} gamma={gamma} pass={pass} engine={engine} /><div className="render-footer"><span>CAMERA {camera}</span><span>{resolution}% RES</span><span>{samples} SAMPLES</span><span>WORKER {renderState === 'AWAITING_RENDER_WORKER' ? 'UNAVAILABLE' : 'READY'}</span></div></div>
    </section> : <section className="workspace comp-workspace">
      <aside className="layer-panel"><div className="panel-title">LAYER STACK</div>{layers.map((layer, index) => <button key={layer} className={index === 0 ? 'layer active' : 'layer'} onClick={() => setLayers(current => { const copy = [...current]; [copy[index], copy[Math.max(0, index - 1)]] = [copy[Math.max(0, index - 1)], copy[index]]; return copy; })}><span>◈</span>{layer}<small>{index === 0 ? '100%' : `${Math.max(20, 90 - index * 11)}%`}</small></button>)}<div className="truth-card"><b>COMPOSITING AUTHORITY</b><span>Node/effect edits are authoring state until serialized into a real comp artifact and rendered.</span></div></aside>
      <div className="comp-main"><div className="comp-toolbar"><span>NODE GRAPH / VFX STACK</span><button onClick={() => setSelectedNode('render')}>RESET VIEW</button></div><div className="node-graph">{nodes.slice(0, -1).map(node => <div key={node.id} className="wire" style={{ left: node.x + 120, top: node.y + 25, width: Math.max(40, (nodes.find(n => n.x > node.x)?.x ?? node.x + 180) - node.x - 10), borderColor: node.color }} />)}{nodes.map(node => <button key={node.id} className={`node ${selectedNode === node.id ? 'selected' : ''}`} style={{ left: node.x, top: node.y, borderColor: node.color }} onClick={() => setSelectedNode(node.id)}><small>{node.id.toUpperCase()}</small><b>{node.label}</b></button>)}<div className="node-inspector"><b>{selectedNodeData.label}</b><span>Node parameters</span><Slider label="Mix" value={0.75} min={0} max={1} onChange={() => {}} /></div></div><div className="effects"><div className="panel-title">VFX STACK</div><div className="effect-grid">{effects.map(([name]) => <button key={name} className={selectedEffect === name ? 'effect selected' : 'effect'} onClick={() => setSelectedEffect(name)}><span>{name}</span><b>{Math.round((effectValues[name] ?? 0) * 100)}%</b></button>)}</div><div className="effect-inspector"><b>{selectedEffect}</b><Slider label="Intensity" value={selectedEffectValue} min={0} max={1} onChange={value => setEffectValues(current => ({ ...current, [selectedEffect]: value }))} /><div className="feedback">LIVE PREVIEW FEEDBACK · parameter changes are local workspace state until published.</div></div></div></div>
    </section>}
  </main>;
}
