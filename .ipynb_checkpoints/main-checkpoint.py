# def func(param: str = None):
#     if param:
#         print(True)
#     else:
#
#         print(False)
#
# func("")

import pandas as pd

df = pd.DataFrame({"Col1":[1, 2, 3], "Col2":[4, 5, 6]})
filter_data = df["Col1"] == 1
print(df[filter_data])