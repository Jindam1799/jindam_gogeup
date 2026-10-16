import sys
SKINS={
'tuk':dict(bg='#F8FBF9',surface2='#F2F8F5',line='#E0EBE5',ink='#1F2D27',muted='#5F726A',
  act='#20A57B',act2='#18906B',actsoft='#E3F5EE',hero1='#E6F7EF',hero2='#FFF4D6',accent='#FF8A5B',accentsoft='#FFEDE4',sun='#FFC94D',
  dark=dict(bg='#111816',surface='#1A2420',surface2='#1F2B26',line='#2E3D37',ink='#EEF5F1',muted='#A9BCB4',act='#3CC896',act2='#2FB083',actsoft='#173A2F',hero1='#173A2F',hero2='#3A321A')),
'adv':dict(bg='#FFFAF7',surface2='#FFF4EF',line='#F0E3DC',ink='#2B3256',muted='#6B7090',
  act='#5B6BE0',act2='#4A59C9',actsoft='#ECEEFC',hero1='#FFE9E3',hero2='#EDEBFF',accent='#F2766B',accentsoft='#FDE7E4',sun='#FFB45C',
  dark=dict(bg='#14162A',surface='#1D2039',surface2='#232745',line='#353A5E',ink='#ECEEF7',muted='#A9AFC8',act='#8C98FF',act2='#7683F0',actsoft='#262B55',hero1='#3A2430',hero2='#262B55')),
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
            f"--seal:{base.get('accent',s['accent'])};--seal-soft:{base.get('accentsoft',s['accentsoft'])};--sun:{s['sun']};"
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
