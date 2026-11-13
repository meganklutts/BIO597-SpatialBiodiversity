"""Prepare Assignment11 inputs; see docs/data/CA_data_README.md.

    python scripts/prepare_california_data.py
    python scripts/prepare_california_data.py --gbif-key DOWNLOAD_KEY
    python scripts/prepare_california_data.py --gbif-zip /path/to/DOWNLOAD_KEY.zip
    python scripts/prepare_california_data.py --gbif-csv docs/data/0002705-261110092616502.csv

The default action prepares the California boundary, all 19 climate layers,
and a GBIF bulk-download request. GBIF authentication is performed by the user,
not this script. A completed download can then be fetched publicly by key or
imported from a local SIMPLE_CSV ZIP. No partial search export is substituted.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import urllib.request
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/data"
BOUNDARY = DATA / "CA_ShapeFiles/California_State_Boundary.shp"
CLIMATE_SOURCE = ROOT / "docs/labs/bioclim"
CENSUS_URL = "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip"
GBIF_API = "https://api.gbif.org/v1"
USER_AGENT = "BIO597-SpatialBiodiversity-teaching-data/1.0"


def read_url(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def save_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def prepare_boundary(archive=None):
    with TemporaryDirectory() as temporary:
        if archive is None:
            archive = Path(temporary) / "states.zip"
            archive.write_bytes(read_url(CENSUS_URL))
        states = gpd.read_file(archive)
        california = states[states.STUSPS == "CA"].to_crs(4326)
        if len(california) != 1 or not california.is_valid.all():
            raise ValueError("Expected one valid California state feature.")
        BOUNDARY.parent.mkdir(parents=True, exist_ok=True)
        california.to_file(BOUNDARY, driver="ESRI Shapefile", index=False)
        save_json(BOUNDARY.parent / "source.json", {
            "source": CENSUS_URL, "retrieved_utc": utc_now(),
            "description": "2024 Census cartographic state boundary, 1:500,000; STUSPS=CA",
            "archive_sha256": hashlib.sha256(Path(archive).read_bytes()).hexdigest(),
            "output_crs": "EPSG:4326", "includes_islands": True,
        })
    return california


def prepare_climate(california, source=CLIMATE_SOURCE):
    paths = [Path(source) / f"wc2.1_2.5m_bio_{n}.tif" for n in range(1, 20)]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    destination = DATA / "bioclim_CA"
    destination.mkdir(parents=True, exist_ok=True)
    layers = []
    for path in paths:
        with rasterio.open(path) as raster:
            shapes = california.to_crs(raster.crs).geometry
            image, transform = mask(raster, shapes, crop=True)
            profile = raster.profile.copy()
            profile.update(height=image.shape[1], width=image.shape[2],
                           transform=transform, compress="deflate")
            output = destination / path.name
            with rasterio.open(output, "w", **profile) as target:
                target.write(image)
                target.update_tags(**raster.tags())
                target.scales = raster.scales
                target.offsets = raster.offsets
        with rasterio.open(output) as clipped:
            layers.append({"file": output.name, "shape": list(clipped.shape),
                           "crs": str(clipped.crs), "resolution": list(clipped.res),
                           "valid_pixels": int(clipped.read(1, masked=True).count()),
                           "sha256": hashlib.sha256(output.read_bytes()).hexdigest()})
        print("Clipped", output.name, flush=True)
    save_json(destination / "source.json", {
        "created_utc": utc_now(), "source_directory": "docs/labs/bioclim",
        "source": "https://www.worldclim.org/data/worldclim21.html",
        "climate_period": "1970–2000", "version": "WorldClim 2.1, 2.5 arc-minutes",
        "boundary": "docs/data/CA_ShapeFiles/California_State_Boundary.shp",
        "method": "Crop and mask using native raster pixel centers; no resampling or reprojection",
        "layers": layers,
    })


def prepare_gbif_request(california):
    xmin, ymin, xmax, ymax = california.total_bounds
    # Counter-clockwise rectangle. The importer applies the exact state polygon.
    rectangle = (f"POLYGON(({xmin} {ymin},{xmax} {ymin},{xmax} {ymax},"
                 f"{xmin} {ymax},{xmin} {ymin}))")
    request = {
        "sendNotification": True, "format": "SIMPLE_CSV",
        "predicate": {"type": "and", "predicates": [
            {"type": "equals", "key": "TAXON_KEY", "value": "131"},
            {"type": "equals", "key": "HAS_COORDINATE", "value": "true"},
            {"type": "within", "geometry": rectangle},
        ]},
    }
    save_json(DATA / "CA_amphibians.gbif-request.json", request)


def import_gbif(archive, output=None, metadata=None):
    """Keep all georeferenced Amphibia records inside California.

    Retain unidentified species, absence records and issue flags in the data;
    the assignment explicitly selects named, present species for analysis.
    Distinct GBIF records at identical coordinates are retained.
    """
    output = Path(output) if output else DATA / "CA_amphibians.geojson"
    california = gpd.read_file(BOUNDARY).to_crs(4326)
    columns = ["gbifID", "species", "scientificName", "taxonRank", "datasetKey",
               "decimalLongitude", "decimalLatitude", "coordinateUncertaintyInMeters",
               "year", "basisOfRecord", "occurrenceStatus", "license", "issue"]
    frames = []
    source_records = valid_coordinate_records = 0
    with zipfile.ZipFile(archive) as zipped:
        csvs = [item for item in zipped.infolist()
                if item.filename.endswith(".csv") and "/" not in item.filename]
        if len(csvs) != 1:
            raise ValueError("Expected a GBIF SIMPLE_CSV ZIP with one root-level occurrence CSV.")
        with zipped.open(csvs[0]) as stream:
            for table in pd.read_csv(stream, sep="\t", dtype="string", chunksize=50000):
                source_records += len(table)
                required = {"gbifID", "class", "species", "occurrenceStatus",
                            "decimalLongitude", "decimalLatitude"}
                if not required.issubset(table.columns):
                    raise ValueError(f"Missing GBIF columns: {required - set(table.columns)}")
                table = table[table["class"] == "Amphibia"].copy()
                for name in ["decimalLongitude", "decimalLatitude", "coordinateUncertaintyInMeters", "year"]:
                    if name in table:
                        table[name] = pd.to_numeric(table[name], errors="coerce")
                table = table.dropna(subset=["decimalLongitude", "decimalLatitude"])
                table = table[table.decimalLongitude.between(-180, 180)
                              & table.decimalLatitude.between(-90, 90)]
                valid_coordinate_records += len(table)
                points = gpd.GeoDataFrame(
                    table, geometry=gpd.points_from_xy(table.decimalLongitude, table.decimalLatitude),
                    crs=4326,
                )
                points = gpd.clip(points, california)
                keep = [name for name in columns if name in points.columns] + ["geometry"]
                frames.append(points[keep])
    if not frames:
        raise ValueError("The archive contains no occurrence rows.")
    records = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=4326)
    if records.empty:
        raise ValueError("No amphibian coordinates fall within the California boundary.")
    if records.gbifID.duplicated().any():
        raise ValueError("Duplicate gbifID values in the export; inspect before importing.")
    # Write compact GeoJSON while retaining GBIF IDs exactly as strings.
    output.write_text(records.to_json(drop_id=True, na="null", separators=(",", ":")) + "\n")
    provenance = {
        "created_utc": utc_now(), "source": "GBIF SIMPLE_CSV occurrence download",
        "archive_name": Path(archive).name,
        "archive_sha256": hashlib.sha256(Path(archive).read_bytes()).hexdigest(),
        "archive_records": source_records, "valid_amphibian_coordinate_records": valid_coordinate_records,
        "california_records": len(records), "species_labels": int(records.species.nunique()),
        "spatial_filter": "Exact California Census boundary, including boundaries and islands",
        "date_basis_quality_filters": "None; raw occurrenceStatus and issue fields retained",
        "download": metadata,
    }
    save_json(output.with_suffix(".source.json"), provenance)
    print(f"Saved {len(records):,} real California records to {output}", flush=True)
    return records


def sample_gbif_csv(source, target_mb=20, seed=11):
    """Write a uniform random California sample in the Maine GeoJSON schema.

    Choose a fixed sample size from the mean serialized feature size, so all
    eligible records have the same inclusion probability. The byte target is
    approximate; it does not favor shorter species names or feature records.
    """
    if not np.isfinite(target_mb) or target_mb <= 0:
        raise ValueError("target_mb must be positive and finite.")
    source = Path(source)
    columns = ["gbifID", "species", "decimalLongitude", "decimalLatitude",
               "coordinateUncertaintyInMeters", "year"]
    frames = []
    source_records = 0
    california = gpd.read_file(BOUNDARY).to_crs(4326)
    for table in pd.read_csv(source, sep="\t", dtype="string", chunksize=50000,
                             usecols=columns + ["class", "occurrenceStatus"]):
        source_records += len(table)
        table = table[(table["class"] == "Amphibia")
                      & table.occurrenceStatus.isin(["PRESENT", "DETECTED"])].copy()
        table["species"] = table.species.replace(r"^\s*$", pd.NA, regex=True)
        for name in columns:
            if name != "species":
                table[name] = pd.to_numeric(table[name], errors="coerce")
        table = table.dropna(subset=["gbifID", "decimalLongitude", "decimalLatitude"])
        table = table[table.decimalLongitude.between(-180, 180)
                      & table.decimalLatitude.between(-90, 90)]
        table["gbifID"] = table.gbifID.astype("int64")
        for name in columns[2:]:
            table[name] = table[name].astype("float64")
        points = gpd.GeoDataFrame(
            table[columns],
            geometry=gpd.points_from_xy(table.decimalLongitude, table.decimalLatitude),
            crs=4326,
        )
        frames.append(gpd.clip(points, california))
    if not frames:
        raise ValueError("The CSV contains no records.")
    records = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=4326)
    if records.empty or records.gbifID.duplicated().any():
        raise ValueError("Expected eligible California records with unique GBIF IDs.")
    features = [json.dumps(feature, ensure_ascii=False, allow_nan=False)
                for feature in records.iterfeatures(na="null", drop_id=True)]
    header = ('{\n"type": "FeatureCollection",\n"name": "CA_amphibians",\n'
              '"crs": { "type": "name", "properties": { "name": '
              '"urn:ogc:def:crs:OGC:1.3:CRS84" } },\n"features": [\n')
    footer = "\n]\n}\n"
    average_bytes = sum(len(feature.encode("utf-8")) + 2 for feature in features) / len(features)
    target_bytes = round(target_mb * 1_000_000)
    n = min(len(records), int((target_bytes - len(header) - len(footer) + 2) / average_bytes))
    if n < 1:
        raise ValueError("The size target is too small for one feature.")
    indices = np.sort(np.random.default_rng(seed).choice(len(records), n, replace=False))
    output = DATA / "CA_amphibians.geojson"
    with output.open("w", encoding="utf-8") as stream:
        stream.write(header)
        stream.write(",\n".join(features[i] for i in indices))
        stream.write(footer)
    sample = records.iloc[indices].copy()
    save_json(output.with_suffix(".source.json"), {
        "created_utc": utc_now(), "source": "User-provided GBIF occurrence CSV",
        "source_file": source.name,
        "download_key": source.stem,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_records": source_records, "eligible_california_records": len(records),
        "sample_records": len(sample), "sample_species": int(sample.species.nunique()),
        "eligible_species": int(records.species.nunique()),
        "sampling": "Uniform random records without replacement; no species or spatial stratification",
        "random_seed": seed, "target_bytes": target_bytes, "output_bytes": output.stat().st_size,
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "filters": "Amphibia; PRESENT or DETECTED; valid coordinates inside or on California boundary; unidentified species retained as null",
        "sample_unidentified_species_records": int(sample.species.isna().sum()),
        "schema_reference": "docs/data/amphibians.geojson",
        "fields": columns, "crs": "OGC:CRS84 (longitude, latitude)",
    })
    print(f"Saved {len(sample):,} records ({output.stat().st_size / 1_000_000:.3f} MB) to {output}", flush=True)
    return sample


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary-archive", type=Path)
    parser.add_argument("--climate-source", type=Path, default=CLIMATE_SOURCE)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--gbif-key", help="A completed GBIF bulk-download key")
    group.add_argument("--gbif-zip", type=Path, help="A local GBIF SIMPLE_CSV ZIP")
    group.add_argument("--gbif-csv", type=Path, help="A local tab-separated GBIF CSV to randomly sample")
    parser.add_argument("--target-mb", type=float, default=20, help="Approximate GeoJSON MB for --gbif-csv")
    parser.add_argument("--seed", type=int, default=11, help="Random seed for --gbif-csv")
    args = parser.parse_args()
    if args.gbif_key:
        metadata = json.loads(read_url(f"{GBIF_API}/occurrence/download/{args.gbif_key}"))
        if metadata["status"] != "SUCCEEDED":
            raise ValueError(f"Download is {metadata['status']}; wait until SUCCEEDED.")
        with TemporaryDirectory() as temporary:
            archive = Path(temporary) / f"{args.gbif_key}.zip"
            archive.write_bytes(read_url(metadata["downloadLink"]))
            import_gbif(archive, metadata=metadata)
    elif args.gbif_zip:
        import_gbif(args.gbif_zip)
    elif args.gbif_csv:
        sample_gbif_csv(args.gbif_csv, target_mb=args.target_mb, seed=args.seed)
    else:
        california = prepare_boundary(args.boundary_archive)
        prepare_climate(california, args.climate_source)
        prepare_gbif_request(california)
        print("Boundary, 19 climate rasters, and GBIF request prepared.")


if __name__ == "__main__":
    main()
