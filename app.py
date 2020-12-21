from flask import Flask
from flask import jsonify
from flask import request
import LaptopRecommend

CONST_COUNT_TOP = 20

app = Flask(__name__)

@app.route("/content_based_recommend")
def content_based_recommend():
    product_id = int(request.args.get('product_id'))
    lapRecommender = LaptopRecommend.LaptopRecommend()

    # goi ham tra ve list 20 product id
    arr = lapRecommender.get_contentbased_laptops(product_id)[:CONST_COUNT_TOP]
    print(arr)

    arrOut = []
    for row in arr:
        arrOut.append(row[0])
        
    return jsonify(arrOut)

@app.route("/collaborative_recommend")
def collaborative_recommend():
    user_id = int(request.args.get('user_id'))
    lapRecommender = LaptopRecommend.LaptopRecommend()

    # goi ham tra ve list 20 product id
    arr = lapRecommender.get_KNN_CF(user_id)[:CONST_COUNT_TOP]
    print(arr)
    
    arrOut = []
    for row in arr:
        arrOut.append(row[0])
        
    return jsonify(arrOut)

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"), debug=False)
