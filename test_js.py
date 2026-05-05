# -*- coding: utf-8 -*-
"""测试合并后的index.html的JS语法是否正确"""
import re

with open('c:/Users/chenx/WorkBuddy/Claw/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# 提取JS
start = h.find('<script>') + 8
end = h.find('</script>')
js = h[start:end]

print(f'JS length: {len(js)} chars')

# 写一个测试HTML，看能不能在浏览器里正常执行
test_html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body>
<div id="testResult">Testing...</div>
<script>
try {
''' + js + '''
    document.getElementById('testResult').textContent = 'JS OK - All functions loaded';
} catch(e) {
    document.getElementById('testResult').textContent = 'JS ERROR: ' + e.message;
}
</script>
</body></html>'''

with open('c:/Users/chenx/WorkBuddy/Claw/_test.html', 'w', encoding='utf-8') as f:
    f.write(test_html)

print('Test file created: _test.html')

# Also check: are there any raw </script> inside the NOTES_DB strings?
# This would prematurely close the script tag!
raw_close = js.find('</script>')
while raw_close >= 0:
    print(f'WARNING: Found raw </script> at JS offset {raw_close}')
    print(f'  Context: ...{repr(js[max(0,raw_close-30):raw_close+20])}...')
    raw_close = js.find('</script>', raw_close + 1)

# Check for <script (case insensitive)
import re
script_tags = list(re.finditer(r'<script', js, re.IGNORECASE))
if script_tags:
    for m in script_tags:
        ctx = js[max(0,m.start()-20):m.end()+20]
        print(f'WARNING: Found <script at JS offset {m.start()}: ...{repr(ctx)}...')
else:
    print('No embedded <script> tags found in JS - good!')

# Count total </script> in the whole file
all_script_closes = list(re.finditer(r'</script>', h))
print(f'Total </script> tags in file: {len(all_script_closes)}')
for m in all_script_closes:
    print(f'  at pos {m.start()}: ...{repr(h[max(0,m.start()-10):m.start()+20])}...')
