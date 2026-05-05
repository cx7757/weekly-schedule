import sys
path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()
checks = [
    'function render', 'function toggleDone', 'function load', 'function save',
    'function openNotes', 'function goHome', 'function openNotesCat',
    'function onNotesSearch', 'const NOTES_DB=', 'function openEditModal',
    'function submitAdd', 'function startTimer', 'function initPWA',
    'function initTheme', 'function calcInitWeek', '</script>', '</body>', '</html>'
]
all_ok = True
for c in checks:
    ok = c in h
    if not ok:
        all_ok = False
    print(('OK' if ok else 'MISSING') + '  ' + c)
count = h.count('{"t":')
print('\nTotal knowledge items: ' + str(count))
print('File size: ' + str(len(h)) + ' bytes')
print('\nAll checks passed!' if all_ok else '\nSome checks FAILED!')
