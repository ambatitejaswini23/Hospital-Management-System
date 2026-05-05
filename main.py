import sqlite3

# ---------------- Database Setup ----------------
def setup_database():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        disease TEXT,
        status TEXT DEFAULT 'Discharged'
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS doctors(
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
    )""")

    conn.commit()
    conn.close()

# ---------------- Patient Registration ----------------
def register_patient(name, age, gender, disease):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients(name, age, gender, disease) VALUES (?, ?, ?, ?)",
                   (name, age, gender, disease))
    conn.commit()
    conn.close()
    print("✅ Patient Registered Successfully!")

# ---------------- Doctor Details ----------------
def add_doctor(name, specialization):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors(name, specialization) VALUES (?, ?)",
                   (name, specialization))
    conn.commit()
    conn.close()
    print("✅ Doctor Added Successfully!")

# ---------------- Appointment Booking ----------------
def book_appointment(patient_id, doctor_id, date, time):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments(patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                   (patient_id, doctor_id, date, time))
    conn.commit()
    conn.close()
    print("✅ Appointment Booked Successfully!")

# ---------------- Admit/Discharge ----------------
def update_status(patient_id, status):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET status=? WHERE patient_id=?", (status, patient_id))
    conn.commit()
    conn.close()
    print(f"✅ Patient {status} Successfully!")

# ---------------- Bill Generation ----------------
def generate_bill(patient_id, days, doctor_fee, medicine_cost):
    room_charge = days * 1000
    total = room_charge + doctor_fee + medicine_cost
    print(f"💰 Bill for Patient {patient_id}: Rs.{total}")

# ---------------- Search Patient ----------------
def search_patient(name):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    conn.close()
    for row in results:
        print(row)

# ---------------- Menu System ----------------
def menu():
    setup_database()
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Register Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. Update Admit/Discharge")
        print("5. Generate Bill")
        print("6. Search Patient")
        print("7. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            name = input("Name: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            disease = input("Disease: ")
            register_patient(name, age, gender, disease)

        elif choice == 2:
            name = input("Doctor Name: ")
            specialization = input("Specialization: ")
            add_doctor(name, specialization)

        elif choice == 3:
            pid = int(input("Patient ID: "))
            did = int(input("Doctor ID: "))
            date = input("Date (YYYY-MM-DD): ")
            time = input("Time: ")
            book_appointment(pid, did, date, time)

        elif choice == 4:
            pid = int(input("Patient ID: "))
            status = input("Status (Admitted/Discharged): ")
            update_status(pid, status)

        elif choice == 5:
            pid = int(input("Patient ID: "))
            days = int(input("Days Stayed: "))
            doctor_fee = int(input("Doctor Fee: "))
            medicine_cost = int(input("Medicine Cost: "))
            generate_bill(pid, days, doctor_fee, medicine_cost)

        elif choice == 6:
            name = input("Enter Patient Name: ")
            search_patient(name)

        elif choice == 7:
            print("👋 Exiting System...")
            break

# ---------------- Run Program ----------------
if __name__ == "__main__":
    menu()