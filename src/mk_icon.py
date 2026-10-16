import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BLACK='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
N=2048
def make(top,bot,blk1,blk2,bubble,txt,txtshadow,label,labelcol,full=True):
  im=Image.new('RGBA',(N,N));d=ImageDraw.Draw(im)
  for y in range(N):
    t=y/N;d.line([(0,y),(N,y)],fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))+(255,))
  blk=Image.new('RGBA',(N,N));bd=ImageDraw.Draw(blk)
  bd.rounded_rectangle((300,1240,820,1640),radius=90,fill=blk1+(255,))
  bd.rounded_rectangle((1260,1180,1760,1580),radius=90,fill=blk2+(255,))
  im.alpha_composite(blk.rotate(-6,resample=Image.BICUBIC,center=(N/2,N/2)))
  sh=Image.new('RGBA',(N,N));sd=ImageDraw.Draw(sh)
  sd.rounded_rectangle((330,380,1720,1340),radius=300,fill=(0,0,0,70));sd.polygon([(620,1260),(560,1640),(940,1300)],fill=(0,0,0,70))
  sh=sh.filter(ImageFilter.GaussianBlur(40));im.alpha_composite(sh.transform((N,N),Image.AFFINE,(1,0,-10,0,1,-40)))
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((330,340,1720,1300),radius=300,fill=bubble+(255,));d.polygon([(640,1220),(560,1620),(960,1260)],fill=bubble+(255,))
  f=ImageFont.truetype(BLACK,640,index=1);t='툭!';bb=d.textbbox((0,0),t,font=f);cx,cy=1025,815
  d.text((cx-(bb[0]+bb[2])/2+18,cy-(bb[1]+bb[3])/2+22),t,font=f,fill=txtshadow+(255,))
  d.text((cx-(bb[0]+bb[2])/2,cy-(bb[1]+bb[3])/2),t,font=f,fill=txt+(255,))
  if full:
    f2=ImageFont.truetype(BLACK,190,index=2);bb=d.textbbox((0,0),label,font=f2)
    d.text((1300-(bb[0]+bb[2])/2,1720-(bb[1]+bb[3])/2),label,font=f2,fill=labelcol+(255,))
  return im
P={'tuk':dict(top=(255,150,172),bot=(255,104,140),blk1=(44,201,167),blk2=(255,209,102),bubble=(255,255,255),txt=(255,95,135),txtshadow=(255,214,224),label='速成·下',labelcol=(255,255,255)),
   'adv':dict(top=(168,140,255),bot=(123,91,232),blk1=(255,159,122),blk2=(44,201,167),bubble=(255,255,255),txt=(139,108,240),txtshadow=(226,218,255),label='高级会话',labelcol=(255,255,255))}
k=sys.argv[1];out=sys.argv[2];p=P[k]
full=make(**p);simple=make(**{**p,'full':False})
for s,name in ((512,'icon-512.png'),(192,'icon-192.png'),(180,'apple-touch-icon.png')): full.resize((s,s),Image.LANCZOS).convert('RGB').save(f'{out}/{name}')
simple.resize((64,64),Image.LANCZOS).convert('RGB').save(f'{out}/favicon-64.png')
src=full.resize((512,512),Image.LANCZOS);bg=Image.new('RGB',(512,512));bd=ImageDraw.Draw(bg)
for y in range(512):
  t=y/512;bd.line([(0,y),(512,y)],fill=tuple(int(a*(1-t)+b*t) for a,b in zip(p['top'],p['bot'])))
s=int(512*.78);bg.paste(src.resize((s,s),Image.LANCZOS).convert('RGB'),((512-s)//2,(512-s)//2));bg.save(f'{out}/icon-maskable-512.png')
