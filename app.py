from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ваш_секретный_ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_pressure.db'
db = SQLAlchemy(app)

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    pulse = db.Column(db.Integer)
    comment = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            systolic = int(request.form["systolic"])
            diastolic = int(request.form["diastolic"])
            pulse = int(request.form.get("pulse", 0))
            comment = request.form.get("comment", "")

            if systolic <= 0 or diastolic <= 0:
                flash("❌ Давление должно быть положительным!", "error")
                return redirect(url_for("index"))

            new_record = BloodPressure(
                systolic=systolic,
                diastolic=diastolic,
                pulse=pulse,
                comment=comment
            )
            db.session.add(new_record)
            db.session.commit()
            flash("✅ Измерение сохранено!", "success")

        except ValueError:
            flash("❌ Введите числа корректно!", "error")

    records = BloodPressure.query.order_by(BloodPressure.date.desc()).limit(10).all()
    return render_template("index.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)