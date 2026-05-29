import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS do seletor de jogos
# ══════════════════════════════════════════════════════════════════
OLD_CSS_END = '#app-container{display:none;}'
NEW_CSS_END = (
    '#app-container{display:none;}\r\n'
    '#game-selector{position:fixed;inset:0;background:var(--bg);z-index:9998;display:none;flex-direction:column;overflow-y:auto;}\r\n'
    '.gs-header{background:var(--sf);border-bottom:2px solid var(--usp);padding:20px 32px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;position:sticky;top:0;z-index:2;}\r\n'
    '.gs-body{padding:28px 32px;max-width:1100px;margin:0 auto;width:100%;}\r\n'
    '.gs-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:12px;margin-bottom:28px;}\r\n'
    '.gs-card{background:var(--sf);border:2px solid var(--bd);border-radius:10px;padding:16px;cursor:pointer;transition:all .18s;user-select:none;position:relative;}\r\n'
    '.gs-card:hover{border-color:var(--mu);}\r\n'
    '.gs-card.sel{border-color:var(--usp);background:rgba(245,197,24,0.05);}\r\n'
    '.gc-badge{font-family:\'Barlow Condensed\',sans-serif;font-weight:800;font-size:10px;letter-spacing:1px;padding:2px 8px;border-radius:3px;display:inline-block;margin-bottom:10px;}\r\n'
    '.gc-badge.w{background:rgba(34,197,94,.15);color:var(--gr);}\r\n'
    '.gc-badge.l{background:rgba(239,68,68,.15);color:var(--rd);}\r\n'
    '.gc-adv{font-weight:600;font-size:14px;margin-bottom:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--tx);}\r\n'
    '.gc-score{font-family:\'Barlow Condensed\',sans-serif;font-size:24px;font-weight:900;margin-bottom:5px;line-height:1;}\r\n'
    '.gc-date{font-size:10px;color:var(--mu);letter-spacing:.5px;}\r\n'
    '.gs-chk{position:absolute;top:12px;right:12px;width:18px;height:18px;border-radius:50%;border:2px solid var(--bd);transition:all .18s;}\r\n'
    '.gs-card.sel .gs-chk{background:var(--usp);border-color:var(--usp);}\r\n'
    '.gs-card.sel .gs-chk::after{content:\'\';display:block;width:5px;height:9px;border:2px solid #000;border-top:none;border-left:none;transform:rotate(45deg) translate(1px,-1px);margin:1px auto;}\r\n'
    '.gs-btn-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}\r\n'
    '.gs-action-btn{background:none;border:1px solid var(--bd);color:var(--mu2);padding:6px 14px;border-radius:6px;cursor:pointer;font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;transition:all .18s;}\r\n'
    '.gs-action-btn:hover{border-color:var(--mu);color:var(--tx);}\r\n'
    '#gs-count{font-size:12px;color:var(--mu);font-family:\'Barlow Condensed\',sans-serif;letter-spacing:.5px;}\r\n'
    '#gs-gen-btn{background:var(--usp);color:#000;border:none;border-radius:8px;padding:14px 40px;font-family:\'Barlow Condensed\',sans-serif;font-weight:900;font-size:16px;letter-spacing:2px;text-transform:uppercase;cursor:pointer;transition:opacity .2s;display:flex;align-items:center;gap:10px;}\r\n'
    '#gs-gen-btn:hover{opacity:.85;}#gs-gen-btn:disabled{opacity:.4;cursor:default;}\r\n'
    '@media(max-width:768px){.gs-header{padding:14px 16px;}.gs-body{padding:16px;}}'
)
if OLD_CSS_END in c:
    c = c.replace(OLD_CSS_END, NEW_CSS_END, 1)
    print('1 OK: CSS do seletor')
