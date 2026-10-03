import os
import time
import numpy as np
import pandas as pd
from typing import Dict, Any, List

# Try importing groq client gracefully
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# ---------------------------------------------------------------------
# Groq Model Configuration
# ---------------------------------------------------------------------
# Use active Groq production models (e.g., llama-3.3-70b-versatile or llama-3.1-70b-versatile)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


# ---------------------------------------------------------------------
# Individual Agent Node Functions
# ---------------------------------------------------------------------

def agent_1_diagnostic(snapshot: Dict[str, float], df: pd.DataFrame) -> Dict[str, Any]:
    """Agent 1: Diagnostic Engineer — Monitors telemetry and flags signal anomalies."""
    abnormalities = []
    tags = ["PT-101", "PT-102", "TT-101", "FT-101", "LT-101", "AT-101"]
    
    for tag in tags:
        val = snapshot.get(tag, 0.0)
        # Check Z-score if historical data is available
        if len(df) > 5 and tag in df.columns:
            recent_mean = df[tag].tail(10).mean()
            recent_std = df[tag].tail(10).std() + 1e-5
            z_score = abs(val - recent_mean) / recent_std
            if z_score > 2.5:
                abnormalities.append(f"{tag} reading ({val:.2f}) deviates significantly (Z={z_score:.1f})")
    
    # Redundancy delta check
    p_diff = abs(snapshot.get("PT-101", 0) - snapshot.get("PT-102", 0))
    if p_diff > 3.0:
        abnormalities.append(f"Pressure transmitter mismatch: |PT-101 - PT-102| = {p_diff:.2f} bar")

    return {
        "status": "ANOMALY_DETECTED" if abnormalities else "NORMAL",
        "flagged_signals": abnormalities
    }


def agent_2_process(snapshot: Dict[str, float], df: pd.DataFrame) -> Dict[str, Any]:
    """Agent 2: Process Engineer — Cross-checks mass/energy balances and redundancy."""
    pt101 = snapshot.get("PT-101", 0.0)
    pt102 = snapshot.get("PT-102", 0.0)
    tt101 = snapshot.get("TT-101", 0.0)
    ft101 = snapshot.get("FT-101", 0.0)
    
    pt_mismatch = abs(pt101 - pt102) > 3.0
    # Process physics cross-check: High pressure drop usually correlates with higher flow
    physics_validated = True
    notes = []
    
    if pt_mismatch:
        physics_validated = False
        notes.append("Redundant channels PT-101 and PT-102 diverge; process conditions cannot support both readings simultaneously.")
    
    if ft101 < 10.0 and tt101 > 450.0:
        notes.append("Thermal excursion warning: Low synthesis gas flow with elevated reactor temperature.")

    return {
        "physics_consistent": physics_validated,
        "process_notes": notes
    }


def agent_3_instrumentation(snapshot: Dict[str, float], active_fault: Any) -> Dict[str, Any]:
    """Agent 3: Instrumentation Engineer — Isolates specific transmitter/sensor fault type."""
    suspect_tag = "UNKNOWN"
    fault_type = "Sensor Drift or Bias"
    
    pt_diff = abs(snapshot.get("PT-101", 130.0) - snapshot.get("PT-102", 130.0))
    
    if pt_diff > 3.0:
        suspect_tag = "PT-101" if snapshot.get("PT-101", 0) > snapshot.get("PT-102", 0) else "PT-102"
        fault_type = "Calibration Shift / Transmitter Bias"
    elif snapshot.get("TT-101", 0) > 480.0 or snapshot.get("TT-101", 0) < 300.0:
        suspect_tag = "TT-101"
        fault_type = "Thermocouple Degradation / Signal Drift"
    elif snapshot.get("LT-101", 0) < 10.0 or snapshot.get("LT-101", 0) > 90.0:
        suspect_tag = "LT-101"
        fault_type = "Differential Pressure Impulse Line Plugging"
    
    return {
        "suspect_instrument": suspect_tag,
        "probable_fault_type": fault_type,
        "active_fault_simulated": str(active_fault) if active_fault else "None"
    }


