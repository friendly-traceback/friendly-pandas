import re

from pandas.core.frame import DataFrame
from pandas.errors import SettingWithCopyWarning
from friendly_traceback.about_warnings import WarningInfo, get_warning_parser
from friendly_traceback.typing_info import CauseInfo  # for type checking only

parser = get_warning_parser(SettingWithCopyWarning)


@parser.add
def setting_with_copy_warning(message: str, warning_data: WarningInfo) -> CauseInfo:
    statement = re.sub(r"\s+", "", warning_data.problem_statement)
    pattern = re.compile(
        r"""
        (.*)  # dataframe name
        \s*\.\s*loc    # .loc  including possible spaces
        \[(.*)\]       # first index
        \s*
        \[(.*)\]       # second index
        """,
        re.VERBOSE,
    )
    match = re.match(pattern, statement)
    if not match:
        return {}
    dataframe_name = match[1]
    index_1 = match[2]
    index_2 = match[3]
    cause = (
        "You used direct chained indexing of a dataframe which made a copy\n"
        "of the original content of the dataframe. If you try to assign a value\n"
        "to that copy, the original dataframe will not be modified.\n"
        "Instead of doing a direct chained indexing\n\n"
        "    {statement}\n\n"
        " try:\n\n"
        "    {dataframe_name}.loc[{index_1}, {index_2}]\n"
    ).format(
        statement=statement,
        dataframe_name=dataframe_name,
        index_1=index_1,
        index_2=index_2,
    )
    return {"cause": cause}


def find_all_dataframes(frame):
    dataframes = {
        name for name in frame.f_locals if isinstance(frame.f_locals[name], DataFrame)
    }
    gl_dataframes = {
        name for name in frame.f_globals if isinstance(frame.f_globals[name], DataFrame)
    }
    return dataframes.union(gl_dataframes)
