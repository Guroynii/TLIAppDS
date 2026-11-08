import numpy as np, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
D='/home/user/TLIAppDS/back-in-time/ep01/'; M=D+'assets/meam/'
W,H,FPS=1920,1080,25; k=W/1670
O=np.asarray(Image.open(M+'SRC_meam_car.webp').convert('RGB').resize((W,H),Image.LANCZOS),np.float32)
C=Image.open(M+'CLEAN_meam_car_higgsfield.png').convert('RGB').resize((W,H),Image.LANCZOS).filter(ImageFilter.GaussianBlur(5))
C=np.asarray(C,np.float32)
def P(v): return int(round(v*k))
box=np.zeros((H,W),bool); box[P(160):P(565),P(105):P(875)]=True
lum=O.mean(2); r,g,b=O[...,0],O[...,1],O[...,2]
txt=box&(((lum>175)&(np.abs(r-b)<60))|((r>200)&(g>80)&(g<190)&(b<90)))
tm=Image.fromarray((txt*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(43)).filter(ImageFilter.GaussianBlur(12))
tm=np.asarray(tm,np.float32)[...,None]/255
# match clean plate brightness to original surroundings inside box
ring=(np.asarray(Image.fromarray((txt*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(81)),np.float32)>0)&(tm[...,0]<0.02)&box
gain=O[ring].mean(0)/np.maximum(C[ring].mean(0),1)
Cg=np.clip(C*gain,0,255)
letters=np.asarray(Image.fromarray((txt*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)),np.float32)>0
valid=(tm[...,0]>0.2)&(~letters)
ratio=np.where(valid[...,None],O/np.maximum(Cg,8),0); wv=valid.astype(np.float32)
def blur(a,s): return np.asarray(Image.fromarray(a.astype(np.float32)).filter(ImageFilter.GaussianBlur(s)) if a.ndim==2 else None)
num=np.stack([np.asarray(Image.fromarray((ratio[...,c]*wv).astype(np.float32),'F').resize((W//48,H//48),Image.BOX).resize((W,H),Image.BICUBIC)) for c in range(3)],-1)
den=np.asarray(Image.fromarray(wv,'F').resize((W//48,H//48),Image.BOX).resize((W,H),Image.BICUBIC))[...,None]
R=np.clip(np.where(den>0.02,num/np.maximum(den,1e-3),1),0.45,1.0)
PLATE=O*(1-tm)+np.clip(Cg*R,0,255)*tm
Image.fromarray(PLATE.astype(np.uint8)).save(M+'PLATE_meam_car_no-text_1920x1080.png')
LINES=[('l1',(125,170,690,245)),('ul',(250,236,625,266)),('l2',(118,266,805,362)),('l3',(110,360,868,458)),('l4',(115,455,632,560))]
T=dict(l1=(0.30,0.90),ul=(0.85,1.30),l2=(1.30,1.90),l3=(2.00,2.70),l4=(2.80,3.30),dur=7.0)
if os.environ.get('MEAM_TIMING'): exec(open(os.environ['MEAM_TIMING']).read())
X=np.arange(W,dtype=np.float32)
def lm(x0,y0,x1,y1):
    m=np.zeros((H,W),np.float32); m[P(y0):P(y1),P(x0)-10:P(x1)+10]=1
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)),np.float32)/255
MK={n:lm(*b) for n,b in LINES}
def ss(u): u=min(max(u,0),1); return u*u*(3-2*u)
def render(t):
    w=np.zeros((H,W),np.float32)
    for n,(x0,y0,x1,y1) in LINES:
        a,b=T[n]; u=ss((t-a)/(b-a))
        if u<=0: continue
        fr=P(x0)-40+(P(x1)-P(x0)+80)*u
        wipe=np.clip((fr-X)/50,0,1)[None,:]
        w=np.maximum(w,MK[n]*wipe*min(1,(t-a)/0.25))
    img=PLATE*(1-w[...,None]*tm)+O*(w[...,None]*tm)
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    s=1+0.03*t/T['dur']; w2,h2=W/s,H/s; x0,y0=(W-w2)*0.62,(H-h2)/2
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
if __name__=='__main__':
    if 'check' in sys.argv:
        for t in (0.0,0.6,1.6,2.4,4.0): render(t).resize((960,540)).save(f'meam_{t}.jpg',quality=85)
    else:
        out=D+'renders/S_MEAM_title-reveal_1920x1080.mp4'
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        N=int(round(T['dur']*FPS))
        for i in range(N): p.stdin.write(np.asarray(render(i/FPS)).tobytes())
        p.stdin.close(); p.wait(); print('frames',N)
