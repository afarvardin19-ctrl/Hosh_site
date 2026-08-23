from flask import Flask, render_template, request, redirect
import sqlite3
import uuid

app = Flask(__name__)
DB = "database.db"


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

        conn = sqlite3.connect(DB)

        conn.execute("""
            INSERT INTO students (
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        conn.close()

        return redirect(
            "https://esanj.ir/multiple-intelligences-inventory"
        )

    return render_template("register.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        students=students
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
