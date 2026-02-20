import streamlit as st
from database import *
from queue_engine import *
from ambulance_engine import *

st.set_page_config(page_title="SmartCare System", layout="wide")
init_db()

# Hide Streamlit header
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# SESSION INIT
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# HEADER
st.title("🏥 SmartCare System")
st.caption("AI Powered Hospital Queue + Rural SOS 🚑")

# LOGOUT
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# LOGIN BLOCK
if not st.session_state.logged_in:

    st.subheader("Login / Register")

    option = st.radio("Select Option", ["Login", "Register"])

    name = st.text_input("Full Name")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Admin", "Doctor", "Patient"])

    if option == "Register":
        if st.button("Register"):
            if register(name, mobile, password, role):
                st.success("Registered Successfully")
            else:
                st.error("Mobile already exists")

    if option == "Login":
        if st.button("Login"):
            result = login(mobile, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.user = result[0]
                st.session_state.role = result[1]
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# LOAD DATA
patients = get_patients()
doctors = get_doctors()
sorted_p = sort_queue(patients)

# METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", len(sorted_p))
col2.metric("Available Doctors", len(doctors))
col3.metric("Active Rural SOS",
            len([p for p in sorted_p if check_ambulance(p)]))

st.divider()

# ADMIN DASHBOARD
if st.session_state.role == "Admin":

    st.subheader("Add Patient")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    location = st.selectbox("Location", ["Urban", "Rural"])
    symptoms = st.text_area("Symptoms")

    if st.button("Add Patient"):
        priority = 1 if "chest" in symptoms.lower() else 3
        uid = add_patient(name, age, location, symptoms, priority)

        if uid:
            st.success(f"Patient Added | UID: {uid}")
            st.rerun()
        else:
            st.error("Duplicate patient name")

# QUEUE DISPLAY
st.subheader("Live Queue")

if not sorted_p:
    st.info("No patients in queue")
else:
    for i, p in enumerate(sorted_p):
        wait = calculate_wait(i, len(doctors))

        st.markdown(f"""
        ---
        🆔 {p[1]}  
        👤 {p[2]}  
        📍 {p[4]}  
        ⚠ Priority: {p[6]}  
        👨‍⚕ Doctor: {p[7]}  
        ⏳ Estimated Wait: {wait} mins  
        """)

        if check_ambulance(p):
            st.error("🚑 Ambulance Dispatched (Rural Emergency)")