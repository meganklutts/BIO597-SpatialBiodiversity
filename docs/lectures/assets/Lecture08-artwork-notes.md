# Lecture08 visual provenance

## Cover illustration

File: `Lecture08-habitat.png`

Created with the built-in image-generation tool. This is a natural-history illustration of a pickerel frog, not a photograph or a documented survey site.

Prompt: Use case: scientific-educational. Create a wide 3:2 natural-history watercolor illustration for a biology lecture cover about species distribution models. Show an anatomically accurate pickerel frog, Lithobates palustris, on a mossy damp bank beside a small stream and wooded pool in Maine. The tan-brown frog has TWO orderly rows of dark rectangular dorsal spots, pale dorsolateral folds, a narrow pale lip stripe, and normal small amphibian eyes. Foreground frog toward lower right, entire frog visible, a few sedges and wet leaf litter. Reflective teal water and mixed deciduous woods recede softly behind it. Restrained naturalist pencil and watercolor style, earth tones, subtle coral and ochre leaves, paper #f7f8f6 fading toward left. No letters, no map, no logos or watermarks, no exaggerated cartoon features. Clearly a scientific illustration, not a photograph. Leave generous pale negative space at upper left and preserve all limbs.

## Weighted-mean balance illustration

File: `Lecture08-mean-balance.png`

Created with the built-in image-generation tool. The beam is a conceptual analogy using rounded illustrative relative weights. The mean is 6°C; it is not an assertion of a temperature optimum. Balancing the mean is one constraint, and maximum entropy selects among the many distributions that can meet it.

Prompt: Use case: scientific-educational. Create a wide 2:1 teaching illustration for a biology lecture explaining a weighted mean as a balance point. Clean off-white #f7f8f6, dark navy sans-serif labels, teal #087e8b and coral #d95d39 accents, minimal textbook style. A single straight LEVEL horizontal balance beam spans the image. Four clearly marked equally spaced positions left to right are labeled exactly '2°C', '4°C', '6°C', '8°C'. Put a triangular fulcrum DIRECTLY UNDER the 6°C mark, NOT at the beam's midpoint: the beam extends farther to the left of the fulcrum than to the right. At the four positions, show small piles of identical weight discs, with pile sizes proportional to 12, 18, 28 and 42. Use restrained teal for all piles. Label each pile clearly above it, left to right, exactly '12%', '18%', '28%', '42%'. The 28% pile must sit over the fulcrum at 6°C. The heaviest 42% pile sits at 8°C to the right. The level beam must show correct balance: 12 times 4 plus 18 times 2 equals 42 times 2. Do NOT display this equation, it is only a constraint for mathematical accuracy. Beneath the fulcrum place the exact readable label 'Mean = 6°C'. On the lower left add exact small annotation 'Cooler cells pull the mean down'. On the lower right add 'Warmer cells balance them'. No arrows indicating that 6°C is an optimum, no ecology claims, no frogs, no bar chart, no other text, no watermark. Spacious composition with large labels. This is an illustration using rounded relative weights, totaling 100%, not actual physical temperature weights.

## Scientific figures

All `Lecture08-*.png` figures except `Lecture08-habitat.png` and `Lecture08-mean-balance.png` are data plots created by `Lecture08-build-figures.py`. They are not generated illustrations.

The script uses the supplied Maine amphibian occurrences and climate data, elapid 1.0.4, a seeded temperature-biased background, 19 climate predictors and geographic sample weights. The lecture uses *Lithobates palustris*, the pickerel frog. Numeric results, sample sizes and seeds are saved in `Lecture08-example-results.json`. Student results can differ.

The following examples are explicitly illustrative rather than fitted ecological results:

- The maximum-entropy example distributes relative weight across four equally available cells at 2, 4, 6 and 8°C, constrained to a weighted mean of 6°C. Its weights sum to one; they are not site occupancy probabilities.
- The two-dimensional balance example uses four equally available combinations of 2 or 8°C and 800 or 1,200 mm rainfall. The exact maximum-entropy weights are 1/12, 1/6, 1/4 and 1/2, producing means of 6°C and 1,100 mm. The plotted percentages are rounded; circle area is proportional to weight. The coral cross is the weighted center in climate space. These are relative weights, not occupancy probabilities. The example constrains only the two raw means.
- The ranking/ROC example uses presence scores 0.9, 0.8 and 0.6, and background scores 0.7, 0.4 and 0.2. Eight of nine pairs rank correctly, giving AUC 8/9.
- The condensed ROC/AUC slides use `Lecture08-positive-predictions.png`: recorded-site scores 0.9, 0.8, 0.6, 0.3 and background scores 0.7, 0.4, 0.2, 0.1. At cutoff 0.5, TP = 3, FN = 1, FP = 1 and TN = 3. Background is the evaluation negative class, not confirmed absence.
- `Lecture08-roc-performance.png` shows smooth illustrative ROC curves with exact population AUCs 0.95, 0.75 and 0.50. They derive from two equal-variance normal score populations, with mean separations chosen using AUC = Φ(separation / √2). Numerical integration checks the displayed areas. The good/medium/bad labels describe these examples, not general-purpose grading thresholds.

To regenerate the scientific figures from the repository root, use the Lab08 Python environment and run:

```bash
python docs/lectures/assets/Lecture08-build-figures.py
```
