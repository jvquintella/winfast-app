import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS — substituir todo o bloco gs-* pelo novo design
# ══════════════════════════════════════════════════════════════════
NEW_CSS = (
    "#game-selector{position:fixed;inset:0;background:var(--bg);z-index:9998;display:none;flex-direction:column;overflow-y:auto;}\r\n"
    ".gs-topbar{background:var(--sf);border-bottom:2px solid var(--usp);padding:16px 32px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;position:sticky;top:0;z-index:3;}\r\n"
    ".gs-filterbar{background:var(--sf2);border-bottom:1px solid var(--bd);padding:10px 32px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;position:sticky;top:57px;z-index:2;}\r\n"
    ".gs-search-wrap{position:relative;flex:1;min-width:180px;max-width:300px;}\r\n"
    ".gs-search-icon{position:absolute;left:10px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:var(--mu);pointer-events:none;}\r\n"
    ".gs-search-input{background:var(--bg);border:1px solid var(--bd);border-radius:20px;padding:7px 12px 7px 30px;color:var(--tx);font-family:'Barlow',sans-serif;font-size:13px;width:100%;box-sizing:border-box;outline:none;transition:border-color .2s;}\r\n"
    ".gs-search-input:focus{border-color:var(--mu);}\r\n"
    ".gs-pills{display:flex;gap:6px;align-items:center;flex-wrap:wrap;}\r\n"
    ".gs-pill{background:none;border:1px solid var(--bd);color:var(--mu2);padding:5px 14px;border-radius:20px;cursor:pointer;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:11px;letter-spacing:1px;transition:all .18s;white-space:nowrap;}\r\n"
    ".gs-pill:hover{border-color:var(--mu);color:var(--tx);}\r\n"
    ".gs-pill.active{background:var(--usp);color:#000;border-color:var(--usp);}\r\n"
    ".gs-period-wrap{position:relative;}\r\n"
    ".gs-period-dd{position:absolute;top:calc(100% + 8px);left:0;background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:6px;min-width:230px;z-index:200;box-shadow:0 8px 24px rgba(0,0,0,.5);}\r\n"
    ".gs-period-mi{padding:8px 12px;border-radius:6px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-family:'Barlow Condensed',sans-serif;font-size:13px;color:var(--tx);font-weight:600;letter-spacing:.5px;transition:background .15s;}\r\n"
    ".gs-period-mi:hover{background:var(--sf2);}\r\n"
    ".gs-period-mi.active{color:var(--usp);}\r\n"
    ".gs-cal{padding:4px;}\r\n"
    ".gs-cal-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;padding:0 2px;}\r\n"
    ".gs-cal-title{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:13px;letter-spacing:1px;color:var(--tx);text-transform:uppercase;}\r\n"
    ".gs-cal-nb{background:none;border:none;color:var(--mu);cursor:pointer;font-size:13px;padding:2px 6px;border-radius:4px;transition:color .15s;}\r\n"
    ".gs-cal-nb:hover{color:var(--tx);}\r\n"
    ".gs-cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;}\r\n"
    ".gs-cal-dow{font-family:'Barlow Condensed',sans-serif;font-size:10px;color:var(--mu);text-align:center;padding:3px 0;font-weight:700;}\r\n"
    ".gs-cal-day{text-align:center;padding:3px 1px;border-radius:5px;min-height:32px;font-family:'Barlow Condensed',sans-serif;font-size:12px;color:var(--mu2);cursor:default;}\r\n"
    ".gs-cal-day.hg{color:var(--tx);cursor:pointer;}\r\n"
    ".gs-cal-day.hg:hover{background:var(--sf2);}\r\n"
    ".gs-cal-day.act{background:var(--usp)!important;color:#000!important;}\r\n"
    ".gs-cal-dots{display:flex;justify-content:center;gap:2px;margin-top:2px;flex-wrap:wrap;}\r\n"
    ".gs-cal-dot{width:5px;height:5px;border-radius:50%;}\r\n"
    ".gs-filter-count{font-size:11px;color:var(--mu);font-family:'Barlow Condensed',sans-serif;letter-spacing:.5px;margin-left:auto;white-space:nowrap;}\r\n"
    ".gs-body{padding:24px 32px;max-width:1100px;margin:0 auto;width:100%;box-sizing:border-box;}\r\n"
    "#gs-cards{display:block;}\r\n"
    ".gs-section{margin-bottom:32px;}\r\n"
    ".gs-section-title{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;padding-bottom:8px;display:flex;align-items:center;justify-content:space-between;}\r\n"
    ".gs-section-count{font-size:10px;font-weight:400;letter-spacing:.5px;text-transform:none;opacity:.7;}\r\n"
    ".gs-gt-badge{font-size:9px;font-weight:700;letter-spacing:1px;padding:2px 8px;border-radius:3px;text-transform:uppercase;margin-left:8px;}\r\n"
    ".gs-gt-badge.comp{background:rgba(59,130,246,.15);color:var(--bl);}\r\n"
    ".gs-gt-badge.ami{background:rgba(107,114,128,.15);color:var(--mu2);}\r\n"
    ".gs-cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:12px;}\r\n"
    ".gs-card{background:var(--sf);border:2px solid var(--bd);border-radius:10px;padding:16px;cursor:pointer;transition:all .18s;user-select:none;position:relative;}\r\n"
    ".gs-card:hover{border-color:var(--mu);}\r\n"
    ".gs-card.sel{border-color:var(--usp);}\r\n"
    ".gs-chk{position:absolute;top:12px;right:12px;width:22px;height:22px;border-radius:50%;border:2px solid var(--bd);transition:all .18s;background:var(--bg);}\r\n"
    ".gs-card.sel .gs-chk{background:var(--usp);border-color:var(--usp);}\r\n"
    ".gs-card.sel .gs-chk::after{content:'';display:block;width:6px;height:10px;border:2px solid #000;border-top:none;border-left:none;transform:rotate(45deg) translate(1px,-1px);margin:2px auto 0;}\r\n"
    ".gc-badge{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:10px;letter-spacing:1px;padding:2px 8px;border-radius:3px;display:inline-block;margin-bottom:10px;}\r\n"
    ".gc-badge.w{background:rgba(34,197,94,.15);color:var(--gr);}\r\n"
    ".gc-badge.l{background:rgba(239,68,68,.15);color:var(--rd);}\r\n"
    ".gc-adv{font-weight:600;font-size:13px;margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--tx);}\r\n"
    ".gc-score{font-family:'Barlow Condensed',sans-serif;font-size:36px;font-weight:900;margin-bottom:6px;line-height:1;}\r\n"
    ".gc-date{font-size:10px;color:var(--mu);letter-spacing:.5px;}\r\n"
    ".gs-action-btn{background:none;border:1px solid var(--bd);color:var(--mu2);padding:6px 14px;border-radius:6px;cursor:pointer;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;transition:all .18s;}\r\n"
    ".gs-action-btn:hover{border-color:var(--mu);color:var(--tx);}\r\n"
    "#gs-count{font-size:12px;color:var(--mu);font-family:'Barlow Condensed',sans-serif;letter-spacing:.5px;}\r\n"
    "#gs-gen-btn{background:var(--usp);color:#000;border:none;border-radius:8px;padding:14px 40px;font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:16px;letter-spacing:2px;text-transform:uppercase;cursor:pointer;transition:opacity .2s;display:flex;align-items:center;gap:10px;}\r\n"
    "#gs-gen-btn:hover{opacity:.85;}#gs-gen-btn:disabled{opacity:.4;cursor:default;}\r\n"
    "@media(max-width:768px){.gs-topbar{padding:12px 16px;}.gs-filterbar{padding:8px 16px;}.gs-body{padding:16px;}}"
)

