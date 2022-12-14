# Make this example usable with friendly_traceback instead of requiring
# friendly. By default, warnings are disabled in friendly_traceback.
from friendly_traceback import enable_warnings
enable_warnings()
# Will automatically register the required parsers.
import friendly_pandas  # noqa

import pandas as pd

df = pd.DataFrame([[10, 20, 30], [40, 50., 60]],
                  index=list("ab"),
                  columns=list("xyz"))

series = df.loc["b"]
series["x"] = 99

series_1 = df["x"]
series_1.loc["b"] = 99
