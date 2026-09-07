/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { StudioOpsWorkspace } from './components/StudioOpsWorkspace';
import { ActiveProduction } from './components/ActiveProduction';
import { ShowBible } from './components/ShowBible';
import { AILab } from './components/AILab';
import { ToolManager } from './components/ToolManager';
import { StoryWorkspace } from './components/StoryWorkspace';
import { JobsPipeline } from './components/JobsPipeline';
import { AssetWorkspace } from './components/AssetWorkspace';
import { FormatsWorkspace } from './components/FormatsWorkspace';
import { EpisodeWorkspace } from './components/EpisodeWorkspace';
import { DriveIngestWorkspace } from './components/DriveIngestWorkspace';
import { PeopleCastWorkspace } from './components/PeopleCastWorkspace';
import { ProductionControlWorkspace } from './components/ProductionControlWorkspace';
import { PhysicalEvidenceWorkspace } from './components/PhysicalEvidenceWorkspace';
import { EditorialReviewWorkspace } from './components/EditorialReviewWorkspace';
import { MakeTheShowWorkspace } from './components/MakeTheShowWorkspace';
import { motion, AnimatePresence } from 'motion/react';
import { Wrench } from 'lucide-react';

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard setCurrentView={setCurrentView} />;

      case 'studio_ops':
        return <StudioOpsWorkspace />;
      case 'people_cast':
        return <PeopleCastWorkspace />;
      case 'control':
        return <ProductionControlWorkspace />;

      case 'physical_evidence':
        return <PhysicalEvidenceWorkspace />;
      case 'make_show':
        return <MakeTheShowWorkspace />;
      case 'editorial_review':
        return <EditorialReviewWorkspace />;
      case 'production':
        return <ActiveProduction />;
      case 'formats':
        return <FormatsWorkspace />;
      case 'bible':
        return <ShowBible />;
      case 'ailab':
        return <AILab />;
      case 'tool_manager':
        return <ToolManager />;
      case 'episodes':
        return <EpisodeWorkspace />;
      case 'ingest':
        return <DriveIngestWorkspace />;
      case 'story':
        return <StoryWorkspace />;
      case 'jobs':
        return <JobsPipeline />;
      case 'assets':
        return <AssetWorkspace />;
      // Placeholders for un-implemented tools/views
      case 'tool_video':
      case 'tool_comfy':
      case 'tool_blender':
      case 'tool_unreal':
      case 'tool_audio':
      case 'tool_capture':
      case 'tool_2d':
      case 'settings':
        return (
          <div className="flex-1 flex flex-col items-center justify-center text-neutral-500 h-full p-8 text-center min-h-full">
            <Wrench size={48} className="mb-4 opacity-20" />
            <h2 className="text-xl font-bold text-neutral-400 mb-2 font-mono tracking-widest uppercase">Integration Not Implemented</h2>
            <p className="text-sm max-w-md">The {currentView.replace('tool_', '')} module is pending implementation in the Tool Registry.</p>
          </div>
        );
      default:
        return (
          <div className="flex-1 flex items-center justify-center text-neutral-500 font-mono text-sm min-h-full">
            Module [{currentView}] in development...
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-black text-white font-sans overflow-hidden selection:bg-blue-500/30">
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
      <main className="flex-1 overflow-y-auto bg-neutral-950/50 relative">
        {/* Subtle grid background */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none"></div>
        <div className="relative z-10 min-h-full h-full flex flex-col">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentView}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="flex-1 flex flex-col"
            >
              {renderView()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
