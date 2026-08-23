import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or os.environ.get("POSTGRES_URL")
    or os.environ.get("POSTGRESQL_URL")
)

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )


def get_db():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL در Environment سرویس Hosh-site-1 تنظیم نشده است."
        )

    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_db()

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hosh_registrations (
                id SERIAL PRIMARY KEY,
                registration_code VARCHAR(20) UNIQUE NOT NULL,
                fullname TEXT NOT NULL,
                father_name TEXT NOT NULL,
                province TEXT NOT NULL,
                city TEXT NOT NULL,
                national_id TEXT NOT NULL,
                age INTEGER NOT NULL,
                birth_date TEXT NOT NULL,
                father_phone TEXT,
                phone TEXT NOT NULL,
                school TEXT,
                grade TEXT NOT NULL,
                address TEXT,
                postal_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        father_name = request.form.get("father_name", "").strip()
        province = request.form.get("province", "").strip()
        city = request.form.get("city", "").strip()
        national_id = request.form.get("national_id", "").strip()
        age = request.form.get("age", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        father_phone = request.form.get("father_phone", "").strip()
        phone = request.form.get("phone", "").strip()
        school = request.form.get("school", "").strip()
        grade = request.form.get("grade", "").strip()
        address = request.form.get("address", "").strip()
        postal_code = request.form.get("postal_code", "").strip()

        if not fullname:
            return "نام و نام خانوادگی وارد نشده است."

        if not father_name:
            return "نام پدر وارد نشده است."

        if not province:
            return "استان وارد نشده است."

        if not city:
            return "شهر وارد نشده است."

        if not national_id:
            return "کد ملی وارد نشده است."

        if not age:
            return "سن وارد نشده است."

        if not birth_date:
            return "تاریخ تولد وارد نشده است."

        if not phone:
            return "شماره تلفن وارد نشده است."

        if not grade:
            return "پایه تحصیلی انتخاب نشده است."

        try:
            age = int(age)
        except ValueError:
            return "سن باید عدد باشد."

        code = uuid.uuid4().hex[:8].upper()

        conn = get_db()

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO hosh_registrations (
                        registration_code,
                        fullname,
                        father_name,
                        province,
                        city,
                        national_id,
                        age,
                        birth_date,
                        father_phone,
                        phone,
                        school,
                        grade,
                        address,
                        postal_code
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    code,
                    fullname,
                    father_name,
                    province,
                    city,
                    national_id,
                    age,
                    birth_date,
                    father_phone,
                    phone,
                    school,
                    grade,
                    address,
                    postal_code
                ))

            conn.commit()

        finally:
            conn.close()

        return redirect(
            "https://esanj.ir/multiple-intelligences-inventory"
        )

    return render_template("register.html")


@app.route("/admin")
def admin():

    conn = get_db()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM hosh_registrations
                ORDER BY id DESC
            """)

            students = cur.fetchall()

    finally:
        conn.close()

    return render_template(
        "admin.html",
        students=students
    )


# ساخت جدول هنگام شروع برنامه
with app.app_context():
    init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
