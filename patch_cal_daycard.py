import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS — mini-card do jogo no calendário
# ══════════════════════════════════════════════════════════════════
OLD_CAL_DOT = '.gs-cal-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}'
NEW_CAL_DOT = (
    '.gs-cal-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}\r\n'
    '.gs-cal-day-games{border-top:1px solid var(--bd);margin-top:8px;padding-top:8px;}\r\n'
    '.gs-cal-day-label{font-family:\'Barlow Condensed\',sans-serif;font-size:10px;letter-spacing:1px;color:var(--mu);text-transform:uppercase;margin-bottom:6px;}\r\n'
    '.gs-cal-game{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:7px;cursor:pointer;transition:background .15s;border:1px solid var(--bd);margin-bottom:4px;background:var(--sf2);}\r\n'
    '.gs-cal-game:hover{background:var(--sf);border-color:var(--mu);}\r\n'
    '.gs-cal-chk{width:18px;height:18px;border-radius:50%;border:2px solid var(--bd);flex-shrink:0;transition:all .18s;margin-left:auto;background:var(--bg);}\r\n'
    '.gs-cal-chk.sel{background:var(--usp);border-color:var(--usp);}\r\n'
    '.gs-cal-chk.sel::after{content:\'\';display:block;width:5px;height:8px;border:2px solid #000;border-top:none;border-left:none;transform:rotate(45deg) translate(1px,-1px);margin:1px auto 0;}'
)
if OLD_CAL_DOT in c:
    c = c.replace(OLD_CAL_DOT, NEW_CAL_DOT, 1)
    print('1 OK: CSS day-game card')
