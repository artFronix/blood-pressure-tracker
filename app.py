from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blood_pressure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# Создаем таблицы при первом запросе
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    """Главная страница с формой и графиками"""
    records = BloodPressure.query.order_by(BloodPressure.date.asc()).all()
    records_json = [record.to_dict() for record in records]
    return render_template(
        'index.html',
        records=records[-10:],  # Последние 10 записей для таблицы
        records_json=records_json  # Все записи для графиков
    )

@app.route("/add", methods=["POST"])
def add_measurement():
    """Обработка добавления нового измерения"""
    try:
        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])
        pulse = int(request.form.get("pulse", 0))
        comment = request.form.get("comment", "")

        if systolic <= 0 or diastolic <= 0:
            flash("❌ Давление должно быть положительным числом!", "error")
            return redirect(url_for("index"))

        new_record = BloodPressure(
            systolic=systolic,
            diastolic=diastolic,
            pulse=pulse,
            comment=comment
        )
        db.session.add(new_record)
        db.session.commit()
        
        status = analyze_pressure(systolic, diastolic)
        if status != "normal":
            flash(f"⚠️ {status}", "warning")
        else:
            flash("✅ Измерение сохранено!", "success")

    except ValueError:
        flash("❌ Введите корректные числа!", "error")
    
    return redirect(url_for("index"))

@app.route('/static/<path:path>')
def serve_static(path):
    """Обработка статических файлов"""
    return send_from_directory('static', path)

def analyze_pressure(systolic, diastolic):
    """Анализ показателей давления"""
    if systolic < 90 or diastolic < 60:
        return "Гипотензия (низкое давление)"
    elif systolic >= 140 or diastolic >= 90:
        return "Гипертензия (высокое давление)"
    elif systolic >= 120 or diastolic >= 80:
        return "Прегипертензия (повышенное)"
    return "normal"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)