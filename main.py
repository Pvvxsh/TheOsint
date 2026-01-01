import webview
import webbrowser
import requests


class Api:
    def open_url(self, url):
        try:
            webbrowser.open(url)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def ip_lookup(self, ip):
        url = f"http://ip-api.com/json/{ip}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=6)
            data = r.json()
            if data.get("status") != "success":
                return {"ok": False, "error": "IP not found"}
            return {"ok": True, "data": data}
        except Exception:
            return {"ok": False, "error": "Network error"}


HTML = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Osint</title>
<style>
:root{
  --bg:#000000;
  --ink:#07010a;
  --fog1:#140013;
  --fog2:#090010;

  --redDeep:#3b0508;
  --red:#7b0a12;
  --redHot:#b10d1a;

  --uiLine: rgba(255,255,255,0.14);
  --uiLine2: rgba(255,255,255,0.22);

  --uiText: rgba(255,255,255,0.92);
  --uiMuted: rgba(255,255,255,0.62);

  --panelA: rgba(10,0,12,0.62);
  --panelB: rgba(0,0,0,0.50);
  --panelC: rgba(0,0,0,0.35);
}

*{box-sizing:border-box}
html,body{
  height:100%;
  margin:0;
  overflow:hidden;
  background:var(--bg);
  color:var(--uiText);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "DejaVu Sans", sans-serif;
}

#wrap{position:fixed; inset:0}

#splash{
  position:absolute;
  inset:0;
  background:#000;
  z-index:50;
}
#c{
  display:block;
  width:100%;
  height:100%;
}
#overlay{
  position:absolute;
  inset:0;
  display:grid;
  place-items:center;
  pointer-events:none;
  isolation:isolate;
  z-index:60;
}
#title{
  position:relative;
  opacity:0;
  transform: translateY(18px) scale(0.975);
  text-align:center;
  letter-spacing:0.30em;
  text-transform:uppercase;
  font-weight:800;
  font-size: clamp(26px, 4.4vw, 64px);
  line-height:1.07;
  color: var(--red);
  text-shadow:
    0 2px 0 rgba(0,0,0,0.75),
    0 0 12px rgba(0,0,0,0.65),
    0 0 22px rgba(177,13,26,0.12),
    0 0 54px rgba(177,13,26,0.10);
  mix-blend-mode: screen;
  filter: saturate(1.08) contrast(1.08);
  animation: appear 1.9s cubic-bezier(.16,1,.18,1) 1s forwards;
  will-change: opacity, transform, filter;
}
#title span{display:block}
#title .top{
  font-size: 0.70em;
  color: var(--redDeep);
  letter-spacing:0.38em;
  text-shadow:
    0 2px 0 rgba(0,0,0,0.80),
    0 0 18px rgba(177,13,26,0.10);
  mix-blend-mode: screen;
}
#title .bot{
  margin-top: 12px;
  font-size: 1.0em;
  color: var(--redHot);
  text-shadow:
    0 2px 0 rgba(0,0,0,0.80),
    0 0 16px rgba(177,13,26,0.18),
    0 0 46px rgba(177,13,26,0.14),
    0 0 86px rgba(177,13,26,0.08);
}
#title::after{
  content:"";
  position:absolute;
  left:50%;
  top:50%;
  width:min(920px, 80vw);
  height:min(360px, 36vh);
  transform: translate(-50%,-50%);
  background:
    radial-gradient(closest-side at 50% 52%, rgba(177,13,26,0.12), rgba(177,13,26,0.0) 70%);
  filter: blur(18px);
  opacity:0.85;
  z-index:-1;
  mix-blend-mode: screen;
}
#splashFade{
  position:absolute;
  inset:0;
  opacity:0;
  pointer-events:none;
  background: radial-gradient(70% 70% at 50% 45%, rgba(177,13,26,0.10), rgba(0,0,0,0.92) 70%);
  animation: splashOut 1.0s cubic-bezier(.2,1,.2,1) 3.2s forwards;
  z-index:65;
}
@keyframes appear{
  0%{opacity:0;transform: translateY(22px) scale(0.97);filter: blur(10px) saturate(0.95) contrast(0.95);}
  40%{opacity:0.92;transform: translateY(1px) scale(1.008);filter: blur(1.6px) saturate(1.10) contrast(1.05);}
  70%{opacity:1;transform: translateY(-1px) scale(1.01);filter: blur(0px) saturate(1.12) contrast(1.08);}
  100%{opacity:1;transform: translateY(0px) scale(1.0);filter: blur(0px) saturate(1.10) contrast(1.08);}
}
@keyframes splashOut{0%{opacity:0}20%{opacity:1}100%{opacity:1}}

