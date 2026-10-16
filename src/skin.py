import sys
SKINS={
# 速成: 메인 코랄 핑크 + 민트 + 레몬
'tuk':dict(bg='#FFFBF8',surface2='#FFF5F2',line='#F3E4E0',ink='#2B2730',muted='#6E6670',
  act='#1FB596',act2='#169A80',actsoft='#DDF6EF',hero1='#FFE3EA',hero2='#FFF3CF',accent='#FF6F91',accentsoft='#FFE6EE',sun='#FFD166',
  dark=dict(bg='#17141A',surface='#221D25',surface2='#2A242E',line='#3B3340',ink='#F4EEF2',muted='#B9AEB8',act='#36D2B0',act2='#27B596',actsoft='#173A33',hero1='#3D2230',hero2='#3A331C',accent='#FF85A2',accentsoft='#3D2230')),
# 고급회화: 메인 바이올렛 + 피치 + 민트
'adv':dict(bg='#FFFBF8',surface2='#FAF6FF',line='#ECE4F3',ink='#2A2740',muted='#6C6880',
  act='#FF8A65',act2='#E9704B',actsoft='#FFEDE5',hero1='#EEE8FF',hero2='#FFEADF',accent='#8B6CF0',accentsoft='#EEE8FF',sun='#FFC266',
  dark=dict(bg='#16141F',surface='#201D2D',surface2='#272338',line='#3A3550',ink='#F0EEF8',muted='#B1ACC8',act='#FF9A78',act2='#F08260',actsoft='#3A2620',hero1='#2C2550',hero2='#3A2620',accent='#A68DFF',accentsoft='#2C2550')),
}

TUKCARDS="""
/* 速成 과 카드 파스텔 (민트·노랑·살구·하늘 반복) */
.grid .lcard:nth-child(4n+1){background:#EEF9F3}.grid .lcard:nth-child(4n+2){background:#FFF8E3}
.grid .lcard:nth-child(4n+3){background:#FFF0E8}.grid .lcard:nth-child(4n+4){background:#EAF4FE}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .grid .lcard{background:var(--surface)!important}}
:root[data-theme="dark"] .grid .lcard{background:var(--surface)!important}
"""
def css(k):
  s=SKINS[k];d=s['dark']
  def toks(t,dk=False):
    base=dict(s);base.update(t if dk else {})
    return (f"--bg:{base['bg']};--surface2:{base['surface2']};--line:{base['line']};--ink:{base['ink']};--muted:{base['muted']};"
            f"--act:{base['act']};--act2:{base['act2']};--act-soft:{base['actsoft']};--hero1:{base['hero1']};--hero2:{base['hero2']};"
            f"--seal:{base['accent']};--seal-soft:{base['accentsoft']};--sun:{s['sun']};"
            +(f"--surface:{base['surface']};" if dk else "--surface:#FFFFFF;"))
  return f"""
/* ===== 밝은 스킨: 흰 바탕 · 파스텔 · 진한 덩어리 제거 (남녀노소 친화) ===== */
:root{{{toks({})}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{{toks(d,True)}}}}}
:root[data-theme="dark"]{{{toks(d,True)}}}
body{{background:var(--bg)}}
.hero2{{background:linear-gradient(120deg,var(--hero1),var(--hero2));color:var(--ink);border:1.5px solid var(--line)}}
.hero2 p{{opacity:1;color:var(--muted)}} .hero2 b{{color:var(--ink)}} .hero2 b::first-letter{{color:inherit}}
.hero2 .hseal{{background:var(--surface);border-color:var(--seal);color:var(--seal)}}
.btn{{border-radius:18px;box-shadow:0 2px 0 var(--line)}}
.btn.dark{{background:var(--act);border-color:var(--act);color:#fff;box-shadow:0 3px 0 var(--act2)}}
.btn.primary{{box-shadow:0 3px 0 color-mix(in srgb,var(--seal) 75%,#000)}}
.btn:active{{transform:translateY(2px);box-shadow:none}}
.seg button[aria-pressed="true"],.gtabs button[aria-selected="true"],.pill.tg[aria-pressed="true"]{{background:var(--act);color:#fff;border-color:var(--act)}}
.stepbtn{{box-shadow:0 2px 0 var(--line)}}
.stepbtn .n{{background:var(--act-soft);color:var(--act)}}
.stepbtn.done .n{{background:var(--act);color:#fff}}
.ans .tile{{background:var(--act);border-color:var(--act);color:#fff}}
.gnum li span{{background:var(--act-soft);color:var(--act)}}
.lcard{{box-shadow:0 2px 0 var(--line)}}
.opt{{box-shadow:0 2px 0 var(--line)}}
.qcard{{box-shadow:0 4px 18px color-mix(in srgb,var(--ink) 6%,transparent)}}
.tile{{box-shadow:0 3px 0 var(--line)}}
.pill{{box-shadow:0 1px 0 var(--line)}}
.gchips span{{background:var(--seal-soft);color:var(--seal)}}
.lhead .k{{color:var(--seal)}}
/* 단계별 색 (1 민트 · 2 하늘 · 3 살구 · 4 라벤더) */
.stepbtn[data-s="0"] .n{{background:#DDF4EA;color:#1C9A70}}.stepbtn[data-s="1"] .n{{background:#DDEEFD;color:#2A7BD0}}
.stepbtn[data-s="2"] .n{{background:#FFE9DC;color:#E06A35}}.stepbtn[data-s="3"] .n{{background:#ECE6FD;color:#7353D6}}
.stepbtn.done .n{{background:var(--act);color:#fff}}
.isteps li:nth-child(1){{background:#DDF4EA}}.isteps li:nth-child(2){{background:#DDEEFD}}.isteps li:nth-child(3){{background:#FFE9DC}}.isteps li:nth-child(4){{background:#ECE6FD}}
.isteps li:nth-child(1) span{{background:#1C9A70}}.isteps li:nth-child(2) span{{background:#2A7BD0}}.isteps li:nth-child(3) span{{background:#E06A35}}.isteps li:nth-child(4) span{{background:#7353D6}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) .stepbtn:not(.done) .n,:root:not([data-theme="light"]) .isteps li{{filter:brightness(.55) saturate(1.2)}}}}
"""+(TUKCARDS if k=='tuk' else '')
if __name__=='__main__':
  k=sys.argv[1];p=f'/home/claude/{k}/app.html';s=open(p,encoding='utf-8').read()
  mark='/* ===== 밝은 스킨'
  if mark in s:
    a=s.index('\n'+mark);b=s.index('</style>',a);s=s[:a]+s[b:]
  i=s.index('</style>');s=s[:i]+css(k)+s[i:]
  open(p,'w',encoding='utf-8').write(s);print('skin applied',k)
