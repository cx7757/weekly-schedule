import re
with open('index.html','r',encoding='utf-8') as f:
    h = f.read()
cats = re.findall(r'"cat":\s*"([^"]+)"', h)
print('Categories:', sorted(set(cats)))
print('Total items:', h.count('"title":'))
print('File size:', len(h))
