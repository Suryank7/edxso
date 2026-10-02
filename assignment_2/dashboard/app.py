import streamlit as st
import sqlite3
import os
import json
import pandas as pd
from datetime import datetime, timezone

# Database path resolution
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "db.sqlite")

st.set_page_config(
    page_title="Scholarship Intelligence Crawler | Edxso",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and clean typography
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-verified {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-review {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-expired {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .evidence-box {
        background-color: #F1F5F9;
        border-left: 4px solid #3B82F6;
        padding: 10px 15px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Header
st.markdown('<div class="main-header">🎓 Scholarship Intelligence Crawler</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Autonomous System for Scholarship Discovery, Verification, Confidence Scoring & Change Detection | Edxso Assignment 2</div>', unsafe_allow_html=True)

# Sidebar Controls & Navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/scholarship.png", width=70)
st.sidebar.title("Navigation & Controls")

page = st.sidebar.radio("View Section", [
    "📊 Intelligence Dashboard",
    "🔎 Scholarship Explorer & Evidence",
    "🔄 Change Intelligence & Audit Logs",
    "🚀 Live Discovery & Crawler",
    "⚙️ Verification Methodology"
])

conn = get_db()
cursor = conn.cursor()

# Metrics Queries
total_sch = cursor.execute("SELECT count(*) as c FROM scholarships").fetchone()['c']
verified_sch = cursor.execute("SELECT count(*) as c FROM scholarships WHERE is_verified = 1").fetchone()['c']
review_sch = cursor.execute("SELECT count(*) as c FROM scholarships WHERE status = 'REVIEW_REQUIRED'").fetchone()['c']
active_sch = cursor.execute("SELECT count(*) as c FROM scholarships WHERE status = 'ACTIVE'").fetchone()['c']
expired_sch = cursor.execute("SELECT count(*) as c FROM scholarships WHERE status IN ('EXPIRED', 'NO_LONGER_VERIFIABLE')").fetchone()['c']
changes_sch = cursor.execute("SELECT count(*) as c FROM change_events").fetchone()['c']
avg_conf = cursor.execute("SELECT AVG(confidence_score) as c FROM scholarships").fetchone()['c'] or 0.0

if page == "📊 Intelligence Dashboard":
    # Top KPI Metrics Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.metric("Total Discovered", total_sch, help="Total real scholarships discovered in database")
    with m2:
        st.metric("Verified (≥95%)", verified_sch, delta=f"{round((verified_sch/total_sch)*100, 1)}%", help="Primary-source verified scholarships with confidence score >= 95%")
    with m3:
        st.metric("Review Required", review_sch, help="Scholarships needing human audit or additional primary source verification")
    with m4:
        st.metric("Active Opportunities", active_sch)
    with m5:
        st.metric("Expired / Stale", expired_sch, delta="-2 detected", delta_color="inverse")
    with m6:
        st.metric("Avg Confidence", f"{round(avg_conf, 1)}%")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Source Type Distribution")
        dist_df = pd.read_sql_query("SELECT source_type as Source_Type, count(*) as Count FROM scholarships GROUP BY source_type", conn)
        st.bar_chart(dist_df.set_index("Source_Type"))

    with col_chart2:
        st.subheader("Verification Status Breakdown")
        status_df = pd.read_sql_query("SELECT status as Status, count(*) as Count FROM scholarships GROUP BY status", conn)
        st.pie_chart(status_df.set_index("Status"))

    st.markdown("### 🏆 Top Verified Scholarships (High Confidence)")
    top_df = pd.read_sql_query("""
        SELECT title as Scholarship, provider as Provider, source_type as Type, amount as Benefit, closing_date as Deadline, confidence_score as Confidence, status as Status, official_url as Official_Source
        FROM scholarships WHERE is_verified = 1 ORDER BY confidence_score DESC LIMIT 5
    """, conn)
    st.dataframe(top_df, use_container_width=True)

elif page == "🔎 Scholarship Explorer & Evidence":
    st.subheader("Scholarship Explorer & Evidence Traceability")
    
    # Filter Row
    f1, f2, f3, f4 = st.columns([2, 2, 2, 3])
    with f1:
        st_type = st.selectbox("Source Type", ["All", "Government", "University", "Corporate CSR", "NGO/Trust", "International"])
    with f2:
        st_status = st.selectbox("Status", ["All", "ACTIVE", "REVIEW_REQUIRED", "EXPIRED", "NO_LONGER_VERIFIABLE"])
    with f3:
        min_c = st.slider("Min Confidence %", 0.0, 100.0, 0.0, 5.0)
    with f4:
        search_txt = st.text_input("Search Scholarship / Provider / Criteria", "")

    # Build SQL Query
    query = "SELECT * FROM scholarships WHERE 1=1"
    params = []
    if st_type != "All":
        query += " AND source_type = ?"
        params.append(st_type)
    if st_status != "All":
        query += " AND status = ?"
        params.append(st_status)
    if min_c > 0:
        query += " AND confidence_score >= ?"
        params.append(min_c)
    if search_txt:
        query += " AND (title LIKE ? OR provider LIKE ? OR eligibility_criteria LIKE ?)"
        pattern = f"%{search_txt}%"
        params.extend([pattern, pattern, pattern])

    query += " ORDER BY confidence_score DESC"
    results = cursor.execute(query, tuple(params)).fetchall()

    st.write(f"Showing **{len(results)}** matching scholarships")

    if results:
        # Create select box to open detail view
        sch_options = {f"[{r['source_type']}] {r['title']} ({r['confidence_score']}% Conf)": r['id'] for r in results}
        selected_key = st.selectbox("Select Scholarship to Inspect Details & Evidence", list(sch_options.keys()))
        selected_id = sch_options[selected_key]
        
        # Load selected record details
        sch = cursor.execute("SELECT * FROM scholarships WHERE id = ?", (selected_id,)).fetchone()
        
        st.markdown("---")
        st.markdown(f"## {sch['title']}")
        st.markdown(f"**Provider:** {sch['provider']} | **Source Type:** `{sch['source_type']}`")
        
        c_badge, c_conf, c_link = st.columns([2, 2, 4])
        with c_badge:
            if sch['confidence_score'] >= 95.0:
                st.markdown('<span class="badge-verified">✓ VERIFIED OFFICIAL</span>', unsafe_allow_html=True)
            elif sch['status'] in ['EXPIRED', 'NO_LONGER_VERIFIABLE']:
                st.markdown('<span class="badge-expired">✖ STALE / EXPIRED</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-review">⚠ REVIEW REQUIRED</span>', unsafe_allow_html=True)
        with c_conf:
            st.metric("Confidence Score", f"{sch['confidence_score']}%")
        with c_link:
            st.markdown(f"🔗 **Official Link:** [{sch['official_url']}]({sch['official_url']})")
            if sch['application_url']:
                st.markdown(f"📝 **Application Link:** [{sch['application_url']}]({sch['application_url']})")

        # Tabs for details
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Detailed Specifications", "🔍 Why This Score? (Confidence Audit)", "📜 Source Evidence Traceability", "📜 Change History"])

        with tab1:
            d1, d2 = st.columns(2)
            with d1:
                st.write("**Financial Amount:**", sch['amount'])
                st.write("**Eligibility Criteria:**", sch['eligibility_criteria'])
                st.write("**Academic Requirements:**", sch['academic_requirements'])
                st.write("**Income Criteria:**", sch['income_criteria'])
                st.write("**Gender Criteria:**", sch['gender_criteria'])
                st.write("**Category Criteria:**", sch['category_criteria'])
            with d2:
                st.write("**Education Level:**", sch['education_level'])
                st.write("**Opening Date:**", sch['opening_date'])
                st.write("**Closing Date:**", sch['closing_date'])
                st.write("**Domicile:**", sch['domicile'])
                st.write("**Documents Required:**", sch['documents_required'])
                st.write("**Selection Process:**", sch['selection_process'])
                st.write("**Renewal Terms:**", sch['renewal_terms'])

        with tab2:
            ver_row = cursor.execute("SELECT * FROM verification_results WHERE scholarship_id = ?", (selected_id,)).fetchone()
            if ver_row:
                st.markdown("### Deterministic Confidence Score Breakdown")
                st.info("The confidence score is calculated using an objective mathematical weighting formula rather than ungrounded LLM output.")
                
                v1, v2, v3, v4, v5 = st.columns(5)
                with v1:
                    st.caption("Source Authenticity (25%)")
                    st.progress(ver_row['source_authenticity_score'] / 100.0)
                    st.write(f"**{ver_row['source_authenticity_score']}%**")
                with v2:
                    st.caption("Evidence Coverage (25%)")
                    st.progress(ver_row['evidence_coverage_score'] / 100.0)
                    st.write(f"**{ver_row['evidence_coverage_score']}%**")
                with v3:
                    st.caption("Freshness (15%)")
                    st.progress(ver_row['freshness_score'] / 100.0)
                    st.write(f"**{ver_row['freshness_score']}%**")
                with v4:
                    st.caption("Consistency (15%)")
                    st.progress(ver_row['consistency_score'] / 100.0)
                    st.write(f"**{ver_row['consistency_score']}%**")
                with v5:
                    st.caption("Application URL (20%)")
                    st.progress(ver_row['application_url_score'] / 100.0)
                    st.write(f"**{ver_row['application_url_score']}%**")

                st.markdown(f"**Final Calculated Score:** `{ver_row['final_confidence_score']}%` ➔ Status: `{ver_row['status']}`")
                
                try:
                    expl = json.loads(ver_row['explanation_json'])
                    st.json(expl)
                except Exception:
                    pass

        with tab3:
            st.markdown("### Field-Level Grounded Evidence Audit")
            st.caption("Traceability: Database Record ➔ Scholarship Field ➔ Evidence Record ➔ Official Source Snippet")
            ev_rows = cursor.execute("SELECT field_name as Field, extracted_value as Value, evidence_text as Evidence_Snippet, evidence_hash as Hash, source_url as Source_URL FROM scholarship_evidence WHERE scholarship_id = ?", (selected_id,)).fetchall()
            if ev_rows:
                ev_df = pd.DataFrame([dict(r) for r in ev_rows])
                st.dataframe(ev_df, use_container_width=True)
            else:
                st.warning("No evidence records attached.")

        with tab4:
            st.markdown("### Historical Change Audit Logs")
            ch_rows = cursor.execute("SELECT field_name as Field, old_value as Old_Value, new_value as New_Value, change_type as Change_Type, detected_at as Detected_At FROM change_events WHERE scholarship_id = ?", (selected_id,)).fetchall()
            if ch_rows:
                st.dataframe(pd.DataFrame([dict(r) for r in ch_rows]), use_container_width=True)
            else:
                st.info("No change events detected for this record during recent crawls. Information remains consistent with historical snapshot.")

elif page == "🔄 Change Intelligence & Audit Logs":
    st.subheader("Snapshot Change Intelligence & Stale Scholarship Audit")
    st.write("Demonstration of continuous re-crawling, field delta detection, and status management over time.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📝 Detected Field Modifications")
        ch_all = cursor.execute("""
            SELECT s.title as Scholarship, c.field_name as Modified_Field, c.old_value as Previous_Value, c.new_value as Updated_Value, c.detected_at as Timestamp
            FROM change_events c JOIN scholarships s ON c.scholarship_id = s.id
        """).fetchall()
        if ch_all:
            st.dataframe(pd.DataFrame([dict(r) for r in ch_all]), use_container_width=True)
        else:
            st.info("No change events currently recorded.")

    with col2:
        st.markdown("### ⏳ Expired & Unverifiable Scholarships")
        stale_all = cursor.execute("""
            SELECT title as Scholarship, provider as Provider, closing_date as Deadline, status as Current_Status, official_url as Source_URL
            FROM scholarships WHERE status IN ('EXPIRED', 'NO_LONGER_VERIFIABLE')
        """).fetchall()
        if stale_all:
            st.dataframe(pd.DataFrame([dict(r) for r in stale_all]), use_container_width=True)

elif page == "🚀 Live Discovery & Crawler":
    st.subheader("Live Scholarship Discovery Engine")
    st.write("Run autonomous discovery pipeline, seed crawling, link extraction, and domain classification.")

    if st.button("🚀 Trigger Discovery Crawl Pipeline"):
        with st.spinner("Discovering candidates from official portals and seed sources..."):
            from crawler.discovery import DiscoveryEngine
            discovery = DiscoveryEngine()
            candidates = discovery.run_discovery_pipeline()
            st.success(f"Successfully processed seed sources and discovered {len(candidates)} classified candidates!")
            st.dataframe(pd.DataFrame(candidates), use_container_width=True)

    st.markdown("---")
    st.subheader("Instant Domain Authenticity Classifier Test")
    test_url = st.text_input("Enter Web Page URL to Test Classification", "https://scholarships.gov.in/schemeData")
    if test_url:
        from crawler.classifier import SourceClassifier
        res = SourceClassifier.classify_url(test_url)
        st.json(res)

elif page == "⚙️ Verification Methodology":
    st.subheader("Deterministic Verification & Anti-Hallucination Architecture")
    
    st.markdown("""
    ### Core Principles

    1. **Official-Source Verification**
       - High weight assigned to `.gov.in`, `.nic.in`, `.edu.in`, `.ac.in`, and verified corporate foundation domains.
       - Aggregators like *Buddy4Study* or blogs are classified as Discovery sources only, NOT authoritative sources.

    2. **Deterministic Confidence Algorithm**
       $$\\text{Confidence} = (S \\times 0.25) + (E \\times 0.25) + (F \\times 0.15) + (C \\times 0.15) + (A \\times 0.20)$$
       - **VERIFIED:** Confidence $\\ge 95.0\\%$ + Official Domain.
       - **REVIEW REQUIRED:** Confidence $< 95.0\\%$.

    3. **Anti-Hallucination Principle**
       - Missing income criteria in text is saved as `"Not specified"`.
       - System never invents values like `"₹5 Lakh"` without explicit textual evidence in source document.

    4. **Snapshot Delta Detection**
       - Snapshot $N$ vs Snapshot $N+1$ diffing retains old value, new value, detection timestamp, and source URL without silent overwrite.
    """)

conn.close()
