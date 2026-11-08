import random, math, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
random.seed(7)
W,H=1920,1080
OUT='/home/user/TLIAppDS/back-in-time/ep01/assets/'
FD='fonts/'
# ---------- 1. Safe area guide ----------
g=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(g)
def dashed_rect(x0,y0,x1,y1,col,dash=18,gap=12,w=2):
    for (a,b,c,e) in [(x0,y0,x1,y0),(x0,y1,x1,y1),(x0,y0,x0,y1),(x1,y0,x1,y1)]:
        L=math.hypot(c-a,e-b); n=int(L//(dash+gap))+1
        for i in range(n):
            s=i*(dash+gap)/L; t=min((i*(dash+gap)+dash)/L,1)
            d.line([(a+(c-a)*s,b+(e-b)*s),(a+(c-a)*t,b+(e-b)*t)],fill=col,width=w)
dashed_rect(192,108,W-192,H-108,(224,122,58,200))            # 10% minimum
d.rectangle([230,130,W-230,H-130],outline=(201,164,92,255),width=3)  # 12% target
for x in (W/3,2*W/3): d.line([(x,130),(x,H-130)],fill=(237,230,216,70),width=1)
for y in (H/3,2*H/3): d.line([(230,y),(W-230,y)],fill=(237,230,216,70),width=1)
d.line([(W/2-20,H/2),(W/2+20,H/2)],fill=(237,230,216,160),width=2); d.line([(W/2,H/2-20),(W/2,H/2+20)],fill=(237,230,216,160),width=2)
d.line([(230,950),(900,950)],fill=(18,58,64,255),width=2)
f=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',20)
d.text((236,108),'GRAPHIC SAFE 12%  (230 / 130 px)',font=f,fill=(201,164,92,255))
d.text((198,86),'MIN 10%  (192 / 108 px)',font=f,fill=(224,122,58,220))
d.text((236,956),'LOWER-THIRD BASELINE  y=950',font=f,fill=(120,170,175,255))
g.save(OUT+'series/GUIDE_safe-area_1920x1080.png')

# ---------- 2. Past film frame overlay ----------
fr=Image.new('L',(W,H),0); fd=ImageDraw.Draw(fr)
fd.rounded_rectangle([34,30,W-34,H-30],radius=46,fill=255)
fr=fr.filter(ImageFilter.GaussianBlur(5))
alpha=ImageChops.invert(fr)
burn=Image.new('RGBA',(W,H),(28,18,10,255)); burn.putalpha(alpha)
# vignette
vig=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vig)
for i in range(60):
    a=int(110*(1-i/60)**2.2); m=i*6
    vd.rounded_rectangle([m,m*0.56,W-m,H-m*0.56],radius=80,outline=a,width=7)
vig=vig.filter(ImageFilter.GaussianBlur(30))
vigimg=Image.new('RGBA',(W,H),(20,12,6,0)); vigimg.putalpha(vig)
frame=Image.alpha_composite(vigimg,burn)
fd2=ImageDraw.Draw(frame)
# edge scratches & dust (inside border band only)
for _ in range(260):
    side=random.choice('tblr')
    if side in 'tb':
        x=random.uniform(40,W-40); y=random.uniform(30,70) if side=='t' else random.uniform(H-70,H-30)
    else:
        y=random.uniform(40,H-40); x=random.uniform(34,80) if side=='l' else random.uniform(W-80,W-34)
    r=random.uniform(0.6,2.4); c=random.choice([(240,226,200,170),(30,20,12,190)])
    fd2.ellipse([x-r,y-r,x+r,y+r],fill=c)
for _ in range(14):
    x=random.uniform(120,W-120); y=random.uniform(90,H-90); L=random.uniform(30,140); ang=random.uniform(-0.25,0.25)+math.pi/2
    fd2.line([(x,y),(x+L*math.cos(ang),y+L*math.sin(ang))],fill=(245,235,215,38),width=1)
# warm light leak (left edge)
leak=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(leak)
ld.ellipse([-260,180,180,900],fill=(224,122,58,90)); ld.ellipse([W-120,-160,W+220,260],fill=(201,164,92,60))
leak=leak.filter(ImageFilter.GaussianBlur(90))
frame=Image.alpha_composite(leak,frame)
frame.save(OUT+'series/PAST_film-frame-overlay_1920x1080.png')

# ---------- 3. Tape labels ----------
def torn_poly(w,h,j=5):
    pts=[]
    for x in range(0,w+1,14): pts.append((x,random.uniform(0,j)))
    for y in range(0,h+1,10): pts.append((w-random.uniform(0,j*1.6),y))
    for x in range(w,-1,-14): pts.append((x,h-random.uniform(0,j)))
    for y in range(h,-1,-10): pts.append((random.uniform(0,j*1.6),y))
    return pts
