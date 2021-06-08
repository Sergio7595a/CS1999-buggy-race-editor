import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your SQLite database for you, just
# to get you started... there are better ways to express the
# data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#-------------------------------------------------------------

connection = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:
def create_buggy(buggy_id):
  connection.execute(f"""
  
    CREATE TABLE IF NOT EXISTS buggies{buggy_id} (
      id                    INTEGER PRIMARY KEY,
      qty_wheels            INTEGER DEFAULT 4,
      power_type            VARCHAR(20) DEFAULT petrol,
      power_units           INTEGER DEFAULT 1,
      aux_power_type        VARCHAR(20),
      aux_power_units       INTEGER DEFAULT 0,
      hamster_booster       INTEGER DEFAULT 0,
      flag_color            VARCHAR(20) DEFAULT white,
      flag_pattern          VARCHAR(20) DEFAULT plain,
      flag_color_secondary  VARCHAR(20) DEFAULT black,
      tyres                 VARCHAR(20) DEFAULT knobbly,
      qty_tyres             INTEGER DEFAULT 4,
      armour                VARCHAR(20),
      attack                VARCHAR(20),
      qty_attacks           INTEGER DEFAULT 0,
      fireproof             BOOLEAN,
      insulated             BOOLEAN,
      antibiotic            BOOLEAN,
      banging               BOOLEAN,
      algo                  VARCHAR(20) DEFAULT steady,
      total_cost            INTEGER DEFAULT 0
    )
  
  """)

  print(f"- Table \"buggies{buggy_id}\" exists OK")

  cursor = connection.cursor()

  cursor.execute(f"SELECT * FROM buggies{buggy_id} LIMIT 1")
  rows = cursor.fetchall()
  if len(rows) == 0:
    cursor.execute(f"INSERT INTO buggies{buggy_id} (qty_wheels) VALUES (4)")
    connection.commit()
    print(f"- Added one 4-wheeled buggy to buggies{buggy_id}")
  else:
    print(f"- Found a buggy in the database, nice")

  print("- OK, your database is ready")
create_buggy(1)
connection.close()