else:
    print('1 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 2. JS — reescrever showGsCalendar + setGsDay + toggleCalDayGame
# ══════════════════════════════════════════════════════════════════
OLD_SHOW_CAL = (
    "function showGsCalendar(monthKey){\r\n"
    "  _gsCalMonth=monthKey;_gsMonthFilter=monthKey;_gsDayFilter=null;"
)
NEW_SHOW_CAL = "function showGsCalendar(monthKey,keepDay){\r\n  _gsCalMonth=monthKey;_gsMonthFilter=monthKey;if(!keepDay)_gsDayFilter=null;"

if OLD_SHOW_CAL in c:
    c = c.replace(OLD_SHOW_CAL, NEW_SHOW_CAL, 1)
    print('2a OK: showGsCalendar keepDay param')
else:
    print('2a FAIL showGsCalendar param')

# Adicionar mini-cards antes do fechamento do html
OLD_CAL_END = (
    "  html+='</div></div>';\r\n"
    "  var dd3=document.getElementById('gs-period-dd');\r\n"
    "  if(dd3){dd3.style.display='';dd3.innerHTML=html;}"
)
NEW_CAL_END = (
    "  html+='</div></div>';\r\n"
    "  // Mini-cards do dia selecionado\r\n"
    "  if(_gsDayFilter){\r\n"
    "    var dfp=_gsDayFilter.split('/'),dfDd=dfp[0],dfMo=dfp[1],dfYr=dfp[2];\r\n"
    "    var dayIdxs=[];\r\n"
    "    games.forEach(function(g,i){\r\n"
    "      var d=(g.date||'').split('/');\r\n"
    "      if(d[0]===dfDd&&d[1]===dfMo&&d[2]===dfYr)dayIdxs.push(i);\r\n"
    "    });\r\n"
    "    if(dayIdxs.length){\r\n"
    "      html+='<div class=\"gs-cal-day-games\">';\r\n"
    "      html+='<div class=\"gs-cal-day-label\">'+_gsDayFilter+'</div>';\r\n"
    "      html+=dayIdxs.map(function(i){\r\n"
    "        var g=games[i],teams=g.teams||[];\r\n"
    "        var uspIdx=teams.findIndex(function(t){return (t.name||'').trim()===myTeam.trim();});\r\n"
    "        if(uspIdx<0)uspIdx=0;\r\n"
    "        var adv=teams[1-uspIdx]||{},usp=teams[uspIdx]||{};\r\n"
    "        var uspPts=usp.score||0,advPts=adv.score||0,win=uspPts>advPts;\r\n"
    "        var advName=(adv.name||'?').trim(),isSel=!!_gsSelected[i];\r\n"
    "        var col=gsCompColor(compNames[i]);\r\n"
    "        return '<div class=\"gs-cal-game\" onclick=\"toggleCalDayGame('+i+')\">'+'<div style=\"width:8px;height:8px;border-radius:50%;background:'+col+';flex-shrink:0;\"></div>'+'<span class=\"gc-badge '+(win?'w':'l')+'\" style=\"margin-bottom:0;padding:1px 6px;\">'+(win?'V':'D')+'</span>'+'<span style=\"font-size:12px;color:var(--tx);flex:1;\">vs '+advName+'</span>'+'<span style=\"font-family:\\'Barlow Condensed\\',sans-serif;font-weight:900;font-size:14px;color:'+(win?'var(--gr)':'var(--rd)')+'\">'+uspPts+'<span style=\"color:var(--mu);font-size:10px;margin:0 2px;\">x</span>'+advPts+'</span>'+'<div class=\"gs-cal-chk'+(isSel?' sel':'')+'\"></div>'+'</div>';\r\n"
    "      }).join('');\r\n"
    "      html+='</div>';\r\n"
    "    }\r\n"
    "  }\r\n"
    "  var dd3=document.getElementById('gs-period-dd');\r\n"
    "  if(dd3){dd3.style.display='';dd3.innerHTML=html;}"
)
if OLD_CAL_END in c:
    c = c.replace(OLD_CAL_END, NEW_CAL_END, 1)
    print('2b OK: day games mini-cards')
else:
    print('2b FAIL cal end anchor')

# Também precisamos que myTeam e compNames estejam disponíveis no escopo da renderização do calendário
# Verificar se a variavel myTeam já existe no showGsCalendar
# (existe como _gsMyTeamCache)

# Substituir referência da variável no bloco novo (já usamos games e compNames acima)
# Precisamos garantir que 'myTeam' e 'compNames' estão definidos antes do bloco
# No showGsCalendar, games=_gsGamesCache e compNames=_gsCompNamesCache já estão presentes

# Verificar se compNames está definido no início da função
idx_show = c.find('function showGsCalendar(monthKey,keepDay){')
if idx_show >= 0:
    # Checar se compNames está definido
    snippet = c[idx_show:idx_show+300]
    if 'compNames' not in snippet:
        print('2c WARN: compNames nao encontrado no inicio da funcao — adicionando')
        OLD_GAMES_LINE = "  var games=_gsGamesCache,compNames=_gsCompNamesCache,dayMap={};"
        if OLD_GAMES_LINE not in c[idx_show:idx_show+500]:
            # Adicionar compNames
            OLD_GAMES_ONLY = "  var games=_gsGamesCache,dayMap={};"
            NEW_GAMES_ONLY = "  var games=_gsGamesCache,compNames=_gsCompNamesCache,myTeam=_gsMyTeamCache,dayMap={};"
            if OLD_GAMES_ONLY in c:
                c = c.replace(OLD_GAMES_ONLY, NEW_GAMES_ONLY, 1)
                print('2c OK: adicionou compNames/myTeam')
            else:
                print('2c skip: variavel games ja tem compNames')
        else:
            print('2c OK: compNames ja presente')
    else:
        print('2c OK: compNames presente')

# Corrigir setGsDay para usar keepDay=true
OLD_SET_DAY = (
    "function setGsDay(dayKey){\r\n"
    "  _gsDayFilter=(_gsDayFilter===dayKey)?null:dayKey;\r\n"
    "  if(_gsCalMonth)showGsCalendar(_gsCalMonth);\r\n"
    "  renderGsSections();"
)
NEW_SET_DAY = (
    "function setGsDay(dayKey){\r\n"
    "  _gsDayFilter=(_gsDayFilter===dayKey)?null:dayKey;\r\n"
    "  if(_gsCalMonth)showGsCalendar(_gsCalMonth,true);\r\n"
    "  renderGsSections();"
)
if OLD_SET_DAY in c:
    c = c.replace(OLD_SET_DAY, NEW_SET_DAY, 1)
    print('2d OK: setGsDay usa keepDay=true')
else:
    print('2d FAIL setGsDay')

# Adicionar toggleCalDayGame antes de showGsPeriodMonths
OLD_SHOW_MONTHS = "function showGsPeriodMonths(){"
NEW_SHOW_MONTHS = (
    "function toggleCalDayGame(i){\r\n"
    "  _gsSelected[i]=!_gsSelected[i];\r\n"
    "  updateGsCount();\r\n"
    "  if(_gsCalMonth)showGsCalendar(_gsCalMonth,true);\r\n"
    "  renderGsSections();\r\n"
    "}\r\n"
    "\r\n"
    "function showGsPeriodMonths(){"
)
if OLD_SHOW_MONTHS in c:
    c = c.replace(OLD_SHOW_MONTHS, NEW_SHOW_MONTHS, 1)
    print('2e OK: toggleCalDayGame adicionado')
else:
    print('2e FAIL toggleCalDayGame anchor')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
