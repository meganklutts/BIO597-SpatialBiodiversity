# Week 5: Raster Data and Environmental Covariates

## Icebreaker

Are there any foods you disliked as a child, but love (or at least tolerate) now?

## Introductory business

* Fair warning: The icebreaker question next week is going to be "What is a good icebreaker question?"

## Paper discussion
- Carly will be leading the discussion this week of [Van Nuland et al 2025 "Global hotspots of mycorrhizal fungal richness are poorly protected"](https://www.nature.com/articles/s41586-025-09277-4)

# Lab Exercise: Raster Data and Environmental Covariates

* [First, a brief lecture on raster data and environmental covariates](../lectures/Lecture05-RasterData.html)

* Next, the usual intro update exercise: Go to your [JupyterHub](https://maine.cloudbank.2i2c.cloud/)
and pull the latest version of the class github repository.

??? note "Commands to pull the latest version of the class repository"

    1. Change directory to your local copy of the course repo
    2. Pull the latest copy of 'upstream' which is my copy of the class website
    3. Push the changes to your own github repo
    ```
    cd ~/BIO597-SpatialBiodiversity/`
    git upstream
    git push
    ```

## Core Questions

- How do rasters represent environmental variation?
- How do resolution, extent, alignment, and NoData values affect biodiversity analysis?
- Which environmental covariates are biologically meaningful for a study system?

## Concepts

- Raster versus vector data
- Cells, pixels, resolution, extent, and NoData
- Raster alignment and extraction
- Environmental covariates including elevation and climate
- Ecological interpretation of predictors

## Python Tools

- geopandas
- rioxarray

## Applied Lab

Students extract elevation, temperature, precipitation, and other bioclim
values at species occurrence locations, producing an analysis table that 
combines species, coordinates, and environmental covariates.

## Assignment

Submit a raster spatial analysis report with maps, code, and short
interpretations for at least three spatial questions.

- `docs/assignments/Assignment-05-RasterData.ipynb`

**Paper discussion leader next week:** Drew! Please select a paper for
the group to discuss before Sunday 10/04 6pm and send it around to the
class email list: bio597-fall2026-group@maine.edu
