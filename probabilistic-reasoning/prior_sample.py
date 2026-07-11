import random

from bayesnet import BayesNet


class PriorSample:

    def __init__(self, net: BayesNet):
        self.net = net
        self.bn = self.net.burglary_bn

    """The goal here is to generate a sample"""

    def prior_sample(self) -> dict[str, bool]:
        # variables must be in topological order so that a node's parents
        # are always sampled before the node itself
        variables = list(self.bn.keys())
        x: dict[str, bool] = {}

        for key in variables:
            # draw a uniform random number to decide the sampled value
            r = random.random()
            # get P(key=True | parents), using values already sampled in x
            p_true = self.net.get_probability(key, {**x, key: True})
            # if r falls below p_true, sample this variable as True
            x[key] = r < p_true
        return x


if __name__ == "__main__":
    net = BayesNet()
    algo = PriorSample(net)
    for i in range(1000):
        algo.prior_sample()
