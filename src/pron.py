# 다음자(多音字) 발음 보정: 데이터의 병음으로 글자별 독음을 맞춘 뒤, TTS가 헷갈리는 독음은 같은 소리의 다른 글자로 바꿔 읽힌다(화면 표시는 그대로).
import re,unicodedata
INIT=['zh','ch','sh','b','p','m','f','d','t','n','l','g','k','h','j','q','x','r','z','c','s','y','w','']
FIN=['iang','iong','uang','ueng','ang','eng','ing','ong','ian','iao','uai','uan','van','üan','ai','ei','ao','ou','an','en','in','un','ün','vn','ia','ie','iu','ua','uo','ui','ue','üe','ve','er','a','o','e','i','u','ü','v','n','ng','m']
SYL=set(i+f for i in INIT for f in FIN if i+f)
TONE={'ā':('a',1),'á':('a',2),'ǎ':('a',3),'à':('a',4),'ē':('e',1),'é':('e',2),'ě':('e',3),'è':('e',4),'ī':('i',1),'í':('i',2),'ǐ':('i',3),'ì':('i',4),'ō':('o',1),'ó':('o',2),'ǒ':('o',3),'ò':('o',4),'ū':('u',1),'ú':('u',2),'ǔ':('u',3),'ù':('u',4),'ǖ':('ü',1),'ǘ':('ü',2),'ǚ':('ü',3),'ǜ':('ü',4)}
def plain(s): return ''.join(TONE.get(c,(c,0))[0] for c in s)
def split_tok(tok,k):
  p=plain(tok);n=len(p);memo={}
  def go(i,left):
    if i==n: return [] if left==0 else None
    if left==0: return None
    key=(i,left)
    if key in memo: return memo[key]
    res=None
    for j in range(min(n,i+6),i,-1):
      if p[i:j] in SYL:
        r=go(j,left-1)
        if r is not None: res=[tok[i:j]]+r;break
      if p[i:j].endswith('r') and p[i:j-1] in SYL and left>=2:
        r=go(j,left-2)
        if r is not None: res=[tok[i:j-1],'r']+r;break
    memo[key]=res;return res
  return go(0,k)
HAN=re.compile(r'[一-鿿]')
def align(zh,py):
  chars=[c for c in zh if HAN.match(c)]
  toks=[t for t in re.split(r"[\s\-'’,，.。!！?？;；:：\"“”()（）…/]+",py.lower()) if t]
  # 숫자/영문(HSK 등) 제거
  toks=[t for t in toks if not re.fullmatch(r'[0-9a-z]*[0-9][0-9a-z]*',t) and t not in ('hsk',)]
  # 토큰별 음절 수를 앞에서부터 탐욕적으로 배정
  out=[];
  def solve(ti,ci):
    if ti==len(toks): return [] if ci==len(chars) else None
    for k in range(1,6):
      if ci+k>len(chars): break
      s=split_tok(toks[ti],k)
      if s:
        r=solve(ti+1,ci+k)
        if r is not None: return s+r
    return None
  syl=solve(0,0)
  if syl is None or len(syl)!=len(chars): return None
  return list(zip(chars,syl))
# (글자, 독음) → TTS용 대체 글자
FIX={('地','de'):'的',('还','huán'):'环',('觉','jiào'):'叫',('为','wéi'):'维',('当','dàng'):'荡',('少','shào'):'绍',
     ('重','chóng'):'虫',('倒','dǎo'):'岛',('相','xiàng'):'象',('空','kòng'):'控',('量','liáng'):'凉',('夫','fu'):'夫',
     ('大','dài'):'代',('得','děi'):'得',('了','liǎo'):'了',('着','zháo'):'着',('长','zhǎng'):'掌',('背','bēi'):'杯',
     ('便','pián'):'便',('应','yìng'):'应',('行','háng'):'航',('好','hào'):'号',('中','zhòng'):'众',('只','zhī'):'枝',
     ('闷','mēn'):'闷',('干','gàn'):'干',('称','chèn'):'趁',('处','chǔ'):'楚',('朝','cháo'):'潮',('传','zhuàn'):'赚',
     ('发','fà'):'珐',('种','zhòng'):'众',('数','shǔ'):'鼠',('调','diào'):'掉',('乐','yuè'):'月',('看','kān'):'刊'}
def fix(zh,py):
  al=align(zh,py)
  if not al: return None,None
  it=iter(al);out=[];changes=[]
  for c in zh:
    if HAN.match(c):
      ch,s=next(it);rep=FIX.get((ch,s.lower()))
      # 경성 표기(de)는 성조 없음
      if rep and rep!=ch: out.append(rep);changes.append(f'{ch}({s})→{rep}');continue
    out.append(c)
  return ''.join(out),changes
import json,subprocess,os,tempfile
def build_map(files):
  js=''.join(open(f,encoding='utf-8').read()+'\n' for f in files)
  dump=";const o=[];for(const l of LESSONS){l.c.forEach(x=>{const a=x.split('|');o.push([a[0],a[1]])});l.s.forEach(x=>{const a=x.split('|');o.push([a[1].replace(/\\//g,''),a[2]])});l.q.forEach(x=>{const a=x.split('|');o.push([a[0],a[1]]);o.push([a[3],a[4]])});l.m.forEach(x=>{const a=x.split('|');o.push([a[2],a[3]])})};for(const V of [typeof BOOK_VOCAB!=='undefined'?BOOK_VOCAB:{},typeof EXTRA_VOCAB!=='undefined'?EXTRA_VOCAB:{},typeof IDIOMS!=='undefined'?IDIOMS:{}])for(const k in V)V[k].split(';').forEach(e=>{const a=e.split('|');o.push([a[0],a[1]])});console.log(JSON.stringify(o))"
  fd,tmp=tempfile.mkstemp(suffix='.js');os.write(fd,(js+dump).encode());os.close(fd)
  pairs=json.loads(subprocess.run(['node',tmp],capture_output=True,text=True,check=True).stdout);os.remove(tmp)
  m={}
  for zh,py in pairs:
    for z,p in ((re.sub(r'\(.*?\)|（.*?）|……|…','',zh),re.sub(r'\(.*?\)|（.*?）|…','',py)),(re.sub(r'[()（）]|……|…','',zh),re.sub(r'[()（）]|…','',py))):
      f,c=fix(z,p)
      if f and c and f!=z: m[z]=f
  return m
