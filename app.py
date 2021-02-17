from flask import Flask
from flask import jsonify
from flask import request
import LaptopRecommend

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

    # get limit
    limit = CONST_COUNT_TOP
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = CONST_COUNT_TOP

    # print("user_id: ", user_id)
    # print("product_id: ", product_id)

    # init data recommend
    lapRecommender = LaptopRecommend.LaptopRecommend()

    # return list  product id
    arr = lapRecommender.get_contentbased_laptops(product_id)[:limit]
    # print(arr)

    arrOut = []
    for row in arr:
        arrOut.append(row[0])

    #print("ket qua: ",  arrOut)
    return jsonify(arrOut)


@app.route("/collaborative_recommend")
def collaborative_recommend():
    # get user_id
    user_id = 0
    try:
        user_id = int(request.args.get('user_id'))
    except:
        user_id = 0

    # get limit
    limit = CONST_COUNT_TOP
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = CONST_COUNT_TOP
    lapRecommender = LaptopRecommend.LaptopRecommend()
    #print("user_id: ", user_id)

    # return list product id
    arr = lapRecommender.get_KNN_CF(user_id)[:limit]
    # print(arr)

    arrOut = []
    for row in arr:
        arrOut.append(row[0])

    #print("ket qua: ", arrOut)
    return jsonify(arrOut)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=False)
