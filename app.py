import streamlit as st
import time
from database import *
from queue_logic import sort_queue,calculate_wait
from ai_engine import grok_triage

st.set_page_config(page_title="Smart Hospital",layout="wide",page_icon="🏥")
init_db()

# =========================
# SESSION
# =========================
if "logged" not in st.session_state:
    st.session_state.logged=False
    st.session_state.role=None
    st.session_state.user=None

# =========================
# HEADER
# =========================
col1,col2=st.columns([8,1])
with col1:
    st.title("🏥 Smart Hospital System")
with col2:
    if st.session_state.logged:
        if st.button("🔓 Logout"):
            st.session_state.logged=False
            st.rerun()

# =========================
# LOGIN
# =========================
def login_ui():
    st.subheader("Login / Register")
    option=st.radio("Select",["Login","Register"])
    user=st.text_input("Username")
    pwd=st.text_input("Password",type="password")
    role=st.selectbox("Role",["Admin","Doctor","Patient"])

    if option=="Register":
        if st.button("Register"):
            if create_user(user,pwd,role):
                st.success("Registered Successfully")
            else:
                st.error("Username already exists")

    if option=="Login":
        if st.button("Login"):
            r=authenticate_user(user,pwd)
            if r:
                st.session_state.logged=True
                st.session_state.role=r
                st.session_state.user=user
                st.rerun()
            else:
                st.error("Invalid credentials")

if not st.session_state.logged:
    login_ui()
    st.stop()

# =========================
# LOAD DATA
# =========================
patients=get_all_patients()
sorted_p=sort_queue(patients)
docs=get_available_doctors()

# =========================
# METRICS
# =========================
m1,m2=st.columns(2)
m1.metric("Available Doctors",docs)
m2.metric("Queue Length",len(sorted_p))
st.divider()

# =========================
# ADMIN
# =========================
if st.session_state.role=="Admin":
    st.subheader("Admin Panel")

    tab1,tab2=st.tabs(["Add Patient","Live Queue"])

    with tab1:
        name=st.text_input("Patient Name")
        age=st.number_input("Age",0,120)
        location=st.selectbox("Location",["Urban","Rural"])
        premium=st.checkbox("₹99 Premium")
        symptoms=st.text_area("Symptoms")

        if st.button("Submit"):
            priority,label=grok_triage(symptoms,age,location)
            uid=add_patient(name,age,location,symptoms,priority,label,premium)

            if uid:
                st.success(f"Patient Added | UID: {uid}")
            else:
                st.error("Patient name already exists")

    with tab2:
        st.dataframe(calculate_wait(sorted_p,docs),use_container_width=True)

# =========================
# DOCTOR
# =========================
elif st.session_state.role=="Doctor":
    st.subheader("Doctor Dashboard")
    st.dataframe(calculate_wait(sorted_p,docs),use_container_width=True)

# =========================
# PATIENT
# =========================
elif st.session_state.role=="Patient":
    st.subheader("My Status")

    my_data=[p for p in sorted_p if p[2]==st.session_state.user]

    if my_data:
        p=my_data[0]
        position=sorted_p.index(p)+1
        wait=(position-1)//docs*10

        st.success(f"🆔 UID: {p[1]}")
        st.info(f"Priority: {p[6]}")
        st.warning(f"Estimated Wait: {wait} mins")
    else:
        st.warning("You are not in queue")

# =========================
# AUTO REFRESH
# =========================
time.sleep(5)
st.rerun()
