import pandas as pd
import pytest

from data_division import Divide
from ripple import Ripple


@pytest.fixture
def sample_data():
    glucose_data = pd.DataFrame({
        "time": pd.to_datetime(['2021-01-01 00:00', '2021-01-01 01:00', '2021-01-01 02:00']),
        "glucose": [100, 110, 120]
    })

    return Divide(glucose=glucose_data)


@pytest.fixture
def trend_list():
    return [10, 10, 0]


@pytest.fixture
def trend_list_count():
    return [1, 1]


def test_create_ripple(sample_data, trend_list):
    ripple_instance = sample_data.create_ripple(0, 1, trend_list)

    assert isinstance(ripple_instance, Ripple)

    assert ripple_instance.bg.tolist() == [100]
    assert ripple_instance.time_v.tolist() == [pd.to_datetime('2021-01-01 00:00')]
    assert ripple_instance.trend_v == [10]


def test_generate_ripples(sample_data, trend_list, trend_list_count):
    ripple_list = sample_data.generate_ripples(trend_list=trend_list, trend_list_count=trend_list_count)
    assert len(ripple_list) == 2

    # Check the first ripple instance
    ripple1 = ripple_list[0]
    assert isinstance(ripple1, Ripple)
    assert ripple1.bg.tolist() == [100]
    assert ripple1.time_v.tolist() == [pd.to_datetime('2021-01-01 00:00')]
    assert ripple1.trend_v == [10]

    # Check the second ripple instance
    ripple2 = ripple_list[1]
    assert isinstance(ripple2, Ripple)
    assert ripple2.bg.tolist() == [110]
    assert ripple2.time_v.tolist() == [pd.to_datetime('2021-01-01 01:00')]
    assert ripple2.trend_v == [10]
