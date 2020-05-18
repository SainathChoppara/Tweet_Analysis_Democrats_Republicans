#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing all the required pacakages for performing the analysis. Wehereever possible we will name the packages as aliases.
import nltk
import tweepy
import json
import re
import pandas as pd
import numpy as np
from pprint import pprint 


# In[2]:


#for retrieving tweets from twitter we need to use API keys. Here, we are storing keys and password as local variables for accesing them whenever possible
user_key = 'NDftFMzyOVTqKZf4TkzpJAN8E'
user_secret = 'YuvOwUZ6dytuMk52mw7eqcPuSKdvkelaziWOo6w2W7kGcGdE9X'

#twitter provides with unique access for users which are know as tokens. These help in retrieving the tweets. We are storing Access Tokens as local variables for accessinng them whereever possible
user_auth_token = '1244759591365328896-5ghELsW3rwRfvPK90GtcQ3aeO23qGz'
user_auth_secret = 'gZXQVyHxjnHTeV9ao7ybiOAfNX2akBRulwzh3I9lRXNfB'

#initialising a variable which will authorize our access to twitter
auth = tweepy.OAuthHandler(user_key,user_secret)
#using the auth variable and token details we are authorizing our access to twitter  
auth.set_access_token(user_auth_token,user_auth_secret)
#initialising api variable which will act as a resuable function to call api as required
api = tweepy.API(auth)


# In[3]:


#creating a list of twitter usernames, who are popular in Republican party. This list will be used as a iterable list for retrieving the tweets of these politicians.
handles = ['realDonaldTrump', 'Mike_Pence','SecretaryCarson','tedcruz', 'sarahpalinusa','NikkiHaley']

#Added Empty dataframe to fill the details from JSON file requested from twitter web datasource
merged_republicans=pd.DataFrame()

#Added loop which will basically iterate through the handles list and append tweets for each of the user in the handles list
for handle in handles:
    #initialising a tweets variable which will consits of user_timeline function(). 
    #The out of this function is that it will return the 200 tweets of each user present in handles list. 
    tweets = api.user_timeline(screen_name=handle, count=200)
    #prints the number of JSON format tweets retried for each user in handles list
    print("Number of tweets extracted: {}.\n".format(len(tweets)))
    #initialising a data frame called 'data', where it will consist text part of the tweet retrieved using JSON format
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    #retrieving ID from JSON formatted tweet and storing it as a column in dataframe
    data['ID']   = np.array([tweet.id for tweet in tweets])
    #retrieving Date from JSON formatted tweet and storing it as a column in dataframe
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    #retrieving count of retweets from JSON formatted tweet and storing it as a column in dataframe
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    #created new column handle to identify the source of tweet.
    data.loc[:,'Handle']=handle
    #adding an extra column to identity the political affiliation of the politician
    data.loc[:,'Political_party'] = 'Republicans'
    #merging the data frames
    merged_republicans = pd.concat([merged_republicans,data])


# In[4]:


#creating a list of twitter usernames, who are popular in Democratic party. This list will be used as a iterable list for retrieving the tweets of these politicians.
handles = ['BernieSanders', 'JoeBiden','SpeakerPelosi','ewarren','KamalaHarris','HillaryClinton']

#Added Empty dataframe to fill the details from JSON file requested from twitter web datasource
merged_democrats =pd.DataFrame()

#Added loop which will basically iterate through the handles list and append tweets for each of the user in the handles list
for handle in handles:
    #initialising a tweets variable which will consits of user_timeline function(). 
    #The out of this function is that it will return the 200 tweets of each user present in handles list. 
    tweets = api.user_timeline(screen_name=handle, count=200)
    #prints the number of JSON format tweets retried for each user in handles list
    print("Number of tweets extracted: {}.\n".format(len(tweets)))
    #initialising a data frame called 'data', where it will consist text part of the tweet retrieved using JSON format
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    #retrieving ID from JSON formatted tweet and storing it as a column in dataframe    
    data['ID']   = np.array([tweet.id for tweet in tweets])
    #retrieving Date from JSON formatted tweet and storing it as a column in dataframe    
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    #retrieving count of retweets from JSON formatted tweet and storing it as a column in dataframe
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    #created new column handle to identify the source of tweet.
    data.loc[:,'Handle']=handle
    #adding an extra column to identity the political affiliation of the politician
    data.loc[:,'Political_party'] = 'Democrats'
    #merging the data frames
    merged_democrats =pd.concat([merged_democrats,data])


# In[5]:


#creating a uniform dataframe which will consist of both republicans and democrats
merged_dem_rep =pd.concat([merged_democrats, merged_republicans],sort=False)


# In[6]:


########### ANALYSIS 1 : We are interested in knowing what day of a week did republicans and democrats tweeted the most ?

