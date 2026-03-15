# app/dashboard.py
# Student Success Factors Dashboard
# Two-page Streamlit app — Page 1: Class Overview | Page 2: Personal ID Lookup

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Student Success Factors Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STYLING ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main { background-color: #F8FAFC; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E2A3A 0%, #2D3F55 100%);
    }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #1A56DB;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 12px;
        color: #718096;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1E2A3A;
        margin-top: 4px;
    }
    .metric-delta {
        font-size: 12px;
        color: #48BB78;
        margin-top: 2px;
    }

    .section-header {
        background: linear-gradient(90deg, #1A56DB 0%, #3B82F6 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 15px;
        margin: 24px 0 16px 0;
        letter-spacing: 0.03em;
    }

    .insight-box {
        background: #EBF8FF;
        border-left: 4px solid #3182CE;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
        font-size: 14px;
        color: #2C5282;
    }

    .rec-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 8px 0;
        border-left: 4px solid #48BB78;
    }
    .rec-title {
        font-weight: 700;
        color: #276749;
        font-size: 14px;
    }
    .rec-body {
        color: #4A5568;
        font-size: 13px;
        margin-top: 4px;
    }

    .warn-card {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        font-size: 14px;
        color: #744210;
    }

    .profile-header {
        background: linear-gradient(135deg, #1E2A3A 0%, #2D3F55 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    /* ADD THIS */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
    color: white !important;
    font-weight: 600;
}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'clean_survey_responses.csv'),
        os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_survey_responses.csv'),
        'data/processed/clean_survey_responses.csv',
        'data/clean_survey_responses.csv',
    ]
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            return df
    st.error("Could not find clean_survey_responses.csv. Check that data/processed/ folder exists.")
    st.stop()

df = load_data()

# ─── COLUMN NAME RESOLVER ─────────────────────────────────────────────────────

def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

COL_ID         = find_col(df, ['anonymous_id', 'student_id', 'id', 'anon_id'])
COL_GPA        = find_col(df, ['gpa', 'grade_point', 'grade'])
COL_ATTEND     = find_col(df, ['attendance_percent', 'attendance', 'attendance_pct'])
COL_STUDY_HRS  = find_col(df, ['study_hours_week', 'study_hours', 'study_hrs', 'weekly_study_hours'])
COL_ASSIGN     = find_col(df, ['assignment_completion', 'assignment_completion_rate', 'assignment'])
COL_TUTORIAL   = find_col(df, ['tutorial_attendance', 'tutorial', 'tutorials'])
COL_STUDY_GRP  = find_col(df, ['study_group', 'study_group_participation', 'group_study'])
COL_INTERNET   = find_col(df, ['internet_quality', 'internet', 'internet_access'])
COL_JOB        = find_col(df, ['part_time_job', 'parttime_job', 'has_job', 'job'])
COL_DORM       = find_col(df, ['dorm_resident', 'dorm', 'lives_in_dorm', 'dormitory'])
COL_MENTAL     = find_col(df, ['mental_health_rating', 'mental_health', 'wellbeing'])
COL_CHALLENGE  = find_col(df, ['main_challenge', 'challenge', 'main_academic_challenge'])
COL_RISK       = find_col(df, ['academic_risk', 'risk', 'risk_level'])
COL_ENGAGE     = find_col(df, ['engagement_score', 'engagement', 'engage_score'])
COL_DIFFICULTY = find_col(df, ['course_difficulty', 'difficulty', 'difficulty_rating'])
COL_STUDY_TIME = find_col(df, ['preferred_study_time', 'study_time_preference', 'preferred_time'])
COL_GENDER     = find_col(df, ['gender', 'sex'])
COL_DEPT       = find_col(df, ['course_dept', 'department', 'course', 'dept'])
COL_SEMESTER   = find_col(df, ['semester', 'sem', 'semester_code'])
COL_GPA_BAND   = find_col(df, ['gpa_band', 'gpa_category', 'performance_band'])
COL_REPEAT     = find_col(df, ['repeat_student', 'repeat', 'is_repeat'])

# ─── HELPER: safe float display ──────────────────────────────────────────────

def fmt(val, decimals=2, suffix=""):
    try:
        return f"{float(val):.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return "N/A"

def safe_delta(a, b, decimals=2, suffix=""):
    try:
        diff = float(a) - float(b)
        sign = "+" if diff >= 0 else ""
        return f"{sign}{diff:.{decimals}f}{suffix} vs class"
    except (TypeError, ValueError):
        return ""