css_pattern = r'#game-selector\{position:fixed.*?@media\(max-width:768px\)\{\.gs-header\{padding:14px 16px;\}\.gs-body\{padding:16px;\}\}'
m = re.search(css_pattern, c, re.DOTALL)
if m:
    c = c[:m.start()] + NEW_CSS + c[m.end():]
    print('1 OK: CSS redesenhado')
else:
    print('1 FAIL CSS regex')

# ══════════════════════════════════════════════════════════════════
# 2. HTML — redesenhar #game-selector
# ══════════════════════════════════════════════════════════════════
NEW_HTML = (
    '<!-- ── SELETOR DE JOGOS ───────────────────────────────────────── -->\r\n'
    '<div id="game-selector">\r\n'
    '  <!-- barra superior -->\r\n'
    '  <div class="gs-topbar">\r\n'
    '    <div>\r\n'
    '      <div style="font-family:\'Barlow Condensed\',sans-serif;font-weight:900;font-size:20px;letter-spacing:2px;color:var(--usp);">WIN<span style="color:var(--tx);">FAST</span></div>\r\n'
    '      <div style="font-size:10px;color:var(--mu);letter-spacing:2px;text-transform:uppercase;margin-top:2px;">Selecione os jogos para analisar</div>\r\n'
    '    </div>\r\n'
    '    <div style="display:flex;align-items:center;gap:10px;">\r\n'
    '      <button class="gs-action-btn" onclick="selectAllGames()">Todos</button>\r\n'
    '      <button class="gs-action-btn" onclick="clearAllGames()">Nenhum</button>\r\n'
    '      <span id="gs-count">0 selecionados</span>\r\n'
    '    </div>\r\n'
    '  </div>\r\n'
    '  <!-- barra de filtros -->\r\n'
    '  <div class="gs-filterbar">\r\n'
    '    <div class="gs-search-wrap">\r\n'
    '      <svg class="gs-search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="8.5" cy="8.5" r="5.5"/><line x1="13" y1="13" x2="17" y2="17"/></svg>\r\n'
    '      <input type="text" id="gs-search" class="gs-search-input" placeholder="Buscar adversario ou competicao..." oninput="applyGsFilters()">\r\n'
    '    </div>\r\n'
    '    <div class="gs-pills">\r\n'
    '      <button class="gs-pill active" id="gspill-all" onclick="setGsQuick(\'all\',this)">TODAS</button>\r\n'
    '      <button class="gs-pill" id="gspill-w" onclick="setGsQuick(\'w\',this)">VITORIAS</button>\r\n'
    '      <button class="gs-pill" id="gspill-l" onclick="setGsQuick(\'l\',this)">DERROTAS</button>\r\n'
    '      <div class="gs-period-wrap" id="gs-period-wrap">\r\n'
    '        <button class="gs-pill" id="gspill-period" onclick="toggleGsPeriod(event)">&#128197; PERIODO &#9662;</button>\r\n'
    '        <div id="gs-period-dd" class="gs-period-dd" style="display:none;"></div>\r\n'
    '      </div>\r\n'
    '    </div>\r\n'
    '    <div id="gs-filter-count" class="gs-filter-count"></div>\r\n'
    '  </div>\r\n'
    '  <!-- area de cards -->\r\n'
    '  <div class="gs-body">\r\n'
    '    <div id="gs-cards"></div>\r\n'
    '    <div style="display:flex;justify-content:center;padding:24px 0 48px;">\r\n'
    '      <button id="gs-gen-btn" onclick="generateReport()" disabled>\r\n'
    '        Gerar Relatorio &nbsp;&#8594;\r\n'
    '      </button>\r\n'
    '    </div>\r\n'
    '  </div>\r\n'
    '</div>'
)

