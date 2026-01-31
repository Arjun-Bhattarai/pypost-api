from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating,
        }


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route("/destination", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([dest.dict() for dest in destinations])


@app.route("/destination/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.dict())
    else:
        return jsonify({"error": "Destination not found"}), 404


@app.route("/destination", methods=["POST"])
def add_destination():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    required = ["destination", "name", "country", "rating"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_destination = Destination(
        destination=data["destination"],
        name=data["name"],
        country=data["country"],
        rating=data["rating"],
    )

    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.dict()), 201



@app.route("/destination/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)
    if destination:
        destination.destination = data.get("destination", destination.destination)
        destination.name = data.get("name", destination.name)
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)
        db.session.commit()
        return jsonify(destination.dict())
    else:
        return jsonify({"error": "Destination not found"}), 404
    

@app.route("/destination/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id): 
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message": "Destination deleted"})
    else:
        return jsonify({"error": "Destination not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
