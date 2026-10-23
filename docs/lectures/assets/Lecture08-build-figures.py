"""Rebuild lecture figures from course data; requires elapid and the Lab08 packages."""
from pathlib import Path
import json
import platform
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.special import softmax
import elapid as ela
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PAPER, INK, TEAL, CORAL, GRAY = '#f7f8f6', '#18212b', '#087e8b', '#d95d39', '#aab5bb'
plt.rcParams.update({'font.family':'sans-serif', 'font.sans-serif':['Arial','DejaVu Sans'],
    'font.size':17, 'text.color':INK, 'axes.labelcolor':INK, 'xtick.color':INK, 'ytick.color':INK,
    'figure.facecolor':PAPER, 'axes.facecolor':PAPER, 'savefig.facecolor':PAPER,
    'axes.spines.top':False, 'axes.spines.right':False})
def save(fig, name):
    fig.savefig(OUT / f'Lecture08-{name}.png', dpi=160, bbox_inches='tight', pad_inches=.16)
    plt.close(fig)

def map_points(ax, frame, colors, size=6):
    boundary.boundary.plot(ax=ax, color=INK, linewidth=.6)
    frame.plot(ax=ax, color=colors, markersize=size, alpha=.65)
    ax.set_xlabel(''); ax.set_ylabel(''); ax.set_xticks([]); ax.set_yticks([])

np.random.seed(597)
variables = [f'bio_{i}' for i in range(1,20)]
labels = ['Annual mean temperature', 'Mean diurnal temperature range', 'Isothermality',
    'Temperature seasonality', 'Max temperature, warmest month', 'Min temperature, coldest month',
    'Annual temperature range', 'Mean temperature, wettest quarter', 'Mean temperature, driest quarter',
    'Mean temperature, warmest quarter', 'Mean temperature, coldest quarter', 'Annual precipitation',
    'Precipitation, wettest month', 'Precipitation, driest month', 'Precipitation seasonality',
    'Precipitation, wettest quarter', 'Precipitation, driest quarter', 'Precipitation, warmest quarter',
    'Precipitation, coldest quarter']
rasters = [str(ROOT / f'docs/data/bioclim_ME/wc2.1_2.5m_bio_{i}.tif') for i in range(1,20)]
amphibians = gpd.read_file(ROOT / 'docs/data/amphibians.geojson')
species = 'Lithobates palustris'
points = amphibians[amphibians.species == species].copy()
boundary = gpd.read_file(ROOT / 'docs/labs/ME_ShapeFiles/Maine_State_Boundary.shp').to_crs(26919).dissolve()
uniform = ela.sample_raster(rasters[0],1000).drop_duplicates()
biased = ela.sample_bias_file(rasters[0],1000).drop_duplicates()
presence = ela.annotate(points.geometry,rasters,labels=labels,drop_na=True,quiet=True)
background = ela.annotate(biased,rasters,labels=labels,drop_na=True,quiet=True)
presence['SampleWeight'] = ela.distance_weights(presence.to_crs(26919),n_neighbors=-1)
background['SampleWeight'] = ela.distance_weights(background.to_crs(26919),n_neighbors=-1)
merged = ela.stack_geodataframes(presence,background,add_class_label=True).to_crs(26919)
train,test = ela.checkerboard_split(merged,grid_size=50_000)
# Use exactly the same eligible rows for random-versus-spatial comparison.
# The library can omit points on its checkerboard boundaries.
eligible = ela.stack_geodataframes(train,test)
random_train,random_test = train_test_split(eligible,test_size=len(test),stratify=eligible['class'],random_state=597)
models={}; summaries=[]; predictions={}
for name,learning,evaluation in [('Training rows',eligible,eligible), ('Random test',random_train,random_test),
        ('Checkerboard A to B',train,test), ('Checkerboard B to A',test,train)]:
    model=ela.MaxentModel(n_cpus=4,random_state=597)
    model.fit(learning[labels],learning['class'],sample_weight=learning['SampleWeight'])
    scores=model.predict(evaluation[labels])
    assert np.isfinite(scores).all()
    assert learning['class'].nunique()==evaluation['class'].nunique()==2
    models[name]=model; predictions[name]=(evaluation['class'].to_numpy(),scores)
    summaries.append({'evaluation':name,'n_train':len(learning),'n_evaluate':len(evaluation),
        'AUC':roc_auc_score(evaluation['class'],scores),
        'weighted_AUC':roc_auc_score(evaluation['class'],scores,sample_weight=evaluation['SampleWeight'])})
