# California data for Assignment 11

## Available inputs

| Input | Location | Status |
| --- | --- | --- |
| California state boundary | `CA_ShapeFiles/California_State_Boundary.shp` | Prepared |
| All 19 clipped WorldClim layers | `bioclim_CA/wc2.1_2.5m_bio_1.tif` through `..._19.tif` | Prepared |
| Random sample of California amphibian occurrences | `CA_amphibians.geojson` | Prepared, about 20 MB |

## Amphibian occurrences

The source is the supplied GBIF tab-separated file
`0002705-261110092616502.csv`, from download
[0002705-261110092616502](https://www.gbif.org/occurrence/download/0002705-261110092616502).
Use the DOI shown on that download page to cite the source snapshot.

The source has **352,239 records**. After retaining detected amphibians
with valid coordinates inside or on the California boundary, including islands,
**344,263 records** are eligible. A uniform random sample without
replacement contains **71,578 records**, with **89 named species**, in a
**20,004,584-byte** GeoJSON (about 20 MB, using decimal megabytes).
Records without species names are retained as null: there are
8,749 such records in the sample. The assignment drops these
before building community matrices.

The GeoJSON matches `amphibians.geojson`: a longitude/latitude Point
FeatureCollection in CRS84 with these six properties:

- `gbifID`: integer
- `species`: species name or null
- `decimalLongitude`, `decimalLatitude`: numbers matching the Point coordinates
- `coordinateUncertaintyInMeters`: number or null
- `year`: number or null

Sampling uses seed **11** and does not balance species or locations. Some rarely
recorded species may disappear from the sample. Distinct GBIF records at the
same location remain separate records. Dates, uncertainty, and GBIF issue flags
are not used to filter the records. The six-field GeoJSON omits the other source
columns; they remain available in the original CSV.

Recreate the sample from the repository root, using an environment with NumPy,
Pandas, GeoPandas and Rasterio:

```bash
python scripts/prepare_california_data.py \
  --gbif-csv docs/data/0002705-261110092616502.csv \
  --target-mb 20 --seed 11
```

The sample count is determined from the mean serialized feature size of the
eligible records. Every eligible record has the same selection probability;
the output size is approximate. `CA_amphibians.source.json` records the source
and output checksums, counts, filters, seed, schema, and actual byte size.
The source CSV is left unchanged.

## Boundary and climate sources

The [2024 U.S. Census cartographic state boundary](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip)
is at 1:500,000 scale and includes California's islands. The California feature
(`STUSPS=CA`) is saved in EPSG:4326 with its Shapefile sidecar files.
`CA_ShapeFiles/source.json` records the archive URL, checksum and retrieval date.

The climate inputs come from the full WorldClim 2.1, 2.5 arc-minute rasters in
`docs/labs/bioclim`, summarizing 1970–2000. Each is cropped and masked to the
California boundary using native pixel centers. Resolution, values, CRS,
NoData, scales and offsets are preserved; there is no resampling. The
`bioclim_CA/source.json` manifest records output hashes and valid-pixel counts.
See the [WorldClim documentation](https://www.worldclim.org/data/worldclim21.html).

## Rebuild the boundary and climate layers

From the repository root:

```bash
python scripts/prepare_california_data.py
```

This downloads the Census archive and reads the existing global climate
rasters. `--boundary-archive /path/to/states.zip` can use a local copy of the
official archive. `--climate-source /path/to/global/bioclim` changes only the
global raster input directory. The original global rasters and Maine data are
left untouched.
