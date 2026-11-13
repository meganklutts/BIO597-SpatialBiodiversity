# California state boundary

`California_State_Boundary.shp` and its `.shx`, `.dbf`, `.prj` and `.cpg`
sidecars describe California, including islands, in EPSG:4326.

Source: [2024 U.S. Census cartographic state boundaries, 1:500,000](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip),
filtered to `STUSPS=CA`. These are generalized cartographic boundaries suitable
for the assignment's grid analysis. `source.json` records retrieval details and
the source archive checksum. Preparation code is
`scripts/prepare_california_data.py` in the repository root.
