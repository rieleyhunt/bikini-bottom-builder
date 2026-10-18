"""Build the editor: dist/bikini-bottom-builder.html (web), dist/BikiniBottomBuilder-local.html (offline),
and ../desktop/index.html (embedded into the .exe). Run `npm install` here first for the fonts."""
import base64, os
D = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f'{D}/dist', exist_ok=True)
core = open(f'{D}/core.js').read() + '\n' + open(f'{D}/objinfo.js').read()
app = open(f'{D}/app.html').read().replace('/*__CORE__*/', core)
open(f'{D}/dist/bikini-bottom-builder.html', 'w').write(app)
open(f'{D}/dist/BikiniBottomBuilder-local.html', 'w').write('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>' + app + '</body></html>')
# desktop build: embedded fonts, desktop flag, heartbeat
F = f'{D}/node_modules'
arch = base64.b64encode(open(f'{F}/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2', 'rb').read()).decode()
silk = base64.b64encode(open(f'{F}/@fontsource/silkscreen/files/silkscreen-latin-400-normal.woff2', 'rb').read()).decode()
fonts = ('<style>@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,' + arch + ') format("woff2");font-weight:100 900;font-stretch:62% 125%;font-display:block}'
         '@font-face{font-family:"Silkscreen";src:url(data:font/woff2;base64,' + silk + ') format("woff2");font-weight:400;font-display:block}</style>')
d = app
i = d.index('<link rel="preconnect"'); j = d.index('display=swap">') + len('display=swap">')
d = d[:i] + fonts + d[j:]
d = d.replace('<script>\n(() => {', '<script>window.BBB_DESKTOP = true; fetch("/ping").catch(() => {}); setInterval(() => fetch("/ping").catch(() => {}), 5000); addEventListener("pagehide", () => navigator.sendBeacon("/bye"));</script>\n<script>\n(() => {', 1)
open(f'{D}/../desktop/index.html', 'w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>:root{color-scheme:light dark}body{margin:0}</style></head><body>' + d + '</body></html>')
print('desktop html', len(d))
