import sqlite3

conn = sqlite3.connect("physics.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    chapter TEXT UNIQUE,
    weightage INTEGER,
    pyq INTEGER,
    difficulty INTEGER,
    revision_time INTEGER
)
""")

data = [
    ("Physics","Current Electricity",5,24,2,5),
    ("Physics","Electrostatics",5,22,3,6),
    ("Physics","Ray Optics",5,21,2,5),
    ("Physics","Magnetic Effects",4,18,2,4),
    ("Physics","Thermodynamics",4,16,3,5),
    ("Physics","Dual Nature",3,14,1,3),
    ("Physics","Atomic Physics",3,12,1,3),

    ("Physics","Rotational Motion",4,18,3,6),
    ("Physics","Gravitation",4,17,2,4),
    ("Physics","Fluids",4,16,2,4),
    ("Physics","Semiconductors",3,14,1,3),
    ("Physics","Work Power Energy",3,14,2,4),
    ("Physics","Units and Dimensions",3,13,1,2),
    ("Physics","Wave Optics",3,13,2,4),
    ("Physics","Laws of Motion",3,12,2,4),
    ("Physics","Motion in 1D",3,11,1,3)
]

cur.executemany(
    "INSERT OR IGNORE INTO chapters VALUES (NULL,?,?,?,?,?,?)",
    data
)

conn.commit()
conn.close()

print("✅ Database created & Physics data inserted")
