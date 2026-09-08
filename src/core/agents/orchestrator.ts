/**
 * TRIPPEDD autonomous studio kernel.
 *
 * This is deliberately model/tool agnostic: agents propose work, the kernel
 * enforces permissions/dependencies, and adapters perform the actual work.
 * The showrunner remains the final authority for editorial/greenlight actions.
 */

export type StudioAgentRole =
  | 'SHOWRUNNER'
  | 'STORY_EDITOR'
  | 'MEDIA_ANALYST'
  | 'COMEDY_EDITOR'
  | 'DIRECTOR'
  | 'SCRIPT_SUPERVISOR'
  | 'ANIMATION_DIRECTOR'
  | 'VFX_ARTIST'
  | 'ASSET_MANAGER'
  | 'POST_SUPERVISOR'
  | 'QC_EDITOR'
  | 'PRODUCTION_MANAGER';

export type StudioCapability =
  | 'READ_SOURCE'
  | 'ANALYZE_MEDIA'
  | 'DISCOVER_GAGS'
  | 'DRAFT_STORY'
  | 'DRAFT_SCRIPT'
  | 'PLAN_SHOTS'
  | 'CREATE_ASSET'
  | 'EDIT_ASSEMBLY'
  | 'RUN_TOOL'
  | 'RUN_QC'
  | 'PUBLISH_INTERNAL'
  | 'GREENLIGHT_EPISODE';

export type AutonomyLevel = 'SUGGEST' | 'EXECUTE' | 'EXECUTE_UNTIL_REVIEW' | 'FINAL_AUTHORITY';

export interface AgentDefinition {
  id: string;
  name: string;
  role: StudioAgentRole;
  capabilities: StudioCapability[];
  autonomy: AutonomyLevel;
  systemPurpose: string;
}

export type ProductionWorkKind =
  | 'INGEST'
  | 'MEDIA_ANALYSIS'
  | 'EVIDENCE_REVIEW'
  | 'GAG_DISCOVERY'
  | 'STORY_DEVELOPMENT'
  | 'SEGMENT_ASSEMBLY'
  | 'ASSET_GENERATION'
  | 'EDITORIAL_ASSEMBLY'
  | 'QC'
  | 'DELIVERY';

export interface ProductionWorkItem {
  id: string;
  kind: ProductionWorkKind;
  title: string;
  description: string;
  dependencies: string[];
  requiredCapabilities: StudioCapability[];
  ownerAgentId?: string;
  status: 'BLOCKED' | 'READY' | 'RUNNING' | 'REVIEW' | 'DONE' | 'FAILED';
  requiresHumanApproval: boolean;
  sourceRefs: string[];
  outputRefs: string[];
  createdAt: string;
  updatedAt: string;
}

export interface AutonomyDecision {
  allowed: boolean;
  reason: string;
  requiresHumanApproval: boolean;
}

const HUMAN_GATES = new Set<ProductionWorkKind>(['DELIVERY']);
const CAPABILITY_BY_KIND: Record<ProductionWorkKind, StudioCapability[]> = {
  INGEST: ['READ_SOURCE'],
  MEDIA_ANALYSIS: ['READ_SOURCE', 'ANALYZE_MEDIA'],
  EVIDENCE_REVIEW: ['READ_SOURCE'],
  GAG_DISCOVERY: ['DISCOVER_GAGS'],
  STORY_DEVELOPMENT: ['DRAFT_STORY'],
  SEGMENT_ASSEMBLY: ['EDIT_ASSEMBLY'],
  ASSET_GENERATION: ['CREATE_ASSET', 'RUN_TOOL'],
  EDITORIAL_ASSEMBLY: ['EDIT_ASSEMBLY'],
  QC: ['RUN_QC'],
  DELIVERY: ['PUBLISH_INTERNAL'],
};

