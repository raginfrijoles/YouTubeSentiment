import math
import os
import googleapiclient.discovery
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def getcomments(video, maxComments):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    try:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAWTipNMfd8w9DtTV3Eb88OAKXeOQb7Hug"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            order="relevance",
            maxResults=maxComments,
            videoId=video
        )
        response = request.execute()
        commentList = []
        for comment in response["items"]:
            commentList.append(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        return commentList
    except:
        return None

def sentimentanalysis(comments):
    sentiment = SentimentIntensityAnalyzer()
    results = {"compoundAvg": 0, "comments": []}
    for comment in comments:

        score = sentiment.polarity_scores(comment)

        score["comment"] = comment
        neg = abs(score["neg"])
        pos = score["pos"]
        compound = score["compound"]
        negpos = neg + pos

        if negpos > 0:
            score["negpercent"] = round((neg/negpos)*100)
            score["pospercent"] = round(pos/negpos*100)
        else:
            score["negpercent"] = 0
            score["pospercent"] = 0

        if compound > 0:
            score["overall"] = "pos"
        elif compound < 0:
            score["overall"] = "neg"
        else:
            score["overall"] = "neu"

        results["compoundAvg"] += score["compound"]
        results["comments"].append(score)

    results["compoundAvg"] = results["compoundAvg"]/len(results["comments"])

    return results