#app{
  position:absolute;
  inset:0;
  display:none;
  background:
    radial-gradient(90% 90% at 50% 0%, rgba(177,13,26,0.08), rgba(0,0,0,0) 55%),
    radial-gradient(120% 120% at 50% 60%, rgba(10,0,12,0.45), rgba(0,0,0,0.95) 70%),
    #000;
}
#app.show{
  display:flex;
  flex-direction:column;
}

.header{
  padding: 14px 18px 12px 18px;
  border-bottom: 1px solid var(--uiLine);
  display:flex;
  align-items:center;
  gap: 12px;
  background: linear-gradient(to bottom, rgba(10,0,12,0.72), rgba(0,0,0,0.52));
  box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

.title{
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 0.06em;
  margin-right: 18px;
  color: rgba(255,255,255,0.92);
  text-shadow: 0 2px 0 rgba(0,0,0,0.6);
  white-space:nowrap;
}
.title .n-letter{
  color: var(--redHot);
  text-shadow:
    0 0 10px rgba(177,13,26,0.55),
    0 0 20px rgba(177,13,26,0.30),
    0 0 40px rgba(177,13,26,0.20);
}

.channel{
  margin-left:auto;
  display:flex;
  align-items:center;
  gap: 10px;
  font-size: 12px;
  color: var(--uiMuted);
  letter-spacing: 0.08em;
  text-transform: none;
  white-space:nowrap;
}
.channel a{
  color: rgba(255,255,255,0.90);
  text-decoration:none;
  border-bottom: 1px solid rgba(177,13,26,0.45);
  padding-bottom: 2px;
}
.channel a:hover{
  color: rgba(255,255,255,1);
  border-bottom-color: rgba(177,13,26,0.85);
}

.toolbar{
  padding: 10px 18px 14px 18px;
  border-bottom: 1px solid var(--uiLine);
  display:flex;
  align-items:center;
  gap: 10px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.55), rgba(0,0,0,0.30));
}

.macbtn{
  padding: 9px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background:
    radial-gradient(120% 160% at 30% 20%, rgba(255,255,255,0.10), rgba(255,255,255,0.02) 55%, rgba(0,0,0,0.10)),
    linear-gradient(to bottom, rgba(20,0,22,0.55), rgba(0,0,0,0.35));
  color: rgba(255,255,255,0.90);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: none;
  cursor:pointer;
  box-shadow: 0 10px 18px rgba(0,0,0,0.25);
  transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}
.macbtn:hover{
  transform: translateY(-1px);
  border-color: rgba(177,13,26,0.55);
  background:
    radial-gradient(120% 160% at 30% 20%, rgba(177,13,26,0.10), rgba(255,255,255,0.02) 55%, rgba(0,0,0,0.10)),
    linear-gradient(to bottom, rgba(20,0,22,0.55), rgba(0,0,0,0.35));
}
.macbtn.active{
  border-color: rgba(177,13,26,0.85);
  box-shadow:
    0 0 0 1px rgba(177,13,26,0.20) inset,
    0 0 26px rgba(177,13,26,0.12),
    0 10px 18px rgba(0,0,0,0.25);
}

.form{
  margin-left:auto;
  display:flex;
  align-items:center;
  gap: 10px;
}
.form label{
  font-size: 12px;
  color: var(--uiMuted);
  letter-spacing: 0.08em;
  white-space:nowrap;
}
.form input{
  padding: 9px 10px;
  border: 1px solid rgba(255,255,255,0.22);
  background: rgba(0,0,0,0.50);
  color: rgba(255,255,255,0.92);
  width: 260px;
  font-size: 12px;
  outline:none;
  border-radius: 12px;
  box-shadow: 0 10px 18px rgba(0,0,0,0.25);
}
.form input:focus{
  border-color: rgba(177,13,26,0.65);
  box-shadow:
    0 0 0 3px rgba(177,13,26,0.18),
    0 10px 18px rgba(0,0,0,0.25);
}
.form button{
  padding: 9px 12px;
  border: 1px solid rgba(177,13,26,0.60);
  background: rgba(0,0,0,0.42);
  color: rgba(255,255,255,0.92);
  cursor:pointer;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.10em;
  border-radius: 12px;
  box-shadow: 0 10px 18px rgba(0,0,0,0.25);
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.form button:hover{
  background: rgba(177,13,26,0.10);
  border-color: rgba(177,13,26,0.85);
  transform: translateY(-1px);
}
.form button:active{transform: translateY(0px);}

#content-wrap{
  flex:1;
  display:flex;
  gap: 18px;
  padding: 18px;
  overflow:hidden;
}

