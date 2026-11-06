# Lecture 09 figures

The lecture follows `docs/labs/Lab09-GradientForest.ipynb`, the Week 09 notebook
present in this checkout. The fitted PNGs were generated with Matplotlib.
The conceptual SVG diagrams are drawn with a Python standard-library script;
their sample positions, genotypes, model rules, and scores are invented teaching
examples. No AI-generated artwork or third-party figure reproductions are used.

## Data and fit

The fitted figures use the matching example inputs from the local
[pyGF repository](https://github.com/isaacovercast/pygf):

- `examples/Pguttatus_coords.txt`: 36 individual sample coordinates.
- `examples/Pguttatus.vcf`: diploid SNP genotype calls.
- `envs/wc2.1_2.5m_bio_*.tif`: 19 bioclimatic layers.

These are the upstream counterparts of the JupyterHub shared files referenced
by the course notebook. The lecture does not assume that the Hub files are
byte-identical; the input SHA-256 hashes, source commit, software versions, and
fit settings used for these figures are recorded in
[Lecture09-example-results.json](Lecture09-example-results.json).
No VCF or climate raster is copied into the lecture assets.

The fit uses the notebook settings: call rate ≥ 0.8, MAF ≥ 0.05, one SNP per
RAD contig, up to 256 SNPs, 100 trees per SNP, approximate conditional
permutations (`max_level=2`), seed 42, and retained response curves. Of the 256
SNPs, 136 contribute and 120 have nonpositive OOB skill. The highest-ranked
predictor is `bio18` (precipitation of the warmest quarter). These are results
for this subset and model configuration, not evidence of adaptive causation.

## Figure guide

| Asset | Meaning |
| --- | --- |
| `Lecture09-sites.png` | Actual example sample coordinates; no species range is inferred. |
| `Lecture09-oob.png` | SNP OOB R² distribution and inclusion status. |
| `Lecture09-importance.png` | Six highest mean allocated OOB R² values. |
| `Lecture09-curves.png` | Four leading cumulative predictor curves, with a common y scale. |
| `Lecture09-turnover-explained.png` | **Invented teaching values**, showing opposite dosage responses and a cumulative turnover curve. This is a conceptual illustration, not a fit to those toy responses. |
| `Lecture09-turnover-map.png` | The transformed `bio18` coordinate across the buffered raster region. High values are cumulative position, not a local rate. |
| `Lecture09-biplot.png` | Aggregate transformed-environment PCA map and biplot. |
| `Lecture09-snp-biplot.png` | Independent PCA/color calibration for `RAD_11467:26:C:A`, the highest-OOB-R² SNP. |

Map calculations use a 20% buffer around sites and stride 4. PCA uses complete
transformed raster cells, centered without scaling to unit variance. The first
three PCs explain approximately 69.2%, 14.4%, and 10.2% of variance in the
aggregate view. PC1/2 determine plotted positions; PC1/2/3 supply RGB channels,
scaled at the regional 2nd–98th percentiles. Separate response maps do not share
color calibrations. Environmental arrows are PCA covariance loadings.

## Conceptual diagrams

The lecture now uses figures in place of its comparison and mechanism tables.
The current slide sequence is preserved, including the instructor's removals.

| SVG asset | Visual explanation |
| --- | --- |
| `Lecture09-response-cartoon.svg` | Same environmental predictors, different occurrence versus genetic responses. |
| `Lecture09-dosage-cartoon.svg` | Paired allele copies become dosage 0, 1, or 2; missing calls remain separate. |
| `Lecture09-filtering-cartoon.svg` | Call rate, minor allele frequency, one SNP per RAD contig, and a reproducible subset. |
| `Lecture09-snp-forests.svg` | The same twelve samples A–L appear in the same temperature–rainfall positions for three SNPs. **White = 0, gray = 1, black = 2** alternate copies. Each SNP has its own forest. |
| `Lecture09-oob-cartoon.svg` | Bootstrap samples include or exclude A; only trees excluding A supply its OOB prediction. |
| `Lecture09-r2-cartoon.svg` | Exact toy R² values: observed dosages 0, 0, 1, 1, 2, 2; perfect predictions give 1, the constant mean gives 0, and reversed predictions give −3. |
| `Lecture09-permutation-cartoon.svg` | Shuffle temperature while retaining sample dosages and a fixed prediction rule. Toy MSE rises from 0 to 8/6 ≈ 1.33. |
| `Lecture09-correlation-cartoon.svg` | Marginal shuffling versus shuffling within coarse climate groups. Bands symbolize approximate grouping, not actual fitted tree partitions. |
| `Lecture09-allocation-cartoon.svg` | A 3:1 importance ratio allocates OOB R² 0.40 as 0.30 and 0.10; average allocations across contributing SNPs. |
| `Lecture09-splits-cartoon.svg` | Useful splits → smoothed, density-corrected mass → cumulative turnover. Shapes are illustrative, not a numeric fit. |
| `Lecture09-transform-cartoon.svg` | Equal raw intervals transform into different distances according to curve slope. |
| `Lecture09-coverage-cartoon.svg` | NoData masking, clamping outside ranges, and unfamiliar combinations within separate predictor ranges. |
| `Lecture09-arrows-cartoon.svg` | Enlarged schematic PCA scores and covariance arrows for interpreting direction, relative length, and proximity. |
| `Lecture09-inference-cartoon.svg` | Identical observed dosage patterns can arise under different candidate causal explanations. |
| `Lecture09-workflow-cartoon.svg` | An illustrated lab checklist from aligned samples through exports. |

The dosage grayscale is repeated across the allele, SNP, OOB, and genotype
prediction figures. Predictor colors (teal and coral) have separate legends and
do not encode dosage. Real biplot RGB colors retain their documented PCA meaning.

## Reproduction

Rebuild the conceptual diagrams without third-party dependencies:

```sh
python docs/lectures/assets/Lecture09-build-diagrams.py
```

Run in an environment with pyGF and its notebook dependencies installed:

```sh
MPLCONFIGDIR=/tmp/bio597-mpl python docs/lectures/assets/Lecture09-build-figures.py --pygf-root /path/to/pyGF
```

The script validates sample alignment, finite predictors, monotone curves,
curve endpoints, and conservation of mean retained OOB R². It saves the PNGs,
fit metadata, SNP diagnostics, and predictor importance beside this file.

The lecture links to the existing course notebook rather than copying it.
Its single-SNP biplot cell currently uses an upstream-relative `../envs` path;
on JupyterHub, use the same shared bioclim directory as the aggregate biplot.

## Method sources

- [Ellis, Smith & Pitcher (2012)](https://doi.org/10.1890/11-0252.1): original Gradient Forest framework.
- [pyGF README](https://github.com/isaacovercast/pygf): implemented allocation, smoothing, conditional permutations, genotype handling, mapping, and inference limits. This implementation does not claim numerical parity with R gradientForest.
- [Scikit-learn OOB example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html), [R²](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html), and [permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html).
- [WorldClim variable definitions](https://www.worldclim.org/data/bioclim.html): BIO18 is precipitation of the warmest quarter; BIO19 is precipitation of the coldest quarter; BIO12 is annual precipitation; BIO9 is mean temperature of the driest quarter. Check source raster scaling before assigning units to plotted values.
