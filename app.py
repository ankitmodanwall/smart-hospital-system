import streamlit as st
from database import *
from queue_engine import *
from ambulance_engine import *

st.set_page_config(layout="wide")
init_db()

# -------------------- CUSTOM UI --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.card {
    background-color: #1f2937;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.stButton>button {
    border-radius: 10px;
    background-color: #4f46e5;
    color: white;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #6366f1;
}

[data-testid="stMetric"] {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = None
    st.session_state.user = None
    st.session_state.mobile = None

# ---------------- HEADER ----------------
col1, col2 = st.columns([8,1])
with col1:
    st.markdown("""
    <h1 style='font-size:40px;'>🏥 SmartCare System</h1>
    <p style='color:lightgray;'>AI Powered Hospital Queue + Rural SOS 🚑</p>
    """, unsafe_allow_html=True)

with col2:
    if st.session_state.login:
        if st.button("Logout"):
            st.session_state.login = False
            st.session_state.role = None
            st.session_state.user = None
            st.session_state.mobile = None
            st.rerun()

# =====================================================
# LOGIN / REGISTER SYSTEM (Mobile Based)
# =====================================================
if not st.session_state.login:

    st.markdown("### 👋 Welcome! Login / Register")

    option = st.radio("Select", ["Login", "Register"])

    name = st.text_input("Full Name")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Admin", "Doctor", "Patient"])

    # ---------------- REGISTER ----------------
    if option == "Register":
        if st.button("Register"):
            if len(mobile) != 10 or not mobile.isdigit():
                st.error("Enter valid 10 digit mobile number")
                st.stop()

            if register(name, mobile, password, role):
                st.success("Registered Successfully ✅")
            else:
                st.error("Mobile already registered ❌")

    # ---------------- LOGIN ----------------
    if option == "Login":
        if st.button("Login"):
            result = login(mobile, password)

            if result:
                st.session_state.login = True
                st.session_state.user = result[0]
                st.session_state.role = result[1]
                st.session_state.mobile = mobile
                st.rerun()
            else:
                st.error("Invalid Mobile or Password ❌")

    st.stop()

# =====================================================
# LOAD DATA
# =====================================================
patients = get_patients()
doctors = get_doctors()
sorted_p = sort_queue(patients)

# =====================================================
# METRICS
# =====================================================
m1, m2, m3 = st.columns(3)

m1.metric("👥 Total Patients", len(sorted_p))
m2.metric("👨‍⚕ Available Doctors", len(doctors))
m3.metric("🚑 Active SOS",
          len([p for p in sorted_p if check_ambulance(p)]))

st.divider()

# =====================================================
# ADMIN DASHBOARD
# =====================================================
if st.session_state.role == "Admin":

    st.header("👑 Admin Dashboard")

    tab1, tab2 = st.tabs(["➕ Add Patient", "📋 Live Queue"])

    with tab1:
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 0, 120)
        loc = st.selectbox("Location", ["Urban", "Rural"])
        sym = st.text_area("Symptoms")

        if st.button("Add Patient"):
            if not name or not sym:
                st.warning("Fill all fields")
            else:
                priority = 1 if "chest" in sym.lower() else 3
                uid = add_patient(name, age, loc, sym, priority)

                if uid:
                    st.success(f"Patient Added | UID: {uid}")
                    st.rerun()
                else:
                    st.error("Duplicate Patient Name")

# =====================================================
# DOCTOR DASHBOARD
# =====================================================
elif st.session_state.role == "Doctor":

    st.header("👨‍⚕ Doctor Dashboard")
    st.info("Live Priority Queue")

# =====================================================
# PATIENT DASHBOARD
# =====================================================
elif st.session_state.role == "Patient":

    st.header("🧑 Patient Dashboard")
    st.success(f"Welcome {st.session_state.user}")

# =====================================================
# LIVE QUEUE DISPLAY (ALL ROLES)
# =====================================================

st.markdown("### 🏥 Live Queue")

if not sorted_p:
    st.info("No patients in queue")
else:
    for i, p in enumerate(sorted_p):
        wait = calculate_wait(i, len(doctors))

        st.markdown(f"""
        <div class="card">
        🆔 <b>{p[1]}</b><br>
        👤 {p[2]}<br>
        📍 {p[4]}<br>
        ⚠ Priority: {p[6]}<br>
        👨‍⚕ Doctor: {p[7]}<br>
        ⏳ Estimated Wait: {wait} mins
        </div>
        """, unsafe_allow_html=True)

        if check_ambulance(p):
            st.error("🚑 Ambulance Dispatched (Rural Emergency)")
