import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo
import time

client = pymongo.MongoClient(
    "mongodb+srv://SaikatBiswas:1234@cluster0.t6iodjp.mongodb.net/?retryWrites=true&w=majority")
mydb = client["Twitter_Database"]
tweets_df = pd.DataFrame()
dfm = pd.DataFrame()
st.write("# Twitter Data Scraping")
option = st.selectbox('How would you want to search?', ('Keyword', 'Hashtag'))
word = st.text_input('Please enter a ' + option, 'Example: Elon Musk')
start = st.date_input("Select the Start Date", datetime.date(2022, 1, 1), key='d1')
end = st.date_input("Select the End Date", datetime.date(2023, 1, 1), key='d2')
tweet_c = st.slider('Count of tweets to scrape', 0, 1000, 5)
tweets_list = []
if word:
    if option == 'Keyword':
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i > tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount,
                                tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'Source', 'Url'])
    else:
        for i, tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i > tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount,
                                tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'Source', 'Url'])
else:
    st.warning(option, ' cant be empty', icon="⚠️")


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV", data=csv, file_name='Twitter_data.csv', mime='text/csv', )

    json_string = tweets_df.to_json(orient='records')
    st.download_button(label="Download data as JSON", file_name="Twitter_data.json", mime="application/json",
                       data=json_string, )

    if st.button('Upload Tweets to Database'):
        coll = word
        coll = coll.replace(' ', '_') + '_Tweets'
        mycoll = mydb[coll]
        dict = tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict)
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word + str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
            st.balloons()
        else:
            st.warning('Cant upload because there are no tweets', icon="⚠️")

    if st.button('Show Tweets'):
        st.write(tweets_df)

with st.sidebar:
    st.write('Uploaded Datasets: ')
    for i in mydb.list_collection_names():
        mycollection = mydb[i]
        st.write(i, mycollection.count_documents({}))
        if st.button(i):
            dfm = pd.DataFrame(list(mycollection.find()))
if not dfm.empty:
    st.write(len(dfm), 'Records Found')
    st.write(dfm)
