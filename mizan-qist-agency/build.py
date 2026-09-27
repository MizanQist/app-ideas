"""Build index.html (a self-contained presentation) from deck.json and slides/*.html."""
import json, pathlib
root = pathlib.Path(__file__).parent
deck = json.loads((root / "deck.json").read_text())
slides = "\n".join((root / "slides" / f"{sid}.html").read_text() for sid in deck["order"])
fonts = "\n".join(f'<link rel="stylesheet" href="{f["href"]}">' for f in deck["faces"].values() if "href" in f)
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{deck['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">{fonts}
<style>
*{{box-sizing:border-box;margin:0}}
html,body{{height:100%;background:#0b1512;overflow:hidden}}
#stage{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:center}}
section{{position:absolute;inset:0;width:1920px;height:1080px;visibility:hidden;overflow:hidden;font-family:'IBM Plex Sans',Arial,sans-serif;color:#12241F}}
section.on{{visibility:visible}}
aside{{display:none}} ul,ol{{padding-left:1.2em}}
table{{border-collapse:collapse}} th,td{{padding:.35em .6em;border-bottom:1px solid rgba(128,128,128,.35);vertical-align:top}}
x-shape{{display:block}} x-shape[kind=ellipse]{{border-radius:50%}}
x-icon{{display:block}}
#ui{{position:fixed;bottom:12px;right:16px;font:14px Arial,sans-serif;color:#9FB0A8}}
@media print{{html,body{{overflow:visible;height:auto}} #stage{{position:static;transform:none!important}} section{{visibility:visible!important;position:relative;page-break-after:always}} #ui{{display:none}}}}
</style></head><body>
<div id="stage">
{slides}
</div>
<div id="ui"><span id="n"></span> · ← → to navigate · F for fullscreen</div>
<script>
const s=[...document.querySelectorAll('#stage > section')];let i=Math.max(0,Math.min(s.length-1,(parseInt(location.hash.slice(1))||1)-1));
function show(){{s.forEach((e,k)=>e.classList.toggle('on',k===i));document.getElementById('n').textContent=(i+1)+' / '+s.length;history.replaceState(null,'','#'+(i+1))}}
function fit(){{const k=Math.min(innerWidth/1920,innerHeight/1080);document.getElementById('stage').style.transform='translate(-50%,-50%) scale('+k+')'}}
addEventListener('resize',fit);addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))i=Math.min(s.length-1,i+1);else if(['ArrowLeft','PageUp'].includes(e.key))i=Math.max(0,i-1);else if(e.key==='f')document.documentElement.requestFullscreen?.();else return;show()}});
addEventListener('click',e=>{{i=e.clientX>innerWidth/2?Math.min(s.length-1,i+1):Math.max(0,i-1);show()}});
addEventListener('hashchange',()=>{{const n=parseInt(location.hash.slice(1));if(n>=1&&n<=s.length&&n-1!==i){{i=n-1;show()}}}});
fit();show();
</script></body></html>"""
(root / "index.html").write_text(html)
print("built index.html with", len(deck["order"]), "slides")
