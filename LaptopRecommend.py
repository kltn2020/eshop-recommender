#importing required modules
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ReadData as data
import codecs
from sklearn.model_selection import train_test_split


##### FUNCTION #####
#a function to combine the values of the important columns into a single string
def combined_specs(row):
    return(row['brand_id']+" "+row['cpu']+" "+row['os']+" "+row['ram']+" "+row['display']+" "+row['display_resolution']+" "+row['display_screen']+" "+row['weight']+" "+row['price']+" "+row['discount_price'])


#a function to get the Name from Index
def get_name_from_index(index):
    return df[df.id==index]['name'].values[0]

#a function to get the Index from Name
def get_index_from_name(name):
    return df[df.name==name]['id'].values[0]

#
def get_contentbased_laptops(laptopName, df):
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

    #Find laptop index of popular laptop
    laptop_index=get_index_from_name(laptopName)

    #Enumerating through all the similarity scores of laptop_popular
    #making a ordered pair of laptop index and similarity scores
    #and returning a list of such ordered pairs in the form of (laptop_index,similarity_scores)
    similar_laptops=list(enumerate(cosine_sim_mat[laptop_index]))
    #print (cosine_sim_mat[laptop_index])

    #Sort similar_laptops in descending order of similarity scores and exclude the similar laptop itself
    sorted_similar_laptops=sorted(similar_laptops,key=lambda x:x[1],reverse=True)[1:]

    return sorted_similar_laptops


def get_collaborative_laptops(laptopName, df):
    specs=['brand_id','cpu','os','ram','display','weight', 'rating_avg', 'discount_price']

    #converting all integer values to string so that they can be concattinated later in the program
    for column in specs:
        df[column]=df[column].apply(str)
    
    #applly the function to each row in the dataframe to store the combined strings into a new column called combined_specs
    df['combined_specs']=df.apply(combined_specs,axis=1)

    # 2. get list result
    #convert a collection of data into Tfidf matrix
    vectorizer = TfidfVectorizer()
    vectorizer=vectorizer.fit_transform(df['combined_specs'])

    #convert a the count matrix into cosine similarity matrix
    cosine_sim_mat=cosine_similarity(vectorizer)

    #Find laptop index of popular laptop
    laptop_index=get_index_from_name(laptopName)

    #Enumerating through all the similarity scores of laptop_popular
    #making a ordered pair of laptop index and similarity scores
    #and returning a list of such ordered pairs in the form of (laptop_index,similarity_scores)
    similar_laptops=list(enumerate(cosine_sim_mat[laptop_index]))
    #print (cosine_sim_mat[laptop_index])

    #Sort similar_laptops in descending order of similarity scores and exclude the similar laptop itself
    sorted_similar_laptops=sorted(similar_laptops,key=lambda x:x[1],reverse=True)[1:]

    return sorted_similar_laptops


def ShowResults(top, list, laptopName):
    i=1
    print("===== LAPTOPS RECOMMEND =====")
    print("The top " + str(top) + " recommended laptops similar to '" + laptopName + "' are: ")
    for element in list:
        if i <= top:
            print(i, ': ', element[0], '-', get_name_from_index(element[0]))
            i+=1

##### MAIN #####
# 1. get data
df = data.getDataProducts()
#df = data.getDataReviews()



laptopInput='Laptop Dell Inspiron 7591 i5 9300H/8GB/256GB/3GB GTX1050/Win10 (N5I5591W)'
#laptopInput='Laptop Apple MacBook Air 2020 i5 1.1GHz/8GB/256GB (Z0YL)'

# 2. get recommend laptop list
laptopsRecommend = get_contentbased_laptops(laptopInput, df)
#laptopsRecommend = get_collaborative_laptops(laptopInput, df)

# 3
ShowResults(5, laptopsRecommend, laptopInput)