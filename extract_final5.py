import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

target = b'schedule_week7'
pos = raw.find(target)
json_pos = raw.find(b'{"', pos)
data = raw[json_pos:]

def decode_chrome_storage(data):
    result = []
    i = 0
    while i < len(data):
        b = data[i]
        if b == 0x0d:
            i += 1
            if i >= len(data):
                break
            next_b = data[i]
            if next_b == 0x00:
                i += 1
                continue
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
        else:
            i += 1
    return ''.join(result)

text = decode_chrome_storage(data)
print(f"Decoded {len(text)} chars")

# Find JSON
json_start = text.find('{')
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
    
    json_str = text[json_start:json_end+1]
    print(f"JSON length: {len(json_str)}")
    print(f"First 200: {json_str[:200]}")
    print(f"Last 100: {json_str[-100:]}")
    
    try:
        obj = json.loads(json_str)
        print(f"\nParsed: {len(obj)} keys")
        print(f"Keys: {list(obj.keys())[:20]}")
        
        outpath = r'c:\Users\chenx\WorkBuddy\Claw\extracted_schedule_data.json'
        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"\nSaved!")
        
        for k, v in list(obj.items())[:2]:
            print(f"\n--- {k} ---")
            print(json.dumps(v, ensure_ascii=False, indent=2)[:400])
    except json.JSONDecodeError as e:
        print(f"\nJSON error at pos {e.pos}: {e}")
        print(f"Context: ...{json_str[max(0,e.pos-80):e.pos+80]}...")
else:
    print("No JSON start found")
