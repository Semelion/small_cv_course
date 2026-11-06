"""Build the local HTML textbook; requires Python package markdown."""
from pathlib import Path
import re
import markdown

root = Path(__file__).resolve().parents[1]
files = [root / 'README.md', *sorted((root / 'chapters').glob('*.md'))]
parts = []
for path in files:
    source = path.read_text(encoding='utf-8')
    if path.parent.name == 'chapters':
        source = source.replace('../assets/', 'assets/').replace('../examples/', 'examples/').replace('../arduino/', 'arduino/')
    for chapter in files:
        source = source.replace(f'chapters/{chapter.name}', f'#{chapter.stem}')
    rendered = markdown.markdown(source, extensions=['fenced_code', 'tables', 'toc'])
    parts.append(f'<section id="{path.stem}">{rendered}</section>')
css = '''body{margin:0;background:#eef2f5;color:#17212b;font:18px/1.65 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:40px 56px;background:white}h1,h2,h3{line-height:1.25;color:#103c55}h1{font-size:2.2rem;margin-top:1.4em}h2{margin-top:1.8em}a{color:#006a92}img{max-width:100%;height:auto;border:1px solid #d4dee4;border-radius:8px}pre{background:#102936;color:#eff8fc;padding:20px;overflow:auto;border-radius:8px;font-size:14px;line-height:1.55}code{font-family:ui-monospace,monospace}p code,li code,td code{background:#edf3f6;padding:2px 5px;border-radius:4px}table{border-collapse:collapse;width:100%;font-size:16px}td,th{border:1px solid #c9d6dd;padding:10px;text-align:left}th{background:#e6f1f5}section+section{border-top:3px solid #cee0e8;margin-top:64px;padding-top:24px}nav{position:sticky;top:0;background:#103c55;color:white;padding:12px 20px;font-size:14px;text-align:center}nav a{color:white;margin:0 9px}@media(max-width:650px){main{padding:18px}body{font-size:16px}nav{position:static}h1{font-size:1.8rem}}@media print{nav{display:none}body{background:white;font-size:11pt}main{padding:0;max-width:none}pre{white-space:pre-wrap;background:#eee;color:#111}section{break-before:page}img{max-height:17cm;object-fit:contain}h1,h2,h3{break-after:avoid}}'''
nav = '<nav><a href="#README">Начало</a><a href="#00_start">Запуск</a><a href="#01_images">Изображения</a><a href="#02_camera_aruco">Камера / ArUco</a><a href="#03_serial">Serial</a><a href="#04_teacher">Преподавателю</a></nav>'
(root / 'index.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Компьютерное зрение — мини-курс</title><style>'+css+'</style></head><body>'+nav+'<main>'+''.join(parts)+'</main></body></html>', encoding='utf-8')
print(root / 'index.html')
