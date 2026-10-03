```python
# ---------------------------------------------------------------------
# Theme / UI — LIGHT / WHITE
# ---------------------------------------------------------------------
st.markdown("""
<style>
:root {
    --bg: #ffffff;
    --panel: #ffffff;
    --panel2: #f8fafc;
    --line: #d9e2ec;
    --text: #172033;
    --muted: #64748b;
    --green: #16a34a;
    --cyan: #0284c7;
    --yellow: #d97706;
    --red: #dc2626;
    --purple: #7c3aed;
}

/* Main application */
.stApp {
    background: #ffffff !important;
    color: #172033 !important;
}

/* Main content */
.main {
    background: #ffffff !important;
}

.block-container {
    background: #ffffff !important;
    padding-top: 0.7rem;
    max-width: 1600px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f8fafc !important;
    border-right: 1px solid #d9e2ec;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
    background: #f8fafc !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: #172033;
}

/* Small text */
.small-muted {
    color: #64748b;
    font-size: 0.78rem;
}

/* Top bar */
.topbar {
    background: linear-gradient(90deg, #f8fafc, #ffffff);
    border: 1px solid #d9e2ec;
    border-radius: 10px;
    padding: 9px 14px;
    margin-bottom: 8px;
}

.top-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: #172033;
}

.top-sub {
    color: #64748b;
    font-size: 0.72rem;
    margin-top: 2px;
}

/* Status */
.status-pill {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
}

.green {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}

.red {
    background: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
}

/* Main panels */
.panel {
    background: #ffffff;
    border: 1px solid #d9e2ec;
    border-radius: 9px;
    padding: 10px 12px;
    margin-bottom: 9px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}

.panel-title {
    color: #172033;
    font-size: 0.84rem;
    font-weight: 700;
    padding-bottom: 7px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 8px;
}

/* Tags */
.tag {
    display: inline-block;
    border: 1px solid #bae6fd;
    background: #f0f9ff;
    color: #0369a1;
    border-radius: 5px;
    padding: 2px 5px;
    font-size: 0.65rem;
    margin-right: 3px;
}

/* Values */
.value {
    color: #172033;
    font-size: 1.25rem;
    font-weight: 700;
}

.unit {
    color: #64748b;
    font-size: 0.67rem;
}

.health-ok {
    color: #15803d;
    font-weight: 700;
}

.health-bad {
    color: #dc2626;
    font-weight: 700;
}

/* Equipment blocks */
.eq {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 7px 8px;
    min-width: 108px;
    text-align: center;
}

.eq-name {
    color: #172033;
    font-size: 0.72rem;
    font-weight: 700;
}

.eq-sub {
    color: #64748b;
    font-size: 0.58rem;
    margin-top: 2px;
}

.eq-value {
    color: #0284c7;
    font-size: 0.72rem;
    margin-top: 4px;
}

/* Process vessel */
.vessel {
    background: linear-gradient(180deg, #e0f2fe, #f0f9ff);
    border: 2px solid #38bdf8;
    border-radius: 24px 24px 18px 18px;
    min-width: 145px;
    min-height: 112px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 0 25px rgba(14, 165, 233, 0.08);
}

.vessel .name {
    font-weight: 800;
    font-size: 0.78rem;
    color: #172033;
}

.vessel .contents {
    color: #0284c7;
    font-size: 0.65rem;
    margin-top: 4px;
}

/* Pipes */
.pipe {
    color: #0284c7;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
}

/* Instruments */
.instrument {
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    background: #f8fafc;
    padding: 5px 7px;
    min-width: 78px;
    text-align: center;
}

.instrument .it {
    font-size: 0.62rem;
    color: #64748b;
}

.instrument .iv {
    font-size: 0.78rem;
    font-weight: 700;
    color: #172033;
}

.instrument.ok {
    border-color: #86efac;
    background: #f0fdf4;
}

.instrument.bad {
    border-color: #fca5a5;
    background: #fef2f2;
}

/* AI workflow */
.workflow {
    border-left: 3px solid #0284c7;
    padding: 7px 10px;
    margin: 6px 0;
    background: #f8fafc;
    border-radius: 0 7px 7px 0;
}

.workflow .wtitle {
    font-weight: 700;
    font-size: 0.72rem;
    color: #172033;
}

.workflow .wtext {
    font-size: 0.65rem;
    color: #64748b;
    margin-top: 3px;
}

/* Engineering report */
.report {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px;
    font-size: 0.72rem;
    color: #172033;
}

/* Warning */
.warning {
    background: #fffbeb;
    border: 1px solid #fbbf24;
    color: #92400e;
    border-radius: 7px;
    padding: 8px;
    font-size: 0.68rem;
}

/* Streamlit metrics */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d9e2ec;
    border-radius: 8px;
    padding: 7px 9px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

div[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {
    font-size: 1.12rem !important;
    color: #172033 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #d9e2ec;
    border-radius: 8px;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #475569 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #0284c7 !important;
}

/* Buttons */
.stButton > button {
    background: #ffffff;
    color: #172033;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
}

.stButton > button:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
}

/* Primary buttons */
button[kind="primary"] {
    background: #0284c7 !important;
    color: #ffffff !important;
    border-color: #0284c7 !important;
}

button[kind="primary"]:hover {
    background: #0369a1 !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #172033 !important;
    border-color: #cbd5e1 !important;
}

/* Select boxes */
div[data-baseweb="select"] {
    background: #ffffff !important;
}

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #172033 !important;
    border-color: #cbd5e1 !important;
}

/* Slider */
div[data-testid="stSlider"] {
    color: #0284c7;
}

/* Expander */
details {
    background: #ffffff !important;
    border: 1px solid #d9e2ec !important;
}

summary {
    color: #172033 !important;
}

/* Dividers */
hr {
    border-color: #e2e8f0 !important;
}

</style>
""", unsafe_allow_html=True)
```
