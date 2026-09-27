"""Build index.html (a self-contained presentation) from deck.json and slides/*.html."""
import json, pathlib
root = pathlib.Path(__file__).parent
deck = json.loads((root / "deck.json").read_text())
slides = "\n".join((root / "slides" / f"{sid}.html").read_text() for sid in deck["order"])
fonts = "\n".join(f'<link rel="stylesheet" href="{f["href"]}">' for f in deck["faces"].values() if "href" in f)
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b1512">
<title>{deck['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">{fonts}
<style>
*{{box-sizing:border-box;margin:0}}
html,body{{height:100%;background:#0b1512;overflow:hidden;overscroll-behavior:none}}
body{{touch-action:pinch-zoom;-webkit-user-select:none;user-select:none;cursor:grab}}
body.dragging{{cursor:grabbing}}
#view{{position:fixed;left:0;right:0;top:0;bottom:64px}}
#stage{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:center;will-change:transform}}
#stage.anim{{transition:transform .28s cubic-bezier(.2,.8,.2,1)}}
section{{position:absolute;inset:0;width:1920px;height:1080px;visibility:hidden;overflow:hidden;font-family:'IBM Plex Sans',Arial,sans-serif;color:#12241F}}
section.on{{visibility:visible}}
aside{{display:none}} ul,ol{{padding-left:1.2em}}
table{{border-collapse:collapse}} th,td{{padding:.35em .6em;border-bottom:1px solid rgba(128,128,128,.35);vertical-align:top}}
x-shape{{display:block}} x-shape[kind=ellipse]{{border-radius:50%}}
x-icon{{display:block}}
#bar{{position:fixed;left:0;right:0;bottom:0;height:64px;padding:0 12px env(safe-area-inset-bottom);display:flex;align-items:center;gap:12px;font:14px/1 Arial,sans-serif;color:#9FB0A8;cursor:default}}
#bar button{{flex:none;width:44px;height:44px;border-radius:22px;border:1px solid #2C4740;background:#12241F;color:#F5F1E8;font-size:20px;cursor:pointer;display:grid;place-items:center;touch-action:manipulation}}
#bar button:disabled{{opacity:.35;cursor:default}}
#bar button:hover:not(:disabled){{background:#1C3A32}}
#track{{flex:1;height:4px;border-radius:2px;background:#2C4740;overflow:hidden}}
#fill{{height:100%;background:#F08A4B;transition:width .28s}}
#n{{min-width:52px;text-align:center;font-variant-numeric:tabular-nums}}
#rot{{display:none}}
@media (orientation:portrait) and (max-width:700px){{#rot{{display:block;position:fixed;left:0;right:0;top:calc(50% - 32px + 28vw + 20px);text-align:center;color:#9FB0A8;font:14px Arial,sans-serif;pointer-events:none}}}}
#hint{{position:fixed;left:50%;bottom:76px;transform:translateX(-50%);padding:10px 16px;border-radius:20px;background:rgba(18,36,31,.92);color:#F5F1E8;font:14px Arial,sans-serif;pointer-events:none;transition:opacity .6s}}
@media print{{html,body{{overflow:visible;height:auto}} #view{{position:static}} #stage{{position:static;transform:none!important}} section{{visibility:visible!important;position:relative;page-break-after:always}} #bar,#hint{{display:none}}}}
</style></head><body>
<div id="view"><div id="stage">
{slides}
</div></div>
<div id="bar">
<button id="prev" aria-label="Previous slide">&#8249;</button>
<div id="track"><div id="fill"></div></div>
<span id="n"></span>
<button id="fs" aria-label="Full screen">&#x26F6;</button>
<button id="next" aria-label="Next slide">&#8250;</button>
</div>
<div id="rot">&#x21BB; Turn your phone sideways for a bigger view</div>
<div id="hint">Swipe or drag to change slides</div>
<script>
const s=[...document.querySelectorAll('#stage > section')],st=document.getElementById('stage'),view=document.getElementById('view');
let i=Math.max(0,Math.min(s.length-1,(parseInt(location.hash.slice(1))||1)-1)),k=1,dx=0;
function place(){{st.style.transform='translate(calc(-50% + '+dx+'px),-50%) scale('+k+')'}}
function fit(){{k=Math.min(view.clientWidth/1920,view.clientHeight/1080);place()}}
function show(){{s.forEach((e,j)=>e.classList.toggle('on',j===i));document.getElementById('n').textContent=(i+1)+' / '+s.length;
document.getElementById('fill').style.width=((i+1)/s.length*100)+'%';prev.disabled=i===0;next.disabled=i===s.length-1;history.replaceState(null,'','#'+(i+1))}}
function go(d){{const j=Math.max(0,Math.min(s.length-1,i+d));if(j!==i){{i=j;show()}}}}
prev.onclick=()=>go(-1);next.onclick=()=>go(1);
fs.onclick=()=>{{const d=document;if(d.fullscreenElement)d.exitFullscreen();else(d.documentElement.requestFullscreen||d.documentElement.webkitRequestFullscreen||(()=>{{}})).call(d.documentElement)}};
addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))go(1);else if(['ArrowLeft','PageUp'].includes(e.key))go(-1);else if(e.key==='f')fs.onclick()}});
// swipe (touch) and drag (mouse)
let x0=null,y0=0,t0=0,pid=null;
view.addEventListener('pointerdown',e=>{{if(!e.isPrimary)return;x0=e.clientX;y0=e.clientY;t0=Date.now();pid=e.pointerId;dx=0;st.classList.remove('anim');view.setPointerCapture(pid);document.body.classList.add('dragging')}});
view.addEventListener('pointermove',e=>{{if(x0===null||e.pointerId!==pid)return;dx=e.clientX-x0;if((i===0&&dx>0)||(i===s.length-1&&dx<0))dx/=3;place()}});
function end(e){{if(x0===null||e.pointerId!==pid)return;const d=e.clientX-x0,dy=Math.abs(e.clientY-y0),fast=Math.abs(d)>30&&Date.now()-t0<300;
st.classList.add('anim');dx=0;place();document.body.classList.remove('dragging');
if(Math.abs(d)>Math.max(50,view.clientWidth*0.12)||fast){{if(Math.abs(d)>dy)go(d<0?1:-1)}}
else if(Math.abs(d)<6&&dy<6&&e.pointerType!=='mouse'){{go(e.clientX>innerWidth/2?1:-1)}}
x0=null;pid=null;hint.style.opacity=0}}
view.addEventListener('pointerup',end);view.addEventListener('pointercancel',end);
addEventListener('resize',fit);
addEventListener('hashchange',()=>{{const n=parseInt(location.hash.slice(1));if(n>=1&&n<=s.length&&n-1!==i){{i=n-1;show()}}}});
setTimeout(()=>hint.style.opacity=0,3500);
fit();show();
</script></body></html>"""
(root / "index.html").write_text(html)
print("built index.html with", len(deck["order"]), "slides")