else:
    print('1 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 2. HTML do overlay de seleção (inserir antes de </body>... na verdade
#    inserir logo após o div#login-overlay)
# ══════════════════════════════════════════════════════════════════
OLD_AFTER_LOGIN = '<div id="app-container">'
NEW_AFTER_LOGIN = (
    '<!-- ── SELETOR DE JOGOS ───────────────────────────────────────── -->\r\n'
    '<div id="game-selector">\r\n'
    '  <div class="gs-header">\r\n'
    '    <div>\r\n'
    '      <div style="font-family:\'Barlow Condensed\',sans-serif;font-weight:900;font-size:22px;letter-spacing:2px;color:var(--usp);">WIN<span style="color:var(--tx);">FAST</span></div>\r\n'
    '      <div style="font-size:10px;color:var(--mu);letter-spacing:2px;text-transform:uppercase;margin-top:2px;">Selecione os jogos para analisar</div>\r\n'
    '    </div>\r\n'
    '    <div class="gs-btn-row">\r\n'
    '      <button class="gs-action-btn" onclick="selectAllGames()">Todos</button>\r\n'
    '      <button class="gs-action-btn" onclick="clearAllGames()">Nenhum</button>\r\n'
    '      <span id="gs-count">0 selecionados</span>\r\n'
    '    </div>\r\n'
    '  </div>\r\n'
    '  <div class="gs-body">\r\n'
    '    <div id="gs-cards" class="gs-cards"></div>\r\n'
    '    <div style="display:flex;justify-content:center;padding-bottom:32px;">\r\n'
    '      <button id="gs-gen-btn" onclick="generateReport()" disabled>\r\n'
    '        Gerar Relatório &nbsp;&#8594;\r\n'
    '      </button>\r\n'
    '    </div>\r\n'
    '  </div>\r\n'
    '</div>\r\n'
    '\r\n'
    '<div id="app-container">'
)
if OLD_AFTER_LOGIN in c:
    c = c.replace(OLD_AFTER_LOGIN, NEW_AFTER_LOGIN, 1)
    print('2 OK: HTML overlay seletor')
else:
    print('2 FAIL HTML')

# ══════════════════════════════════════════════════════════════════
# 3. JS: showGameSelector, toggleGameCard, selectAllGames,
#        clearAllGames, updateGsCount, generateReport
#    Inserir antes de function renderPL
# ══════════════════════════════════════════════════════════════════
SELECTOR_JS = (
    "/* ── SELETOR DE JOGOS ──────────────────────────────────────────── */\r\n"
    "var _gsRawRows=[];\r\n"
    "var _gsSession=null;\r\n"
    "var _gsSelected=[];\r\n"
    "\r\n"
    "function showGameSelector(rawRows,session){\r\n"
    "  _gsRawRows=rawRows;_gsSession=session;\r\n"
    "  var allGames=rawRows.filter(function(r){return (r[SB_COL]||r.data||{}).finished;});\r\n"
    "  allGames.sort(function(a,b){var ga=a[SB_COL]||a.data||{},gb=b[SB_COL]||b.data||{};return parseDt(ga.date)-parseDt(gb.date);});\r\n"
    "  var games=allGames.map(function(r){return r[SB_COL]||r.data;});\r\n"
    "  var myTeam=detectMyTeam(games);\r\n"
    "  _gsSelected=games.map(function(){return true;});\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
    "  container.innerHTML=games.map(function(g,i){\r\n"
    "    var teams=g.teams||[];\r\n"
    "    var uspIdx=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "    if(uspIdx<0)uspIdx=0;\r\n"
    "    var advIdx=1-uspIdx;\r\n"
    "    var usp=teams[uspIdx]||{},adv=teams[advIdx]||{};\r\n"
    "    var uspPts=usp.score||0,advPts=adv.score||0;\r\n"
    "    var win=uspPts>advPts;\r\n"
    "    var advName=(adv.name||'?').trim();\r\n"
    "    return '<div class=\"gs-card sel\" data-i=\"'+i+'\" onclick=\"toggleGameCard('+i+')\" title=\"'+(win?'Vitória':'Derrota')+'\">'\r\n"
    "      +'<div class=\"gs-chk\" id=\"gs-chk-'+i+'\"></div>'\r\n"
    "      +'<span class=\"gc-badge '+(win?'w':'l')+'\">'+(win?'VITÓRIA':'DERROTA')+'</span>'\r\n"
    "      +'<div class=\"gc-adv\">vs '+advName+'</div>'\r\n"
    "      +'<div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)')+'\">'+uspPts+'</span>'\r\n"
    "      +'<span style=\"color:var(--mu);font-size:14px;\"> × </span>'\r\n"
    "      +'<span style=\"color:var(--tx);\">'+advPts+'</span></div>'\r\n"
    "      +'<div class=\"gc-date\">'+( g.date||'')+'</div>'\r\n"
    "      +'</div>';\r\n"
    "  }).join('');\r\n"
    "  updateGsCount();\r\n"
    "  document.getElementById('login-overlay').style.display='none';\r\n"
    "  document.getElementById('game-selector').style.display='flex';\r\n"
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
    "  document.querySelectorAll('.gs-card').forEach(function(c){c.classList.add('sel');});\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function clearAllGames(){\r\n"
    "  _gsSelected=_gsSelected.map(function(){return false;});\r\n"
    "  document.querySelectorAll('.gs-card').forEach(function(c){c.classList.remove('sel');});\r\n"
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
    "/* ─────────────────────────────────────────────────────────────── */\r\n"
)

OLD_RPL = 'function refreshCmpSelectors(){'
if OLD_RPL in c:
    c = c.replace(OLD_RPL, SELECTOR_JS + OLD_RPL, 1)
    print('3 OK: JS do seletor')
else:
    print('3 FAIL JS anchor')

# ══════════════════════════════════════════════════════════════════
# 4. loadUserGames: trocar processGames(data) por showGameSelector
# ══════════════════════════════════════════════════════════════════
OLD_LOAD = (
    "    msg.textContent='';\r\n"
    "    processGames(data||[]);\r\n"
    "    // Mostrar info do usuário no header\r\n"
    "    var email=(session&&session.user&&session.user.email)||'';\r\n"
    "    var badge=document.getElementById('user-badge');\r\n"
    "    if(badge)badge.textContent=email;"
)
NEW_LOAD = (
    "    msg.textContent='';\r\n"
    "    showGameSelector(data||[],session);"
)
if OLD_LOAD in c:
    c = c.replace(OLD_LOAD, NEW_LOAD, 1)
    print('4 OK: loadUserGames atualizado')
else:
    print('4 FAIL loadUserGames')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
