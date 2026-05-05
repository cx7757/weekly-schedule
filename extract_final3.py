import json, re

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

# Find "schedule_week7" as bytes
target = b'schedule_week7'
pos = raw.find(target)
print(f"'schedule_week7' found at byte position: {pos}")

# The actual data is stored as: key_length(4 bytes varint) + key + value_length(4 bytes varint) + value
# After the key "schedule_week7", skip a few bytes (type/tag) then the value starts

# Let's look at what comes after the key
if pos >= 0:
    # Show bytes around this area
    start = pos - 20
    end = pos + 200
    chunk = raw[start:end]
    print(f"\nHex dump around 'schedule_week7':")
    for i in range(0, len(chunk), 16):
        hex_str = ' '.join(f'{b:02x}' for b in chunk[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk[i:i+16])
        print(f"  {start+i:04x}: {hex_str:<48s} {ascii_str}")

# Also try to find the JSON value by looking for patterns after the key
# The value should be a UTF-16LE encoded JSON string
# Find the first { after the key area
json_start_options = []
for i in range(pos, min(pos + 100, len(raw))):
    if raw[i:i+1] == b'{':
        json_start_options.append(i)
        
print(f"\nFound '{{' at positions after key: {[p - pos for p in json_start_options]}")

# Try reading from each potential JSON start position
for js_pos in json_start_options[:5]:
    # Try UTF-16LE
    chunk = raw[js_pos:js_pos+20000]
    try:
        text = chunk.decode('utf-16-le', errors='strict')
        # Find end of JSON
        depth = 0
        end_idx = -1
        for i, c in enumerate(text):
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
        if end_idx > 0:
            json_str = text[:end_idx+1]
            obj = json.loads(json_str)
            print(f"\n✅ UTF-16LE parse success at +{js_pos-pos}: {len(obj)} keys")
            print(f"Keys: {list(obj.keys())[:10]}")
            
            outpath = r'c:\Users\chenx\WorkBuddy\Claw\extracted_schedule_data.json'
            with open(outpath, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            print(f"Saved to {outpath}")
            
            # Show sample
            for k, v in list(obj.items())[:2]:
                print(f"\n--- {k} ---")
                print(json.dumps(v, ensure_ascii=False, indent=2)[:300])
            break
    except Exception as e:
        print(f"UTF-16LE at +{js_pos-pos}: {e}")

# Also try raw UTF-8
for js_pos in json_start_options[:5]:
    chunk = raw[js_pos:js_pos+20000]
    # Find matching } by byte count
    depth = 0
    end_idx = -1
    for i, b in enumerate(chunk):
        if b == ord('{'):
            depth += 1
        elif b == ord('}'):
            depth -= 1
            if depth == 0:
                end_idx = i
                break
    if end_idx > 0:
        json_bytes = chunk[:end_idx+1]
        try:
            obj = json.loads(json_bytes)
            print(f"\n✅ Raw UTF-8 parse success at +{js_pos-pos}: {len(obj)} keys")
            print(f"Keys: {list(obj.keys())[:10]}")
            break
        except:
            pass
