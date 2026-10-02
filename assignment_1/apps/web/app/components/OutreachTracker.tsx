'use client';

import React, { useState } from 'react';
import { OutreachRecord } from '../types';
import { Send, ShieldCheck, Mail, MessageSquare, AlertCircle, Clock, RefreshCw, CheckCircle2 } from 'lucide-react';

interface OutreachTrackerProps {
  records: OutreachRecord[];
  onRefresh: () => void;
  onTestDuplicate: () => void;
  isTestingDuplicate?: boolean;
}

export const OutreachTracker: React.FC<OutreachTrackerProps> = ({
  records,
  onRefresh,
  onTestDuplicate,
  isTestingDuplicate
}) => {
  const [filterChannel, setFilterChannel] = useState<'ALL' | 'Email' | 'Instagram_DM'>('ALL');

  const filtered = records.filter(r => {
    return filterChannel === 'ALL' || r.channel === filterChannel;
  });

  return (
    <div className="space-y-4">
      {/* Tracker Toolbar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <Send className="w-4 h-4 text-blue-400" />
            <span>Outreach Activity & Delivery Tracker</span>
          </h3>
          <p className="text-xs text-slate-400">
            Immutable audit logs of all simulated and transmitted collaboration pitches
          </p>
        </div>

        <div className="flex items-center space-x-2.5">
          {/* Test Duplicate Shield Button */}
          <button
            onClick={onTestDuplicate}
            disabled={isTestingDuplicate}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-300 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 transition-all cursor-pointer disabled:opacity-50"
            title="Demonstrate Duplicate Outreach Prevention Shield"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
            <span>Test Duplicate Shield</span>
          </button>

          <button
            onClick={onRefresh}
            className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors cursor-pointer"
            title="Refresh logs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tracker Table */}
      <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/40 backdrop-blur-md">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800/80 bg-slate-950/60 text-slate-400 font-medium">
              <th className="py-3 px-4">Outreach ID</th>
              <th className="py-3 px-4">Influencer</th>
              <th className="py-3 px-4">Channel & Recipient</th>
              <th className="py-3 px-4">Dispatch Status</th>
              <th className="py-3 px-4">Sent At / Timestamp</th>
              <th className="py-3 px-4">Execution Notes</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/40">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-12 text-center text-slate-500">
                  No outreach records logged yet. Dispatch pitches from the Creator Pipeline to populate logs.
                </td>
              </tr>
            ) : (
              filtered.map((record) => {
                const isSimulated = record.status === 'SIMULATED';
                const isSent = record.status === 'SENT';
                const isFailed = record.status === 'FAILED';

                return (
                  <tr key={record.outreach_id} className="hover:bg-slate-800/20 transition-colors">
                    {/* Outreach ID */}
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-400">
                      {record.outreach_id}
                    </td>

                    {/* Influencer Name */}
                    <td className="py-3 px-4 font-semibold text-slate-200">
                      {record.creator_name}
                    </td>

                    {/* Channel & Recipient */}
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-1.5">
                        {record.channel === 'Email' ? (
                          <Mail className="w-3.5 h-3.5 text-blue-400" />
                        ) : (
                          <MessageSquare className="w-3.5 h-3.5 text-purple-400" />
                        )}
                        <span className="font-mono text-[11px] text-slate-300">
                          {record.recipient}
                        </span>
                      </div>
                    </td>

                    {/* Status Badge */}
                    <td className="py-3 px-4">
                      <span
                        className={`inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                          isSimulated
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                            : isSent
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                            : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        }`}
                      >
                        {isSimulated ? (
                          <ShieldCheck className="w-3 h-3 text-amber-400" />
                        ) : isSent ? (
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                        ) : (
                          <AlertCircle className="w-3 h-3 text-rose-400" />
                        )}
                        <span>{record.status}</span>
                      </span>
                    </td>

                    {/* Timestamp */}
                    <td className="py-3 px-4 text-slate-400 text-[11px]">
                      {record.sent_at ? new Date(record.sent_at).toLocaleTimeString() : 'N/A'}
                    </td>

                    {/* Notes */}
                    <td className="py-3 px-4 text-slate-400 text-[11px] max-w-xs truncate">
                      {record.notes || (record.error ? `Error: ${record.error}` : 'Delivered cleanly')}
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
