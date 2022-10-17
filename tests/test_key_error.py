import pandas as pd
import friendly_traceback as ft
from friendly_pandas.specific import key_error  # noqa

df = pd.DataFrame([[1, 2, 3], [1, 4, 9]],
                  index=["number", "square"],
                  columns=["one", "two", "three"])

normal_dict = {"alpha": 1, "beta": 2, "gamma": 3}


def test_no_loc_for_col():
    try:
        df.loc["one"]
    except KeyError:
        ft.explain_traceback(redirect="capture")
    result = ft.get_output()
    assert "You tried to use loc to retrieve a column" in result


def test_unknown_row():
    try:
        df.loc["unknown"]
    except KeyError:
        ft.explain_traceback(redirect="capture")
    result = ft.get_output()
    assert "You tried to retrieve an unknown row. The valid values are:" in result
    assert "number, square" in result


def test_row_name_typo():
    try:
        df.loc["squares"]
    except KeyError:
        ft.explain_traceback(redirect="capture")
    result = ft.get_output()
    assert "Did you mean `square`" in result


def test_normal_dict_key_typo():
    try:
        normal_dict["alphas"]
    except KeyError:
        ft.explain_traceback(redirect="capture")
    result = ft.get_output()
    assert "Did you mean `'alpha'`" in result
