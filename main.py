import streamlit as st #type: ignore

from scraper import scrape_reviews
from sentiment import sentiment_score
from sentiment_finalizer import sentiment_name

st.title("Data Analysis of British Airways Reviews")
st.write("This app analyses British Airways reviews")

# scraping
st.write("Scraping data...")
df = scrape_reviews()
st.write("Data scraped successfully!")

# sentiment analysis
st.write("Performing sentiment analysis...")
sentiment_scores = sentiment_score(df["Reviews"].to_numpy())
st.write(sentiment_scores[:5])
st.write("Calulating final sentiments")
review_sentiment = sentiment_name(sentiment_scores)
st.write(review_sentiment[:5])
df["Sentiment"] = review_sentiment
df.to_csv("BA_reviews.csv", index=False)
st.write(df)
st.write("Sentiment Analysis DONE BABY LESGOOOOOOO !!!!!!!!!!")