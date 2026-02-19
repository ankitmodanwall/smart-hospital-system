import sqlite3
import random

def init_db():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        mobile TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # PATIENT TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        name TEXT,
        age INTEGER,
        location TEXT,
        symptoms TEXT,
        priority INTEGER,
        doctor TEXT
    )
    """)

    # DOCTORS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        available INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- USER SYSTEM ---------------- #

def register(username, mobile, password, role):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, mobile, password, role) VALUES (?,?,?,?)",
                  (username, mobile, password, role))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def login(mobile, password):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute("SELECT username, role FROM users WHERE mobile=? AND password=?",
              (mobile, password))

    result = c.fetchone()
    conn.close()

    if result:
        return result  # (username, role)
    return None


# ---------------- PATIENT SYSTEM ---------------- #

def generate_uid():
    return str(random.randint(100, 999))


def add_patient(name, age, location, symptoms, priority):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    # Prevent duplicate patient name
    c.execute("SELECT * FROM patients WHERE name=?", (name,))
    if c.fetchone():
        conn.close()
        return None

    uid = generate_uid()

    c.execute("""
    INSERT INTO patients (uid, name, age, location, symptoms, priority, doctor)
    VALUES (?,?,?,?,?,?,?)
    """, (uid, name, age, location, symptoms, priority, "Pending"))

    conn.commit()
    conn.close()

    return uid


def get_patients():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute("SELECT * FROM patients")
    data = c.fetchall()

    conn.close()
    return data


def get_doctors():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute("SELECT * FROM doctors WHERE available=1")
    data = c.fetchall()

    conn.close()
    return data
