def analyze_monitoring(snapshot, history_df, active_fault):
    result = {"abnormal": False, "signals": []}

    if not active_fault:
        return result

    result["abnormal"] = True
    tag = active_fault["instrument"]
    fault = active_fault["fault"]
    result["signals"].append(f"{tag} has an injected {fault} condition.")

    if len(history_df) >= 5:
        recent = history_df[tag].tail(5)
        if recent.max() - recent.min() < 0.01:
            result["signals"].append(f"{tag} has remained effectively constant.")
        else:
            result["signals"].append(f"{tag} shows a changing signal trend.")

    return result
