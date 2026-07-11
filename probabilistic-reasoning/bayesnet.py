from abc import ABC, abstractmethod


class BayesNet(ABC):
    @property
    @abstractmethod
    def net(self) -> dict:
        """CPT table for the network, keyed by variable name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def topological_order(self) -> list[str]:
        """Variables ordered so that every variable follows all of its parents."""
        raise NotImplementedError

    def get_probability(self, node: str, evidence: dict[str, bool]) -> float:
        parents = self.net[node]["parents"]
        parent_values = {p: evidence[p] for p in parents}
        cpt_row = next(
            row
            for row in self.net[node]["cpt"]
            if all(row[p] == parent_values[p] for p in parents)
        )
        p = cpt_row["cpt"]
        if evidence[node]:
            return p
        else:
            return 1 - p


class BurglaryBayesNet(BayesNet):
    def __init__(self):
        # This represents the CPT table for the burglary example from AIMA
        # CPT here is a list, where first value is when all parents are positive, followed by values for negative parents in order from left to right
        # Last value thus is for when all parents are negative
        self._net = {
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
        self._topological_order = ["burglary", "earthquake", "alarm", "johnCalls", "maryCalls"]

    @property
    def net(self) -> dict:
        return self._net

    @property
    def topological_order(self) -> list[str]:
        return self._topological_order


class SprinklerBayesNet(BayesNet):
    def __init__(self):
        # This represents the CPT table for the sprinkler/rain/wet-grass example from AIMA
        # CPT here is a list, where first value is when all parents are positive, followed by values for negative parents in order from left to right
        # Last value thus is for when all parents are negative
        self._net = {
            "cloudy": {
                "parents": [],
                "cpt": [{"cpt": 0.5}],
            },
            "sprinkler": {
                "parents": ["cloudy"],
                "cpt": [
                    {"cloudy": True, "cpt": 0.10},
                    {"cloudy": False, "cpt": 0.50},
                ],
            },
            "rain": {
                "parents": ["cloudy"],
                "cpt": [
                    {"cloudy": True, "cpt": 0.80},
                    {"cloudy": False, "cpt": 0.20},
                ],
            },
            "wetGrass": {
                "parents": ["sprinkler", "rain"],
                "cpt": [
                    {"sprinkler": True, "rain": True, "cpt": 0.99},
                    {"sprinkler": True, "rain": False, "cpt": 0.90},
                    {"sprinkler": False, "rain": True, "cpt": 0.90},
                    {"sprinkler": False, "rain": False, "cpt": 0.00},
                ],
            },
        }
        self._topological_order = ["cloudy", "sprinkler", "rain", "wetGrass"]

    @property
    def net(self) -> dict:
        return self._net

    @property
    def topological_order(self) -> list[str]:
        return self._topological_order
