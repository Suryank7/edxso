'use client';

import React from 'react';
import { Sparkles, ShieldCheck, Play, RefreshCw, Send, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  campaignName: string;
  brand: string;
  isDiscovering: boolean;
  onDiscover: () => void;
  dryRunMode: boolean;
  lastRunTime?: string | null;
}

export const Navbar: React.FC<NavbarProps> = ({
  campaignName,
  brand,
  isDiscovering,
  onDiscover,
  dryRunMode,
  lastRunTime
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & System Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25">
            <Sparkles className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-100 tracking-tight">EDXSO Influencer AI</span>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">
                InfluenceFlow
              </span>
            </div>
            <p className="text-xs text-slate-400">Automated Micro-Influencer Discovery & Outreach</p>
          </div>
        </div>

        {/* Campaign Context & Active Badges */}
        <div className="hidden md:flex items-center space-x-3">
          <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-xs text-slate-300 font-medium">{brand}</span>
            <span className="text-xs text-slate-500">•</span>
            <span className="text-xs text-slate-400">{campaignName}</span>
          </div>

          {dryRunMode && (
            <div className="px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/25 flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
              <span className="text-[11px] font-medium text-amber-300">Dry-Run Simulation Active</span>
            </div>
          )}
        </div>

        {/* Action Trigger */}
        <div className="flex items-center space-x-3">
          <button
            onClick={onDiscover}
            disabled={isDiscovering}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-md shadow-blue-600/25 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer active:scale-95"
          >
            {isDiscovering ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-white" />
                <span>Evaluating 50+ Creators...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current text-white" />
                <span>Run AI Pipeline</span>
              </>
            )}
          </button>
        </div>

      </div>
    </header>
  );
};
