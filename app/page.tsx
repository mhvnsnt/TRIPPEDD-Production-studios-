const REPO = 'https://raw.githubusercontent.com/mhvnsnt/TRIPPEDD-Production-studios-';
const FACE_BRANCH = 'claude/trippedd-toolchain-provisioning-8pccfc';

const evidence = [
  ['REST', 'docs/evidence/expression/01_REST_front.png'],
  ['BLINK', 'docs/evidence/expression/02_BLINK_front.png'],
  ['BLINK LEFT ONLY', 'docs/evidence/expression/03_BLINK_L_ONLY_front.png'],
  ['SMILE', 'docs/evidence/expression/04_SMILE_front.png'],
  ['NOSTRIL FLARE', 'docs/evidence/expression/05_NOSTRIL_FLARE_front.png'],
  ['BROW UP', 'docs/evidence/expression/06_BROW_UP_front.png'],
  ['BROW DOWN', 'docs/evidence/expression/07_BROW_DOWN_front.png'],
  ['CHEEK PUFF', 'docs/evidence/expression/08_CHEEK_PUFF_front.png'],
  ['PUCKER', 'docs/evidence/expression/09_PUCKER_front.png'],
  ['JAW OPEN', 'docs/evidence/expression/10_JAW_OPEN_front.png'],
  ['SQUINT', 'docs/evidence/expression/11_SQUINT_front.png'],
  ['DISGUST', 'docs/evidence/expression/12_DISGUST_front.png'],
];

const links = [
  ['Face authority', `https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/blob/${FACE_BRANCH}/docs/character/MARS-FACE-AUTHORITY.md`],
  ['Motion proof', `https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/blob/main/tools/character/motion_proof.py`],
  ['Hair measurement', `https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/blob/main/tools/character/measure_hair.py`],
  ['MARS placement manifest', 'https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/blob/main/artifacts/evidence/god_molecule/mars_lod2_placement_plate_manifest.json'],
];

export default function Page() {
  return (
    <main>
      <header><span>TRIPPEDD / GOD MOLECULE</span><strong>PRODUCTION COCKPIT</strong></header>
      <section>
        <p className="eyebrow">EP01 / MARS / LIVE WORK SURFACE</p>
        <h1>FACE + MOTION LAB</h1>
        <p className="lead">A subscription-free control surface for the actual production repository. The production runtime stays authoritative; this Next.js surface exposes the latest measurable face, hair, motion, and evidence work without pretending a screenshot is a render PASS.</p>

        <div className="statusGrid">
          <article><b>FACE AUTHORITY</b><span>MediaPipe semantic landmarks → measured lid/brow/nose anchors</span><em>STRUCTURAL / FAIL-CLOSED</em></article>
          <article><b>EYE PLACEMENT</b><span>GNM + ICT-FaceKit donors; similarity/non-rigid fit recorded</span><em>VISUAL REVIEW REQUIRED</em></article>
          <article><b>HAIR</b><span>Trimesh lock segmentation is already in the production tree; next step is bone chains + dynamics.</span><em>MOTION NEXT</em></article>
          <article><b>MOTION</b><span>motion_proof.py renders every frame and emits a video when ffmpeg is available.</span><em>SEQUENCE GATE</em></article>
        </div>

        <div className="toolbar">
          <span>Latest facial-toolchain evidence branch: <code>{FACE_BRANCH}</code></span>
          <div>{links.map(([label, href]) => <a key={href} href={href} target="_blank" rel="noreferrer">{label}</a>)}</div>
        </div>

        <h2>Visual evidence</h2>
        <p className="note">These are the committed expression plates from the latest facial-toolchain work. They are evidence to inspect, not an automatic visual PASS.</p>
        <div className="gallery">
          {evidence.map(([label, path]) => (
            <figure key={path}>
              <img src={`${REPO}/${FACE_BRANCH}/${path}`} alt={label} loading="lazy" />
              <figcaption>{label}</figcaption>
            </figure>
          ))}
        </div>
      </section>
    </main>
  );
}