.view-box{
  flex:1;
  border: 1px solid rgba(255,255,255,0.22);
  border-radius: 16px;
  padding: 14px;
  overflow:auto;
  position:relative;
  cursor:pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  background:
    radial-gradient(90% 90% at 30% 10%, rgba(177,13,26,0.06), rgba(0,0,0,0) 55%),
    linear-gradient(to bottom, rgba(10,0,12,0.55), rgba(0,0,0,0.40));
  box-shadow: 0 18px 40px rgba(0,0,0,0.35);
}

.view-box:hover{
  border-color: rgba(177,13,26,0.55);
  transform: translateY(-1px);
}

.view-box.active{
  border-color: rgba(177,13,26,0.80);
  box-shadow:
    0 0 0 1px rgba(177,13,26,0.25) inset,
    0 0 30px rgba(177,13,26,0.16),
    0 22px 50px rgba(0,0,0,0.38);
}

.view-title{
  position: sticky;
  top: 0;
  left: 0;
  width: fit-content;
  margin: 0 auto 10px auto;
  font-size: 12px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  background: rgba(0,0,0,0.55);
  padding: 6px 12px;
  border: 1px solid rgba(255,255,255,0.22);
  border-radius: 999px;
  z-index: 100;
  color: rgba(255,255,255,0.90);
  text-shadow: 0 2px 0 rgba(0,0,0,0.6);
}

svg{
  width:100%;
  height: calc(100% - 34px);
}

.node circle{
  fill: rgba(255,255,255,0.92);
  stroke: rgba(0,0,0,0.88);
  stroke-width: 2.5;
}
.center-node circle{
  fill: rgba(255,255,255,0.95);
  stroke: rgba(0,0,0,0.95);
  stroke-width: 3.5;
}
.category-node circle{
  fill: rgba(255,255,255,0.92);
  stroke: rgba(0,0,0,0.9);
  stroke-width: 3;
}
.link{
  stroke: rgba(255,255,255,0.70);
  stroke-width: 0.9;
  marker-end: url(#arrow);
}
.label-text{
  fill: rgba(255,255,255,0.88);
  font-size: 7px;
  text-anchor: middle;
}
foreignObject{pointer-events:none}
.fo-inner{
  width:100%;
  height:100%;
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 3px;
  box-sizing:border-box;
  text-align:center;
  font-size: 5px;
  line-height: 1.1;
  color: rgba(0,0,0,0.92);
  overflow:hidden;
  word-break: break-all;
}
.center-node .fo-inner{
  font-size: 10px;
  font-weight: 900;
}
.category-node .fo-inner{
  font-size: 7px;
  font-weight: 900;
}

#text-list{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "DejaVu Sans Mono", monospace;
  font-size: 11px;
  line-height: 1.8;
  margin-top: 10px;
  color: rgba(255,255,255,0.88);
}

#ip-visualization{
  width:100%;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-start;
  gap:0;
  margin-top: 10px;
}

.pyramid-level{
  display:flex;
  gap: 34px;
  align-items:center;
  justify-content:center;
  position:relative;
  width:100%;
  margin-bottom: 48px;
  flex-wrap:wrap;
}

.node-container{
  position:relative;
  display:flex;
  flex-direction:column;
  align-items:center;
}

.ipnode{
  width: 92px;
  height: 92px;
  border-radius: 50%;
  background: rgba(255,255,255,0.94);
  border: 2px solid rgba(0,0,0,0.92);
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 12px;
  text-align:center;
  font-size: 11px;
  font-weight: 900;
  word-break: break-word;
  box-shadow:
    0 10px 18px rgba(0,0,0,0.25),
    0 0 0 1px rgba(255,255,255,0.10) inset;
  position:relative;
  z-index:2;
  line-height:1.15;
  color: rgba(0,0,0,0.92);
}

.ipnode.main{
  width: 118px;
  height: 118px;
  background: rgba(0,0,0,0.92);
  color: rgba(255,255,255,0.92);
  font-size: 14px;
  border: 2px solid rgba(177,13,26,0.65);
  box-shadow:
    0 0 26px rgba(177,13,26,0.14),
    0 14px 28px rgba(0,0,0,0.35);
}

.connector-down{
  position:absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 48px;
  background: rgba(255,255,255,0.62);
  z-index:1;
}

.error-msg{
  font-size: 13px;
  color: rgba(255,90,90,0.92);
  font-weight: 900;
  letter-spacing: 0.06em;
}