def label(text,size,paper,ink,w,h,underline=False,rot=0,font='Sriracha-Regular.ttf'):
    pad=40
    im=Image.new('RGBA',(w+pad*2,h+pad*2),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x+pad+6,y+pad+8) for x,y in torn_poly(w,h)],fill=(0,0,0,110))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(8)))
    p=Image.new('RGBA',im.size,(0,0,0,0)); pd=ImageDraw.Draw(p)
    pd.polygon([(x+pad,y+pad) for x,y in torn_poly(w,h)],fill=paper)
    # paper fibre noise
    for _ in range(int(w*h/60)):
        x=random.uniform(pad+6,pad+w-6); y=random.uniform(pad+6,pad+h-6)
        v=random.choice([(255,255,255,26),(90,70,40,22)]); pd.point((x,y),fill=v)
    im=Image.alpha_composite(im,p); dd=ImageDraw.Draw(im)
    f=ImageFont.truetype(FD+font,size)
    bb=dd.textbbox((0,0),text,font=f,features=['-kern']) if False else dd.textbbox((0,0),text,font=f)
    tx=pad+(w-(bb[2]-bb[0]))/2-bb[0]; ty=pad+(h-(bb[3]-bb[1]))/2-bb[1]-4
    dd.text((tx,ty),text,font=f,fill=ink)
    if underline:
        x0=tx+bb[0]-4; x1=tx+bb[2]+6; yb=ty+bb[3]+6
        dd.line([(x0,yb+3),((x0+x1)/2,yb),(x1,yb-4)],fill=(200,64,47,235),width=6,joint='curve')
    return im.rotate(rot,resample=Image.BICUBIC,expand=True)
L1=label('วันเสาร์',92,(241,232,212,255),(31,47,79,255),400,140,underline=True,rot=4)
L2=label('บ่าย 2 โมง',78,(233,198,74,255),(31,47,79,255),400,118,rot=-2)
L1.save(OUT+'shot01-02/S01_label-1_wansao.png'); L2.save(OUT+'shot01-02/S01_label-2_bai2mong.png')
# placement: top-left corner of each PNG in 1920x1080 frame
P1=(230-40+6,130-40+4); P2=(270-40,300-40)
place={'S01_label-1_wansao.png':{'png_size':L1.size,'top_left':P1,'center':(P1[0]+L1.size[0]//2,P1[1]+L1.size[1]//2)},
       'S01_label-2_bai2mong.png':{'png_size':L2.size,'top_left':P2,'center':(P2[0]+L2.size[0]//2,P2[1]+L2.size[1]//2)}}
for k,v in place.items():
    cx,cy=v['center']; v['capcut_position_xy']=(cx-W//2, H//2-cy)
json.dump(place,open(OUT+'shot01-02/S01_label-placement.json','w'),indent=1)

# ---------- 4. Clock hands (pivot = image centre, pointing 12 o'clock) ----------
S=1200; c=S//2
def hand(length,tail,wid,tip):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); dd=ImageDraw.Draw(im)
    poly=[(c-wid/2,c+tail),(c-wid*0.42,c-length*0.82),(c,c-length),(c+wid*0.42,c-length*0.82),(c+wid/2,c+tail)]
    sh=Image.new('RGBA',(S,S),(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x+6,y+8) for x,y in poly],fill=(0,0,0,90))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(im).polygon(poly,fill=(22,20,18,255))
    return im
hh=hand(300,50,30,0); mh=hand(470,70,20,0)
cap=ImageDraw.Draw(mh); cap.ellipse([c-26,c-26,c+26,c+26],fill=(28,26,24,255)); cap.ellipse([c-9,c-9,c+9,c+9],fill=(120,110,95,255))
hh.save(OUT+'shot01-02/S02_clock-hand-hour_pivot-center.png'); mh.save(OUT+'shot01-02/S02_clock-hand-minute_pivot-center.png')

# ---------- 5. Previews ----------
ref=Image.open('/home/user/TLIAppDS/back-in-time/ep01/references/REF-B_mbk-saturday-2pm.png').convert('RGBA').resize((W,H),Image.LANCZOS)
# cover old labels roughly so preview reads (preview only)
pv=ref.copy()
pv=Image.alpha_composite(pv,frame)
pv.alpha_composite(L1,P1); pv.alpha_composite(L2,P2)
pv=Image.alpha_composite(pv,g)
pv.convert('RGB').save(OUT+'shot01-02/S01_layout-preview_on-REF-B.jpg',quality=88)
# Shot 02 angle check on placeholder dial
ANG={'2:00':(60,0),'2:15':(67.5,90),'2:30':(75,180)}
row=Image.new('RGB',(W,H//2),(30,31,33))
for i,(t,(ha,ma)) in enumerate(ANG.items()):
    tile=Image.new('RGBA',(S,S),(0,0,0,0)); td=ImageDraw.Draw(tile)
    td.rounded_rectangle([60,60,S-60,S-60],radius=140,fill=(236,226,203,255),outline=(90,70,50,255),width=30)
    nf=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',90)
    for n in range(1,13):
        a=math.radians(n*30); r=440 if n%3 else 455
        x=c+r*math.sin(a); y=c-r*math.cos(a)
        td.text((x,y),str(n),font=nf,fill=(30,28,26,255),anchor='mm')
    tile=Image.alpha_composite(tile,hh.rotate(-ha,resample=Image.BICUBIC))
    tile=Image.alpha_composite(tile,mh.rotate(-ma,resample=Image.BICUBIC))
    tile=tile.resize((430,430),Image.LANCZOS)
    row.paste(tile,(150+i*560,40),tile)
    ImageDraw.Draw(row).text((150+i*560+215,500),f'{t}   hour {ha}°  ·  minute {ma}°',font=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',26),fill=(201,164,92),anchor='mm')
row.save(OUT+'shot01-02/S02_hand-angle-check.png')
print(json.dumps(place,indent=1))
