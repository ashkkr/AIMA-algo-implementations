import random

from bayesnet import BayesNet


class ImportanceSampling:
    def __init__(self):
        self.net = BayesNet()
        self.bn = self.net.burglary_bn

    def normalised(self, weights: dict[bool, float]) -> dict[bool, float]:
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}

    def importance_sampling(self, query: str, e: dict[str, bool], n: int):
        # make a tuple to store likelihoods for query string being true and false, initialise with 0,0
        W = {True: 0, False: 0}
        for _ in range(n):
            # here get a sample and its weight from weightedsampling
            x, w = self.weightedSampling(e)
            # check the sample to get value of query, and add the weight value to corresponding element
            W[x[query]] += w
        # here check if total weight of samples is greater than zero, if not short circuit with error,
        # no valid samples consistent with evidence could be generated
        if sum(W.values()) == 0:
            print("No samples consistent with evidence were generated")
            return None
        # here implement another function to normalise
        result = self.normalised(W)
        # print here and return
        print(f"P({query}=True  | e) = {result[True]:.6f}")
        print(f"P({query}=False | e) = {result[False]:.6f}")
        return result

    """ here we will generate samples in topological order that are
    consistent with the provided evidence. This also returns the likelihood of the sample"""

    def weightedSampling(self, e: dict[str, bool]):
        keys = list(self.bn.keys())
        # we store likelihood of the sample in a variable
        w = 1
        x: dict[str, bool] = {}
        for key in keys:
            # if key is in the evidence, then we get the probability of the value of key given its parents
            if key in e:
                x[key] = e[key]
                # we update w = w * probability from last line
                w = w * self.net.get_probability(key, x)
            else:
                # else us this logic r = random.random()
                # p_true = self.net.get_probability(key, {**x, key: True})
                # x[key] = r < p_true
                r = random.random()
                p_true = self.net.get_probability(key, {**x, key: True})
                x[key] = r < p_true

        # here we return the sample dictionary and the likelihood weight
        return x, w


if __name__ == "__main__":
    importanceSampling = ImportanceSampling()
    importanceSampling.importance_sampling("burglary", {"alarm": True}, 1000000)