.loading-msg{
  font-size: 13px;
  color: rgba(255,255,255,0.82);
  font-weight: 900;
  letter-spacing: 0.06em;
}
</style>
</head>
<body>
<div id="wrap">
  <div id="splash">
    <canvas id="c"></canvas>
    <div id="overlay">
      <div id="title">
        <span class="top">WELCOME TO</span>
        <span class="bot">THE OSINT</span>
      </div>
    </div>
    <div id="splashFade"></div>
  </div>

  <div id="app">
    <div class="header">
      <div class="title"><span class="n-letter">T</span>he Osint</div>
      <div class="channel">
        <span>Channel</span>
        <a href="#" onclick="openChannel(event)"></a>
      </div>
    </div>

    <div class="toolbar">
      <button class="macbtn active" id="btnNick" onclick="setMode('nick')">Search Nick</button>
      <button class="macbtn" id="btnIP" onclick="setMode('ip')">Search IP</button>
      <button class="macbtn" id="btnMail" onclick="setMode('mail')">Search Mail</button>

      <div class="form">
        <label id="inputLabel" for="q">enter nickname -></label>
        <input id="q" type="text" placeholder="nickname">
        <button onclick="runSearch()">search</button>
      </div>
    </div>

    <div id="content-wrap">
      <div class="view-box active" id="circles-box" onclick="showCircles()">
        <div class="view-title" id="leftTitle">Circles</div>
        <svg id="canvas"></svg>
        <div id="ip-visualization" style="display:none"></div>
      </div>
      <div class="view-box" id="text-box" onclick="showText()">
        <div class="view-title" id="rightTitle">InText</div>
        <div id="text-list"></div>
      </div>
    </div>
  </div>
</div>

<script>
const splashDurationMs = 3600

setTimeout(() => {
  const splash = document.getElementById('splash')
  const app = document.getElementById('app')
  splash.style.display = 'none'
  app.classList.add('show')
  window.dispatchEvent(new Event('resize'))
}, splashDurationMs)

function openChannel(e){
  e.preventDefault()
  if(window.pywebview && window.pywebview.api){
    window.pywebview.api.open_url('https://t.me/noxsangchannel')
  }
}

const canvas = document.getElementById('c')
const ctx = canvas.getContext('2d')

let W = 0, H = 0, DPR = 1
function resize(){
  DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1))
  W = Math.floor(window.innerWidth)
  H = Math.floor(window.innerHeight)
  canvas.width = Math.floor(W * DPR)
  canvas.height = Math.floor(H * DPR)
  canvas.style.width = W + 'px'
  canvas.style.height = H + 'px'
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0)
}
window.addEventListener('resize', resize)
resize()

const cx = () => W * 0.5
const cy = () => H * 0.5
function rnd(a,b){ return a + Math.random() * (b-a) }

const STAR_COUNT = 980
const stars = []

function resetStar(s, near){
  s.x = rnd(-W, W)
  s.y = rnd(-H, H)
  s.z = near ? rnd(0.2, 1.0) : rnd(0.02, 1.0)
  s.sz = rnd(0.55, 1.9)
  s.tint = rnd(0, 1)
}

for(let i=0;i<STAR_COUNT;i++){
  const s = {}
  resetStar(s, false)
  stars.push(s)
}

let tPrev = 0
let speed = 0.115
let driftX = 0.00055
let driftY = -0.00032

function drawBackground(){
  ctx.fillStyle = '#000'
  ctx.fillRect(0,0,W,H)

  const g1 = ctx.createRadialGradient(cx(), cy()*0.92, Math.min(W,H)*0.05, cx(), cy()*0.92, Math.max(W,H)*0.86)
  g1.addColorStop(0, 'rgba(20,0,19,0.10)')
  g1.addColorStop(0.40, 'rgba(10,0,16,0.30)')
  g1.addColorStop(1, 'rgba(0,0,0,0.95)')
  ctx.fillStyle = g1
  ctx.fillRect(0,0,W,H)

  const g2 = ctx.createRadialGradient(cx()*0.92, cy()*0.86, 0, cx()*0.92, cy()*0.86, Math.max(W,H)*0.55)
  g2.addColorStop(0, 'rgba(177,13,26,0.06)')
  g2.addColorStop(0.35, 'rgba(177,13,26,0.03)')
  g2.addColorStop(1, 'rgba(177,13,26,0)')
  ctx.fillStyle = g2
  ctx.fillRect(0,0,W,H)
}

function drawVignette(){
  const g = ctx.createRadialGradient(cx(), cy(), Math.min(W,H)*0.06, cx(), cy(), Math.max(W,H)*0.62)
  g.addColorStop(0, 'rgba(0,0,0,0)')
  g.addColorStop(0.55, 'rgba(0,0,0,0.12)')
  g.addColorStop(1, 'rgba(0,0,0,0.78)')
  ctx.fillStyle = g
  ctx.fillRect(0,0,W,H)
}

