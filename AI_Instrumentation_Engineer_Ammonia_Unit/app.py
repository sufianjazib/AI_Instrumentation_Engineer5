import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from simulation.ammonia_process import AmmoniaProcess
from simulation.fault_injection import FAULTS
from agents.orchestrator import run_diagnosis

st.set_page_config(
    page_title="AI Instrumentation Engineer - Ammonia Unit",
    page_icon="🤖",
    layout="wide",
)

@st.cache_resource
def get_process():
    return AmmoniaProcess()

process = get_process()

st.title("🤖 AI Instrumentation Engineer")
st.caption("Multi-agent instrumentation diagnostics for a virtual ammonia unit")

with st.sidebar:
    st.header("⚙️ Simulation Controls")
    instrument = st.selectbox("Instrument", list(FAULTS.keys()))
    fault = st.selectbox("Fault", FAULTS[instrument])
    severity = st.slider("Fault severity", 0.1, 1.0, 0.7, 0.1)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ Run Process", use_container_width=True):
            process.step()
    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            process.reset()
            st.rerun()

    if st.button("💥 Inject Fault", use_container_width=True):
        process.inject_fault(instrument, fault, severity)
        st.success(f"{fault} injected into {instrument}")

    st.divider()
    st.info(
        "Demo system only. It is not a safety instrumented system (SIS), "
        "control system, or substitute for plant procedures."
    )

snapshot = process.snapshot()
df = process.history_df()

# Header status
status = "🔴 FAULT INJECTED" if process.active_fault else "🟢 NORMAL"
st.subheader(f"Ammonia Unit Status: {status}")

cols = st.columns(5)
metrics = [
    ("Reactor Pressure", snapshot["PT-101"], "bar"),
    ("Reactor Temperature", snapshot["TT-101"], "°C"),
    ("Feed Gas Flow", snapshot["FT-101"], "t/h"),
    ("Separator Level", snapshot["LT-101"], "%"),
    ("NH₃ Analyzer", snapshot["AT-101"], "%"),
]
for col, (name, value, unit) in zip(cols, metrics):
    col.metric(name, f"{value:.2f} {unit}")

st.divider()

left, right = st.columns([1.35, 1])

with left:
    st.subheader("📈 Instrument Trends")
    fig = go.Figure()
    for tag in ["PT-101", "PT-102"]:
        fig.add_trace(go.Scatter(
            x=df["time"], y=df[tag], mode="lines", name=tag
        ))
    fig.update_layout(
        height=350,
        xaxis_title="Simulation step",
        yaxis_title="Pressure (bar)",
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure()
    for tag in ["TT-101", "FT-101", "LT-101"]:
        fig2.add_trace(go.Scatter(
            x=df["time"], y=df[tag], mode="lines", name=tag
        ))
    fig2.update_layout(
        height=350,
        xaxis_title="Simulation step",
        yaxis_title="Normalized process value",
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("🔧 Instrument Health")
    health = []
    for tag in ["PT-101", "PT-102", "TT-101", "FT-101", "LT-101", "AT-101"]:
        abnormal = process.is_abnormal(tag)
        health.append({
            "Tag": tag,
            "Status": "🔴 Abnormal" if abnormal else "🟢 Normal",
            "Value": round(snapshot[tag], 2),
        })
    st.dataframe(pd.DataFrame(health), hide_index=True, use_container_width=True)

    st.subheader("🤖 AI Multi-Agent Diagnosis")
    if st.button("🔍 Run AI Diagnosis", type="primary", use_container_width=True):
        with st.spinner("Agents analyzing process and instrument evidence..."):
            result = run_diagnosis(snapshot, df, process.active_fault)

        st.markdown("### Diagnosis")
        st.write(result["diagnosis"])
        st.metric("Confidence", f'{result["confidence"]}%')

        st.markdown("### Evidence")
        for item in result["evidence"]:
            st.write(f"• {item}")

        st.markdown("### Troubleshooting")
        for i, step in enumerate(result["troubleshooting"], 1):
            st.write(f"**{i}.** {step}")

        st.markdown("### 🛡️ Safety Review")
        st.warning(result["safety"])

        if result.get("llm_reasoning"):
            with st.expander("Groq AI response"):
                st.write(result["llm_reasoning"])

st.divider()
st.caption(
    "Architecture: Monitoring Agent → Process Agent → Diagnostics Agent → "
    "Troubleshooting Agent → Safety Agent → Groq LLM"
)
