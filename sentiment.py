import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
plt.style.use('ggplot') # type: ignore
import nltk

# roberta model
# tranformer based model
from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification
from scipy.special import softmax # type: ignore

# softmax function is a mathematical fuction used to convert a vector of raw scores (logits) into probabilities.


def sentiment_score(reviews_arr):
    tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
    model = TFAutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

    sentiment_scores = []
    for review in reviews_arr:
        encoded_text = tokenizer(review, truncation=True, padding="max_length", max_length=512, return_tensors="tf")
        output = model(**encoded_text)
        scores = output[0][0].numpy()
        scores = softmax(scores)
        sentiment_scores.append(scores)
    return sentiment_scores