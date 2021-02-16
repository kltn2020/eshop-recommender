# importing required modules
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ReadData as data
import codecs
import KNNCollaborativeFiltering as BNCF
from sklearn.model_selection import train_test_split

# Constant value
CONST_K = 100  # K Neighbor User
CONST_UUCF = 1
CONST_TEST_PERCENT = 0.05  # only TEST 5%

##### FUNCTION #####
# hàm để kết hợp các giá trị của các cột quan trọng thành một chuỗi đơn


def combined_specs(row):
    return(row['brand_id']+" "+row['cpu']+" "+row['os']+" "+row['ram']+" "+row['display']+" "+row['display_resolution']+" "+row['display_screen']+" "+row['weight']+" "+row['price']+" "+row['discount_price'])


# a function to get the Name from Index
def get_name_from_index(index, df):
    return df[df.id == index]['name'].values[0]

# a function to get the Index from Name


def get_index_from_name(name, df):
    return df[df.name == name]['id'].values[0]


class LaptopRecommend(object):
    def __init__(self):
        self.dfProducts = data.getDataProducts()
        self.dfReviews = data.getDataReviews()
        # print(self.dfReviews)

    def get_contentbased_laptops(self, laptop_id):
        df = self.dfProducts
        specs = ['brand_id', 'cpu', 'os', 'ram', 'display', 'display_resolution',
                 'display_screen', 'weight', 'price', 'discount_price']

        # chuyển đổi tất cả các giá trị số nguyên thành chuỗi => nối chuỗi
        for column in specs:
            df[column] = df[column].apply(str)

        # áp dụng hàm cho mỗi hàng trong khung dữ liệu để lưu trữ các chuỗi được kết hợp vào một cột mới được gọi là combined_specs
        df['combined_specs'] = df.apply(combined_specs, axis=1)

        # 2. nhận kết quả danh sách
        # chuyển đổi tập hợp dữ liệu thành ma trận Tfidf
        vectorizer = TfidfVectorizer()
        vectorizer = vectorizer.fit_transform(df['combined_specs'])

        # chuyển đổi ma trận Tfidf thành ma trận tương tự cosine
        cosine_sim_mat = cosine_similarity(vectorizer)

        # tạo một cặp dữ liệu trả về của laptop có thứ tự và điểm số tương tự
        # => trả về danh sách các cặp được sắp xếp như vậy ở dạng (laptop_id, similarity_scores)
        similar_laptops = list(enumerate(cosine_sim_mat[laptop_id]))

        # Sắp xếp các laptop tương tự theo thứ tự giảm dần của điểm số tương tự và loại trừ chính nó
        sorted_similar_laptops = sorted(
            similar_laptops, key=lambda x: x[1], reverse=True)[1:]

        return sorted_similar_laptops

    def get_KNN_CF(self, userID):
        # prepare data
        df = self.dfReviews
        dfRating = df.filter(items=['user_id', 'product_id', 'point'])
        rate_train = dfRating

        # Training data
        Y_data = rate_train.to_numpy()
        rs = BNCF.KNN_CF(Y_data, k=CONST_K, uuCF=CONST_UUCF)
        rs.training()

        return rs.get_recommendation(userID)