html_pattern = r'<!-- ── SELETOR DE JOGOS[^>]*-->\s*<div id="game-selector">[\s\S]*?</div>\s*</div>\s*</div>\s*</div>'
m2 = re.search(html_pattern, c)
if m2:
    c = c[:m2.start()] + NEW_HTML + c[m2.end():]
    print('2 OK: HTML redesenhado')
else:
    # fallback: procurar pelo comentario + div exato
    old_html_start = '<!-- ── SELETOR DE JOGOS ───────────────────────────────────────── -->'
    idx = c.find(old_html_start)
    # achar o </div> que fecha #game-selector
    gs_start = c.find('<div id="game-selector">', idx)
    if gs_start >= 0:
        # contar brackets para achar o fechamento
        depth = 0
        pos = gs_start
        while pos < len(c):
            if c[pos:pos+4] == '<div':
                depth += 1
            elif c[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    gs_end = pos + 6
                    break
            pos += 1
        c = c[:idx] + NEW_HTML + c[gs_end:]
        print('2 OK: HTML redesenhado (fallback)')
    else:
        print('2 FAIL HTML')

# ══════════════════════════════════════════════════════════════════
# 3. JS — substituir todo o bloco do seletor
# ══════════════════════════════════════════════════════════════════
NEW_JS = (
    "/* ── SELETOR DE JOGOS ──────────────────────────────────────────── */\r\n"
    "var _gsRawRows=[];\r\n"
    "var _gsSession=null;\r\n"
    "var _gsSelected=[];\r\n"
    "var _gsGamesCache=[];\r\n"
    "var _gsCompNamesCache=[];\r\n"
    "var _gsGameTypesCache=[];\r\n"
    "var _gsMyTeamCache='';\r\n"
    "var _gsQuickFilter='all';\r\n"
    "var _gsSearchText='';\r\n"
    "var _gsMonthFilter=null;\r\n"
    "var _gsDayFilter=null;\r\n"
    "var _gsCalMonth=null;\r\n"
    "var _gsCompColorMap={};\r\n"
    "var GS_MONTHS=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];\r\n"
    "var GS_MONTHS_FULL=['Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];\r\n"
    "var GS_DOW=['D','S','T','Q','Q','S','S'];\r\n"
    "var GS_PALETTE=['#f5c518','#3b82f6','#a855f7','#f97316','#14b8a6','#ec4899','#84cc16','#fb923c'];\r\n"
    "\r\n"
    "function gsCompColor(name){\r\n"
    "  if(!_gsCompColorMap[name]){\r\n"
    "    var idx=Object.keys(_gsCompColorMap).length % GS_PALETTE.length;\r\n"
    "    _gsCompColorMap[name]=GS_PALETTE[idx];\r\n"
    "  }\r\n"
    "  return _gsCompColorMap[name];\r\n"
    "}\r\n"
    "\r\n"
    "function showGameSelector(rawRows,session){\r\n"
    "  _gsRawRows=rawRows;_gsSession=session;\r\n"
    "  var allGames=rawRows.filter(function(r){return (r[SB_COL]||r.data||{}).finished;});\r\n"
    "  allGames.sort(function(a,b){var ga=a[SB_COL]||a.data||{},gb=b[SB_COL]||b.data||{};return parseDt(ga.date)-parseDt(gb.date);});\r\n"
    "  var games=allGames.map(function(r){return r[SB_COL]||r.data;});\r\n"
    "  var gameTypes=allGames.map(function(r){return r.gametype||(r[SB_COL]||r.data||{}).gametype||'';});\r\n"
    "  var compNames=allGames.map(function(r,i){var cn=r.competitionName||(r[SB_COL]||r.data||{}).competitionName||'';return cn||gameTypes[i]||'Sem Competicao';});\r\n"
    "  var myTeam=detectMyTeam(games);\r\n"
    "  _gsGamesCache=games;_gsCompNamesCache=compNames;_gsGameTypesCache=gameTypes;_gsMyTeamCache=myTeam;\r\n"
    "  _gsSelected=games.map(function(){return true;});\r\n"
    "  _gsQuickFilter='all';_gsSearchText='';_gsMonthFilter=null;_gsDayFilter=null;_gsCalMonth=null;\r\n"
    "  _gsCompColorMap={};\r\n"
    "  // pre-assign competition colors in order of appearance\r\n"
    "  compNames.forEach(function(n){gsCompColor(n);});\r\n"
    "  document.getElementById('login-overlay').style.display='none';\r\n"
    "  document.getElementById('game-selector').style.display='flex';\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function applyGsFilters(){\r\n"
    "  var el=document.getElementById('gs-search');\r\n"
    "  _gsSearchText=el?el.value.toLowerCase():'';\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function setGsQuick(f,btn){\r\n"
    "  _gsQuickFilter=f;\r\n"
    "  _gsMonthFilter=null;_gsDayFilter=null;_gsCalMonth=null;\r\n"
    "  closeGsPeriod();\r\n"
    "  document.querySelectorAll('.gs-pills .gs-pill').forEach(function(p){p.classList.remove('active');});\r\n"
    "  if(btn)btn.classList.add('active');\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function toggleGsPeriod(e){\r\n"
    "  if(e)e.stopPropagation();\r\n"
    "  var dd=document.getElementById('gs-period-dd');\r\n"
    "  if(!dd)return;\r\n"
    "  if(dd.style.display==='none'||!dd.style.display){\r\n"
    "    _gsCalMonth=null;\r\n"
    "    dd.innerHTML=buildGsPeriodMonths();\r\n"
    "    dd.style.display='';\r\n"
    "  } else {\r\n"
    "    dd.style.display='none';\r\n"
    "  }\r\n"
    "}\r\n"
    "\r\n"
    "function closeGsPeriod(){\r\n"
    "  var dd=document.getElementById('gs-period-dd');\r\n"
    "  if(dd)dd.style.display='none';\r\n"
    "}\r\n"
    "\r\n"
    "function buildGsPeriodMonths(){\r\n"
    "  var games=_gsGamesCache,myTeam=_gsMyTeamCache;\r\n"
    "  var mmap={};\r\n"
    "  games.forEach(function(g){\r\n"
    "    var d=(g.date||'').split('/');\r\n"
    "    if(d.length!==3)return;\r\n"
    "    var key=d[1]+'/'+d[2];\r\n"
    "    if(!mmap[key])mmap[key]={wins:0,total:0,mo:parseInt(d[1],10),yr:parseInt(d[2],10)};\r\n"
    "    var teams=g.teams||[];\r\n"
    "    var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "    if(ui<0)ui=0;\r\n"
    "    var u=teams[ui]||{},a=teams[1-ui]||{};\r\n"
    "    if((u.score||0)>(a.score||0))mmap[key].wins++;\r\n"
    "    mmap[key].total++;\r\n"
    "  });\r\n"
    "  var sorted=Object.keys(mmap).sort(function(a,b){var ma=mmap[a],mb=mmap[b];return ma.yr!==mb.yr?ma.yr-mb.yr:ma.mo-mb.mo;});\r\n"
    "  return sorted.map(function(k){\r\n"
    "    var m=mmap[k];\r\n"
    "    var name=(GS_MONTHS_FULL[m.mo-1]||k)+' '+m.yr;\r\n"
    "    var cls='gs-period-mi'+(_gsCalMonth===k?' active':'');\r\n"
    "    return '<div class=\"'+cls+'\" onclick=\"showGsCalendar(\\''+k+'\\')\">'+'<span>'+name+'</span>'+'<span style=\"color:var(--mu);font-size:11px;\">'+m.wins+'V '+(m.total-m.wins)+'D &middot; '+m.total+'j</span>'+'</div>';\r\n"
    "  }).join('');\r\n"
    "}\r\n"
    "\r\n"
    "function showGsCalendar(monthKey){\r\n"
    "  _gsCalMonth=monthKey;\r\n"
    "  _gsMonthFilter=monthKey;\r\n"
    "  _gsDayFilter=null;\r\n"
    "  var parts=monthKey.split('/');\r\n"
    "  var mo=parseInt(parts[0],10),yr=parseInt(parts[1],10);\r\n"
    "  var games=_gsGamesCache,compNames=_gsCompNamesCache;\r\n"
    "  var dayMap={};\r\n"
    "  games.forEach(function(g,i){\r\n"
    "    var d=(g.date||'').split('/');\r\n"
    "    if(d.length!==3||parseInt(d[1],10)!==mo||parseInt(d[2],10)!==yr)return;\r\n"
    "    var dd=d[0];\r\n"
    "    if(!dayMap[dd])dayMap[dd]=[];\r\n"
    "    var col=gsCompColor(compNames[i]);\r\n"
    "    if(dayMap[dd].indexOf(col)<0)dayMap[dd].push(col);\r\n"
    "  });\r\n"
    "  var firstDow=new Date(yr,mo-1,1).getDay();\r\n"
    "  var daysInMo=new Date(yr,mo,0).getDate();\r\n"
    "  var mname=(GS_MONTHS_FULL[mo-1]||monthKey)+' '+yr;\r\n"
    "  var html='<div class=\"gs-cal\">';\r\n"
    "  html+='<div class=\"gs-cal-nav\">';\r\n"
    "  html+='<button class=\"gs-cal-nb\" onclick=\"showGsPeriodMonths()\">&#8592; Meses</button>';\r\n"
    "  html+='<span class=\"gs-cal-title\">'+GS_MONTHS[mo-1]+' '+yr+'</span>';\r\n"
    "  html+='<button class=\"gs-cal-nb\" onclick=\"clearGsPeriod()\" title=\"Limpar\">&#215;</button>';\r\n"
    "  html+='</div>';\r\n"
    "  html+='<div class=\"gs-cal-grid\">';\r\n"
    "  GS_DOW.forEach(function(d){html+='<div class=\"gs-cal-dow\">'+d+'</div>';});\r\n"
    "  for(var e=0;e<firstDow;e++)html+='<div class=\"gs-cal-day\"></div>';\r\n"
    "  for(var d=1;d<=daysInMo;d++){\r\n"
    "    var dd=String(d).padStart(2,'0');\r\n"
    "    var dayKey=dd+'/'+parts[0]+'/'+yr;\r\n"
    "    var hasg=!!dayMap[dd];\r\n"
    "    var isAct=_gsDayFilter===dayKey;\r\n"
    "    var cls='gs-cal-day'+(hasg?' hg':'')+(isAct?' act':'');\r\n"
    "    html+='<div class=\"'+cls+'\"'+(hasg?' onclick=\"setGsDay(\\''+dayKey+'\\')\"':'')+'>';\r\n"
    "    html+='<div>'+d+'</div>';\r\n"
    "    if(hasg){\r\n"
    "      html+='<div class=\"gs-cal-dots\">';\r\n"
    "      dayMap[dd].forEach(function(col){html+='<div class=\"gs-cal-dot\" style=\"background:'+col+';\"></div>';});\r\n"
    "      html+='</div>';\r\n"
    "    }\r\n"
    "    html+='</div>';\r\n"
    "  }\r\n"
    "  html+='</div></div>';\r\n"
    "  var dd2=document.getElementById('gs-period-dd');\r\n"
    "  if(dd2){dd2.style.display='';dd2.innerHTML=html;}\r\n"
    "  // ativar pill de periodo\r\n"
    "  document.querySelectorAll('.gs-pills .gs-pill').forEach(function(p){p.classList.remove('active');});\r\n"
    "  var pb=document.getElementById('gspill-period');\r\n"
    "  if(pb)pb.classList.add('active');\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function showGsPeriodMonths(){\r\n"
    "  _gsCalMonth=null;\r\n"
    "  var dd=document.getElementById('gs-period-dd');\r\n"
    "  if(dd)dd.innerHTML=buildGsPeriodMonths();\r\n"
    "}\r\n"
    "\r\n"
    "function setGsDay(dayKey){\r\n"
    "  _gsDayFilter=(_gsDayFilter===dayKey)?null:dayKey;\r\n"
    "  if(_gsCalMonth)showGsCalendar(_gsCalMonth);\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function clearGsPeriod(){\r\n"
    "  _gsDayFilter=null;_gsMonthFilter=null;_gsCalMonth=null;\r\n"
    "  closeGsPeriod();\r\n"
    "  document.querySelectorAll('.gs-pills .gs-pill').forEach(function(p){p.classList.remove('active');});\r\n"
    "  var ab=document.getElementById('gspill-all');\r\n"
    "  if(ab){ab.classList.add('active');_gsQuickFilter='all';}\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function renderGsSections(){\r\n"
    "  var games=_gsGamesCache,compNames=_gsCompNamesCache,gameTypes=_gsGameTypesCache,myTeam=_gsMyTeamCache;\r\n"
    "  var search=(_gsSearchText||'').toLowerCase();\r\n"
    "  var indices=games.map(function(_,i){return i;}).filter(function(i){\r\n"
    "    var g=games[i],teams=g.teams||[];\r\n"
    "    var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "    if(ui<0)ui=0;\r\n"
    "    var u=teams[ui]||{},a=teams[1-ui]||{};\r\n"
    "    var win=(u.score||0)>(a.score||0);\r\n"
    "    if(_gsQuickFilter==='w'&&!win)return false;\r\n"
    "    if(_gsQuickFilter==='l'&&win)return false;\r\n"
    "    if(_gsDayFilter){if((g.date||'')!==_gsDayFilter)return false;}\r\n"
    "    else if(_gsMonthFilter){var d=(g.date||'').split('/');if(d.length!==3||(d[1]+'/'+d[2])!==_gsMonthFilter)return false;}\r\n"
    "    if(search){var adv=(a.name||'').toLowerCase(),comp=(compNames[i]||'').toLowerCase();if(adv.indexOf(search)<0&&comp.indexOf(search)<0)return false;}\r\n"
    "    return true;\r\n"
    "  });\r\n"
    "  var groups={},groupOrder=[],groupType={};\r\n"
    "  indices.forEach(function(i){var key=compNames[i];if(!groups[key]){groups[key]=[];groupOrder.push(key);groupType[key]=gameTypes[i];}groups[key].push(i);});\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
    "  if(!groupOrder.length){\r\n"
    "    container.innerHTML='<div style=\"text-align:center;color:var(--mu);padding:60px 0;font-family:\\'Barlow Condensed\\',sans-serif;font-size:15px;\">Nenhum jogo encontrado</div>';\r\n"
    "    updateGsFilterCount(0,games.length);return;\r\n"
    "  }\r\n"
    "  container.innerHTML=groupOrder.map(function(key){\r\n"
    "    var wins=groups[key].filter(function(i){var g=games[i],teams=g.teams||[];var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});if(ui<0)ui=0;var u=teams[ui]||{},a=teams[1-ui]||{};return (u.score||0)>(a.score||0);}).length;\r\n"
    "    var total=groups[key].length;\r\n"
    "    var gt=groupType[key]||'';\r\n"
    "    var badgeCls=(gt||'').toLowerCase().indexOf('comp')>=0?'comp':'ami';\r\n"
    "    var badgeHtml=gt?'<span class=\"gs-gt-badge '+badgeCls+'\">'+gt+'</span>':'';\r\n"
    "    var col=gsCompColor(key);\r\n"
    "    var html='<div class=\"gs-section\"><div class=\"gs-section-title\" style=\"color:'+col+';border-bottom:1px solid '+col+'33;\">'+key+badgeHtml+'<span class=\"gs-section-count\">'+wins+'V '+(total-wins)+'D &nbsp;&middot;&nbsp; '+total+' jogo'+(total!==1?'s':'')+'</span></div><div class=\"gs-cards-grid\">';\r\n"
    "    html+=groups[key].map(function(i){\r\n"
    "      var g=games[i],teams=g.teams||[];\r\n"
    "      var uspIdx=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "      if(uspIdx<0)uspIdx=0;\r\n"
    "      var adv=teams[1-uspIdx]||{},usp=teams[uspIdx]||{};\r\n"
    "      var uspPts=usp.score||0,advPts=adv.score||0;\r\n"
    "      var win=uspPts>advPts;\r\n"
    "      var advName=(adv.name||'?').trim();\r\n"
    "      var sel=_gsSelected[i]?'sel':'';\r\n"
    "      return '<div class=\"gs-card '+sel+'\" data-i=\"'+i+'\" onclick=\"toggleGameCard('+i+')\"><div class=\"gs-chk\" id=\"gs-chk-'+i+'\"></div><span class=\"gc-badge '+(win?'w':'l')+'\">'+(win?'VITORIA':'DERROTA')+'</span><div class=\"gc-adv\">vs '+advName+'</div><div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)\')+'\">'+uspPts+'</span><span style=\"color:var(--mu);font-size:16px;margin:0 4px;\">×</span><span style=\"color:var(--tx);\">'+advPts+'</span></div><div class=\"gc-date\">'+(g.date||'')+'</div></div>';\r\n"
    "    }).join('');\r\n"
    "    html+='</div></div>';\r\n"
    "    return html;\r\n"
    "  }).join('');\r\n"
    "  updateGsFilterCount(indices.length,games.length);\r\n"
    "}\r\n"
    "\r\n"
    "function updateGsFilterCount(shown,total){\r\n"
    "  var el=document.getElementById('gs-filter-count');\r\n"
    "  if(!el)return;\r\n"
    "  var s=shown!==undefined?shown:_gsGamesCache.length;\r\n"
    "  var t=total!==undefined?total:_gsGamesCache.length;\r\n"
    "  el.textContent=s+' de '+t+' jogo'+(t!==1?'s':'');\r\n"
    "}\r\n"
    "\r\n"
    "function toggleGameCard(i){\r\n"
    "  _gsSelected[i]=!_gsSelected[i];\r\n"
    "  var card=document.querySelector('.gs-card[data-i=\"'+i+'\"]');\r\n"
    "  if(card)card.classList.toggle('sel',_gsSelected[i]);\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function selectAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return true;});\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function clearAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return false;});\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function updateGsCount(){\r\n"
    "  var n=_gsSelected.filter(Boolean).length;\r\n"
    "  var el=document.getElementById('gs-count');\r\n"
    "  if(el)el.textContent=n+' jogo'+(n!==1?'s':'')+' selecionado'+(n!==1?'s':'');\r\n"
    "  var btn=document.getElementById('gs-gen-btn');\r\n"
    "  if(btn)btn.disabled=n===0;\r\n"
    "}\r\n"
    "\r\n"
    "function generateReport(){\r\n"
    "  var allGames=(_gsRawRows||[]).filter(function(r){return (r[SB_COL]||r.data||{}).finished;});\r\n"
    "  allGames.sort(function(a,b){var ga=a[SB_COL]||a.data||{},gb=b[SB_COL]||b.data||{};return parseDt(ga.date)-parseDt(gb.date);});\r\n"
    "  var selected=allGames.filter(function(_,i){return _gsSelected[i];});\r\n"
    "  if(!selected.length)return;\r\n"
    "  document.getElementById('game-selector').style.display='none';\r\n"
    "  var email=(_gsSession&&_gsSession.user&&_gsSession.user.email)||'';\r\n"
    "  var badge=document.getElementById('user-badge');\r\n"
    "  if(badge)badge.textContent=email;\r\n"
    "  processGames(selected);\r\n"
    "}\r\n"
    "\r\n"
    "// fechar dropdown ao clicar fora\r\n"
    "document.addEventListener('click',function(e){\r\n"
    "  var wrap=document.getElementById('gs-period-wrap');\r\n"
    "  if(wrap&&!wrap.contains(e.target))closeGsPeriod();\r\n"
    "});\r\n"
    "/* ─────────────────────────────────────────────────────────────── */\r\n"
)

# substituir todo o bloco JS do seletor
js_pattern = r'/\* ── SELETOR DE JOGOS ──+[\s\S]*?/\* ─+[\s\S]*?\*/'
m3 = re.search(js_pattern, c)
if m3:
    c = c[:m3.start()] + NEW_JS + c[m3.end():]
    print('3 OK: JS redesenhado')
else:
    # tentar substituir via ancora unica
    js_start = c.find('/* ── SELETOR DE JOGOS')
    js_end_marker = '/* ─────────────────────────────────────────────────────────────── */'
    js_end = c.find(js_end_marker)
    if js_start >= 0 and js_end >= 0:
        c = c[:js_start] + NEW_JS + c[js_end + len(js_end_marker):]
        print('3 OK: JS redesenhado (fallback)')
    else:
        print('3 FAIL JS — start:', js_start, 'end:', js_end)

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