print(pd.DataFrame(summaries).to_string(index=False),flush=True)

# The record map uses geographic locations, not model predictions.
fig,ax=plt.subplots(figsize=(6.4,5.6))
map_points(ax,presence.to_crs(26919),TEAL,size=7)
ax.set_title('Pickerel-frog occurrence records',fontsize=18)
save(fig,'records')

fig,axes=plt.subplots(1,2,figsize=(11,4.4))
for ax,label,unit in zip(axes,[labels[0],labels[11]],['°C','mm']):
    lo=min(presence[label].min(),background[label].min());hi=max(presence[label].max(),background[label].max())
    bins=np.linspace(lo,hi,24)
    ax.hist(background[label],bins=bins,density=True,alpha=.45,color=CORAL,label='Available background')
    ax.hist(presence[label],bins=bins,density=True,alpha=.55,color=TEAL,label='Recorded frogs')
    ax.set_xlabel(f'{label} ({unit})'); ax.set_ylabel('Density')
axes[0].legend(fontsize=13)
fig.tight_layout();save(fig,'used-available')

# A constrained maximum-entropy example over four equal-area cells.
temperatures=np.array([2.,4.,6.,8.])
beta=brentq(lambda b:np.dot(softmax(b*temperatures),temperatures)-6.,0.,3.)
maxent_mass=softmax(beta*temperatures)
fig,ax=plt.subplots(figsize=(8.8,4.2))
ax.bar(temperatures,[25]*4,width=1.1,color=GRAY)
ax.set(xlabel='Temperature of each equal-area cell (°C)',ylabel='Share of total weight (%)',ylim=(0,55),xticks=temperatures)
for t in temperatures:ax.text(t,26,'25%',ha='center',fontsize=17)
ax.text(.02,.92,'Weighted mean temperature = 5°C',transform=ax.transAxes,fontsize=17)
save(fig,'equal-weights')

fig,axes=plt.subplots(1,3,figsize=(12.8,4.5),sharey=True)
for ax,mass,title,color in zip(axes,[np.ones(4)/4,np.array([0,0,1,0]),maxent_mass],
        ['Equal weights','Only the 6°C cell','Maximum entropy'],[GRAY,CORAL,TEAL]):
    ax.bar(temperatures,mass*100,width=1.2,color=color)
    ax.set(xticks=temperatures,xlabel='Temperature (°C)',ylim=(0,120),title=title)
    ax.text(.5,.92,f'Mean = {np.dot(mass,temperatures):.0f}°C',transform=ax.transAxes,ha='center',fontsize=16)
axes[0].set_ylabel('Share of total weight (%)')
fig.tight_layout();save(fig,'maxent-constraint')
assert abs(np.dot(maxent_mass,temperatures)-6)<1e-9
assert abs(maxent_mass.sum()-1)<1e-12

