import json
from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
	"user1": {"username": "eduardo", "age": 20, "admin": False},
	"user2": {"username": "daniela", "age": 33, "admin": False},
}

@app.route('/users/<username>', methods=["GET"])
def update_user(username):
	user = users.get(username)
	if user:
		user.update(request.json)
		print(user)
		return jsonify(user), 200
	return jsonify({"message": "User not found"}), 404

@app.route('/secret', methods=["GET"])
def secret():
	return jsonify({"message": "This is a secret message"}), 200

if __name__ == '__main__':
	app.run(debug=True)