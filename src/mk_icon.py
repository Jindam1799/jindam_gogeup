from PIL import Image,ImageDraw,ImageFont,ImageFilter
BLACK='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
N=2048
def make(variant):
  im=Image.new('RGBA',(N,N));d=ImageDraw.Draw(im)
  # 배경: 짙은 초록 세로 그라데이션
  top=(62,76,124);bot=(38,47,84)
  for y in range(N):
    t=y/N;d.line([(0,y),(N,y)],fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))+(255,))
  # 덩어리 블록 (뒤쪽, 살짝 기울인 노란·초록 블록)
  blk=Image.new('RGBA',(N,N));bd=ImageDraw.Draw(blk)
  bd.rounded_rectangle((300,1240,820,1640),radius=90,fill=(182,220,199,255))
  bd.rounded_rectangle((1260,1180,1760,1580),radius=90,fill=(243,195,147,255))
  blk=blk.rotate(-6,resample=Image.BICUBIC,center=(N/2,N/2))
  im.alpha_composite(blk)
  # 말풍선 그림자
  sh=Image.new('RGBA',(N,N));sd=ImageDraw.Draw(sh)
  sd.rounded_rectangle((330,380,1720,1340),radius=300,fill=(0,0,0,110))
  sd.polygon([(620,1260),(560,1640),(940,1300)],fill=(0,0,0,110))
  sh=sh.filter(ImageFilter.GaussianBlur(40));sh=sh.transform((N,N),Image.AFFINE,(1,0,-10,0,1,-40))
  im.alpha_composite(sh)
  # 말풍선 (빨강)
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((330,340,1720,1300),radius=300,fill=(222,95,87,255))
  d.polygon([(640,1220),(560,1620),(960,1260)],fill=(222,95,87,255))
  # 툭!
  f=ImageFont.truetype(BLACK,640,index=1)
  t='툭!';bb=d.textbbox((0,0),t,font=f)
  cx,cy=1025,815
  d.text((cx-(bb[0]+bb[2])/2+18,cy-(bb[1]+bb[3])/2+22),t,font=f,fill=(130,40,35,255))
  d.text((cx-(bb[0]+bb[2])/2,cy-(bb[1]+bb[3])/2),t,font=f,fill=(255,255,255,255))
  # 아래 라벨
  if variant=='full':
    f2=ImageFont.truetype(BLACK,190,index=2)  # SC
    t2='高级会话';bb=d.textbbox((0,0),t2,font=f2)
    d.text((1180-(bb[0]+bb[2])/2+120,1720-(bb[1]+bb[3])/2),t2,font=f2,fill=(255,236,190,255))
  return im
full=make('full')
for s,name in ((512,'icon-512.png'),(192,'icon-192.png'),(180,'apple-touch-icon.png')):
  full.resize((s,s),Image.LANCZOS).convert('RGB').save(name)
simple=make('simple')
simple.resize((64,64),Image.LANCZOS).convert('RGB').save('favicon-64.png')
# 미리보기: 둥근 모서리 마스크로 홈화면처럼
prev=Image.new('RGB',(1400,560),(237,243,239))
for i,(s,src) in enumerate(((440,full),(200,full),(96,full),(64,simple))):
  ic=src.resize((s,s),Image.LANCZOS);m=Image.new('L',(s,s),0);ImageDraw.Draw(m).rounded_rectangle((0,0,s-1,s-1),radius=int(s*.22),fill=255)
  x=[40,560,840,1020][i];prev.paste(ic,(x,(560-s)//2),m)
prev.save('preview.png')
