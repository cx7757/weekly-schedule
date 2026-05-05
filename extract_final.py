import json, os, re, struct

ldb_dir = r'C:\Users\chenx\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb'

# Read all .ldb files
all_data = {}
for fname in os.listdir(ldb_dir):
    if not fname.endswith('.ldb'):
        continue
    fpath = os.path.join(ldb_dir, fname)
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Find all JSON objects that look like schedule data
    # Try UTF-16LE first
    try:
        text16 = raw.decode('utf-16-le', errors='ignore')
    except:
        text16 = ''
    
    # Also try UTF-8
    try:
        text8 = raw.decode('utf-8', errors='ignore')
    except:
        text8 = ''
    
    for text, enc in [(text16, 'utf16'), (text8, 'utf8')]:
        if 'mon' in text.lower() and ('task' in text.lower() or 'time' in text.lower()):
            # Try to find JSON objects
            depth = 0
            start = -1
            for i, c in enumerate(text):
                if c == '{':
                    if depth == 0:
                        start = i
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0 and start >= 0:
                        json_str = text[start:i+1]
                        # Clean non-printable chars
                        json_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
                        # Check if it looks like schedule data
                        if 'mon' in json_clean or 'tue' in json_clean or 'wed' in json_clean:
                            try:
                                obj = json.loads(json_clean)
                                if isinstance(obj, dict) and len(obj) > 3:
                                    # Check if it has day-based keys like "2026-04-08-mon"
                                    day_keys = [k for k in obj.keys() if re.match(r'20\d\d-\d\d-\d\d', k)]
                                    if day_keys:
                                        print(f"Found schedule data in {fname} ({enc}): {len(day_keys)} day entries")
                                        print(f"  Day keys: {day_keys[:5]}")
                                        print(f"  Total keys: {len(obj)}")
                                        all_data = obj
                            except json.JSONDecodeError:
                                pass
                        start = -1

if all_data:
    outpath = r'c:\Users\chenx\WorkBuddy\Claw\extracted_schedule_data.json'
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {outpath}")
    
    # Show a sample entry
    for k, v in list(all_data.items())[:3]:
        print(f"\n--- {k} ---")
        if isinstance(v, dict):
            print(json.dumps(v, ensure_ascii=False, indent=2)[:500])
        else:
            print(str(v)[:500])
else:
    print("No schedule data found. Listing all .ldb files:")
    for fname in os.listdir(ldb_dir):
        if fname.endswith('.ldb'):
            fpath = os.path.join(ldb_dir, fname)
            size = os.path.getsize(fpath)
            with open(fpath, 'rb') as f:
                header = f.read(100)
            print(f"  {fname}: {size} bytes, header: {header[:50]}")
