import re, subprocess, sys, tempfile, os

html = open('index.html', 'r', encoding='utf-8').read()

# 提取所有 <script> 内容
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f'找到 {len(scripts)} 个 script 标签')

all_js = '\n'.join(scripts)

# 写出到临时文件
tmp = '___check_temp.js'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(all_js)

# 用 node 检查语法
try:
    r = subprocess.run(['node', '-c', tmp], capture_output=True, text=True)
    print('STDOUT:', r.stdout)
    print('STDERR:', r.stderr)
    print('返回码:', r.returncode)
except Exception as e:
    print('执行失败:', e)

os.remove(tmp)

# 找关键函数
fns = re.findall(r'function\s+(\w+)', all_js)
print('\n关键函数检查:')
keys = ['openFinance','finRenderUI','finShowFinanceUI','finLoadRecords','finSaveRecords','finRender','finShowPwdModal','finCheckPwd']
for k in keys:
    print(f'  {k}: {"✅" if k in fns else "❌"}')

# 检查 openFinance 内容
m = re.search(r'function openFinance\(\)\{.*?\}', all_js, re.DOTALL)
if m:
    print('\nopenFinance 内容（前500字）:')
    print(m.group(0)[:500])
else:
    print('\n❌ openFinance 函数未找到或格式异常')
