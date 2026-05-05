# -*- coding: utf-8 -*-
"""用Python验证JS语法 - 逐步合并"""

with open('c:/Users/chenx/WorkBuddy/Claw/v7_good_backup.html', 'r', encoding='utf-8') as f:
    v7 = f.read()

# 从之前生成的index.html中提取NOTES_DB
with open('c:/Users/chenx/WorkBuddy/Claw/index.html', 'r', encoding='utf-8') as f:
    full = f.read()

start = full.find('const NOTES_DB={')
end = full.find('\nfunction notesGetTotal', start)
NOTES_DB_STR = full[start:end].rstrip()
# 确保以};结尾
if not NOTES_DB_STR.endswith('};'):
    NOTES_DB_STR += '\n};'

print(f'NOTES_DB extracted: {len(NOTES_DB_STR)} chars')

# 用Python写一个测试HTML，让浏览器自己报错
# Step 1: V7 + 空 function (已知OK)
# Step 2: V7 + CSS + HTML + button + 函数(不含DB) 
# Step 3: V7 + CSS + HTML + button + 函数 + DB

# 构建 step 2: 只有函数，DB设为空对象
NOTES_FUNCS_NO_DB = """
// ── Notes Sub-page Functions ──
const NOTES_COLORS={"政治":"#e74c3c","经济":"#f39c12","法律":"#9b59b6","历史":"#2ecc71","人文":"#1abc9c","科技":"#3498db","地理":"#e67e22","申论":"#e91e63"};
const NOTES_ICONS={"政治":"🏛️","经济":"💰","法律":"⚖️","历史":"📜","人文":"🎨","科技":"🔬","地理":"🌏","申论":"📝"};
let notesCat=null,notesSub=null,notesSearchMode=false;
const NOTES_DB={"政治":{},"经济":{},"法律":{},"历史":{},"人文":{},"科技":{},"地理":{},"申论":{}};

function notesGetTotal(){var t=0;for(const c of Object.keys(NOTES_DB))for(const s of Object.keys(NOTES_DB[c]))t+=NOTES_DB[c][s].length;return t;}
function notesGetCatTotal(c){var t=0;for(const s of Object.keys(NOTES_DB[c]||{}))t+=NOTES_DB[c][s].length;return t;}
function notesGetSubTotal(c,s){return(NOTES_DB[c]&&NOTES_DB[c][s])?NOTES_DB[c][s].length:0;}

function openNotes(){
  document.getElementById('notesView').style.display='block';
  document.querySelector('.header').style.display='none';
  document.querySelector('.progress-wrap').style.display='none';
  document.getElementById('dayTabs').style.display='none';
  document.getElementById('mainArea').style.display='none';
  document.getElementById('timerBar').style.display='none';
  notesCat=null;notesSub=null;notesSearchMode=false;
  renderNotesHome();
}
function closeNotes(){
  document.getElementById('notesView').style.display='none';
  document.querySelector('.header').style.display='';
  document.querySelector('.progress-wrap').style.display='';
  document.getElementById('dayTabs').style.display='';
  document.getElementById('mainArea').style.display='';
  var tb=document.getElementById('timerBar');
  if(tb.classList.contains('active'))tb.style.display='block';
}
function goHome(){notesCat=null;notesSub=null;notesSearchMode=false;renderNotesHome();}
function renderNotesHome(){
  var el=document.getElementById('notesContent');
  var total=notesGetTotal();
  var cats=Object.keys(NOTES_DB);
  el.innerHTML='<div class="notes-home"><h2>📚 考公资料库</h2><div class="notes-stats">共 '+total+' 条知识点 · '+cats.length+' 大分类</div><input class="notes-search" id="notesSearchInput" placeholder="🔍 搜索知识点..." oninput="onNotesSearch()"><div class="notes-search-results" id="notesSearchResults"></div><div class="notes-grid" id="notesGrid"></div></div>';
  document.getElementById('notesHomeBtn').style.display='none';
  var grid=document.getElementById('notesGrid');
  grid.innerHTML=cats.map(function(c){
    var cnt=notesGetCatTotal(c);var icon=NOTES_ICONS[c]||'📖';var color=NOTES_COLORS[c]||'#6c63ff';
    return '<div class="notes-card" onclick="openNotesCat(\\''+c+'\\')" style="border-left:3px solid '+color+'"><div class="nc-icon">'+icon+'</div><div class="nc-name">'+c+'</div><div class="nc-count">'+cnt+' 条</div></div>';
  }).join('');
}
function openNotesCat(c){
  notesCat=c;notesSub=null;notesSearchMode=false;
  var el=document.getElementById('notesContent');
  var total=notesGetCatTotal(c);var subs=Object.keys(NOTES_DB[c]);
  var icon=NOTES_ICONS[c]||'📖';var color=NOTES_COLORS[c]||'#6c63ff';
  el.innerHTML='<div class="notes-home"><div class="notes-back-row"><button class="notes-back-btn" onclick="goHome()">← 返回首页</button></div><div class="notes-cat-header" style="border-color:'+color+'"><span class="nch-icon">'+icon+'</span><span class="nch-name">'+c+'</span><span class="nch-count">('+total+'条)</span></div><input class="notes-search" id="notesSearchInput" placeholder="🔍 在'+c+'中搜索..." oninput="onNotesSearch()"><div class="notes-search-results" id="notesSearchResults"></div><div class="notes-sub-grid" id="notesSubGrid"></div></div>';
  document.getElementById('notesHomeBtn').style.display='flex';
  var grid=document.getElementById('notesSubGrid');
  grid.innerHTML=subs.map(function(s){
    var cnt=notesGetSubTotal(c,s);
    return '<div class="notes-sub-card" onclick="openNotesSub(\\''+c+'\\',\\''+s+'\\')" style="border-left:3px solid '+color+'"><div class="nsc-name">'+s+'</div><div class="nsc-count">'+cnt+' 条</div></div>';
  }).join('');
}
function openNotesSub(c,s){
  notesCat=c;notesSub=s;notesSearchMode=false;
  var el=document.getElementById('notesContent');
  var items=NOTES_DB[c][s];var icon=NOTES_ICONS[c]||'📖';var color=NOTES_COLORS[c]||'#6c63ff';
  el.innerHTML='<div class="notes-home"><div class="notes-back-row"><button class="notes-back-btn" onclick="openNotesCat(\\''+c+'\\')">← 返回'+c+'</button></div><div class="notes-cat-header" style="border-color:'+color+'"><span class="nch-icon">'+icon+'</span><span class="nch-name">'+s+'</span><span class="nch-count">('+items.length+'条)</span></div><div class="notes-items" id="notesItemsList"></div></div>';
  document.getElementById('notesHomeBtn').style.display='flex';
  var list=document.getElementById('notesItemsList');
  list.innerHTML=items.map(function(item){
    return '<div class="notes-item" style="border-left-color:'+color+'">'+item.t+'</div>';
  }).join('');
}
function onNotesSearch(){
  var q=document.getElementById('notesSearchInput').value.trim().toLowerCase();
  var resEl=document.getElementById('notesSearchResults');
  if(!q){resEl.style.display='none';resEl.classList.remove('active');return;}
  var results=[];
  var cats=notesCat?[notesCat]:Object.keys(NOTES_DB);
  cats.forEach(function(c){
    var subs=notesSub?[notesSub]:Object.keys(NOTES_DB[c]);
    subs.forEach(function(s){
      if(!NOTES_DB[c][s])return;
      NOTES_DB[c][s].forEach(function(item,idx){
        if(item.t.toLowerCase().indexOf(q)>=0){results.push({c:c,s:s,i:idx,t:item.t});}
      });
    });
  });
  resEl.textContent='找到 '+results.length+' 条结果';
  resEl.style.display='block';resEl.classList.add('active');
  var list=document.getElementById('notesItemsList');
  if(!list){return;}
  if(results.length===0){list.innerHTML='<div class="notes-item" style="color:var(--sub);text-align:center">未找到匹配的知识点</div>';return;}
  list.innerHTML=results.map(function(r){
    var color=NOTES_COLORS[r.c]||'#6c63ff';
    var re=new RegExp('('+q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','gi');
    var highlighted=r.t.replace(re,'<mark>$1</mark>');
    return '<div class="notes-item" style="border-left-color:'+color+'"><span style="font-size:11px;color:var(--sub)">['+r.c+' · '+r.s+']</span><br>'+highlighted+'</div>';
  }).join('');
}
"""

