import numpy as np, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
D='/home/user/TLIAppDS/back-in-time/ep01/'; M=D+'assets/reminiscence-bump/'
W,H,FPS=1920,1080,25; k=W/1672
def load(n): return np.asarray(Image.open(M+n).convert('RGB').resize((W,H),Image.LANCZOS),np.float32)
F=load('SRC_final_highlight.webp'); B0=load('SRC_base_graph.webp')
def P(v): return int(round(v*k))
def rmask(x0,y0,x1,y1,f=4):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rectangle([P(x0),P(y0),P(x1),P(y1)],fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(f)),np.float32)[...,None]/255
X=(np.arange(W,dtype=np.float32)/k)[None,:,None]
PLOT=rmask(603,348,1598,664,2)
ghost=np.asarray(Image.fromarray(B0.astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)),np.float32)*0.30
VR=np.clip(((np.arange(H,dtype=np.float32)/k)-440)/60,0,1)[:,None,None]
R={'band':rmask(758,352,1036,667,2)*VR,'c10':rmask(722,670,815,735,3),'c30':rmask(980,670,1075,735,3),
   'label':rmask(735,290,1060,452,3),'call':rmask(1036,255,1580,600,3)}
# ---- timing (seconds from clip start); replace with real VO timings when available ----
T=dict(draw=(0.4,2.6), c10=10.6, c30=11.9, band=(10.6,12.2), label=12.5, call=14.4, dur=27.0)
if os.environ.get('RB_TIMING'): exec(open(os.environ['RB_TIMING']).read())
def ss(u): u=min(max(u,0),1); return u*u*(3-2*u)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def render(t):
    img=B0.copy()
    a,b=T['draw']; fr=603+(1598-603)*ss((t-a)/(b-a))
    rev=np.clip((fr-X)/25,0,1)
    img=img*(1-PLOT)+(ghost*(1-rev)+img*rev)*PLOT
    if a<t<b+0.1:
        g=np.exp(-((xx-fr*k)/10)**2)*(yy>P(348))*(yy<P(664))
        img=img+g[...,None]*np.array([60,220,230],np.float32)*0.35
    # highlight build
    b0,b1=T['band']; front=758+(1036-758)*ss((t-b0)/(b1-b0)) if t>b0 else -1
    wb=np.clip((front-X)/20,0,1)*R['band']
    img=img*(1-wb)+F*wb
    for key,t0,d in (('c10',T['c10'],0.35),('c30',T['c30'],0.35),('label',T['label'],0.5),('call',T['call'],0.6)):
        w=ss((t-t0)/d)*R[key]
        if w.max()>0: img=img*(1-w)+F*w
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    s=1+0.03*t/T['dur']; w2,h2=W/s,H/s; x0,y0=(W-w2)/2,(H-h2)/2
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
if __name__=='__main__':
    if 'check' in sys.argv:
        for t in (1.5,5.0,11.2,13.5,20.0): render(t).save(f'rb_{t}.png')
    else:
        out=sys.argv[1] if len(sys.argv)>1 else D+'renders/S27_reminiscence-bump_1920x1080.mp4'
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        N=int(round(T['dur']*FPS))
        for i in range(N): p.stdin.write(np.asarray(render(i/FPS)).tobytes())
        p.stdin.close(); p.wait(); print('frames',N)
