import React, { useState } from 'react';
import { FormatRegistry } from '../core/pipeline/formats';
import { ProductionFormat, LocationRecord } from '../core/types';
import { Map, BookOpen, PenTool, LayoutTemplate, MapPin } from 'lucide-react';

export function FormatsWorkspace() {
  const formats = FormatRegistry.getAllFormats();
  const locations = FormatRegistry.getAllLocations();
  const [activeTab, setActiveTab] = useState<'FORMATS' | 'LOCATIONS'>('FORMATS');
  const [selectedItem, setSelectedItem] = useState<string | null>(formats[0]?.id || null);

  const selectedFormat = formats.find(f => f.id === selectedItem);
  const selectedLocation = locations.find(l => l.id === selectedItem);

  return (
    <div className="h-full flex flex-col">
      <header className="px-6 py-4 border-b border-neutral-800 bg-black/50 backdrop-blur-md flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-xl font-bold uppercase tracking-widest text-white flex items-center">
            <BookOpen className="mr-3 text-blue-500" size={20} />
            Formats & Lore
          </h1>
          <p className="text-neutral-400 text-sm mt-1">Manage reusable TRIPPEDD production formats and fictionalized geography.</p>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <div className="w-80 border-r border-neutral-800 bg-neutral-900/50 flex flex-col">
          <div className="flex border-b border-neutral-800">
            <button 
              className={`flex-1 py-3 text-xs font-bold tracking-wider uppercase transition-colors ${activeTab === 'FORMATS' ? 'text-white border-b-2 border-blue-500' : 'text-neutral-500 hover:text-neutral-300'}`}
              onClick={() => { setActiveTab('FORMATS'); setSelectedItem(formats[0]?.id || null); }}
            >
              Formats
            </button>
            <button 
              className={`flex-1 py-3 text-xs font-bold tracking-wider uppercase transition-colors ${activeTab === 'LOCATIONS' ? 'text-white border-b-2 border-blue-500' : 'text-neutral-500 hover:text-neutral-300'}`}
              onClick={() => { setActiveTab('LOCATIONS'); setSelectedItem(locations[0]?.id || null); }}
            >
              Locations
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {activeTab === 'FORMATS' && formats.map(format => (
              <button
                key={format.id}
                onClick={() => setSelectedItem(format.id)}
                className={`w-full text-left p-3 rounded border transition-colors ${selectedItem === format.id ? 'bg-blue-900/20 border-blue-500/50' : 'bg-neutral-800/50 border-neutral-800 hover:border-neutral-700'}`}
              >
                <div className="flex items-center text-sm font-bold text-white mb-1">
                  <LayoutTemplate size={14} className="mr-2 text-neutral-400" />
                  {format.name}
                </div>
                <div className="text-xs text-neutral-500 truncate">{format.description}</div>
              </button>
            ))}
            {activeTab === 'LOCATIONS' && locations.map(location => (
              <button
                key={location.id}
                onClick={() => setSelectedItem(location.id)}
                className={`w-full text-left p-3 rounded border transition-colors ${selectedItem === location.id ? 'bg-green-900/20 border-green-500/50' : 'bg-neutral-800/50 border-neutral-800 hover:border-neutral-700'}`}
              >
                <div className="flex items-center text-sm font-bold text-white mb-1">
                  <MapPin size={14} className="mr-2 text-neutral-400" />
                  {location.name}
                </div>
                <div className="text-xs text-neutral-500 truncate">{location.type.replace('_', ' ')}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6 overflow-y-auto bg-black">
          {activeTab === 'FORMATS' && selectedFormat && (
            <div className="max-w-3xl">
              <div className="mb-8">
                <h2 className="text-2xl font-black uppercase tracking-tight text-white mb-2">{selectedFormat.name}</h2>
                <p className="text-neutral-400">{selectedFormat.description}</p>
              </div>

              <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-8">
                <h3 className="text-sm font-bold text-neutral-500 uppercase tracking-widest mb-4">Production Guidelines</h3>
                <ul className="space-y-3">
                  {selectedFormat.guidelines.map((guideline, i) => (
                    <li key={i} className="flex items-start">
                      <span className="text-blue-500 mr-3 mt-1">•</span>
                      <span className="text-neutral-300">{guideline}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-8">
                <h3 className="text-sm font-bold text-neutral-500 uppercase tracking-widest mb-4">IP Mode</h3>
                <div className="inline-block px-3 py-1 bg-neutral-800 border border-neutral-700 text-sm font-bold text-white rounded">
                  {selectedFormat.ipMode}
                </div>
                {selectedFormat.ipMode === 'PARODY' && (
                  <p className="text-xs text-neutral-500 mt-2">
                    Must use original TRIPPEDD characters and settings. Do not directly copy existing IP characters, music, or dialogue.
                  </p>
                )}
              </div>

              <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
                <h3 className="text-sm font-bold text-neutral-500 uppercase tracking-widest mb-4">Default Provenance</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  {Object.entries(selectedFormat.defaultProvenance).map(([key, value]) => (
                    <div key={key}>
                      <div className="text-xs text-neutral-500 mb-1">{key}</div>
                      <div className="font-mono text-blue-400">
                        {Array.isArray(value) ? value.join(', ') || 'NONE' : String(value)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'LOCATIONS' && selectedLocation && (
            <div className="max-w-3xl">
              <div className="mb-8">
                <h2 className="text-2xl font-black uppercase tracking-tight text-white mb-2">{selectedLocation.name}</h2>
                <div className="inline-block px-2 py-0.5 bg-neutral-800 text-neutral-400 text-xs font-bold rounded mb-4">
                  {selectedLocation.type.replace('_', ' ')}
                </div>
                <p className="text-neutral-300">{selectedLocation.description}</p>
              </div>

              {selectedLocation.metadata && Object.entries(selectedLocation.metadata).map(([key, value]) => (
                <div key={key} className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 mb-6">
                  <h3 className="text-sm font-bold text-neutral-500 uppercase tracking-widest mb-4">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </h3>
                  <p className="text-neutral-300">{String(value)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