# Two raw-mean constraints over four equally available climate combinations.
# The entropy-maximizing joint distribution is the product of its marginals.
def plot_two_dimensional_balance():
    temperature = np.array([2., 8., 2., 8.])
    rainfall = np.array([800., 800., 1200., 1200.])
    mass = np.array([1/12, 1/6, 1/4, 1/2])
    assert np.isclose(mass.sum(), 1)
    assert np.isclose(mass @ temperature, 6)
    assert np.isclose(mass @ rainfall, 1100)
    fig, ax = plt.subplots(figsize=(7.4, 5.5))
    ax.plot([6, 6], [650, 1100], '--', color=CORAL, lw=1.7)
    ax.plot([.3, 6], [1100, 1100], '--', color=CORAL, lw=1.7)
    ax.scatter(temperature, rainfall, s=mass*18000, color=TEAL, alpha=.92,
               edgecolors=PAPER, linewidths=2, zorder=3)
    for x, y, label in zip(temperature, rainfall, ['8.3%', '16.7%', '25%', '50%']):
        ax.text(x, y, label, ha='center', va='center', color='white',
                fontsize=16, fontweight='bold', zorder=4)
    ax.scatter([6], [1100], marker='X', s=200, color=CORAL,
               edgecolors=PAPER, linewidths=1.5, zorder=5)
    ax.annotate('Balance point', (6, 1100), xytext=(4.2, 1320),
                color=CORAL, fontsize=18, ha='center',
                arrowprops={'arrowstyle':'->', 'color':CORAL, 'lw':1.6})
    ax.set(xlim=(.3, 9.7), ylim=(650, 1400), xticks=[2, 6, 8],
           yticks=[800, 1100, 1200], xlabel='Temperature (°C)',
           ylabel='Annual rainfall (mm)')
    ax.tick_params(labelsize=15)
    fig.tight_layout()
    save(fig, 'two-dimensional-balance')

plot_two_dimensional_balance()

with xr.open_dataset(ROOT/'docs/data/maine_bioclim.nc') as source:
    climate=source.load()
grid=climate[variables].to_dataframe().reset_index()[['x','y']+variables].dropna(subset=variables)
grid=grid.rename(columns=dict(zip(variables,labels)))
grid['score']=models['Training rows'].predict(grid[labels])
score=grid.set_index(['y','x']).score.to_xarray().reindex(y=climate.y,x=climate.x)
fig,ax=plt.subplots(figsize=(6.4,5.8))
score.plot(ax=ax,vmin=0,vmax=1,cmap='viridis',cbar_kwargs={'label':'Relative suitability score','shrink':.85})
boundary.to_crs(4326).boundary.plot(ax=ax,color=INK,lw=.5)
ax.set(xlabel='Longitude',ylabel='Latitude',title='')
save(fig,'maxent-map')

fig,axes=plt.subplots(1,2,figsize=(9,5.4))
for ax,pts,title in zip(axes,[uniform,biased],['Uniform background','Temperature-biased background']):
    map_points(ax,gpd.GeoDataFrame(geometry=pts).to_crs(26919),CORAL,size=5)
    ax.set_title(title,fontsize=17)
fig.tight_layout();save(fig,'backgrounds')

fig,ax=plt.subplots(figsize=(6.6,5.7))
boundary.boundary.plot(ax=ax,color=INK,lw=.6)
presence.to_crs(26919).plot(ax=ax,column='SampleWeight',markersize=9,cmap='YlOrBr',legend=True,
    legend_kwds={'label':'Relative sample weight','shrink':.8})
ax.set_xticks([]);ax.set_yticks([])
save(fig,'weights')

fig,axes=plt.subplots(1,2,figsize=(9,5.4))
for ax,learning,evaluation,title in zip(axes,[random_train,train],[random_test,test],['Random split','50 km checkerboard']):
    map_points(ax,learning,TEAL,size=4)
    evaluation.plot(ax=ax,color=CORAL,markersize=4,alpha=.6)
    ax.set_title(title,fontsize=18)
fig.tight_layout();save(fig,'split-comparison')

fig,ax=plt.subplots(figsize=(6.2,5.8))
map_points(ax,train,TEAL,size=7)
test.plot(ax=ax,color=CORAL,markersize=7,alpha=.7)
ax.set_title('Teal: training   Coral: testing',fontsize=17)
save(fig,'checkerboard')

fig,axes=plt.subplots(1,2,figsize=(9,5.4))
for ax,learning,evaluation,title in zip(axes,[train,test],[test,train],['Round 1: learn A, test B','Round 2: learn B, test A']):
    map_points(ax,learning,TEAL,size=5)
    evaluation.plot(ax=ax,color=CORAL,markersize=5,alpha=.65)
    ax.set_title(title,fontsize=17)
fig.tight_layout();save(fig,'swap-folds')

