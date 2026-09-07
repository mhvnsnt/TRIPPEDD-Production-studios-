import { describe, it, expect } from 'vitest';
import os from 'os';
import path from 'path';
import { mkdtempSync, writeFileSync, readFileSync, statSync, existsSync } from 'fs';
import { deflateSync } from 'zlib';
import { ModelArtifactManager, WHISPERX_ALIGN_EN, type ModelSpec } from '../ModelArtifactManager';

/** A real, minimal zip so validation is exercised against actual bytes. */
function makeZip(): Buffer {
  const name = Buffer.from('m.bin');
  const data = Buffer.alloc(64, 7);
  const comp = deflateSync(data);
  const local = Buffer.concat([
    Buffer.from([0x50, 0x4b, 0x03, 0x04, 20, 0, 0, 0, 8, 0, 0, 0, 0, 0]),
    Buffer.alloc(4), // crc (not validated by our header/EOCD check)
    u32(comp.length), u32(data.length), u16(name.length), u16(0), name, comp,
  ]);
  const central = Buffer.concat([
    Buffer.from([0x50, 0x4b, 0x01, 0x02, 20, 0, 20, 0, 0, 0, 8, 0, 0, 0, 0, 0]),
    Buffer.alloc(4),
    u32(comp.length), u32(data.length), u16(name.length),
    Buffer.alloc(8), u16(0), Buffer.alloc(4), u32(0), name,
  ]);
  const eocd = Buffer.concat([
    Buffer.from([0x50, 0x4b, 0x05, 0x06, 0, 0, 0, 0]),
    u16(1), u16(1), u32(central.length), u32(local.length), u16(0),
  ]);
  return Buffer.concat([local, central, eocd]);
}
function u16(n: number) { const b = Buffer.alloc(2); b.writeUInt16LE(n); return b; }
function u32(n: number) { const b = Buffer.alloc(4); b.writeUInt32LE(n); return b; }

const spec = (over: Partial<ModelSpec> = {}): ModelSpec => ({
  id: 'test-model', url: 'https://example.invalid/m.pth',
  filename: 'm.pth', validate: 'zip', ...over,
});

describe('ModelArtifactManager — a partial model can never look installed', () => {
  it('rejects an archive missing its end-of-archive record', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    const full = makeZip();
    // Truncate: header intact, central directory gone. This is exactly the
    // shape the real 377MB model arrived in through the proxy.
    writeFileSync(path.join(dir, 'm.pth'), full.subarray(0, full.length - 30));

    const m = new ModelArtifactManager(dir);
    expect(await m.isValid(spec())).toBe(false);
  });

  it('accepts a complete archive', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    writeFileSync(path.join(dir, 'm.pth'), makeZip());
    const m = new ModelArtifactManager(dir);
    expect(await m.isValid(spec())).toBe(true);
  });

  it('rejects a file of the wrong length even if it parses', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    const z = makeZip();
    writeFileSync(path.join(dir, 'm.pth'), z);
    const m = new ModelArtifactManager(dir);
    expect(await m.isValid(spec({ expectedBytes: z.length + 1 }))).toBe(false);
    expect(await m.isValid(spec({ expectedBytes: z.length }))).toBe(true);
  });

  it('an existing valid model is reported AVAILABLE without re-downloading', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    const z = makeZip();
    writeFileSync(path.join(dir, 'm.pth'), z);

    const m = new ModelArtifactManager(dir);
    // The URL is unreachable on purpose: a valid cache must not hit the network.
    const rec = await m.ensure(spec(), { maxRetries: 0 });
    expect(rec.state).toBe('AVAILABLE');
    expect(rec.receivedBytes).toBe(z.length);
    expect(rec.retries).toBe(0);
  });

  it('reports MODEL_DOWNLOAD_INCOMPLETE rather than an opaque loader error', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    const m = new ModelArtifactManager(dir);
    const rec = await m.ensure(
      spec({ url: 'https://localhost:1/definitely-not-there.pth' }),
      { maxRetries: 0, timeoutMs: 3000 }
    );

    expect(rec.state).toBe('MODEL_DOWNLOAD_INCOMPLETE');
    expect(rec.error).toBeTruthy();
    expect(rec.url).toContain('definitely-not-there');
    // Nothing was published into the cache.
    expect(existsSync(path.join(dir, 'm.pth'))).toBe(false);
  }, 30_000);

  it('purges invalid artifacts and abandoned partials', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    const full = makeZip();
    writeFileSync(path.join(dir, 'm.pth'), full.subarray(0, full.length - 30)); // corrupt
    writeFileSync(path.join(dir, 'other.pth.partial'), Buffer.alloc(2048, 1));  // abandoned

    const m = new ModelArtifactManager(dir);
    const res = await m.purgeInvalid([spec()]);

    expect(res.removed).toContain('m.pth');
    expect(res.removed).toContain('other.pth.partial');
    expect(res.bytesReclaimed).toBeGreaterThan(2048);
    expect(existsSync(path.join(dir, 'm.pth'))).toBe(false);
    expect(existsSync(path.join(dir, 'other.pth.partial'))).toBe(false);
  });

  it('leaves a valid artifact alone when purging', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-'));
    writeFileSync(path.join(dir, 'm.pth'), makeZip());
    const m = new ModelArtifactManager(dir);
    const res = await m.purgeInvalid([spec()]);
    expect(res.removed).toEqual([]);
    expect(existsSync(path.join(dir, 'm.pth'))).toBe(true);
  });

  it('names the real WhisperX alignment model as a zip-validated artifact', () => {
    // The one that actually broke; it must be covered by validation.
    expect(WHISPERX_ALIGN_EN.validate).toBe('zip');
    expect(WHISPERX_ALIGN_EN.url).toMatch(/^https:\/\//);
    expect(WHISPERX_ALIGN_EN.filename).toMatch(/\.pth$/);
  });
});

describe('ModelArtifactManager — real cached model', () => {
  const real = path.join(process.cwd(), '.trippedd_tools', 'models', WHISPERX_ALIGN_EN.filename);
  const hasReal = existsSync(real);

  it.skipIf(!hasReal)('validates the actual downloaded alignment model', async () => {
    const m = new ModelArtifactManager(path.dirname(real));
    expect(await m.isValid(WHISPERX_ALIGN_EN)).toBe(true);
    expect(statSync(real).size).toBeGreaterThan(300 * 1024 * 1024);
  }, 60_000);

  it.skipIf(!hasReal)('rejects a truncated copy of the actual model', async () => {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'mam-real-'));
    const bytes = readFileSync(real);
    // 5MB short of 377MB — subtle enough that a size-only check could miss it.
    writeFileSync(path.join(dir, WHISPERX_ALIGN_EN.filename), bytes.subarray(0, bytes.length - 5_000_000));

    const m = new ModelArtifactManager(dir);
    expect(await m.isValid(WHISPERX_ALIGN_EN)).toBe(false);
    const purged = await m.purgeInvalid([WHISPERX_ALIGN_EN]);
    expect(purged.bytesReclaimed).toBeGreaterThan(100 * 1024 * 1024);
  }, 120_000);
});
