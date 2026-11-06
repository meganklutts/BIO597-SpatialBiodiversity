"""Rebuild Lecture09 figures with the pyGF example data and notebook settings.

Run with a Python environment containing pyGF and its notebook dependencies:
    python Lecture09-build-figures.py --pygf-root /path/to/pyGF
The input repository supplies examples/Pguttatus.{vcf,...} and envs/*.tif.
No genotype data are copied into the course repository.
"""
import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from pygf import GradientForest, read_coordinates, read_vcf, sample_environment

OUT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--pygf-root", type=Path, default=OUT.parents[3] / "pyGF")
args = parser.parse_args()
data = args.pygf_root.resolve()
PAPER, INK, TEAL, CORAL, GRAY = "#f7f8f6", "#18212b", "#087e8b", "#d95d39", "#aab5bb"
plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 16, "text.color": INK,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "axes.spines.top": False, "axes.spines.right": False,
})

def save(fig, name):
    fig.savefig(OUT / f"Lecture09-{name}.png", dpi=150, bbox_inches="tight", pad_inches=.2)
    plt.close(fig)

sites = read_coordinates(data / "examples/Pguttatus_coords.txt")
genotypes = read_vcf(
    data / "examples/Pguttatus.vcf", samples=sites, min_call_rate=.8,
    min_maf=.05, one_per_contig=True, max_variants=256, random_state=42,
)
X = sample_environment(data / "envs", sites)
y = genotypes.dosage.to_pandas()
assert X.index.equals(y.index) and X.index.equals(sites.index)
assert np.isfinite(X.to_numpy()).all()
print(f"Fitting {len(sites)} individuals, {X.shape[1]} predictors, {y.shape[1]} SNPs", flush=True)
gf = GradientForest(
    n_estimators=100, max_level=2, random_state=42, keep_response_curves=True,
).fit(X, y)
scores = gf.response_scores_
print(scores.groupby(["retained", "reason"]).size().to_string(), flush=True)

# Actual sample locations; axes show coordinates, without an inferred range boundary.
fig, ax = plt.subplots(figsize=(7.2, 5.3), layout="constrained")
ax.scatter(sites.geometry.x, sites.geometry.y, c=TEAL, s=65, edgecolor=PAPER)
ax.set(xlabel="Longitude (°)", ylabel="Latitude (°)", title=f"{len(sites)} sampled individuals")
ax.grid(alpha=.15)
save(fig, "sites")

fig, ax = plt.subplots(figsize=(9, 4.7), layout="constrained")
for retained, color, label in [(False, GRAY, "Excluded"), (True, TEAL, "Contributing")]:
    values = scores.loc[scores.retained == retained, "oob_r2"].dropna()
    ax.hist(values, bins=np.linspace(-1, 1, 31), alpha=.8, color=color, label=label)
ax.axvline(0, color=CORAL, linestyle="--")
ax.set(xlabel="SNP out-of-bag R²", ylabel="Number of SNPs")
ax.legend(frameon=False)
save(fig, "oob")

fig, ax = plt.subplots(figsize=(8.5, 4.8), layout="constrained")
gf.importance_.head(6).sort_values().plot.barh(ax=ax, color=TEAL)
ax.set(xlabel="Mean allocated OOB R²", ylabel="")
save(fig, "importance")

fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.5), layout="constrained")
for ax, name in zip(axes.flat, gf.importance_.head(4).index):
    curve = gf.turnover_[name]
    ax.plot(curve.value, curve.cumulative_importance, color=TEAL, linewidth=3)
    ax.set(title=name, xlabel="Environmental value (raster units)", ylabel="Cumulative importance")
    ax.set_ylim(0, gf.importance_.iloc[0] * 1.08)
save(fig, "curves")

# Invented teaching example: accumulation is independent of allele-change direction.
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), layout="constrained")
t = np.array([5, 9, 10, 11, 12, 16, 20])
axes[0].plot(t, [0, 0, .3, 1.3, 1.8, 2, 2], color=TEAL, linewidth=3, label="SNP A")
axes[0].plot(t, [2, 2, 1.7, .7, .2, 0, 0], color=CORAL, linewidth=3, label="SNP B")
axes[0].set(xlabel="Temperature (°C)", ylabel="Mean alternate-allele dosage", title="Opposite response directions")
axes[0].legend(frameon=False)
axes[1].plot(t, [0, .01, .04, .19, .28, .30, .31], color=TEAL, linewidth=3)
axes[1].axvspan(10, 12, color=CORAL, alpha=.13)
axes[1].set(xlabel="Temperature (°C)", ylabel="Cumulative importance", title="Turnover accumulates")
save(fig, "turnover-explained")

result = gf.plot_turnover()
save(result.figure, "turnover-map")
biplot = gf.plot_biplot(X, sites, environment=data / "envs", n_vectors=3)
save(biplot.figure, "biplot")
snp = scores.oob_r2.idxmax()
single = gf.plot_biplot(X, sites, environment=data / "envs", response=snp, n_vectors=3)
save(single.figure, "snp-biplot")

assert np.allclose(gf.importance_.sum(), scores.loc[scores.retained, "oob_r2"].mean())
for name, curve in gf.turnover_.items():
    assert np.all(np.diff(curve.cumulative_importance) >= -1e-12)
    assert np.isclose(curve.cumulative_importance.iloc[-1], gf.importance_[name])
scores.to_csv(OUT / "Lecture09-snp-scores.csv")
gf.importance_.to_csv(OUT / "Lecture09-predictor-importance.csv")
summary = {
    "source_repository": "https://github.com/isaacovercast/pygf",
    "source_commit": subprocess.check_output(["git", "-C", str(data), "rev-parse", "HEAD"], text=True).strip(),
    "input_sha256": {str(p.relative_to(data)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [data / "examples/Pguttatus.vcf", data / "examples/Pguttatus_coords.txt", *sorted((data / "envs").glob("*.tif"))]},
    "python": platform.python_version(), "numpy": np.__version__, "sklearn": sklearn.__version__,
    "n_samples": len(X), "n_predictors": X.shape[1], "n_snps": y.shape[1],
    "n_contributing": int(scores.retained.sum()), "n_estimators": 100,
    "max_level": 2, "random_state": 42, "min_call_rate": .8, "min_maf": .05,
    "one_per_contig": True, "map_stride": 4, "map_buffer": .2,
    "top_predictor": gf.importance_.index[0], "single_snp": snp,
    "importance": gf.importance_.to_dict(),
    "oob_r2_range": [float(scores.oob_r2.min()), float(scores.oob_r2.max())],
    "biplot_explained_variance_ratio": biplot.pca.explained_variance_ratio_.tolist(),
    "illustration": "turnover-explained uses invented values; all other plots use the example fit",
}
(OUT / "Lecture09-example-results.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2), flush=True)
