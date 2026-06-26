def book_appointment(patient, doctor):
    import sqlite3
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    #  Check duplicate booking
    cursor.execute(
        "SELECT * FROM appointments WHERE patient=? AND doctor=?",
        (patient, doctor)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "❌ You already have an appointment with this doctor"

    # Available slots
    slots = ["10:00AM", "10:15AM", "10:30AM", "10:45AM",
             "11:00AM", "11:30AM", "12:00PM"]

    # Get already booked slots for that doctor
    cursor.execute("SELECT time FROM appointments WHERE doctor=?", (doctor,))
    booked = [row[0] for row in cursor.fetchall()]

    # Get available slots
    available_slots = [s for s in slots if s not in booked]

    if not available_slots:
        conn.close()
        return "No slots available"

    # Show slots
    print("\nAvailable slots:")
    for i, s in enumerate(available_slots):
        print(f"{i+1}. {s}")

    # User input with validation
    try:
        choice = int(input("Select slot number: "))
        if choice < 1 or choice > len(available_slots):
            conn.close()
            return "Invalid choice"
    except:
        conn.close()
        return "Invalid input"

    slot = available_slots[choice - 1]

    # Insert appointment
    cursor.execute(
        "INSERT INTO appointments (patient, doctor, time) VALUES (?, ?, ?)",
        (patient, doctor, slot)
    )
    conn.commit()
    conn.close()

    # Generate and save bill
    bill = generate_bill(patient, doctor, slot)

    return f"\nAppointment booked at {slot}\n{bill}"


def get_appointments():
    import sqlite3
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT patient, doctor, time FROM appointments")
    data = cursor.fetchall()

    conn.close()
    return data


def generate_bill(patient, doctor, slot):
    import sqlite3
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # Get fee from doctors table
    cursor.execute("SELECT fee FROM doctors WHERE name=?", (doctor,))
    result = cursor.fetchone()

    if result:
        fee = result[0]
    else:
        fee = 0

    # Save bill in database
    cursor.execute(
        "INSERT INTO bills (patient, doctor, time, amount) VALUES (?, ?, ?, ?)",
        (patient, doctor, slot, fee)
    )
    conn.commit()
    conn.close()

    # Bill format
    bill = f"""
----- Clinic Bill -----
Patient Name : {patient}
Doctor Name  : {doctor}
Time         : {slot}
Consultation Fee : ₹{fee}
-----------------------
"""

    return bill