import { Asset, ContentProvenance, AssetStatus } from '../types';

class AssetRegistryManager {
  private assets: Map<string, Asset> = new Map();
  private listeners: ((assets: Asset[]) => void)[] = [];

  constructor() {
    // Seed with an initial real file for demonstration purposes
    this.registerAsset({
      id: 'ast_leprechaun_v001',
      name: 'luck_leprechaun_v001',
      type: 'image',
      fileFormat: 'png',
      path: '/assets/luck_leprechaun_v001.png',
      projectId: 'prj_luck_01',
      episodeId: 'ep_01',
      sceneId: 'sc_04_irish',
      provenance: { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: 'FICTIONAL_CREATION' },
      verificationState: 'UNVERIFIED',
      contentType: 'concept_art',
      sourceTool: 'comfyui',
      version: 1,
      status: 'AVAILABLE'
    });
  }

  registerAsset(params: Omit<Asset, 'createdAt' | 'id'> & { id?: string }): Asset {
    const newAsset: Asset = {
      ...params,
      id: params.id || '',
      createdAt: new Date().toISOString()
    };
    
    // Auto-versioning: if an asset with this name exists, find the highest version
    const existingVersions = this.getAssets().filter(a => a.name.replace(/_v\d+$/, '') === params.name.replace(/_v\d+$/, ''));
    if (existingVersions.length > 0 && !params.id) { // Only auto-version if id isn't strictly provided (meaning it's new)
       const highestVersion = Math.max(...existingVersions.map(a => a.version));
       newAsset.version = highestVersion + 1;
       newAsset.id = `ast_${newAsset.name}_v${newAsset.version.toString().padStart(3, '0')}`;
       newAsset.name = `${newAsset.name.replace(/_v\d+$/, '')}_v${newAsset.version.toString().padStart(3, '0')}`;
       
       // Lineage
       const parent = existingVersions.find(a => a.version === highestVersion);
       if (parent) {
         newAsset.parentAssets = [parent.id];
         parent.derivedAssets = [...(parent.derivedAssets || []), newAsset.id];
       }
    } else if (!params.id) {
       newAsset.id = `ast_${Date.now()}`;
    }

    this.assets.set(newAsset.id, newAsset);
    this.notify();
    return newAsset;
  }

  getAsset(id: string): Asset | undefined {
    return this.assets.get(id);
  }

  getAssets(): Asset[] {
    return Array.from(this.assets.values()).sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  updateAsset(id: string, updates: Partial<Asset>) {
    const asset = this.assets.get(id);
    if (asset) {
      this.assets.set(id, { ...asset, ...updates });
      this.notify();
    }
  }

  subscribe(callback: (assets: Asset[]) => void) {
    this.listeners.push(callback);
    callback(this.getAssets()); // Initial call
    return () => {
      this.listeners = this.listeners.filter(l => l !== callback);
    };
  }

  private notify() {
    const currentAssets = this.getAssets();
    this.listeners.forEach(l => l(currentAssets));
  }
}

export const AssetRegistry = new AssetRegistryManager();
