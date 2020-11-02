from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from csv import DictReader

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///state_parks"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class CampingGear(db.Model):
    """A class object representing camping equipment."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    is_rainy = db.Column(db.Boolean)
    is_winter = db.Column(db.Boolean)
    is_optional = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return "<CampingGear '%s'>" % self.name


def insert_gear(csv_file):
    """Parse CSV and insert into database."""

    with open(csv_file, newline="") as f:
        reader = DictReader(f)
        for row in reader:
            item = CampingGear(
                name=row["name"],
                is_rainy=eval(row["is_rainy"]),
                is_winter=eval(row["is_winter"]),
                is_optional=eval(row["is_optional"]),
                category=row["category"],
            )

            db.session.add(item)

        db.session.commit()


if __name__ == "__main__":
    db.create_all()
    insert_gear("camping-gear.csv")
