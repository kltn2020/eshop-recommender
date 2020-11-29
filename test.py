import pandas as pd
import numpy as np
import KNNCollaborativeFiltering as BNCF
import ReadData as data
from sklearn.model_selection import train_test_split

# data file 
dfRating = data.getDataReviews()
dfRating = dfRating.filter(items=['user_id', 'product_id', 'point'])
rate_train, rate_test = train_test_split(dfRating, test_size=0.2)    #only TEST 20%
size_train = int(len(dfRating) * .75)
print(size_train)
train_data = dfRating.iloc[9:10] 
print(train_data)
print(dfRating.head(10))
Y_data = rate_train.to_numpy()
rs = BNCF.KNN_CF(Y_data, k = 30, uuCF = 0)
rs.fit()

#rs.print_recommendation()
n_tests = rate_test.shape[0]
SE = 0 # squared error

for index, row in rate_test.iterrows():
     u_id = row[0]
     i_id = row[1]
     point = row[2]
     #print (u_id, i_id, point)
     pred = rs.pred(u_id, i_id, normalized = 0)
     SE += (pred - point)**2 

RMSE = np.sqrt(SE/n_tests)
print ('User-user CF, RMSE =', RMSE)