# Lecture07 artwork provenance

These illustrations were created with the built-in image-generation tool for this lecture. They are not photographs or fitted model outputs.

## Habitat illustration

File: `Lecture07-habitat.png`

Prompt: Use case: scientific-educational. Asset: wide 3:2 illustration for a graduate biology lecture. Create a beautiful accurate natural-history illustration of a wood frog, Boreorana sylvatica, on damp brown leaf litter beside a temporary woodland pool in a Maine mixed forest. The small tan frog has its characteristic dark mask behind the eye, a narrow light upper lip and dorsolateral folds, anatomically accurate four limbs, no exaggerated eyes. Frog sharp foreground lower right, woodland pond and trunks softly receding, broad clean pale off-white upper left with no text. Restrained watercolor and crisp pencil naturalist rendering, teal water, earthy coral and ochre leaves, paper color #f7f8f6. No symbols, no diagrams, no letters, no watermark. Clearly an illustration, not a photograph.

## Decision-tree teaching example

File: `Lecture07-tree.png`

The threshold, counts and scores are illustrative.

Prompt: Use case: scientific-educational. Asset: wide 3:2 teaching diagram for biology students encountering random forests for the first time. Clean elegant flat textbook infographic on solid off-white #f7f8f6 background, very large dark navy sans-serif lettering, teal #087e8b and coral #d95d39 accents, no decorative texture. Draw a single clear decision tree with ONE root question centered near top, exactly 'Warmer than 5°C?' Two non-crossing branches to two large terminal groups below. Left branch label 'No', terminal label '2 presence, 8 background', large score below '0.2'. Right branch label 'Yes', terminal label '8 presence, 2 background', large score below '0.8'. Each terminal group contains exactly ten small circles, teal filled for presence and hollow coral for background, matching the labels. Root connects only to these two groups, no further branches. At bottom small legend 'Filled: presence' and 'Open: background'. Spacious, balanced composition, highly legible. No headline, no additional text, no frog illustrations, no watermark. Numbers are an invented teaching example.

## Forest averaging teaching example

File: `Lecture07-forest.png`

The three scores and their mean are illustrative. The final revision uses three simple binary stumps, each with one root and two children, to avoid ambiguous branching.

Initial prompt: Use case: scientific-educational. Asset: wide 3:2 educational illustration explaining averaging in a random forest regressor to biology beginners. Off-white #f7f8f6, dark navy text, teal #087e8b, coral #d95d39, ochre accents, clean textbook style. Across upper half three distinct small branching decision-tree diagrams, each a root with 2 to 4 terminal leaves, no detailed node text. Under each tree a large exact label, left '0.2', middle '0.6', right '0.7'. Below the trees three fine lines converge to one big central label 'Average = 0.5'. Add exact small label 'Same location, three trees' at top. The trees differ in branch structure to show distinct models. Large accessible typography, generous margins, crisp lines, no other text, no decorative forest landscape, no watermark. Illustrative scores, not empirical results.

Final edit: Keep all text and scores, the palette and averaging connectors. Replace the three tree diagrams with simple binary stumps, each with one teal root, two branches and two ochre leaves.

## Depth-two temperature tree

File: `Lecture07-tree-depth2.png`

Generated with the built-in image-generation tool. The thresholds, label counts, and scores are illustrative. A 6°C example follows the highlighted path through two questions to the score 0.8.

Prompt: Use case: scientific-educational. Create a WIDE LANDSCAPE 2:1 teaching infographic, ideally 2048 by 1024, for a biology lecture introducing decision trees. Match clean off-white #f7f8f6 paper, dark navy sans-serif text, teal #087e8b and coral #d95d39. Show EXACTLY a depth-2 binary decision tree: one root, two internal child questions, four terminal groups. All questions use annual mean temperature. Root centered at top reads exactly 'Warmer than 5°C?'. Root's left branch is labeled 'No' and connects to a question 'Warmer than 3°C?'. Root's right branch is labeled 'Yes' and connects to 'Warmer than 7°C?'. Each of those two questions has TWO outgoing branches, labeled 'No' on the left and 'Yes' on the right. Bottom row exactly four large terminal boxes, ordered left to right, with these exact three lines each: first '3°C or cooler' / '1 presence, 9 background' / 'Score 0.1'; second 'Above 3°C to 5°C' / '3 presence, 7 background' / 'Score 0.3'; third 'Above 5°C to 7°C' / '8 presence, 2 background' / 'Score 0.8'; fourth 'Above 7°C' / '4 presence, 6 background' / 'Score 0.4'. Use large legible text and generous spacing, edges never cross, no botanical trees, no frog icons, no charts. Highlight just the route for temperature 6°C in thick teal: root to RIGHT question, then that question to its LEFT terminal group 'Score 0.8'. All other branch lines dark navy or light gray. Highlight that third final box with a soft teal fill. Keep every No/Yes label accurate: a value greater than the stated threshold takes Yes. Each terminal group's score is the fraction of presence labels in its ten examples. No headline or footer, no watermark. These are invented teaching numbers, not fitted results. All text must match exactly and the tree must have only two levels of splits.

## Empirical plots

The other `Lecture07-*.png` figures are scientific plots of the supplied occurrence and climate data, not generated illustrations. `Lecture07-build-figures.py` reproduces them. `Lecture07-example-results.json` records the sample sizes, settings and metrics.
