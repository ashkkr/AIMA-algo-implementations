class BayesNet:
    # Burglary = "burglary"
    # Earthquake = "earthquake"
    # Alarm = "alarm"
    # JohnCalls = "johnCalls"
    # MaryCalls = "maryCalls"

    def __init__(self):
        # This represents the CPT table for the burglary example from AIMA
        # CPT here is a list, where first value is when all parents are positive, followed by values for negative parents in order from left to right
        # Last value thus is for when all parents are negative
        self.burglary_bn = {
            "burglary": {
                "parents": [],
                "cpt": [{"cpt": 0.001}],
            },
            "earthquake": {
                "parents": [],
                "cpt": [{"cpt": 0.002}],
            },
            "alarm": {
                "parents": ["burglary", "earthquake"],
                "cpt": [
                    {"burglary": True, "earthquake": True, "cpt": 0.95},
                    {"burglary": True, "earthquake": False, "cpt": 0.94},
                    {"burglary": False, "earthquake": True, "cpt": 0.29},
                    {"burglary": False, "earthquake": False, "cpt": 0.001},
                ],
            },
            "johnCalls": {
                "parents": ["alarm"],
                "cpt": [
                    {"alarm": True, "cpt": 0.90},
                    {"alarm": False, "cpt": 0.05},
                ],
            },
            "maryCalls": {
                "parents": ["alarm"],
                "cpt": [
                    {"alarm": True, "cpt": 0.70},
                    {"alarm": False, "cpt": 0.01},
                ],
            },
        }

    def get_probability(self, node: str, evidence: dict[str, bool]) -> float:
        parents = self.burglary_bn[node]["parents"]
        parent_values = {p: evidence[p] for p in parents}
        cpt_row = next(
            row
            for row in self.burglary_bn[node]["cpt"]
            if all(row[p] == parent_values[p] for p in parents)
        )
        p = cpt_row["cpt"]
        if evidence[node]:
            return p
        else:
            return 1 - p
