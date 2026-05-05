import re

content = open('index.html', 'r', encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
all_js = '\n'.join(scripts)

print(f'JS 总长度: {len(all_js)} 字符')
print(f'JS 总行数: {all_js.count(chr(10))} 行')

# 检查括号匹配
def check_brackets(js, open_char, close_char, name):
    stack = []
    in_string = False
    string_char = None
    escaped = False
    line = 1
    
    for i, c in enumerate(js):
        if c == '\n':
            line += 1
        if escaped:
            escaped = False
            continue
        if c == '\\':
            escaped = True
            continue
        if in_string:
            if c == string_char:
                in_string = False
            continue
        if c in ('"', "'", '`'):
            in_string = True
            string_char = c
            continue
        if c == '/' and i+1 < len(js) and js[i+1] == '/':
            # 单行注释
            while i < len(js) and js[i] != '\n':
                i += 1
            continue
        if c == open_char:
            stack.append((i, line))
        elif c == close_char:
            if not stack:
                print(f'  ❌ {name} 括号多余: 位置 {i}, 行 {line}')
                return False
            stack.pop()
    
    if stack:
        print(f'  [X] {name} 括号未闭合: {len(stack)} 个未关闭')
        for pos, ln in stack[:3]:
            print(f'    行 {ln}')
        return False
    else:
        print(f'  [OK] {name} 括号匹配正确')
        return True

print('\n括号匹配检查:')
check_brackets(all_js, '{', '}', '大括号')
check_brackets(all_js, '(', ')', '小括号')
check_brackets(all_js, '[', ']', '中括号')

# 检查关键函数是否存在
print('\n关键函数检查:')
functions = ['openFinance', 'finShowFinanceUI', 'finRender', 'finLoadRecords', 
             'finSaveRecords', 'finShowPwdModal', 'finCheckPwd', 'closeFinance',
             'finSwitchTab', 'finRenderOverview', 'finRenderBook', 'finRenderStats',
             'finRenderSettings']

found = []
missing = []
for fn in functions:
    if re.search(r'function\s+' + re.escape(fn) + r'\s*\(', all_js):
        found.append(fn)
    else:
        missing.append(fn)

print(f'  [OK] 找到 {len(found)} 个函数')
if missing:
    print(f'  [X] 缺失 {len(missing)} 个函数: {missing}')

# 检查是否有 finRenderUI 调用（应该改成 finRender）
print('\nfinRenderUI 检查:')
if 'finRenderUI()' in all_js:
    print('  [X] 仍有 finRenderUI() 调用！')
    # 找出位置
    lines = all_js.split('\n')
    for i, line in enumerate(lines):
        if 'finRenderUI()' in line:
            print(f'    行 {i+1}: {line.strip()[:80]}')
else:
    print('  [OK] 没有 finRenderUI() 调用')

# 检查 openFinance 内容
print('\nopenFinance 函数内容:')
m = re.search(r'function openFinance\(\)\s*\{(.*?)\}', all_js, re.DOTALL)
if m:
    print(m.group(0)[:400])
else:
    print('  [X] openFinance 函数格式异常')
