# Lecture11 figure provenance

Run from the repository root in the Lab11 Python environment:

```bash
python docs/lectures/assets/Lecture11-build-figures.py
```

The script requires GeoPandas, Rasterio, NumPy, pandas, SciPy, Matplotlib,
scikit-learn and `gdmbayes`. It reuses the original amphibian vector symbols in
`Lecture10-build-figures.py`; importing that helper does not rebuild Lecture10.
There are no network downloads and no dependencies on instructor answer keys.

## Empirical figures

All empirical panels use `docs/data/amphibians.geojson`, the Maine state
boundary in `docs/labs/ME_ShapeFiles`, and all 19 clipped WorldClim rasters in
`docs/data/bioclim_ME`. They use original observations, not the synthetic Lab10
parks or the California assignment sample. Named species within the state are
retained, and taxonomy is used as supplied. Input hashes and exact settings are
in `Lecture11-example-results.json`.

- **Grid and richness:** EPSG:26919, origin (320,000, 4,720,000) m, and nested
  10/20/40 km cells match Lab11. Only occupied cells become sites. Cell outlines
  are clipped to Maine; original square centers are used for distances. Coastal
  cells contain varying land area. Richness maps share a color scale.
- **Sampling:** occurrence points, record counts and richness describe the
  archive's observation pattern. Repeated locations are retained. A missing
  cell is not a surveyed absence or an empty community.
- **Opening occurrence map:** `Lecture11-occurrences.png` shows the 14,466
  named-species records within the Maine boundary before defining grid sites.
  It introduces the question "How do we delineate communities?" without adding
  community boundaries or aggregating the records.
- **Distance decay:** Jaccard uses presence/absence. Each pair is calculated
  once. Black lines and comparison curves are arithmetic means in 50 km bands,
  not fitted regressions, confidence intervals or independent-pair tests.
- **Local differences:** mean Jaccard to sampled neighbors within 1.5 cell
  widths, excluding the focal cell. Sites without a neighbor have missing
  values. This is total dissimilarity, not a turnover partition or a rate per km.
- **Climate:** unweighted means of valid raster pixels intersecting each
  clipped site, including edge pixels (`all_touched=True`). These are
  approximate zonal means. BIO1/BIO12 maps are illustrative; every full model
  uses all 19 variables with the revised lab's names and order.
- **GDM:** standard `GDM(geo=True, knots=0)` at each grain. Missing-climate
  sites are removed, community rows aligned, and Jaccard pairs recomputed.
  Geography-only and full models within a grain use identical sites. Fit is
  training deviance explained. Curves and importance are conditional fitted
  contributions; correlated predictors can share information.
- **PCA:** at 20 km, sum each predictor's weighted spline bases to obtain 19
  transformed columns. Center and run PCA without standardization. PC1 and PC2
  are separately min–max scaled into red and green; blue is 0.5. Map and biplot
  use identical site colors. Geographic distance is excluded from the site-level
  transformation. Loadings are component directions multiplied by the square
  root of component variance. Select the two longest PC1/PC2 vectors, independent
  of sign. Their original-variable maps aid interpretation. Unshown PCs retain
  additional variation; colors are not calibrated Jaccard distances or richness.
- **Sensitivity:** minimum-five filtering is shown for site counts and
  descriptive distance decay. It does not standardize observation effort. These
  panels do not claim a held-out prediction test or show refitted sensitivity
  models.

The figure builder refits all 19-variable models directly. It deliberately does
not read older two-predictor Lab11 exports. Summary values and PCA loadings are
also saved as `Lecture11-grain-comparison.csv` and `Lecture11-pca-loadings.csv`.

## Teaching illustrations

All species lists, environmental values and geographic positions in SVG
cartoons are invented. They are not inferred amphibian ranges or habitat models.
Species letters and colors are labels; the symbols are not identification keys.

- `identity`: ABC/ABC/DEF/DEF lists all have richness three.
- `grain`: the same 85 toy points in a fixed 80 km extent with 10/20/40 km grids.
- `pooling`: AB, BC, CD and D have mean richness 1.75 and pooled richness four.
- `boundary`: shifting a grid changes whether two fixed records share a cell.
- `pairs`: ABC, ABD and DEF have Jaccard values 0.5, 0.8 and 1.0. The
  30–40–50 km triangle supplies consistent illustrative geographic distances.
- `mechanisms`: environmental sorting, barriers/history and observation
  differences are hypotheses, not statistically separated effects.
- `dependence`: AB and AC share the information about site A.
- `local`: three identical and four disjoint neighbors give mean Jaccard 4/7;
  an unsampled neighbor is excluded. The focal list has three species.
- `gdm-inputs`: two sites with ABC/ACD give Jaccard 0.5. Only two of 19
  environmental values are written out for readability.
- `stretching`: a logistic-shaped monotone transformation compares two equal
  2 °C intervals. The curve is invented, not a Maine threshold.
- `gdm-link`: ecological-distance contributions 0.2 + 0.5 + 0.4 + 0.3 = 1.4
  give expected dissimilarity `1 - exp(-1.4)`, about 0.753.
- `pca-workflow` and `lab-workflow`: conceptual operations; the bars and points
  are illustrative rather than fitted values.
- `validation`: random edge splitting reuses sites; holding out a group of
  sites permits testing pairs composed of new sites. The lab itself reports
  training fit rather than performing this validation.
- `Lecture10-nestedness.svg`, reused from the preceding lecture, compares
  AB/ABCD with ABC/ACD; both have total Jaccard dissimilarity 0.5.

The conceptual and methodological sources are linked on relevant slides and in
the lecture's reading slide. No figures are copied from published papers.
