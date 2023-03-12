# Twitter-Scraping
Twitter Scraping using Python scripting, Data Collection, MongoDB, Streamlit

Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.

Approach: 
•	By using the “snscrape” Library, Scrape the twitter data from Twitter Reference
•	Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
•	Store each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 
eg:({“Scraped Word”            : “Elon Musk”,
        “Scraped Date”             :15-02-2023,
        “Scraped Data”             : [{1000  Scraped data from past 100 days }]})
•	Create a GUI using streamlit that should contain the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped. After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.

How it works:
First, the inputs like the Keyword/Hashtag, Start date, end date, number of tweets to be scraped should be collected from the user using Streamlit.
These inputs are then fed to TwitterSearchScraper and TwitterHashtagScraper, after which a dataframe is created to store the same, which we will download as CSV or JSON.
Using mongodb, a connection is established and the data is uploaded to a new collection in the database.
Then a sidebar is kept to display the collections uploaded in the database, which can be visible upon clicking on the collection.