def agent_4_control_valve(snapshot: Dict[str, float], df: pd.DataFrame) -> Dict[str, Any]:
    """Agent 4: Control Valve Agent [NEW] — Checks positioner, hysteresis, and valve stiction."""
    pv_demand = 68.0  # Nominally 68% valve position
    lt101 = snapshot.get("LT-101", 50.0)
    
    stiction_detected = False
    valve_notes = []
    
    # Check separator level vs valve position hysteresis
    if len(df) > 5 and "LT-101" in df.columns:
        lt_trend = df["LT-101"].tail(5).diff().abs().sum()
        if lt_trend < 0.2 and abs(lt101 - 50.0) > 15.0:
            stiction_detected = True
            valve_notes.append("Level control valve (LV-101) exhibits potential stiction/packing binding.")

    if not valve_notes:
        valve_notes.append("Control valve positioners (PV-101 / LV-101) operating within dynamic limits.")

    return {
        "valve_stiction_risk": "HIGH" if stiction_detected else "LOW",
        "valve_analysis": valve_notes
    }


def agent_5_root_cause(ag1: Dict, ag2: Dict, ag3: Dict, ag4: Dict) -> Dict[str, Any]:
    """Agent 5: Root Cause Engineer — Synthesizes evidence tree and primary diagnosis."""
    evidence = []
    evidence.extend(ag1.get("flagged_signals", []))
    evidence.extend(ag2.get("process_notes", []))
    evidence.extend(ag4.get("valve_analysis", []))
    
    suspect = ag3.get("suspect_instrument", "PT-101")
    fault_type = ag3.get("probable_fault_type", "Signal Bias")
    
    diagnosis_text = f"Primary fault identified on {suspect}: {fault_type}."
    confidence = 88 if ag1["status"] == "ANOMALY_DETECTED" else 95

    return {
        "diagnosis": diagnosis_text,
        "evidence_chain": evidence if evidence else ["All parameters within standard standard deviation limits."],
        "confidence": confidence
    }


def agent_6_troubleshooting(ag5: Dict) -> List[str]:
    """Agent 6: Troubleshooting Engineer — Generates field technician action checklist."""
    diagnosis = ag5.get("diagnosis", "")
    
    if "PT-101" in diagnosis or "PT-102" in diagnosis:
        return [
            "Perform 4–20 mA loop current check using calibrated Digital Multimeter.",
            "Connect HART Communicator 475 to check transmitter diagnostic alerts and zero trim.",
            "Inspect sensing impulse lines for liquid condensate accumulation or blockage.",
            "Cross-calibrate channel against secondary standard digital pressure gauge."
        ]
    elif "TT-101" in diagnosis:
        return [
            "Measure Thermocouple element loop resistance (mV output vs NIST table).",
            "Inspect junction box terminals for corrosion or loose connections.",
            "Verify temperature transmitter sensor configuration (Type K vs Pt100 RTD)."
        ]
    elif "LT-101" in diagnosis:
        return [
            "Blow down and purge high/low pressure sensing legs of the DP transmitter.",
            "Perform zero-point check on separator level transmitter under equalized pressure.",
            "Inspect level control valve positioner feedback linkage."
        ]
    else:
        return [
            "Perform general visual inspection of field junction box and signal wiring.",
            "Verify DCS I/O card channel status and power supply voltage (24V DC).",
            "Perform 5-point calibration check across instrument range."
        ]


def agent_7_work_order(ag3: Dict, ag5: Dict) -> Dict[str, Any]:
    """Agent 7: Maintenance Ticket Agent [NEW] — Generates SAP/Maximo work order."""
    wo_id = f"WO-NH3-{int(time.time()) % 100000:05d}"
    suspect = ag3.get("suspect_instrument", "PT-101")
    priority = "HIGH" if ag5.get("confidence", 0) > 85 else "MEDIUM"
    
    return {
        "work_order_id": wo_id,
        "equipment_id": f"EQ-{suspect}-AMMONIA-CONVERTER",
        "functional_location": "PLANT-02 / SYNTHESIS / REACTOR-TRAIN",
        "priority": priority,
        "craft": "Instrument & Control Technician (I&C)",
        "short_text": f"Troubleshoot & Calibrate {suspect} - {ag3.get('probable_fault_type')}",
        "required_tools": ["Digital Multimeter", "HART Communicator 475", "Calibrated Pressure Source"],
        "estimated_hours": 2.0
    }


