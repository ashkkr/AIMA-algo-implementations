import random

from bayesnet import BayesNet
from prior_sample import PriorSample


class GibbsSampling:
    def __init__(self, net: BayesNet):
        self.net = net
        self.sample = PriorSample(self.net)

    def normalised(self, weights: dict[bool, float]) -> dict[bool, float]:
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def children_of(self, node: str) -> list[str]:
        return [v for v, data in self.net.net.items() if node in data["parents"]]

    def gibbs_sampling(self, query: str, e: dict[str, bool], n: int):
        initialSample = self.sample.prior_sample()
        # here make initialsample consistent with values of evidence e
        initialSample.update(e)
        # here make a tuple to count query true and false values of samples
        counts = {True: 0, False: 0}

        nonEvidenceVars = [v for v in self.net.topological_order if v not in e]
        currentSample = initialSample

        for i in range(n):
            # pick at random any non evidence variable, call it curr_node
            currNode = random.choice(nonEvidenceVars)
            # calculate its probability distribution given its markov blanket
            children = self.children_of(currNode)
            weights: dict[bool, float] = {}
            for value in (True, False):
                # we make two calculations, one for curr_node being true and one for it being false
                candidate = {**currentSample, currNode: value}
                # for true, calculate its probability of being true given its parents (values in sample),
                # then multiply that with product of all curr_nodes children given their parents (here curr_node is true)
                # make similary calculation for curr_node being false. Here note that when fetching children's cpt
                # the curr_node parent is false
                w = self.net.get_probability(currNode, candidate)
                for child in children:
                    w *= self.net.get_probability(child, candidate)
                weights[value] = w
            # when we have both the values, we normalise in a separate function
            distribution = self.normalised(weights)
            # pick at random one of the values from prob distribution and update the sample
            r = random.random()
            currentSample[currNode] = r < distribution[True]
            # now update value of count corresponding to value of query var in sample
            counts[currentSample[query]] += 1
        # return normlised values
        result = self.normalised(counts)
        print(f"P({query}=True  | e) = {result[True]:.6f}")
        print(f"P({query}=False | e) = {result[False]:.6f}")
        return result


if __name__ == "__main__":
    from bayesnet import BurglaryBayesNet

    gibbsSampling = GibbsSampling(BurglaryBayesNet())
    gibbsSampling.gibbs_sampling("burglary", {"alarm": True}, 1000000)
