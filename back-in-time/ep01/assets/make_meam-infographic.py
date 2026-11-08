import numpy as np, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
D='/home/user/TLIAppDS/back-in-time/ep01/'; M=D+'assets/meam-info/'
W,H,FPS=1920,1080,25; k=W/1671
O=np.asarray(Image.open(M+'SRC_meam_info.webp').convert('RGB').resize((W,H),Image.LANCZOS),np.float32)
Pl=np.asarray(Image.open(M+'CLEAN_meam_info_higgsfield.png').convert('RGB').resize((W,H),Image.LANCZOS),np.float32)
def P(v): return int(round(v*k))
def rect(x0,y0,x1,y1,f=8,r=0):
    m=Image.new('L',(W,H),0); d=ImageDraw.Draw(m)
    if r: d.rounded_rectangle([P(x0),P(y0),P(x1),P(y1)],radius=P(r),fill=255)
    else: d.rectangle([P(x0),P(y0),P(x1),P(y1)],fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(f)),np.float32)/255
PR=rect(1108,228,1602,634,4,r=40); PB=rect(236,676,1464,864,4,r=60)
ELR=[(555,58,972,145),(546,118,1058,212),(1048,92,1398,172),(755,168,1250,228),(560,298,668,474),(478,330,872,442),(712,240,1045,484),(510,460,730,646),(716,478,888,644),(862,466,1070,660)]
GM=np.maximum.reduce([rect(x0-20,y0-20,x1+20,y1+20,30) for x0,y0,x1,y1 in ELR]+[rect(1080,200,1630,662,30,r=56),rect(210,650,1490,890,30,r=76)])
ring=(GM<0.02)&(rect(1080,650,1670,940,1)>0.5)
Pbg=np.clip(Pl+(O[ring].mean(0)-Pl[ring].mean(0)),0,255)
patch=rect(255,598,470,668,1)>0.5
mO,sO=O[patch].mean(0),O[patch].std(0)+1; mP,sP=Pl[patch].mean(0),Pl[patch].std(0)+1
Pman=np.clip((Pl-mP)/sP*sO+mO,0,255)
manm=rect(0,560,540,941,30)[...,None]
Pl=Pman*manm+Pbg*(1-manm)
BASE=O*(1-GM[...,None])+Pl*GM[...,None]
diff=np.abs(O-BASE).max(2)
content=np.asarray(Image.fromarray(np.clip((diff-10)/35*255,0,255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3)),np.float32)/255
def glass(pm):
    inside=(pm>0.99)&(O.mean(2)<80)
    r=np.median(O[inside]/np.maximum(Pl[inside],1),axis=0); return np.clip(Pl*r,0,255)
GR_=glass(rect(1108,228,1602,634,1,r=40)); GB_=glass(rect(236,676,1464,864,1,r=60))
E={ # name: (rect, reveal type)
 't1':(555,58,972,145),'t2':(546,118,1058,212),'t3':(1048,92,1398,172),'brush':(755,168,1250,228),
 'notes':(560,298,668,474),'wave':(478,330,872,442),'brain':(712,240,1045,484),
 'p1':(510,460,730,646),'p2':(716,478,888,644),'p3':(862,466,1070,660),
 'rTop':(1150,248,1575,338),'rSong':(1150,336,1435,402),'rIcon':(1138,425,1240,535),'rTxt':(1243,418,1585,525),'rTxt2':(1243,523,1585,610),
 'bLeft':(285,695,795,850),'eHappy':(822,692,992,848),'eWarm':(1032,692,1212,848),'eSad':(1248,692,1418,848)}
MK={n:rect(*b,f=6) for n,b in E.items()}
T={'t1':(2.10,2.95),'t2':(3.40,4.50),'t3':(4.55,5.20),'brush':(5.00,5.55),
   'panelR':5.95,'rTop':6.26,'rSong':9.42,'notes':9.42,'wave':(9.42,10.40),'brain':10.00,
   'rIcon':11.14,'rTxt':11.14,'p1':13.90,'p2':14.30,'p3':14.70,'rTxt2':17.55,'pulse':18.02,
   'panelB':20.26,'bLeft':20.26,'eWarm':28.90,'eSad':33.26,'eHappy':35.44,'dim':(38.40,40.70),'dur':47.30}
if os.environ.get('MI_TIMING'): exec(open(os.environ['MI_TIMING']).read())
X=(np.arange(W,dtype=np.float32)/k)[None,:]
def ss(u): u=min(max(u,0),1); return u*u*(3-2*u)
def fade(t,t0,d=0.35): return ss((t-t0)/d)
def wipe(t,a,b,x0,x1,soft=40):
    if t<=a: return 0
    fr=x0-20+(x1-x0+40)*ss((t-a)/(b-a)); return np.clip((fr-X)/soft*k,0,1)
def render(t):
    img=BASE.copy()
    def put(src,alpha):
        nonlocal img
        if np.isscalar(alpha) and alpha<=0: return
        a=alpha[...,None] if not np.isscalar(alpha) else alpha
        img=img*(1-a)+src*a
    # panels (empty glass + border) first
    for pm,t0,box,G in ((PR,T['panelR'],(1108,228,1602,634),GR_),(PB,T['panelB'],(236,676,1464,864),GB_)):
        a=fade(t,t0,0.45)
        if a>0:
            inner=rect(box[0]+14,box[1]+14,box[2]-14,box[3]-14,3,r=30)
            put(G*inner[...,None]+O*(1-inner[...,None]),pm*a)
    for n in ('t1','t2','t3','brush'):
        a,b=T[n]; x0,_,x1,_=E[n]; w=wipe(t,a,b,x0,x1)
        if not np.isscalar(w): put(O,MK[n]*content*w*min(1,(t-a)/0.2))
    a,b=T['wave']; w=wipe(t,a,b,478,872)
    if not np.isscalar(w): put(O,MK['wave']*content*w)
    for n in ('notes','brain','p1','p2','p3'):
        put(O,MK[n]*content*fade(t,T[n],0.4))
    for n in ('rTop','rSong','rIcon','rTxt','rTxt2'):
        put(O,MK[n]*PR*fade(t,T[n],0.4))
    put(O,MK['bLeft']*PB*fade(t,T['bLeft'],0.45))
    dim=1-0.6*(ss((t-T['dim'][0])/0.5)-ss((t-T['dim'][1])/0.5))
    for n in ('eHappy','eWarm','eSad'):
        put(O,MK[n]*PB*fade(t,T[n],0.4)*dim)
    # emotional pulse on brain glow
    pu=np.exp(-((t-T['pulse']-0.4)/0.5)**2)
    if pu>0.01: img=img+(MK['brain']*content)[...,None]*np.clip(O-90,0,255)*0.35*pu
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    s=1+0.03*t/T['dur']; w2,h2=W/s,H/s; x0,y0=(W-w2)*0.55,(H-h2)*0.45
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
if __name__=='__main__':
    if 'check' in sys.argv:
        for t in (1.0,4.0,7.0,10.2,15.5,22.0,30.0,39.5,46.0): render(t).resize((640,360)).save(f'mi_{t}.jpg',quality=85)
    else:
        out=D+'renders/S_MEAM_infographic_1920x1080.mp4'
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        N=int(round(T['dur']*FPS))
        for i in range(N): p.stdin.write(np.asarray(render(i/FPS)).tobytes())
        p.stdin.close(); p.wait(); print('frames',N)
