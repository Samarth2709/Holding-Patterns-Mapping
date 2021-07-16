import pandas as pd
import json

population_data = {}
population_data[1980] = pd.read_html('https://en.wikipedia.org/wiki/1980_United_States_census')[2]
population_data[1990] = pd.read_html('https://en.wikipedia.org/wiki/1990_United_States_census')[2]
population_data[2000] = pd.read_html('https://en.wikipedia.org/wiki/2000_United_States_census')[2]
population_data[2010] = pd.read_html('https://en.wikipedia.org/wiki/2010_United_States_census')[3]
for element in population_data:
    col_year_values = None
    for col_name in population_data[element].columns:
        if str(element) in str(col_name):
            col_year_values = col_name
            break

    if not col_year_values:
        print(element, population_data[element])
        col_year_values = input()


    temp ={}
    for row in population_data[element].index:
        if population_data[element].loc[row, "State"] == 'United States':
            continue
        temp[population_data[element].loc[row, "State"]] = int(population_data[element].loc[row, col_year_values])
        # population_data[element].loc[row, "State"]

    population_data[element]=temp
    print(element)
    print(population_data[element])
    print('\n\n\n\n')

print(population_data)

with open('state_pops.json', 'w') as convert_file:
    convert_file.write(json.dumps(population_data))

print("\n\n\n\n\n")
with open('state_pops.json', 'r') as read_state:
    dict_pop = json.load(read_state)
    dict_pop_2 = read_state

print(dict_pop)
print(dict_pop_2)