import re,os,json,hashlib
app=open('app.html',encoding='utf-8').read()
data=open('data.js',encoding='utf-8').read()
import os,sys,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from pron import build_map
PRON=build_map(['data.js'])
print('pron fixes',len(PRON))
data+='\nconst PRON='+json.dumps(PRON,ensure_ascii=False)+';'
art=app.replace('/*__DATA__*/',data)
open('dist_artifact.html','w',encoding='utf-8').write(art)
m=re.match(r'(<title>.*?</title>)\s*<meta name="claude:viewport-fit-sides" content="cover">\s*(<style>.*?</style>)(.*)',art,re.S)
title,style,body=m.group(1),m.group(2),m.group(3)
_h=hashlib.md5(art.encode())
for _f in sorted(os.listdir('site/icons')) if os.path.isdir('site/icons') else []:
  _h.update(open(os.path.join('site/icons',_f),'rb').read())
ver=_h.hexdigest()[:8]
pwa='''<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon-64.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="툭! 고급회화">'''
reg='''<script>
if('serviceWorker' in navigator && location.protocol==='https:'){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){})})}
</script>'''
chrome='''<script>
/* 항상 크롬으로 열기: 크롬이 아닌 모바일 브라우저(카톡·네이버·인스타 등 앱 안 화면, 삼성 인터넷, 사파리 등)면 매번 크롬으로 이동.
   크롬이 없는 폰은 한 번 확인 후 기억해서 다시 시도하지 않음(무한 반복 방지). */
(function(){
  if(location.protocol!=='https:')return;
  var ua=navigator.userAgent;
  var android=/Android/i.test(ua),ios=/iPhone|iPad|iPod/i.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  var isChrome=ios?/CriOS/.test(ua):(/Chrome\\//.test(ua)&&!/; wv\\)|SamsungBrowser|EdgA|OPR|Whale|KAKAOTALK|NAVER|DaumApps|Instagram|FBAN|FBAV|Line\\//i.test(ua));
  // 홈 화면에 추가한 웹앱으로 실행 중이면 아무것도 하지 않음 (이동·안내 띠 모두 없음)
  var standalone=(window.matchMedia&&(matchMedia('(display-mode: standalone)').matches||matchMedia('(display-mode: fullscreen)').matches||matchMedia('(display-mode: minimal-ui)').matches))||navigator.standalone===true||/^android-app:/.test(document.referrer);
  if(standalone)return;
  if(isChrome||!(android||ios))return;
  var NO='dtuk_no_chrome';
  var u=new URL(location.href);
  if(u.searchParams.get('nochrome')==='1'){try{localStorage.setItem(NO,'1')}catch(e){}}
  u.searchParams.delete('nochrome');u.hash='';
  var url=u.toString(),noPrefix=url.replace(/^https:\\/\\//,'');
  var fb=new URL(url);fb.searchParams.set('nochrome','1');
  var androidIntent='intent://'+noPrefix+'#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url='+encodeURIComponent(fb.toString())+';end';
  function noChrome(){try{return localStorage.getItem(NO)==='1'}catch(e){return false}}
  function openChrome(manual){
    if(android){location.href=androidIntent;return}
    location.href='googlechromes://'+noPrefix;
    setTimeout(function(){
      if(document.hidden)return;               // 크롬으로 넘어감
      if(!manual){try{localStorage.setItem(NO,'1')}catch(e){}}  // 크롬 없음 → 다음부터 자동 시도 안 함
      if(/KAKAOTALK/i.test(ua))location.href='kakaotalk://web/openExternal?url='+encodeURIComponent(url);
    },1600);
  }
  if(!noChrome())setTimeout(function(){openChrome(false)},250);
  function banner(){
    if(document.getElementById('gochrome'))return;
    var d=document.createElement('div');d.id='gochrome';
    d.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:9999;padding:12px max(16px,env(safe-area-inset-right,0px)) calc(12px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));background:#2E3A63;color:#fff;font:600 15px/1.4 system-ui,sans-serif;display:flex;gap:8px;align-items:center;box-shadow:0 -6px 20px rgba(0,0,0,.2)';
    d.innerHTML='<span style="flex:1">'+(noChrome()?'이 게임은 <b>크롬</b>에 맞춰 만들었어요. 크롬을 설치하면 가장 잘 나와요.':'크롬에서 열면 소리와 화면이 가장 잘 나와요.')+'</span><button id="gcgo" style="border:0;border-radius:12px;padding:10px 14px;background:#DE5F57;color:#fff;font:800 15px system-ui,sans-serif;white-space:nowrap">크롬으로 열기</button><button id="gcx" aria-label="닫기" style="border:0;background:none;color:#fff;font-size:20px;padding:4px 6px">✕</button>';
    document.body.appendChild(d);
    document.getElementById('gcgo').onclick=function(){try{localStorage.removeItem(NO)}catch(e){}openChrome(true)};
    document.getElementById('gcx').onclick=function(){d.remove()};
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',banner);else banner();
})();
</script>'''
def page(with_pwa):
  return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#2E3A63">
{title}
{pwa if with_pwa else ''}
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
{style}
</head>
<body>{body}
{reg if with_pwa else ''}
{chrome if with_pwa else ''}
</body>
</html>
'''
os.makedirs('site/icons',exist_ok=True)
open('index.html','w',encoding='utf-8').write(page(False))          # 오프라인 비상용 단일 파일
open('site/index.html','w',encoding='utf-8').write(page(True))      # GitHub Pages용
open('site/manifest.webmanifest','w',encoding='utf-8').write(json.dumps({
 "name":"덩어리 툭! 고급회화","short_name":"툭! 고급회화","start_url":"./","scope":"./","display":"standalone",
 "orientation":"portrait","background_color":"#F6F3F0","theme_color":"#2E3A63","lang":"ko",
 "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
          {"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
          {"src":"icons/icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},ensure_ascii=False,indent=1))
open('site/sw.js','w',encoding='utf-8').write(f'''// 덩어리 툭! 오프라인 캐시 (버전 {ver})
const CACHE='dtuk-adv-{ver}';
const FILES=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/icon-maskable-512.png','./icons/apple-touch-icon.png','./icons/favicon-64.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
// 화면은 인터넷이 되면 최신본, 안 되면 저장본
self.addEventListener('fetch',e=>{{
  if(e.request.method!=='GET')return;
  const isPage=e.request.mode==='navigate';
  if(isPage){{e.respondWith(fetch(e.request).then(r=>{{const cp=r.clone();caches.open(CACHE).then(c=>c.put('./index.html',cp));return r}}).catch(()=>caches.match('./index.html')));return}}
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
}});
''')
print('ver',ver,len(art))
