# eshop-recommender

Call WEBSERVER:
http://localhost:5000/content_based_recommend?product_id=6

http://localhost:5000/collaborative_recommend?user_id=5



-- > Data item cần import vào hệ thống bao gồm: table products
brand_id
cpu
gpu
os
ram
display
display_resolution
display_screen
weight
rating_avg
discount_price

--> Data user cần sử dụng: table reviews
user_id
product_id
point

--> Doc tham khảo:
https://heartbeat.fritz.ai/recommender-systems-with-python-part-i-content-based-filtering-5df4940bd831
https://sites.google.com/a/tvu.edu.vn/phucnhan/home/tai-lieu-tham-khao/data-mining/he-thong-goi-y
https://viblo.asia/p/xay-dung-mot-he-thong-goi-y-collaborative-filtering-de-dang-nhu-the-nao-GrLZDXv3Zk0
https://realpython.com/build-recommendation-engine-collaborative-filtering/



https://github.com/nghthanhtam/movierecommender/blob/master/flask_be/api/Dataset/RecommendationSystem.py
