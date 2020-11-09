#importing required modules and reading the file called 'laptop'
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
df=pd.read_csv('laptop.csv')

#list of specifications of laptops to work on
specs=['HDD','SSD','RAM','Processor','Weight','Price']

#converting all integer values to string so that they can be concattinated later in the program
for column in specs:
    df[column]=df[column].apply(str)

#a function to combine the values of the important columns into a single string
def combined_specs(row):
    return(row['HDD']+" "+row['SSD']+" "+row['RAM']+" "+row['Processor']+" "+row['Weight']+" "+row['Price'])

#a function to get the Name from Index
def get_name_from_index(index):
    return df[df.Index==index]['Name'].values[0]

#a function to get the Index from Name
def get_index_from_name(name):
    return df[df.Name==name]['Index'].values[0]

#applly the function to each row in the dataframe to store the combined strings into a new column called combimed_specs
df['combined_specs']=df.apply(combined_specs,axis=1)

#convert a collection of data into count matrix
count_matrix=CountVectorizer()
count_matrix=count_matrix.fit_transform(df['combined_specs'])

#convert a the count matrix into cosine similarity matrix
cosine_sim_mat=cosine_similarity(count_matrix)

#Get the most sold laptop or most popular laptop
laptop_popular='HP pavillion 15-CS208 2TX'

#Find laptop index of popular laptop
laptop_index=get_index_from_name(laptop_popular)

#Enumerating through all the similarity scores of laptop_popular
#making a ordered pair of laptop index and similarity scores
#and returning a list of such ordered pairs in the form of (laptop_index,similarity_scores)
similar_laptops=list(enumerate(cosine_sim_mat[laptop_index]))

#Sort similar_laptops in descending order of similarity scores and exclude the similar laptop itself
sorted_similar_laptops=sorted(similar_laptops,key=lambda x:x[1],reverse=True)[1:]

#A loop to print the first 5 entries from the sorted_similar_laptops list
i=0
print("The top 10 recommended laptops similar to "+laptop_popular+" are:")
for element in sorted_similar_laptops:
        if i < 10:
            print(element[0],get_name_from_index(element[0]))
            i+=1




