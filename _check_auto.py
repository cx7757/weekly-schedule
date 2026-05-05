import sqlite3
db = r'c:\Users\chenx\AppData\Roaming\WorkBuddy\automations\automations.db'
conn = sqlite3.connect(db)
conn.execute("PRAGMA wal_checkpoint(FULL)")
cur = conn.cursor()
cur.execute("SELECT id, name, status, rrule, prompt, cwds FROM automations")
rows = cur.fetchall()
for r in rows:
    print("ID:", r[0])
    print("NAME:", r[1])
    print("STATUS:", r[2])
    print("RRULE:", r[3])
    print("PROMPT:", r[4][:80] if r[4] else "")
    print("CWDS:", r[5])
    print("---")
conn.close()
