"""Rebuild Lecture11 figures from the original Maine data and explicit toy examples.

Run from the repository root in the Lab11 environment:
    python docs/lectures/assets/Lecture11-build-figures.py

No downloads, notebook execution, or answer-key inputs are required. Full GDMs
use all 19 bioclimatic predictors and the current Lab11 naming convention.
"""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from scipy.spatial.distance import pdist, squareform, jaccard
from shapely.geometry import box
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from gdmbayes import GDM

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
INK, MUTED, TEAL, CORAL = '#18212b', '#52606d', '#087e8b', '#d95d39'
PAPER, LINE, PALE = '#f7f8f6', '#ccd3d7', '#e6eeed'
COLORS = [TEAL, '#c48d21', '#8660a4', CORAL, '#3f6ca8', '#527b3d']
GRAINS = [10, 20, 40]
CRS = 'EPSG:26919'
plt.rcParams.update({'font.size': 17, 'font.family': 'sans-serif',
                     'figure.facecolor': PAPER, 'axes.facecolor': PAPER,
                     'savefig.facecolor': PAPER, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.spines.top': False, 'axes.spines.right': False})
# Reuse the course's original vector amphibian symbols, not a published figure.
spec = importlib.util.spec_from_file_location('lecture10_art', OUT/'Lecture10-build-figures.py')
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)

class Drawing(art.Drawing):
    def save(self):
        (OUT/f'Lecture11-{self.name}.svg').write_text('\n'.join(self.parts)+'\n</svg>\n')


def pond(d, x, y, species, label='', radius=115):
    d.ellipse(x, y, radius, 63, '#dcecef', '#9bbdc4')
    for i, sp in enumerate(species):
        d.animal(x+(i-(len(species)-1)/2)*60, y, sp, .7, True)
    if label: d.text(x, y+105, label, 27, weight=700, anchor='middle')


def schematics():
    d=Drawing('identity','Four sites have richness three, but the species identities change across the landscape.')
    for x, species, label in [(170,[0,1,2],'Site A'),(490,[0,1,2],'Site B'),
                              (810,[3,4,5],'Site C'),(1130,[3,4,5],'Site D')]:
        pond(d,x,150,species,label)
        d.text(x,330,'Richness = 3',30,TEAL,700,'middle')
        d.rect(x-105,375,210,60,TEAL if species[0]==0 else CORAL,'none',12)
    d.text(648,490,'Equal richness can hide a change in species identity.',31,weight=700,anchor='middle')
    d.save()

    rng=np.random.default_rng(11)
    pts=rng.uniform(0,1,(85,2))
    species=np.minimum((pts[:,0]*4).astype(int),3)
    d=Drawing('grain','The same invented records in an 80 kilometer landscape are divided into 10, 20 or 40 kilometer cells.')
    for panel,grain in enumerate(GRAINS):
        x=35+panel*430;y=85;size=350
        d.text(x+size/2,40,f'{grain} km cells',35,weight=700,anchor='middle')
        d.rect(x,y,size,size,'#edf0e5',LINE)
        for i in range(1,80//grain):
            s=i*size/(80//grain)
            d.line(x+s,y,x+s,y+size,'#a7b5ae',1.5)
            d.line(x,y+s,x+size,y+s,'#a7b5ae',1.5)
        for (px,py),sp in zip(pts,species):
            d.add(f'<circle cx="{x+px*size}" cy="{y+py*size}" r="5" fill="{COLORS[sp]}"/>')
        d.text(x+size/2,480,'Same records · same extent',25,MUTED,anchor='middle')
    d.save()

    d=Drawing('pooling','Four 10 kilometer cells have lists AB, BC, CD and D. A single 20 kilometer cell pools them into ABCD.')
    for (x,y),s in zip([(90,75),(310,75),(90,270),(310,270)],[[0,1],[1,2],[2,3],[3]]):
        d.rect(x,y,210,175,'white',LINE)
        d.species_row(x+62,y+75,s,80,.8)
    d.text(300,480,'Mean cell richness = 1.75',30,TEAL,700,'middle')
    d.line(565,245,720,245,TEAL,5,True)
    d.rect(785,75,425,370,'white',TEAL,10)
    d.species_row(865,245,[0,1,2,3],90,1.05)
    d.text(997,480,'Pooled richness = 4',31,TEAL,700,'middle')
    d.save()

    d=Drawing('boundary','Two nearby records fall in separate cells under one grid origin but the same cell after shifting the grid.')
    for x,offset,title in [(55,0,'Origin 1: separate lists'),(705,75,'Origin 2: pooled list')]:
        d.text(x+250,42,title,31,weight=700,anchor='middle')
        d.rect(x,90,500,330,'#edf0e5',LINE)
        d.ellipse(x+250,255,120,90,'#dcecef','#9bbdc4')
        for gx in [x+125+offset,x+250+offset,x+375+offset]:d.line(gx,90,gx,420,TEAL,3)
        d.line(x,255+offset,x+500,255+offset,TEAL,3)
        d.animal(x+225,230,0,.9,True);d.animal(x+275,285,1,.9,True)
    d.text(648,485,'Grid cells are analysis units; habitat boundaries need not follow them.',29,MUTED,anchor='middle')
    d.save()

    d=Drawing('pairs','Three sites generate three pairwise comparisons. Shared and unique species determine Jaccard dissimilarity.')
    for x,y,s,label in [(150,110,[0,1,2],'A'),(530,110,[0,1,3],'B'),(530,350,[3,4,5],'C')]:
        pond(d,x,y,s,label,radius=110)
    d.line(265,100,415,100,TEAL,3);d.text(340,75,'30 km',24,MUTED,anchor='middle')
    d.line(600,195,600,265,TEAL,3);d.text(650,240,'40 km',24,MUTED,anchor='middle')
    d.line(210,200,415,335,TEAL,3);d.text(240,300,'50 km',24,MUTED,anchor='middle')
    for i,(pair,shared,union,j) in enumerate([('A–B',2,4,.5),('B–C',1,5,.8),('A–C',0,6,1.)]):
        y=135+i*115
        d.text(800,y,pair,31,weight=700)
        d.text(965,y,f'1 − {shared}/{union}',31)
        d.text(1200,y,f'{j:.1f}',35,CORAL,700,'middle')
    d.text(1000,55,'Jaccard dissimilarity',30,TEAL,700,'middle')
    d.text(648,490,'The response is a difference between two recorded communities.',29,MUTED,anchor='middle')
    d.save()

    d=Drawing('mechanisms','Environmental gradients, dispersal barriers and uneven observations can each contribute to distance decay.')
    for x,title in [(15,'Environment'),(450,'Dispersal / history'),(885,'Observation')]:
        d.text(x+190,45,title,32,weight=700,anchor='middle')
    # A colored environment changes between two ponds.
    for i in range(12):
        d.rect(20+i*32,85,32,325,f'rgb({230-i*5},{235-i*3},{200+i*3})','none')
    pond(d,210,170,[0,1,2],'Cool / wet',100)
    pond(d,210,340,[3,4,5],'Warmer / drier',100)
    d.rect(455,85,380,325,'#edf0e5','none')
    pond(d,650,155,[0,1,2],'',100);pond(d,650,350,[3,4,5],'',100)
    d.add('<path d="M470 275 L530 220 L585 275 L660 215 L735 275 L790 230 L825 275" fill="none" stroke="#9ca69c" stroke-width="18"/>')
    d.rect(890,85,380,325,'#edf0e5','none')
    pond(d,1080,160,[0,1,2],'',100)
    pond(d,1080,340,[0],'',100)
    d.text(1080,252,'Less reporting ↓',25,CORAL,700,'middle')
    d.text(648,480,'A geographic pattern alone does not identify its cause.',31,TEAL,700,'middle')
    d.save()

    d=Drawing('dependence','Pairs AB and AC share site A. Three sites yield three pairs, not three independent ecological replicates.')
    for x,y,label,color in [(185,240,'A',CORAL),(550,100,'B',TEAL),(550,380,'C',TEAL)]:
        d.ellipse(x,y,48,48,'white',color);d.text(x,y+12,label,37,color,700,'middle')
    d.line(235,220,495,115,CORAL,6);d.line(235,260,495,365,CORAL,6)
    d.line(550,150,550,325,LINE,3)
    d.text(990,145,'A–B',43,CORAL,700,'middle')
    d.text(990,255,'A–C',43,CORAL,700,'middle')
    d.text(990,370,'Both reuse site A',30,weight=700,anchor='middle')
    d.text(648,485,'More pairs do not create more independent sampled sites.',31,MUTED,anchor='middle')
    d.save()

    d=Drawing('local','The focal ABC cell is compared with seven sampled neighbors. Three identical lists give zero, four disjoint lists give one; an unsampled cell is excluded.')
    lists=[[0,1,2],[0,1,2],[3,4,5],[0,1,2],[0,1,2],[3,4,5],[],[3,4,5],[3,4,5]]
    for i,s in enumerate(lists):
        col=i%3;row=i//3;x=55+col*195;y=45+row*140
        d.rect(x,y,185,130,'white' if s else '#d9dedc',TEAL if i==4 else LINE,8)
        if s:
            for j,sp in enumerate(s):d.animal(x+40+j*50,y+55,sp,.54,True)
        else:d.text(x+92,y+70,'No site',23,MUTED,anchor='middle')
        if i==4:d.text(x+92,y+117,'Focal cell',23,TEAL,700,'middle')
    d.text(995,110,'3 identical neighbors → 0',29,TEAL,700,'middle')
    d.text(995,190,'4 disjoint neighbors → 1',29,CORAL,700,'middle')
    d.text(995,295,'Mean = 4 / 7 = 0.57',37,weight=700,anchor='middle')
    d.text(995,375,'Gray cell is excluded',27,MUTED,anchor='middle')
    d.text(648,485,'The comparison radius grows with grain: 15, 30, then 60 km.',29,MUTED,anchor='middle')
    d.save()

    d=Drawing('gdm-inputs','Each site has climate values and a species list; GDM relates pairwise compositional difference to environmental and geographic differences.')
    for x,s,label,values in [(245,[0,1,2],'Site A',['6 °C','900 mm','… 17 more variables']),
                              (1050,[0,2,3],'Site B',['8 °C','1,200 mm','… 17 more variables'])]:
        pond(d,x,100,s,label)
        for i,v in enumerate(values):d.text(x,275+i*52,v,29,anchor='middle')
    d.line(385,90,910,90,TEAL,4,True)
    d.text(648,58,'Geographic separation',27,TEAL,700,'middle')
    d.text(648,235,'Compare both',29,weight=700,anchor='middle')
    d.text(648,285,'environments',29,weight=700,anchor='middle')
    d.text(648,420,'Observed Jaccard = 0.5',34,CORAL,700,'middle')
    d.text(648,485,'Fit the expected difference between sites, not a single species map.',28,MUTED,anchor='middle')
    d.save()

    d=Drawing('pca-workflow','Nineteen site climate predictors are GDM transformed, then compressed to two PCA coordinates for a shared color key.')
    labels=[('Site climate','19 original variables'),('GDM transforms','19 weighted columns'),('PCA','2 displayed axes'),('Map + biplot','One shared color key')]
    for i,(title,caption) in enumerate(labels):
        x=20+i*325
        d.text(x+140,55,title,30,weight=700,anchor='middle')
        if i<2:
            for j in range(19):
                h=60+(j*23)%180
                if i==1:h=25+(j*47)%220
                d.rect(x+12+j*13,350-h,9,h,COLORS[j%len(COLORS)] if i==0 else TEAL,'none')
        elif i==2:
            d.line(x+25,340,x+260,340,MUTED,2,True);d.line(x+25,340,x+25,110,MUTED,2,True)
            for j in range(20):
                px=x+45+(j*57)%200;py=130+(j*31)%190
                d.add(f'<circle cx="{px}" cy="{py}" r="8" fill="{TEAL}"/>')
        else:
            for row in range(5):
                for col in range(5):
                    color=f'rgb({50+col*45},{50+row*45},128)'
                    d.rect(x+20+col*43,120+row*43,43,43,color,'none')
        d.text(x+140,420,caption,23,MUTED,anchor='middle')
        if i<3:d.line(x+277,245,x+322,245,TEAL,3,True)
    d.text(648,490,'Keep GDM weights: do not standardize the transformed columns.',29,TEAL,700,'middle')
    d.save()

    d=Drawing('validation','Random pair splits reuse sites, while holding out a geographic group of sites tests predictions for new places.')
    for x,title,blocked in [(30,'Random pairs',False),(700,'Hold out places',True)]:
        d.text(x+260,40,title,33,weight=700,anchor='middle')
        coords=[(x+80,140),(x+250,140),(x+420,140),(x+80,340),(x+250,340),(x+420,340)]
        if blocked:
            d.rect(x+15,230,485,190,'#f6e4dd','none',12)
            pairs=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]
        else:pairs=[(0,1),(0,3),(0,4),(1,2),(1,4),(2,5),(3,4),(4,5)]
        for k,(i,j) in enumerate(pairs):
            color=CORAL if (blocked and i>=3) or (not blocked and k%3==0) else TEAL
            d.line(*coords[i],*coords[j],color,4)
        for k,(cx,cy) in enumerate(coords):
            color=CORAL if blocked and k>=3 else INK
            d.ellipse(cx,cy,30,30,'white',color);d.text(cx,cy+10,chr(65+k),27,color,700,'middle')
        d.text(x+250,465,'Same sites leak across splits' if not blocked else 'Held-out sites are genuinely new',27,MUTED,anchor='middle')
    d.save()

    d=Drawing('lab-workflow','Lab11 follows occurrences to nested grids, Jaccard differences, GDM at every grain, and PCA composition maps.')
    labels=[('Records','Map sampling'),('10 / 20 / 40 km','Build communities'),('Site pairs','Jaccard + distance'),('GDM at each grain','Geography + 19 layers'),('Composition map','PCA + two arrows')]
    for i,(a,b) in enumerate(labels):
        x=10+i*260
        d.ellipse(x+120,210,90,90,PALE,TEAL)
        d.text(x+120,225,i+1,57,TEAL,700,'middle')
        d.text(x+120,365,a,25,weight=700,anchor='middle')
        d.text(x+120,410,b,23,MUTED,anchor='middle')
        if i<4:d.line(x+215,210,x+265,210,TEAL,4,True)
    d.save()


def save(fig,name):
    fig.savefig(OUT/f'Lecture11-{name}.png',dpi=160,bbox_inches='tight',pad_inches=.18)
    plt.close(fig)


def occurrence_map(maine, records):
    fig, ax = plt.subplots(figsize=(6.5, 6), layout='constrained')
    maine.plot(ax=ax, color='#e9ece5', edgecolor='#8b9696', linewidth=.8)
    records.plot(ax=ax, markersize=2, color=TEAL, alpha=.4)
    ax.set_axis_off()
    save(fig, 'occurrences')


def toy_curves():
    x=np.linspace(2,16,300)
    g=lambda value:1.5/(1+np.exp(-(np.asarray(value)-9)/1.2))
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    axes[0].plot(x,g(x),color=TEAL,lw=4)
    for a,b,color in [(3,5,TEAL),(8,10,CORAL)]:
        axes[0].axvspan(a,b,color=color,alpha=.12)
        axes[0].scatter([a,b],g([a,b]),s=70,c=color,zorder=3)
        axes[0].plot([b,b],g([a,b]),color=color,lw=4)
    axes[0].set(xlabel='Temperature (°C)',ylabel='GDM-transformed value',title='Equal 2 °C differences',ylim=(0,1.65))
    for y,a,b,color in [(1,3,5,TEAL),(0,8,10,CORAL)]:
        axes[1].plot([0,1.5],[y,y],color=LINE,lw=3)
        axes[1].plot(g([a,b]),[y,y],color=color,lw=7)
        axes[1].scatter(g([a,b]),[y,y],c=color,s=100,zorder=3)
        axes[1].text(.75,y+.2,f'{a}–{b} °C → distance {g(b)-g(a):.2f}',ha='center',color=color)
    axes[1].set(title='Different ecological distances',xlabel='GDM-transformed value',yticks=[],ylim=(-.3,1.5),xlim=(-.06,1.56))
    save(fig,'stretching')

    fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    left=0
    for label,v,color in [('Intercept',.2,'#aab5bb'),('Climate 1',.5,TEAL),('Climate 2',.4,'#527b3d'),('Geography',.3,CORAL)]:
        axes[0].barh([0],v,left=left,color=color,height=.35,label=label)
        axes[0].text(left+v/2,0,f'{v:.1f}',ha='center',va='center',color='white',fontsize=15)
        left+=v
    axes[0].set(xlabel='Contributions to ecological distance',yticks=[],ylim=(-.4,.65),xlim=(0,1.55),title='Add nonnegative contributions')
    axes[0].legend(loc='upper left',bbox_to_anchor=(-.01,1.02),ncols=2,frameon=False,fontsize=13)
    t=np.linspace(0,5,200)
    axes[1].plot(t,1-np.exp(-t),color=TEAL,lw=4)
    axes[1].scatter([1.4],[1-np.exp(-1.4)],c=CORAL,s=120,zorder=3)
    axes[1].annotate('1.4 → 0.75',(1.4,1-np.exp(-1.4)),xytext=(2.2,.45),arrowprops={'arrowstyle':'->','color':CORAL},color=CORAL)
    axes[1].set(xlabel='Total ecological distance',ylabel='Expected dissimilarity',ylim=(0,1.04),title='Dissimilarity approaches one')
    save(fig,'gdm-link')


def get_layers():
    book=json.loads((ROOT/'docs/labs/Lab11-SpatialCommunityComposition.ipynb').read_text())
    layers=None
    for cell in book['cells']:
        if cell['cell_type']!='code':continue
        for node in ast.parse(''.join(cell['source'])).body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CLIMATE_LAYERS' for t in node.targets):
                value=ast.literal_eval(node.value)
                if len(value)==19:layers=value
    if layers is None:raise ValueError('Expected the revised Lab11 19-layer mapping.')
    return layers


def main():
    schematics();toy_curves()
    layers=get_layers();predictors=list(layers.values())
    maine_path=ROOT/'docs/labs/ME_ShapeFiles/Maine_State_Boundary.shp'
    records_path=ROOT/'docs/data/amphibians.geojson'
    maine=gpd.read_file(maine_path).to_crs(CRS).dissolve()
    records=gpd.read_file(records_path).to_crs(CRS).dropna(subset=['species'])
    records=gpd.clip(records[records.species!=''],maine)
    occurrence_map(maine, records)
    sites_by_grain={};communities={};pairs_by_grain={};bands_by_grain={}
    Xs={};ys={};models={};climate_sites={};summary={};importance={}

    for grain in GRAINS:
        print('Build and fit Maine',grain,'km; all 19 predictors',flush=True)
        width=grain*1000;points=records.copy()
        points['col']=((points.geometry.x-320_000)//width).astype(int)
        points['row']=((points.geometry.y-4_720_000)//width).astype(int)
        points['site_id']=points.col.astype(str)+'_'+points.row.astype(str)
        community=pd.crosstab(points.site_id,points.species)
        cells=[]
        for cell in points[['site_id','col','row']].drop_duplicates().itertuples():
            x=320_000+cell.col*width;y=4_720_000+cell.row*width
            cells.append({'site_id':cell.site_id,'xc':x+width/2,'yc':y+width/2,'geometry':box(x,y,x+width,y+width)})
        sites=gpd.GeoDataFrame(cells,crs=CRS).set_index('site_id')
        sites=gpd.clip(sites,maine).sort_index();community=community.loc[sites.index]
        sites['n_records']=community.sum(axis=1);sites['richness']=(community>0).sum(axis=1)
        y=pdist(community>0,'jaccard');dist=pdist(sites[['xc','yc']])/1000
        pairs=pd.DataFrame({'distance_km':dist,'jaccard':y,'similarity':1-y})
        bands=[]
        for lower in range(0,650,50):
            b=pairs[(dist>=lower)&(dist<lower+50)]
            if len(b):bands.append({'distance_km':b.distance_km.mean(),'mean_similarity':b.similarity.mean(),'n_pairs':len(b)})
        bands=pd.DataFrame(bands)
        D=squareform(dist);J=squareform(y);local=[]
        for i in range(len(sites)):
            neighbors=(D[i]>0)&(D[i]<=1.5*grain)
            local.append(J[i,neighbors].mean() if neighbors.any() else np.nan)
        sites['neighbor_dissimilarity']=local
        sites_by_grain[grain]=sites;communities[grain]=community
        pairs_by_grain[grain]=pairs;bands_by_grain[grain]=bands
        climate=sites.copy()
        for filename,name in layers.items():
            means=[]
            with rasterio.open(ROOT/'docs/data/bioclim_ME'/filename) as raster:
                for geometry in sites.to_crs(raster.crs).geometry:
                    pixels,_=mask(raster,[geometry],crop=True,filled=False,all_touched=True)
                    valid=pixels[0].compressed();means.append(float(valid.mean()) if len(valid) else np.nan)
            climate[name]=means
        climate_sites[grain]=climate
        fitted=climate.dropna(subset=predictors)
        X=fitted[['xc','yc']].copy();X['time_idx']=0;X[predictors]=fitted[predictors]
        yfit=pdist(community.loc[fitted.index]>0,'jaccard')
        baseline=GDM(geo=True,knots=0).fit(X[['xc','yc','time_idx']],yfit)
        model=GDM(geo=True,knots=0).fit(X,yfit)
        Xs[grain]=X;ys[grain]=yfit;models[grain]=model;importance[grain]=model.predictor_importance_
        summary[grain]={'n_sites':len(sites),'n_model_sites':len(X),'n_pairs':len(yfit),
                        'mean_richness':float(sites.richness.mean()),
                        'distance_similarity_rho':float(pairs.distance_km.corr(pairs.similarity,method='spearman')),
                        'geography_deviance_pct':100*baseline.explained_,
                        'all19_deviance_pct':100*model.explained_}
    imp=pd.DataFrame(importance).T
    bio_numbers={name:i for i,name in enumerate(predictors,1)}
    pretty=lambda name:f'BIO{bio_numbers[name]} · '+name.replace('_',' ')
    def climate_axis(name):
        number=bio_numbers[name]
        if number==3:return 'Isothermality (%)'
        if number==4:return 'Temperature SD × 100'
        if number==15:return 'Precipitation CV (%)'
        return 'Temperature (°C)' if number<=11 else 'Precipitation (mm)'

    def map_base(ax):
        maine.plot(ax=ax,color='#dedfda',edgecolor='#8b9696',linewidth=.7)
        ax.set_axis_off()

    vmax=max(x.richness.max() for x in sites_by_grain.values())
    fig,axes=plt.subplots(1,3,figsize=(13,5.3),layout='constrained')
    for ax,grain in zip(axes,GRAINS):
        map_base(ax);sites_by_grain[grain].plot(ax=ax,column='richness',vmin=0,vmax=vmax,cmap='viridis')
        ax.set_title(f'{grain} km\n{len(sites_by_grain[grain])} sampled sites')
    fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(0,vmax),cmap='viridis'),ax=list(axes),shrink=.72,label='Recorded species richness')
    save(fig,'richness')

    fig,axes=plt.subplots(1,3,figsize=(13,5.3),layout='constrained')
    map_base(axes[0]);records.plot(ax=axes[0],markersize=2,color=TEAL,alpha=.25);axes[0].set_title('Occurrence records')
    for ax,column,title in zip(axes[1:],['n_records','richness'],['Records per 10 km cell','Species per 10 km cell']):
        map_base(ax);sites_by_grain[10].plot(ax=ax,column=column,legend=True,cmap='viridis',legend_kwds={'shrink':.65});ax.set_title(title)
    save(fig,'sampling')

    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    p=pairs_by_grain[20];b=bands_by_grain[20]
    axes[0].scatter(p.distance_km,p.similarity,s=4,alpha=.04,c=TEAL,rasterized=True)
    axes[0].plot(b.distance_km,b.mean_similarity,c=INK,lw=3,marker='o')
    axes[0].set(title='20 km cells: pairs + band means')
    for grain,color in zip(GRAINS,[TEAL,CORAL,'#8660a4']):
        b=bands_by_grain[grain];axes[1].plot(b.distance_km,b.mean_similarity,lw=3,marker='o',color=color,label=f'{grain} km')
    axes[1].legend(frameon=False);axes[1].set_title('The pattern changes with grain')
    for ax in axes:ax.set(xlabel='Cell-center distance (km)',ylabel='Jaccard similarity',ylim=(0,1),xlim=(0,600))
    save(fig,'distance-decay')

    fig,axes=plt.subplots(1,2,figsize=(10,5.4),layout='constrained')
    for ax,col,title,cmap,limits in [(axes[0],'richness','Recorded richness','viridis',(0,vmax)),
                                    (axes[1],'neighbor_dissimilarity','Neighbor differences','magma',(0,1))]:
        map_base(ax);sites_by_grain[20].plot(ax=ax,column=col,cmap=cmap,vmin=limits[0],vmax=limits[1],legend=True,legend_kwds={'shrink':.65});ax.set_title(title)
    save(fig,'local-map')

    fig,axes=plt.subplots(1,2,figsize=(10,5.4),layout='constrained')
    for ax,name,title in zip(axes,['temperature_c','precip'],['Annual mean temperature (°C)','Annual precipitation (mm/year)']):
        map_base(ax);climate_sites[20].plot(ax=ax,column=name,legend=True,legend_kwds={'shrink':.65},cmap='viridis');ax.set_title(title,fontsize=16)
    save(fig,'climate')

    def curve(model,X,name):
        a=pd.DataFrame({column:np.repeat(X[column].median(),100) for column in X.columns})
        a[name]=np.linspace(X[name].min(),X[name].max(),100)
        effect=model.gdm_transform(a).sum(axis=1)
        return a[name],effect-effect[0]

    top_climate=list(imp.loc[20,predictors].nlargest(3).index)
    fig,axes=plt.subplots(1,3,figsize=(13,4.6),layout='constrained')
    for ax,name in zip(axes,top_climate):
        for grain,color in zip(GRAINS,[TEAL,CORAL,'#8660a4']):
            a,b=curve(models[grain],Xs[grain],name);ax.plot(a,b,lw=3,label=f'{grain} km',c=color)
        ax.set(title=pretty(name).replace(' · ','\n'),xlabel=climate_axis(name),ylabel='Partial ecological distance')
    axes[0].legend(frameon=False);save(fig,'curves')

    names=list(imp.loc[20,predictors].nlargest(6).index)
    fig,ax=plt.subplots(figsize=(11,5.1),layout='constrained')
    for i,(grain,color) in enumerate(zip(GRAINS,[TEAL,CORAL,'#8660a4'])):
        ax.barh(np.arange(6)+(i-1)*.24,imp.loc[grain,names],height=.22,label=f'{grain} km',color=color)
    ax.set_yticks(range(6),[pretty(name) for name in names],fontsize=14)
    ax.invert_yaxis();ax.set_xlabel('Fitted transformation height');ax.legend(frameon=False)
    save(fig,'importance')

    fig,axes=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    for i,(col,label,color) in enumerate([('geography_deviance_pct','Geography',LINE),('all19_deviance_pct','Geography + 19 climate',TEAL)]):
        axes[0].bar(np.arange(3)+(i-.5)*.3,[summary[g][col] for g in GRAINS],width=.28,label=label,color=color)
    axes[0].set_xticks(range(3),[f'{g} km' for g in GRAINS]);axes[0].set(ylabel='Training deviance explained (%)');axes[0].legend(frameon=False,fontsize=13)
    pred=models[20].predict(Xs[20]);axes[1].scatter(pred,ys[20],s=6,c=TEAL,alpha=.05,rasterized=True)
    axes[1].plot([0,1],[0,1],c=CORAL,ls='--',lw=2)
    axes[1].set(xlabel='Predicted dissimilarity',ylabel='Observed dissimilarity',xlim=(0,1),ylim=(0,1),title='20 km training pairs')
    save(fig,'fit')

    weighted=models[20].gdm_transform(Xs[20]);n_basis=models[20].preprocessor_.n_spline_bases_
    transformed=pd.DataFrame(index=Xs[20].index)
    for i,name in enumerate(predictors):transformed[name]=weighted[:,i*n_basis:(i+1)*n_basis].sum(axis=1)
    pca=PCA(n_components=2);scores=pca.fit_transform(transformed)
    rgb=np.column_stack([MinMaxScaler(clip=True).fit_transform(scores),np.full(len(scores),.5)])
    loadings=pd.DataFrame(pca.components_.T*np.sqrt(pca.explained_variance_),index=predictors,columns=['PC1','PC2'])
    loadings['length']=np.sqrt(loadings.PC1**2+loadings.PC2**2)
    loadings=loadings.sort_values('length',ascending=False);selected=list(loadings.head(2).index)
    pca_sites=climate_sites[20].loc[Xs[20].index]
    fig,axes=plt.subplots(1,2,figsize=(12,5.6),layout='constrained')
    map_base(axes[0]);pca_sites.plot(ax=axes[0],color=rgb);axes[0].set_title('Expected composition · 20 km')
    axes[1].scatter(scores[:,0],scores[:,1],c=rgb,s=35)
    for name in selected:
        v=loadings.loc[name,['PC1','PC2']].to_numpy()
        axes[1].annotate('',xy=v,xytext=(0,0),arrowprops={'arrowstyle':'->','color':INK,'lw':2})
        axes[1].annotate(f'BIO{bio_numbers[name]}',xy=v,xytext=(6,6),textcoords='offset points',fontsize=15)
    axes[1].set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.1%})',title='Same sites · same colors')
    axes[1].set_aspect('equal');save(fig,'pca')
    fig,ax=plt.subplots(figsize=(5.8,6.6),layout='constrained');map_base(ax);pca_sites.plot(ax=ax,color=rgb);save(fig,'pca-map')
    fig,axes=plt.subplots(1,2,figsize=(10,5.3),layout='constrained')
    for ax,name in zip(axes,selected):
        map_base(ax);pca_sites.plot(ax=ax,column=name,cmap='viridis',legend=True,legend_kwds={'shrink':.65});ax.set_title(pretty(name).replace(' · ','\n'),fontsize=16)
    save(fig,'pca-gradients')

    fig,axes=plt.subplots(1,3,figsize=(13,5.4),layout='constrained')
    for ax in axes:map_base(ax)
    sites_by_grain[20].plot(ax=axes[0],column='richness',cmap='viridis');axes[0].set_title('How many species?')
    sites_by_grain[20].plot(ax=axes[1],column='neighbor_dissimilarity',cmap='magma',vmin=0,vmax=1);axes[1].set_title('How different nearby?')
    pca_sites.plot(ax=axes[2],color=rgb);axes[2].set_title('Which expected composition?')
    save(fig,'three-questions')

    sensitivity={}
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    for grain,color in zip(GRAINS,[TEAL,CORAL,'#8660a4']):
        sites=sites_by_grain[grain];sites=sites[sites.n_records>=5]
        community=communities[grain].loc[sites.index]
        D=pdist(sites[['xc','yc']])/1000;similarity=1-pdist(community>0,'jaccard')
        means=[];centers=[]
        for lower in range(0,650,50):
            keep=(D>=lower)&(D<lower+50)
            if keep.any():means.append(float(similarity[keep].mean()));centers.append(float(D[keep].mean()))
        sensitivity[grain]={'n_sites':len(sites),'mean_richness':float(sites.richness.mean()),
                            'distance_similarity_rho':float(pd.Series(D).corr(pd.Series(similarity),method='spearman'))}
        if grain==10:
            b=bands_by_grain[grain];axes[1].plot(b.distance_km,b.mean_similarity,c=TEAL,lw=3,label='Minimum 1 record')
            axes[1].plot(centers,means,c=CORAL,lw=3,label='Minimum 5 records')
    for i,(threshold,color) in enumerate([(1,TEAL),(5,CORAL)]):
        counts=[summary[g]['n_sites'] if threshold==1 else sensitivity[g]['n_sites'] for g in GRAINS]
        axes[0].bar(np.arange(3)+(i-.5)*.3,counts,width=.28,color=color,label=f'Minimum {threshold}')
    axes[0].set_xticks(range(3),[f'{g} km' for g in GRAINS]);axes[0].set_ylabel('Sampled cells');axes[0].legend(frameon=False)
    axes[1].set(title='10 km distance decay',xlabel='Cell-center distance (km)',ylabel='Mean Jaccard similarity',ylim=(0,1));axes[1].legend(frameon=False,fontsize=14)
    save(fig,'sensitivity')

    # Validation and provenance accompany every empirical slide.
    assert len(predictors)==19 and transformed.shape[1]==19
    assert np.isfinite(scores).all() and len(selected)==2
    for grain in GRAINS:
        assert list(Xs[grain].columns)==['xc','yc','time_idx']+predictors
        assert len(ys[grain])==len(Xs[grain])*(len(Xs[grain])-1)//2
        assert int(communities[grain].to_numpy().sum())==len(records)
    inputs=[records_path,*sorted(maine_path.parent.glob('Maine_State_Boundary.*')),
            *[ROOT/'docs/data/bioclim_ME'/filename for filename in layers]]
    provenance={'description':'Original Maine occurrence data; all 19 predictors, not Lab10 synthetic parks or California answer-key data',
                'n_records':len(records),'n_species':int(records.species.nunique()),'crs':CRS,'origin_m':[320000,4720000],
                'grains_km':GRAINS,'min_records':1,'gdm':{'geo':True,'knots':0},'climate_layers':layers,
                'summary':summary,'predictor_importance':importance,'sensitivity_min5':sensitivity,
                'pca_grain_km':20,'pca_standardized':False,'pca_variance_ratio':pca.explained_variance_ratio_.tolist(),
                'pca_top_predictors':selected,'pca_loading_selection':'Euclidean loading-vector length in PC1/PC2 plane',
                'top_climate_curves':top_climate,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                'toy_jaccard':{'AB':.5,'BC':.8,'AC':1.},'toy_pooling_mean_richness':1.75,
                'toy_local_mean_dissimilarity':4/7,'toy_gdm_total_distance':1.4,'toy_gdm_expected_dissimilarity':float(1-np.exp(-1.4))}
    (OUT/'Lecture11-example-results.json').write_text(json.dumps(provenance,indent=2,allow_nan=False)+'\n')
    loadings.to_csv(OUT/'Lecture11-pca-loadings.csv');pd.DataFrame(summary).T.to_csv(OUT/'Lecture11-grain-comparison.csv')
    assert jaccard([1,1,1,0,0,0],[1,1,0,1,0,0])==.5
    assert np.isclose(jaccard([1,1,0,1,0,0],[0,0,0,1,1,1]),.8)
    print('Built Lecture11 teaching diagrams, original-data figures, and provenance.',flush=True)

if __name__=='__main__':main()
