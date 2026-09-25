# Week 4: Vector Spatial Analysis

## Icebreaker

What is your favorite magical or mythological creature and why?

## Introductory business

* Isaac's seminar will be this afternoon (09/25) at 4:30pm Eastern (sent the zoom link in email) 

## Paper discussion
- Elle will be leading the discussion this week of [Wyatt et al 2021 "Ecological 
niche modelling and phylogeography reveal range shifts of pawpaw, a North 
American understorey tree"](https://onlinelibrary.wiley.com/doi/abs/10.1111/jbi.14054)

# Lab Exercise: Vector Spatial Analysis

* The usual intro update exercise: Go to your [JupyterHub](https://maine.cloudbank.2i2c.cloud/)
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

- How can vector operations answer ecological and conservation questions?
- Which observations fall inside protected areas, watersheds, or habitat polygons?
- How do buffers, intersections, and spatial joins change the unit of analysis?

## Concepts

- Spatial joins
- Intersection, union, and difference
- Buffers
- Nearest-neighbor operations
- Point-in-polygon analysis
- Distance matrices

## Python Tools

- pandas
- GeoPandas

## Applied Lab

Using species observations, protected areas, watersheds, roads, and habitat 
polygons, students ask which observations occur inside protected areas, how 
many species occur within 500 m of a road, and which sampling locations fall 
within each watershed.

## Assignment

Submit a vector spatial analysis report with maps, code, and short 
interpretations for at least three spatial questions.

- `docs/assignments/Assignment-04-VectorSpatialAnalysis.ipynb`

**Paper discussion leader next week:** Carly! Please select a paper for
the group to discuss before Sunday 09/27 6pm and send it around to the
class email list: bio597-fall2026-group@maine.edu
