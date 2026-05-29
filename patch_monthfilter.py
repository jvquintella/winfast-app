import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. HTML: inserir div#gs-month-filter antes de div#gs-cards
# ══════════════════════════════════════════════════════════════════
OLD_HTML = '    <div id="gs-cards" class="gs-cards"></div>'
NEW_HTML = (
    '    <div id="gs-month-filter" class="gs-month-filter"></div>\r\n'
    '    <div id="gs-cards" class="gs-cards"></div>'
)
if OLD_HTML in c:
    c = c.replace(OLD_HTML, NEW_HTML, 1)
    print('1 OK: HTML month filter div')
else:
    print('1 FAIL HTML')

# ══════════════════════════════════════════════════════════════════
# 2. CSS: estilos dos cards de mes
# ══════════════════════════════════════════════════════════════════
OLD_CSS = '.gs-gt-badge.ami{background:rgba(107,114,128,.15);color:var(--mu2);}'
NEW_CSS = (
    '.gs-gt-badge.ami{background:rgba(107,114,128,.15);color:var(--mu2);}\r\n'
    '.gs-month-filter{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid var(--bd);}\r\n'
    '.gs-month-card{background:var(--sf);border:2px solid var(--bd);border-radius:8px;padding:10px 14px;cursor:pointer;transition:all .18s;text-align:center;min-width:72px;user-select:none;}\r\n'
    '.gs-month-card:hover{border-color:var(--mu);}\r\n'
    '.gs-month-card.active{border-color:var(--usp);background:rgba(245,197,24,0.08);}\r\n'
    ".gm-name{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:16px;letter-spacing:1px;color:var(--tx);}\r\n"
    '.gm-year{font-size:9px;color:var(--mu);letter-spacing:1px;margin-top:1px;}\r\n'
    '.gm-stats{font-size:9px;color:var(--mu2);margin-top:3px;}'
)
if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS, 1)
    print('2 OK: CSS month cards')
