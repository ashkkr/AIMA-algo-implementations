import pytest

from elimination_ask import EliminationAsk
from expected_cases import CASES


def as_dict(factor, query):
    return {row[query]: row["cpt"] for row in factor.values}


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_elimination_ask_matches_expected(query, evidence, expected):
    result = EliminationAsk().elimination_ask(query, evidence)
    assert as_dict(result, query)[True] == pytest.approx(expected)


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_elimination_ask_normalizes(query, evidence, expected):
    result = EliminationAsk().elimination_ask(query, evidence)
    probs = as_dict(result, query)
    assert probs[True] + probs[False] == pytest.approx(1.0)


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_elimination_ask_result_shape(query, evidence, expected):
    result = EliminationAsk().elimination_ask(query, evidence)
    assert len(result.values) == 2
    for row in result.values:
        assert query in row
        assert "cpt" in row
