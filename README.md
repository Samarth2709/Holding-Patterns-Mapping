Creates a site with 2 maps: one displaying raw carbon 
emission data, and the other displaying carbon emissions 
per major airport

Files necessary: 
```
Holding_patterns_mapping
├── assets
│   └── reset.css
├── Avitaion_Centers
│   └── Unziped-json
│       └── LowCenter2006.json
├── Geo-json
│   └── states.json
├── Major_airports
│   ├── cy01_primary.xlsx
│   ├── cy02_all_primary.xlsx
│   ├── cy03_all_primary.xlsx
│   ├── cy04_primary_boardings.xlsx
│   ├── cy05_primary_np_commercial.xlsx
│   ├── cy06_primary_np_comm.xlsx
│   ├── cy07_primary_np_comm.xlsx
│   ├── cy08_primary_np_comm.xlsx
│   ├── cy09_cs_enplanements.xlsx
│   ├── cy10_primary_enplanements.xlsx
│   ├── cy11_primary_enplanements.xlsx
│   ├── CY12CommercialServiceEnplanements.xlsx
│   ├── cy13-commercial-service-enplanements.xlsx
│   ├── cy14-commercial-service-enplanements.xlsx
│   ├── cy15-commercial-service-enplanements.xlsx
│   ├── cy16-commercial-service-enplanements.xlsx
│   ├── cy17-commercial-service-enplanements.xlsx
│   ├── cy18-commercial-service-enplanements.xlsx
│   └── Major_airports.xlsx
├── abbreviation_to_full_state_name.json
├── edit_major_airports_rank.py
├── get_sector_mjr_airport.py
├── eia_data_pull.py
└── EIA_live_map-copy.py 
```

EIA_live_map-copy.py is the main file which creates maps. When EIA_live_map-copy is run, it creates a link that displays
the map. To have the map embedded into the html of the project site, the python program must be running on the user's 
computer. To fully run program (pull new EIA data instead of read xlsx), load_data must equal False 
(ln. 239 EIA_live_map-copy). To load existing data from all_data_df.xlsx, load_data must equal True.
(ln. 239 EIA_live_map-copy).   

Necessary libraries:
- Pandas
- dash
- dash_core_components
- dash_html_components
- plotly
- eia_data_pull
- requests


eia_data_pull.py creates functions to obtain EIA carbon emission data using the python requests library and the EIA's 
api. It also has functions that format data such as the updated time and the CO2 value for all fuel(from million metric
tons to metric tons).

A dictionary is used to store the data values for each state and fuel type and then converted to the CarbonEmission 
class (ln. 19 EIA_live_map-copy). A dataframe is created from the class with the number of major airports for each state
and the geojson id (to connect each data point with state region on json borders)(ln. 245-247 EIA_live_map-copy).

edit_major_airports_rank.py reads all enplanement xlsx spreadsheets and formats it into one dataframe. Dataframe is used
to calculate CO2 per major airport.

get_sector_mjr_airport.py gets data for plotting major airports and gets json data for aviation center borders. 
Aviation center border data is formatted from a GeometryCollection to a FeatureCollection (go.Choropleth function for 
plotting regions only accepts FeatureCollection).