function starColor(glow){
  const a = 0.10 + glow * 0.82
  if(glow > 0.74){
    return `rgba(255,210,150,${a})`
  }
  return `rgba(245,245,255,${a})`
}

function animate(ts){
  const dt = Math.min(40, ts - tPrev || 16.67)
  tPrev = ts

  drawBackground()

  const centerX = cx()
  const centerY = cy()

  const accel = 0.0008 * dt
  speed += (0.115 - speed) * accel
  driftX += (0.00055 - driftX) * accel
  driftY += (-0.00032 - driftY) * accel

  for(let i=0;i<stars.length;i++){
    const s = stars[i]
    const ox = s.x
    const oy = s.y

    s.z -= speed * (0.0017 + s.z * 0.010) * dt
    s.x += driftX * dt * (0.8 + s.z * 2.0) * 60
    s.y += driftY * dt * (0.8 + s.z * 2.0) * 60

    if(s.z <= 0.02){
      resetStar(s, true)
      s.z = 1.0
    }

    const depth2 = 1.0 / (s.z * 0.92 + 0.08)
    const x2 = centerX + s.x * depth2
    const y2 = centerY + s.y * depth2

    const depth1 = 1.0 / ((s.z + 0.06) * 1.1)
    const x1 = centerX + ox * depth1
    const y1 = centerY + oy * depth1

    if(x2 < -80 || x2 > W+80 || y2 < -80 || y2 > H+80){
      resetStar(s, false)
      continue
    }

    const glow = Math.max(0, Math.min(1, (1.15 - s.z) * 0.95))
    const w = s.sz * (0.55 + glow * 2.4)

    ctx.lineWidth = w
    ctx.strokeStyle = starColor(glow)
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()

    const r = (0.55 + glow * 1.85) * s.sz
    const a2 = 0.07 + glow * 0.52
    ctx.fillStyle = `rgba(255,255,255,${a2})`
    ctx.beginPath()
    ctx.arc(x2, y2, r, 0, Math.PI*2)
    ctx.fill()

    if(glow > 0.72){
      const rg = ctx.createRadialGradient(x2, y2, 0, x2, y2, 10 + glow*22)
      rg.addColorStop(0, `rgba(255,190,130,${0.10*glow})`)
      rg.addColorStop(0.35, `rgba(255,70,30,${0.05*glow})`)
      rg.addColorStop(1, 'rgba(255,70,30,0)')
      ctx.fillStyle = rg
      ctx.beginPath()
      ctx.arc(x2, y2, 14 + glow*20, 0, Math.PI*2)
      ctx.fill()
    }
  }

  drawVignette()
  requestAnimationFrame(animate)
}
requestAnimationFrame(animate)

const categories = [
  { label: "Email", children: [
    {label:"Gmail", tpl:"{n}@gmail.com"},
    {label:"ProtonMail", tpl:"{n}@protonmail.com"},
    {label:"Yahoo", tpl:"{n}@yahoo.com"},
    {label:"Outlook", tpl:"{n}@outlook.com"}
  ]},
  { label: "Email RU", children: [
    {label:"Mail.ru", tpl:"{n}@mail.ru"},
    {label:"Yandex", tpl:"{n}@yandex.ru"},
    {label:"BK.ru", tpl:"{n}@bk.ru"}
  ]},
  { label: "Domains", children: [
    {label:".com", tpl:"{n}.com"},
    {label:".ru", tpl:"{n}.ru"},
    {label:".org", tpl:"{n}.org"},
    {label:".net", tpl:"{n}.net"}
  ]},
  { label: "Social", children: [
    {label:"Instagram", tpl:"instagram.com/{n}"},
    {label:"Twitter", tpl:"twitter.com/{n}"},
    {label:"Facebook", tpl:"facebook.com/{n}"},
    {label:"VK", tpl:"vk.com/{n}"},
    {label:"Reddit", tpl:"reddit.com/u/{n}"}
  ]},
  { label: "Messengers", children: [
    {label:"Telegram", tpl:"t.me/{n}"},
    {label:"TikTok", tpl:"tiktok.com/@{n}"}
  ]},
  { label: "Dev & Media", children: [
    {label:"GitHub", tpl:"github.com/{n}"},
    {label:"YouTube", tpl:"youtube.com/@{n}"},
    {label:"Twitch", tpl:"twitch.tv/{n}"},
    {label:"Steam", tpl:"steamcommunity.com/id/{n}"}
  ]}
]

let currentNick = ""
let mode = "nick"

