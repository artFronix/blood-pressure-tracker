from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_pressure.db'
db = SQLAlchemy(app)

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)  # верхнее
    diastolic = db.Column(db.Integer, nullable=False)  # нижнее
    pulse = db.Column(db.Integer)  # пульс
    comment = db.Column(db.String(200))  # комментарий
    date = db.Column(db.DateTime, default=datetime.now)  # дата и время

    def to_dict(self):
        """Конвертация записи в словарь для JSON"""
        return {
            'date': self.date.isoformat(),
            'systolic': self.systolic,
            'diastolic': self.diastolic,
            'pulse': self.pulse,
            'comment': self.comment
        }

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
                flash("❌ Давление должно быть положительным числом!", "error")
                return redirect(url_for("index"))

            # Анализ давления
            status = analyze_pressure(systolic, diastolic)
            if status != "normal":
                flash(f"⚠️ {status}", "warning")

            # Сохраняем новое измерение
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
            flash("❌ Введите корректные числа!", "error")

        return redirect(url_for("index"))

    # Получаем все записи в хронологическом порядке для графиков
    records = BloodPressure.query.order_by(BloodPressure.date.asc()).all()
    
    # Конвертируем записи в словари для JSON
    records_json = [record.to_dict() for record in records]
    
    return render_template(
        "index.html",
        records=records,  # для таблицы
        records_json=records_json  # для графиков
    )

def analyze_pressure(systolic, diastolic):
    """Анализ показателей давления"""
    if systolic < 90 or diastolic < 60:
        return "Гипотензия (низкое давление)"
    elif systolic >= 140 or diastolic >= 90:
        return "Гипертензия (высокое давление)"
    elif systolic >= 120 or diastolic >= 80:
        return "Прегипертензия (повышенное)"
    else:
        return "normal"

if __name__ == "__main__":
    app.run(debug=True)