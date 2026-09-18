# Week 3: Biodiversity Data Cleaning

### 
[Emerging Frontiers Symposium: AI, Genomics & Community Science in Biogeography](https://sps.columbia.edu/events/emerging-frontiers-symposium-ai-genomics-community-science-biogeography?program_id=15373)
We will join first for this symposium from 10-11:15 or so, and then reconvene at 11:30
at the [usual class zoom link](https://maine.zoom.us/j/81375585733?pwd=mkyUtpLIJM4dv5m9b1cZkpUsqmmlNt.1).

## Icebreaker

What is something you enjoy doing when you are not doing science?

## Introductory business

* Isaac will be giving the [LSU Museum of Natural Science 
Seminar](https://www.lsu.edu/mns/education-and-programs/museum-seminar.php) next week (09/25),
so the status of class is up in the air at the moment. I am going to _try_ to get the morning off to join
for class but I'm still working on it. Also, if they have a zoom option I will forward this if you want to
watch my talk.
    * LSUMNS Seminar (4:30pm Eastern) "Integrating eco-evolutionary models and machine learning for predictive biodiversity science."

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

* Review Assignment-02-pygbif.ipynb


## Paper discussion
- John will be leading discussion of [Lemos et al 2014 "Modeling distribution of 
Schinus molle L. in the Brazilian Pampa: insights on vegetation dynamics and 
conservation of the biome"](https://afrjournal.org/index.php/afr/article/view/272/356)

## Core Questions

- What can go wrong when using biodiversity occurrence records?
- How should taxonomic, coordinate, temporal, and metadata uncertainty be documented?
- How can bad spatial data produce convincing but wrong analyses?

## Concepts

- Occurrence records
- Handling taxonomic uncertainty
- Assessing coordinate uncertainty
- Removing duplicate observations
- Dealing with sampling bias
- Standardizing metadata

## Python Tools

- pandas
- GeoPandas

## Applied Lab

Students download occurrence data for a species or taxonomic group and build a 
cleaning pipeline that handles missing coordinates, duplicate records, impossible 
coordinates, obvious spatial outliers, coordinate uncertainty, and duplicate 
specimens or observations.

## Assignment

**Remember:** Next week Isaac will be in Baton Rouge. We will almost certainly
still have class but it will probably only be the first 2 hours. More to come...

Complete and submit this assignment, including a data cleaning report with raw 
and filtered maps, a table of filtering decisions, and a short explanation of
remaining uncertainty.

- `docs/assignments/Assignment-03-DataCleaning.ipynb`

**Paper discussion leader next week:** elle! Please select a paper for
the group to discuss before Sunday 09/20 6pm and send it around to the
class email list: bio597-fall2026-group@maine.edu

Be prepared to lead a brief discussion on this paper next Friday 09/18,
following the guidelines in the [Paper Discussion section on the 
assignments page](../assignments/index.md).
