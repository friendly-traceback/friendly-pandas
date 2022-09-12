import pathlib
import re
import pandas as pd
import friendly_traceback as ft
from friendly_traceback.runtime_errors.key_error import parser

# We want to focus on the code entered by the user.
# We remove anything that occurs inside pandas' library from the traceback
pandas_init = pathlib.Path(pd.__file__)
pandas_dir = pandas_init.parents[0]
ft.exclude_directory_from_traceback(pandas_dir)

# TODO: Improve friendly_traceback by
#  adding disabling chained traceback when all the information
#  given comes from excluded files or directories


@parser.insert  # ensure that this is used before the default from friendly_traceback
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
            # Note the use of backticks to surround code: this is markdown notation that
            # friendly can use to add syntax coloring.
            return {
                "cause": "You tried to use loc to retrieve a column, but it takes a row or a row selector.\n",
                "suggest": f'To retrieve a column, just use square brackets: `{df}["{key}`\n"]',
            }
        else:
            rows = list(target.index.values)
            similar = ft.similar = ft.utils.get_similar_words(key, rows)
            if len(similar) == 1:
                hint = ("Did you mean `{name}`?\n").format(name=similar[0])
                cause = (
                    "`{name}` is a key of `{dict_}` which is similar to `{key}`.\n"
                ).format(name=similar[0], dict_=df, key=repr(key))
                return {"cause": cause, "suggest": hint}

            elif len(similar) > 1:
                hint = f"Did you mean `{similar[0]}`?\n"
                names = ", ".join(similar)
                cause = f"`{df}` has some keys similar to `{key!r}` including:\n`{names}`.\n"
                return {"cause": cause, "suggest": hint}

            rows = ft.utils.list_to_string(rows) # Remove the brackets surrounding list items
            return {
                "cause": (
                    f"You tried to retrieve an unknown row. The valid values are:\n`{rows}`.\n"
                )
            }
    return {}
