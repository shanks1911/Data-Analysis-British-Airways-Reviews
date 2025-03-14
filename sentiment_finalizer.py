def sentiment_name(sentiment_scores):
    sentiment_name = []    
    
    for i in range(len(sentiment_scores)):
        score_1 = sentiment_scores[i][0]
        score_2 = sentiment_scores[i][1]
        score_3 = sentiment_scores[i][2]

        if max(score_1,score_2,score_3) == score_1:
            sentiment_name.append("Negative")
        elif max(score_1,score_2,score_3) == score_2:
            sentiment_name.append("Neutal")
        elif max(score_1,score_2,score_3) == score_3:
            sentiment_name.append("Positive")
    
    return sentiment_name