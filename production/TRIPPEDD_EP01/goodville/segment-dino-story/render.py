"""Render the Goodville segment from timeline.json + layers/ (no regeneration; edit the JSON).
python3 render.py [--frames 0,250,...]  -> out/segment.mp4 (+ proof stills)"""
import json,os,sys,subprocess,wave,numpy as np
from PIL import Image,ImageDraw,ImageFont
D=os.path.dirname(os.path.abspath(__file__));T=json.load(open(f'{D}/timeline.json'))
W,H,FPS,N=T['width'],T['height'],T['fps'],T['duration_frames'];os.makedirs(f'{D}/out/frames',exist_ok=True)
cache={}
def L(p):
    if p not in cache: cache[p]=Image.open(f'{D}/{p}').convert('RGBA')
    return cache[p]
def inr(fr,f):
    rs=fr if isinstance(fr[0],list) else [fr]
    return any(a<=f<=b for a,b in rs)
def key(d,f):
    ks=sorted((int(k),v) for k,v in d.items())
    if f<=ks[0][0]: return ks[0][1]
    for (k0,v0),(k1,v1) in zip(ks,ks[1:]):
        if f<k1: return v0          # stepped (held) keys: cutout grammar, no tweening
    return ks[-1][1]
# voice envelope for the head wobble
au={a['id']:a for a in T['tracks']['audio']}
v=au['voice_dangly'];w=wave.open(f"{D}/{v['src']}");sr=w.getframerate();ch=w.getnchannels();sw=w.getsampwidth()
x=np.frombuffer(w.readframes(w.getnframes()),{2:np.int16,4:np.int32}[sw]).astype(float);x=x.reshape(-1,ch).mean(1)
env=[];spf=sr//FPS
for f in range(N):
    i=int((f/FPS-v['start_s'])*sr);seg=x[max(0,i):max(0,i)+spf] if i>=0 else np.zeros(1)
    env.append(np.sqrt((seg**2).mean()) if len(seg) else 0)
env=np.array(env);env=env/(env.max() or 1)
def place(c,im,x,y,scale=1,rot=0,pivot=None):
    if scale!=1: im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.LANCZOS)
    if rot:
        if pivot=='right_end':
            big=Image.new('RGBA',(im.width*2,im.height*2));big.alpha_composite(im,(0,im.height//2))
            im=big.rotate(rot,resample=Image.BICUBIC,center=(im.width,im.height));x-=im.width//2;y-=im.height//4
        else: im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    c.alpha_composite(im,(int(x),int(y))) if 0<=x and 0<=y and x+im.width<=W and y+im.height<=H else c.paste(im,(int(x),int(y)),im)
def frame(f):
    c=Image.new('RGBA',(W,H),(135,206,235,255))
    for t in T['tracks']['video']:
        if not inr(t['frames'],f): continue
        if t.get('type')=='text':
            d=ImageDraw.Draw(c);c.paste((20,20,20,255),(0,0,W,H))
            try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',90);F2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',40)
            except: F=F2=ImageFont.load_default()
            d.text((W//2,300),t['lines'][0],font=F,fill='white',anchor='mm');d.text((W//2,420),t['lines'][1],font=F2,fill=(255,220,0),anchor='mm');continue
        im=L(t['src'])
        if t.get('flip'): im=im.transpose(Image.FLIP_LEFT_RIGHT)
        if 'stretch' in t: im=im.resize(tuple(t['stretch']))
        if t.get('fit')=='cover': im=im.resize((W,H))
        if 'head_patch_from' in t:
            im=im.copy();hp=L(t['head_patch_from']).crop(t['head_patch_box']);im.alpha_composite(hp,tuple(t['head_patch_box'][:2]))
        x,y,s,r=t.get('x',0),t.get('y',0),t.get('scale',1),0
        if 'push_in' in t:
            a,b=t['push_in'];fr=t['frames'];s*=a+(b-a)*((f-fr[0])//12*12)/(fr[1]-fr[0])   # stepped push-in
        if t.get('wobble_on'):
            r=t['wobble_deg']*env[f]*(1 if (f//3)%2 else -1); y-=int(10*env[f])
        if 'rot_keys' in t: r=key(t['rot_keys'],f); x+=key(t['lunge_dx'],f)
        if 'hit_at' in t and f>=t['hit_at']: x+=t['knockback_dx'];r=t['knockback_rot']
        if s!=1 and 'push_in' in t: x-= (im.width*s-im.width*t['scale'])/2
        place(c,im,x-(im.width*s/2 if t['id']=='dangly_head' else 0),y-(im.height*s/2 if t['id']=='dangly_head' else 0),s,r,t.get('pivot'))
    return c.convert('RGB')
only=[int(a) for a in sys.argv[sys.argv.index('--frames')+1].split(',')] if '--frames' in sys.argv else None
for f in (only or range(N)): frame(f).save(f'{D}/out/frames/f{f:04d}.png')
if only: sys.exit()
# audio mix: voice + synthesized whacks
mix=np.zeros(int(N/FPS*sr))
vi=int(v['start_s']*sr);seg=x[:len(mix)-vi];mix[vi:vi+len(seg)]+=seg/ (np.abs(x).max() or 1)*0.9
for a in T['tracks']['audio']:
    if a.get('synth')=='whack':
        n=int(0.12*sr);tt=np.arange(n)/sr;wv=(np.random.RandomState(1).randn(n)*0.5+np.sin(2*np.pi*90*tt))*np.exp(-tt*35)*0.8
        i=int(a['start_s']*sr);mix[i:i+n]+=wv[:len(mix)-i]
mix=np.clip(mix,-1,1);ww=wave.open(f'{D}/out/mix.wav','wb');ww.setnchannels(1);ww.setsampwidth(2);ww.setframerate(sr);ww.writeframes((mix*32767).astype(np.int16).tobytes());ww.close()
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{D}/out/frames/f%04d.png','-i',f'{D}/out/mix.wav','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-shortest',f'{D}/out/segment.mp4'],check=True)
print('ok',f'{D}/out/segment.mp4')
