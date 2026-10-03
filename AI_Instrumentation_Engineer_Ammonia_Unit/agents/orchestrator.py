from agents.monitoring_agent import analyze_monitoring
from agents.process_agent import analyze_process
from agents.diagnostics_agent import diagnose_instrument
from agents.troubleshooting_agent import make_troubleshooting
from agents.safety_agent import safety_review
from utils.groq_client import ask_groq

def run_diagnosis(snapshot, history_df, active_fault):
    monitoring = analyze_monitoring(snapshot, history_df, active_fault)
    process = analyze_process(snapshot, history_df, active_fault)
    diagnosis = diagnose_instrument(snapshot, history_df, monitoring, process, active_fault)
    troubleshooting = make_troubleshooting(diagnosis)
    safety = safety_review(diagnosis)

    prompt = f"""
You are an industrial instrumentation diagnostic assistant for a VIRTUAL
ammonia-unit training simulator.

Process snapshot:
{snapshot}

Monitoring analysis:
{monitoring}

Process analysis:
{process}

Probable diagnosis:
{diagnosis}

Give a concise engineering explanation. Do not claim that the simulator
represents a real plant. Do not provide instructions to bypass interlocks,
SIS, alarms, permits, isolation, or other safety systems.
"""
    llm = ask_groq(prompt)

    return {
        "diagnosis": diagnosis["fault"],
        "confidence": diagnosis["confidence"],
        "evidence": diagnosis["evidence"],
        "troubleshooting": troubleshooting,
        "safety": safety,
        "llm_reasoning": llm,
    }
