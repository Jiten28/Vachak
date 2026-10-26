import json,re,sys,os
import os
H=os.path.dirname(os.path.abspath(__file__))+'/'; B=H; R=H+'../'
app=open(B+'app.src.html',encoding='utf-8').read()
legacy=open(H+'legacy.js',encoding='utf-8').read()
gita=open(H+'gita.json',encoding='utf-8').read()
pal_css=open(B+'palettes.css').read(); pal_json=open(B+'palettes.json').read()
def fill(t,paths):
    return (t.replace('/*__LEGACY__*/',legacy).replace('/*__GITA__*/',gita).replace('/*__PALETTES__*/',pal_css)
             .replace('/*__PALJSON__*/',pal_json).replace('/*__PATHS__*/',json.dumps(paths)))
EARLY='''<script>try{var _p=JSON.parse(localStorage.getItem('vachak.palette')||'null')||'mayur',_m=JSON.parse(localStorage.getItem('vachak.mode')||'null')||'system',_d=_m==='dark'||(_m==='system'&&matchMedia('(prefers-color-scheme: dark)').matches),_r=document.documentElement;_r.setAttribute('data-palette',_p);_r.setAttribute('data-theme',_d?'dark':'light')}catch(e){}
(function(){var u=navigator.userAgent||'',p=navigator.platform||'',t=navigator.maxTouchPoints||0;window.__plat=function(o){if(o&&o!=='auto')return o;if(/iPhone|iPad|iPod/.test(u)||(p==='MacIntel'&&t>1))return'ios';if(/Android/.test(u))return'android';if(/Mac/.test(p))return'mac';if(/Win/.test(p))return'windows';return'desktop'};var o='auto';try{o=JSON.parse(localStorage.getItem('vachak.ui')||'"auto"')}catch(e){}document.documentElement.setAttribute('data-platform',window.__plat(o))})()</script>'''
# ---------- PWA build ----------
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Vachak Reader</title>
<meta name="description" content="Open a Hindi, Sanskrit or English PDF and listen to it in a natural voice. Works offline.">
<meta name="theme-color" content="#DCE8E8">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Vachak">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="stylesheet" href="vendor/fonts/fonts.css">
'''+EARLY+'''
<script src="vendor/pdfjs/pdf.min.js"></script>
<style>body{margin:0}[hidden]{display:none!important}</style>
</head>
<body>
'''
pwa=head+fill(app,{'pdfWorker':'vendor/pdfjs/pdf.worker.min.js','pack':True,'sw':True})+'\n</body>\n</html>\n'
open(R+'index.html','w',encoding='utf-8').write(pwa)
# ---------- artifact preview build (no service worker, no voice pack, CDN libraries) ----------
art_head='''<title>Vachak Reader</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=Tiro+Devanagari+Hindi:ital@0;1&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
'''+EARLY+'\n'
art=art_head+fill(app,{'pdfWorker':'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js','pack':False,'sw':False})
open(H+'vachak-artifact.html','w',encoding='utf-8').write(art)
print('pwa',len(pwa),'artifact',len(art))
