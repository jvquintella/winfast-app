import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS: section title + override outer #gs-cards to block layout
# ══════════════════════════════════════════════════════════════════
OLD_CSS = '.gc-date{font-size:10px;color:var(--mu);letter-spacing:.5px;}'
NEW_CSS = (
    '.gc-date{font-size:10px;color:var(--mu);letter-spacing:.5px;}\r\n'
    '#gs-cards{display:block!important;}\r\n'
    '.gs-section{margin-bottom:28px;}\r\n'
    ".gs-section-title{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:13px;"
    'letter-spacing:2px;text-transform:uppercase;color:var(--usp);margin-bottom:10px;'
    'padding-bottom:8px;border-bottom:1px solid var(--bd);display:flex;align-items:center;'
    'justify-content:space-between;}\r\n'
    '.gs-section-count{font-size:10px;color:var(--mu);font-weight:400;letter-spacing:.5px;text-transform:none;}'
)
if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS, 1)
    print('1 OK: CSS section titles')
else:
    print('1 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 2. Replace showGameSelector via regex — agrupar por gametype
# ══════════════════════════════════════════════════════════════════
NEW_SHOW = (
    "function showGameSelector(rawRows,session){\r\n"
    "  _gsRawRows=rawRows;_gsSession=session;\r\n"
    "  var allGames=rawRows.filter(function(r){return (r[SB_COL]||r.data||{}).finished;});\r\n"
    "  allGames.sort(function(a,b){var ga=a[SB_COL]||a.data||{},gb=b[SB_COL]||b.data||{};return parseDt(ga.date)-parseDt(gb.date);});\r\n"
    "  var games=allGames.map(function(r){return r[SB_COL]||r.data;});\r\n"
    "  var gameTypes=allGames.map(function(r){return r.gametype||(r[SB_COL]||r.data||{}).gametype||'Sem Competição';});\r\n"
    "  var myTeam=detectMyTeam(games);\r\n"
    "  _gsSelected=games.map(function(){return true;});\r\n"
    "  // Agrupar por competicao\r\n"
    "  var groups={},groupOrder=[];\r\n"
    "  games.forEach(function(g,i){\r\n"
    "    var gt=gameTypes[i];\r\n"
    "    if(!groups[gt]){groups[gt]=[];groupOrder.push(gt);}\r\n"
    "    groups[gt].push(i);\r\n"
    "  });\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
    "  container.innerHTML=groupOrder.map(function(gt){\r\n"
    "    var wins=groups[gt].filter(function(i){\r\n"
    "      var g=games[i],teams=g.teams||[];\r\n"
    "      var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "      if(ui<0)ui=0;\r\n"
    "      var u=teams[ui]||{},a=teams[1-ui]||{};\r\n"
    "      return (u.score||0)>(a.score||0);\r\n"
    "    }).length;\r\n"
    "    var total=groups[gt].length;\r\n"
    "    var html='<div class=\"gs-section\">';\r\n"
    "    html+='<div class=\"gs-section-title\">'+gt\r\n"
    "      +'<span class=\"gs-section-count\">'+wins+'V '+(total-wins)+'D &nbsp;·&nbsp; '+total+' jogo'+(total!==1?'s':'')+'</span></div>';\r\n"
    "    html+='<div class=\"gs-cards\">';\r\n"
    "    html+=groups[gt].map(function(i){\r\n"
    "      var g=games[i];\r\n"
    "      var teams=g.teams||[];\r\n"
    "      var uspIdx=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "      if(uspIdx<0)uspIdx=0;\r\n"
    "      var advIdx=1-uspIdx;\r\n"
    "      var usp=teams[uspIdx]||{},adv=teams[advIdx]||{};\r\n"
    "      var uspPts=usp.score||0,advPts=adv.score||0;\r\n"
    "      var win=uspPts>advPts;\r\n"
    "      var advName=(adv.name||'?').trim();\r\n"
    "      return '<div class=\"gs-card sel\" data-i=\"'+i+'\" onclick=\"toggleGameCard('+i+')\" title=\"'+(win?'Vitória':'Derrota')+'\">'\\r\\n"
    "        +'<div class=\"gs-chk\" id=\"gs-chk-'+i+'\"></div>'\\r\\n"
    "        +'<span class=\"gc-badge '+(win?'w':'l')+'\">'+(win?'VITÓRIA':'DERROTA')+'</span>'\\r\\n"
    "        +'<div class=\"gc-adv\">vs '+advName+'</div>'\\r\\n"
    "        +'<div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)')+'\">'+ uspPts+'</span>'\\r\\n"
    "        +'<span style=\"color:var(--mu);font-size:14px;\"> × </span>'\\r\\n"
    "        +'<span style=\"color:var(--tx);\">'+ advPts+'</span></div>'\\r\\n"
    "        +'<div class=\"gc-date\">'+(g.date||'')+'</div>'\\r\\n"
    "        +'</div>';\r\n"
    "    }).join('');\r\n"
    "    html+='</div></div>';\r\n"
    "    return html;\r\n"
    "  }).join('');\r\n"
    "  updateGsCount();\r\n"
    "  document.getElementById('login-overlay').style.display='none';\r\n"
    "  document.getElementById('game-selector').style.display='flex';\r\n"
    "}"
)

# Usar regex para substituir a funcao inteira
pattern = r'function showGameSelector\(rawRows,session\)\{[\s\S]*?document\.getElementById\(\'game-selector\'\)\.style\.display=\'flex\';\r\n\}'
m = re.search(pattern, c)
if m:
    c = c[:m.start()] + NEW_SHOW + c[m.end():]
    print('2 OK: showGameSelector com grupos por gametype')
else:
    print('2 FAIL regex nao encontrou a funcao')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
