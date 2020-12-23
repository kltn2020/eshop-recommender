from flask import Flask
from flask import jsonify
from flask import request
import LaptopRecommend
import ReadData

CONST_COUNT_TOP = 20

app = Flask(__name__)

@app.route("/content_based_recommend")
def content_based_recommend():
    # get user_id
    user_id = 0
    try:
        user_id = int(request.args.get('user_id'))
    except:
        user_id = 0

    # get product_id
    product_id = 0
    try:
        product_id = int(request.args.get('product_id'))
    except:
        product_id = 0

    if product_id == 0:
        product_id = ReadData.GetProductID(user_id)

    # init data recommend
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
