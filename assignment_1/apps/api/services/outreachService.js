const nodemailer = require('nodemailer');
const { v4: uuidv4 } = require('uuid');
const store = require('../data/store');

class OutreachService {
  /**
   * Dispatches outreach to an influencer with strict duplicate prevention,
   * dry-run simulation, and audit tracking.
   */
  static async sendOutreach({
    campaignId,
    creatorId,
    creatorName,
    channel = 'Email', // 'Email' or 'Instagram_DM'
    recipient, // email address or social handle
    subject,
    messageBody,
    isManualApproval = true
  }) {
    const isDryRun = process.env.DRY_RUN !== 'false';
    const existingRecords = store.getOutreachRecords(campaignId);

    // 1. Strict Duplicate Prevention Check: campaign_id + creator_id + channel
    const duplicate = existingRecords.find(
      r => r.campaign_id === campaignId && 
           r.creator_id === creatorId && 
           r.channel.toLowerCase() === channel.toLowerCase() &&
           ['SENT', 'SIMULATED'].includes(r.status)
    );

    if (duplicate) {
      return {
        success: false,
        duplicate_prevented: true,
        message: `Duplicate outreach prevented: Creator '${creatorName}' already contacted on channel '${channel}' for campaign '${campaignId}'.`,
        existing_record: duplicate
      };
    }

    const outreachId = `out_${uuidv4().substring(0, 8)}`;
    const now = new Date().toISOString();

    // 2. Validate Contact Channel Requirements
    if (channel === 'Email') {
      if (!recipient || recipient === 'Not Found' || !recipient.includes('@')) {
        const failedRecord = {
          outreach_id: outreachId,
          campaign_id: campaignId,
          creator_id: creatorId,
          creator_name: creatorName,
          recipient: recipient || 'Not Found',
          channel: 'Email',
          subject: subject || 'N/A',
          message_body: messageBody,
          status: 'FAILED',
          sent_at: null,
          error: 'Missing or unverified public contact email',
          retry_count: 0,
          is_dry_run: isDryRun,
          notes: 'Creator profile did not expose a verified business email.'
        };
        store.saveOutreachRecord(failedRecord);
        return {
          success: false,
          error: failedRecord.error,
          record: failedRecord
        };
      }
    }

    // 3. Execution: Dry-Run / Simulation vs Live SMTP Dispatch
    if (isDryRun || channel === 'Instagram_DM') {
      // Dry-Run Simulation or Simulated Social DM
      const outreachRecord = {
        outreach_id: outreachId,
        campaign_id: campaignId,
        creator_id: creatorId,
        creator_name: creatorName,
        recipient: recipient,
        channel: channel,
        subject: subject || `Collab: EDXSO AI x ${creatorName}`,
        message_body: messageBody,
        status: isDryRun ? 'SIMULATED' : 'SENT_MANUAL',
        sent_at: now,
        error: null,
        retry_count: 0,
        is_dry_run: isDryRun,
        notes: channel === 'Instagram_DM' 
          ? 'Instagram DM prepared for compliant manual dispatch.' 
          : 'Dry-run active: Email dispatch simulated safely without real SMTP transmission.'
      };

      store.saveOutreachRecord(outreachRecord);

      return {
        success: true,
        duplicate_prevented: false,
        status: outreachRecord.status,
        message: isDryRun
          ? `[DRY_RUN] Email simulated for ${creatorName} (${recipient}). No real email sent.`
          : `Instagram DM logged and marked ready for dispatch to @${recipient}.`,
        record: outreachRecord
      };
    }

    // 4. Live SMTP Email Dispatch
    try {
      const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST || 'smtp.gmail.com',
        port: parseInt(process.env.SMTP_PORT || '587'),
        secure: false,
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS
        }
      });

      const mailOptions = {
        from: `"${process.env.SENDER_NAME || 'EDXSO Partnerships'}" <${process.env.SENDER_EMAIL || process.env.SMTP_USER}>`,
        to: recipient,
        subject: subject,
        text: messageBody
      };

      const info = await transporter.sendMail(mailOptions);

      const liveRecord = {
        outreach_id: outreachId,
        campaign_id: campaignId,
        creator_id: creatorId,
        creator_name: creatorName,
        recipient: recipient,
        channel: 'Email',
        subject: subject,
        message_body: messageBody,
        status: 'SENT',
        sent_at: now,
        error: null,
        retry_count: 0,
        is_dry_run: false,
        message_id: info.messageId,
        notes: `Delivered via SMTP server ${process.env.SMTP_HOST}.`
      };

      store.saveOutreachRecord(liveRecord);

      return {
        success: true,
        duplicate_prevented: false,
        status: 'SENT',
        message: `Live email dispatched to ${recipient}.`,
        record: liveRecord
      };
    } catch (err) {
      console.error('[OutreachService] SMTP Error:', err);
      const errorRecord = {
        outreach_id: outreachId,
        campaign_id: campaignId,
        creator_id: creatorId,
        creator_name: creatorName,
        recipient: recipient,
        channel: 'Email',
        subject: subject,
        message_body: messageBody,
        status: 'FAILED',
        sent_at: null,
        error: err.message,
        retry_count: 1,
        is_dry_run: false,
        notes: 'SMTP transmission failed.'
      };

      store.saveOutreachRecord(errorRecord);

      return {
        success: false,
        error: err.message,
        record: errorRecord
      };
    }
  }

  static async batchSend({ campaignId, creatorIds, channel = 'Email' }) {
    const campaign = store.getCampaignById(campaignId);
    if (!campaign) {
      throw new Error(`Campaign '${campaignId}' not found.`);
    }

    const creators = campaign.enriched_creators || [];
    const targets = creatorIds && creatorIds.length > 0
      ? creators.filter(c => creatorIds.includes(c.profile.creator_id))
      : creators.filter(c => c.filter_evaluation.status === 'PASS');

    const results = [];
    for (const c of targets) {
      const recipient = channel === 'Email' ? c.profile.contact_email : c.profile.username;
      const messageBody = channel === 'Email' 
        ? (c.personalization ? c.personalization.email_body : 'Collaboration proposal')
        : (c.personalization ? c.personalization.dm_body : 'Hey, let\'s collaborate!');
      const subject = c.personalization ? c.personalization.email_subject : `Partnership with ${campaign.brand}`;

      const res = await this.sendOutreach({
        campaignId,
        creatorId: c.profile.creator_id,
        creatorName: c.profile.name,
        channel,
        recipient,
        subject,
        messageBody
      });

      // Update creator outreach status in campaign cache
      if (res.success) {
        c.outreach_status = res.status;
      }
      results.push(res);
    }

    store.saveCampaign(campaign);

    return {
      total_processed: targets.length,
      successful: results.filter(r => r.success).length,
      duplicates_prevented: results.filter(r => r.duplicate_prevented).length,
      failed: results.filter(r => !r.success && !r.duplicate_prevented).length,
      details: results
    };
  }
}

module.exports = OutreachService;
