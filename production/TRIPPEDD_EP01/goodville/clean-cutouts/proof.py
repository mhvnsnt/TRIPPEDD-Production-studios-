import json,sys
from PIL import Image,ImageDraw;import numpy as np
r=json.load(open('maskcut-report.json'))
r=[x for x in r if not any(k in x['out'] for k in ['bldg_','sky_clean','street_clean','dino_punch_final'])]
json.dump(r,open('maskcut-report.json','w'),indent=1)
R='/workspace/TRIPPEDD-Production-studios-/'
fs=sys.argv[2:]
def chk(w,h):
  a=((np.indices((h,w))//12).sum(0)%2)*70+185;return Image.fromarray(np.dstack([a,a,a,np.full_like(a,255)]).astype(np.uint8))
C=260;s=chk(2*C+30,len(fs)*C+16)
for i,f in enumerate(fs):
  for j,p in enumerate([R+f,f]):
    im=Image.open(p).convert('RGBA');im.thumbnail((C-10,C-10));s.alpha_composite(im,(j*(C+30),16+i*C))
d=ImageDraw.Draw(s);d.rectangle((0,0,2*C+30,15),fill='black');d.text((5,2),'BEFORE (original)',fill='red');d.text((C+35,2),'AFTER (mask-cut, checkerboard)',fill='lime')
s.save(sys.argv[1])
