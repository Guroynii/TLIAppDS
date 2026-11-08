from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1920,1080
E='/home/user/TLIAppDS/back-in-time/ep01/'
A=E+'assets/shot03-04/'; FD='fonts/'
TEAL=(18,58,64); GOLD=(201,164,92); ORANGE=(224,122,58); OFF=(237,230,216); CHAR=(30,31,33)
raw=Image.open(E+'renders/S01_higgsfield_raw.png').convert('RGB')
k=raw.width/1920
def crop(x0,y0,x1,y1): return raw.crop((int(x0*k),int(y0*k),int(x1*k),int(y1*k))).resize((W,H),Image.LANCZOS)
crop(300,405,1500,1080).save(E+'renders/S03_plate_crop_1920x1080.png')
crop(0,270,1440,1080).save(E+'renders/S04_plate_crop_1920x1080.png')
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))
f48=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',50); f40=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',42); f28=ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',30)
PX0,PY0,PX1,PY1=1060,300,1690,780
# L0 scrim
s=layer(); sd=ImageDraw.Draw(s)
for x in range(900,W):
    a=int(110*min(1,(x-900)/500)); sd.line([(x,0),(x,H)],fill=CHAR+(a,))
s.save(A+'S03_L0_scrim.png')
# L1 panel
p=layer(); d=ImageDraw.Draw(p)
d.rounded_rectangle([PX0,PY0,PX1,PY1],radius=28,fill=TEAL+(217,),outline=GOLD+(150,),width=2)
d.line([(PX0+40,540),(PX1-40,540)],fill=GOLD+(70,),width=1)
p.save(A+'S03_L1_panel.png')
# L2 phone icon (row 1)
ic=layer(); d=ImageDraw.Draw(ic); cx,cy=1150,420
d.rounded_rectangle([cx-30,cy-56,cx+30,cy+56],radius=10,outline=GOLD+(255,),width=4)
d.line([(cx-12,cy-44),(cx+12,cy-44)],fill=GOLD+(255,),width=3)
d.ellipse([cx-6,cy+38,cx+6,cy+50],outline=GOLD+(255,),width=3)
for i,dy in enumerate((-22,-6,10)):  # signal arcs
    pass
ic.save(A+'S03_L2_icon-phone.png')
st=layer(); d=ImageDraw.Draw(st); d.line([(cx-48,cy+60),(cx+48,cy-60)],fill=ORANGE+(255,),width=7)
st.save(A+'S03_L3_strike.png')
t=layer(); d=ImageDraw.Draw(t); d.text((1230,420),'ไม่มีมือถือ',font=f48,fill=OFF+(255,),anchor='lm')
t.save(A+'S03_L4_text-no-mobile.png')
# L5 bubble (row 2)
b=layer(); d=ImageDraw.Draw(b)
bx0,by0,bx1,by1=1110,590,1530,680
sh=layer(); ImageDraw.Draw(sh).rounded_rectangle([bx0+4,by0+6,bx1+4,by1+6],radius=26,fill=(0,0,0,90)); b=Image.alpha_composite(b,sh.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(b)
d.rounded_rectangle([bx0,by0,bx1,by1],radius=26,fill=OFF+(255,))
d.polygon([(bx1-46,by1-2),(bx1-8,by1+24),(bx1-18,by1-2)],fill=OFF+(255,))
d.text(((bx0+bx1)/2,(by0+by1)/2-2),'ถึงไหนแล้ววะ?',font=f40,fill=CHAR+(255,),anchor='mm')
b.save(A+'S03_L5_bubble.png')
# L6 send failed
fl=layer(); d=ImageDraw.Draw(fl); fx,fy=1200,728
d.ellipse([fx-17,fy-17,fx+17,fy+17],fill=ORANGE+(255,))
d.text((fx,fy-1),'!',font=f28,fill=OFF+(255,),anchor='mm')
d.text((fx+30,fy),'ส่งไม่ได้',font=f28,fill=ORANGE+(255,),anchor='lm')
fl.save(A+'S03_L6_send-failed.png')
# preview final state
frame=Image.open(E+'assets/series/PAST_film-frame-overlay_1920x1080.png')
guide=Image.open(E+'assets/series/GUIDE_safe-area_1920x1080.png')
bg=Image.open(E+'renders/S03_plate_crop_1920x1080.png').convert('RGBA')
c=bg
for n in ['S03_L0_scrim','S03_L1_panel','S03_L2_icon-phone','S03_L3_strike','S03_L4_text-no-mobile']:
    c=Image.alpha_composite(c,Image.open(A+n+'.png'))
bub=Image.open(A+'S03_L5_bubble.png'); r,g,bb,al=bub.split(); bub.putalpha(al.point(lambda v:int(v*0.55)))
c=Image.alpha_composite(c,bub); c=Image.alpha_composite(c,Image.open(A+'S03_L6_send-failed.png'))
c=Image.alpha_composite(c,frame)
c.convert('RGB').save(E+'renders/S03_comp_final.jpg',quality=90)
Image.alpha_composite(c,guide).convert('RGB').resize((960,540)).save('s03g.jpg')
c4=Image.alpha_composite(Image.open(E+'renders/S04_plate_crop_1920x1080.png').convert('RGBA'),frame)
c4.convert('RGB').save(E+'renders/S04_comp_final.jpg',quality=90); c4.convert('RGB').resize((960,540)).save('s04.jpg')
