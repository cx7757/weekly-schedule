import re

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

# Extract all readable text sequences
# Find sequences of printable chars
text_blocks = []
current = b''
for byte in raw:
    if 32 <= byte <= 126 or byte in (9, 10, 13):
        current += bytes([byte])
    else:
        if len(current) > 3:
            text_blocks.append(current.decode('ascii'))
        current = b''

# Print all text blocks that look like keys or schedule data
for block in text_blocks:
    if any(kw in block.lower() for kw in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'task', 'week', 'schedule', 'check', 'streak', 'template', 'eisenhower', 'matrix', '2026-0']):
        print(f"[{len(block)} chars] {block[:200]}")
        if len(block) > 200:
            print(f"  ... {block[200:400]}")
        print()
