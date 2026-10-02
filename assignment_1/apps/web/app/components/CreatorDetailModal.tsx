'use client';

import React from 'react';
import { X, CheckCircle2, XCircle, ExternalLink, Mail, Globe, Users, BarChart3, ShieldCheck, MapPin } from 'lucide-react';
import { EnrichedCreator } from '../types';

interface CreatorDetailModalProps {
  creator: EnrichedCreator | null;
  onClose: () => void;
  onOpenReview: (creator: EnrichedCreator) => void;
}

export const CreatorDetailModal: React.FC<CreatorDetailModalProps> = ({
  creator,
  onClose,
  onOpenReview
}) => {
  if (!creator) return null;

  const p = creator.profile;
  const isPass = creator.filter_evaluation.status === 'PASS';
  const fit = creator.brand_fit;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center font-bold text-lg text-white shadow-md shadow-blue-500/20">
              {p.name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-lg font-bold text-white">{p.name}</h2>
                <a
                  href={p.profile_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-slate-400 hover:text-blue-400 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
              <p className="text-xs text-slate-400">
                @{p.username} • {p.platform} • {p.niche}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <span
              className={`px-3 py-1 rounded-full text-xs font-bold border ${
                isPass
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
              }`}
            >
              {isPass ? 'QUALIFIED' : 'FILTER REJECTED'}
            </span>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Scrollable Content */}
        <div className="p-6 space-y-6 overflow-y-auto">
          
          {/* Quick Metrics Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 rounded-2xl bg-slate-950/70 border border-slate-800">
              <span className="text-[11px] text-slate-400 font-medium">Followers</span>
              <div className="text-lg font-bold text-white">{p.follower_count.toLocaleString()}</div>
            </div>
            <div className="p-3 rounded-2xl bg-slate-950/70 border border-slate-800">
              <span className="text-[11px] text-slate-400 font-medium">Engagement Rate</span>
              <div className={`text-lg font-bold ${p.engagement_rate >= 3.0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                {p.engagement_rate}%
              </div>
            </div>
            <div className="p-3 rounded-2xl bg-slate-950/70 border border-slate-800">
              <span className="text-[11px] text-slate-400 font-medium">Brand-Fit Score</span>
              <div className="text-lg font-bold text-blue-400">{fit.composite_score} / 100</div>
            </div>
            <div className="p-3 rounded-2xl bg-slate-950/70 border border-slate-800">
              <span className="text-[11px] text-slate-400 font-medium">Posting Frequency</span>
              <div className="text-sm font-semibold text-slate-200 mt-0.5">{p.posting_frequency}</div>
            </div>
          </div>

          {/* Qualification Pass/Fail Explainability */}
          <div className="p-4 rounded-2xl bg-slate-950/50 border border-slate-800 space-y-2.5">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-blue-400" />
              <span>Explainable Filter Evaluation</span>
            </h3>
            <div className="space-y-1.5">
              {creator.filter_evaluation.reasons.map((reason, idx) => (
                <div
                  key={idx}
                  className={`text-xs p-2 rounded-xl flex items-start space-x-2 ${
                    reason.startsWith('✓')
                      ? 'bg-emerald-500/5 text-emerald-300/90 border border-emerald-500/10'
                      : reason.startsWith('✗')
                      ? 'bg-rose-500/5 text-rose-300/90 border border-rose-500/10'
                      : 'bg-slate-800/40 text-slate-300 border border-slate-800'
                  }`}
                >
                  <span className="leading-relaxed">{reason}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Transparent Multi-Factor Brand-Fit Breakdown */}
          <div className="p-4 rounded-2xl bg-slate-950/50 border border-slate-800 space-y-3">
            <div className="flex justify-between items-center">
              <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-indigo-400" />
                <span>Multi-Factor Brand-Fit Scoring (Transparent Breakdown)</span>
              </h3>
              <span className="text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20">
                Composite: {fit.composite_score}/100
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Niche Relevance (30%)</span>
                  <span className="font-bold text-white">{fit.niche_relevance}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-500 h-full rounded-full" style={{ width: `${fit.niche_relevance}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Audience Relevance (20%)</span>
                  <span className="font-bold text-white">{fit.audience_relevance}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${fit.audience_relevance}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Engagement (20%)</span>
                  <span className="font-bold text-white">{fit.engagement_score}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${fit.engagement_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Content Relevance (15%)</span>
                  <span className="font-bold text-white">{fit.content_relevance}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-purple-500 h-full rounded-full" style={{ width: `${fit.content_relevance}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Geography (10%)</span>
                  <span className="font-bold text-white">{fit.geography_score}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full rounded-full" style={{ width: `${fit.geography_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-medium">Contact Availability (5%)</span>
                  <span className="font-bold text-white">{fit.contact_availability}/100</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-teal-500 h-full rounded-full" style={{ width: `${fit.contact_availability}%` }} />
                </div>
              </div>
            </div>
          </div>

          {/* Audience & Content Context */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Demographics */}
            <div className="p-4 rounded-2xl bg-slate-950/50 border border-slate-800 space-y-2 text-xs">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Audience Demographics
              </span>
              <div className="space-y-1 text-slate-300">
                <div><span className="text-slate-500">Age:</span> {p.audience_age}</div>
                <div><span className="text-slate-500">Gender:</span> {p.audience_gender}</div>
                <div><span className="text-slate-500">Geography:</span> {p.audience_geography}</div>
              </div>
            </div>

            {/* Contact & Verification Source */}
            <div className="p-4 rounded-2xl bg-slate-950/50 border border-slate-800 space-y-2 text-xs">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Contact & Verification Source
              </span>
              <div className="space-y-1 text-slate-300">
                <div>
                  <span className="text-slate-500">Email:</span>{' '}
                  <span className="font-mono text-blue-400">{p.contact_email}</span>
                </div>
                <div><span className="text-slate-500">Source:</span> {p.email_source}</div>
                <div>
                  <span className="text-slate-500">Confidence:</span>{' '}
                  <span className="uppercase text-[10px] font-bold px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400">
                    {p.email_confidence}
                  </span>
                </div>
              </div>
            </div>

          </div>

          {/* Recent Content */}
          <div className="p-4 rounded-2xl bg-slate-950/50 border border-slate-800 space-y-2">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Recent Content Titles
            </span>
            <ul className="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
              {p.recent_content.map((post, idx) => (
                <li key={idx} className="italic text-slate-300/90">"{post}"</li>
              ))}
            </ul>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 flex justify-between items-center bg-slate-950/60">
          <div className="text-xs text-slate-500">
            Discovery Source: <span className="text-slate-400">{p.discovery_source}</span>
          </div>

          <div className="flex space-x-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-300 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors cursor-pointer"
            >
              Close
            </button>

            {isPass && creator.personalization && (
              <button
                onClick={() => {
                  onClose();
                  onOpenReview(creator);
                }}
                className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-xl transition-colors cursor-pointer"
              >
                Review AI Pitch
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