function setMode(m){
  mode = m
  document.getElementById('btnNick').classList.toggle('active', m === 'nick')
  document.getElementById('btnIP').classList.toggle('active', m === 'ip')
  document.getElementById('btnMail').classList.toggle('active', m === 'mail')

  const label = document.getElementById('inputLabel')
  const input = document.getElementById('q')
  const leftTitle = document.getElementById('leftTitle')
  const rightTitle = document.getElementById('rightTitle')

  if(m === 'ip'){
    label.textContent = 'enter ip ->'
    input.placeholder = '8.8.8.8'
    leftTitle.textContent = 'IP'
    rightTitle.textContent = 'InText'
  } else if(m === 'mail'){
    label.textContent = 'enter mail ->'
    input.placeholder = 'durov@mail.ru'
    leftTitle.textContent = 'Circles'
    rightTitle.textContent = 'InText'
  } else {
    label.textContent = 'enter nickname ->'
    input.placeholder = 'nickname'
    leftTitle.textContent = 'Circles'
    rightTitle.textContent = 'InText'
  }
}

function showCircles(){
  document.getElementById('circles-box').classList.add('active')
  document.getElementById('text-box').classList.remove('active')
}

function showText(){
  document.getElementById('circles-box').classList.remove('active')
  document.getElementById('text-box').classList.add('active')
}

function getNickFromMail(s){
  const t = (s || '').trim()
  const at = t.indexOf('@')
  if(at > 0) return t.slice(0, at)
  return t
}

function runSearch(){
  const q = document.getElementById('q').value.trim()
  if(mode === 'ip'){
    searchIP(q)
  } else if(mode === 'mail'){
    currentNick = getNickFromMail(q) || 'nickname'
    showNickPanels()
    drawCircles()
    drawText()
  } else {
    currentNick = q || 'nickname'
    showNickPanels()
    drawCircles()
    drawText()
  }
}

function showNickPanels(){
  document.getElementById('canvas').style.display = 'block'
  document.getElementById('ip-visualization').style.display = 'none'
}

function showIPPanels(){
  document.getElementById('canvas').style.display = 'none'
  document.getElementById('ip-visualization').style.display = 'flex'
}

