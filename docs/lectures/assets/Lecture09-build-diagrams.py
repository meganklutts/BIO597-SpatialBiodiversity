"""Build the lecture's schematic SVG figures (Python standard library only).

All samples, dosages, relationships and scores in these diagrams are invented.
They explain mechanisms; fitted PNGs are built by Lecture09-build-figures.py.
Run: python docs/lectures/assets/Lecture09-build-diagrams.py
"""
from html import escape
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent
W, H = 1296, 500
INK, MUTED, TEAL, CORAL = "#18212b", "#52606d", "#087e8b", "#d95d39"
PAPER, LINE, PALE = "#f7f8f6", "#ccd3d7", "#e6eeed"
DOSAGE = {0: "#ffffff", 1: "#969696", 2: "#111111"}
SAMPLES = [(0.08, .18), (.14, .65), (.22, .38), (.30, .86),
           (.38, .12), (.46, .58), (.54, .36), (.62, .82),
           (.70, .18), (.78, .58), (.86, .38), (.92, .88)]


class Drawing:
    def __init__(self, name, title, height=H):
        self.name, self.height = name, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" role="img" aria-labelledby="title">',
                      f'<title id="title">{escape(title)}</title>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>']

    def rect(self, x, y, w, h, fill="none", stroke=LINE, r=0, dash=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')

    def text(self, x, y, text, size=24, color=INK, weight=400, anchor="start", rotate=None):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"'+(f' transform="rotate({rotate} {x} {y})"' if rotate else '')+f'>{escape(str(text))}</text>')

    def line(self, x1, y1, x2, y2, color=LINE, width=2, arrow=False, dash=None):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')

    def circle(self, x, y, r=13, fill="white", stroke=INK, width=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def path(self, points, color=TEAL, width=4, dash=None):
        coords = ' '.join(f'{x:.2f},{y:.2f}' for x, y in points)
        self.parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')

    def tree(self, x, y, size=1, color=TEAL):
        for a,b,c,d in [(0,0,-18,20),(0,0,18,20),(-18,20,-29,40),(-18,20,-8,40),(18,20,8,40),(18,20,29,40)]:
            self.line(x+a*size,y+b*size,x+c*size,y+d*size,color,2.5)
        for a,b in [(0,0),(-18,20),(18,20),(-29,40),(-8,40),(8,40),(29,40)]:
            self.circle(x+a*size,y+b*size,3*size,color,color)

    def axes(self, x, y, w, h, xlabel="Temperature →", ylabel="Rainfall →"):
        self.line(x,y,x,y-h,INK,2)
        self.line(x,y,x+w,y,INK,2)
        self.text(x+w/2,y+34,xlabel,21,MUTED,anchor="middle")
        self.text(x-27,y-h/2,ylabel,21,MUTED,anchor="middle",rotate=-90)

    def legend(self, y=25, x=820):
        self.text(x-30,y+7,"Dosage",22,MUTED,anchor="end")
        for i in range(3):
            self.circle(x+90*i,y,13,DOSAGE[i])
            self.text(x+90*i+22,y+7,i,23)

    def save(self):
        (OUT/f'Lecture09-{self.name}.svg').write_text('\n'.join(self.parts)+"\n</svg>\n")


def dose_plot(d, x, y, w, h, dosages, ids=False):
    d.axes(x,y,w,h)
    for i, ((a,b), dose) in enumerate(zip(SAMPLES,dosages)):
        px, py = x+a*w, y-b*h
        d.circle(px,py,13,DOSAGE[dose])
        if ids:
            d.text(px+17,py+5,chr(65+i),15,MUTED)


def forests():
    d=Drawing('snp-forests', 'Same twelve samples in environmental space, colored by dosage at three SNPs; a separate forest learns each SNP.', 530)
    d.text(24,30,'Same samples. Same environments. Different SNP responses.',27,weight=700)
    d.legend(y=72,x=950)
    doses=[[0,0,0,1,0,1,1,1,2,2,2,2],
           [0,2,1,2,0,1,1,2,0,1,1,2],
           [1,0,0,0,1,2,2,1,1,0,0,1]]
    for k,dosages in enumerate(doses):
        x=65+k*424
        d.text(x+155,116,f'SNP {chr(65+k)}',28,weight=700,anchor='middle')
        dose_plot(d,x,350,300,220,dosages,ids=True)
        d.line(x+150,398,x+150,433,TEAL,3,arrow=True)
        for tx in [x+90,x+150,x+210]: d.tree(tx,450,.8)
        d.text(x+150,521,f'Forest {chr(65+k)}',26,TEAL,700,anchor='middle')
    d.save()


def response():
    d=Drawing('response-cartoon','The same climate axes can support occurrence labels or individual SNP dosages.')
    d.text(320,40,'Where is the species recorded?',29,weight=700,anchor='middle')
    d.text(1000,40,'How do genotypes vary?',29,weight=700,anchor='middle')
    d.axes(95,350,410,240)
    for i,(a,b) in enumerate(SAMPLES):
        present=i in [3,5,6,7,9,11]
        d.circle(95+a*410,350-b*240,15,TEAL if present else 'white',TEAL if present else MUTED)
    dose_plot(d,800,350,410,240,[0,0,0,1,0,1,1,1,2,2,2,2])
    d.line(565,225,705,225,TEAL,4,arrow=True)
    d.text(635,195,'Change y',26,TEAL,700,anchor='middle')
    d.circle(130,420,12,TEAL,TEAL);d.text(152,427,'Presence',22)
    d.circle(330,420,12,'white',MUTED);d.text(352,427,'Background',22)
    d.legend(y=420,x=930)
    d.text(320,480,'Map relative suitability',27,TEAL,700,anchor='middle')
    d.text(1000,480,'Map modeled turnover',27,TEAL,700,anchor='middle')
    d.save()


def dosage():
    d=Drawing('dosage-cartoon','Two chromosome copies encode dosage zero, one or two; a missing call is shown separately.')
    for i,(gt,alleles,label) in enumerate([('0/0',('R','R'),'0 alternate copies'),('0/1',('R','A'),'1 alternate copy'),('1/1',('A','A'),'2 alternate copies'),('./.',('?','?'),'Missing call')]):
        x=30+i*325
        d.text(x+135,55,gt,38,weight=700,anchor='middle')
        for j,a in enumerate(alleles):
            xx=x+100+j*70
            d.rect(xx-14,100,28,125,PALE,LINE,r=14)
            d.circle(xx,162,22,TEAL if a=='A' else 'white', TEAL if a=='A' else INK)
            d.text(xx,170,a,23,'white' if a=='A' else INK,700,anchor='middle')
        d.line(x+135,247,x+135,285,TEAL,3,arrow=True)
        if i<3:
            d.circle(x+135,350,44,DOSAGE[i],width=3)
            d.text(x+135,360,i,31,'white' if i==2 else INK,700,anchor='middle')
        else:
            d.rect(x+91,306,88,88,'none',MUTED,r=8,dash='7 5')
            d.text(x+135,360,'?',39,MUTED,700,anchor='middle')
        d.text(x+135,445,label,24,anchor='middle')
    d.text(648,492,'R = reference allele     A = alternate allele',23,MUTED,anchor='middle')
    d.save()


def filtering():
    d=Drawing('filtering-cartoon','Four visual filtering steps: call rate, minor allele frequency, one SNP per RAD contig, reproducible subset.')
    labels=[('1','Enough calls','Call rate ≥ 80%'),('2','Enough variation','Minor allele frequency ≥ 5%'),('3','Less local repetition','One SNP per RAD contig'),('4','A manageable subset','Up to 256 SNPs; seed 42')]
    for i,(n,title,subtitle) in enumerate(labels):
        x=12+i*325
        d.circle(x+35,48,23,TEAL,TEAL);d.text(x+35,56,n,24,'white',700,anchor='middle')
        d.text(x+150,110,title,25,weight=700,anchor='middle')
        if i==0:
            for j in range(10):
                xx=x+46+(j%5)*51; yy=195+(j//5)*66
                d.circle(xx,yy,18,TEAL if j<8 else 'white',TEAL if j<8 else LINE)
                if j>=8:d.text(xx,yy+7,'?',21,MUTED,anchor='middle')
            d.text(x+150,330,'8 called / 10 samples',22,MUTED,anchor='middle')
        elif i==1:
            for j in range(20):
                d.circle(x+38+(j%5)*55,175+(j//5)*37,12,INK if j==0 else 'white')
            d.text(x+150,330,'1 minor / 20 called alleles',21,MUTED,anchor='middle')
        elif i==2:
            for row in range(3):
                yy=185+row*48
                d.line(x+32,yy,x+275,yy,MUTED,3)
                for j in range(5):
                    xx=x+55+j*45
                    d.line(xx,yy-13,xx,yy+13,TEAL if j==0 else LINE,5)
                d.circle(x+55,yy,22,'none',TEAL)
            d.text(x+150,345,'Keep one eligible site',22,MUTED,anchor='middle')
        else:
            for j in range(64):
                d.circle(x+61+(j%8)*25,170+(j//8)*22,7,TEAL,TEAL)
            d.text(x+150,365,'A repeatable sample',22,MUTED,anchor='middle')
        d.text(x+150,432,subtitle,20,TEAL,700,anchor='middle')
    d.save()


def oob():
    d=Drawing('oob-cartoon','Predict individual A using only trees whose bootstrap training sample excludes A.')
    d.text(40,34,'Bootstrap training samples',27,weight=700)
    d.text(785,34,'Can this tree predict A out of bag?',27,weight=700,anchor='middle')
    for row,(samples,eligible,pred) in enumerate([('ABBCEF',False,None),('BCCDEF',True,'.8'),('BBCDEF',True,'1.2')]):
        yy=112+row*122
        for j,sample in enumerate(samples):
            xx=65+j*62
            dose={'A':1,'B':0,'C':1,'D':0,'E':2,'F':2}[sample]
            d.circle(xx,yy,23,DOSAGE[dose],CORAL if sample=='A' else INK,3 if sample=='A' else 2)
            d.text(xx,yy+8,sample,24,'white' if dose==2 else INK,weight=700,anchor='middle')
        d.line(430,yy,495,yy,TEAL,3,arrow=True)
        d.tree(545,yy-24,1.1,TEAL if eligible else MUTED)
        d.line(596,yy,674,yy,TEAL if eligible else LINE,3,arrow=eligible)
        d.text(705,yy+8,'A left out' if eligible else 'A used in training',25,TEAL if eligible else CORAL,700)
        if eligible:
            d.text(1018,yy+8,pred,30,TEAL,700,anchor='middle')
        else:
            d.text(1018,yy+8,'Skip',27,MUTED,anchor='middle')
    d.rect(774,421,484,65,PALE,'none',r=8)
    d.text(1016,462,'OOB prediction for A = 1.0',28,TEAL,700,anchor='middle')
    d.line(1110,234,1198,234,TEAL,3)
    d.line(1110,356,1198,356,TEAL,3)
    d.line(1198,234,1198,410,TEAL,3,arrow=True)
    d.text(43,462,'A’s observed dosage = 1',28,weight=700)
    d.save()


def r2():
    d=Drawing('r2-cartoon','Three toy prediction sets with R squared 1, 0 and minus 3, shown against observed genotypes.')
    observed=[0,0,1,1,2,2]
    for i,(pred,label,score,color) in enumerate([([0,0,1,1,2,2],'Perfect prediction','1',TEAL),([1]*6,'Predict the mean','0',MUTED),([2,2,1,1,0,0],'Larger errors','−3',CORAL)]):
        x=65+i*430
        d.text(x+140,36,label,27,weight=700,anchor='middle')
        d.line(x,296,x+290,296,INK,2)
        d.line(x,296,x,83,INK,2)
        for val in range(3):d.text(x-16,292-val*86,str(val),21,MUTED,anchor='end')
        for j,(obs,p) in enumerate(zip(observed,pred)):
            xx=x+24+j*49; yy=282-obs*86; py=282-p*86
            d.line(xx,yy,xx,py,CORAL,4)
            d.circle(xx,yy,12,DOSAGE[obs])
            d.line(xx-8,py-8,xx+8,py+8,TEAL,3);d.line(xx-8,py+8,xx+8,py-8,TEAL,3)
        d.text(x+140,330,'Individuals',22,MUTED,anchor='middle')
        d.text(x+140,401,'R² = '+score,41,color,700,anchor='middle')
    d.circle(380,467,11,DOSAGE[1]);d.text(401,474,'Observed dosage',22)
    d.line(647,459,663,475,TEAL,3);d.line(647,475,663,459,TEAL,3);d.text(676,474,'Prediction',22)
    d.line(889,457,889,478,CORAL,4);d.text(906,474,'Error',22)
    d.save()


def permutation():
    d=Drawing('permutation-cartoon','Shuffle temperature among six OOB individuals while keeping their observed dosages and the fitted prediction rule fixed.')
    xs=[5,7,9,11,13,15]
    shuffled=[13,5,15,7,11,9]
    dosages=[0,0,1,1,2,2]
    for i,(values,title) in enumerate([(xs,'Original climate'),(shuffled,'Shuffle temperature')]):
        x=60+i*454
        d.text(x+155,42,title,28,weight=700,anchor='middle')
        d.axes(x,335,320,225,'Temperature →','Dosage')
        def px(v):return x+20+(v-5)*28
        def py(v):return 315-v*92
        # The same fitted rule is drawn in both panels. MSE is calculated below.
        rule=[(px(5),py(0)),(px(8),py(0)),(px(8),py(1)),(px(12),py(1)),(px(12),py(2)),(px(15),py(2))]
        d.path(rule,TEAL,3)
        squared=[]
        for j,(v,dose) in enumerate(zip(values,dosages)):
            pred=0 if v<8 else 1 if v<12 else 2
            squared.append((pred-dose)**2)
            d.line(px(v),py(dose),px(v),py(pred),CORAL,4)
            d.circle(px(v),py(dose),14,DOSAGE[dose])
            d.text(px(v)+17,py(dose)+6,chr(65+j),17,MUTED)
        mse=sum(squared)/len(squared)
        d.text(x+155,410,f'MSE = {mse:.2f}',29,TEAL if i==0 else CORAL,700,anchor='middle')
    d.line(419,230,476,230,CORAL,3,arrow=True)
    d.text(1137,166,'Error',30,weight=700,anchor='middle')
    d.text(1137,206,'increases',30,weight=700,anchor='middle')
    d.text(1137,285,'+1.33',48,CORAL,700,anchor='middle')
    d.text(648,482,'Same individuals and dosages. Same fitted rule. Only temperature is shuffled.',25,MUTED,anchor='middle')
    d.save()


def correlation():
    d=Drawing('correlation-cartoon','Marginal shuffling can break correlated climate combinations; coarse conditional shuffling limits that disruption.')
    for i,title in enumerate(['Shuffle across all samples','Shuffle within climate groups']):
        x=110+i*680
        d.text(x+200,40,title,28,weight=700,anchor='middle')
        if i:
            for j in range(3):
                d.rect(x,350-j*85,420,85,PALE if j%2==0 else '#f0f3f2','none')
        d.axes(x,435,420,285,'Annual temperature →','Coldest-month temperature →')
        for j in range(13):
            xx=x+35+j*28; yy=411-j*19+([0,7,-5][j%3])
            d.circle(xx,yy,8,TEAL,TEAL)
        start=(x+145,335)
        end=(x+345,335) if i==0 else (x+180,335)
        d.circle(*start,14,'white',INK)
        d.line(start[0]+17,start[1],end[0]-18,end[1],CORAL if i==0 else TEAL,4,arrow=True)
        d.circle(*end,14,'white',CORAL if i==0 else TEAL,3)
        d.text(x+210,100,'Breaks the original relationship' if i==0 else 'Keeps some coarse associations',23,CORAL if i==0 else TEAL,anchor='middle')
    d.save()


def allocation():
    d=Drawing('allocation-cartoon','A retained SNP with OOB R squared 0.40 allocates 0.30 to temperature and 0.10 to rainfall; predictor allocations are averaged across SNPs.')
    d.text(90,45,'One retained SNP',29,weight=700)
    d.text(91,116,'OOB R² = 0.40',34,TEAL,700)
    d.rect(90,150,600,78,TEAL,'none',r=3)
    d.rect(540,150,150,78,CORAL,'none')
    d.text(315,200,'0.30',35,'white',700,anchor='middle')
    d.text(615,200,'0.10',35,'white',700,anchor='middle')
    d.text(315,268,'Temperature',27,TEAL,700,anchor='middle')
    d.text(615,268,'Rainfall',27,CORAL,700,anchor='middle')
    d.text(390,328,'3:1 share of positive permutation importance',24,MUTED,anchor='middle')
    d.line(745,190,832,190,TEAL,4,arrow=True)
    d.text(1030,68,'Repeat for every',28,weight=700,anchor='middle')
    d.text(1030,104,'contributing SNP',28,weight=700,anchor='middle')
    for row,(temp,rain) in enumerate([(.30,.10),(.05,.15),(.20,.10)]):
        yy=157+row*64
        d.rect(900,yy,temp*700,32,TEAL,'none')
        d.rect(900+temp*700,yy,rain*700,32,CORAL,'none')
    d.line(1030,360,1030,405,TEAL,3,arrow=True)
    d.text(1030,453,'Average by predictor',27,TEAL,700,anchor='middle')
    d.save()


def splits():
    d=Drawing('splits-cartoon','Tree split locations are smoothed and density corrected, then integrated into a cumulative turnover curve.')
    titles=['Useful tree splits','Smooth and density-correct','Accumulate change']
    for i,title in enumerate(titles):
        x=65+i*438
        d.text(x+140,45,title,25,weight=700,anchor='middle')
        d.axes(x,356,285,230,'Environmental value →','Split improvement' if i==0 else 'Turnover mass' if i==1 else 'Cumulative importance')
        if i==0:
            values=[.05,.18,.31,.40,.43,.46,.48,.49,.51,.53,.54,.56,.59,.68,.81,.94]
            for j,v in enumerate(values):
                d.line(x+v*280,352,x+v*280,352-35-(j%4)*23,TEAL,4)
        elif i==1:
            pts=[(x+t*280,350-195*math.exp(-((t-.51)/.15)**2)) for t in [j/100 for j in range(101)]]
            d.path(pts,TEAL,4)
        else:
            pts=[(x+t*280,350-215/(1+math.exp(-14*(t-.51)))) for t in [j/100 for j in range(101)]]
            d.path(pts,TEAL,4)
        d.line(x+112,110,x+112,356,CORAL,1.5,dash='5 5')
        d.line(x+170,110,x+170,356,CORAL,1.5,dash='5 5')
    d.line(377,240,421,240,TEAL,3,arrow=True)
    d.line(815,240,859,240,TEAL,3,arrow=True)
    d.text(648,446,'The same environmental interval carries the strongest change through each step.',26,MUTED,anchor='middle')
    d.save()


def transform():
    d=Drawing('transform-cartoon','Two equal differences in raw environment become different distances in turnover coordinates after transformation.')
    d.text(210,36,'Equal climate differences',27,weight=700,anchor='middle')
    d.text(665,36,'Through the turnover curve',27,weight=700,anchor='middle')
    d.text(1120,36,'Different turnover distances',27,weight=700,anchor='middle')
    d.line(45,230,373,230,INK,2)
    raw=[.1,.3,.4,.6]
    trans=[.025,.075,.1,.8]
    for i,v in enumerate(raw):
        xx=45+v*460
        d.circle(xx,230,11,TEAL if i<2 else CORAL,TEAL if i<2 else CORAL)
        d.text(xx,202,chr(65+i),23,TEAL if i<2 else CORAL,700,anchor='middle')
    for a,b,yy,c in [(.1,.3,284,TEAL),(.4,.6,330,CORAL)]:
        d.line(45+a*460,yy,45+b*460,yy,c,5)
        d.text(45+(a+b)/2*460,yy+35,'Same Δ',23,c,700,anchor='middle')
    x,y,w,h=520,390,300,260
    d.axes(x,y,w,h,'Raw environment →','Cumulative importance')
    curve=[(0,0),(.2,.05),(.4,.1),(.6,.8),(.8,.95),(1,1)]
    d.path([(x+a*w,y-b*h) for a,b in curve],TEAL,4)
    for i,(a,b) in enumerate(zip(raw,trans)):
        c=TEAL if i<2 else CORAL
        d.circle(x+a*w,y-b*h,9,c,c)
        dx,dy=[(-20,28),(-18,-18),(17,23),(14,-14)][i]
        d.text(x+a*w+dx,y-b*h+dy,chr(65+i),22,c,700)
    d.line(1060,400,1060,115,INK,2)
    for i,v in enumerate(trans):
        yy=400-v*285
        c=TEAL if i<2 else CORAL
        d.circle(1060,yy,8,c,c)
        # Stagger labels near the base so A, B and C stay distinct.
        tx=1034 if i in (0,2) else 1082
        d.text(tx,yy+(-8 if i==2 else 7),chr(65+i),23,c,700,anchor='end' if tx<1060 else 'start')
    d.line(1150,400-trans[2]*285,1150,400-trans[3]*285,CORAL,5)
    d.text(1173,278,'Large',24,CORAL,700)
    d.text(1173,309,'change',24,CORAL,700)
    d.line(420,240,470,240,TEAL,3,arrow=True)
    d.line(855,240,922,240,TEAL,3,arrow=True)
    d.text(648,488,'Crossing a steep section separates locations much more than crossing a flat section.',26,MUTED,anchor='middle')
    d.save()


def extrapolation():
    d=Drawing('coverage-cartoon','Three map interpretation issues: missing predictors, clamped values outside training ranges, and new combinations of familiar predictor values.')
    for x,title in [(30,'Missing climate'),(468,'Outside the range'),(916,'New combination')]:
        d.text(x+150,42,title,27,weight=700,anchor='middle')
    for i in range(36):
        x=62+(i%6)*43; y=125+(i//6)*43
        missing=i in [8,9,14,15]
        d.rect(x,y,39,39,'white' if missing else '#6ea99e','white')
        if missing:
            d.line(x+8,y+8,x+31,y+31,LINE,2)
            d.line(x+8,y+31,x+31,y+8,LINE,2)
    d.text(177,443,'Mask the output pixel',24,TEAL,700,anchor='middle')
    d.axes(485,365,300,230,'Environmental value →','Turnover')
    d.path([(485,350),(545,350)],MUTED,4,dash='6 5')
    d.path([(545,350),(580,342),(610,300),(642,185),(675,155),(720,150)],TEAL,4)
    d.path([(720,150),(790,150)],MUTED,4,dash='6 5')
    for xx in [545,720]:d.line(xx,100,xx,370,CORAL,1.5,dash='5 5')
    d.text(634,405,'Training range',22,MUTED,anchor='middle')
    d.text(635,443,'Clamp to endpoints',24,TEAL,700,anchor='middle')
    d.axes(952,365,280,230,'Temperature →','Rainfall →')
    for j in range(14):
        a=.10+(j%7)*.055+(j//7)*.42
        b=.12+(j%7)*.04+(j//7)*.50
        d.circle(952+a*280,365-b*230,7,TEAL,TEAL)
    d.rect(970,170,245,172,'none',LINE,dash='5 5')
    d.circle(1188,313,17,'white',CORAL,3)
    d.text(1188,320,'?',23,CORAL,700,anchor='middle')
    d.text(1092,443,'In range ≠ well sampled',24,CORAL,700,anchor='middle')
    d.save()


def arrows():
    d=Drawing('arrows-cartoon','An enlarged schematic PCA biplot with neighboring sample scores and environmental arrows.')
    d.line(250,286,1015,286,LINE,2)
    d.line(570,465,570,80,LINE,2)
    d.text(1026,292,'PC1',24,MUTED)
    d.text(570,58,'PC2',24,MUTED,anchor='middle')
    points=[(330,345,'#5364a3'),(350,362,'#5364a3'),(378,337,'#607ea5'),(448,316,'#538fa1'),(610,240,'#819e66'),(743,207,'#b3ad51'),(790,189,'#b3ad51'),(853,251,'#c98a62'),(913,242,'#c98a62')]
    for x,y,c in points:d.circle(x,y,14,c,'white')
    d.line(570,286,874,137,TEAL,5,arrow=True)
    d.text(888,127,'Temperature',27,TEAL,700)
    d.line(570,286,706,391,CORAL,5,arrow=True)
    d.text(725,412,'Rainfall',27,CORAL,700)
    d.text(54,124,'Nearby points:',27,weight=700)
    d.text(54,160,'similar PC1/2 scores',24,MUTED)
    d.line(252,175,352,321,MUTED,2,arrow=True)
    d.text(900,345,'Arrow direction:',27,weight=700)
    d.text(900,382,'increasing values',24,MUTED)
    d.text(900,454,'Length: contribution',24,MUTED)
    d.text(900,485,'to these two axes',24,MUTED)
    d.save()


def inference():
    d=Drawing('inference-cartoon','Adaptation and shared spatial history can produce similar observed climate-genotype associations; independent evidence is needed.')
    for i,title in enumerate(['Local adaptation?','Shared spatial history?']):
        x=30+i*680
        d.text(x+275,40,title,30,weight=700,anchor='middle')
        d.line(x+40,320,x+520,320,MUTED,3,arrow=True)
        d.text(x+280,362,'Climate gradient',24,MUTED,anchor='middle')
        for j in range(9):
            d.circle(x+60+j*54,265,18,DOSAGE[j//3])
        d.text(x+280,421,'Same observed dosage pattern',25,TEAL,700,anchor='middle')
    for x,label in [(50,'Climate'),(236,'Selection'),(435,'Genotypes')]:
        d.text(x,145,label,26,TEAL,700)
    d.line(151,136,212,136,TEAL,3,arrow=True)
    d.line(360,136,415,136,TEAL,3,arrow=True)
    d.text(765,113,'Climate',25,TEAL,700)
    d.text(992,82,'Geography',25,MUTED,700,anchor='middle')
    d.text(1000,166,'Ancestry',25,TEAL,700,anchor='middle')
    d.text(1168,166,'Genotypes',25,TEAL,700,anchor='middle')
    d.line(940,89,850,108,MUTED,2,arrow=True)
    d.line(997,97,997,136,MUTED,2,arrow=True)
    d.line(1061,157,1092,157,TEAL,2,arrow=True)
    d.text(648,490,'A convincing map motivates a hypothesis; fitness and population evidence help test it.',26,MUTED,anchor='middle')
    d.save()


def workflow():
    d=Drawing('workflow-cartoon','Five illustrated lab steps: align inputs, fit forests, diagnose skill, read curves and maps, and export results.')
    titles=['Align','Fit','Diagnose','Interpret','Export']
    for i,title in enumerate(titles):
        x=18+i*261
        d.text(x+111,66,title,29,weight=700,anchor='middle')
        if i==0:
            for row in range(4):
                yy=148+row*43
                d.text(x+12,yy+7,chr(65+row),22,MUTED)
                for j in range(3):d.rect(x+48+j*48,yy-17,37,31,PALE,TEAL)
        elif i==1:
            for row in range(2):
                for col in range(2):d.tree(x+65+col*90,155+row*90,1.05)
        elif i==2:
            for j,height in enumerate([45,75,120,145,100,60]):
                d.rect(x+25+j*29,300-height,22,height,TEAL if j>2 else '#aab5bb','none')
            d.line(x+106,125,x+106,310,CORAL,2,dash='5 5')
        elif i==3:
            d.path([(x+20,235),(x+60,232),(x+85,207),(x+110,135),(x+145,121),(x+195,116)],TEAL,4)
            for j in range(15):
                d.rect(x+40+(j%5)*29,255+(j//5)*20,27,18,['#4f7b8d','#739a8a','#c5b672'][j%3],'none')
        else:
            for j in range(3):
                d.rect(x+43+j*15,139-j*15,115,157,'white',TEAL,r=5)
            d.text(x+131,203,'CSV',26,TEAL,700,anchor='middle')
            d.text(x+131,246,'TIF',26,TEAL,700,anchor='middle')
        if i<4:d.line(x+217,210,x+247,210,TEAL,3,arrow=True)
    for i,caption in enumerate(['IDs + climate + SNPs','One SNP at a time','OOB + importance','Curves + biplots','Tables + rasters']):
        d.text(129+i*261,389,caption,21,MUTED,anchor='middle')
    d.save()


if __name__ == '__main__':
    for build in [response,dosage,filtering,forests,oob,r2,permutation,correlation,
                  allocation,splits,transform,extrapolation,arrows,inference,workflow]:
        build()
    print('Built 15 schematic SVG figures.')
