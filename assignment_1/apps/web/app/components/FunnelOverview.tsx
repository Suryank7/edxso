'use client';

import React from 'react';
import { Users, CheckCircle2, XCircle, FileText, Send, ShieldAlert, TrendingUp } from 'lucide-react';
import { CampaignAnalytics } from '../types';

interface FunnelOverviewProps {
  analytics: CampaignAnalytics | null;
}

export const FunnelOverview: React.FC<FunnelOverviewProps> = ({ analytics }) => {
  if (!analytics) return null;

  const funnel = analytics.funnel;

  const cards = [
    {
      title: 'Discovered Creators',
      value: funnel.discovered,
      subtitle: 'Permitted public & API profiles',
      icon: Users,
      color: 'from-blue-500/20 to-blue-600/10 text-blue-400 border-blue-500/20'
    },
    {
      title: 'Qualified Creators',
      value: funnel.qualified,
      subtitle: `${analytics.qualification_rate_percent}% qualification pass rate`,
      icon: CheckCircle2,
      color: 'from-emerald-500/20 to-emerald-600/10 text-emerald-400 border-emerald-500/20'
    },
    {
      title: 'Filter Rejected',
      value: funnel.rejected,
      subtitle: 'Explainable pass/fail criteria',
      icon: XCircle,
      color: 'from-rose-500/20 to-rose-600/10 text-rose-400 border-rose-500/20'
    },
    {
      title: 'Pitches Generated',
      value: funnel.messages_generated,
      subtitle: '60-90w Email & 15-30w DM',
      icon: FileText,
      color: 'from-purple-500/20 to-purple-600/10 text-purple-400 border-purple-500/20'
    },
    {
      title: 'Outreach Simulated',
      value: funnel.outreach_simulated,
      subtitle: 'Safe dry-run execution log',
      icon: Send,
      color: 'from-amber-500/20 to-amber-600/10 text-amber-400 border-amber-500/20'
    },
    {
      title: 'Duplicates Shielded',
      value: funnel.duplicates_prevented,
      subtitle: 'Key: campaign + creator + channel',
      icon: ShieldAlert,
      color: 'from-indigo-500/20 to-indigo-600/10 text-indigo-400 border-indigo-500/20'
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className={`p-4 rounded-2xl bg-gradient-to-b ${card.color} border backdrop-blur-sm transition-all duration-200 hover:-translate-y-0.5 shadow-sm`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-slate-400">{card.title}</span>
              <Icon className="w-4 h-4 opacity-80" />
            </div>
            <div className="text-2xl font-bold tracking-tight text-white mb-1">
              {card.value}
            </div>
            <p className="text-[11px] text-slate-400/80 truncate">
              {card.subtitle}
            </p>
          </div>
        );
      })}
    </div>
  );
};