function drawCircles(){
  const nick = currentNick
  const svg = document.getElementById('canvas')
  svg.innerHTML = ""

  const w = svg.clientWidth || svg.parentElement.clientWidth
  const h = svg.clientHeight || svg.parentElement.clientHeight

  const defs = document.createElementNS("http://www.w3.org/2000/svg","defs")
  const marker = document.createElementNS("http://www.w3.org/2000/svg","marker")
  marker.setAttribute("id","arrow")
  marker.setAttribute("markerWidth","5")
  marker.setAttribute("markerHeight","5")
  marker.setAttribute("refX","4")
  marker.setAttribute("refY","2.5")
  marker.setAttribute("orient","auto")
  const path = document.createElementNS("http://www.w3.org/2000/svg","path")
  path.setAttribute("d","M0,0 L5,2.5 L0,5 Z")
  path.setAttribute("fill","rgba(255,255,255,0.75)")
  marker.appendChild(path)
  defs.appendChild(marker)
  svg.appendChild(defs)

  const cx0 = w / 2
  const cy0 = h / 2
  const centerR = 35
  const categoryR = 25
  const childR = 16

  const linesGroup = document.createElementNS("http://www.w3.org/2000/svg","g")
  svg.appendChild(linesGroup)

  const nodesGroup = document.createElementNS("http://www.w3.org/2000/svg","g")
  svg.appendChild(nodesGroup)

  const categoryRadius = Math.min(w, h) * 0.28
  const childRadius = 90

  categories.forEach((cat, catIndex) => {
    const catAngle = (2 * Math.PI * catIndex) / categories.length - Math.PI / 2
    const catX = cx0 + categoryRadius * Math.cos(catAngle)
    const catY = cy0 + categoryRadius * Math.sin(catAngle)

    const line1 = document.createElementNS("http://www.w3.org/2000/svg","line")
    line1.setAttribute("class","link")
    line1.setAttribute("x1", cx0)
    line1.setAttribute("y1", cy0)
    line1.setAttribute("x2", catX - categoryR * Math.cos(catAngle) * 0.8)
    line1.setAttribute("y2", catY - categoryR * Math.sin(catAngle) * 0.8)
    linesGroup.appendChild(line1)

    const catGroup = document.createElementNS("http://www.w3.org/2000/svg","g")
    catGroup.setAttribute("class","node category-node")
    const catCircle = document.createElementNS("http://www.w3.org/2000/svg","circle")
    catCircle.setAttribute("cx", catX)
    catCircle.setAttribute("cy", catY)
    catCircle.setAttribute("r", categoryR)
    catGroup.appendChild(catCircle)

    const catFO = document.createElementNS("http://www.w3.org/2000/svg","foreignObject")
    catFO.setAttribute("x", catX - categoryR)
    catFO.setAttribute("y", catY - categoryR)
    catFO.setAttribute("width", categoryR*2)
    catFO.setAttribute("height", categoryR*2)
    const catDiv = document.createElement("div")
    catDiv.className = "fo-inner"
    catDiv.textContent = cat.label
    catFO.appendChild(catDiv)
    catGroup.appendChild(catFO)
    nodesGroup.appendChild(catGroup)

    const childCount = cat.children.length
    const angleSpread = Math.PI / 2.5
    const startAngle = catAngle - angleSpread / 2

    cat.children.forEach((child, childIndex) => {
      const childAngle = startAngle + (childIndex / (childCount - 1 || 1)) * angleSpread
      const childX = catX + childRadius * Math.cos(childAngle)
      const childY = catY + childRadius * Math.sin(childAngle)

      const line2 = document.createElementNS("http://www.w3.org/2000/svg","line")
      line2.setAttribute("class","link")
      line2.setAttribute("x1", catX)
      line2.setAttribute("y1", catY)
      line2.setAttribute("x2", childX - childR * Math.cos(childAngle) * 0.8)
      line2.setAttribute("y2", childY - childR * Math.sin(childAngle) * 0.8)
      linesGroup.appendChild(line2)

      const childGroup = document.createElementNS("http://www.w3.org/2000/svg","g")
      childGroup.setAttribute("class","node")
      const childCircle = document.createElementNS("http://www.w3.org/2000/svg","circle")
      childCircle.setAttribute("cx", childX)
      childCircle.setAttribute("cy", childY)
      childCircle.setAttribute("r", childR)
      childGroup.appendChild(childCircle)

      const val = child.tpl.replace("{n}", nick)
      const childFO = document.createElementNS("http://www.w3.org/2000/svg","foreignObject")
      childFO.setAttribute("x", childX - childR)
      childFO.setAttribute("y", childY - childR)
      childFO.setAttribute("width", childR*2)
      childFO.setAttribute("height", childR*2)
      const childDiv = document.createElement("div")
      childDiv.className = "fo-inner"
      childDiv.textContent = val
      childFO.appendChild(childDiv)
      childGroup.appendChild(childFO)
      nodesGroup.appendChild(childGroup)

      const labelText = document.createElementNS("http://www.w3.org/2000/svg","text")
      labelText.setAttribute("class","label-text")
      labelText.setAttribute("x", childX)
      labelText.setAttribute("y", childY + childR + 9)
      labelText.setAttribute("text-anchor","middle")
      labelText.textContent = child.label
      nodesGroup.appendChild(labelText)
    })
  })

  const centerGroup = document.createElementNS("http://www.w3.org/2000/svg","g")
  centerGroup.setAttribute("class","node center-node")
  const cCircle = document.createElementNS("http://www.w3.org/2000/svg","circle")
  cCircle.setAttribute("cx", cx0)
  cCircle.setAttribute("cy", cy0)
  cCircle.setAttribute("r", centerR)
  centerGroup.appendChild(cCircle)

  const cFO = document.createElementNS("http://www.w3.org/2000/svg","foreignObject")
  cFO.setAttribute("x", cx0 - centerR)
  cFO.setAttribute("y", cy0 - centerR)
  cFO.setAttribute("width", centerR*2)
  cFO.setAttribute("height", centerR*2)
  const cDiv = document.createElement("div")
  cDiv.className = "fo-inner"
  cDiv.textContent = nick
  cFO.appendChild(cDiv)
  centerGroup.appendChild(cFO)
  nodesGroup.appendChild(centerGroup)
}

function drawText(){
  const nick = currentNick
  const list = document.getElementById('text-list')
  list.innerHTML = ""

  categories.forEach(cat => {
    const header = document.createElement("div")
    header.style.fontWeight = "800"
    header.style.marginTop = "10px"
    header.style.color = "rgba(177,13,26,0.92)"
    header.style.textShadow = "0 2px 0 rgba(0,0,0,0.55)"
    header.textContent = cat.label + ":"
    list.appendChild(header)

    cat.children.forEach(child => {
      const val = child.tpl.replace("{n}", nick)
      const line = document.createElement("div")
      line.textContent = "  " + val
      list.appendChild(line)
    })
  })
}

