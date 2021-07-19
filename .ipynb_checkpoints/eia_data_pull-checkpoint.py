# Created by Samarth
# Nasa VIP Internship

import pandas as pd
import requests
import time


class CarbonEmission:
    def __init__(self, link):
        self.link = link
        self.data = requests.get(link)

    def get_link(self):
        return self.link

    def get_data_json(self):
        return self.data.json()

    def get_series_id(self):
        return self.data.json()["request"]["series_id"]

    def get_description(self):
        return self.data.json()["series"][0]["name"]

    def get_state(self):
        for state in states:
            if state.lower() in str(self.get_description().lower()):
                return state

    def get_units(self):
        return self.data.json()["series"][0]["units"]

    def get_updated_date(self):
        return self.data.json()["series"][0]["updated"]

    def get_range_years(self):
        return list(range(int(self.data.json()["series"][0]["start"]), int(self.data.json()["series"][0]["end"]) + 1))

    def get_data_values(self):
        data_vals = []
        for element in self.data.json()["series"][0]["data"]:
            data_vals.append(element[-1])
        return data_vals

    def get_df(self):
        col_names = self.get_range_years()
        df = pd.DataFrame(columns=col_names)
        data_vals = pd.Series(self.get_data_values(), index=df.columns)
        df = df.append(data_vals, ignore_index=True)
        return df


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return "Time Elapsed: {0}hrs,  {1}min,  {2}sec".format(int(hours), int(mins), round(sec, 2))


def status(func):
    def wrapper(*args, **kwargs):
        print("-------------")
        print(func.__name__, "Began running")
        start_time = time.time()

        stuff = func(*args, **kwargs)

        print(time_convert(time.time() - start_time))
        print('     ', func.__name__, "END")
        print('')
        return stuff
    return wrapper


states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "New Jersey",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
    ]

api_key = "a692666e8f7ab3e626b3e3530c44d2c8"

eia_url = {
    "category_base": "http://api.eia.gov/category/?api_key=" + str(api_key) + "&category_id=",
    "category": "http://api.eia.gov/category/?api_key=" + str(api_key) + "&category_id=2251670",
    "series_base": "http://api.eia.gov/series/?api_key=" + str(api_key) + "&series_id="
           }
# category id 2251670 dict of states (with each category_id) r.json()["category"]["childcategories"]
# series id is the id of type of data for state (final link)

data = {}


@ status
def get_link_to_all_data_sets_for_state():
    r_category_states = requests.get(eia_url["category"])
    for ele in r_category_states.json()["category"]["childcategories"]:
        if ele['name'] in states:
            data[ele['name']] = str(eia_url["category_base"] + str(ele["category_id"]))
            # stores {"state name" : link to data sets} in data dictionary
    return data


@ status
def get_data_links_for_aviation_sectors(data):
    for head, val in data.items():
        state_data = {}
        state_data_sets = requests.get(val).json()["category"]["childseries"]
        for data_set in state_data_sets:
            if "aviation gasoline" in data_set["name"]:
                state_data["aviation gasoline"] = eia_url["series_base"] + str(data_set["series_id"])
            elif "jet fuel" in data_set["name"]:
                state_data["jet fuel"] = eia_url["series_base"] + str(data_set["series_id"])
            elif "all fuel" in data_set["name"]:
                state_data["all fuel"] = eia_url["series_base"] + str(data_set["series_id"])
        data[head] = state_data
    return data

@ status
def convert_links_to_classes(data):
    for state, sectors in data.items():
        for sector, link in sectors.items():
            data[state][sector] = CarbonEmission(link)
    return data


@status
def combine_state_df_all(save = False, save_as="All_EIA_Data", data=data):
    df = pd.DataFrame(columns=["ID", "State", "Carbon Output Type", "Year", "Carbon Output Value", "Unit Measurement",
                               "Updated Time"])
    for i, state in enumerate(data):
        for sector in data[state]:
            if i == 0:
                range_years = data[state][sector].get_range_years()
            for j, year in enumerate(range_years):
                row_to_append = ['', state, sector, year, data[state][sector].get_data_values()[j],
                                 data[state][sector].get_units(), data[state][sector].get_updated_date()]
                # [ID, State, Sector, Year, CO2 Output, Unit, Date]
                df = df.append(pd.Series(row_to_append, index=df.columns), ignore_index=True)
    if save:
        df.to_excel(save_as + ".xlsx", index=False)
    return df


@status
def combine_state_df(sector_name, save = False, save_as: str = None, data = data):
    # jet fuel, aviation gasoline, all fuel  --  sector names
    df = pd.DataFrame(columns=["ID", "State", "Year", "Carbon Output Value", "Unit Measurement", "Updated Time"])
    for i, state in enumerate(data):
        if i == 0:
            range_years = data[state][sector_name].get_range_years()
        for j, year in enumerate(range_years):
            row_to_append = ['', state, year, data[state][sector_name].get_data_values()[j],
                             data[state][sector_name].get_units(), data[state][sector_name].get_updated_date()]
            # [ID, State, Year, CO2 Output, Unit, Date]
            df = df.append(pd.Series(row_to_append, index=df.columns), ignore_index=True)
    if save:
        if save_as:
            df.to_excel(save_as + ".xlsx", index=False)
        else:
            df.to_excel(sector_name + "_EIA_Data.xlsx", index=False)
    return df


# links = get_link_to_all_data_sets_for_state()
# links = get_data_links_for_aviation_sectors(links)
# class_data = convert_links_to_classes(links)
# print(class_data)

if __name__ == "__main__":
    links = get_link_to_all_data_sets_for_state()
    links = get_data_links_for_aviation_sectors(links)
    class_data = convert_links_to_classes(links)
    print(class_data)
    # with open('eia_dict_data.txt', 'w') as text_file:
    #     text_file.write(json.dumps(data))

    print("Link", data["California"]["jet fuel"].get_link())
    print("Json data", data["California"]["jet fuel"].get_data_json())
    print("Series ID", data["California"]["jet fuel"].get_series_id())
    print("Description", data["California"]["jet fuel"].get_description())
    print("State", data["California"]["jet fuel"].get_state())
    print("Units", data["California"]["jet fuel"].get_units())
    print("Updated date", data["California"]["jet fuel"].get_updated_date())
    print("Range Years", data["California"]["jet fuel"].get_range_years())
    print("Data Vals", data["California"]["jet fuel"].get_data_values())
    print("DF", data["California"]["jet fuel"].get_df())
    print("obj", data)
    print("obj", data["California"]["jet fuel"])
    combine_state_df_all(save=True)
