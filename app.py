from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Настройка БД
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or 'sqlite:///blood_pressure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BloodPressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    pulse = db.Column(db.Integer)
    comment = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'systolic': self.systolic,
            'diastolic': self.diastolic,
            'pulse': self.pulse,
            'comment': self.comment
        }

# Инициализация БД
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    """Главная страница с формой и списком измерений"""
    try:
        # Всегда получаем записи, даже для POST-запросов
        records = BloodPressure.query.order_by(BloodPressure.date.desc()).limit(10).all()
        
        if request.method == "POST":
            try:
                # Обработка данных формы
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
                flash("✅ Измерение сохранено!", "success")
                
                # Обновляем записи после добавления нового измерения
                records = BloodPressure.query.order_by(BloodPressure.date.desc()).limit(10).all()

            except ValueError:
                flash("❌ Введите корректные числа!", "error")

        return render_template('index.html', records=records)
    
    except Exception as e:
        flash(f"⚠️ Произошла ошибка: {str(e)}", "error")
        return render_template('index.html', records=[])

@app.route('/get_records')
def get_records():
    """API для получения данных в формате JSON"""
    try:
        records = BloodPressure.query.order_by(BloodPressure.date.asc()).all()
        return jsonify([record.to_dict() for record in records])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)