subset=eligible.sample(n=min(200,len(eligible)),random_state=597).reset_index(drop=True)
train_idx,test_idx=next(ela.BufferedLeaveOneOut(distance=50_000).split(subset,class_label='class'))
kept,held=subset.iloc[train_idx],subset.iloc[test_idx]
fig,ax=plt.subplots(figsize=(6.6,5.8))
boundary.boundary.plot(ax=ax,color=INK,lw=.6)
subset.plot(ax=ax,color='#cdd3d7',markersize=12,label='Excluded or unused')
kept.plot(ax=ax,color=TEAL,markersize=12,label='Training points')
held.buffer(50_000).boundary.plot(ax=ax,color=CORAL,lw=2)
held.plot(ax=ax,color=CORAL,markersize=70,label='Test presence')
ax.set_xticks([]);ax.set_yticks([]);ax.legend(fontsize=12,loc='upper left')
save(fig,'buffered')
assert (ela.nearest_point_distance(held,kept)>50_000).all()

# Illustrative scores for explaining ranking and ROC geometry.
def plot_auc_teaching_figures():
    # One threshold, with deliberately imperfect predictions for both classes.
    scores = np.array([.9, .8, .6, .3, .7, .4, .2, .1])
    observed = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    positive = scores >= .5
    assert ((positive & (observed == 1)).sum(),
            (positive & (observed == 0)).sum()) == (3, 1)
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.axvline(.5, color=INK, ls='--', lw=2)
    ax.text(.5, 1.61, 'Cutoff = 0.5', ha='center', fontsize=19)
    ax.text(.23, 1.36, 'Predicted unsuitable', ha='center', fontsize=18)
    ax.text(.77, 1.36, 'Predicted suitable', ha='center', fontsize=18)
    for label, y, color, name in [(1, 1, TEAL, 'Recorded frogs'),
                                 (0, 0, CORAL, 'Background*')]:
        mask = observed == label
        ax.scatter(scores[mask], np.full(mask.sum(), y), s=260,
                   color=color, zorder=3)
        for x in scores[mask]:
            category = ('TP' if x >= .5 else 'FN') if label else ('FP' if x >= .5 else 'TN')
            ax.text(x, y + .17, category, ha='center', fontsize=18,
                    color=color, fontweight='bold')
    ax.set(xlim=(0, 1), ylim=(-.4, 1.78), yticks=[0, 1],
           yticklabels=['Background*', 'Recorded frogs'],
           xlabel='Model score = predicted suitability')
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    save(fig, 'positive-predictions')

    # Smooth illustrative ROC curves from equal-variance normal score populations.
    # Their exact population AUC is Phi(separation / sqrt(2)).
    from scipy.stats import norm
    from scipy.integrate import trapezoid
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.1), sharex=True, sharey=True)
    fpr = np.linspace(0, 1, 10001)
    for ax, title, auc, color in zip(axes, ['Good', 'Medium', 'Bad (chance)'],
                                   [.95, .75, .5], [TEAL, CORAL, '#52606d']):
        separation = np.sqrt(2) * norm.ppf(auc)
        tpr = norm.cdf(norm.ppf(fpr) + separation)
        assert abs(trapezoid(tpr, fpr) - auc) < .0001
        ax.fill_between(fpr, tpr, color=color, alpha=.16)
        ax.plot(fpr, tpr, color=color, lw=3)
        ax.plot([0, 1], [0, 1], '--', color=GRAY, lw=1.6)
        ax.set(title=f'{title}\nAUC = {auc:.2f}', xlim=(0, 1), ylim=(0, 1),
               xticks=[0, .5, 1], yticks=[0, .5, 1],
               xlabel='False-positive rate')
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.set_aspect('equal')
    axes[0].set_ylabel('True-positive rate')
    fig.tight_layout(w_pad=2)
    save(fig, 'roc-performance')

plot_auc_teaching_figures()

