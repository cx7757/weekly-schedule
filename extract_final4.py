"""
Edge localStorage LevelDB uses a custom string encoding.
The format is: for each character, if ASCII < 128, store as 1 byte.
For chars >= 128 (like Chinese), they seem to be stored with a length prefix.
Let's try a different approach: just decode the raw bytes as the 
Chrome/Edge localStorage format.
"""

import json, re, struct

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

# Find schedule_week7
target = b'schedule_week7'
pos = raw.find(target)
print(f"Key at position: {pos}")

# After the key, there's a type byte (0x01), then value length, then value
# The format seems to be: key_data + type(1) + length(varint) + value_data
# Looking at the hex: after "schedule_week7" we have: 01 da 09 2c 38 01 7b 22...
# 01 = type (string)
# da 09 = ? (might be part of varint for length)
# 2c 38 = more header?
# 7b 22 = {"  which is the start of JSON

# Let's find the JSON start
json_pos = raw.find(b'{"', pos)
print(f"JSON starts at: {json_pos}")

# Now we need to find the end. The value is encoded where:
# - ASCII chars are stored as-is
# - Non-ASCII chars are encoded as: 0x0d + high_byte + low_byte (UTF-16LE pairs) + 0x00
# - Or: 0x0d + length + UTF-16LE bytes

# Let's manually decode from the JSON start
data = raw[json_pos:]

def decode_chrome_storage(data):
    """Decode Chrome's localStorage value encoding"""
    result = []
    i = 0
    while i < len(data):
        b = data[i]
        if b == 0x0d:
            # Extended encoding for non-ASCII
            i += 1
            if i >= len(data):
                break
            next_b = data[i]
            if next_b == 0x00:
                # This might be a null terminator or escape
                i += 1
                continue
            # Read UTF-16LE string until we hit a delimiter
            # The format seems to be: 0x0d + varint_length + utf16le_bytes
            length = next_b
            i += 1
            chars = []
            for j in range(length):
                if i + 1 < len(data):
                    char_code = data[i] | (data[i+1] << 8)
                    chars.append(chr(char_code))
                    i += 2
            result.append(''.join(chars))
        elif 0x20 <= b <= 0x7e:
            result.append(chr(b))
            i += 1
        elif b in (0x09, 0x0a, 0x0d):
            # Wait, 0x0d is already handled above as extended encoding
            # This means our logic is wrong for 0x0d as newline
            result.append('\n')
            i += 1
        else:
            # Unknown byte, skip
            i += 1
    return ''.join(result)

# Try decoding
text = decode_chrome_storage(data)
print(f"\nDecoded text (first 500 chars):\n{text[:500]}")

# Find the JSON object
json_start = text.find('{')
json_end = -1
if json_start >= 0:
    depth = 0
    for i in range(json_start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                json_end = i
                break

if json_end > json_start:
    json_str = text[json_start:json_end+1]
    print(f"\nJSON found: {len(json_str)} chars")
    try:
        obj = json.loads(json_str)
        print(f"Parsed: {len(obj)} keys")
        print(f"Keys: {list(obj.keys())[:20]}")
        
        outpath = r'c:\Users\chenx\WorkBuddy\Claw\extracted_schedule_data.json'
        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to {outpath}")
        
        for k, v in list(obj.items())[:2]:
            print(f"\n--- {k} ---")
            print(json.dumps(v, ensure_ascii=False, indent=2)[:400])
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Problem area: ...{json_str[max(0,e.pos-50):e.pos+50]}...")
else:
    print("No complete JSON object found")