#we are formatting the dataframe to include a new column, which consists of the day of week for each of the tweet made these politicians
merged_dem_rep['Date_WeekDay_Derived'] = merged_dem_rep["Date"].apply(lambda timestamp: timestamp.dayofweek)
#initialising a new variable, wherein we store the grouped data based on two columns of the dataframe and later bin the number of tweets made in each day of the week
tweets_day = merged_dem_rep.groupby(['Political_party','Date_WeekDay_Derived'],sort=False)['ID'].count()
#converting the grouped data into a dataframe for better visualisation
tweets_day = tweets_day.to_frame()
#sorting the data by Political_party, ID in decending order, so that we can see the highest tweeted day of week for both republicans and democrats
tweets_day = tweets_day.sort_values(['Political_party','ID'], ascending = (False))
#resetting the index
tweets_day = tweets_day.reset_index()
#as the Date_WeekDay_Derived column is in numeric format denote by 0 - monday ..... 6- sunday. So we have to replace them by week day names.
#in order for replace we have to convert the column into a string datatype
tweets_day['Date_WeekDay_Derived'] = tweets_day['Date_WeekDay_Derived'].apply(str)
#here we are replace by names of the week days such as monday, tuesday ....
tweets_day['Date_WeekDay_Derived'] = tweets_day['Date_WeekDay_Derived'].replace(['0','1','2','3','4','5','6'], ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
#displaying the result
print(tweets_day)
#it can be observed that, democrats tweeted most on thursday, wednesday and friday. However, republicans tweeted most on friday, thursday
#converting the output into excel
tweets_day.to_excel("C://Users//nehai//Downloads//IST_652_Mini_Project_2//analysis_1.xlsx")  


# In[7]:


########### ANALYSIS 2 : we are interested in the highest number of retweets a particular politician of republic or democratic party has recorded for his tweets or any f the corresponding retweets performed by him 

#we are using combined dataframe of both repulicans and democrats for this analysis.

#using merged_dem_rep dataframe, a groupby funciton is performed on 'Political_party','Handle' and later we summing the 'RTs' column for understanding estimating the who has got highest retweets from each of the party
retweets_dem_rep = merged_dem_rep.groupby(['Political_party','Handle'])['RTs'].sum()
#converting the grouped data into a dataframe for better visualisation
retweets_dem_rep = retweets_dem_rep.to_frame()
#sorting the grouped data by 'RTs' column for analysis purpose
retweets_dem_rep = retweets_dem_rep.sort_values(['RTs'], ascending = (False))
#resetting the index
retweets_dem_rep = retweets_dem_rep.reset_index()
#displaying the result
#it can observed from the output that Donald trump from Republic party and Hillary clinton from Democratic party have highest number of tweets
print(retweets_dem_rep)
#converting the output into excel
retweets_dem_rep.to_excel("C://Users//nehai//Downloads//IST_652_Mini_Project_2//analysis_2.xlsx")  


# In[8]:


##############Analysis 3 : We are interested to know the number times the words 'american or americans' was used in tweet by politicians from republic and democratic party.

#creating a list which will include text of all tweets made by democrats
text_dem = merged_democrats['Tweets'].tolist() 

#making the characters in the list into lower case letters and creating tokens of them
dem_tokens = [tok.lower() for tweet in text_dem for tok in nltk.word_tokenize(tweet)]

#initialising a variable which consists of all the stop letters in english 
nltk_stopwords = nltk.corpus.stopwords.words('english')

#iterating each token for the stop words and making a list of token which are not stopwords
dem_cleaned_tokens = [tok for tok in dem_tokens if not tok in nltk_stopwords]

#creating a function which will filter out all the non-alphabetical characers from the tokens
#defining a function called tweet_filter()
def tweet_filter(w):
    #the following pattern matches a word of non-alphabetical characters       
    pattern = re.compile('^[^a-z]+$')
    #using if else, we are iterating over the list to match for the parttern 
    if (pattern.match(w)):
        return True
    else:
        return False

#now iterating the token lis over the tweet_filter() for removing all the non-alphabetical characters
final_dem_token = [tok for tok in dem_cleaned_tokens if not tweet_filter(tok)]

#now we are creating a function which will iterate over the above token list to count the number of times the word 'american' or 'americans' was used.
#defining a function called tweet_america()
def tweet_america(x):
    pattern = re.compile('\W*(americans*)\W*')
    if (pattern.match(x)):
        return True
    else:
        return False
#now we are iterating our token list over tweet_america()
final_dem_token = [tok for tok in final_dem_token if tweet_america(tok)]

demo_freq = nltk.FreqDist(final_dem_token)

print('The democrats have referred americans in ',demo_freq)


# In[9]:


#creating a list which will include text of all tweets made by republicans
text_rep = merged_republicans['Tweets'].tolist() 

#making the characters in the list into lower case letters and creating tokens of them
rep_tokens = [tok.lower() for tweet in text_rep for tok in nltk.word_tokenize(tweet)]

#iterating each token for the stop words and making a list of token which are not stopwords
rep_cleaned_tokens = [tok for tok in rep_tokens if not tok in nltk_stopwords]

#now iterating the token lis over the tweet_filter() for removing all the non-alphabetical characters
final_rep_token = [tok for tok in rep_cleaned_tokens if not tweet_filter(tok)]

#now we are creating a function which will iterate over the above token list to count the number of times the word 'american' or 'americans' was used.
#defining a function called tweet_america()
final_rep_token = [tok for tok in final_rep_token if tweet_america(tok)]

rep_freq = nltk.FreqDist(final_rep_token)
print('The republicans have referred americans in ',rep_freq)