toy_y=np.array([1,1,1,0,0,0]); toy_scores=np.array([.9,.8,.6,.7,.4,.2])
toy_auc=roc_auc_score(toy_y,toy_scores)
fig,ax=plt.subplots(figsize=(9.6,3.6))
ax.scatter(toy_scores[:3],np.ones(3),s=190,color=TEAL)
ax.scatter(toy_scores[3:],np.zeros(3),s=190,facecolors='none',edgecolors=CORAL,lw=3)
for x,y0 in zip(toy_scores,toy_y):ax.text(x,y0+.17,f'{x:.1f}',ha='center',fontsize=19)
ax.set(xlim=(0,1),ylim=(-.4,1.5),yticks=[0,1],yticklabels=['Background','Recorded sites'],xlabel='Predicted suitability score (higher = more suitable)')
ax.spines['left'].set_visible(False)
ax.grid(axis='x',alpha=.2)
fig.tight_layout();save(fig,'ranking-scores')

fpr,tpr,thresholds=roc_curve(toy_y,toy_scores,drop_intermediate=False)
fig,ax=plt.subplots(figsize=(7.4,5.7))
ax.fill_between(fpr,tpr,alpha=.12,color=TEAL)
ax.plot(fpr,tpr,color=TEAL,lw=3,label=f'Toy model: AUC = {toy_auc:.2f}')
ax.plot([0,1],[0,1],ls='--',color=GRAY,lw=2,label='Chance ranking: 0.50')
for cutoff,offset in [(.8,(.08,-.13)),(.5,(.12,-.12))]:
    x=float((toy_scores[toy_y==0]>=cutoff).mean());y=float((toy_scores[toy_y==1]>=cutoff).mean())
    ax.scatter([x],[y],s=80,color=CORAL,zorder=5)
    ax.annotate(f'Cutoff {cutoff:.1f}',(x,y),xytext=(x+offset[0],y+offset[1]),fontsize=16,
        arrowprops={'arrowstyle':'-','color':CORAL})
ax.set(xlabel='Background predicted suitable',ylabel='Recorded sites predicted suitable',xlim=(-.025,1.025),ylim=(-.025,1.08))
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.legend(loc='lower right',fontsize=13)
save(fig,'roc-explained')
assert abs(toy_auc-8/9)<1e-12

fig,axes=plt.subplots(1,3,figsize=(12.5,4.5),sharex=True,sharey=True)
for ax,name,title in zip(axes,['Training rows','Random test','Checkerboard A to B'],['Training rows','Random test','Spatial test']):
    y,scores=predictions[name];x0,y0,_=roc_curve(y,scores)
    ax.plot(x0,y0,color=TEAL,lw=3);ax.plot([0,1],[0,1],ls='--',color=GRAY)
    ax.set(title=title,xlabel='Background fraction',xlim=(0,1),ylim=(0,1.03))
    ax.text(.38,.13,f'AUC = {roc_auc_score(y,scores):.3f}',transform=ax.transAxes,fontsize=16)
axes[0].set_ylabel('Presence fraction')
fig.tight_layout();save(fig,'example-roc')

summary={'species':species,'n_presence':len(presence),'n_background':len(background),'background':'temperature-biased',
    'sample_count_requested':1000,'np_seed':597,'split_seed':597,'model_random_state':597,
    'climate_predictors':19,'sample_weights':'distance_weights(n_neighbors=-1), separate presence/background',
    'projected_crs':'EPSG:26919','checkerboard_grid_m':50_000,'buffer_m':50_000,
    'checkerboard_boundary_rows_omitted':len(merged)-len(eligible),'evaluation':summaries,
    'toy_temperature_cells_C':temperatures.tolist(),'toy_observed_mean_C':6.,'toy_maxent_relative_weights':maxent_mass.tolist(),
    'toy_AUC':toy_auc,'python':platform.python_version(),'elapid':ela.__version__,'sklearn':sklearn.__version__,
    'notes':'Empirical example uses the Lab08 pickerel frog, 19 rasters, temperature-biased background and geographic sample weights. Random and checkerboard fits use equal-sized training/test partitions from the same eligible rows. Seeds are fixed for illustration; student results can differ. Toy entropy and AUC examples are illustrative, not fitted ecological results.'}
(OUT/'Lecture08-example-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Figures and metadata saved.',flush=True)
