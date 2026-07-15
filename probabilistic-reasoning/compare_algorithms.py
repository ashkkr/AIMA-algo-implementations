from bayesnet import BayesNet, BurglaryBayesNet, SprinklerBayesNet
from elimination_ask import EliminationAsk
from expected_cases import CASES, SPRINKLER_CASES
from gibbs_sampling import GibbsSampling
from importance_sampling import ImportanceSampling
from rejection_sampling import RejectionSampling

N = 1_000_000


def as_dict(factor, query: str) -> dict[bool, float]:
    return {row[query]: row["cpt"] for row in factor.values}


def run_comparison(net: BayesNet, cases: list[tuple[str, dict[str, bool], float]]):
    elimination = EliminationAsk(net)
    rejection = RejectionSampling(net)
    importance = ImportanceSampling(net)
    gibbs = GibbsSampling(net)

    for query, evidence, _expected in cases:
        print("=" * 70)
        print(f"query = {query!r}, evidence = {evidence!r}")
        print("=" * 70)

        print("-- Variable Elimination (exact) --")
        result = elimination.elimination_ask(query, evidence)
        exact = as_dict(result, query)

        print("-- Rejection Sampling (n = 1,000,000) --")
        rejection.rejection_sampling(query, evidence, N)

        print("-- Importance Sampling / Likelihood Weighting (n = 1,000,000) --")
        importance.importance_sampling(query, evidence, N)

        print("-- Gibbs Sampling (n = 1,000,000) --")
        gibbs.gibbs_sampling(query, evidence, N)

        print(f"[reference] P({query}=True | e) via variable elimination = {exact[True]:.6f}")
        print()


def main():
    print("#" * 70)
    print("# Burglary Bayes net")
    print("#" * 70)
    # five (query, evidence) pairs pulled from the shared ground-truth cases,
    # spanning no evidence, single evidence and multiple evidence variables
    run_comparison(BurglaryBayesNet(), CASES[:5])

    print("#" * 70)
    print("# Sprinkler/Rain/WetGrass Bayes net")
    print("#" * 70)
    run_comparison(SprinklerBayesNet(), SPRINKLER_CASES)


if __name__ == "__main__":
    main()
