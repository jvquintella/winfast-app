import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# Reescrever showGameSelector — card return em UMA LINHA (sem \r\n no meio)
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
    "    return cn||gameTypes[i]||'Sem Competicao';\r\n"
    "  });\r\n"
    "  var myTeam=detectMyTeam(games);\r\n"
    "  _gsSelected=games.map(function(){return true;});\r\n"
    "  var groups={},groupOrder=[],groupType={};\r\n"
    "  games.forEach(function(g,i){\r\n"
    "    var key=compNames[i];\r\n"
    "    if(!groups[key]){groups[key]=[];groupOrder.push(key);groupType[key]=gameTypes[i];}\r\n"
    "    groups[key].push(i);\r\n"
    "  });\r\n"
    "  var container=document.getElementById('gs-cards');\r\n"
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
    "      return '<div class=\"gs-card sel\" data-i=\"'+i+'\" onclick=\"toggleGameCard('+i+')\" title=\"'+(win?'Vitoria':'Derrota')+'\"><div class=\"gs-chk\" id=\"gs-chk-'+i+'\"></div><span class=\"gc-badge '+(win?'w':'l')+'\">'+(win?'VITORIA':'DERROTA')+'</span><div class=\"gc-adv\">vs '+advName+'</div><div class=\"gc-score\"><span style=\"color:'+(win?'var(--gr)':'var(--rd)')+'\">'+ uspPts+'</span><span style=\"color:var(--mu);font-size:14px;\"> x </span><span style=\"color:var(--tx);\">'+ advPts+'</span></div><div class=\"gc-date\">'+(g.date||'')+'</div></div>';\r\n"
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
    print('OK: showGameSelector reescrita sem \\r\\n embutido')
else:
    print('FAIL: regex nao encontrou a funcao')
    idx = c.find('function showGameSelector')
    if idx >= 0:
        print('SNIPPET:', repr(c[idx:idx+80]))

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
