from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/content_based_recommend")
def content_based_recommend():
    user_id = request.args.get('user_id')
    print(user_id)
    return jsonify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

@app.route("/collaborative_recommend")
def collaborative_recommend():
    user_id = request.args.get('user_id')
    print(user_id)
    return jsonify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
