import random
import pandas as pd

class AmmoniaProcess:
    def __init__(self):
        self.reset()

    def reset(self):
        self.step_no = 0
        self.active_fault = None
        self.data = {
            "PT-101": 145.0,
            "PT-102": 145.5,
            "TT-101": 475.0,
            "FT-101": 21.0,
            "LT-101": 62.0,
            "AT-101": 17.5,
        }
        self.history = []
        self._record()

    def inject_fault(self, instrument, fault, severity):
        self.active_fault = {
            "instrument": instrument,
            "fault": fault,
            "severity": severity,
        }

    def step(self):
        self.step_no += 1

        # Simple virtual process dynamics
        self.data["PT-101"] += random.uniform(-0.7, 0.9)
        self.data["PT-102"] += random.uniform(-0.6, 0.8)
        self.data["TT-101"] += random.uniform(-1.8, 1.8)
        self.data["FT-101"] += random.uniform(-0.35, 0.35)
        self.data["LT-101"] += random.uniform(-0.8, 0.8)
        self.data["AT-101"] += random.uniform(-0.12, 0.12)

        # Keep process in realistic demo ranges
        self.data["PT-101"] = max(135, min(165, self.data["PT-101"]))
        self.data["PT-102"] = max(135, min(165, self.data["PT-102"]))
        self.data["TT-101"] = max(450, min(500, self.data["TT-101"]))
        self.data["FT-101"] = max(16, min(26, self.data["FT-101"]))
        self.data["LT-101"] = max(40, min(85, self.data["LT-101"]))
        self.data["AT-101"] = max(14, min(21, self.data["AT-101"]))

        self._apply_fault()
        self._record()

    def _apply_fault(self):
        if not self.active_fault:
            return

        tag = self.active_fault["instrument"]
        fault = self.active_fault["fault"]
        s = self.active_fault["severity"]

        if fault == "Stuck transmitter":
            if self.history:
                self.data[tag] = self.history[-1][tag]

        elif fault == "Signal drift":
            self.data[tag] += s * 0.8

        elif fault == "Noisy signal":
            self.data[tag] += random.uniform(-1, 1) * s * 8

        elif fault == "Zero / low signal":
            self.data[tag] = 0.0 + random.uniform(0, 0.15)

        elif fault == "High signal":
            self.data[tag] *= 1 + 0.35 * s

        elif fault == "Impulse-line blockage":
            if self.history:
                old = self.history[-1][tag]
                self.data[tag] = 0.85 * old + 0.15 * self.data[tag]

        elif fault == "Analyzer bias":
            self.data[tag] += 2.0 * s

        elif fault == "Valve stuck":
            # Simulate process response rather than an instrument signal.
            self.data["FT-101"] -= 0.8 * s
            self.data["PT-101"] += 1.0 * s

    def _record(self):
        row = {"time": self.step_no, **self.data}
        self.history.append(row)

    def snapshot(self):
        return dict(self.data)

    def history_df(self):
        return pd.DataFrame(self.history)

    def is_abnormal(self, tag):
        if not self.active_fault:
            return False
        if self.active_fault["instrument"] == tag:
            return True
        if self.active_fault["fault"] == "Valve stuck" and tag in ("FT-101", "PT-101"):
            return True
        return False
