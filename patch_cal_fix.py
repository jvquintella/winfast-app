import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. Corrigir click-outside handler: usar composedPath para nao fechar
#    o dropdown quando o target foi removido do DOM pelo innerHTML update
# ══════════════════════════════════════════════════════════════════
OLD_CLICK = (
    "document.addEventListener('click',function(e){\r\n"
    "  var wrap=document.getElementById('gs-period-wrap');\r\n"
    "  if(wrap&&!wrap.contains(e.target))closeGsPeriod();\r\n"
    "});"
)
NEW_CLICK = (
    "document.addEventListener('click',function(e){\r\n"
    "  var wrap=document.getElementById('gs-period-wrap');\r\n"
    "  if(!wrap)return;\r\n"
    "  // composedPath captura o caminho ANTES de qualquer mutacao do DOM\r\n"
    "  var path=e.composedPath?e.composedPath():[];\r\n"
    "  var inside=path.indexOf(wrap)>=0||wrap.contains(e.target);\r\n"
    "  if(!inside)closeGsPeriod();\r\n"
    "});"
)
if OLD_CLICK in c:
    c = c.replace(OLD_CLICK, NEW_CLICK, 1)
    print('1 OK: click-outside fix (composedPath)')
else:
    print('1 FAIL click-outside')

# ══════════════════════════════════════════════════════════════════
# 2. Aumentar largura do dropdown quando exibindo calendario
#    e melhorar tamanho dos dias
# ══════════════════════════════════════════════════════════════════
OLD_PERIOD_CSS = '.gs-period-dd{position:absolute;top:calc(100% + 8px);left:0;background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:6px;min-width:230px;z-index:200;box-shadow:0 8px 24px rgba(0,0,0,.5);}'
NEW_PERIOD_CSS = '.gs-period-dd{position:absolute;top:calc(100% + 8px);left:0;background:var(--sf);border:1px solid var(--bd);border-radius:10px;padding:8px;min-width:240px;width:max-content;z-index:200;box-shadow:0 8px 24px rgba(0,0,0,.5);}'
if OLD_PERIOD_CSS in c:
    c = c.replace(OLD_PERIOD_CSS, NEW_PERIOD_CSS, 1)
    print('2 OK: dropdown width fix')
else:
    print('2 skip: dropdown width (pode ja estar diferente)')

OLD_CAL_DAY = '.gs-cal-day{text-align:center;padding:3px 1px;border-radius:5px;min-height:32px;font-family:\'Barlow Condensed\',sans-serif;font-size:12px;color:var(--mu2);cursor:default;}'
NEW_CAL_DAY = '.gs-cal-day{text-align:center;padding:4px 2px;border-radius:5px;min-height:36px;font-family:\'Barlow Condensed\',sans-serif;font-size:13px;color:var(--mu2);cursor:default;}'
if OLD_CAL_DAY in c:
    c = c.replace(OLD_CAL_DAY, NEW_CAL_DAY, 1)
    print('3 OK: cal day size')
else:
    print('3 skip: cal day size')

OLD_CAL_GRID = '.gs-cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;}'
NEW_CAL_GRID = '.gs-cal-grid{display:grid;grid-template-columns:repeat(7,32px);gap:2px;}'
if OLD_CAL_GRID in c:
    c = c.replace(OLD_CAL_GRID, NEW_CAL_GRID, 1)
    print('4 OK: cal grid fixed columns')
else:
    print('4 skip: cal grid')

OLD_CAL_DOT = '.gs-cal-dot{width:5px;height:5px;border-radius:50%;}'
NEW_CAL_DOT = '.gs-cal-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}'
if OLD_CAL_DOT in c:
    c = c.replace(OLD_CAL_DOT, NEW_CAL_DOT, 1)
    print('5 OK: cal dot size')
else:
    print('5 skip: cal dot')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
