from enum import Enum

# example query is P(b|j ^ m)


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

    def normalised(self, queryDict: dict[bool, float]) -> dict[bool, float]:
        total = sum(queryDict.values())
        return {k: v / total for k, v in queryDict.items()}

    # here e can be negative or positive
    # query is just variable name
    def enumeration_ask(self, query: str, e: dict[str, bool]):
        vars = list(self.burglary_bn.keys())

        queryDict = {}
        for queryValue in [True, False]:
            extendedE = e.copy()
            extendedE[query] = queryValue
            queryDict[queryValue] = self.enumerate_all(vars, extendedE)

        result = self.normalised(queryDict)
        print(f"P({query}=True  | e) = {result[True]:.6f}")
        print(f"P({query}=False | e) = {result[False]:.6f}")
        return result

    def enumerate_all(self, vars: list[str], e: dict[str, bool]) -> float:
        if len(vars) == 0:
            return 1.0
        v = vars[0]
        if v in e.keys():
            rest = self.enumerate_all(vars[1:], e)
            parents = self.burglary_bn[v]["parents"]
            parent_values = {p: e[p] for p in parents}
            cpt_row = next(
                row
                for row in self.burglary_bn[v]["cpt"]
                if all(row[p] == parent_values[p] for p in parents)
            )
            p = cpt_row["cpt"]
            if e[v] == True:
                return p * rest
            else:
                return (1 - p) * rest
        else:
            total = 0.0
            for vValue in [True, False]:
                updatedE = e.copy()
                updatedE[v] = vValue
                rest = self.enumerate_all(vars[1:], updatedE)

                parents = self.burglary_bn[v]["parents"]
                parent_values = {p: e[p] for p in parents}
                cpt_row = next(
                    row
                    for row in self.burglary_bn[v]["cpt"]
                    if all(row[p] == parent_values[p] for p in parents)
                )
                p = cpt_row["cpt"]
                total += (p if vValue else (1 - p)) * rest
            return total


bn = BayesNet()
bn.enumeration_ask(
    "johnCalls",
    {"alarm": True},
)