async function searchIP(ip){
  const viz = document.getElementById('ip-visualization')
  showIPPanels()

  const ipTrim = (ip || '').trim()
  if(!ipTrim){
    viz.innerHTML = '<div class="error-msg">Enter IP</div>'
    return
  }

  viz.innerHTML = '<div class="loading-msg">Loading data...</div>'

  try{
    if(!(window.pywebview && window.pywebview.api && window.pywebview.api.ip_lookup)){
      viz.innerHTML = '<div class="error-msg">API not ready</div>'
      return
    }

    const resp = await window.pywebview.api.ip_lookup(ipTrim)
    if(!resp || !resp.ok){
      viz.innerHTML = '<div class="error-msg">' + ((resp && resp.error) ? resp.error : 'IP not found') + '</div>'
      return
    }

    const data = resp.data || {}
    renderIP(data)
  }catch(e){
    viz.innerHTML = '<div class="error-msg">Network error</div>'
  }
}

function renderIP(result){
  const viz = document.getElementById('ip-visualization')
  viz.innerHTML = ''

  const status = result.status || 'N/A'
  const query = result.query || 'N/A'
  const org = result.org || 'N/A'
  const isp = result.isp || 'N/A'
  const country = result.country || 'N/A'
  const countryCode = result.countryCode || 'N/A'
  const city = result.city || 'N/A'
  const region = result.region || 'N/A'
  const regionName = result.regionName || 'N/A'
  const timezone = result.timezone || 'N/A'
  const lat = (result.lat !== undefined && result.lat !== null) ? result.lat : 'N/A'
  const lon = (result.lon !== undefined && result.lon !== null) ? result.lon : 'N/A'
  const asname = result.asname || 'N/A'
  const mobile = !!result.mobile
  const proxy = !!result.proxy
  const hosting = !!result.hosting
  const vpn = !!result.vpn
  const currency = result.currency || 'N/A'

  const payload = {
    main: query,
    level1: [
      String(org).slice(0,25),
      String(country)
    ],
    level2: [
      String(city),
      String(region),
      String(regionName),
      String(timezone)
    ],
    level3: [
      'Lat: ' + lat,
      'Lon: ' + lon,
      String(asname).slice(0,22),
      'Code: ' + String(countryCode),
      'ISP: ' + String(isp).slice(0,20)
    ],
    level4: [
      'Mobile: ' + mobile,
      'Proxy: ' + proxy,
      'VPN: ' + vpn,
      'Host: ' + hosting,
      'Curr: ' + String(currency)
    ]
  }

  const makeNode = (text, cls, down) => {
    const d = document.createElement('div')
    d.className = 'node-container'
    const n = document.createElement('div')
    n.className = 'ipnode' + (cls ? ' ' + cls : '')
    n.textContent = text
    d.appendChild(n)
    if(down){
      const c = document.createElement('div')
      c.className = 'connector-down'
      d.appendChild(c)
    }
    return d
  }

  const lvl0 = document.createElement('div')
  lvl0.className = 'pyramid-level'
  lvl0.appendChild(makeNode(payload.main, 'main', true))
  viz.appendChild(lvl0)

  const lvl1 = document.createElement('div')
  lvl1.className = 'pyramid-level'
  payload.level1.forEach((t) => lvl1.appendChild(makeNode(t, '', true)))
  viz.appendChild(lvl1)

  const lvl2 = document.createElement('div')
  lvl2.className = 'pyramid-level'
  payload.level2.forEach((t) => lvl2.appendChild(makeNode(t, '', true)))
  viz.appendChild(lvl2)

  const lvl3 = document.createElement('div')
  lvl3.className = 'pyramid-level'
  payload.level3.forEach((t) => lvl3.appendChild(makeNode(t, '', true)))
  viz.appendChild(lvl3)

  const lvl4 = document.createElement('div')
  lvl4.className = 'pyramid-level'
  payload.level4.forEach((t) => lvl4.appendChild(makeNode(t, '', false)))
  viz.appendChild(lvl4)

  const badge = document.createElement('div')
  badge.style.marginTop = '8px'
  badge.style.fontSize = '12px'
  badge.style.color = 'rgba(255,255,255,0.62)'
  badge.style.letterSpacing = '0.06em'
  badge.textContent = 'status: ' + status
  viz.appendChild(badge)
}

document.getElementById('q').addEventListener('keypress', function(ev){
  if(ev.key === 'Enter') runSearch()
})

window.addEventListener('load', () => {
  currentNick = 'nickname'
  drawCircles()
  drawText()
})
</script>
</body>
</html>
"""

if __name__ == "__main__":
    window = webview.create_window(
        "The Osint",
        html=HTML,
        width=1300,
        height=800,
        resizable=True,
        js_api=Api()
    )
    webview.start()