# 构建step2: V7 + CSS + HTML + button + 函数(空DB)
import re

NOTES_CSS = """
/* ── Notes Sub-page ── */
[data-theme="dark"] .notes-body,
.notes-body{font-family:inherit;background:var(--bg);color:var(--text);min-height:100vh;padding:12px 16px 80px}
.notes-home{max-width:420px;margin:0 auto}
.notes-home h2{text-align:center;font-size:18px;margin-bottom:16px}
.notes-stats{text-align:center;font-size:13px;color:var(--sub);margin-bottom:16px}
.notes-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}
.notes-card{background:var(--card);border-radius:12px;padding:14px 12px;cursor:pointer;box-shadow:var(--shadow);transition:transform .15s}
.notes-card:active{transform:scale(.97)}
.notes-card .nc-icon{font-size:24px;margin-bottom:6px}
.notes-card .nc-name{font-size:14px;font-weight:600}
.notes-card .nc-count{font-size:11px;color:var(--sub);margin-top:2px}
.notes-cat-header{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.notes-cat-header .nch-icon{font-size:22px}
.notes-cat-header .nch-name{font-size:16px;font-weight:600}
.notes-cat-header .nch-count{font-size:12px;color:var(--sub)}
.notes-back-row{margin-bottom:12px}
.notes-back-btn{background:var(--card);border:1.5px solid var(--border);border-radius:20px;padding:8px 18px;font-size:13px;cursor:pointer;color:var(--text);font-family:inherit}
.notes-back-btn:active{opacity:.8}
.notes-search{width:100%;padding:10px 14px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;outline:none;color:var(--text);background:var(--card);margin-bottom:14px;box-sizing:border-box;font-family:inherit}
.notes-search:focus{border-color:var(--accent)}
.notes-search-results{margin-bottom:10px;font-size:13px;color:var(--sub);display:none}
.notes-search-results.active{display:block}
.notes-sub-grid{display:grid;gap:10px;margin-bottom:14px}
.notes-sub-card{background:var(--card);border-radius:12px;padding:12px 14px;cursor:pointer;box-shadow:var(--shadow);transition:transform .15s}
.notes-sub-card:active{transform:scale(.97)}
.notes-sub-card .nsc-name{font-size:14px;font-weight:600;margin-bottom:4px}
.notes-sub-card .nsc-count{font-size:11px;color:var(--sub)}
.notes-items{display:grid;gap:8px;padding-bottom:20px}
.notes-item{background:var(--card);border-radius:10px;padding:12px 14px;font-size:13px;line-height:1.6;box-shadow:var(--shadow);border-left:3px solid var(--accent)}
.notes-item mark{background:#ffe066;color:#000;padding:1px 2px;border-radius:3px}
.notes-home-btn{position:fixed;bottom:20px;right:20px;width:48px;height:48px;border-radius:50%;border:none;font-size:22px;cursor:pointer;box-shadow:0 2px 12px rgba(0,0,0,.2);z-index:100;display:flex;align-items:center;justify-content:center;background:var(--accent);color:#fff}
"""

