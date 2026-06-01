import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('WinFast_App.html', 'rb') as f:
    c = f.read().decode('utf-8')

# ══════════════════════════════════════════════════════════════════
# 1. CSS — estilo do botão voltar
# ══════════════════════════════════════════════════════════════════
OLD_CSS = '.logout-btn{background:none;border:1px solid var(--bd);color:var(--mu2);padding:5px 12px;border-radius:4px;cursor:pointer;font-size:11px;font-family:\'Barlow\',sans-serif;letter-spacing:.5px;transition:all .2s;}'
NEW_CSS = (
    '.logout-btn{background:none;border:1px solid var(--bd);color:var(--mu2);padding:5px 12px;border-radius:4px;cursor:pointer;font-size:11px;font-family:\'Barlow\',sans-serif;letter-spacing:.5px;transition:all .2s;}\r\n'
    '.back-btn{background:none;border:1px solid var(--bd);color:var(--mu2);padding:5px 12px;border-radius:4px;cursor:pointer;font-size:11px;font-family:\'Barlow\',sans-serif;letter-spacing:.5px;transition:all .2s;display:flex;align-items:center;gap:5px;}\r\n'
    '.back-btn:hover{border-color:var(--usp);color:var(--usp);}'
)
if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS, 1)
    print('1 OK: CSS back-btn')
else:
    print('1 FAIL CSS')

# ══════════════════════════════════════════════════════════════════
# 2. HTML — inserir botão "← Selecionar jogos" no header
#    (antes do theme-toggle, logo depois da logo)
# ══════════════════════════════════════════════════════════════════
OLD_HDR = '  <button id="theme-toggle"'
NEW_HDR = (
    '  <button class="back-btn" onclick="backToSelector()" title="Voltar para seleção de jogos">\r\n'
    '    &#8592; Selecionar jogos\r\n'
    '  </button>\r\n'
    '  <button id="theme-toggle"'
)
if OLD_HDR in c:
    c = c.replace(OLD_HDR, NEW_HDR, 1)
    print('2 OK: botão voltar no header')
else:
    print('2 FAIL HTML')

# ══════════════════════════════════════════════════════════════════
# 3. JS — função backToSelector()
#    Inserir antes de function initDashboard
# ══════════════════════════════════════════════════════════════════
OLD_ANCHOR = 'function initDashboard(){'
NEW_ANCHOR = (
    "function backToSelector(){\r\n"
    "  document.getElementById('app-container').style.display='none';\r\n"
    "  document.getElementById('game-selector').style.display='flex';\r\n"
    "  // Re-renderizar seletor com dados ja em memoria\r\n"
    "  renderGsSections();\r\n"
    "  updateGsCount();\r\n"
    "}\r\n"
    "\r\n"
    "function initDashboard(){"
)
if OLD_ANCHOR in c:
    c = c.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    print('3 OK: backToSelector()')
else:
    print('3 FAIL JS anchor')

# ══════════════════════════════════════════════════════════════════
with open('WinFast_App.html', 'wb') as f:
    f.write(c.encode('utf-8'))
print('\nFILE SAVED')
