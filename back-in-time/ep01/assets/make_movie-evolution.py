import numpy as np, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
D='/home/user/TLIAppDS/back-in-time/ep01/'
W,H,FPS=1920,1080,25; k=W/1670
SAFE='safe' in sys.argv
base=Image.open(D+'assets/movie-evolution/SRC_movie-evolution.webp').convert('RGB').resize((W,H),Image.LANCZOS)
def P(v): return int(round(v*k))
if SAFE:   # soften real posters / platform logos
    for box in [(98,335,252,578),(262,358,408,578),(1248,355,1598,528)]:
        b=tuple(P(v) for v in box); reg=base.crop(b).filter(ImageFilter.GaussianBlur(14))
        m=Image.new('L',reg.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,reg.size[0]-1,reg.size[1]-1],radius=12,fill=255)
        base.paste(reg,b[:2],m.filter(ImageFilter.GaussianBlur(4)))
B=np.asarray(base,np.float32)
X=(np.arange(W,dtype=np.float32)/k)
Y=(np.arange(H,dtype=np.float32)/k)
def band(x0,x1,f=70): return np.clip(np.minimum((X-x0+f)/(2*f),(x1-X+f)/(2*f)),0,1)
COLS={'cin':band(-200,525),'vhs':band(545,850),'dvd':band(895,1205),'tv':band(1225,1900)}
title=np.clip((262-Y)/40,0,1)[:,None]          # always-bright title zone
LY=632; NODES={'cin':330,'vhs':690,'dvd':1063,'tv':1435}
T=dict(cin=0.30,vhs=1.08,dvd=2.78,tv=5.52,release=(6.4,7.4),dur=10.25,spark=[(0.0,180),(0.30,330),(1.08,690),(2.78,1063),(5.52,1435)])
if os.environ.get('MV_TIMING'): exec(open(os.environ['MV_TIMING']).read())
def ss(u): u=min(max(u,0),1); return u*u*(3-2*u)
def act(t):
    order=['cin','vhs','dvd','tv']; w={}
    for i,n in enumerate(order):
        on=ss((t-T[n]+0.15)/0.4)
        off=ss((t-T[order[i+1]]+0.15)/0.4) if i<3 else 0
        w[n]=on*(1-off)
    return w
def sparkx(t):
    kf=T['spark']
    for (t0,x0),(t1,x1) in zip(kf,kf[1:]):
        if t0<=t<=t1:
            # travel during last 0.6 s before reaching next node
            u=ss((t-(t1-0.6))/0.6) if t1-t0>0.6 else ss((t-t0)/(t1-t0)); return x0+(x1-x0)*u, True
    return kf[-1][1], False
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
ORG=np.array([255,140,50],np.float32)
def glow_line(x_to):
    xe=x_to*k; core=np.exp(-((yy[:,:1]-LY*k)/3.2)**2); halo=np.exp(-((yy[:,:1]-LY*k)/14)**2)
    xm=np.clip((xe-np.arange(W,dtype=np.float32)[None,:])/30,0,1)*(np.arange(W)[None,:]>=P(180))
    return (core*0.9+halo*0.35)*xm
def node_glow(xn,a):
    return a*np.exp(-(((xx-xn*k)/34)**2+((yy-LY*k)/34)**2))
def render(t):
    w=act(t); rel=ss((t-T['release'][0])/(T['release'][1]-T['release'][0]))
    spot=np.zeros(W,np.float32)
    for n,c in COLS.items(): spot=np.maximum(spot,c*w[n])
    light=0.52+0.48*np.maximum(spot[None,:],title)
    light=light*(1-rel)+1.0*rel
    img=B*light[...,None]
    sx,moving=sparkx(t)
    img=img+glow_line(sx)[...,None]*ORG*0.55
    g=np.zeros((H,W),np.float32)
    for n,xn in NODES.items():
        if t>=T[n]-0.05: g+=node_glow(xn,ss((t-T[n]+0.05)/0.3)*(0.9 if n!='tv' else 0.5))
    if moving: g+=np.exp(-(((xx-sx*k)/24)**2+((yy-LY*k)/12)**2))*1.2
    img=img+g[...,None]*ORG*0.6
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    s=1+0.025*t/T['dur']; w2,h2=W/s,H/s; x0,y0=(W-w2)/2,(H-h2)/2
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
if __name__=='__main__':
    if 'check' in sys.argv:
        for t in (0.6,1.6,3.5,6.0,9.0): render(t).save(f'mv_{t}.png')
    else:
        out=D+('renders/S20_movie-evolution_SAFE_1920x1080.mp4' if SAFE else 'renders/S20_movie-evolution_1920x1080.mp4')
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        N=int(round(T['dur']*FPS))
        for i in range(N): p.stdin.write(np.asarray(render(i/FPS)).tobytes())
        p.stdin.close(); p.wait(); print('frames',N,out)
