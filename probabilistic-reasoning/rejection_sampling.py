from bayesnet import BayesNet, BurglaryBayesNet
from prior_sample import PriorSample


class RejectionSampling:
    def __init__(self, net: BayesNet):
        self.net = net
        self.sample = PriorSample(self.net)

    def normalised(self, counts: dict[bool, int]) -> dict[bool, float]:
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    def rejection_sampling(self, query: str, e: dict[str, bool], n: int):
        # create a tuple to store counts of query variable being true and false
        counts = {True: 0, False: 0}
        for _ in range(n):
            x = self.sample.prior_sample()
            # if every value in e is present and same with values in x, then increment count in the tuple for correspoding value
            if all(x[key] == value for key, value in e.items()):
                counts[x[query]] += 1
        if sum(counts.values()) == 0:
            print("No samples consistent with evidence were generated")
            return None
        # implement another function to normalise the tuple
        result = self.normalised(counts)
        # print the tuple
        print(f"P({query}=True  | e) = {result[True]:.6f}")
        print(f"P({query}=False | e) = {result[False]:.6f}")
        return result


if __name__ == "__main__":
    rejectionSampling = RejectionSampling(BurglaryBayesNet())
    rejectionSampling.rejection_sampling("burglary", {"alarm": True}, 1000000)
