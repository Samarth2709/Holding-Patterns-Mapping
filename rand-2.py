# numbs = [2, 7, 333, 7, 9]
# num = 3
# def take_closest(num,collection):
#    return min(collection,key=lambda x:abs(x-num))
#
# print(take_closest(num, numbs))

import pandas as pd
import os

# a_list.count("a")
# year -> state -> count
# {'2018':
#       {'Alabama': 2,
#        'Alaska': 3}
#  }
def convert_main_air_json(filename):
    df = pd.read_excel(filename)
    main_airport_dict = {}
    for year in df['Year'].unique():
        states_in_year = {}
        for state in df[df['Year'] == year]['ST'].unique():
            states_in_year[state] = int(list(df[df['Year'] == year]['ST']).count(state))
        main_airport_dict[year] = states_in_year
    return main_airport_dict


# x = convert_main_air_json('main_df_major_airports.xlsx')
# print(x)

# data = {'2000':{'car':2},
#         '2001':{'car':4}}


list_stuff = [1].extend([x for x in range(4)])
print(list_stuff)