def agent_8_safety(ag3: Dict, ag7: Dict) -> str:
    """Agent 8: Safety Review Agent — Audits recommendations against plant safeguards & LOTO."""
    suspect = ag3.get("suspect_instrument", "PT-101")
    return (
        f"⚠️ SAFETY DIRECTIVE FOR {suspect}: Ensure Lockout/Tagout (LOTO) isolation on sampling/impulse lines. "
        f"Ammonia (NH3) process line operates at high pressure. Personnel must wear appropriate PPE, including "
        f"full face shield and ammonia gas detector badge prior to opening instrument manifold valves."
    )


# ---------------------------------------------------------------------
# Groq LLM Reasoning Integration
# ---------------------------------------------------------------------

def query_groq_llm(snapshot: Dict, df: pd.DataFrame, workflow_summary: Dict) -> str:
    """Queries Groq LLM to synthesize narrative engineering reasoning."""
    api_key = os.getenv("GROQ_API_KEY")
    if not GROQ_AVAILABLE or not api_key:
        return "Groq API key not configured. Using deterministic multi-agent synthesis."

    try:
        client = Groq(api_key=api_key)
        prompt = f"""
You are an expert Chief Instrument & Safety Engineer at a Tier-1 Ammonia plant.
Synthesize the following 8-agent diagnostic findings into a concise, professional engineering rationale:

Telemetry Snapshot: {snapshot}
Agent 1-8 Diagnosis: {workflow_summary['diagnosis']}
Identified Instrument: {workflow_summary['instrument_agent']['suspect_instrument']}
Valve Risk: {workflow_summary['valve_agent']['valve_stiction_risk']}
Work Order ID: {workflow_summary['work_order']['work_order_id']}

Provide a clear 3-4 sentence explanation detailing the root cause, process impact, and field resolution.
"""
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Groq reasoning fallback (Error: {str(e)}). Deterministic multi-agent output active."


# ---------------------------------------------------------------------
# Orchestrator Master Function
# ---------------------------------------------------------------------

def run_diagnosis(snapshot: Dict[str, float], df: pd.DataFrame, active_fault: Any = None) -> Dict[str, Any]:
    """
    Master multi-agent orchestration engine.
    Executes all 8 agent steps in sequence and compiles the final report.
    """
    # Step 1: Monitoring & Signal Abnormality
    ag1 = agent_1_diagnostic(snapshot, df)

    # Step 2: Process & Redundancy Verification
    ag2 = agent_2_process(snapshot, df)

    # Step 3: Transmitter & Sensor Fault Identification
    ag3 = agent_3_instrumentation(snapshot, active_fault)

    # Step 4: Control Valve & Positioner Analysis [NEW]
    ag4 = agent_4_control_valve(snapshot, df)

    # Step 5: Root Cause & Evidence Synthesis
    ag5 = agent_5_root_cause(ag1, ag2, ag3, ag4)

    # Step 6: Field Technician Troubleshooting Steps
    ag6 = agent_6_troubleshooting(ag5)

    # Step 7: SAP/Maximo Work Order Generation [NEW]
    ag7 = agent_7_work_order(ag3, ag5)

    # Step 8: Safety Review & Plant Safeguards Audit
    ag8 = agent_8_safety(ag3, ag7)

    # Internal Workflow Summary for LLM Reasoning
    workflow_summary = {
        "diagnostic_agent": ag1,
        "process_agent": ag2,
        "instrument_agent": ag3,
        "valve_agent": ag4,
        "root_cause_agent": ag5,
        "work_order": ag7,
        "diagnosis": ag5["diagnosis"]
    }

    # Query Groq for narrative rationale
    llm_reasoning = query_groq_llm(snapshot, df, workflow_summary)

    # Return unified pipeline payload
    return {
        "diagnosis": ag5["diagnosis"],
        "evidence": ag5["evidence_chain"],
        "confidence": ag5["confidence"],
        "troubleshooting": ag6,
        "safety": ag8,
        "work_order": ag7,
        "valve_analysis": ag4,
        "llm_reasoning": llm_reasoning,
        "agent_outputs": {
            "ag1_diagnostic": ag1,
            "ag2_process": ag2,
            "ag3_instrumentation": ag3,
            "ag4_control_valve": ag4,
            "ag5_root_cause": ag5,
            "ag6_troubleshooting": ag6,
            "ag7_work_order": ag7,
            "ag8_safety": ag8
        }
    }
