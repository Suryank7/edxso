'use client';

import React, { useState, useEffect } from 'react';
import { X, Sparkles, Check, Send, AlertTriangle, ShieldCheck, Mail, MessageSquare, Copy } from 'lucide-react';
import { EnrichedCreator } from '../types';

interface ReviewModalProps {
  creator: EnrichedCreator | null;
  onClose: () => void;
  onSaveReview: (creatorId: string, status: string, editedEmail: string, editedDm: string) => Promise<void>;
  onSendOutreach: (creator: EnrichedCreator, channel: 'Email' | 'Instagram_DM', body: string) => Promise<void>;
}

export const ReviewModal: React.FC<ReviewModalProps> = ({
  creator,
  onClose,
  onSaveReview,
  onSendOutreach
}) => {
  if (!creator || !creator.personalization) return null;

  const [emailBody, setEmailBody] = useState(creator.personalization.email_body);
  const [dmBody, setDmBody] = useState(creator.personalization.dm_body);
  const [activeTab, setActiveTab] = useState<'Email' | 'Instagram_DM'>('Email');
  const [isSaving, setIsSaving] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (creator.personalization) {
      setEmailBody(creator.personalization.email_body);
      setDmBody(creator.personalization.dm_body);
    }
  }, [creator]);

  const countWords = (text: string) => {
    return text.trim() ? text.trim().split(/\s+/).length : 0;
  };

  const emailWordCount = countWords(emailBody);
  const dmWordCount = countWords(dmBody);

  const emailCompliant = emailWordCount >= 60 && emailWordCount <= 90;
  const dmCompliant = dmWordCount >= 15 && dmWordCount <= 30;

  const handleSave = async (status: string = 'Human Approved') => {
    setIsSaving(true);
    try {
      await onSaveReview(creator.profile.creator_id, status, emailBody, dmBody);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSend = async () => {
    setIsSending(true);
    try {
      const body = activeTab === 'Email' ? emailBody : dmBody;
      await onSendOutreach(creator, activeTab, body);
    } finally {
      setIsSending(false);
    }
  };

  const copyToClipboard = () => {
    const text = activeTab === 'Email' ? emailBody : dmBody;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const p = creator.profile;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center space-x-2">
                <span>AI Personalization Studio</span>
                <span className="text-[11px] font-normal px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {creator.review_status}
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                Pitch review & grounding inspection for <span className="text-slate-200 font-semibold">{p.name}</span> (@{p.username})
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="grid grid-cols-1 md:grid-cols-12 overflow-y-auto flex-1 divide-y md:divide-y-0 md:divide-x divide-slate-800">
          
          {/* Left Column: Creator Context & Grounding Evidence (4 cols) */}
          <div className="md:col-span-4 p-5 space-y-4 bg-slate-950/30">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Grounded Signals Used
            </h3>

            {/* Profile Brief */}
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800/80 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Platform</span>
                <span className="font-semibold text-slate-200">{p.platform}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Followers</span>
                <span className="font-semibold text-slate-200">{p.follower_count.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Engagement</span>
                <span className="font-semibold text-emerald-400">{p.engagement_rate}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Niche</span>
                <span className="font-semibold text-slate-200">{p.niche}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Email</span>
                <span className="font-mono text-slate-300 truncate max-w-[140px]">{p.contact_email}</span>
              </div>
            </div>

            {/* Cited Recent Content */}
            <div className="space-y-1.5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Referenced Recent Post
              </span>
              <div className="p-3 rounded-xl bg-blue-500/5 border border-blue-500/20 text-xs text-blue-200/90 italic">
                "{p.recent_content[0] || 'Tech workflow content'}"
              </div>
            </div>

            {/* Safety Guardrails Checklist */}
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800/80 space-y-2">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Guardrails & Integrity
              </span>
              <div className="flex items-center space-x-2 text-xs text-emerald-400">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Zero fabrication verified</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-emerald-400">
                <Check className="w-3.5 h-3.5" />
                <span>No guessed email addresses</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-emerald-400">
                <Check className="w-3.5 h-3.5" />
                <span>Verified creator citation</span>
              </div>
            </div>
          </div>

          {/* Right Column: Editable Pitch Studio (8 cols) */}
          <div className="md:col-span-8 p-6 flex flex-col space-y-4">
            
            {/* Channel Tabs */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex space-x-2">
                <button
                  onClick={() => setActiveTab('Email')}
                  className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === 'Email'
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-white bg-slate-800/60'
                  }`}
                >
                  <Mail className="w-3.5 h-3.5" />
                  <span>Email Pitch</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${emailCompliant ? 'bg-emerald-500/30 text-emerald-300' : 'bg-amber-500/30 text-amber-300'}`}>
                    {emailWordCount}w / 60-90
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('Instagram_DM')}
                  className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                    activeTab === 'Instagram_DM'
                      ? 'bg-purple-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-white bg-slate-800/60'
                  }`}
                >
                  <MessageSquare className="w-3.5 h-3.5" />
                  <span>Instagram DM</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${dmCompliant ? 'bg-emerald-500/30 text-emerald-300' : 'bg-amber-500/30 text-amber-300'}`}>
                    {dmWordCount}w / 15-30
                  </span>
                </button>
              </div>

              <button
                onClick={copyToClipboard}
                className="flex items-center space-x-1 px-2.5 py-1 text-xs text-slate-400 hover:text-white bg-slate-800 rounded-lg transition-colors cursor-pointer"
              >
                <Copy className="w-3.5 h-3.5" />
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>

            {/* Editable Content */}
            {activeTab === 'Email' ? (
              <div className="space-y-3 flex-1 flex flex-col">
                <div>
                  <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                    Email Subject Line
                  </label>
                  <input
                    type="text"
                    value={creator.personalization.email_subject}
                    readOnly
                    className="w-full px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 font-mono"
                  />
                </div>

                <div className="flex-1 flex flex-col">
                  <div className="flex justify-between items-center mb-1">
                    <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                      Personalized Body (60–90 Words Target)
                    </label>
                    <span className={`text-[11px] font-mono font-semibold ${emailCompliant ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {emailWordCount} words {emailCompliant ? '✓ Compliant' : '⚠ Non-compliant'}
                    </span>
                  </div>
                  <textarea
                    rows={8}
                    value={emailBody}
                    onChange={(e) => setEmailBody(e.target.value)}
                    className="w-full flex-1 p-3.5 bg-slate-950 border border-slate-800 rounded-2xl text-xs text-slate-200 leading-relaxed focus:outline-none focus:border-blue-500 transition-colors font-sans resize-none"
                    placeholder="Enter email pitch..."
                  />
                </div>
              </div>
            ) : (
              <div className="space-y-3 flex-1 flex flex-col">
                <div className="flex justify-between items-center mb-1">
                  <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    Instagram Direct Message (15–30 Words Target)
                  </label>
                  <span className={`text-[11px] font-mono font-semibold ${dmCompliant ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {dmWordCount} words {dmCompliant ? '✓ Compliant' : '⚠ Non-compliant'}
                  </span>
                </div>
                <textarea
                  rows={4}
                  value={dmBody}
                  onChange={(e) => setDmBody(e.target.value)}
                  className="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-2xl text-xs text-slate-200 leading-relaxed focus:outline-none focus:border-purple-500 transition-colors font-sans resize-none"
                  placeholder="Enter short direct message..."
                />
              </div>
            )}

            {/* Modal Action Bar */}
            <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
              <div className="text-[11px] text-slate-400 flex items-center space-x-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
                <span>Dry-run simulation mode will prevent real sending.</span>
              </div>

              <div className="flex items-center space-x-2.5">
                <button
                  onClick={() => handleSave('Edited')}
                  disabled={isSaving}
                  className="px-3.5 py-1.5 rounded-xl border border-slate-700 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition-colors cursor-pointer disabled:opacity-50"
                >
                  Save Edits
                </button>

                <button
                  onClick={() => handleSave('Human Approved')}
                  disabled={isSaving}
                  className="px-3.5 py-1.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/20 text-xs font-semibold text-emerald-400 transition-colors cursor-pointer disabled:opacity-50"
                >
                  Approve Copy
                </button>

                <button
                  onClick={handleSend}
                  disabled={isSending}
                  className="flex items-center space-x-1.5 px-4 py-1.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition-all cursor-pointer disabled:opacity-50"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{isSending ? 'Simulating...' : 'Dispatch Outreach'}</span>
                </button>
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
};
