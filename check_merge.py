# -*- coding: utf-8 -*-
"""诊断：比较V7干净版 vs 合并版，找出功能丢失原因"""
import sys

print("=== Step 1: 检查V7干净版 ===")
with open('v7_clean.html', 'r', encoding='utf-8') as f:
    v7 = f.read()
print(f"V7 size: {len(v7)} bytes, {v7.count(chr(10))} lines")

# 检查所有关键V7函数
v7_funcs = [
    'function render()',
    'function switchDay(',
    'function submitAdd(',
    'function toggleTask(',
    'function deleteTask(',
    'function toggleTheme(',
    'function openEdit(',
    'function saveEdit(',
    'function openSummary(',
    'function openMonthly(',
    'function openSettings(',
    'function saveData(',
    'function loadData(',
    'function getTasksOf(',
    'function getDataKey(',
    'function changeWeek(',
    'function exportData(',
    'function importData(',
    'function startTimer(',
    'function stopTimer(',
    'function updateTimerDisplay(',
]
print("\nV7 functions:")
for func in v7_funcs:
    found = func in v7
    print(f"  {func}: {'OK' if found else 'MISSING!'}")

# 检查V7 HTML结构
v7_html = [
    'id="mainArea"',
    'id="dayTabs"',
    'id="editModal"',
    'id="weekLabel"',
    'id="weekRange"',
    'id="weekPct"',
    'id="weekBar"',
    'id="todayBadge"',
    'id="progressWrap"',
    'class="day-tab"',
    'id="scheduleHeader"',
]
print("\nV7 HTML elements:")
for el in v7_html:
    found = el in v7
    print(f"  {el}: {'OK' if found else 'MISSING!'}")

# 检查初始化代码
v7_init = ['render()', 'loadData()', 'switchDay(']
print("\nV7 init calls:")
for ini in v7_init:
    # 找init块
    idx = v7.find('// ── Init ──')
    if idx >= 0:
        init_block = v7[idx:idx+500]
        found = ini in init_block
        print(f"  {ini} in init block: {'OK' if found else 'MISSING!'}")
    else:
        print(f"  Init block: NOT FOUND!")

# === 检查合并后的版本 ===
print("\n\n=== Step 2: 检查合并后的index.html ===")
with open('index.html', 'r', encoding='utf-8') as f:
    merged = f.read()
print(f"Merged size: {len(merged)} bytes, {merged.count(chr(10))} lines")

print("\nMerged V7 functions:")
for func in v7_funcs:
    found = func in merged
    print(f"  {func}: {'OK' if found else 'MISSING!'}")

print("\nMerged HTML elements:")
for el in v7_html:
    found = el in merged
    print(f"  {el}: {'OK' if found else 'MISSING!'}")

print("\nMerged init calls:")
idx = merged.find('// ── Init ──')
if idx >= 0:
    init_block = merged[idx:idx+500]
    print(f"  Init block found at char {idx}")
    for ini in v7_init:
        found = ini in init_block
        print(f"    {ini}: {'OK' if found else 'MISSING!'}")
else:
    # Try other patterns
    for pattern in ['// ── Init', '// Init', 'init()', 'render();']:
        pidx = merged.rfind(pattern)
        if pidx >= 0:
            print(f"  Found '{pattern}' at char {pidx}")
    print("  WARNING: '// ── Init ──' block NOT FOUND!")

# === 检查script标签 ===
print("\n=== Step 3: 检查script标签 ===")
import re
v7_scripts = re.findall(r'<script[^>]*>|</script>', v7)
merged_scripts = re.findall(r'<script[^>]*>|</script>', merged)
print(f"V7 script tags: {v7_scripts}")
print(f"Merged script tags: {merged_scripts}")

# 检查是否有未闭合的script标签
v7_script_opens = v7.count('<script')
v7_script_closes = v7.count('</script>')
merged_script_opens = merged.count('<script')
merged_script_closes = merged.count('</script>')
print(f"\nV7: <script> x{v7_script_opens}, </script> x{v7_script_closes}")
print(f"Merged: <script> x{merged_script_opens}, </script> x{merged_script_closes}")
if merged_script_opens != merged_script_closes:
    print("  ERROR: Unclosed <script> tag!")

# === 检查是否有JS语法错误 ===
print("\n=== Step 4: 检查NOTES_DB中是否有特殊字符 ===")
# 找NOTES_DB的范围
notes_start = merged.find('const NOTES_DB=')
notes_end = merged.find('};', notes_start + 100) + 2 if notes_start >= 0 else -1
if notes_start >= 0 and notes_end > notes_start:
    notes_block = merged[notes_start:notes_end]
    # 检查是否有未转义的引号问题
    # 统计花括号是否匹配
    braces = 0
    brackets = 0
    for i, c in enumerate(notes_block):
        if c == '{': braces += 1
        elif c == '}': braces -= 1
        elif c == '[': brackets += 1
        elif c == ']': brackets -= 1
    print(f"NOTES_DB block: char {notes_start}-{notes_end}, braces balance: {braces}, brackets balance: {brackets}")
    if braces != 0 or brackets != 0:
        print("  WARNING: Unmatched braces or brackets!")

# === 检查考公JS函数 ===
print("\n=== Step 5: 检查考公JS函数 ===")
notes_funcs = [
    'function openNotes(',
    'function closeNotes(',
    'function goHome(',
    'function openNotesCat(',
    'function onNotesSearch(',
]
for func in notes_funcs:
    found = func in merged
    print(f"  {func}: {'OK' if found else 'MISSING!'}")

# === 关键检查：考公代码中是否有</script>标签导致提前结束 ===
print("\n=== Step 6: 检查考公代码中是否有</script> ===")
if notes_start >= 0:
    after_notes = merged[notes_start:]
    # 检查考公数据中是否意外包含</script>
    dangerous = after_notes.find('</script>')
    if dangerous >= 0 and dangerous < (notes_end - notes_start if notes_end > 0 else 10000):
        print(f"  ERROR! Found </script> inside JS at offset {notes_start + dangerous}!")
        context = merged[notes_start + dangerous - 50:notes_start + dangerous + 20]
        print(f"  Context: ...{context}...")
    else:
        print("  OK - no </script> inside JS block")

print("\n=== DONE ===")
