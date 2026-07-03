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
