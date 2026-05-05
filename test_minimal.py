# -*- coding: utf-8 -*-
"""最简单的合并测试 - 只加一个空函数"""
with open('c:/Users/chenx/WorkBuddy/Claw/v7_good_backup.html', 'r', encoding='utf-8') as f:
    h = f.read()

marker = '// ── Init ──'
insert = '\n// Test function\nfunction testFunction(){return true;}\n\n'
h = h.replace(marker, insert + marker)

with open('c:/Users/chenx/WorkBuddy/Claw/_v7_plus_test.html', 'w', encoding='utf-8') as f:
    f.write(h)

print(f'Created: {len(h)} bytes')
has_test = 'function testFunction' in h
has_init = marker in h
print(f'Insert OK: {has_test}')
print(f'Init still present: {has_init}')
