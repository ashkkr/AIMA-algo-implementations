# Ground-truth (query, evidence, expected P(query=True | evidence)) cases for the
# burglary Bayes net, shared by test_enumeration_ask.py and test_elimination_ask.py.
CASES = [
    ("burglary", {"johnCalls": True, "maryCalls": True}, 0.2841718353643929),
    ("burglary", {"alarm": True}, 0.373551228281836),
    ("alarm", {"burglary": True, "earthquake": True}, 0.9500000000000001),
    ("burglary", {}, 0.001),
    ("earthquake", {"alarm": True}, 0.23100870196889095),
    ("johnCalls", {"burglary": True}, 0.849017),
]

# Ground-truth (query, evidence, expected P(query=True | evidence)) cases for the
# sprinkler/rain/wet-grass Bayes net (AIMA Figure 13.15), used to exercise the
# same inference algorithms against a second, multiply-connected network.
SPRINKLER_CASES = [
    ("cloudy", {}, 0.5),
    ("sprinkler", {"cloudy": True}, 0.1),
    ("wetGrass", {"sprinkler": True, "rain": True}, 0.99),
    ("cloudy", {"wetGrass": True}, 0.5757997218358832),
    ("rain", {"sprinkler": True, "wetGrass": True}, 0.32038834951456313),
]
