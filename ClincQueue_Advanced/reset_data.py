import sqlite3

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM appointments")
cursor.execute("DELETE FROM bills")

conn.commit()
conn.close()

print("Appointments and Bills cleared ✅")