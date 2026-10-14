"""Mask-cut every character piece: rembg (isnet-anime) subject mask intersected with
the existing alpha; flags rectangular-crop residue; writes clean RGBA + report.
Usage: maskcut.py OUT_DIR SRC_DIR [SRC_DIR...]"""
import sys,os,json,glob,numpy as np
from PIL import Image,ImageFilter
from rembg import remove,new_session
S=new_session("u2net")
out=sys.argv[1];rep=[]
def border_opaque(a):
    b=np.concatenate([a[:2].ravel(),a[-2:].ravel(),a[:,:2].ravel(),a[:,-2:].ravel()]);return float((b>200).mean())
for d in sys.argv[2:]:
  for f in sorted(glob.glob(d+'/*.png')):
    im=Image.open(f).convert('RGBA');A=np.array(im)
    if A.shape[0]*A.shape[1]>1.5e6 or 'sheet' in f: continue
    a0=A[...,3];bo=border_opaque(a0)
    sc=max(1,400//max(im.size));big=im.resize((im.width*sc,im.height*sc));pad=40
    bg=Image.new('RGB',(big.width+2*pad,big.height+2*pad),(255,255,255));bg.paste(big,(pad,pad),big)
    m=np.array(remove(bg,session=S,only_mask=True).crop((pad,pad,pad+big.width,pad+big.height)).resize(im.size))
    m=np.clip((m.astype(float)-90)*255/80,0,255)  # ghost/smear kill: flat-art matte
    new=np.minimum(a0,m).astype(np.uint8)
    # 1px edge erode+smooth to kill halos
    na=np.array(Image.fromarray(new).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6)))
    na=np.where(new<8,0,na)
    na=np.clip((na.astype(float)-110)*255/100,0,255).astype(np.uint8)  # kill semi-transparent ghosts/smears
    from scipy import ndimage
    lab,n=ndimage.label(na>40)
    if n>1:
        sz=ndimage.sum(np.ones_like(lab),lab,range(1,n+1));big=sz.max()
        keepl=[i+1 for i,v in enumerate(sz) if v>=0.04*big]  # drop crumbs and stray fragments
        na=np.where(np.isin(lab,keepl),na,0).astype(np.uint8)
    keep=(na>128).sum()/max(1,(a0>128).sum())
    st='cleaned' if keep>=0.55 else 'REVIEW_kept_original'
    if st!='cleaned': na=a0
    A2=A.copy();A2[...,3]=na
    rel=os.path.relpath(f,os.path.commonpath(sys.argv[2:]) if len(sys.argv)>3 else os.path.dirname(d))
    o=os.path.join(out,rel);os.makedirs(os.path.dirname(o),exist_ok=True);Image.fromarray(A2).save(o,optimize=True)
    rep.append(dict(src=f.split('TRIPPEDD-Production-studios-/')[-1],out=rel,border_opaque_before=round(bo,3),border_opaque_after=round(border_opaque(na),3),area_kept=round(float(keep),3),status=st))
    print(rep[-1],flush=True)
json.dump(rep,open(os.path.join(out,'maskcut-report.json'),'w'),indent=1)
