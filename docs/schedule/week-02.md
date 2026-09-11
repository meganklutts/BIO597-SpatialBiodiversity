# Week 2: Species Distribution Modeling Step 1 (Biodiversity data acquisition)

## Icebreaker question
What is one thing you wish you understood but don't?

## Introductory business
- [Introduce the FAQ page](../faq.md)
- [NY-SDM Symposium 9/18](https://sps.columbia.edu/events/emerging-frontiers-symposium-ai-genomics-community-science-biogeography?program_id=15373)
- I added the [UMaine CloudBank JupyterHub](https://maine.cloudbank.2i2c.cloud/) link to the course home page.
    - Exercise 1: Pull the latest version of the class github repository. Launch your jupyterhub, 
    open a terminal and see if you can remember how to do this yourself before checking
    the answer in the box below.

??? note "Commands to pull the latest version of the class repository"

    1. Change directory to your local copy of the course repo
    2. Pull the latest copy of 'upstream' which is my copy of the class website  
    3. Push the changes to your own github repo
    ```
    cd ~/BIO597-SpatialBiodiversity/`  
    git upstream 
    git push
    ```
- Review Assignment-01-Geopandas


## Core Questions

- What are Species Distribution Models and what are the major steps in constructing them?
- Where to obtain biodiversity occurrence records at scale? (hint: GBIF)
- How do I use python to programatically fetch occurence data?

## Paper discussion
- [Review slides for Huang et al 2024 & Intro to SDMs](https://docs.google.com/presentation/d/1oK78Qvi5SVGCvKuuiGBRAz-K39vhoPWbALfSsmNNP6g)
- [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/)

## Applied Lab

Students use `pygbif` to search GBIF for *Storeria dekayi*, inspect the returned 
list and dictionary objects, save the GBIF species key, count matching occurrence 
records, fetch up to 100 georeferenced records, convert those records to a 
DataFrame and then a GeoDataFrame, and map the points with `.explore()`.

The lab also introduces simple summaries and filters, including grouping records 
by year and selecting records by location.

### Lab Concepts

- GBIF as a source of biodiversity occurrence data.
- Scientific names and 'taxon keys'.
- Occurrence records with coordinates.
- Converting and plotting GBIF records with GeoDataFrames
- Simple record summaries using grouping and filtering.

### Python Tools

- pygbif
- GeoPandas


## Homework

Register for the symposium next week: [NY-SDM Emerging Frontiers Symposium: AI, Genomics & Community Science in Biogeography](https://sps.columbia.edu/events/emerging-frontiers-symposium-ai-genomics-community-science-biogeography?program_id=15373)

Complete and submit these two assignment:

- `docs/assignments/Assignment-02-PythonCollections.ipynb`
- `docs/assignments/Assignment-02-pygbif.ipynb`

**Paper discussion leader next week:** John! Please select a paper for
the group to discuss before Sunday 09/13 6pm and send it around to the
class email list: bio597-fall2026-group@maine.edu  

Be prepared to lead a brief discussion on this paper next Friday 09/18,
following the guidelines in the [Paper Discussion section on the 
assignments page](../assignments/index.md).
