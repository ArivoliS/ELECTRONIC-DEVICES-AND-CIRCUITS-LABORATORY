"""Interactive terminal wiring trainer. Expected electrical nets, not wire order, are checked."""
import json
import streamlit.components.v1 as components

def part(name,pins):return (name,pins)
CIRCUITS = [
('DC maximum power transfer',[part('DC source',['+','−']),part('Rth',['1','2']),part('RL',['1','2'])],[['DC source.+','Rth.1'],['Rth.2','RL.1'],['RL.2','DC source.−']]),
('Series RLC',[part('Isolated AC',['+','−']),part('R',['1','2']),part('L',['1','2']),part('C',['1','2'])],[['Isolated AC.+','R.1'],['R.2','L.1'],['L.2','C.1'],['C.2','Isolated AC.−']]),
('Series resonance',[part('Isolated AC',['+','−']),part('R',['1','2']),part('L',['1','2']),part('C',['1','2'])],[['Isolated AC.+','R.1'],['R.2','L.1'],['L.2','C.1'],['C.2','Isolated AC.−']]),
('RC charging',[part('DC source',['+','−']),part('Switch',['1','2']),part('R',['1','2']),part('C',['+','−'])],[['DC source.+','Switch.1'],['Switch.2','R.1'],['R.2','C.+'],['C.−','DC source.−']]),
('PN diode forward bias',[part('DC source',['+','−']),part('R limit',['1','2']),part('Diode',['A','K'])],[['DC source.+','R limit.1'],['R limit.2','Diode.A'],['Diode.K','DC source.−']]),
('Half-wave rectifier',[part('Isolated AC',['a','b']),part('D1',['A','K']),part('RL',['+','−']),part('C filter',['+','−'])],[['Isolated AC.a','D1.A'],['D1.K','RL.+','C filter.+'],['Isolated AC.b','RL.−','C filter.−']]),
('BJT common-emitter characteristics',[part('Base DC',['+','−']),part('RB',['1','2']),part('Collector DC',['+','−']),part('RC limit',['1','2']),part('NPN',['B','C','E'])],[['Base DC.+','RB.1'],['RB.2','NPN.B'],['Collector DC.+','RC limit.1'],['RC limit.2','NPN.C'],['Base DC.−','Collector DC.−','NPN.E']]),
('CE amplifier, emitter unbypassed',[part('VCC',['+','−']),part('R1',['1','2']),part('R2',['1','2']),part('RC',['1','2']),part('RE',['1','2']),part('NPN',['B','C','E']),part('Input AC',['+','−']),part('Cin',['1','2']),part('Cout',['1','2']),part('RL',['1','2'])],[['VCC.+','R1.1','RC.1'],['R1.2','R2.1','NPN.B','Cin.2'],['RC.2','NPN.C','Cout.1'],['NPN.E','RE.1'],['Input AC.+','Cin.1'],['Cout.2','RL.1'],['VCC.−','R2.2','RE.2','Input AC.−','RL.2']]),
('BJT RC phase-shift oscillator',[part('VCC',['+','−']),part('R1',['1','2']),part('R2',['1','2']),part('RC',['1','2']),part('RE',['1','2']),part('CE bypass',['+','−']),part('NPN',['B','C','E']),part('C1',['1','2']),part('C2',['1','2']),part('C3',['1','2']),part('Rf1',['1','2']),part('Rf2',['1','2'])],[['VCC.+','R1.1','RC.1'],['RC.2','NPN.C','C1.1'],['C1.2','Rf1.1','C2.1'],['C2.2','Rf2.1','C3.1'],['C3.2','NPN.B','R1.2','R2.1'],['NPN.E','RE.1','CE bypass.+'],['VCC.−','R2.2','RE.2','CE bypass.−','Rf1.2','Rf2.2']]),
('N-channel JFET switch',[part('Drain DC',['+','−']),part('RD',['1','2']),part('JFET',['G','D','S']),part('Gate DC',['+','−'])],[['Drain DC.+','RD.1'],['RD.2','JFET.D'],['JFET.S','Drain DC.−','Gate DC.+'],['JFET.G','Gate DC.−']])
]
DIODE_REVERSE=('PN reverse / Zener breakdown',[part('DC source',['+','−']),part('R limit',['1','2']),part('Diode',['A','K'])],[['DC source.+','R limit.1'],['R limit.2','Diode.K'],['Diode.A','DC source.−']])
BRIDGE=('Bridge rectifier with filter',[part('Isolated AC',['a','b']),part('D1',['A','K']),part('D2',['A','K']),part('D3',['A','K']),part('D4',['A','K']),part('RL',['+','−']),part('C filter',['+','−'])],[['Isolated AC.a','D1.A','D3.K'],['Isolated AC.b','D2.A','D4.K'],['D1.K','D2.K','RL.+','C filter.+'],['D3.A','D4.A','RL.−','C filter.−']])
DISCHARGE=('RC discharging (supply disconnected)',[part('C initially charged',['+','−']),part('Switch',['1','2']),part('R',['1','2'])],[['C initially charged.+','Switch.1'],['Switch.2','R.1'],['R.2','C initially charged.−']])
PARALLEL=('Parallel RLC (supplementary)',[part('Isolated AC',['+','−']),part('R',['1','2']),part('L',['1','2']),part('C',['1','2'])],[['Isolated AC.+','R.1','L.1','C.1'],['Isolated AC.−','R.2','L.2','C.2']])

