import pytest

from Tools.utility.time import (
    calculate_Datenbr,
)

testdata_calculate_Datenbr = [("2020-01-01", "2020-01-05", 4), ("2019-12-29", "2020-01-03", 5)]

@pytest.mark.parametrize(
    "day1, day2, expected", testdata_calculate_Datenbr,
)
def test_calculate_Datenbr(day1, day2, expected):
    resp = calculate_Datenbr(day1, day2)
    assert resp == expected