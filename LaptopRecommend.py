#importing required modules
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ReadData as data
import codecs
import KNNCollaborativeFiltering as BNCF
import MFCollaborativeFiltering as MFCF
from sklearn.model_selection import train_test_split

# Constant value
CONST_K = 100   #K Neighbor User
CONST_UUCF = 1
CONST_TEST_PERCENT = 0.05    #only TEST 5%

##### FUNCTION #####
#a function to combine the values of the important columns into a single string
def combined_specs(row):
    return(row['brand_id']+" "+row['cpu']+" "+row['os']+" "+row['ram']+" "+row['display']+" "+row['display_resolution']+" "+row['display_screen']+" "+row['weight']+" "+row['price']+" "+row['discount_price'])


#a function to get the Name from Index
def get_name_from_index(index, df):
    return df[df.id==index]['name'].values[0]

#a function to get the Index from Name
def get_index_from_name(name, df):
    return df[df.name==name]['id'].values[0]


def ShowResults(top, list):
    i=1
    print("===== LAPTOPS RECOMMEND =====")
    print("The top " + str(top) + " recommended laptops are: ")
    
    for element in list:
        if i <= top:
            #print(i, ': ', element[0], '-', get_name_from_index(element[0], dfProducts))
            print(i, ': ', element[0], '-', element[1], '-')
            i+=1

class LaptopRecommend(object):
    def __init__(self):
        self.dfProducts = data.getDataProducts()
        self.dfReviews = data.getDataReviews()
        #print(self.dfReviews) 

    def get_contentbased_laptops(self, laptop_id):
        df = self.dfProducts
        specs=['brand_id','cpu','os','ram','display', 'display_resolution', 'display_screen', 'weight', 'price', 'discount_price']

        #converting all integer values to string so that they can be concattinated later in the program
        for column in specs:
            df[column]=df[column].apply(str)
        
        #applly the function to each row in the dataframe to store the combined strings into a new column called combined_specs
        df['combined_specs']=df.apply(combined_specs,axis=1)

        # 2. get list result
        #convert a collection of data into Tfidf matrix
        vectorizer = TfidfVectorizer()
        vectorizer=vectorizer.fit_transform(df['combined_specs'])

        #convert a the Tfidf matrix into cosine similarity matrix
        cosine_sim_mat=cosine_similarity(vectorizer)

        #Enumerating through all the similarity scores of laptop_popular
        #making a ordered pair of laptop index and similarity scores
        #and returning a list of such ordered pairs in the form of (laptop_id,similarity_scores)
        similar_laptops=list(enumerate(cosine_sim_mat[laptop_id]))

        #Sort similar_laptops in descending order of similarity scores and exclude the similar laptop itself
        sorted_similar_laptops=sorted(similar_laptops,key=lambda x:x[1],reverse=True)[1:]

        return sorted_similar_laptops
    
    def get_KNN_CF(self, userID):
        # prepare data
        df = self.dfReviews
        dfRating = df.filter(items=['user_id', 'product_id', 'point'])
        rate_train, rate_test = train_test_split(dfRating, test_size=CONST_TEST_PERCENT)        

        # Training data
        Y_data = rate_train.to_numpy()
        rs = BNCF.KNN_CF(Y_data, k = CONST_K, uuCF = CONST_UUCF)
        rs.training()

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
        print ('User-user CF, (Root mean square error) RMSE =', RMSE)
        return rs.get_recommendation(userID)

##### MAIN #####
# 1. get data
#lapRecommend = LaptopRecommend()
#inputLaptopID = 1
#inputUserID = 3
#laptopInput='Laptop Dell Inspiron 7591 i5 9300H/8GB/256GB/3GB GTX1050/Win10 (N5I5591W)'


# 2. get recommend laptop list
#laptopsRecommend = get_contentbased_laptops(laptopInput, dfProducts)
#get_MF_CF(inputUserID, dfReviews)
#laptopsRecommend = lapRecommend.get_KNN_CF(inputUserID)

# 3
#ShowResults(5, laptopsRecommend)