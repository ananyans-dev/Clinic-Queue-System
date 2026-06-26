from appointment import book_appointment
from appointment import get_appointments
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import create_tables
from doctor import add_doctor,get_doctors

def start_app():
    create_tables()

    root = tk.Tk()
    root.title("Clinic Queue Management System")
    root.geometry("500x400")

    tk.Label(root, text="Clinic Queue System", font=("Arial", 18, "bold")).pack(pady=20)

    # 🔥 Add Doctor Function
    def open_add_doctor():
        win = tk.Toplevel(root)
        win.title("Add Doctor")
        win.geometry("300x300")

        tk.Label(win, text="Doctor Name").pack()
        name = tk.Entry(win)
        name.pack()

        tk.Label(win, text="Specialization").pack()
        spec = tk.Entry(win)
        spec.pack()

        tk.Label(win, text="Fee").pack()
        fee = tk.Entry(win)
        fee.pack()

       
        def save_doctor():
            add_doctor(name.get(), spec.get(), float(fee.get()))
            tk.Label(win, text="Doctor Added Successfully!", fg="green").pack()

        tk.Button(win, text="Save", command=save_doctor).pack(pady=10)
    def view_doctors():
        win = tk.Toplevel(root)
        win.title("Doctors List")
        win.geometry("400x300")

        doctors = get_doctors()

        if not doctors:
            tk.Label(win, text="No doctors available").pack()
        else:
            for doc in doctors:
                text = f"{doc[1]} - {doc[2]} - ₹{doc[3]}"
                tk.Label(win, text=text).pack()

    from tkinter import ttk

    def open_appointment():
        win = tk.Toplevel(root)
        win.title("Book Appointment")
        win.geometry("300x300")

        tk.Label(win, text="Patient Name").pack()
        patient = tk.Entry(win)
        patient.pack()

        tk.Label(win, text="Select Doctor").pack()

        doctors = get_doctors()
        doctor_names = [doc[1] for doc in doctors]

        doctor_combo = ttk.Combobox(win, values=doctor_names)
        doctor_combo.pack()

        def save():
            result = book_appointment(patient.get(), doctor_combo.get())
            messagebox.showinfo("Status", result)

        tk.Button(win, text="Book Appointment", command=save).pack(pady=10)

    def view_appointments():
        print("Button clicked")   
        win = tk.Toplevel()
        win.title("Appointments")

        data = get_appointments()

        if not data:
           tk.Label(win, text="No Appointments Found").pack()
           return

        for row in data:
            text = f"Patient: {row[0]} | Doctor: {row[1]} | Time: {row[2]}"
            tk.Label(win, text=text).pack()
      
    # Buttons
    tk.Button(root, text="Add Doctor", width=20, command=open_add_doctor).pack(pady=10)
    tk.Button(root, text="View Doctors", width=20, command=view_doctors).pack(pady=10)
    tk.Button(root, text="Book Appointment", width=20, command=open_appointment).pack(pady=10)
    tk.Button(root, text="View Appointments", command=view_appointments).pack(pady=10)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

    root.mainloop()