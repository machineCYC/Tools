import pytest

from Tools.utility.time import (
    transform_Yweek2Date,
    transform_Date2Yweek,
    transform_Date2WeekDay
    add_Weekdelta2Yweek,
    add_Daydelta2Date,
    calculate_Datenbr,
    calculate_Weeknbr,
)


testdata_transform_Yweek2Date = [("2019-28", "2019-07-08"), ("2019-01", "2018-12-31"), ("2020-01", "2019-12-30")]
@pytest.mark.parametrize(
    "yweek, expected", testdata_transform_Yweek2Date,
)
def test_transform_Yweek2Date(yweek, expected):
    resp = transform_Yweek2Date(yweek)
    assert resp == expected


testdata_transform_Date2Yweek = [("2019-10-22", "2019-43"), ("2020-01-01", "2020-01"), ("2019-12-31", "2020-01")]
@pytest.mark.parametrize(
    "date, expected", testdata_transform_Date2Yweek,
)
def test_transform_Date2Yweek(date, expected):
    resp = transform_Date2Yweek(date)
    assert resp == expected


testdata_transform_Date2WeekDay = [("2020-01-01", "3"), ("2020-01-05", "7"), ("2020-03-02", "1")]
@pytest.mark.parametrize(
    "date, expected", testdata_transform_Date2WeekDay,
)
def test_transform_Date2WeekDay(date, expected):
    resp = transform_Date2WeekDay(date)
    assert resp == expected


testdata_add_Weekdelta2Yweek = [("2019-15", 5, "2019-20"), ("2019-50", 10, "2020-08"), ("2020-10", -3, "2020-07"), ("2020-01", -2, "2019-51")]
@pytest.mark.parametrize(
    "yweek, week_nbr, expected", testdata_add_Weekdelta2Yweek,
)
def test_add_Weekdelta2Yweek(yweek, week_nbr, expected):
    resp = add_Weekdelta2Yweek(yweek, week_nbr)
    assert resp == expected


testdata_add_Daydelta2Date = [("2020-01-01", 5, "2020-01-06"), ("2020-01-01", -5, "2019-12-27")]
@pytest.mark.parametrize(
    "yweek, week_nbr, expected", testdata_add_Daydelta2Date,
)
def test_add_Daydelta2Date(date, days, expected):
    resp = add_Daydelta2Date(date, days)
    assert resp == expected


testdata_calculate_Datenbr = [("2020-01-01", "2020-01-05", 4), ("2019-12-29", "2020-01-03", 5)]
@pytest.mark.parametrize(
    "day1, day2, expected", testdata_calculate_Datenbr,
)
def test_calculate_Datenbr(day1, day2, expected):
    resp = calculate_Datenbr(day1, day2)
    assert resp == expected


testdata_calculate_Weeknbr = [("2020-15", "2020-20", 5), ("2019-50", "2020-20", 22)]
@pytest.mark.parametrize(
    "yweek1, yweek2, expected", testdata_calculate_Weeknbr,
)
def test_calculate_Weeknbr(yweek1, yweek2, expected):
    resp = calculate_Weeknbr(yweek1, yweek2)
    assert resp == expected
