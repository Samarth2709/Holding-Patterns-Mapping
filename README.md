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
│       ├── HighCenter2006.json
│       ├── HighSector2006.json
│       ├── LowCenter2006.json
│       ├── LowSector2006.json
│       └── SuperSector2006.json
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
│   └── cy18-commercial-service-enplanements.xlsx
├── abbreviation_to_full_state_name.json
├── edit_major_airports_rank.py
├── eia_data_pull.py
└── EIA_live_map-copy.py 
```

EIA_live_map-copy.py is the main file which creates maps

Necessary libraries:
- Pandas
- dash
- dash_core_components
- dash_html_components
- plotly
- eia_data_pull
- requests



