def make_troubleshooting(diagnosis):
    text = diagnosis["fault"].lower()

    if "stuck" in text or "freeze" in text:
        return [
            "Verify the indicated value against an independent/local indication where available.",
            "Check transmitter status and diagnostic information.",
            "Verify power supply and signal wiring using approved plant procedures.",
            "Check the applicable 4–20 mA signal at the permitted test point.",
            "If required, follow the plant-approved calibration/maintenance procedure.",
        ]

    if "drift" in text:
        return [
            "Compare transmitter indication with an independent reference.",
            "Check transmitter configuration and calibration status.",
            "Inspect sensor and impulse connection condition as applicable.",
            "Perform calibration verification using approved plant procedures.",
            "Document the as-found and as-left condition.",
        ]

    if "noise" in text:
        return [
            "Confirm that the noise is present in the process signal and not only on the display.",
            "Inspect wiring, shielding, grounding and termination according to plant standards.",
            "Check nearby electrical equipment for possible interference.",
            "Review transmitter diagnostics and signal quality.",
            "Retest after corrective action.",
        ]

    if "zero / low" in text or "low signal" in text:
        return [
            "Verify local indication and alarm status.",
            "Check transmitter power and wiring using approved procedures.",
            "Measure the signal at the appropriate permitted test point.",
            "Check sensor/transmitter condition.",
            "Follow the plant-approved repair or replacement procedure.",
        ]

    if "impulse" in text:
        return [
            "Compare the transmitter with an independent pressure indication.",
            "Check transmitter status and manifold condition.",
            "Inspect impulse connections for the applicable blockage or restriction.",
            "Only perform intrusive work under the required isolation and permit procedure.",
            "Verify the transmitter after maintenance.",
        ]

    return [
        "Verify the instrument indication against an independent reference.",
        "Check transmitter diagnostics, power and wiring.",
        "Inspect the sensing element and process connection as applicable.",
        "Follow the plant-approved calibration and maintenance procedure.",
    ]
