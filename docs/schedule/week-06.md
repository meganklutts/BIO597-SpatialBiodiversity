# Week 6: Species Distribution Modeling

## Icebreaker

What is a good icebreaker question?

## Paper discussion

- Drew will be leading the discussion this week of Rzeszowski et al 2026 
["Divergent Environmental Niches and Climate Vulnerabilities of Jonah Crab 
(Cancer borealis) and Atlantic Rock Crab (Cancer irroratus)"](https://doi.org/10.1111/fog.70078) 
## A tour of Github features
[A quick tour through some of githubs more useful features for biologists](../lectures/Lecture-GitHubTour.html)

# Lab Exercise: A simple species distribution model from first principles
* [First, a brief lecture on simple-as-possible species distribution modeling](../lectures/Lecture06-FirstPrinciplesSDM.html)

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

- What is the basic logic behind a species distribution model?
- How can occurrence records be connected to environmental conditions?
- What is the difference between the environment where a species is observed and the environment that is available in the study area?
- How can a simple suitability rule be projected back into geographic space?

## Concepts

- Occurrence records as samples of used environments
- Background environments as samples of available conditions
- One-variable species-environment relationships
- Suitability curves
- Projection from environmental space to geographic space

## Applied Lab

Students build a simple species distribution model from first principles.
Using one amphibian species and one environmental raster, they extract
environmental values at occurrence records, compare those values with
background conditions across Maine, create a hand-built suitability curve,
and project that curve back onto the landscape as a continuous suitability
map.

## Assignment

Submit a completed first-principles SDM notebook with occurrence and
background comparisons, a suitability curve, a projected suitability map,
a thresholded map, and short interpretations of the assumptions and
limitations of the approach.

- `docs/labs/Lab06-FirstPrinciplesSDM.ipynb`
- `docs/assignments/Assignment-06-FirstPrinciplesSDM.ipynb`

**Paper discussion leader next week:** Allie! Please select a paper for
the group to discuss before Sunday 10/11 6pm and send it around to the
class email list: bio597-fall2026-group@maine.edu
