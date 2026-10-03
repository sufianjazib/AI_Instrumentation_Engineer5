import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from simulation.ammonia_process import AmmoniaProcess
from simulation.fault_injection import FAULTS
from agents.orchestrator import run_diagnosis

st.set_page_config(
    page_title="AI Instrumentation Engineer — Ammonia Unit",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Theme / UI
# ---------------------------------------------------------------------
st.markdown("""
<style>
:root {
    --bg: #06111d;
    --panel: #0b1b2b;
    --panel2: #0e2437;
    --line: #24445c;
    --text: #dbeafe;
    --muted: #7892a8;
    --green: #27e08a;
    --cyan: #29b6f6;
    --yellow: #ffc857;
    --red: #ff5b67;
    --purple: #9b7bff;
}
.stApp { background: #050e17; color: var(--text); }
.block-container { padding-top: 0.7rem; max-width: 1600px; }
section[data-testid="stSidebar"] {
    background: #061522;
    border-right: 1px solid #16334a;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
.small-muted { color: #7892a8; font-size: 0.78rem; }
.topbar {
    background: linear-gradient(90deg,#071a2b,#0a2033);
    border: 1px solid #183a54;
    border-radius: 10px;
    padding: 9px 14px;
    margin-bottom: 8px;
}
.top-title { font-size: 1.02rem; font-weight: 700; color: #e7f3ff; }
.top-sub { color:#7e9bb0; font-size:0.72rem; margin-top:2px; }
.status-pill {
    display:inline-block; padding:4px 9px; border-radius:20px;
    font-size:0.72rem; font-weight:700;
}
.green { background:#0a3828; color:#45ef9c; border:1px solid #1b8f63; }
.red { background:#421b21; color:#ff7b84; border:1px solid #a83d49; }
.panel {
    background: linear-gradient(180deg,#0b1c2d,#091725);
    border:1px solid #183a54;
    border-radius:9px;
    padding:10px 12px;
    margin-bottom:9px;
}
.panel-title {
    color:#dceeff; font-size:0.84rem; font-weight:700;
    padding-bottom:7px; border-bottom:1px solid #17354c;
    margin-bottom:8px;
}
.tag {
    display:inline-block; border:1px solid #24506b; background:#0a2132;
    color:#9edcff; border-radius:5px; padding:2px 5px; font-size:0.65rem;
    margin-right:3px;
}
.value { color:#e9f5ff; font-size:1.25rem; font-weight:700; }
.unit { color:#7892a8; font-size:0.67rem; }
.health-ok { color:#39e994; font-weight:700; }
.health-bad { color:#ff6975; font-weight:700; }
.eq {
    background:#0c2537; border:1px solid #27516b; border-radius:8px;
    padding:7px 8px; min-width:108px; text-align:center;
}
.eq-name { color:#dceeff; font-size:0.72rem; font-weight:700; }
.eq-sub { color:#7393a8; font-size:0.58rem; margin-top:2px; }
.eq-value { color:#42dff5; font-size:0.72rem; margin-top:4px; }
.vessel {
    background:linear-gradient(180deg,#123c55,#0b2435);
    border:2px solid #3288aa; border-radius:24px 24px 18px 18px;
    min-width:145px; min-height:112px; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    box-shadow: inset 0 0 25px rgba(34,178,230,.08);
}
.vessel .name {font-weight:800; font-size:.78rem;}
.vessel .contents {color:#56d9ff; font-size:.65rem; margin-top:4px;}
.pipe { color:#35c9ef; font-size:1.4rem; font-weight:700; text-align:center; }
.instrument {
    border:1px solid #315a72; border-radius:7px; background:#081a29;
    padding:5px 7px; min-width:78px; text-align:center;
}
.instrument .it {font-size:.62rem; color:#82a4b8;}
.instrument .iv {font-size:.78rem; font-weight:700; color:#e8f7ff;}
.instrument.ok {border-color:#207c58;}
.instrument.bad {border-color:#9b3946; background:#2a1117;}
.workflow {
    border-left:3px solid #24617e; padding:7px 10px; margin:6px 0;
    background:#091b2a; border-radius:0 7px 7px 0;
}
.workflow .wtitle {font-weight:700; font-size:.72rem;}
.workflow .wtext {font-size:.65rem; color:#91aabd; margin-top:3px;}
.report {
    background:#0a1c2a; border:1px solid #31546a; border-radius:8px;
    padding:10px; font-size:.72rem;
}
.warning {
    background:#382d10; border:1px solid #8d6f21; color:#f4d27b;
    border-radius:7px; padding:8px; font-size:.68rem;
}
div[data-testid="stMetric"] {
    background:#0b1c2b; border:1px solid #173b54;
    border-radius:8px; padding:7px 9px;
}
div[data-testid="stMetricLabel"] { font-size:.68rem !important; }
div[data-testid="stMetricValue"] { font-size:1.12rem !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_process():
    return AmmoniaProcess()

process = get_process()
snapshot = process.snapshot()
df = process.history_df()

# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ AI INSTRUMENTATION")
    st.caption("Ammonia Unit — Virtual Plant Diagnostics")
    page = st.radio(
        "MAIN NAVIGATION",
        ["Overview", "Process View", "AI Diagnosis", "Engineering Report", "Knowledge Base"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**PROCESS CONTROL**")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ Run", use_container_width=True):
            process.step()
            st.rerun()
    with c2:
        if st.button("↻ Reset", use_container_width=True):
            process.reset()
            st.rerun()

    if st.button("⚠ Inject Fault", use_container_width=True):
        st.session_state["show_fault"] = True

    if st.session_state.get("show_fault", False):
        instrument = st.selectbox("Instrument", list(FAULTS.keys()))
        fault = st.selectbox("Fault", FAULTS[instrument])
        severity = st.slider("Severity", 0.1, 1.0, 0.7, 0.1)
        if st.button("Inject selected fault", type="primary", use_container_width=True):
            process.inject_fault(instrument, fault, severity)
            st.session_state["show_fault"] = False
            st.success(f"{fault} → {instrument}")
            st.rerun()

    st.divider()
    st.markdown("**INSTRUMENTS**")
    for tag in ["PT-101", "PT-102", "TT-101", "FT-101", "LT-101", "AT-101"]:
        status = "🔴" if process.is_abnormal(tag) else "🟢"
        st.caption(f"{status} {tag}")

    st.divider()
    st.caption("Training / demonstration simulator")
    st.caption("Not a SIS, DCS or plant safety system.")

# ---------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------
status = "FAULT DETECTED" if process.active_fault else "PLANT SIMULATION ONLINE"
status_cls = "red" if process.active_fault else "green"

st.markdown(f"""
<div class="topbar">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div class="top-title">⚙️ AI INSTRUMENTATION ENGINE — Stage 2</div>
      <div class="top-sub">Ammonia Unit | Multi-Agent Instrument Fault Detection & Troubleshooting</div>
    </div>
    <div>
      <span class="status-pill {status_cls}">● {status}</span>
      <span class="small-muted" style="margin-left:10px;">Simulation Step {process.step_no}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Plant overview / P&ID-like display
# ---------------------------------------------------------------------
st.markdown('<div class="panel"><div class="panel-title">🏭 Plant Overview — Ammonia Synthesis / Reactor Train</div>', unsafe_allow_html=True)

# Equipment row
eq_html = f"""
<div style="display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;">
  <div class="eq">
    <div class="eq-name">FEED GAS</div>
    <div class="eq-sub">Raw synthesis gas</div>
    <div class="eq-value">FT-101 → {snapshot["FT-101"]:.1f} t/h</div>
  </div>
  <div class="pipe">➜</div>
  <div class="eq">
    <div class="eq-name">COMPRESSOR</div>
    <div class="eq-sub">Synthesis gas</div>
    <div class="eq-value">CV / speed control</div>
  </div>
  <div class="pipe">➜</div>

  <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
    <div class="instrument {'bad' if process.is_abnormal('PT-101') else 'ok'}">
      <div class="it">PRESSURE</div>
      <div class="iv">PT-101</div>
      <div class="iv">{snapshot["PT-101"]:.1f} bar</div>
    </div>
    <div class="vessel">
      <div class="name">AMMONIA CONVERTER</div>
      <div class="contents">H₂ + N₂ → NH₃</div>
      <div class="contents">TT-101: {snapshot["TT-101"]:.1f} °C</div>
    </div>
  </div>

  <div class="pipe">➜</div>
  <div class="eq">
    <div class="eq-name">COOLER / CONDENSER</div>
    <div class="eq-sub">NH₃ condensation</div>
    <div class="eq-value">PV-101 control</div>
  </div>
  <div class="pipe">➜</div>

  <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
    <div class="instrument {'bad' if process.is_abnormal('LT-101') else 'ok'}">
      <div class="it">LEVEL</div>
      <div class="iv">LT-101</div>
      <div class="iv">{snapshot["LT-101"]:.1f} %</div>
    </div>
    <div class="eq">
      <div class="eq-name">SEPARATOR</div>
      <div class="eq-sub">NH₃ / gas separation</div>
      <div class="eq-value">LV-101</div>
    </div>
  </div>

  <div class="pipe">➜</div>
  <div class="eq">
    <div class="eq-name">NH₃ PRODUCT</div>
    <div class="eq-sub">Product outlet</div>
    <div class="eq-value">AT-101: {snapshot["AT-101"]:.1f} %</div>
  </div>
</div>

<div style="display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin-top:12px;">
  <div class="instrument {'bad' if process.is_abnormal('PT-101') else 'ok'}">
    <div class="it">REACTOR PRESSURE</div><div class="iv">PT-101</div>
    <div class="iv">{snapshot["PT-101"]:.2f} bar</div>
  </div>
  <div class="instrument {'bad' if process.is_abnormal('PT-102') else 'ok'}">
    <div class="it">REDUNDANT PRESSURE</div><div class="iv">PT-102</div>
    <div class="iv">{snapshot["PT-102"]:.2f} bar</div>
  </div>
  <div class="instrument {'bad' if process.is_abnormal('TT-101') else 'ok'}">
    <div class="it">REACTOR TEMPERATURE</div><div class="iv">TT-101</div>
    <div class="iv">{snapshot["TT-101"]:.2f} °C</div>
  </div>
  <div class="instrument {'bad' if process.is_abnormal('FT-101') else 'ok'}">
    <div class="it">FEED FLOW</div><div class="iv">FT-101</div>
    <div class="iv">{snapshot["FT-101"]:.2f} t/h</div>
  </div>
  <div class="instrument {'bad' if process.is_abnormal('AT-101') else 'ok'}">
    <div class="it">NH₃ ANALYZER</div><div class="iv">AT-101</div>
    <div class="iv">{snapshot["AT-101"]:.2f} %</div>
  </div>
</div>
"""
st.markdown(eq_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Key process parameters + instrument health
# ---------------------------------------------------------------------
left, right = st.columns([1.55, 1])

with left:
    st.markdown('<div class="panel"><div class="panel-title">📊 Key Process Parameters</div>', unsafe_allow_html=True)
    cols = st.columns(6)
    params = [
        ("Level", "LT-101", snapshot["LT-101"], "%"),
        ("Pressure", "PT-101", snapshot["PT-101"], "bar"),
        ("Temperature", "TT-101", snapshot["TT-101"], "°C"),
        ("Flow", "FT-101", snapshot["FT-101"], "t/h"),
        ("Valve", "PV-101", 68, "%"),
        ("Analyzer", "AT-101", snapshot["AT-101"], "% NH₃"),
    ]
    for col, (name, tag, value, unit) in zip(cols, params):
        with col:
            st.metric(f"{name} ({tag})", f"{value:.1f}", unit)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">🩺 Instrument Health</div>', unsafe_allow_html=True)
    health_rows = []
    for tag, desc, unit in [
        ("PT-101", "Pressure", "bar"),
        ("PT-102", "Pressure", "bar"),
        ("TT-101", "Temperature", "°C"),
        ("FT-101", "Flow", "t/h"),
        ("LT-101", "Level", "%"),
        ("AT-101", "Analyzer", "%"),
    ]:
        abnormal = process.is_abnormal(tag)
        health_rows.append({
            "Instrument": tag,
            "PV": f'{snapshot[tag]:.2f} {unit}',
            "Signal": "4–20 mA",
            "Health": "⚠ Abnormal" if abnormal else "● Normal",
        })
    st.dataframe(pd.DataFrame(health_rows), hide_index=True, use_container_width=True, height=245)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Trends + AI workflow
# ---------------------------------------------------------------------
left, right = st.columns([1.25, 1])

with left:
    st.markdown('<div class="panel"><div class="panel-title">📈 Process Trends — Live Simulation</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Pressure", "Temperature / Flow", "Level / Analyzer"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["PT-101"], name="PT-101", mode="lines"))
        fig.add_trace(go.Scatter(x=df["time"], y=df["PT-102"], name="PT-102", mode="lines"))
        fig.update_layout(height=240, margin=dict(l=5,r=5,t=5,b=5), template="plotly_dark",
                          yaxis_title="bar", xaxis_title="Step")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["TT-101"], name="TT-101", mode="lines"))
        fig.add_trace(go.Scatter(x=df["time"], y=df["FT-101"], name="FT-101", mode="lines", yaxis="y2"))
        fig.update_layout(height=240, margin=dict(l=5,r=5,t=5,b=5), template="plotly_dark",
                          yaxis_title="Temperature °C",
                          yaxis2=dict(title="Flow t/h", overlaying="y", side="right"),
                          xaxis_title="Step")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["LT-101"], name="LT-101", mode="lines"))
        fig.add_trace(go.Scatter(x=df["time"], y=df["AT-101"], name="AT-101", mode="lines"))
        fig.update_layout(height=240, margin=dict(l=5,r=5,t=5,b=5), template="plotly_dark",
                          yaxis_title="Value", xaxis_title="Step")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">🧠 AI Analysis — Multi-Agent Workflow</div>', unsafe_allow_html=True)

    workflow = [
        ("🟢", "1. Diagnostic Engineer", "Monitoring and signal abnormality detection"),
        ("🔵", "2. Process Engineer", "Cross-checks process behavior and redundant measurements"),
        ("🟣", "3. Instrumentation Engineer", "Identifies probable transmitter/sensor fault"),
        ("🟠", "4. Root Cause Engineer", "Builds evidence chain and probable cause"),
        ("🟢", "5. Troubleshooting Engineer", "Generates technician-oriented checks"),
        ("🔵", "6. Safety Review", "Screens recommendations against plant safeguards"),
    ]
    for icon, title, text in workflow:
        st.markdown(
            f'<div class="workflow"><div class="wtitle">{icon} {title}</div>'
            f'<div class="wtext">{text}</div></div>',
            unsafe_allow_html=True
        )

    if st.button("🔍 Run Multi-Agent Diagnosis", type="primary", use_container_width=True):
        with st.spinner("Running monitoring → process → diagnostics → troubleshooting → safety agents..."):
            result = run_diagnosis(snapshot, df, process.active_fault)
        st.session_state["diagnosis_result"] = result

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Engineering report
# ---------------------------------------------------------------------
result = st.session_state.get("diagnosis_result")

