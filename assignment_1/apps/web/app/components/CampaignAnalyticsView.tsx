'use client';

import React from 'react';
import { CampaignAnalytics } from '../types';
import { BarChart3, PieChart, TrendingUp, Layers, CheckCircle2, ShieldCheck, Mail } from 'lucide-react';

interface CampaignAnalyticsViewProps {
  analytics: CampaignAnalytics | null;
}

export const CampaignAnalyticsView: React.FC<CampaignAnalyticsViewProps> = ({ analytics }) => {
  if (!analytics) return null;

  const funnel = analytics.funnel;
  const tiers = analytics.brand_fit_distribution;
  const platforms = analytics.platform_breakdown;

  const totalTier = (tiers.elite + tiers.high + tiers.moderate + tiers.low) || 1;
  const totalPlatforms = (platforms.Instagram + platforms.YouTube) || 1;

  return (
    <div className="space-y-6">
      {/* Top Banner KPI Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <span>Average Qualified Engagement</span>
          </div>
          <div className="text-2xl font-bold text-white">{analytics.average_qualified_engagement}%</div>
          <p className="text-[11px] text-slate-500 mt-1">Exceeds the 3.0% campaign baseline</p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <CheckCircle2 className="w-4 h-4 text-blue-400" />
            <span>Qualification Pass Rate</span>
          </div>
          <div className="text-2xl font-bold text-white">{analytics.qualification_rate_percent}%</div>
          <p className="text-[11px] text-slate-500 mt-1">{funnel.qualified} out of {funnel.discovered} creators</p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            <span>Duplicate Prevention Efficacy</span>
          </div>
          <div className="text-2xl font-bold text-white">100%</div>
          <p className="text-[11px] text-slate-500 mt-1">{funnel.duplicates_prevented} duplicate pitches blocked</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Brand-Fit Score Distribution */}
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              <span>Brand-Fit Score Distribution (0 - 100)</span>
            </h3>
            <span className="text-[11px] text-slate-500">{analytics.active_creators_count} Profiles</span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-emerald-400 font-semibold">Elite Fit (85 - 100)</span>
                <span className="text-slate-300">{tiers.elite} ({Math.round((tiers.elite / totalTier) * 100)}%)</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${(tiers.elite / totalTier) * 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-blue-400 font-semibold">High Fit (70 - 84)</span>
                <span className="text-slate-300">{tiers.high} ({Math.round((tiers.high / totalTier) * 100)}%)</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                <div className="bg-blue-500 h-full rounded-full" style={{ width: `${(tiers.high / totalTier) * 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-amber-400 font-semibold">Moderate Fit (50 - 69)</span>
                <span className="text-slate-300">{tiers.moderate} ({Math.round((tiers.moderate / totalTier) * 100)}%)</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full rounded-full" style={{ width: `${(tiers.moderate / totalTier) * 100}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-rose-400 font-semibold">Low Alignment (&lt; 50)</span>
                <span className="text-slate-300">{tiers.low} ({Math.round((tiers.low / totalTier) * 100)}%)</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                <div className="bg-rose-500 h-full rounded-full" style={{ width: `${(tiers.low / totalTier) * 100}%` }} />
              </div>
            </div>
          </div>
        </div>

        {/* Discovery Funnel & Channel Breakdown */}
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
              <PieChart className="w-4 h-4 text-purple-400" />
              <span>Platform & Channel Ingestion Split</span>
            </h3>
            <span className="text-[11px] text-slate-500">{funnel.discovered} Creators</span>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="flex-1 p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-pink-500" />
                  <span className="text-xs font-semibold text-slate-200">Instagram</span>
                </div>
                <div className="text-xl font-bold text-white">{platforms.Instagram}</div>
                <div className="text-[11px] text-slate-500">{Math.round((platforms.Instagram / totalPlatforms) * 100)}% of dataset</div>
              </div>

              <div className="flex-1 p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
                  <span className="text-xs font-semibold text-slate-200">YouTube</span>
                </div>
                <div className="text-xl font-bold text-white">{platforms.YouTube}</div>
                <div className="text-[11px] text-slate-500">{Math.round((platforms.YouTube / totalPlatforms) * 100)}% of dataset</div>
              </div>
            </div>

            {/* Stage Conversion Bars */}
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2 text-xs">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Funnel Progression
              </span>
              <div className="flex items-center justify-between text-slate-300">
                <span>1. Discovered</span>
                <span className="font-bold text-white">{funnel.discovered}</span>
              </div>
              <div className="flex items-center justify-between text-slate-300">
                <span>2. Qualified (PASS)</span>
                <span className="font-bold text-emerald-400">{funnel.qualified}</span>
              </div>
              <div className="flex items-center justify-between text-slate-300">
                <span>3. Pitches Grounded</span>
                <span className="font-bold text-purple-400">{funnel.messages_generated}</span>
              </div>
              <div className="flex items-center justify-between text-slate-300">
                <span>4. Outreach Dispatched</span>
                <span className="font-bold text-amber-400">{funnel.outreach_simulated}</span>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
