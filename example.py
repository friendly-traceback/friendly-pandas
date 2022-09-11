import pandas as pd

df = pd.DataFrame([[10, 20, 30], [40, 50, 60]],
                  index=list("ab"),
                  columns=list("xyz"))

# print(df.loc['y'])
