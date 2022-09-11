import pathlib
import re
import pandas as pd
import friendly_traceback as ft

# from friendly_traceback import info_specific

# We want to focus on the code entered by the user.
# We remove anything that occurs inside pandas' library from the traceback
pandas_init = pathlib.Path(pd.__file__)
pandas_dir = pandas_init.parents[0]
ft.exclude_directory_from_traceback(pandas_dir)

# TODO: Improve friendly_traceback by
#  adding disabling chained traceback when all the information
#  given comes from excluded files or directories


@ft.info_specific.register(KeyError)
def loc_does_not_exist(error, frame, traceback_data):
    # Did we try to use loc?
    m = re.search(r"(.*)\.loc", traceback_data.bad_line)
    if m is None:
        # let the other registered handlers attempt to find an explanation
        return {}

    df = m.group(1)
    target = ft.info_variables.get_object_from_name(df, frame)
    if target is None:
        return {}

    # Is it a data frame?
    if isinstance(target, pd.core.frame.DataFrame):
        key = error.args[0]
        columns = list(target)
        # Is this string a column?
        if key in columns:
            return {
                "cause": "You tried to use loc to retrieve a column, but it takes a row or a row selector.\n",
                "suggest": f'To retrieve a column, just use square brackets: `{df}["{key}`\n"]',
            }
        else:
            return {
                "cause": (
                    "You tried to retrieve an unknown row.\n"
                    "The valid values are: `{rows}`.\n"
                ).format(rows=ft.utils.list_to_string(list(target.index.values)))
            }
            # Just for diagnostic; usually we would not include this.
            # Question: wouldn't we want to have a message about this not being
            # a known row instead^
            print(f"Did not find {key} in {columns}")
    return {}