export const DEFAULT_STUDIO_AGENTS: AgentDefinition[] = [
  { id: 'media-analyst', name: 'Media Analyst', role: 'MEDIA_ANALYST', capabilities: ['READ_SOURCE', 'ANALYZE_MEDIA'], autonomy: 'EXECUTE', systemPurpose: 'Turn raw media into technical, transcript, visual, audio, and physical evidence without rewriting source truth.' },
  { id: 'comedy-editor', name: 'Comedy Editor', role: 'COMEDY_EDITOR', capabilities: ['READ_SOURCE', 'DISCOVER_GAGS'], autonomy: 'EXECUTE_UNTIL_REVIEW', systemPurpose: 'Find escalation, reactions, awkwardness, callbacks, visual jokes, and accidental comedy.' },
  { id: 'story-editor', name: 'Story Editor', role: 'STORY_EDITOR', capabilities: ['READ_SOURCE', 'DRAFT_STORY', 'DRAFT_SCRIPT'], autonomy: 'EXECUTE_UNTIL_REVIEW', systemPurpose: 'Turn evidence and ideas into segment candidates while preserving the show grammar.' },
  { id: 'director', name: 'Director', role: 'DIRECTOR', capabilities: ['PLAN_SHOTS', 'CREATE_ASSET', 'RUN_TOOL'], autonomy: 'EXECUTE_UNTIL_REVIEW', systemPurpose: 'Translate approved editorial intent into shots, staging, animation, VFX, and tool work.' },
  { id: 'asset-manager', name: 'Asset Manager', role: 'ASSET_MANAGER', capabilities: ['READ_SOURCE', 'CREATE_ASSET', 'RUN_TOOL'], autonomy: 'EXECUTE', systemPurpose: 'Create, version, validate, and connect production assets to the graph.' },
  { id: 'post-supervisor', name: 'Post Supervisor', role: 'POST_SUPERVISOR', capabilities: ['EDIT_ASSEMBLY', 'RUN_TOOL'], autonomy: 'EXECUTE_UNTIL_REVIEW', systemPurpose: 'Build reversible editorial assemblies and keep every cut traceable to source evidence.' },
  { id: 'qc-editor', name: 'QC Editor', role: 'QC_EDITOR', capabilities: ['READ_SOURCE', 'RUN_QC'], autonomy: 'EXECUTE', systemPurpose: 'Continuously detect missing media, broken provenance, technical failures, continuity problems, and delivery risks.' },
  { id: 'production-manager', name: 'Production Manager', role: 'PRODUCTION_MANAGER', capabilities: ['READ_SOURCE', 'RUN_QC', 'PUBLISH_INTERNAL'], autonomy: 'EXECUTE', systemPurpose: 'Keep the autonomous queue moving, surface blockers, and optimize the one-person studio workload.' },
  { id: 'showrunner', name: 'Showrunner', role: 'SHOWRUNNER', capabilities: ['READ_SOURCE', 'DRAFT_STORY', 'DRAFT_SCRIPT', 'EDIT_ASSEMBLY', 'GREENLIGHT_EPISODE'], autonomy: 'FINAL_AUTHORITY', systemPurpose: 'Represent the owner's creative authority and make final editorial/greenlight decisions.' },
];

export class AutonomousStudioOrchestrator {
  private readonly agents = new Map<string, AgentDefinition>();
  private readonly work = new Map<string, ProductionWorkItem>();

  constructor(agentDefinitions: AgentDefinition[] = DEFAULT_STUDIO_AGENTS) {
    for (const agent of agentDefinitions) this.agents.set(agent.id, agent);
  }

  registerAgent(agent: AgentDefinition): void {
    this.agents.set(agent.id, agent);
  }

  getAgents(): AgentDefinition[] {
    return [...this.agents.values()];
  }

  addWork(input: Omit<ProductionWorkItem, 'id' | 'status' | 'createdAt' | 'updatedAt'>): ProductionWorkItem {
    const now = new Date().toISOString();
    const item: ProductionWorkItem = {
      ...input,
      id: `work_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      status: input.dependencies.length ? 'BLOCKED' : 'READY',
      createdAt: now,
      updatedAt: now,
    };
    this.work.set(item.id, item);
    return item;
  }

  getWork(): ProductionWorkItem[] {
    return [...this.work.values()];
  }

  getReadyWork(): ProductionWorkItem[] {
    return this.getWork().filter(item => item.status === 'READY');
  }

  assignableAgents(item: ProductionWorkItem): AgentDefinition[] {
    return this.getAgents().filter(agent =>
      item.requiredCapabilities.every(capability => agent.capabilities.includes(capability)),
    );
  }

  decide(agentId: string, itemId: string): AutonomyDecision {
    const agent = this.agents.get(agentId);
    const item = this.work.get(itemId);
    if (!agent || !item) return { allowed: false, reason: 'Unknown agent or work item.', requiresHumanApproval: true };
    if (!this.assignableAgents(item).some(candidate => candidate.id === agent.id)) {
      return { allowed: false, reason: 'Agent lacks the required production capabilities.', requiresHumanApproval: true };
    }
    const requiredByKind = CAPABILITY_BY_KIND[item.kind];
    if (!requiredByKind.every(capability => agent.capabilities.includes(capability))) {
      return { allowed: false, reason: 'Work kind requires capabilities this agent does not possess.', requiresHumanApproval: true };
    }
    const gated = item.requiresHumanApproval || HUMAN_GATES.has(item.kind) || item.requiredCapabilities.includes('GREENLIGHT_EPISODE');
    const approval = gated || agent.autonomy === 'SUGGEST' || agent.autonomy === 'EXECUTE_UNTIL_REVIEW';
    return {
      allowed: !gated || agent.autonomy !== 'SUGGEST',
      reason: gated ? 'Execution is permitted only up to the human review gate.' : 'Autonomous execution permitted.',
      requiresHumanApproval: approval,
    };
  }

  start(itemId: string, agentId: string): AutonomyDecision {
    const decision = this.decide(agentId, itemId);
    const item = this.work.get(itemId);
    if (!item || !decision.allowed) return decision;
    item.ownerAgentId = agentId;
    item.status = decision.requiresHumanApproval ? 'REVIEW' : 'RUNNING';
    item.updatedAt = new Date().toISOString();
    return decision;
  }

  complete(itemId: string, outputRefs: string[] = []): void {
    const item = this.work.get(itemId);
    if (!item) throw new Error(`Unknown work item: ${itemId}`);
    item.outputRefs = [...item.outputRefs, ...outputRefs];
    item.status = 'DONE';
    item.updatedAt = new Date().toISOString();
    this.refreshDependencies();
  }

  fail(itemId: string): void {
    const item = this.work.get(itemId);
    if (!item) throw new Error(`Unknown work item: ${itemId}`);
    item.status = 'FAILED';
    item.updatedAt = new Date().toISOString();
  }

  private refreshDependencies(): void {
    for (const item of this.work.values()) {
      if (item.status !== 'BLOCKED') continue;
      const dependenciesDone = item.dependencies.every(id => this.work.get(id)?.status === 'DONE');
      if (dependenciesDone) {
        item.status = 'READY';
        item.updatedAt = new Date().toISOString();
      }
    }
  }
}
