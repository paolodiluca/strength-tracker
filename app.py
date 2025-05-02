from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

"""Strength‑tracker backend
---------------------------------
Stores users, predefined exercises and workout entries.
Each entry now saves *reps_left*, *reps_right*, *weight* **and** the
estimated 1‑RM strength per side using the classic **Epley formula**::

    1RM = weight × (1 + reps / 30)

The estimated fields are computed once on write and persisted so they
can be queried/sorted later without recalculation.
"""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strength.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

# ---------- Models ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    entries = db.relationship("Entry", backref="user", lazy=True)

    def set_password(self, pw: str):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw: str) -> bool:
        return check_password_hash(self.password_hash, pw)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.String(80), nullable=False)
    reps_left = db.Column(db.Integer, nullable=False)
    reps_right = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    strength_left = db.Column(db.Float, nullable=False)
    strength_right = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @staticmethod
    def epley_1rm(weight: float, reps: int) -> float:
        """Classic Epley 1‑RM estimator (valid up to ~12 reps)."""
        return round(weight * (1 + reps / 30), 2)


# ---------- Routes ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"msg": "invalid payload"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "username exists"}), 409

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "user created", "user_id": user.id}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password", "")):
        return jsonify({"user_id": user.id}), 200
    return jsonify({"msg": "bad credentials"}), 401


@app.route("/entries", methods=["POST"])
def add_entry():
    """Add a new workout entry and compute 1‑RM sides."""
    data = request.get_json(force=True)
    try:
        # basic validation
        reps_l = int(data["reps_left"])
        reps_r = int(data["reps_right"])
        if not (0 < reps_l <= 12 and 0 < reps_r <= 12):
            raise ValueError("reps must be 1–12 for reliable 1‑RM estimate")

        weight = float(data["weight"])
        entry = Entry(
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            exercise=data["exercise"],
            reps_left=reps_l,
            reps_right=reps_r,
            weight=weight,
            strength_left=Entry.epley_1rm(weight, reps_l),
            strength_right=Entry.epley_1rm(weight, reps_r),
            user_id=int(data["user_id"])
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({"msg": "entry stored"}), 201
    except Exception as e:
        return jsonify({"msg": "invalid entry", "detail": str(e)}), 400


@app.route("/entries/<int:user_id>", methods=["GET"])
def get_entries(user_id: int):
    entries = Entry.query.filter_by(user_id=user_id).order_by(Entry.date).all()
    return jsonify([{
        "id": e.id,
        "date": e.date.isoformat(),
        "exercise": e.exercise,
        "reps_left": e.reps_left,
        "reps_right": e.reps_right,
        "weight": e.weight,
        "strength_left": e.strength_left,
        "strength_right": e.strength_right
    } for e in entries])


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify([{"id": e.id, "name": e.name} for e in exercises])


# ---------- App Start ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Exercise.query.count() == 0:
            predefined = [
                "Tricep Extension (Cable or Dumbbell)",
                "Bicep Curl (Cable or Dumbbell)",
                "Bulgarian Split Squat",
                "Single-Leg Leg Curl (Machine)",
                "Standing Calf Raise (Machine)",
                "Dumbbell Bench Press",
                "Dumbbell Shoulder Press",
                "Dumbbell Lateral Raise",
                "Single-Arm Horizontal Row (Cable or Dumbbell)",
                "Single-Arm Vertical Row (Pulldown or Machine)"
            ]
            db.session.bulk_save_objects([Exercise(name=n) for n in predefined])
            db.session.commit()
            print("✅ Predefined exercises added.")

    app.run(debug=True)
