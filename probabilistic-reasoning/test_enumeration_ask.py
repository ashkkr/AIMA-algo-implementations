import pytest

from enumeration_ask import EnumerationAsk
from expected_cases import CASES


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_enumeration_ask_matches_expected(query, evidence, expected):
    result = EnumerationAsk().enumeration_ask(query, evidence)
    assert result[True] == pytest.approx(expected)


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_enumeration_ask_normalizes(query, evidence, expected):
    result = EnumerationAsk().enumeration_ask(query, evidence)
    assert result[True] + result[False] == pytest.approx(1.0)


@pytest.mark.parametrize("query,evidence,expected", CASES)
def test_enumeration_ask_result_shape(query, evidence, expected):
    result = EnumerationAsk().enumeration_ask(query, evidence)
    assert set(result.keys()) == {True, False}
