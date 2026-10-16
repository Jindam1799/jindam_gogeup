import re,os,json,hashlib
app=open('app.html',encoding='utf-8').read()
data=open('data.js',encoding='utf-8').read()
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
