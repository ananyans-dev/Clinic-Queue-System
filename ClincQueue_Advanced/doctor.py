from database import cursor, conn

def add_doctor(name, specialization, fee):
    cursor.execute(
        "INSERT INTO doctors (name, specialization, fee) VALUES (?, ?, ?)",
        (name, specialization, fee)
    )
    conn.commit()

def get_doctors():
    cursor.execute("SELECT * FROM doctors")
    return cursor.fetchall()