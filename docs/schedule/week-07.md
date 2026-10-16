# Week 07: Building a complete SDM w/ a machine learning model

## Icebreaker

If you could bring back any fashion trend, what would it be?

## Paper discussion

- Allie will be leading the discussion this week of Aoyama et al 2020
["Incorporating diversity measures into Ecological Site Descriptions to manage
biodiversity on heterogeneous landscapes"](https://doi.org/10.1016/j.rala.2020.05.002)

# Lab Exercise: Building a more complete SDM w/ Machine Learning

## Core Questions

- How does this 'machine learning' stuff actually work?
- How does a random forest learn a species–environment relationship?
- How does prediction error change when we add more environmental variables?
- Which bioclim variables does the ML model use most, and does importance imply an ecological cause?

## Concepts

- Features vs Targets (machine learning jargon for predictor vs response)
- Decision Trees
- Train/test data splitting
- Comparing one-variable and multiple-variable models
- Prediction evaluation; Mean absolute error (MAE)
- Variable importance

## Applied Lab

* [A visual introduction to machine learning SDMs](../lectures/Lecture07-MachineLearningSDM.html)

* Next, the usual intro update exercise: Go to your
[JupyterHub](https://maine.cloudbank.2i2c.cloud/) and pull the latest version
of the class github repository.

### Python Tools

- scikit-learn
- GeoPandas
- NumPy
- pandas
- xarray
- Matplotlib


Students build a presence/background SDM for a Maine amphibian using
`scikit-learn`'s `RandomForestRegressor` and the supplied occurrence–climate
table and Maine bioclimatic raster stack. In short, guided steps, they
first train a forest using annual mean temperature (`bio_1`) and evaluate
MAE on withheld cells. They add annual precipitation (`bio_12`) and
precipitation seasonality (`bio_15`), refit using the same training cells,
and compare MAE on the same test cells. They then map suitability and
plot variable importance for the three-variable model.

- [Lab 07: Machine Learning SDMs](../labs/lab07-MachineLearningSDM.ipynb)

## Assignment

Repeat the workflow for a chosen amphibian species, justify predictor
roles, and compare the BIO1-only and three-variable models on the same test cells.
Submit a completed notebook with maps, short interpretations, and one
saved suitability raster. Use the lab's model settings throughout.

- Read [A visual introduction to machine learning](https://r2d3.us/visual-intro-to-machine-learning-part-1/) (It's short and fun).
- [Assignment 07: Machine Learning SDMs](../assignments/Assignment-07-MachineLearningSDM.ipynb)

**Paper discussion leader next week:** Next week we will need to do 2 papers
so everyone has a chance to lead over the semester. So, **Meg & Hao!** Please each
select a (hopefully shorter) paper for the group to discuss before Sunday 10/18
6pm and send it around to the class email list: bio597-fall2026-group@maine.edu
