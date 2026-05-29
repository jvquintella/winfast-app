import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS: badge de gametype na secao
# ══════════════════════════════════════════════════════════════════
OLD_CSS = '.gs-section-count{font-size:10px;color:var(--mu);font-weight:400;letter-spacing:.5px;text-transform:none;}'
NEW_CSS = (
    '.gs-section-count{font-size:10px;color:var(--mu);font-weight:400;letter-spacing:.5px;text-transform:none;}\r\n'
    '.gs-gt-badge{font-size:9px;font-weight:700;letter-spacing:1px;padding:2px 8px;border-radius:3px;text-transform:uppercase;margin-left:8px;}\r\n'
    ".gs-gt-badge.comp{background:rgba(59,130,246,.15);color:var(--bl);}\r\n"
    ".gs-gt-badge.ami{background:rgba(107,114,128,.15);color:var(--mu2);}"
)
if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS, 1)
    print('1 OK: CSS badge gametype')
else:
    print('1 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 2. Atualizar showGameSelector — usar competitionName como chave
#    e gametype como badge
# ══════════════════════════════════════════════════════════════════
NEW_SHOW = (
    "function showGameSelector(rawRows,session){\r\n"
    "  _gsRawRows=rawRows;_gsSession=session;\r\n"
    "  var allGames=rawRows.filter(function(r){return (r[SB_COL]||r.data||{}).finished;});\r\n"
    "  allGames.sort(function(a,b){var ga=a[SB_COL]||a.data||{},gb=b[SB_COL]||b.data||{};return parseDt(ga.date)-parseDt(gb.date);});\r\n"
    "  var games=allGames.map(function(r){return r[SB_COL]||r.data;});\r\n"
    "  var gameTypes=allGames.map(function(r){return r.gametype||(r[SB_COL]||r.data||{}).gametype||'';});\r\n"
    "  var compNames=allGames.map(function(r,i){\r\n"
    "    var cn=r.competitionName||(r[SB_COL]||r.data||{}).competitionName||'';\r\n"
    "    return cn||gameTypes[i]||'Sem Competição';\r\n"
    "  });\r\n"
    "  var myTeam=detectMyTeam(games);\r\n"
    "  _gsSelected=games.map(function(){return true;});\r\n"
    "  // Agrupar por competitionName\r\n"
    "  var groups={},groupOrder=[],groupType={};\r\n"
    "  games.forEach(function(g,i){\r\n"
    "    var key=compNames[i];\r\n"
    "    if(!groups[key]){groups[key]=[];groupOrder.push(key);groupType[key]=gameTypes[i];}\r\n"
    "    groups[key].push(i);\r\n"
    "  });\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
    "  container.innerHTML=groupOrder.map(function(key){\r\n"
    "    var wins=groups[key].filter(function(i){\r\n"
    "      var g=games[i],teams=g.teams||[];\r\n"
    "      var ui=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "      if(ui<0)ui=0;\r\n"
    "      var u=teams[ui]||{},a=teams[1-ui]||{};\r\n"
    "      return (u.score||0)>(a.score||0);\r\n"
    "    }).length;\r\n"
    "    var total=groups[key].length;\r\n"
    "    var gt=groupType[key]||'';\r\n"
    "    var gtLower=(gt||'').toLowerCase();\r\n"
    "    var badgeCls=gtLower.indexOf('comp')>=0?'comp':'ami';\r\n"
    "    var badgeHtml=gt?'<span class=\"gs-gt-badge '+badgeCls+'\">'+gt+'</span>':'';\r\n"
    "    var html='<div class=\"gs-section\">';\r\n"
    "    html+='<div class=\"gs-section-title\">'+key+badgeHtml\r\n"
    "      +'<span class=\"gs-section-count\">'+wins+'V '+(total-wins)+'D &nbsp;·&nbsp; '+total+' jogo'+(total!==1?'s':'')+'</span></div>';\r\n"
    "    html+='<div class=\"gs-cards\">';\r\n"
    "    html+=groups[key].map(function(i){\r\n"
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
    "        +'<div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)')+'\">'+uspPts+'</span>'\\r\\n"
    "        +'<span style=\"color:var(--mu);font-size:14px;\"> × </span>'\\r\\n"
    "        +'<span style=\"color:var(--tx);\">'+advPts+'</span></div>'\\r\\n"
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

pattern = r'function showGameSelector\(rawRows,session\)\{[\s\S]*?document\.getElementById\(\'game-selector\'\)\.style\.display=\'flex\';\r\n\}'
m = re.search(pattern, c)
if m:
    c = c[:m.start()] + NEW_SHOW + c[m.end():]
    print('2 OK: showGameSelector agrupa por competitionName + badge gametype')
else:
    print('2 FAIL regex')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
