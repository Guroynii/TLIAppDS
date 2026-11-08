import json, math, subprocess, numpy as np
from PIL import Image, ImageEnhance
E='/home/user/TLIAppDS/back-in-time/ep01/'; A=E+'assets/'
W,H,FPS=1920,1080,25
OFF=1.0                      # VO starts at program 1.0 s
END_VO=20.0
N=int((END_VO+OFF)*FPS)
def L(p): return Image.open(p).convert('RGBA')
frame=L(A+'series/PAST_film-frame-overlay_1920x1080.png')
def grade(im): return ImageEnhance.Color(im).enhance(0.92)
S02=grade(L(E+'renders/S02_plate_1920x1080.png')); S03=grade(L(E+'renders/S03_plate_crop_1920x1080.png')); S04=grade(L(E+'renders/S04_plate_1920x1080.png'))
pl=json.load(open(A+'shot01-02/S01_label-placement.json'))
lab=[(L(A+'shot01-02/S01_label-1_wansao.png'),pl['S01_label-1_wansao.png']['center'],1.94),
     (L(A+'shot01-02/S01_label-2_bai2mong.png'),pl['S01_label-2_bai2mong.png']['center'],2.44)]
n=int(1200*0.66)
hh=L(A+'shot01-02/S02_clock-hand-hour_pivot-center.png').resize((n,n),Image.LANCZOS)
mh=L(A+'shot01-02/S02_clock-hand-minute_pivot-center.png').resize((n,n),Image.LANCZOS)
S3L={k:L(A+f'shot03-04/S03_{k}.png') for k in ['L0_scrim','L1_panel','L2_icon-phone','L3_strike','L4_text-no-mobile','L5_bubble','L6_send-failed']}
def clamp(x): return max(0.0,min(1.0,x))
def eo(x): x=clamp(x); return 1-(1-x)**3
def ramp(t,t0,dur): return clamp((t-t0)/dur)
def zoom(im,s):
    if abs(s-1)<1e-4: return im
    w,h=W/s,H/s; x0=(W-w)/2; y0=(H-h)/2
    return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w,y0+h))
def with_alpha(im,a):
    if a>=0.999: return im
    r,g,b,al=im.split(); return Image.merge('RGBA',(r,g,b,al.point(lambda v:int(v*a))))
# source video for shot 01 at 25 fps
vid=subprocess.Popen(['ffmpeg','-v','error','-i',E+'renders/S01_video_kling_locked.mp4','-vf','fps=25,scale=1920:1080','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
def nextvid():
    b=vid.stdout.read(W*H*3)
    return grade(Image.frombytes('RGB',(W,H),b).convert('RGBA')) if len(b)==W*H*3 else None
lastv=None
rng=np.random.default_rng(3); grains=[(rng.normal(0,9,(H,W,1))).astype(np.int16) for _ in range(6)]
out=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
     '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','video_only.mp4'],stdin=subprocess.PIPE)
def shot01(t,ft):   # t = VO time
    global lastv
    v=nextvid(); lastv=v if v is not None else lastv
    im=zoom(lastv,1+0.03*clamp(ft/6.4))
    for png,(cx,cy),t0 in lab:
        k=eo(ramp(t,t0,6/FPS))
        if k<=0: continue
        s=1.08-0.08*k; r=-3*(1-k)
        p=png.resize((int(png.width*s),int(png.height*s)),Image.BICUBIC).rotate(-r,resample=Image.BICUBIC,expand=True)
        p=with_alpha(p,clamp(ramp(t,t0,3/FPS)))
        im.alpha_composite(p,(int(cx-p.width/2),int(cy-p.height/2)))
    return im
def shot02(t):
    im=zoom(S02,1+0.04*ramp(t,5.40,4.55)).copy()
    k1=eo(ramp(t,5.55,0.55)); k2=eo(ramp(t,8.20,0.62))
    ha=60+7.5*k1+7.5*k2; ma=90*k1+90*k2
    for hand,ang in ((hh,ha),(mh,ma)):
        im.alpha_composite(hand.rotate(-ang,resample=Image.BICUBIC),(960-n//2,494-n//2))
    return im
def shot03(t):
    im=zoom(S03,1+0.03*ramp(t,9.95,6.25)).copy()
    out_a=1-ramp(t,15.80,0.40)
    def put(key,t0,extra=1.0,rise=True):
        k=eo(ramp(t,t0,8/FPS))
        if k<=0: return
        dy=int(12*(1-k)) if rise else 0
        lay=with_alpha(S3L[key],k*extra*out_a)
        im.alpha_composite(lay,(0,dy)) if dy==0 else im.alpha_composite(lay.crop((0,0,W,H-dy)),(0,dy))
    sc=ramp(t,9.95,12/FPS)*out_a
    if sc>0: im.alpha_composite(with_alpha(S3L['L0_scrim'],sc))
    put('L1_panel',10.00); put('L2_icon-phone',10.30); put('L4_text-no-mobile',11.20)
    w=ramp(t,11.46,6/FPS)
    if w>0:
        x1=int(1150-50+100*w); st=S3L['L3_strike'].crop((0,0,x1,H)); im.alpha_composite(with_alpha(st,out_a),(0,0))
    dim=1-0.45*ramp(t,14.80,6/FPS); put('L5_bubble',13.70,dim); put('L6_send-failed',14.80)
    return im
def shot04(t): return zoom(S04,1.06-0.06*ramp(t,16.20,3.8))
WHITE=Image.new('RGBA',(W,H),(255,243,224,255))
for i in range(N):
    pt=i/FPS; t=pt-OFF
    if t<5.40: im=shot01(t,pt)
    else:
        if lastv is not None or True:
            pass
        if t<9.95: im=shot02(t)
        elif t<15.96: im=shot03(t)
        elif t<16.44: im=Image.blend(shot03(t),shot04(t),(t-15.96)/0.48)
        else: im=shot04(t)
    im=Image.alpha_composite(im.convert('RGBA'),frame)
    if pt<0.5: im=Image.blend(Image.new('RGBA',(W,H),(0,0,0,255)),im,pt/0.5)
    if t>=19.22: im=Image.blend(im,WHITE,clamp((t-19.22)/0.48))
    a=np.asarray(im.convert('RGB'),dtype=np.int16)+grains[i%6]
    out.stdin.write(np.clip(a,0,255).astype(np.uint8).tobytes())
    if t>=5.40 and vid.poll() is None: pass
out.stdin.close(); out.wait(); vid.kill(); print('frames',N)
