import itertools

from bayesnet import BayesNet, BurglaryBayesNet


class Factor:
    def __init__(self, parameters: list[str], values: list[dict]):
        self.parameters = parameters
        self.values = values


class EliminationAsk:

    def __init__(self, net: BayesNet):
        self.net = net
        self.bn = self.net.net

    """This function will get cpt values from bayes net of the variable parameter
        Then, we will find out if any value of variable or its parents is already known in the evidence
        We will keep only those cpt values that align with already known values and filter out the rest
        We will return a list of factors
        Each factor is a list of dictionaries
        Each dictionary contains values of variable and parent and cpt value
        Note: If the value of variable is already known to be negative, then we take store 1 - cpt value in cpt"""

    def make_factor(self, variable: str, evidence: dict[str, bool]) -> "Factor":
        node = self.bn[variable]
        parents = node["parents"]
        cpt = node["cpt"]
        evidenceVars = list(evidence.keys())

        values = []
        for row in cpt:
            # skip rows whose parent values conflict with the evidence
            if any(p in evidenceVars and row[p] != evidence[p] for p in parents):
                continue

            if variable in evidenceVars:
                newRow = dict(row)
                newRow[variable] = evidence[variable]
                if not evidence[variable]:
                    newRow["cpt"] = 1 - newRow["cpt"]
                values.append(newRow)
            else:
                trueRow = dict(row)
                trueRow[variable] = True
                values.append(trueRow)

                falseRow = dict(row)
                falseRow[variable] = False
                falseRow["cpt"] = 1 - falseRow["cpt"]
                values.append(falseRow)

        parameters = [p for p in parents if p not in evidenceVars]
        if variable not in evidenceVars:
            parameters.append(variable)

        return Factor(parameters, values)

    """here parameter is the variable and list of factors
        we take all the factors the have the input variable as a parameter
        Then we pointwise product all those factors to make a single factor
        once we have the single factor, we sum out the input variable
        to sum out, we take the row with postive input variable value and sum it with the corresponding
        row with negative input variable value. This happens until we have a new factor with values for all permuatations
        of values except the input variable. The parameter list should also remove the input variable"""

    def sum_out(self, variable: str, factors: list["Factor"]) -> list["Factor"]:
        relevant = [f for f in factors if variable in f.parameters]
        irrelevant = [f for f in factors if variable not in f.parameters]

        combined = relevant[0]
        for f in relevant[1:]:
            combined = self.pointwise_product(combined, f)

        parameters = [p for p in combined.parameters if p != variable]

        values = []
        for combo in itertools.product([True, False], repeat=len(parameters)):
            assignment = dict(zip(parameters, combo))

            trueRow = next(
                r
                for r in combined.values
                if r[variable] is True
                and all(r[p] == assignment[p] for p in parameters)
            )
            falseRow = next(
                r
                for r in combined.values
                if r[variable] is False
                and all(r[p] == assignment[p] for p in parameters)
            )

            newRow = {k: v for k, v in trueRow.items() if k != variable}
            newRow["cpt"] = trueRow["cpt"] + falseRow["cpt"]
            values.append(newRow)

        summedFactor = Factor(parameters, values)
        return irrelevant + [summedFactor]

    """factor 1 and factor 2 are two factors
        This should return a single factor where paramters will be a union of both factors parameters
        now to get values, we will take permutation of all possible values of parameters, then we will calcuate cpt
        value of each row by multiplying corresponding value row from factor 1 and factor 2"""

    def pointwise_product(self, factor1: "Factor", factor2: "Factor") -> "Factor":
        parameters = list(factor1.parameters)
        for p in factor2.parameters:
            if p not in parameters:
                parameters.append(p)

        values = []
        for combo in itertools.product([True, False], repeat=len(parameters)):
            assignment = dict(zip(parameters, combo))

            row1 = next(
                r
                for r in factor1.values
                if all(r[p] == assignment[p] for p in factor1.parameters)
            )
            row2 = next(
                r
                for r in factor2.values
                if all(r[p] == assignment[p] for p in factor2.parameters)
            )

            newRow = {**row1, **row2}
            newRow["cpt"] = row1["cpt"] * row2["cpt"]
            values.append(newRow)

        return Factor(parameters, values)

    def elimination_ask(self, query: str, evidence: dict[str, bool]):
        factors = []
        # eliminate children before their parents, so a hidden variable is only
        # summed out once every factor that mentions it (including from its
        # children's CPTs) has already been folded in
        variables = list(reversed(self.net.topological_order))
        evidenceVariables = list(evidence.keys())

        for variable in variables:
            factors.append(self.make_factor(variable, evidence))
            if variable != query and variable not in evidenceVariables:
                factors = self.sum_out(variable, factors)

        result = factors[0]
        for f in factors[1:]:
            result = self.pointwise_product(result, f)

        total = sum(row["cpt"] for row in result.values)
        result.values = [{**row, "cpt": row["cpt"] / total} for row in result.values]

        for row in result.values:
            print(f"P({query}={row[query]} | e) = {row['cpt']:.6f}")

        return result


if __name__ == "__main__":
    algo = EliminationAsk(BurglaryBayesNet())
    algo.elimination_ask("burglary", {"alarm": True})
