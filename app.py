import streamlit as st
import pandas as pd
import plotly.express as px
from database import connect_db

st.set_page_config(
    page_title="Hospital Management System",
    layout="wide"
)

st.title("🏥 Hospital Management System")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Add Patient",
        "View Patients",
        "Update Patient",
        "Delete Patient",
        "Add Doctor",
        "View Doctors",
        "Book Appointment",
        "View Appointments",
        "Dashboard"
    ]
)

# =========================
# ADD PATIENT
# =========================

if menu == "Add Patient":

    st.subheader("Add Patient")

    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    disease = st.text_input("Disease")
    phone = st.text_input("Phone Number")

    if st.button("Add Patient"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO patients
            (patient_name,age,disease,phone)
            VALUES(%s,%s,%s,%s)
            """,
            (patient_name, age, disease, phone)
        )

        conn.commit()
        conn.close()

        st.success("Patient Added Successfully ✅")

# =========================
# VIEW PATIENTS
# =========================

elif menu == "View Patients":

    st.subheader("All Patients")

    conn = connect_db()

    df = pd.read_sql(
        "SELECT * FROM patients",
        conn
    )

    st.dataframe(df)

    conn.close()

# =========================
# UPDATE PATIENT
# =========================

elif menu == "Update Patient":

    st.subheader("Update Patient")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1
    )

    name = st.text_input("New Name")
    disease = st.text_input("New Disease")

    if st.button("Update"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE patients
            SET patient_name=%s,
                disease=%s
            WHERE patient_id=%s
            """,
            (
                name,
                disease,
                patient_id
            )
        )

        conn.commit()
        conn.close()

        st.success("Patient Updated ✅")

# =========================
# DELETE PATIENT
# =========================

elif menu == "Delete Patient":

    st.subheader("Delete Patient")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1
    )

    if st.button("Delete"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM patients
            WHERE patient_id=%s
            """,
            (patient_id,)
        )

        conn.commit()
        conn.close()

        st.success("Patient Deleted ✅")

# =========================
# ADD DOCTOR
# =========================

elif menu == "Add Doctor":

    st.subheader("Add Doctor")

    doctor_name = st.text_input("Doctor Name")
    specialization = st.text_input("Specialization")

    if st.button("Add Doctor"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO doctors
            (doctor_name,specialization)
            VALUES(%s,%s)
            """,
            (
                doctor_name,
                specialization
            )
        )

        conn.commit()
        conn.close()

        st.success("Doctor Added ✅")

# =========================
# VIEW DOCTORS
# =========================

elif menu == "View Doctors":

    st.subheader("All Doctors")

    conn = connect_db()

    df = pd.read_sql(
        "SELECT * FROM doctors",
        conn
    )

    st.dataframe(df)

    conn.close()

# =========================
# BOOK APPOINTMENT
# =========================

elif menu == "Book Appointment":

    st.subheader("Book Appointment")

    patient_name = st.text_input("Patient Name")

    doctor_name = st.text_input("Doctor Name")

    appointment_date = st.date_input(
        "Appointment Date"
    )

    if st.button("Book Now"):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO appointments
            (patient_name,doctor_name,appointment_date)
            VALUES(%s,%s,%s)
            """,
            (
                patient_name,
                doctor_name,
                appointment_date
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "Appointment Booked ✅"
        )

# =========================
# VIEW APPOINTMENTS
# =========================

elif menu == "View Appointments":

    st.subheader("Appointments")

    conn = connect_db()

    df = pd.read_sql(
        "SELECT * FROM appointments",
        conn
    )

    st.dataframe(df)

    conn.close()

# =========================
# DASHBOARD
# =========================

elif menu == "Dashboard":

    st.subheader("Hospital Dashboard")

    conn = connect_db()

    patients_df = pd.read_sql(
        "SELECT * FROM patients",
        conn
    )

    doctors_df = pd.read_sql(
        "SELECT * FROM doctors",
        conn
    )

    appointments_df = pd.read_sql(
        "SELECT * FROM appointments",
        conn
    )

    conn.close()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Patients",
        len(patients_df)
    )

    col2.metric(
        "Total Doctors",
        len(doctors_df)
    )

    col3.metric(
        "Total Appointments",
        len(appointments_df)
    )

    if not appointments_df.empty:

        st.subheader(
            "Doctor Wise Patients"
        )

        doctor_count = (
            appointments_df
            .groupby("doctor_name")
            .size()
            .reset_index(name="patients")
        )

        fig1 = px.bar(
            doctor_count,
            x="doctor_name",
            y="patients",
            color="doctor_name",
            title="Patients Handled By Doctors"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    if not patients_df.empty:

        st.subheader(
            "Disease Analysis"
        )

        disease_count = (
            patients_df
            .groupby("disease")
            .size()
            .reset_index(name="count")
        )

        fig2 = px.pie(
            disease_count,
            names="disease",
            values="count",
            title="Disease Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    if not appointments_df.empty:

        busiest_doctor = (
            appointments_df["doctor_name"]
            .value_counts()
            .idxmax()
        )

        st.success(
            f"Most Busy Doctor : {busiest_doctor}"
        )