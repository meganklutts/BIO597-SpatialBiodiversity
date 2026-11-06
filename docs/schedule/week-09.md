# Week 09: Gradient Forest: SDMs for genomic data

Use SNP genotypes and climate rasters to estimate environmental correlates of genetic turnover in *P. guttatus*.

## Icebreaker

Who is your favorite cartoon character and why?

## Paper discussion

Cancelled for this week

## Core Questions

- How can we apply an SDM framework to study changes in genetic variation within 
species as a function of environmental variation?
- How does Gradient Forest combine SNP-specific random forests into environmental turnover curves?
- How can we combine all the information from SNP-specific predictions to understand genome-wide 
turnover as a function of environmental variation?

## Concepts

- SNPs, VCF genotype calls, and individual alternate-allele dosage (0, 1, 2)
- One random forest per SNP
- Cumulative turnover curves and environmental thresholds
- PCA of transformed environments; shared map/biplot colors and environmental covariance arrows

## Python Tools

- [pyGF](https://github.com/isaacovercast/pygf)
- GeoPandas, pandas, NumPy, xarray/rioxarray, and Matplotlib

## Applied Lab

- [Lecture09: Gradient Forest and Genomic Turnover](../lectures/Lecture09-GradientForest.html)
- [Lab09: Gradient Forest](../labs/Lab09-GradientForest.ipynb)

Pull the latest course repository on [JupyterHub](https://maine.cloudbank.2i2c.cloud/).

Students read the *P. guttatus* VCF and sample coordinates, filter and sample up
to 256 SNPs, and extract 19 bioclimatic predictors. They fit SNP-specific forests,
inspect OOB scores and predictor importance, interpret cumulative turnover
curves, and map GF-transformed environments with a shared-color PCA biplot.
They compare the aggregate pattern with a single-SNP view and export diagnostics,
turnover coordinates, figures, and a GeoTIFF with one band per predictor.

## Assignment

Repeat the Lab09 workflow for another snake species and submit the completed
assignment notebook, diagnostics, turnover curves, maps, and exported turnover
raster. Identify an important predictor and the part of
its environmental gradient with the fastest modeled turnover. Compare the
aggregate and single-SNP biplots, explaining why their colors cannot be compared
directly. Discuss one limitation of OOB evaluation and one alternative to local
adaptation that could explain a genetic–environmental association.

- [Assignment09: Gradient Forest and Genomic Turnover](../assignments/Assignment-09-GradientForest.ipynb)

**Paper discussion leader next week:** **Braedon!** Please select a paper for the
group to discuss before Sunday 11/01 6pm and send it around to the class email
list: bio597-fall2026-group@maine.edu
