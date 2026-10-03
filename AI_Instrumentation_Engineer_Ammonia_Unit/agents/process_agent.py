def analyze_process(snapshot, history_df, active_fault):
    result = {"assessment": "No active fault", "evidence": []}

    if not active_fault:
        return result

    tag = active_fault["instrument"]

    if tag in ("PT-101", "PT-102"):
        delta = abs(snapshot["PT-101"] - snapshot["PT-102"])
        result["assessment"] = "Pressure measurements should be cross-checked."
        result["evidence"].append(
            f"PT-101/PT-102 difference is approximately {delta:.2f} bar."
        )

    elif tag == "FT-101":
        result["assessment"] = "Feed-flow behavior should be compared with valve position and process pressure."
        result["evidence"].append("FT-101 is a key feed-flow measurement.")

    elif tag == "TT-101":
        result["assessment"] = "Temperature should be checked against process behavior and redundant indications if available."
        result["evidence"].append("TT-101 is the reactor temperature indication.")

    elif tag == "LT-101":
        result["assessment"] = "Separator level should be cross-checked against process conditions."
        result["evidence"].append("LT-101 is the separator level indication.")

    elif tag == "AT-101":
        result["assessment"] = "Analyzer readings should be validated against analyzer health and process conditions."
        result["evidence"].append("AT-101 is an ammonia concentration analyzer.")

    return result