st.markdown('<div class="panel"><div class="panel-title">🧾 AI Engineering Report</div>', unsafe_allow_html=True)

if result:
    c1, c2 = st.columns([2.0, 1])
    with c1:
        st.markdown(f"""
        <div class="report">
        <b>Instrument / Fault Finding</b><br>
        {result["diagnosis"]}<br><br>
        <b>Evidence</b><br>
        {"<br>".join("• " + x for x in result["evidence"])}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.metric("AI Confidence", f'{result["confidence"]}%')
        st.metric("Active Fault", "YES" if process.active_fault else "NO")

    st.markdown("**Recommended troubleshooting sequence**")
    for i, step in enumerate(result["troubleshooting"], 1):
        st.write(f"**{i}.** {step}")

    st.warning(result["safety"])

    if result.get("llm_reasoning"):
        with st.expander("View Groq reasoning / explanation"):
            st.write(result["llm_reasoning"])
else:
    st.markdown(
        '<div class="report">No diagnosis has been run yet. '
        'Inject a fault from the sidebar, run the virtual process, then click '
        '<b>Run Multi-Agent Diagnosis</b>.</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="warning">
⚠ <b>Engineering disclaimer:</b> This application is a virtual training/demo
environment. It must not be used to control an operating ammonia plant or to
override alarms, interlocks, SIS functions, permits, isolation/LOTO, gas
detection, PPE requirements, or qualified-person procedures.
</div>
""", unsafe_allow_html=True)