else:
    print('2 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 3. JS: reescrever showGameSelector + adicionar filterByMonth/renderGsSections
# ══════════════════════════════════════════════════════════════════

# Novos globals e funcoes que vao ANTES de showGameSelector
MONTH_JS_PREFIX = (
    "var _gsMonthFilter=null;\r\n"
    "var _gsGamesCache=[];\r\n"
    "var _gsCompNamesCache=[];\r\n"
    "var _gsGameTypesCache=[];\r\n"
    "var _gsMyTeamCache='';\r\n"
    "\r\n"
    "var GS_MONTHS=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];\r\n"
    "\r\n"
    "function setGsMonth(key){\r\n"
    "  _gsMonthFilter=(key==='all')?null:key;\r\n"
    "  document.querySelectorAll('.gs-month-card').forEach(function(c){c.classList.toggle('active',c.dataset.month===(key||'all'));});\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function renderGsSections(){\r\n"
    "  var games=_gsGamesCache,compNames=_gsCompNamesCache,gameTypes=_gsGameTypesCache,myTeam=_gsMyTeamCache;\r\n"
    "  var indices=games.map(function(_,i){return i;});\r\n"
    "  if(_gsMonthFilter){\r\n"
    "    indices=indices.filter(function(i){\r\n"
    "      var d=(games[i].date||'').split('/');\r\n"
    "      return d.length===3&&(d[1]+'/'+d[2])===_gsMonthFilter;\r\n"
    "    });\r\n"
    "  }\r\n"
    "  var groups={},groupOrder=[],groupType={};\r\n"
    "  indices.forEach(function(i){\r\n"
    "    var key=compNames[i];\r\n"
    "    if(!groups[key]){groups[key]=[];groupOrder.push(key);groupType[key]=gameTypes[i];}\r\n"
    "    groups[key].push(i);\r\n"
    "  });\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
    "  if(!groupOrder.length){container.innerHTML='<div style=\"text-align:center;color:var(--mu);padding:48px 0;font-family:\\'Barlow Condensed\\',sans-serif;font-size:16px;\">Nenhum jogo neste periodo</div>';return;}\r\n"
    "  container.innerHTML=groupOrder.map(function(key){\r\n"
    "    var wins=groups[key].filter(function(i){var g=games[i],teams=g.teams||[];var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});if(ui<0)ui=0;var u=teams[ui]||{},a=teams[1-ui]||{};return (u.score||0)>(a.score||0);}).length;\r\n"
    "    var total=groups[key].length;\r\n"
    "    var gt=groupType[key]||'';\r\n"
    "    var badgeCls=(gt||'').toLowerCase().indexOf('comp')>=0?'comp':'ami';\r\n"
    "    var badgeHtml=gt?'<span class=\"gs-gt-badge '+badgeCls+'\">'+gt+'</span>':'';\r\n"
    "    var html='<div class=\"gs-section\"><div class=\"gs-section-title\">'+key+badgeHtml+'<span class=\"gs-section-count\">'+wins+'V '+(total-wins)+'D &nbsp;&middot;&nbsp; '+total+' jogo'+(total!==1?'s':'')+'</span></div><div class=\"gs-cards\">';\r\n"
    "    html+=groups[key].map(function(i){\r\n"
    "      var g=games[i],teams=g.teams||[];\r\n"
    "      var uspIdx=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "      if(uspIdx<0)uspIdx=0;\r\n"
    "      var advIdx=1-uspIdx;\r\n"
    "      var usp=teams[uspIdx]||{},adv=teams[advIdx]||{};\r\n"
    "      var uspPts=usp.score||0,advPts=adv.score||0;\r\n"
    "      var win=uspPts>advPts;\r\n"
    "      var advName=(adv.name||'?').trim();\r\n"
    "      var sel=_gsSelected[i]?'sel':'';\r\n"
    "      return '<div class=\"gs-card '+sel+'\" data-i=\"'+i+'\" onclick=\"toggleGameCard('+i+')\" title=\"'+(win?'Vitoria':'Derrota')+'\">'+'<div class=\"gs-chk\" id=\"gs-chk-'+i+'\"></div>'+'<span class=\"gc-badge '+(win?'w':'l')+'\">'+(win?'VITORIA':'DERROTA')+'</span>'+'<div class=\"gc-adv\">vs '+advName+'</div>'+'<div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)')+'\">'+uspPts+'</span><span style=\"color:var(--mu);font-size:14px;\"> x </span><span style=\"color:var(--tx);\">'+advPts+'</span></div>'+'<div class=\"gc-date\">'+(g.date||'')+'</div>'+'</div>';\r\n"
    "    }).join('');\r\n"
    "    html+='</div></div>';\r\n"
    "    return html;\r\n"
    "  }).join('');\r\n"
    "}\r\n"
    "\r\n"
)

NEW_SHOW = (
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
    "  _gsMonthFilter=null;\r\n"
    "  // ── Construir filtro de meses ──\r\n"
    "  var monthMap={};\r\n"
    "  games.forEach(function(g,i){\r\n"
    "    var d=(g.date||'').split('/');\r\n"
    "    if(d.length!==3)return;\r\n"
    "    var key=d[1]+'/'+d[2];\r\n"
    "    if(!monthMap[key]){monthMap[key]={wins:0,total:0,mo:parseInt(d[1],10),yr:parseInt(d[2],10)};}\r\n"
    "    var teams=g.teams||[];\r\n"
    "    var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "    if(ui<0)ui=0;\r\n"
    "    var u=teams[ui]||{},a=teams[1-ui]||{};\r\n"
    "    if((u.score||0)>(a.score||0))monthMap[key].wins++;\r\n"
    "    monthMap[key].total++;\r\n"
    "  });\r\n"
    "  var sortedMonths=Object.keys(monthMap).sort(function(a,b){var ma=monthMap[a],mb=monthMap[b];return ma.yr!==mb.yr?ma.yr-mb.yr:ma.mo-mb.mo;});\r\n"
    "  var mfEl=document.getElementById('gs-month-filter');\r\n"
    "  if(mfEl&&sortedMonths.length>1){\r\n"
    "    var html='<div class=\"gs-month-card active\" data-month=\"all\" onclick=\"setGsMonth(\\'all\\')\"><div class=\"gm-name\">Todos</div><div class=\"gm-stats\">'+games.length+' jogo'+(games.length!==1?'s':'')+'</div></div>';\r\n"
    "    html+=sortedMonths.map(function(k){\r\n"
    "      var m=monthMap[k];\r\n"
    "      var mname=GS_MONTHS[m.mo-1]||k;\r\n"
    "      return '<div class=\"gs-month-card\" data-month=\"'+k+'\" onclick=\"setGsMonth(\\''+k+'\\')\">'+'<div class=\"gm-name\">'+mname.toUpperCase()+'</div>'+'<div class=\"gm-year\">'+m.yr+'</div>'+'<div class=\"gm-stats\">'+m.wins+'V '+(m.total-m.wins)+'D</div>'+'</div>';\r\n"
    "    }).join('');\r\n"
    "    mfEl.style.display='';\r\n"
    "    mfEl.innerHTML=html;\r\n"
    "  } else if(mfEl){\r\n"
    "    mfEl.style.display='none';\r\n"
    "  }\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "  document.getElementById('login-overlay').style.display='none';\r\n"
    "  document.getElementById('game-selector').style.display='flex';\r\n"
    "}"
)

# Substituir a funcao showGameSelector via regex E injetar globals antes dela
pattern = r'function showGameSelector\(rawRows,session\)\{[\s\S]*?document\.getElementById\(\'game-selector\'\)\.style\.display=\'flex\';\r\n\}'
m = re.search(pattern, c)
if m:
    c = c[:m.start()] + MONTH_JS_PREFIX + NEW_SHOW + c[m.end():]
    print('3 OK: showGameSelector + filtro de meses + renderGsSections')
else:
    print('3 FAIL regex')
    idx = c.find('function showGameSelector')
    if idx >= 0:
        print('SNIPPET:', repr(c[idx:idx+100]))

# ══════════════════════════════════════════════════════════════════
# 4. selectAllGames / clearAllGames: re-renderizar apos mudar selecao
# ══════════════════════════════════════════════════════════════════
OLD_SEL_ALL = (
    "function selectAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return true;});\r\n"
    "  document.querySelectorAll('.gs-card').forEach(function(c){c.classList.add('sel');});\r\n"
    "  updateGsCount();\r\n"
    "}"
)
NEW_SEL_ALL = (
    "function selectAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return true;});\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}"
)
if OLD_SEL_ALL in c:
    c = c.replace(OLD_SEL_ALL, NEW_SEL_ALL, 1)
    print('4a OK: selectAllGames')
else:
    print('4a skip: selectAllGames (pode ja estar ok)')

OLD_CLR_ALL = (
    "function clearAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return false;});\r\n"
    "  document.querySelectorAll('.gs-card').forEach(function(c){c.classList.remove('sel');});\r\n"
    "  updateGsCount();\r\n"
    "}"
)
NEW_CLR_ALL = (
    "function clearAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return false;});\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}"
)
if OLD_CLR_ALL in c:
    c = c.replace(OLD_CLR_ALL, NEW_CLR_ALL, 1)
    print('4b OK: clearAllGames')
else:
    print('4b skip: clearAllGames (pode ja estar ok)')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
