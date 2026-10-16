from pathlib import Path
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

root=Path(__file__).resolve().parents[3]
out=root/'docs/lectures/assets'
PAPER='#f7f8f6'; INK='#18212b'; TEAL='#087e8b'; CORAL='#d95d39'; GRAY='#aab5bb'
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],'font.size':17,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'figure.facecolor':PAPER,'axes.facecolor':PAPER,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':PAPER,'axes.titleweight':'bold'})
def save(fig,name):
 fig.savefig(out/('Lecture07-'+name+'.png'),dpi=155,bbox_inches='tight',pad_inches=.15);plt.close(fig)

amph=gpd.read_file(root/'docs/data/amphibians+bioclim.geojson')
climate=xr.open_dataset(root/'docs/data/maine_bioclim.nc')
variables=['bio_'+str(i) for i in range(1,20)]
maine=gpd.read_file(root/'docs/labs/ME_ShapeFiles/Maine_State_Boundary.shp').to_crs(4326).dissolve()
pres=amph[(amph.species=='Boreorana sylvatica') & (amph.coordinateUncertaintyInMeters<100)].copy()
n_before=len(pres);pres=pres.dropna(subset=variables).copy()
grid=climate[variables].to_dataframe().reset_index()[['x','y']+variables].dropna(subset=variables)
presence_data=pres[variables].copy();presence_data['x']=pres.geometry.x;presence_data['y']=pres.geometry.y;presence_data['observed']=1
bg=grid.sample(n=len(presence_data),random_state=597).copy();bg['observed']=0
model_data=pd.concat([presence_data,bg],ignore_index=True)
train,test=train_test_split(model_data,test_size=.25,random_state=597,stratify=model_data.observed)
models=[];errors=[]
for features in [['bio_1'],['bio_1','bio_12','bio_15']]:
 model=RandomForestRegressor(n_estimators=100,min_samples_leaf=5,random_state=597).fit(train[features],train.observed)
 models.append(model);errors.append(mean_absolute_error(test.observed,model.predict(test[features])))
features=['bio_1','bio_12','bio_15']
final=RandomForestRegressor(n_estimators=100,min_samples_leaf=5,random_state=597).fit(model_data[features],model_data.observed)

fig,ax=plt.subplots(figsize=(6.2,5.8))
maine.boundary.plot(ax=ax,color=INK,linewidth=.7)
ax.scatter(bg.x,bg.y,s=10,facecolors='none',edgecolors=CORAL,linewidth=.6,alpha=.45,label='Background')
ax.scatter(pres.geometry.x,pres.geometry.y,s=8,color=TEAL,alpha=.6,label='Recorded frogs')
ax.set(xlabel='Longitude',ylabel='Latitude')
ax.legend(loc='upper left',fontsize=13,frameon=True)
save(fig,'records')

fig,ax=plt.subplots(figsize=(9,4.5))
t=np.linspace(grid.bio_1.min(),grid.bio_1.max(),300)
mu=pres.bio_1.mean();sd=pres.bio_1.std()
ax.plot(t,np.exp(-.5*((t-mu)/sd)**2),color=TEAL,linewidth=4)
ax.axvline(mu,ls='--',color=CORAL,lw=2)
ax.set(xlabel='Annual mean temperature (°C)',ylabel='Hand-built suitability',ylim=(0,1.05))
ax.text(mu+.12,.94,'Mean at records',fontsize=15,color=CORAL)
save(fig,'last-week')

fig,ax=plt.subplots(figsize=(9.5,4.6))
tree=DecisionTreeRegressor(max_depth=3,min_samples_leaf=5,random_state=597).fit(train[['bio_1']],train.observed)
ax.plot(t,tree.predict(pd.DataFrame({'bio_1':t})),color=TEAL,lw=4,drawstyle='steps-post')
ax.scatter(train.loc[train.observed==0,'bio_1'],np.full((train.observed==0).sum(),.015),s=11,facecolors='none',edgecolors=CORAL,alpha=.2)
ax.scatter(train.loc[train.observed==1,'bio_1'],np.full((train.observed==1).sum(),.985),s=11,color=TEAL,alpha=.2)
ax.set(xlabel='Annual mean temperature (°C)',ylabel='Tree score',ylim=(-.04,1.04))
ax.text(1,.08,'Background labels',color=CORAL,fontsize=14)
ax.text(1,.88,'Presence labels',color=TEAL,fontsize=14)
save(fig,'tree-response')

fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharex=True,sharey=True)
for ax,rows,title,col in [(axes[0],train,'75% to learn',GRAY),(axes[1],test,'25% to test',CORAL)]:
 ax.scatter(rows.bio_1,rows.bio_12,s=12,alpha=.5,color=col)
 ax.set(xlabel='Temperature (°C)',title=title)
axes[0].set_ylabel('Annual precipitation (mm)')
fig.tight_layout();save(fig,'holdout')

fig,axes=plt.subplots(1,3,figsize=(13,4.6))
for ax,k,title,cmap,label in zip(axes,features,['Temperature','Rainfall','Rainfall seasonality'],['coolwarm','Blues','YlOrBr'],['°C','mm','Coefficient of variation']):
 climate[k].plot(ax=ax,cmap=cmap,cbar_kwargs={'label':label,'shrink':.8})
 maine.boundary.plot(ax=ax,color=INK,lw=.5)
 ax.set(title=title,xlabel='',ylabel='');ax.set_xticks([]);ax.set_yticks([])
fig.tight_layout();save(fig,'climate')

fig,ax=plt.subplots(figsize=(9.5,3.5))
ax.barh([1,0],errors,color=[GRAY,TEAL],height=.5)
ax.set_yticks([1,0],['Temperature only','Temperature + rainfall\n+ rainfall seasonality'])
ax.set(xlim=(0,.5),xlabel='Mean absolute error (lower is better)')
for pos,e in zip([1,0],errors):ax.text(e+.008,pos,f'{e:.3f}',va='center',fontweight='bold')
ax.axvline(.5,color=CORAL,linestyle=':',linewidth=2)
fig.tight_layout();save(fig,'comparison')

grid['score']=final.predict(grid[features])
raster=grid.set_index(['y','x']).score.to_xarray().reindex(y=climate.y,x=climate.x)
fig,ax=plt.subplots(figsize=(6.4,5.8))
raster.plot(ax=ax,vmin=0,vmax=1,cmap='viridis',cbar_kwargs={'label':'Relative suitability score','shrink':.85})
maine.boundary.plot(ax=ax,color=INK,lw=.6)
ax.set(xlabel='Longitude',ylabel='Latitude',title='')
save(fig,'suitability')

fig,ax=plt.subplots(figsize=(8.2,4.2))
imp=final.feature_importances_
ax.barh([2,1,0],imp,color=TEAL,height=.5)
ax.set_yticks([2,1,0],['Temperature','Annual rainfall','Rainfall seasonality'])
ax.set(xlim=(0,1),xlabel='Contribution to tree-building improvements')
for pos,e in zip([2,1,0],imp):ax.text(e+.015,pos,f'{e:.2f}',va='center')
fig.tight_layout();save(fig,'importance')

fig,ax=plt.subplots(figsize=(6.2,5.8))
maine.boundary.plot(ax=ax,color=INK,lw=.7)
h=ax.hexbin(pres.geometry.x,pres.geometry.y,gridsize=40,mincnt=1,cmap='YlOrBr',bins='log',linewidths=.2)
fig.colorbar(h,ax=ax,shrink=.85,label='Occurrence records per hexagon (log scale)')
ax.set(xlabel='Longitude',ylabel='Latitude')
save(fig,'record-density')

summary={'species':'Boreorana sylvatica','coordinate_uncertainty_filter_m':'<100','presence_before_complete_cases':n_before,'n_presence_records':len(pres),'n_background':len(bg),'n_unique_presence_climate_vectors':len(pres[variables].drop_duplicates()),'n_train':len(train),'n_test':len(test),'background_seed':597,'split_seed':597,'forest_seed':597,'n_estimators':100,'min_samples_leaf':5,'bio1_MAE':errors[0],'three_variable_MAE':errors[1],'importance':dict(zip(features,imp.tolist())),'note':'Reproducible lecture example using complete occurrence records and seeded full-grid background sampling. Repeated occurrence cells remain. Lab background draws may differ.'}
(root/'docs/lectures/assets/Lecture07-example-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
