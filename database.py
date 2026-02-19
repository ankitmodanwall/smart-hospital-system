import sqlite3
from datetime import datetime
import hashlib
import random

DB_NAME = "hospital_queue.db"

# ======================
# CONNECTION
# ======================
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ======================
# INIT DATABASE
# ======================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin','Doctor','Patient')) NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uid TEXT UNIQUE NOT NULL,
        name TEXT UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        location TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        priority INTEGER CHECK(priority IN (1,2,3)) NOT NULL,
        urgency_label TEXT NOT NULL,
        premium INTEGER CHECK(premium IN (0,1)) NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_status(
        id INTEGER PRIMARY KEY CHECK(id=1),
        available_doctors INTEGER NOT NULL CHECK(available_doctors>0)
    )
    """)

    cur.execute("INSERT OR IGNORE INTO system_status(id,available_doctors) VALUES(1,3)")

    conn.commit()
    conn.close()

# ======================
# PASSWORD HASH
# ======================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ======================
# USER FUNCTIONS
# ======================
def create_user(username,password,role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username,hash_password(password),role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username,password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username,hash_password(password))
    )
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

# ======================
# UNIQUE 3 DIGIT ID
# ======================
def generate_uid():
    conn = get_connection()
    cur = conn.cursor()

    while True:
        uid = str(random.randint(100,999))
        cur.execute("SELECT patient_uid FROM patients WHERE patient_uid=?",(uid,))
        if not cur.fetchone():
            conn.close()
            return uid

# ======================
# PATIENT FUNCTIONS
# ======================
def add_patient(name,age,location,symptoms,priority,label,premium):
    conn = get_connection()
    cur = conn.cursor()
    try:
        uid = generate_uid()
        cur.execute("""
        INSERT INTO patients
        (patient_uid,name,age,location,symptoms,priority,urgency_label,premium,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(uid,name,age,location,symptoms,priority,label,
             1 if premium else 0,
             datetime.now().isoformat(timespec="seconds")))
        conn.commit()
        return uid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_all_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()
    return data

def get_available_doctors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT available_doctors FROM system_status WHERE id=1")
    value = cur.fetchone()[0]
    conn.close()
    return value

def set_available_doctors(n):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE system_status SET available_doctors=? WHERE id=1",(n,))
    conn.commit()
    conn.close()
