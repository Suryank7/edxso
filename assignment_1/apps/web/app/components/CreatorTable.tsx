'use client';

import React, { useState } from 'react';
import { Search, Filter, CheckCircle2, XCircle, ExternalLink, Mail, Eye, Sparkles, Send, ShieldCheck, ChevronRight } from 'lucide-react';
import { EnrichedCreator } from '../types';

interface CreatorTableProps {
  creators: EnrichedCreator[];
  onOpenReview: (creator: EnrichedCreator) => void;
  onOpenDetail: (creator: EnrichedCreator) => void;
  onSendOutreach: (creator: EnrichedCreator) => void;
}

export const CreatorTable: React.FC<CreatorTableProps> = ({
  creators,
  onOpenReview,
  onOpenDetail,
  onSendOutreach
}) => {
  const [search, setSearch] = useState('');
  const [platformFilter, setPlatformFilter] = useState<'ALL' | 'Instagram' | 'YouTube'>('ALL');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'PASS' | 'FAIL'>('ALL');

  // Filter logic
  const filtered = creators.filter(c => {
    const q = search.toLowerCase();
    const matchesSearch =
      c.profile.name.toLowerCase().includes(q) ||
      c.profile.username.toLowerCase().includes(q) ||
      c.profile.niche.toLowerCase().includes(q) ||
      c.profile.recent_content.some(rc => rc.toLowerCase().includes(q));

    const matchesPlatform = platformFilter === 'ALL' || c.profile.platform === platformFilter;
    const matchesStatus = statusFilter === 'ALL' || c.filter_evaluation.status === statusFilter;

    return matchesSearch && matchesPlatform && matchesStatus;
  });

  const getBrandFitBadge = (score: number) => {
    if (score >= 85) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (score >= 70) return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
    if (score >= 50) return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
  };

  return (
    <div className="space-y-4">
      {/* Search and Filters Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-slate-900/60 p-3.5 rounded-2xl border border-slate-800 backdrop-blur-sm">
        
        {/* Search Input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by name, handle, topic, post..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-950/70 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-2.5 w-full sm:w-auto">
          {/* Platform Toggle */}
          <div className="flex bg-slate-950/70 p-1 rounded-xl border border-slate-800">
            {(['ALL', 'Instagram', 'YouTube'] as const).map(p => (
              <button
                key={p}
                onClick={() => setPlatformFilter(p)}
                className={`px-3 py-1 text-xs font-medium rounded-lg transition-all cursor-pointer ${
                  platformFilter === p
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {p}
              </button>
            ))}
          </div>

          {/* Status Toggle */}
          <div className="flex bg-slate-950/70 p-1 rounded-xl border border-slate-800">
            {(['ALL', 'PASS', 'FAIL'] as const).map(s => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`px-3 py-1 text-xs font-medium rounded-lg transition-all cursor-pointer ${
                  statusFilter === s
                    ? s === 'PASS' ? 'bg-emerald-600 text-white' : s === 'FAIL' ? 'bg-rose-600 text-white' : 'bg-slate-700 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {s === 'PASS' ? 'Qualified' : s === 'FAIL' ? 'Rejected' : 'All Status'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table Container */}
      <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/40 backdrop-blur-md">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800/80 bg-slate-950/60 text-slate-400 font-medium">
              <th className="py-3 px-4">Creator</th>
              <th className="py-3 px-4">Followers & Eng.</th>
              <th className="py-3 px-4">Niche & Platform</th>
              <th className="py-3 px-4">Brand Fit</th>
              <th className="py-3 px-4">Qualification</th>
              <th className="py-3 px-4">Public Email</th>
              <th className="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/40">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-500">
                  No creators found matching current search and filter criteria.
                </td>
              </tr>
            ) : (
              filtered.map((creator) => {
                const p = creator.profile;
                const isPass = creator.filter_evaluation.status === 'PASS';
                const hasPersonalization = !!creator.personalization;

                return (
                  <tr
                    key={p.creator_id}
                    className="hover:bg-slate-800/30 transition-colors group"
                  >
                    {/* Creator Identity */}
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-slate-700 to-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-slate-200">
                          {p.name.charAt(0)}
                        </div>
                        <div>
                          <div className="font-semibold text-slate-100 flex items-center space-x-1.5">
                            <span>{p.name}</span>
                            <a
                              href={p.profile_url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-slate-500 hover:text-blue-400 transition-colors"
                            >
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                          <div className="text-[11px] text-slate-400">@{p.username}</div>
                        </div>
                      </div>
                    </td>

                    {/* Followers & Engagement */}
                    <td className="py-3.5 px-4">
                      <div className="font-medium text-slate-200">
                        {p.follower_count.toLocaleString()}
                      </div>
                      <div className="flex items-center space-x-1 text-[11px]">
                        <span className={`font-semibold ${p.engagement_rate >= 3.0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {p.engagement_rate}%
                        </span>
                        <span className="text-slate-500">eng.</span>
                      </div>
                    </td>

                    {/* Niche & Platform */}
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 font-medium text-[11px] border border-slate-700/60 inline-block mb-1">
                        {p.niche}
                      </span>
                      <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                        <span className={`w-1.5 h-1.5 rounded-full ${p.platform === 'YouTube' ? 'bg-red-500' : 'bg-pink-500'}`} />
                        <span>{p.platform}</span>
                      </div>
                    </td>

                    {/* Brand Fit Score */}
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-2">
                        <div className={`px-2 py-0.5 rounded-md font-bold text-xs border ${getBrandFitBadge(creator.brand_fit.composite_score)}`}>
                          {creator.brand_fit.composite_score}
                        </div>
                        <div className="w-16 h-1.5 rounded-full bg-slate-800 overflow-hidden hidden sm:block">
                          <div
                            className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500"
                            style={{ width: `${creator.brand_fit.composite_score}%` }}
                          />
                        </div>
                      </div>
                    </td>

                    {/* Qualification Status */}
                    <td className="py-3.5 px-4">
                      <button
                        onClick={() => onOpenDetail(creator)}
                        className={`inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-[11px] font-semibold border transition-all cursor-pointer ${
                          isPass
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/25 hover:bg-emerald-500/20'
                            : 'bg-rose-500/10 text-rose-400 border-rose-500/25 hover:bg-rose-500/20'
                        }`}
                        title="Click to see explainable evaluation reasons"
                      >
                        {isPass ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3 text-rose-400" />}
                        <span>{isPass ? 'QUALIFIED' : 'REJECTED'}</span>
                      </button>
                    </td>

                    {/* Public Contact Email */}
                    <td className="py-3.5 px-4">
                      {p.contact_email !== 'Not Found' ? (
                        <div className="flex items-center space-x-1.5">
                          <Mail className="w-3 h-3 text-blue-400" />
                          <span className="text-slate-300 font-mono text-[11px] truncate max-w-[130px]">
                            {p.contact_email}
                          </span>
                        </div>
                      ) : (
                        <span className="text-slate-500 italic text-[11px]">Not Found (DM only)</span>
                      )}
                    </td>

                    {/* Actions */}
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end space-x-1.5">
                        {isPass && hasPersonalization && (
                          <button
                            onClick={() => onOpenReview(creator)}
                            className="px-2.5 py-1 rounded-lg bg-blue-600/15 border border-blue-500/30 text-blue-400 hover:bg-blue-600 hover:text-white transition-all text-[11px] font-medium flex items-center space-x-1 cursor-pointer"
                            title="Human-in-the-loop review and personalization copy edit"
                          >
                            <Sparkles className="w-3 h-3" />
                            <span>Pitch</span>
                          </button>
                        )}

                        <button
                          onClick={() => onOpenDetail(creator)}
                          className="p-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition-colors cursor-pointer"
                          title="Inspect profile & Brand Fit breakdown"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>

                        {isPass && (
                          <button
                            onClick={() => onSendOutreach(creator)}
                            disabled={creator.outreach_status === 'Sent' || creator.outreach_status === 'Simulated'}
                            className={`p-1 rounded-lg transition-colors cursor-pointer ${
                              creator.outreach_status === 'Simulated' || creator.outreach_status === 'Sent'
                                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 opacity-80 cursor-default'
                                : 'bg-slate-800/80 hover:bg-indigo-600 text-slate-300 hover:text-white'
                            }`}
                            title={
                              creator.outreach_status === 'Simulated'
                                ? 'Outreach already simulated'
                                : 'Dispatch outreach pitch'
                            }
                          >
                            {creator.outreach_status === 'Simulated' ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            ) : (
                              <Send className="w-3.5 h-3.5" />
                            )}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
