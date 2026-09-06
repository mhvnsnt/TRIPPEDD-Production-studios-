/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { ActiveProduction } from './components/ActiveProduction';
import { ShowBible } from './components/ShowBible';
import { AILab } from './components/AILab';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard setCurrentView={setCurrentView} />;
      case 'production':
        return <ActiveProduction />;
      case 'bible':
        return <ShowBible />;
      case 'ailab':
        return <AILab />;
      default:
        return (
          <div className="flex-1 flex items-center justify-center text-neutral-500 font-mono text-sm h-full">
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
        <div className="relative z-10 min-h-full">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentView}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              {renderView()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

