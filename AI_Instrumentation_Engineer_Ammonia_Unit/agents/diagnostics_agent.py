def diagnose_instrument(snapshot, history_df, monitoring, process, active_fault):
    if not active_fault:
        return {
            "fault": "No active instrument fault detected",
            "confidence": 95,
            "evidence": ["The virtual plant currently has no injected fault."],
        }

    tag = active_fault["instrument"]
    fault = active_fault["fault"]

    mapping = {
        "Stuck transmitter": "Possible transmitter output freeze / signal stuck condition",
        "Signal drift": "Possible transmitter calibration drift or sensor drift",
        "Noisy signal": "Possible electrical noise, grounding issue, sensor instability, or transmitter problem",
        "Zero / low signal": "Possible loss of signal, wiring/power issue, transmitter failure, or sensor fault",
        "High signal": "Possible transmitter bias, calibration error, or sensor fault",
        "Impulse-line blockage": "Possible pressure measurement restriction or blocked impulse line",
        "Analyzer bias": "Possible analyzer calibration or sample-system bias",
        "Valve stuck": "Possible control-valve mechanical problem affecting the process",
    }

    evidence = list(monitoring["signals"]) + list(process["evidence"])
    confidence = min(96, 72 + int(active_fault["severity"] * 20))

    return {
        "fault": f"{tag}: {mapping.get(fault, fault)}",
        "confidence": confidence,
        "evidence": evidence,
    }
