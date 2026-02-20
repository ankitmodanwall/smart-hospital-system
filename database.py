import sqlite3
import random

DB = "hospital.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        name TEXT UNIQUE,
        age INTEGER,
        location TEXT,
        symptoms TEXT,
        priority INTEGER,
        doctor TEXT DEFAULT 'Pending'
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        available INTEGER
    )
    """)

    c.execute("SELECT COUNT(*) FROM doctors")
    if c.fetchone()[0] == 0:
        doctors = [
            ("Dr. Sharma", 1),
            ("Dr. Verma", 1),
            ("Dr. Khan", 1)
        ]
        c.executemany("INSERT INTO doctors(name,available) VALUES(?,?)", doctors)

    conn.commit()
    conn.close()


# ---------------- USERS ----------------

def register(name, mobile, password, role):
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users(name,mobile,password,role) VALUES(?,?,?,?)",
            (name, mobile, password, role)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False


def login(mobile, password):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "SELECT name, role FROM users WHERE mobile=? AND password=?",
        (mobile, password)
    )
    result = c.fetchone()
    conn.close()
    return result


# ---------------- PATIENTS ----------------

def generate_uid():
    return str(random.randint(100, 999))


def add_patient(name, age, location, symptoms, priority):
    try:
        conn = connect()
        c = conn.cursor()

        uid = generate_uid()

        c.execute("""
        INSERT INTO patients(uid,name,age,location,symptoms,priority)
        VALUES(?,?,?,?,?,?)
        """, (uid, name, age, location, symptoms, priority))

        conn.commit()
        conn.close()
        return uid
    except:
        return None


def get_patients():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()
    conn.close()
    return data


def get_doctors():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM doctors WHERE available=1")
    data = c.fetchall()
    conn.close()
    return data