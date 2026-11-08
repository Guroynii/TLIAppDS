from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, numpy as np
W,H=1920,1080; E='/home/user/TLIAppDS/back-in-time/ep01/'; A=E+'assets/shot06-08/'; FD='fonts/'
TEAL=(18,58,64); GOLD=(201,164,92); ORANGE=(224,122,58); OFF=(237,230,216); CHAR=(30,31,33)
B=lambda s: ImageFont.truetype(FD+'PlexThai-Bold.ttf',s); SB=lambda s: ImageFont.truetype(FD+'PlexThai-SemiBold.ttf',s)
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))
# Title dim
l=layer(); ImageDraw.Draw(l).rectangle([0,0,W,H],fill=CHAR+(120,)); l.save(A+'S07_T0_dim.png')
# Title card
t=layer(); d=ImageDraw.Draw(t)
title='B A C K   I N   T I M E'
d.text((W/2,470),title,font=B(104),fill=GOLD+(255,),anchor='mm')
d.line([(560,575),(860,575)],fill=GOLD+(200,),width=2); d.line([(1060,575),(1360,575)],fill=GOLD+(200,),width=2)
d.text((W/2,576),'EP.01',font=SB(38),fill=OFF+(255,),anchor='mm')
d.text((W/2,665),'ทำไมเราถึงคิดถึงวัยรุ่นยุค 90?',font=SB(56),fill=OFF+(255,),anchor='mm')
sh=t.filter(ImageFilter.GaussianBlur(10)); r,g,b,a=sh.split(); shadow=Image.merge('RGBA',(Image.new('L',(W,H),0),)*3+(a.point(lambda v:int(v*0.6)),))
Image.alpha_composite(shadow,t).save(A+'S07_T1_title.png')
# Question panel top-right
X0,Y0,X1,Y1=1236,140,1690,420
p=layer(); d=ImageDraw.Draw(p)
d.rounded_rectangle([X0,Y0,X1,Y1],radius=24,fill=TEAL+(222,),outline=GOLD+(150,),width=2)
d.text((X0+30,Y0+42),'คำถามของตอนนี้',font=SB(28),fill=GOLD+(255,),anchor='lm')
d.line([(X0+30,Y0+74),(X0+114,Y0+74)],fill=GOLD+(200,),width=3)
p.save(A+'S08_Q0_panel.png')
q1=layer(); ImageDraw.Draw(q1).text((X0+30,Y0+126),'ทำไมชีวิตที่ดูยุ่งยากกว่า',font=SB(37),fill=OFF+(255,),anchor='lm'); q1.save(A+'S08_Q1_line1.png')
q2=layer(); d=ImageDraw.Draw(q2)
d.text((X0+30,Y0+182),'ถึงกลายเป็นความทรงจำ',font=SB(37),fill=OFF+(255,),anchor='lm')
d.text((X0+30,Y0+238),'ที่เรายังอยากกลับไปหา?',font=SB(37),fill=ORANGE+(255,),anchor='lm')
q2.save(A+'S08_Q2_line2-3.png')
# previews from upscaled video
def grab(t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',E+'renders/S06-08_host_1920x1080.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return Image.frombytes('RGB',(W,H),raw).convert('RGBA')
guide=Image.open(E+'assets/series/GUIDE_safe-area_1920x1080.png')
f=grab(4.5).filter(ImageFilter.GaussianBlur(18)); f=Image.alpha_composite(f,Image.open(A+'S07_T0_dim.png')); f=Image.alpha_composite(f,Image.open(A+'S07_T1_title.png'))
f.convert('RGB').save(E+'renders/S07_comp_title.jpg',quality=90); Image.alpha_composite(f,guide).convert('RGB').resize((960,540)).save('s07g.jpg')
for tt in (10.5,11.6):
    f=grab(tt)
    for n in ['S08_Q0_panel','S08_Q1_line1','S08_Q2_line2-3']: f=Image.alpha_composite(f,Image.open(A+n+'.png'))
    f.convert('RGB').save(E+f'renders/S08_comp_question_{tt}.jpg',quality=90)
    Image.alpha_composite(f,guide).convert('RGB').resize((960,540)).save(f's08g_{tt}.jpg')
