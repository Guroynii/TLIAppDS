import subprocess, numpy as np
from PIL import Image, ImageFilter
W,H,FPS=1920,1080,25; E='/home/user/TLIAppDS/back-in-time/ep01/'; A=E+'assets/shot06-08/'
L=lambda n: Image.open(A+n+'.png').convert('RGBA')
dim,title,qp,q1,q2=L('S07_T0_dim'),L('S07_T1_title'),L('S08_Q0_panel'),L('S08_Q1_line1'),L('S08_Q2_line2-3')
def clamp(x): return max(0.,min(1.,x))
def ramp(t,t0,d): return clamp((t-t0)/d)
def eo(x): return 1-(1-clamp(x))**3
def wa(im,a):
    if a>=0.999: return im
    r,g,b,al=im.split(); return Image.merge('RGBA',(r,g,b,al.point(lambda v:int(v*a))))
def zoom(im,s):
    w,h=W/s,H/s; x0,y0=(W-w)/2,(H-h)/2; return im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w,y0+h))
vid=subprocess.Popen(['ffmpeg','-v','error','-i',E+'renders/S06-08_host_1920x1080.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
out=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','v0608.mp4'],stdin=subprocess.PIPE)
rng=np.random.default_rng(5); gr=[rng.normal(0,5,(H,W,1)).astype(np.int16) for _ in range(4)]
i=0
while True:
    b=vid.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    t=i/FPS; im=zoom(Image.frombytes('RGB',(W,H),b).convert('RGBA'),1+0.03*t/13.12)
    k=ramp(t,3.30,0.24)*(1-ramp(t,5.61,0.24))
    if k>0:
        im=Image.blend(im,im.filter(ImageFilter.GaussianBlur(18)),k); im=Image.alpha_composite(im,wa(dim,k))
        a=eo(ramp(t,3.42,0.32))*(1-ramp(t,5.55,0.30))
        if a>0: im=Image.alpha_composite(im,wa(title,a))
    fo=1-ramp(t,12.85,0.27)
    for lay,t0 in ((qp,7.10),(q1,7.22),(q2,9.72)):
        a=eo(ramp(t,t0,0.32))*fo
        if a>0: im=Image.alpha_composite(im,wa(lay,a))
    arr=np.asarray(im.convert('RGB'),np.int16)+gr[i%4]
    out.stdin.write(np.clip(arr,0,255).astype(np.uint8).tobytes()); i+=1
out.stdin.close(); out.wait(); print('frames',i)
