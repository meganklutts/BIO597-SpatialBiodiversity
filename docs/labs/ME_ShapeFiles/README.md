# Maine vector data

This directory contains vector layers used in Lab 04 and Assignment 04.

## Layers

### Maine conserved lands

- Source: Maine Natural Areas Program, Maine Department of Agriculture, Conservation and Forestry
- Dataset: Maine Conserved Lands
- Source page: https://www.maine.gov/dacf/mnap/assistance/conslands.htm
- Download item: https://maine.hub.arcgis.com/datasets/ad59f27a21f24f19bb005868a04b65a3
- Description: Approximate ownership boundaries for federal, state, municipal, nonprofit, and easement conservation lands in Maine.
- Important limitation: The boundaries are an inventory for planning and do not represent legal surveys or imply public access.

### Maine HUC12 watersheds

- Source: U.S. Geological Survey Watershed Boundary Dataset
- Service layer: https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer/6
- Description: HUC12 watershed polygons associated with Maine, with watershed codes and names. Coordinates were simplified by approximately 0.0001 degree when the Maine subset was downloaded so the teaching file remains manageable.
- Important limitation: Some polygons extend beyond Maine because watersheds follow drainage boundaries rather than state boundaries.

### Maine primary and secondary roads

- Source: U.S. Census Bureau TIGER/Line
- Dataset: 2023 Maine Primary and Secondary Roads
- Download: https://www2.census.gov/geo/tiger/TIGER2023/PRISECROADS/tl_2023_23_prisecroads.zip
- Description: Primary roads and major secondary roads. This is not a complete inventory of every local road.

## Shapefile components

An Esri shapefile consists of several files with the same base name. Keep the `.shp`, `.shx`, `.dbf`, and `.prj` files together. GeoPandas opens the `.shp` file.
