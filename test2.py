from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data ={
        "user-id":user_id,
        "username":"Arjun-Bhattarai",  
        "email":"john.doe@example.com"
    }

    extra=request.args.get("extra")
    if extra:
        user_data["extra"]=extra
    return jsonify(user_data),200


@app.route("/create-user/", methods=["POST"])
def create_user():
    print("Creating a new user")
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON"}), 400
    print("Received data:", data)
    return jsonify(data)  ,201

if __name__ == "__main__":
    app.run(debug=True)