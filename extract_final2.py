import re, json

ldb_path = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb\001482.ldb'

with open(ldb_path, 'rb') as f:
    raw = f.read()

# Extract all printable text blocks
text_blocks = []
current = b''
for byte in raw:
    if 32 <= byte <= 126 or byte in (9, 10, 13):
        current += bytes([byte])
    else:
        if len(current) > 3:
            text_blocks.append(current.decode('ascii'))
        current = b''

# Find the schedule data block - it starts with { and contains day keys
schedule_data = None
full_text = '|||'.join(text_blocks)

# Find JSON that starts with { and contains schedule-like content
for block in text_blocks:
    if block.startswith('{') and ('mon' in block.lower() or 'thu' in block.lower() or 'tue' in block.lower()):
        # Try to find complete JSON
        depth = 0
        end = -1
        for i, c in enumerate(block):
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end > 0:
            json_str = block[:end+1]
            try:
                obj = json.loads(json_str)
                print(f"Found JSON object with {len(obj)} keys")
                print(f"Keys: {list(obj.keys())[:20]}")
                schedule_data = obj
            except json.JSONDecodeError as e:
                print(f"JSON error: {e}")
                print(f"Block length: {len(block)}, ends at: {end}")
                print(f"First 300: {json_str[:300]}")
                print(f"Last 100: {json_str[-100:]}")

if schedule_data:
    outpath = r'c:\Users\chenx\WorkBuddy\Claw\extracted_schedule_data.json'
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to extracted_schedule_data.json")
else:
    # Print all blocks with { for debugging
    print("\nAll blocks starting with {:")
    for i, block in enumerate(text_blocks):
        if '{' in block:
            print(f"\n--- Block {i} (len={len(block)}) ---")
            print(block[:500])
