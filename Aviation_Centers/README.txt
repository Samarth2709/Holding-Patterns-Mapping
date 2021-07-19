Boundary files use GeoJSON format, see https://geojson.org/

Example:
{
  "type": "GeometryCollection",
  "geometries": [
    {
      "coordinates": 
        [
          [ -105.34167, 36.716667 ],
          [ -105.0, 36.716667 ],
          [ -103.15, 37.308334 ], ...
          [ -105.34167, 36.716667 ]
        ],
      "type": "Polygon",
      "name": "ZAB"
    },
    { ... },
    { ... }
  ]
}

Supported file extensions:
*.json -- plain text file in JSON format.
*.json.gz -- gzip file of a plain text file in JSON format.
*.json.zip -- zip file of a plain text file in JSON format.
