import numpy as np, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
D='/home/user/TLIAppDS/back-in-time/ep01/'; M=D+'assets/music-evolution/'
W,H,FPS=1920,1080,25; k=W/1672
src=[np.asarray(Image.open(M+f'SRC_state{i}.webp').convert('RGB').resize((W,H),Image.LANCZOS),dtype=np.float32) for i in (1,2,3)]
S1,S2,S3=src
def P(v): return int(round(v*k))
def rmask(x0,y0,x1,y1,f):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rectangle([P(x0),P(y0),P(x1),P(y1)],fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(f)),np.float32)[...,None]/255
# ---- band mask (timeline area only) ----
B=rmask(410,340,1612,746,10)
def clamp(x): return np.clip(x,0,1)
def eo(x): x=float(min(max(x,0),1)); return 1-(1-x)**3
T=dict(spark=[(0.35,425),(1.55,830)],
       k2=[(2.75,830),(3.25,1060),(4.35,1250),(4.70,1395)],
       k3=[(6.30,1255),(6.85,1470),(7.00,1612)],dur=11.30)
if os.environ.get('ME_TIMING'): exec(open(os.environ['ME_TIMING']).read())
X=(np.arange(W,dtype=np.float32)/k)[None,:,None]
def interp(t,kf):
    if t<=kf[0][0]: return None
    for (t0,x0),(t1,x1) in zip(kf,kf[1:]):
        if t<=t1:
            u=(t-t0)/(t1-t0); u=u*u*(3-2*u); return x0+(x1-x0)*u
    return kf[-1][1]+1e4
def trans(A,Bimg,t,kf,soft=45):
    fr=interp(t,kf)
    if fr is None: return A
    w=clamp((fr-X)/soft); xa=kf[0][1]
    w=np.where(X<xa,eo((t-kf[0][0])/0.45),w)
    return A*(1-w)+Bimg*w
def band(t):
    img=trans(S1,S2,t,T['k2'])
    if t>T['k3'][0][0]: img=trans(img,S3,t,T['k3'])
    return img
def front(t):
    for kf,xmax in ((T['spark'],830),(T['k2'],1250),(T['k3'],1470)):
        fr=interp(t,kf)
        if fr is not None and fr<=xmax+5: return min(fr,xmax),1.0
        if fr is not None and fr<xmax+200 and kf is not T['spark']: pass
    return None,0
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
lyy,lxx=np.mgrid[0:H:4,0:W:4].astype(np.float32)
def render(t):
    img=S1*(1-B)+band(t)*B
    fr,a=front(t)
    if fr is not None:
        g=np.exp(-(((xx-fr*k)/28)**2+((yy-593*k)/13)**2))[...,None]
        img=img+g*np.array([255,200,140],np.float32)*0.6*a
    cx=W*(0.70+0.08*t/T['dur'])
    g=np.exp(-(((lxx-cx)/520)**2+((lyy-H*0.25)/380)**2)).astype(np.float32)
    g=np.asarray(Image.fromarray((g*255).astype(np.uint8)).resize((W,H),Image.BILINEAR),np.float32)[...,None]/255
    img=img+g*np.array([36,16,4],np.float32)*(0.6+0.4*np.sin(t*0.7))
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    s=1+0.025*t/T['dur']; w2,h2=W/s,H/s; x0,y0=(W-w2)/2,(H-h2)/2
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='check':
        for t in (0.2,1.0,3.3,4.6,6.6,9.0): render(t).save(f'me2_{t}.png')
    else:
        out=sys.argv[1] if len(sys.argv)>1 else D+'renders/S15_music-evolution_1920x1080.mp4'
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        N=int(round(T['dur']*FPS))
        for i in range(N): p.stdin.write(np.asarray(render(i/FPS)).tobytes())
        p.stdin.close(); p.wait(); print('frames',N)
