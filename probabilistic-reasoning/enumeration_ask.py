from bayesnet import BayesNet, BurglaryBayesNet


class EnumerationAsk:

    def __init__(self, net: BayesNet):
        self.net = net

    def normalised(self, queryDict: dict[bool, float]) -> dict[bool, float]:
        total = sum(queryDict.values())
        return {k: v / total for k, v in queryDict.items()}

    # here e can be negative or positive
    # query is just variable name
    def enumeration_ask(self, query: str, e: dict[str, bool]):
        variables = self.net.topological_order

        queryDict = {}
        for queryValue in [True, False]:
            extendedE = e.copy()
            extendedE[query] = queryValue
            queryDict[queryValue] = self.enumerate_all(variables, extendedE)

        result = self.normalised(queryDict)
        print(f"P({query}=True  | e) = {result[True]:.6f}")
        print(f"P({query}=False | e) = {result[False]:.6f}")
        return result

    def enumerate_all(self, variables: list[str], e: dict[str, bool]) -> float:
        if len(variables) == 0:
            return 1.0
        v = variables[0]
        if v in e.keys():
            rest = self.enumerate_all(variables[1:], e)
            node_prob = self.net.get_probability(v, e)
            return node_prob * rest
        else:
            total = 0.0
            for vValue in [True, False]:
                updatedE = e.copy()
                updatedE[v] = vValue
                rest = self.enumerate_all(variables[1:], updatedE)
                node_prob = self.net.get_probability(v, updatedE)
                total += node_prob * rest
            return total


if __name__ == "__main__":
    algo = EnumerationAsk(BurglaryBayesNet())
    algo.enumeration_ask("burglary", {"alarm": True})
