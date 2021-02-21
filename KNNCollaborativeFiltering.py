import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


class KNN_CF(object):
    # Neighborhood-based Collaborative Filtering (NBCF)
    def __init__(self, Y_data, k, dist_func=cosine_similarity, uuCF=1):
        self.uuCF = uuCF  # user-user Collaborative Filtering
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        # số lượng người dùng và mặt hàng. Note: thêm 1 vì id bắt đầu từ 0
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1

    def add(self, new_data):
        """
        Cập nhật ma trận Y_data khi có rating mới.
        """
        self.Y_data = np.concatenate((self.Y_data, new_data), axis=0)

    def normalize_Y(self):
        users = self.Y_data[:, 0]  # all users - first col of the Y_data
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_users,))
        for n in range(self.n_users):
            # chỉ số xếp hạng hàng được thực hiện bởi user n
            ids = np.where(users == n)[0].astype(np.int32)
            # chỉ số của tất cả các xếp hạng được liên kết với user n
            item_ids = self.Y_data[ids, 1]
            # và xếp hạng tương ứng
            ratings = self.Y_data[ids, 2]
            # tính trung bình cộng (mean)
            m = np.mean(ratings)
            if np.isnan(m):
                m = 0  # to avoid empty array and nan value
            self.mu[n] = m
            # chuẩn hoá
            self.Ybar_data[ids, 2] = ratings - self.mu[n]

        ################################################
        # tạo thành ma trận xếp hạng dưới dạng ma trận thưa thớt -sparse matrix
        # -> chỉ lưu trữ các số khác không và vị trí của chúng.
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
                                       (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)

    def training(self):
        """
        Chuẩn hóa dữ liệu và tính toán lại ma trận tương tự (sau
        một số rating được thêm vào)
        """
        self.normalize_Y()
        self.similarity()

    def __pred(self, u, i, normalized=1):
        """
        dự đoán xếp hạng của người dùng u cho mục i (chuẩn hóa)
        """
        # tìm tất cả người dùng đã rate cho i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)

        # tìm sự tương đồng giữa user hiện tại và những người khác
        sim = self.S[u, users_rated_i]

        # tìm k người dùng giống nhau nhất
        a = np.argsort(sim)[-self.k:]
        # và mức độ giống nhau tương ứng
        nearest_s = sim[a]
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            # thêm một số nhỏ, ví dụ, 1e-8, để tránh chia cho 0
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)

        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized = 1):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.uuCF: 
            return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend(self, u):
        """
        Xác định tất cả các item nên được đề nghị cho người dùng u.
        Dựa vào : self.pred (u, i)> 0 -> Giả sử đang xem xét các mục
        chưa được đánh giá bởi u
        """
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0:
                    recommended_items.append([i, rating])
        # Sorting
        recommended_items.sort(reverse=True, key=lambda x: x[1])

        return recommended_items

    def get_recommendation(self, userID):
        """
        print all items which should be recommended for each user
        """
        recommended_items = self.recommend(userID)
        return recommended_items

    def getRMSE(self, rate_test): 
        n_tests = rate_test.shape[0]
        SE = 0 # squared error
        for index, row in rate_test.iterrows():
            u_id = row[0]
            i_id = row[1]
            point = row[2]
            #print (u_id, i_id, point)
            pred = self.pred(u_id, i_id, normalized = 0)
            SE += (pred - point)**2 

        RMSE = np.sqrt(SE/n_tests)
        return RMSE