def show_circuit(idx,variant='Standard'):
    config=CIRCUITS[idx]
    if idx==4 and variant!='Standard':config=DIODE_REVERSE
    if idx==5 and variant!='Standard':config=BRIDGE
    if idx==3 and variant!='Standard':config=DISCHARGE
    if idx==1 and variant!='Standard':config=PARALLEL
    title,parts,nets=config
    data=json.dumps({'title':title,'parts':parts,'nets':nets})
    page='''<!doctype html><html><head><meta charset="utf-8"><style>
body{font:15px Arial;color:#18314b;margin:8px}button{padding:10px 14px;margin:4px;border:1px solid #9db0c4;border-radius:7px;background:#eef5fa;cursor:pointer}svg{background:#f3f7fc;border:1px solid #c8d6e5;border-radius:12px;width:100%}.terminal{cursor:pointer}.status{padding:12px;background:#e8eef6;border-radius:7px}p{line-height:1.5}</style></head><body>
<h3 id="title"></h3><p>Click a terminal, then another terminal to add a wire. Join every terminal belonging to the same electrical node. Use <b>Check connections</b> before switching on. Crossings do not join unless they share a terminal.</p>
<button onclick="check()">Check connections</button><button onclick="power()">Power ON / OFF</button><button onclick="undo()">Undo wire</button><button onclick="reset()">Clear all</button><button onclick="guide=!guide;draw()">Show / hide reference connections</button>
<p class="status" id="status">Supply OFF · Build the circuit.</p><div style="overflow:auto"><svg id="board" viewBox="0 0 1000 700" role="img" aria-label="Interactive circuit connection board"></svg></div>
<p>Connection trainer only: blocks identify components and their terminals. Wire routing is schematic, not a physical breadboard layout. Correct connectivity does not verify component values, device ratings, bias or oscillation. The Simulator tab performs the numerical model separately.</p>
<script>const cfg=DATA;const svg=document.getElementById('board');document.getElementById('title').textContent=cfg.title;
let wires=[],selected=null,on=false,guide=false;let pins={};
const NS='http://www.w3.org/2000/svg';function el(tag,attrs,text){let e=document.createElementNS(NS,tag);for(let k in attrs)e.setAttribute(k,attrs[k]);if(text)e.textContent=text;svg.appendChild(e);return e;}
function msg(s){document.getElementById('status').textContent=s;}
function clickPin(id){if(on){msg('Switch OFF before changing connections.');return;}if(selected===null)selected=id;else{if(selected!==id&&!wires.some(w=>w.includes(selected)&&w.includes(id)))wires.push([selected,id]);selected=null;}draw();}
function draw(){svg.innerHTML='';pins={};const cols=4;cfg.parts.forEach((p,i)=>{let x=40+(i%cols)*245,y=55+Math.floor(i/cols)*210;el('rect',{x,y,width:190,height:95,rx:12,fill:'#fff',stroke:'#748ca5','stroke-width':2});el('text',{x:x+95,y:y+32,'text-anchor':'middle','font-weight':'bold'},p[0]);p[1].forEach((label,j)=>{let px=x+25+j*(140/Math.max(p[1].length-1,1)),py=y+95;let id=p[0]+'.'+label;pins[id]=[px,py];el('text',{x:px,y:y+73,'text-anchor':'middle'},label);});});
function line(a,b,color,dash){const u=pins[a],v=pins[b];el('line',{x1:u[0],y1:u[1],x2:v[0],y2:v[1],stroke:color,'stroke-width':3,'stroke-dasharray':dash||'','pointer-events':'none'});}
if(guide)cfg.nets.forEach(net=>{for(let i=1;i<net.length;i++)line(net[0],net[i],'#c7861a','7 6');});wires.forEach(w=>line(w[0],w[1],on?'#09864f':'#1769c2'));
Object.entries(pins).forEach(([id,p])=>{let e=el('circle',{cx:p[0],cy:p[1],r:9,fill:selected===id?'#ffb020':'#fff',stroke:'#164b7a','stroke-width':3,class:'terminal',tabindex:0,role:'button','aria-label':id});e.onclick=()=>clickPin(id);e.onkeydown=ev=>{if(ev.key==='Enter'||ev.key===' ')clickPin(id);};el('title',{},'');});}
function assess(){let parent={};Object.keys(pins).forEach(p=>parent[p]=p);function find(a){return parent[a]===a?a:parent[a]=find(parent[a]);}wires.forEach(([a,b])=>parent[find(a)]=find(b));let expected={};cfg.nets.forEach((net,i)=>net.forEach(p=>expected[p]=i));let groups={};for(let p in parent){let r=find(p);if(!groups[r])groups[r]=new Set();groups[r].add(expected[p]);}if(Object.values(groups).some(g=>g.size>1))return 'Incorrect: a wire joins terminals from different electrical nodes. Undo it and check the reference.';if(cfg.nets.some(net=>net.some(p=>find(p)!==find(net[0]))))return 'Incomplete: one or more required node connections are missing.';return '';}
function check(){let error=assess();msg(error||'Connections correct. You may switch the virtual supply ON.');return !error;}
function power(){if(on){on=false;msg('Supply OFF.');draw();}else if(check()){on=true;msg('Virtual supply ON · connectivity verified. Open Simulator for calculated waveforms.');draw();}}
function undo(){if(on){msg('Switch OFF before rewiring.');return;}wires.pop();selected=null;draw();}
function reset(){on=false;wires=[];selected=null;msg('Supply OFF · all wires cleared.');draw();}draw();
</script></body></html>'''.replace('DATA',data)
    components.html(page,height=1040,scrolling=True)