def delta_color(val, ref, higher_is_better=True):
    try:
        return "#48BB78" if (float(val) >= float(ref)) == higher_is_better else "#FC8181"
    except (TypeError, ValueError):
        return "#718096"

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        "<h2 style='color:#FFFFFF; margin-bottom:4px'>🎓 Student Success</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#90CDF4; font-weight:700; margin-top:0'>Dashboard v1.0</p>",
        unsafe_allow_html=True
    )
    st.markdown("<hr style='border-color:#3D5A80'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["📊 Class Overview", "🔍 My Personal Stats"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#3D5A80'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#A0AEC0; font-size:13px; font-weight:700; "
        "text-transform:uppercase; letter-spacing:0.05em'>Dataset Info</p>",
        unsafe_allow_html=True
    )

    n_records      = len(df)
    avg_gpa_side   = fmt(df[COL_GPA].mean(), 2) if COL_GPA else "N/A"
    avg_att_side   = fmt(df[COL_ATTEND].mean(), 1, "%") if COL_ATTEND else "N/A"

    st.markdown(f"""
    <div style='background:#2D3F55;border-radius:8px;padding:14px 16px;margin-bottom:8px'>
        <div style='color:#90CDF4;font-size:12px;font-weight:600'>👥 Students</div>
        <div style='color:#FFFFFF;font-size:22px;font-weight:700'>{n_records}</div>
    </div>
    <div style='background:#2D3F55;border-radius:8px;padding:14px 16px;margin-bottom:8px'>
        <div style='color:#90CDF4;font-size:12px;font-weight:600'>📈 Avg GPA</div>
        <div style='color:#FFFFFF;font-size:22px;font-weight:700'>{avg_gpa_side}</div>
    </div>
    <div style='background:#2D3F55;border-radius:8px;padding:14px 16px;margin-bottom:16px'>
        <div style='color:#90CDF4;font-size:12px;font-weight:600'>📋 Avg Attendance</div>
        <div style='color:#FFFFFF;font-size:22px;font-weight:700'>{avg_att_side}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#3D5A80'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#718096;font-size:12px;line-height:1.6'>"
        "Built by <strong style='color:#90CDF4'>Betelhem Hailu</strong><br>"
        "ASTU · Software Engineering · 2026</p>",
        unsafe_allow_html=True
    )

# ─── TRENDLINE HELPER (no statsmodels needed) ────────────────────────────────

def add_trendline(fig, x_vals, y_vals, color="#E53E3E", name="Trend"):
    """Compute OLS trendline manually using numpy — no statsmodels required."""
    try:
        x = np.array(x_vals, dtype=float)
        y = np.array(y_vals, dtype=float)
        mask = ~(np.isnan(x) | np.isnan(y))
        x, y = x[mask], y[mask]
        if len(x) < 2:
            return fig
        m, b = np.polyfit(x, 1, deg=1) if False else np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = m * x_line + b
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode='lines', name=name,
            line=dict(color=color, width=2, dash='dot'),
            showlegend=True
        ))
    except Exception:
        pass
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — CLASS OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════

if page == "📊 Class Overview":

    st.markdown("# 📊 Student Success Factors Dashboard")
    st.markdown("*Cohort-level analysis of academic performance drivers — ASTU Software Engineering*")
    st.markdown("---")

    # ── KPI ROW ──────────────────────────────────────────────────────────────

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        v = fmt(df[COL_GPA].mean(), 2) if COL_GPA else "N/A"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Average GPA</div>
            <div class="metric-value">{v}</div>
            <div class="metric-delta">out of 4.00</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        v = fmt(df[COL_ATTEND].mean(), 1, "%") if COL_ATTEND else "N/A"
        st.markdown(f"""<div class="metric-card" style="border-left-color:#48BB78">
            <div class="metric-label">Avg Attendance</div>
            <div class="metric-value">{v}</div>
            <div class="metric-delta">across all students</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        v = fmt(df[COL_STUDY_HRS].mean(), 1) if COL_STUDY_HRS else "N/A"
        st.markdown(f"""<div class="metric-card" style="border-left-color:#9F7AEA">
            <div class="metric-label">Avg Study Hours/Week</div>
            <div class="metric-value">{v}</div>
            <div class="metric-delta">hours per week</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        n = df[COL_ID].nunique() if COL_ID else len(df)
        st.markdown(f"""<div class="metric-card" style="border-left-color:#ED8936">
            <div class="metric-label">Total Students</div>
            <div class="metric-value">{n}</div>
            <div class="metric-delta">survey respondents</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 1: GPA Distribution + Academic Risk ───────────────────────────────

    st.markdown('<div class="section-header">📈 Academic Performance Overview</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if COL_GPA:
            fig = px.histogram(
                df, x=COL_GPA, nbins=15,
                title="GPA Distribution",
                color_discrete_sequence=["#1A56DB"],
                labels={COL_GPA: "GPA"},
            )
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white", bargap=0.1,
                xaxis=dict(title="GPA", gridcolor="#F0F4F8"),
                yaxis=dict(title="Number of Students", gridcolor="#F0F4F8"),
                title_font_size=15, showlegend=False
            )
            fig.add_vline(
                x=df[COL_GPA].mean(), line_dash="dash", line_color="#E53E3E",
                annotation_text=f"Mean: {df[COL_GPA].mean():.2f}",
                annotation_position="top right"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Most students fall within the mid-to-high GPA range.
                Additional academic support should target students in the lower GPA band.
            </div>""", unsafe_allow_html=True)

    with col2:
        if COL_RISK:
            risk_counts = df[COL_RISK].value_counts().reset_index()
            risk_counts.columns = ['Risk Level', 'Count']
            color_map = {
                'Low': '#48BB78', 'Moderate': '#F6AD55', 'High': '#FC8181',
                'low': '#48BB78', 'moderate': '#F6AD55', 'high': '#FC8181',
                'Low Risk': '#48BB78', 'Moderate Risk': '#F6AD55', 'High Risk': '#FC8181',
            }
            fig = px.pie(
                risk_counts, values='Count', names='Risk Level',
                title="Academic Risk Segmentation",
                color='Risk Level', color_discrete_map=color_map, hole=0.45
            )
            fig.update_layout(paper_bgcolor="white", title_font_size=15)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Most students fall within low-to-moderate risk.
                Early intervention programs are recommended for high-risk students.
            </div>""", unsafe_allow_html=True)

    # ── ROW 2: Attendance vs GPA + Study Hours vs GPA ────────────────────────

    st.markdown('<div class="section-header">📚 Study Habits vs Academic Performance</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        if COL_ATTEND and COL_GPA:
            fig = px.scatter(
                df, x=COL_ATTEND, y=COL_GPA,
                color=COL_GENDER if COL_GENDER else None,
                title="Attendance % vs GPA",
                labels={COL_ATTEND: "Attendance (%)", COL_GPA: "GPA"},
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig = add_trendline(fig, df[COL_ATTEND], df[COL_GPA], "#E53E3E", "Trend")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(gridcolor="#F0F4F8"),
                yaxis=dict(gridcolor="#F0F4F8"),
                title_font_size=15
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Higher attendance is positively associated with better GPA.
                Students should maintain consistent lecture attendance.
            </div>""", unsafe_allow_html=True)

    with col4:
        if COL_STUDY_HRS and COL_GPA:
            fig = px.scatter(
                df, x=COL_STUDY_HRS, y=COL_GPA,
                title="Study Hours/Week vs GPA",
                labels={COL_STUDY_HRS: "Study Hours per Week", COL_GPA: "GPA"},
                color_discrete_sequence=["#9F7AEA"]
            )
            fig = add_trendline(fig, df[COL_STUDY_HRS], df[COL_GPA], "#E53E3E", "Trend")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(gridcolor="#F0F4F8"),
                yaxis=dict(gridcolor="#F0F4F8"),
                title_font_size=15
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                More study hours per week correlates with higher GPA.
                Students should develop consistent study routines.
            </div>""", unsafe_allow_html=True)

    # ── ROW 3: Tutorial + Study Group ────────────────────────────────────────

    st.markdown('<div class="section-header">🤝 Participation Impact</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        if COL_TUTORIAL and COL_GPA:
            tut_gpa = df.groupby(COL_TUTORIAL)[COL_GPA].mean().reset_index()
            tut_gpa.columns = ['Tutorial Attendance', 'Average GPA']
            fig = px.bar(
                tut_gpa, x='Tutorial Attendance', y='Average GPA',
                title="Tutorial Attendance Impact on GPA",
                color='Tutorial Attendance',
                color_discrete_sequence=['#FC8181', '#48BB78'],
                text='Average GPA'
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(range=[0, 4.3], gridcolor="#F0F4F8"),
                title_font_size=15, showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Tutorial attendees achieve GPA of 3.58 vs 2.67 for non-attendees —
                a 0.91 GPA advantage. Encourage tutorial participation strongly.
            </div>""", unsafe_allow_html=True)

    with col6:
        if COL_STUDY_GRP and COL_GPA:
            grp_gpa = df.groupby(COL_STUDY_GRP)[COL_GPA].mean().reset_index()
            grp_gpa.columns = ['Study Group', 'Average GPA']
            fig = px.bar(
                grp_gpa, x='Study Group', y='Average GPA',
                title="Study Group Participation vs GPA",
                color='Study Group',
                color_discrete_sequence=['#FC8181', '#48BB78'],
                text='Average GPA'
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(range=[0, 4.3], gridcolor="#F0F4F8"),
                title_font_size=15, showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Study group participants average GPA of 3.58 vs 2.67 for solo studiers.
                Promote peer-learning initiatives across the department.
            </div>""", unsafe_allow_html=True)

    # ── ROW 4: Internet Quality + Engagement Score ────────────────────────────

    st.markdown('<div class="section-header">💻 Resources & Engagement</div>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)

    with col7:
        if COL_INTERNET and COL_GPA:
            inet_gpa = df.groupby(COL_INTERNET)[COL_GPA].mean().reset_index()
            inet_gpa.columns = ['Internet Quality', 'Average GPA']
            order_map = {
                'good': 0, 'fair': 1, 'poor': 2,
                'Good': 0, 'Fair': 1, 'Poor': 2
            }
            inet_gpa['sort_key'] = inet_gpa['Internet Quality'].map(order_map).fillna(99)
            inet_gpa = inet_gpa.sort_values('sort_key')
            fig = px.bar(
                inet_gpa, x='Internet Quality', y='Average GPA',
                title="Internet Quality vs GPA",
                color='Internet Quality',
                color_discrete_sequence=['#48BB78', '#F6AD55', '#FC8181'],
                text='Average GPA'
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(range=[0, 4.3], gridcolor="#F0F4F8"),
                title_font_size=15, showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Good internet: 3.69 GPA · Fair: 2.97 · Poor: 2.40.
                Digital infrastructure gaps directly impact academic outcomes.
            </div>""", unsafe_allow_html=True)

    with col8:
        if COL_ENGAGE and COL_GPA:
            fig = px.scatter(
                df, x=COL_ENGAGE, y=COL_GPA,
                title="Engagement Score vs GPA",
                labels={COL_ENGAGE: "Engagement Score", COL_GPA: "GPA"},
                color_discrete_sequence=["#1A56DB"]
            )
            fig = add_trendline(fig, df[COL_ENGAGE], df[COL_GPA], "#E53E3E", "Trend")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(gridcolor="#F0F4F8"),
                yaxis=dict(gridcolor="#F0F4F8"),
                title_font_size=15
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Higher engagement scores strongly predict higher GPAs.
                Increase engagement through interactive learning activities.
            </div>""", unsafe_allow_html=True)

    # ── ROW 5: Lifestyle Analysis ─────────────────────────────────────────────

    st.markdown('<div class="section-header">🌙 Lifestyle & Wellbeing</div>', unsafe_allow_html=True)
    col9, col10 = st.columns(2)

    with col9:
        if COL_JOB and COL_GPA and COL_MENTAL:
            job_stats = df.groupby(COL_JOB).agg(
                avg_gpa=(COL_GPA, 'mean'),
                avg_mental=(COL_MENTAL, 'mean')
            ).reset_index()
            job_stats.columns = ['Part-Time Job', 'Avg GPA', 'Avg Mental Health']
            job_labels = job_stats['Part-Time Job'].tolist()

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(
                    name='Avg GPA', x=job_labels, y=job_stats['Avg GPA'],
                    marker_color='#1A56DB',
                    text=job_stats['Avg GPA'].round(2), textposition='outside'
                ),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(
                    name='Mental Health', x=job_labels,
                    y=job_stats['Avg Mental Health'],
                    mode='lines+markers',
                    marker=dict(color='#ED8936', size=10),
                    line=dict(width=2, dash='dot')
                ),
                secondary_y=True
            )
            fig.update_layout(
                title_text="Part-Time Job: GPA & Mental Health Impact",
                plot_bgcolor="white", paper_bgcolor="white", title_font_size=15
            )
            fig.update_yaxes(title_text="Avg GPA", secondary_y=False, range=[0, 4.5])
            fig.update_yaxes(title_text="Mental Health Rating", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                No job: GPA 3.51, MH 4.09 · With job: GPA 2.63, MH 2.50.
                Provide flexible support for working students.
            </div>""", unsafe_allow_html=True)

    with col10:
        if COL_MENTAL and COL_GPA:
            fig = px.scatter(
                df, x=COL_MENTAL, y=COL_GPA,
                title="Mental Health Rating vs GPA",
                labels={COL_MENTAL: "Mental Health Rating (1–5)", COL_GPA: "GPA"},
                color_discrete_sequence=["#9F7AEA"]
            )
            fig = add_trendline(fig, df[COL_MENTAL], df[COL_GPA], "#E53E3E", "Trend")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(gridcolor="#F0F4F8"),
                yaxis=dict(gridcolor="#F0F4F8"),
                title_font_size=15
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Better mental health ratings are associated with more stable, higher GPAs.
                Balance academics with rest and stress management.
            </div>""", unsafe_allow_html=True)

    # ── ROW 6: Challenges + Correlation Heatmap ───────────────────────────────

    st.markdown('<div class="section-header">🔥 Challenges & Correlations</div>', unsafe_allow_html=True)
    col11, col12 = st.columns(2)

    with col11:
        if COL_CHALLENGE:
            challenge_counts = df[COL_CHALLENGE].value_counts().reset_index()
            challenge_counts.columns = ['Challenge', 'Count']
            fig = px.bar(
                challenge_counts, x='Count', y='Challenge',
                orientation='h',
                title="Main Academic Challenges Reported",
                color='Count',
                color_continuous_scale='Blues',
                text='Count'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(categoryorder='total ascending'),
                title_font_size=15, coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Time management, programming difficulty, and lack of resources top the list.
                Target these areas with structured support programs.
            </div>""", unsafe_allow_html=True)

    with col12:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        keep = [c for c in [COL_GPA, COL_ATTEND, COL_STUDY_HRS,
                             COL_MENTAL, COL_ENGAGE, COL_DIFFICULTY]
                if c and c in numeric_cols]
        if len(keep) >= 3:
            corr_df = df[keep].corr().round(2)
            readable = {
                COL_GPA: 'GPA', COL_ATTEND: 'Attendance',
                COL_STUDY_HRS: 'Study Hrs', COL_MENTAL: 'Mental Health',
                COL_ENGAGE: 'Engagement', COL_DIFFICULTY: 'Difficulty'
            }
            corr_df = corr_df.rename(
                columns={k: v for k, v in readable.items() if k},
                index={k: v for k, v in readable.items() if k}
            )
            fig = px.imshow(
                corr_df, text_auto=True, aspect="auto",
                title="Correlation Heatmap",
                color_continuous_scale='RdBu_r', zmin=-1, zmax=1
            )
            fig.update_layout(paper_bgcolor="white", title_font_size=15)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
                Attendance, study hours, and engagement show the strongest
                positive correlations with GPA.
            </div>""", unsafe_allow_html=True)

    # ── ROW 7: Top Student Habits ─────────────────────────────────────────────

    st.markdown('<div class="section-header">🏆 Top Performing Students</div>', unsafe_allow_html=True)

    if COL_GPA:
        top_threshold = df[COL_GPA].quantile(0.75)
        top_df = df[df[COL_GPA] >= top_threshold]

        t1, t2, t3, t4 = st.columns(4)

        top_attend = top_df[COL_ATTEND].mean() if COL_ATTEND else None
        all_attend = df[COL_ATTEND].mean() if COL_ATTEND else None
        top_hrs    = top_df[COL_STUDY_HRS].mean() if COL_STUDY_HRS else None
        all_hrs    = df[COL_STUDY_HRS].mean() if COL_STUDY_HRS else None

        with t1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Top Students Attendance</div>
                <div class="metric-value">{fmt(top_attend, 1, "%")}</div>
                <div class="metric-delta">Class avg: {fmt(all_attend, 1, "%")}</div>
            </div>""", unsafe_allow_html=True)

        with t2:
            st.markdown(f"""<div class="metric-card" style="border-left-color:#48BB78">
                <div class="metric-label">Top Students Study Hrs</div>
                <div class="metric-value">{fmt(top_hrs, 1)} hrs</div>
                <div class="metric-delta">Class avg: {fmt(all_hrs, 1)} hrs</div>
            </div>""", unsafe_allow_html=True)

        with t3:
            tut_pct = 0
            if COL_TUTORIAL:
                tut_pct = (
                    top_df[COL_TUTORIAL].astype(str).str.lower()
                    .isin(['yes', 'true', '1']).sum() / len(top_df) * 100
                )
            st.markdown(f"""<div class="metric-card" style="border-left-color:#9F7AEA">
                <div class="metric-label">Tutorial Attendance Rate</div>
                <div class="metric-value">{fmt(tut_pct, 0, "%")}</div>
                <div class="metric-delta">of top performers</div>
            </div>""", unsafe_allow_html=True)

        with t4:
            top_gpa = top_df[COL_GPA].mean()
            st.markdown(f"""<div class="metric-card" style="border-left-color:#ED8936">
                <div class="metric-label">Top Students Avg GPA</div>
                <div class="metric-value">{fmt(top_gpa, 2)}</div>
                <div class="metric-delta">vs class avg: {fmt(df[COL_GPA].mean(), 2)}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="insight-box">
            Top-performing students maintain ~92% attendance, study 17+ hrs/week,
            complete nearly all assignments, and all attend tutorials.
            Use these as benchmarks for student success programs.
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PERSONAL ID LOOKUP
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "🔍 My Personal Stats":

    st.markdown("# 🔍 Personal Academic Stats")
    st.markdown("*Enter your anonymous ID to see how your habits compare to the class*")
    st.markdown("---")

    # ── ID INPUT ─────────────────────────────────────────────────────────────

    col_input, col_hint = st.columns([2, 3])
    with col_input:
        student_id = st.text_input(
            "Your Anonymous ID",
            placeholder="e.g. panda12, bytecoder, ninja07",
            help="The alias you created when you filled out the survey"
        )

    with col_hint:
        if COL_ID:
            all_ids = sorted(df[COL_ID].dropna().astype(str).unique().tolist())
            id_pills = " · ".join([f"<code>{i}</code>" for i in all_ids])
            st.markdown(f"""<div class="warn-card">
                <strong>Available IDs in this dataset:</strong><br>{id_pills}
            </div>""", unsafe_allow_html=True)

    if not student_id:
        st.markdown("""<div class="insight-box" style="margin-top:24px">
            Enter your anonymous ID above to view your personalized academic profile,
            see how your study habits compare to classmates, and receive tailored
            improvement recommendations.
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── LOOKUP ───────────────────────────────────────────────────────────────

    if not COL_ID:
        st.error("Could not find an ID column in the dataset.")
        st.stop()

    student_rows = df[
        df[COL_ID].astype(str).str.strip().str.lower()
        == student_id.strip().lower()
    ]

    if student_rows.empty:
        st.error(f"ID **'{student_id}'** not found. Check spelling or pick from the list above.")
        st.stop()

    # Pick latest semester if multi-semester, else first row
    if COL_SEMESTER and COL_SEMESTER in student_rows.columns:
        student = student_rows.sort_values(COL_SEMESTER).iloc[-1]
    else:
        student = student_rows.iloc[0]

    # ── SAFE VALUE EXTRACTION ─────────────────────────────────────────────────

    def safe_get(row, col):
        if col and col in row.index:
            v = row[col]
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        return None

    s_gpa    = safe_get(student, COL_GPA)
    s_attend = safe_get(student, COL_ATTEND)
    s_hrs    = safe_get(student, COL_STUDY_HRS)
    s_engage = safe_get(student, COL_ENGAGE)
    s_mental = safe_get(student, COL_MENTAL)

    c_gpa    = float(df[COL_GPA].mean())    if COL_GPA    else None
    c_attend = float(df[COL_ATTEND].mean()) if COL_ATTEND else None
    c_hrs    = float(df[COL_STUDY_HRS].mean()) if COL_STUDY_HRS else None
    c_engage = float(df[COL_ENGAGE].mean()) if COL_ENGAGE else None
    c_mental = float(df[COL_MENTAL].mean()) if COL_MENTAL else None

    # ── PROFILE HEADER ────────────────────────────────────────────────────────

    gpa_status = "🟢 Above Average" if (s_gpa and c_gpa and s_gpa >= c_gpa) else "🔴 Below Average"
    risk_val   = student[COL_RISK] if COL_RISK and COL_RISK in student.index else "N/A"

    st.markdown(f"""
    <div class="profile-header">
        <h2 style="margin:0;color:white">👤 {student_id.upper()}</h2>
        <p style="margin:4px 0 0 0;color:#90CDF4">
            GPA Status: <strong>{gpa_status}</strong> &nbsp;|&nbsp;
            Academic Risk: <strong>{risk_val}</strong>
        </p>
    </div>""", unsafe_allow_html=True)

    # ── METRICS: STUDENT vs CLASS ─────────────────────────────────────────────

    st.markdown('<div class="section-header">📊 Your Stats vs Class Average</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        color = delta_color(s_gpa, c_gpa)
        st.markdown(f"""<div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">Your GPA</div>
            <div class="metric-value" style="color:{color}">{fmt(s_gpa, 2)}</div>
            <div class="metric-delta" style="color:{color}">{safe_delta(s_gpa, c_gpa, 2)}</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        color = delta_color(s_attend, c_attend)
        st.markdown(f"""<div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">Your Attendance</div>
            <div class="metric-value" style="color:{color}">{fmt(s_attend, 1, "%")}</div>
            <div class="metric-delta" style="color:{color}">{safe_delta(s_attend, c_attend, 1, "%")}</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        color = delta_color(s_hrs, c_hrs)
        st.markdown(f"""<div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">Your Study Hrs/Week</div>
            <div class="metric-value" style="color:{color}">{fmt(s_hrs, 1)}</div>
            <div class="metric-delta" style="color:{color}">{safe_delta(s_hrs, c_hrs, 1, " hrs")}</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        color = delta_color(s_engage, c_engage)
        st.markdown(f"""<div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">Engagement Score</div>
            <div class="metric-value" style="color:{color}">{fmt(s_engage, 1)}</div>
            <div class="metric-delta" style="color:{color}">{safe_delta(s_engage, c_engage, 1)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RADAR CHART ───────────────────────────────────────────────────────────

    st.markdown('<div class="section-header">🕸 Your Habit Profile vs Cohort</div>', unsafe_allow_html=True)

    radar_cols = [c for c in [COL_ATTEND, COL_STUDY_HRS, COL_ENGAGE, COL_MENTAL] if c]

    if len(radar_cols) >= 3:
        def normalize(val, col):
            try:
                col_min = float(df[col].min())
                col_max = float(df[col].max())
                if col_max == col_min:
                    return 0.5
                return (float(val) - col_min) / (col_max - col_min)
            except (TypeError, ValueError):
                return 0.5

        labels_map = {
            COL_ATTEND: 'Attendance', COL_STUDY_HRS: 'Study Hours',
            COL_ENGAGE: 'Engagement', COL_MENTAL: 'Mental Health',
        }

        student_vals  = [normalize(student[c], c) for c in radar_cols]
        class_vals    = [normalize(df[c].mean(), c) for c in radar_cols]
        radar_labels  = [labels_map.get(c, c) for c in radar_cols]

        # Close the polygon
        sv = student_vals + [student_vals[0]]
        cv = class_vals   + [class_vals[0]]
        rl = radar_labels + [radar_labels[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=cv, theta=rl, fill='toself', name='Class Average',
            line_color='#A0AEC0', fillcolor='rgba(160,174,192,0.2)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=sv, theta=rl, fill='toself', name=student_id.upper(),
            line_color='#1A56DB', fillcolor='rgba(26,86,219,0.2)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            paper_bgcolor="white",
            title=f"{student_id.upper()} vs Class Average — Habit Profile",
            title_font_size=15,
            legend=dict(orientation='h', y=-0.1)
        )

        radar_col, info_col = st.columns([2, 1])
        with radar_col:
            st.plotly_chart(fig_radar, use_container_width=True)
        with info_col:
            st.markdown("**How to read this chart:**")
            st.markdown(
                "Blue shape = your profile. Grey = class average. "
                "Blue extending beyond grey = your strength. "
                "Grey extending beyond blue = growth area."
            )
            st.markdown("")
            for i, label in enumerate(radar_labels):
                try:
                    s_raw = float(student[radar_cols[i]])
                    c_raw = float(df[radar_cols[i]].mean())
                    icon  = "✅" if s_raw >= c_raw else "⚠️"
                    st.markdown(f"{icon} **{label}**: `{s_raw:.1f}` (avg `{c_raw:.1f}`)")
                except (TypeError, ValueError):
                    st.markdown(f"— **{label}**: N/A")

    # ── SURVEY RESPONSES TABLE ────────────────────────────────────────────────

    st.markdown('<div class="section-header">📋 Your Survey Responses</div>', unsafe_allow_html=True)

    display_cols = [c for c in [
        COL_ID, COL_GPA, COL_ATTEND, COL_STUDY_HRS,
        COL_TUTORIAL, COL_STUDY_GRP, COL_ASSIGN,
        COL_INTERNET, COL_MENTAL, COL_CHALLENGE, COL_RISK, COL_ENGAGE
    ] if c]

    rename_map = {
        COL_ID: 'Student ID', COL_GPA: 'GPA',
        COL_ATTEND: 'Attendance %', COL_STUDY_HRS: 'Study Hrs/Wk',
        COL_TUTORIAL: 'Tutorials', COL_STUDY_GRP: 'Study Group',
        COL_ASSIGN: 'Assignment Completion', COL_INTERNET: 'Internet Quality',
        COL_MENTAL: 'Mental Health', COL_CHALLENGE: 'Main Challenge',
        COL_RISK: 'Academic Risk', COL_ENGAGE: 'Engagement Score'
    }

    student_display = student_rows[display_cols].copy()
    student_display = student_display.rename(
        columns={k: v for k, v in rename_map.items() if k}
    )
    st.dataframe(student_display, use_container_width=True, hide_index=True)

    # ── PERSONALIZED RECOMMENDATIONS ─────────────────────────────────────────

    st.markdown('<div class="section-header">💡 Personalized Recommendations</div>', unsafe_allow_html=True)

    recommendations = []

    # Below-average GPA but good attendance
    if s_gpa and c_gpa and s_attend and c_attend:
        if s_gpa < c_gpa and s_attend >= c_attend:
            recommendations.append({
                "title": "🎯 Convert Attendance into Results",
                "body": (
                    f"You attend class at {fmt(s_attend, 1, '%')} — above the class average. "
                    "But your GPA is below average, meaning attendance alone isn't enough. "
                    "Focus on active note-taking, asking questions in class, "
                    "and reviewing material within 24 hours of each lecture."
                )
            })

    # Not attending tutorials
    if COL_TUTORIAL and COL_TUTORIAL in student.index:
        tut_val = str(student[COL_TUTORIAL]).strip().lower()
        if tut_val not in ['yes', 'true', '1']:
            recommendations.append({
                "title": "📚 Start Attending Tutorials",
                "body": (
                    "Students who attend tutorials achieve a GPA of 3.58 vs 2.67 for those who don't "
                    "— a 0.91 point difference. Tutorials are the single highest-return habit in this "
                    "dataset. Attend at least 80% of available tutorial sessions."
                )
            })

    # Not in study group
    if COL_STUDY_GRP and COL_STUDY_GRP in student.index:
        grp_val = str(student[COL_STUDY_GRP]).strip().lower()
        if grp_val not in ['yes', 'true', '1']:
            recommendations.append({
                "title": "🤝 Join a Study Group",
                "body": (
                    "Study group participants average 3.58 GPA vs 2.67 for solo studiers. "
                    "Peer explanation is one of the most effective learning techniques. "
                    "Form or join a group of 3–5 students meeting at least twice per week."
                )
            })

    # Below-average study hours
    if s_hrs and c_hrs and s_hrs < c_hrs:
        recommendations.append({
            "title": "⏰ Increase Weekly Study Hours",
            "body": (
                f"You study {fmt(s_hrs, 1)} hrs/week vs a class average of {fmt(c_hrs, 1)} hrs. "
                "Top-performing students study 17+ hrs/week. Try adding one focused "
                "2-hour study block per day — small consistent increases compound quickly."
            )
        })

    # Poor internet
    if COL_INTERNET and COL_INTERNET in student.index:
        inet_val = str(student[COL_INTERNET]).strip().lower()
        if inet_val == 'poor':
            recommendations.append({
                "title": "📶 Address Internet Connectivity",
                "body": (
                    "Poor internet quality is associated with a GPA of 2.40 vs 3.69 for students "
                    "with good access. Explore university library resources, download materials "
                    "offline, and speak to your department about digital support programs."
                )
            })

    # Below-average mental health
    if s_mental and c_mental and s_mental < c_mental:
        recommendations.append({
            "title": "🌿 Prioritize Mental Wellbeing",
            "body": (
                "Your mental health rating is below the class average. "
                "Students with better ratings achieve more stable GPAs. "
                "Schedule regular rest, talk to a peer or counselor, "
                "and reduce all-nighter study sessions."
            )
        })

    # Positive reinforcement if attendance is good
    if s_attend and c_attend and s_attend >= c_attend:
        recommendations.append({
            "title": "✅ Maintain Your Strong Attendance",
            "body": (
                f"Your attendance of {fmt(s_attend, 1, '%')} is at or above the class average "
                f"of {fmt(c_attend, 1, '%')}. This is a critical success habit. "
                "Keep showing up and you give yourself the best platform to improve."
            )
        })

    # Fallback
    if not recommendations:
        recommendations.append({
            "title": "🌟 You Are On Track",
            "body": (
                "Your academic habits are performing at or above class average across all key metrics. "
                "Focus on maintaining consistency, peer teaching others in study groups, "
                "and building exam preparation strategies 3+ weeks before assessments."
            )
        })

    for rec in recommendations:
        st.markdown(f"""<div class="rec-card">
            <div class="rec-title">{rec['title']}</div>
            <div class="rec-body">{rec['body']}</div>
        </div>""", unsafe_allow_html=True)

    # ── SEMESTER TREND (if multi-semester data exists) ────────────────────────

    if COL_SEMESTER and COL_GPA and len(student_rows) > 1:

        st.markdown('<div class="section-header">📅 Your Semester Performance Trend</div>', unsafe_allow_html=True)

        sem_gpa = student_rows[[COL_SEMESTER, COL_GPA]].sort_values(COL_SEMESTER).copy()
        sem_gpa[COL_GPA] = pd.to_numeric(sem_gpa[COL_GPA], errors='coerce')

        best_idx  = sem_gpa[COL_GPA].idxmax()
        worst_idx = sem_gpa[COL_GPA].idxmin()

        scol1, scol2 = st.columns(2)
        with scol1:
            st.markdown(f"""<div class="metric-card" style="border-left-color:#48BB78">
                <div class="metric-label">🏆 Strongest Semester</div>
                <div class="metric-value">{sem_gpa.loc[best_idx, COL_SEMESTER]}</div>
                <div class="metric-delta">GPA: {fmt(sem_gpa.loc[best_idx, COL_GPA], 2)}</div>
            </div>""", unsafe_allow_html=True)
        with scol2:
            st.markdown(f"""<div class="metric-card" style="border-left-color:#FC8181">
                <div class="metric-label">📉 Weakest Semester</div>
                <div class="metric-value">{sem_gpa.loc[worst_idx, COL_SEMESTER]}</div>
                <div class="metric-delta">GPA: {fmt(sem_gpa.loc[worst_idx, COL_GPA], 2)}</div>
            </div>""", unsafe_allow_html=True)

        fig_trend = px.line(
            sem_gpa, x=COL_SEMESTER, y=COL_GPA,
            markers=True,
            title=f"{student_id.upper()} — GPA Trend Across Semesters",
            labels={COL_SEMESTER: "Semester", COL_GPA: "GPA"},
            color_discrete_sequence=["#1A56DB"]
        )
        if c_gpa:
            fig_trend.add_hline(
                y=c_gpa, line_dash="dot", line_color="#E53E3E",
                annotation_text=f"Class avg: {fmt(c_gpa, 2)}",
                annotation_position="top right"
            )
        fig_trend.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[0, 4.2], gridcolor="#F0F4F8"),
            title_font_size=15
        )
        st.plotly_chart(fig_trend, use_container_width=True)