NOTES_HTML = """
<!-- Notes View -->
<div id="notesView" style="display:none">
  <div class="notes-body" id="notesContent"></div>
  <button class="notes-home-btn" onclick="goHome()" title="Home" style="display:none" id="notesHomeBtn">🏠</button>
</div>
"""

# Step 2 build
h = v7

# CSS
pos = h.rfind('</style>')
h = h[:pos] + NOTES_CSS + '\n' + h[pos:]

# HTML
pos = h.find('<!-- Edit Modal -->')
h = h[:pos] + NOTES_HTML + '\n' + h[pos:]

# Button
old_btn = '<button class="header-btn" onclick="toggleTheme()" title="切换主题">🌙</button>'
new_btn = '<button class="header-btn" onclick="openNotes()" title="考公资料" style="font-size:16px">📚</button>\n        ' + old_btn
h = h.replace(old_btn, new_btn)

# JS (empty DB)
marker = '// ── Init ──'
h = h.replace(marker, NOTES_FUNCS_NO_DB + '\n' + marker)

with open('c:/Users/chenx/WorkBuddy/Claw/_step2_no_data.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f'Step 2 saved: {len(h)} bytes (V7 + UI + functions, empty DB)')

# Step 3: 用NOTES_DB_STR替换空DB
h3 = v7
pos = h3.rfind('</style>')
h3 = h3[:pos] + NOTES_CSS + '\n' + h3[pos:]
pos = h3.find('<!-- Edit Modal -->')
h3 = h3[:pos] + NOTES_HTML + '\n' + h3[pos:]
h3 = h3.replace(old_btn, new_btn)

# 这里先插入函数(含空DB)，然后把空DB替换成真实DB
h3 = h3.replace(marker, NOTES_FUNCS_NO_DB + '\n' + marker)
# 替换空DB
h3 = h3.replace(
    'const NOTES_DB={"政治":{},"经济":{},"法律":{},"历史":{},"人文":{},"科技":{},"地理":{},"申论":{}};',
    NOTES_DB_STR
)

with open('c:/Users/chenx/WorkBuddy/Claw/_step3_with_data.html', 'w', encoding='utf-8') as f:
    f.write(h3)
print(f'Step 3 saved: {len(h3)} bytes (V7 + UI + functions + real DB)')

# 验证script标签内JS语法
# 提取<script>内容写入.js文件让用户能在浏览器console里测
scripts = re.findall(r'<script[^>]*>(.*?)</script>', h3, re.DOTALL)
for i, s in enumerate(scripts):
    jsfile = f'c:/Users/chenx/WorkBuddy/Claw/_script{i}.js'
    with open(jsfile, 'w', encoding='utf-8') as f:
        f.write(s)
    # 检查是否有明显的括号不匹配
    opens = s.count('{')
    closes = s.count('}')
    sq_opens = s.count('[')
    sq_closes = s.count(']')
    parens_o = s.count('(')
    parens_c = s.count(')')
    balanced = 'OK' if (opens == closes and sq_opens == sq_closes and parens_o == parens_c) else 'MISMATCH'
    print(f'  Script {i}: {len(s)} chars, braces {opens}/{closes}, brackets {sq_opens}/{sq_closes}, parens {parens_o}/{parens_c} -> {balanced}')
