# Created by Samarth Kumbla
# NASA VIP Internship

import pandas as pd
import os
import json


# path = os.path.join(os.getcwd(), 'Major_airports')
#
# arr = os.listdir(path)
# dfs = {}
# for element in arr:
#     dfs[element] = pd.read_excel(os.path.join(path, element))
#
# max_len = 1000000
# for file, df in dfs.items():
#     print(file)
#     print(df)
#     print(df.columns)
#     print()
#     print()
#     print()
#     max_len = min(max_len, len(df.index))
#
# print(max_len)

# get 300 rows
def get_all_dfs(path=None, state_col="ST"):
    # path is directory with only data excel files
    if path == None:
        path = os.path.join(os.getcwd(), 'Major_airports')
    all_files = os.listdir(path)

    dfs = {}
    year = 0
    for file in all_files:
        year += 1
        if year < 10:
            dfs[file] = pd.read_excel(os.path.join(path, file),
                                      usecols=[state_col, "CY 0" + str(year) + " Enplanements"], nrows=300)
            dfs[file] = dfs[file].rename({"CY 0" + str(year) + " Enplanements": "Enplanements"}, axis=1)
        else:
            dfs[file] = pd.read_excel(os.path.join(path, file),
                                      usecols=[state_col, "CY " + str(year) + " Enplanements"], nrows=300)
            dfs[file] = dfs[file].rename({"CY " + str(year) + " Enplanements": "Enplanements"}, axis=1)
    return dfs



def create_main_df(dic_dfs, state_col='ST'):
    # concatenates all dfs in dict dfs with their associated year
    main_df = pd.DataFrame(columns=["Year", state_col, "Enplanements"])

    year = 2000
    for file, df in dic_dfs.items():
        year+=1
        dic_dfs[file]["Year"] = year
        main_df = pd.concat([main_df, dic_dfs[file]], axis=0, ignore_index=True)
    return main_df




def convert_st_abbrev_to_full(df_main, json_data):
    for row in df_main.index:
        df_main.loc[row, "ST"] = json_data[df_main.loc[row, "ST"]]
    return df_main


def main():
    df = create_main_df(get_all_dfs())
    path = os.path.join(os.getcwd(), 'abbreviation_to_full_state_name.json')
    with open(path, 'r') as raw_json:
        json_data = json.load(raw_json)
    df = convert_st_abbrev_to_full(df, json_data)
    return df

if __name__ == '__main__':
    df = create_main_df(get_all_dfs())
    print(df)

    path = os.path.join(os.getcwd(), 'abbreviation_to_full_state_name.json')
    with open(path, 'r') as raw_json:
        json_data = json.load(raw_json)
    df = convert_st_abbrev_to_full()

    df.to_excel('main_df_major_airports.xlsx')
