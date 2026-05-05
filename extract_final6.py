import json, sys

sys.stdout.reconfigure(encoding='utf-8')

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

# Find schedule_week7
target = b'schedule_week7'
pos = raw.find(target)
print(f"Key at: {pos}")

# After "schedule_week7" (14 bytes), look at the structure
# hex dump from pos to pos+300
chunk = raw[pos:pos+500]
print(f"\nHex dump:")
for i in range(0, len(chunk), 16):
    hex_part = ' '.join(f'{b:02x}' for b in chunk[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk[i:i+16])
    offset = pos + i
    print(f"  {offset:04x}: {hex_part:<48s} {ascii_part}")

# The LevelDB key-value format in Chrome localStorage is:
# META:origin_id (varint) + type (1 byte) + key_string + type (1 byte) + value_string
# The string encoding uses: 0x0d as prefix for strings with special chars
# followed by varint length, then raw bytes

# Let's look at what's between schedule_week7 and the next entry
# After the key "schedule_week7", we should see: 0x01 (string type) + encoded_value

# Find where value data starts after the key
# The key bytes are: 73 63 68 65 64 75 6c 65 5f 77 65 65 6b 37
key_end = pos + len(target)
print(f"\nAfter key ({key_end}):")
after_key = raw[key_end:key_end+30]
for i, b in enumerate(after_key):
    print(f"  +{i}: 0x{b:02x} ({chr(b) if 32<=b<=126 else '.'})")

# The value seems to start with 0x01 which is a type indicator
# Then 0xda = 218 which could be a varint for length
# Let's check: 0xda in varint is 0x5a << 7 | 0x1a... no
# Actually Chrome uses a different varint scheme

# Let's try another approach: find all keys stored in this file
# Keys in Chrome localStorage are prefixed with META:origin
print("\n\n=== All keys in this ldb file ===")
meta = b'META:'
search_start = 0
while True:
    mp = raw.find(meta, search_start)
    if mp == -1:
        break
    
    # After META:, there's the origin (e.g., "file://" or "https://...")
    # then a null byte or separator, then key data
    # Let's find readable text after META:
    text_start = mp + len(meta)
    # Read until we hit a non-readable byte
    key_chars = []
    i = text_start
    while i < len(raw) and (32 <= raw[i] <= 126 or raw[i] in (9, 10, 13, 0)):
        if raw[i] == 0:
            break
        key_chars.append(chr(raw[i]))
        i += 1
    key_text = ''.join(key_chars)
    if len(key_text) > 2 and not key_text.startswith('{'):
        print(f"  [{mp}] {key_text[:100]}")
    
    search_start = mp + 1
