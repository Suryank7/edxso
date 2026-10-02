'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { FunnelOverview } from './components/FunnelOverview';
import { CreatorTable } from './components/CreatorTable';
import { ReviewModal } from './components/ReviewModal';
import { CreatorDetailModal } from './components/CreatorDetailModal';
import { OutreachTracker } from './components/OutreachTracker';
import { CampaignAnalyticsView } from './components/CampaignAnalyticsView';
import { EnrichedCreator, CampaignAnalytics, OutreachRecord, Campaign } from './types';
import { Layers, Send, BarChart3, Clock, Sparkles, CheckCircle2, AlertCircle, ShieldAlert } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_GATEWAY_URL || 'http://localhost:5000';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'creators' | 'analytics' | 'tracker'>('creators');
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [creators, setCreators] = useState<EnrichedCreator[]>([]);
  const [analytics, setAnalytics] = useState<CampaignAnalytics | null>(null);
  const [outreachRecords, setOutreachRecords] = useState<OutreachRecord[]>([]);
  
  const [selectedCreator, setSelectedCreator] = useState<EnrichedCreator | null>(null);
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  const [isDiscovering, setIsDiscovering] = useState(false);
  const [isTestingDuplicate, setIsTestingDuplicate] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'warning' | 'info' } | null>(null);

  const showToast = (message: string, type: 'success' | 'warning' | 'info' = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  // 1. Initial Load: Fetch Default Campaign, Creators, Analytics, and Outreach Logs
  const loadData = async () => {
    try {
      // Fetch default campaign
      const campRes = await fetch(`${API_BASE}/api/v1/campaigns/camp_default_001`);
      if (campRes.ok) {
        const campData: Campaign = await campRes.json();
        setCampaign(campData);
        if (campData.enriched_creators && campData.enriched_creators.length > 0) {
          setCreators(campData.enriched_creators);
        }
      }

      // Fetch analytics
      const anlRes = await fetch(`${API_BASE}/api/v1/campaigns/camp_default_001/analytics`);
      if (anlRes.ok) {
        const anlData: CampaignAnalytics = await anlRes.json();
        setAnalytics(anlData);
      }

      // Fetch outreach records
      const outRes = await fetch(`${API_BASE}/api/v1/outreach?campaign_id=camp_default_001`);
      if (outRes.ok) {
        const outData: OutreachRecord[] = await outRes.json();
        setOutreachRecords(outData);
      }
    } catch (err) {
      console.warn('Backend not responding yet or in setup. Using initial local state.', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // 2. Trigger AI Discovery Pipeline
  const handleDiscover = async () => {
    setIsDiscovering(true);
    showToast('Executing AI Ingestion, Filtering, and Brand-Fit Scoring...', 'info');

    try {
      const res = await fetch(`${API_BASE}/api/v1/campaigns/camp_default_001/discover`, {
        method: 'POST'
      });

      if (res.ok) {
        const data = await res.json();
        setCreators(data.enriched_creators || []);
        showToast(
          `AI Discovery Complete! ${data.total_discovered} creators evaluated (${data.qualified_count} qualified, ${data.rejected_count} rejected).`,
          'success'
        );
        // Refresh analytics and logs
        await loadData();
      } else {
        showToast('Discovery failed. Please verify API Gateway is running on port 5000.', 'warning');
      }
    } catch (err) {
      showToast(`Error connecting to gateway: ${(err as Error).message}`, 'warning');
    } finally {
      setIsDiscovering(false);
    }
  };

  // 3. Human Review Save
  const handleSaveReview = async (creatorId: string, status: string, editedEmail: string, editedDm: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/campaigns/camp_default_001/creators/${creatorId}/review`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reviewStatus: status, editedEmail, editedDm })
      });

      if (res.ok) {
        const updated = await res.json();
        setCreators(prev => prev.map(c => c.profile.creator_id === creatorId ? updated : c));
        if (selectedCreator && selectedCreator.profile.creator_id === creatorId) {
          setSelectedCreator(updated);
        }
        showToast(`Review saved: Pitch status updated to '${status}'.`, 'success');
      }
    } catch (err) {
      showToast('Failed to save review edits.', 'warning');
    }
  };

  // 4. Outreach Dispatch (Single)
  const handleSendOutreach = async (creator: EnrichedCreator, channel: 'Email' | 'Instagram_DM' = 'Email', customBody?: string) => {
    const p = creator.profile;
    const recipient = channel === 'Email' ? p.contact_email : p.username;
    const body = customBody || (channel === 'Email' ? creator.personalization?.email_body : creator.personalization?.dm_body) || 'Hello!';
    const subject = creator.personalization?.email_subject || `Collaboration: EDXSO AI x ${p.name}`;

    try {
      const res = await fetch(`${API_BASE}/api/v1/outreach/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          campaignId: 'camp_default_001',
          creatorId: p.creator_id,
          creatorName: p.name,
          channel,
          recipient,
          subject,
          messageBody: body
        })
      });

      const result = await res.json();

      if (result.duplicate_prevented) {
        showToast(`🛡️ Duplicate Shield: Creator '${p.name}' was already contacted! Blocked.`, 'warning');
      } else if (result.success) {
        showToast(`✓ Outreach Simulated: Pitch prepared for ${p.name} (${recipient}).`, 'success');
        // Update local creator outreach status
        setCreators(prev => prev.map(c => c.profile.creator_id === p.creator_id ? { ...c, outreach_status: result.status } : c));
        setIsReviewOpen(false);
      } else {
        showToast(`Outreach Failed: ${result.error || 'Unknown error'}`, 'warning');
      }

      await loadData();
    } catch (err) {
      showToast(`Outreach request failed: ${(err as Error).message}`, 'warning');
    }
  };

  // 5. Test Duplicate Outreach Prevention Shield
  const handleTestDuplicate = async () => {
    if (creators.length === 0) {
      showToast('Run AI pipeline first to discover creators.', 'warning');
      return;
    }

    setIsTestingDuplicate(true);
    const qualified = creators.find(c => c.filter_evaluation.status === 'PASS');
    if (!qualified) return;

    // Send first time
    await handleSendOutreach(qualified, 'Email');

    // Immediately attempt duplicate send
    setTimeout(async () => {
      await handleSendOutreach(qualified, 'Email');
      setIsTestingDuplicate(false);
    }, 800);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Toast Notification Banner */}
      {toast && (
        <div className="fixed top-20 right-6 z-50 animate-bounce">
          <div
            className={`px-4 py-3 rounded-2xl shadow-xl border flex items-center space-x-2 text-xs font-semibold backdrop-blur-md ${
              toast.type === 'success'
                ? 'bg-emerald-500/20 text-emerald-200 border-emerald-500/40'
                : toast.type === 'warning'
                ? 'bg-amber-500/20 text-amber-200 border-amber-500/40'
                : 'bg-blue-500/20 text-blue-200 border-blue-500/40'
            }`}
          >
            {toast.type === 'warning' ? (
              <ShieldAlert className="w-4 h-4 text-amber-400" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            )}
            <span>{toast.message}</span>
          </div>
        </div>
      )}

      {/* Top Navigation */}
      <Navbar
        campaignName={campaign?.campaign_name || 'AI Productivity SaaS Launch'}
        brand={campaign?.brand || 'EDXSO AI'}
        isDiscovering={isDiscovering}
        onDiscover={handleDiscover}
        dryRunMode={true}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        
        {/* KPI & Funnel Metrics Summary */}
        <FunnelOverview analytics={analytics} />

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800">
          <div className="flex space-x-1 sm:space-x-4">
            <button
              onClick={() => setActiveTab('creators')}
              className={`flex items-center space-x-2 py-3 px-3 sm:px-4 text-xs font-semibold border-b-2 transition-all cursor-pointer ${
                activeTab === 'creators'
                  ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>Creator Pipeline & Vetting</span>
              <span className="px-1.5 py-0.2 rounded-full bg-slate-800 text-[10px] text-slate-300">
                {creators.length}
              </span>
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center space-x-2 py-3 px-3 sm:px-4 text-xs font-semibold border-b-2 transition-all cursor-pointer ${
                activeTab === 'analytics'
                  ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Campaign Analytics & Insights</span>
            </button>

            <button
              onClick={() => setActiveTab('tracker')}
              className={`flex items-center space-x-2 py-3 px-3 sm:px-4 text-xs font-semibold border-b-2 transition-all cursor-pointer ${
                activeTab === 'tracker'
                  ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Clock className="w-4 h-4" />
              <span>Outreach Delivery Log</span>
              <span className="px-1.5 py-0.2 rounded-full bg-slate-800 text-[10px] text-slate-300">
                {outreachRecords.length}
              </span>
            </button>
          </div>
        </div>

        {/* Tab Views */}
        {activeTab === 'creators' && (
          <CreatorTable
            creators={creators}
            onOpenReview={(c) => {
              setSelectedCreator(c);
              setIsReviewOpen(true);
            }}
            onOpenDetail={(c) => {
              setSelectedCreator(c);
              setIsDetailOpen(true);
            }}
            onSendOutreach={(c) => handleSendOutreach(c, 'Email')}
          />
        )}

        {activeTab === 'analytics' && (
          <CampaignAnalyticsView analytics={analytics} />
        )}

        {activeTab === 'tracker' && (
          <OutreachTracker
            records={outreachRecords}
            onRefresh={loadData}
            onTestDuplicate={handleTestDuplicate}
            isTestingDuplicate={isTestingDuplicate}
          />
        )}

      </main>

      {/* Review & Personalization Studio Modal */}
      {isReviewOpen && selectedCreator && (
        <ReviewModal
          creator={selectedCreator}
          onClose={() => setIsReviewOpen(false)}
          onSaveReview={handleSaveReview}
          onSendOutreach={handleSendOutreach}
        />
      )}

      {/* Creator Detail & Brand-Fit Inspector Modal */}
      {isDetailOpen && selectedCreator && (
        <CreatorDetailModal
          creator={selectedCreator}
          onClose={() => setIsDetailOpen(false)}
          onOpenReview={(c) => {
            setSelectedCreator(c);
            setIsDetailOpen(false);
            setIsReviewOpen(true);
          }}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-800/60 py-4 mt-auto bg-slate-950/80 text-center text-xs text-slate-500">
        <p>EDXSO Influencer Outreach AI (InfluenceFlow AI) • AI Engineer Intern Assignment 1 • Production-Grade Prototype</p>
      </footer>

    </div>
  );
}
