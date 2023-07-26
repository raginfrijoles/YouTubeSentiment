import os
import googleapiclient.discovery
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function that retrieves comments from a YouTube video id. Returns between 10 to all comments.
def getcomments(video, maxcomments, nextPage=""):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    try:
        # Create standard YouTube API request for commentThread().list()
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAWTipNMfd8w9DtTV3Eb88OAKXeOQb7Hug"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            order="relevance",
            maxResults=maxcomments,
            videoId=video,
            pageToken=nextPage
        )

        response = request.execute()

        # Create placeholder to store all comments as list
        commentList = []

        # Iterate through response and add original text to commentList
        for comment in response["items"]:
            commentList.append(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"])

        # Iterate through every page of comments if user requested and a "next page" exists
        if int(maxcomments) > 100 and "nextPageToken" in response:
            # Recursively call getcomments while nextPageTokens exist
            nextpagecomments = getcomments(video, 1000, nextPage=response["nextPageToken"])
            # extend result of each recursive call to commentList
            commentList.extend(nextpagecomments)

        return commentList

    # Print exception to console when request fails and return None
    except Exception as e:
        print(e)
        return None


def sentimentanalysis(comments):
    # Create Vader sentiment analyzer
    sentiment = SentimentIntensityAnalyzer()

    # Create dictionary to store comments and analysis
    results = {"compoundAvg": 0, "comments": [], "overallsentiment": "Neutral", "sentimentcolor": "text-secondary"}

    # Iterate through each comment and assign scores
    for comment in comments:

        # Generate Vader score for current comment (creates a dictionary)
        score = sentiment.polarity_scores(comment)

        # Create keys for each vader score to be used for front-end
        score["comment"] = comment
        score["overall"] = "neu"

        # Create variables to simplify arithmetic
        neg = abs(score["neg"])
        pos = score["pos"]
        compound = score["compound"]
        negpos = neg + pos

        # Calculate and assign neg/pos percentages for each comment for front-end use
        if negpos > 0:
            score["negpercent"] = round((neg/negpos)*100)
            score["pospercent"] = round(pos/negpos*100)
        else:
            score["negpercent"] = 0
            score["pospercent"] = 0

        # Assign neg or pos for front-end use
        if compound > 0:
            score["overall"] = "pos"
        elif compound < 0:
            score["overall"] = "neg"

        # Add compound score to overall compound score
        results["compoundAvg"] += score["compound"]
        # Append comment dictionary to results
        results["comments"].append(score)

    # Calculate compound avg for all comments
    results["compoundAvg"] = round(results["compoundAvg"]/len(results["comments"]), 3)

    # Create keys for overall sentiment and color for front-end use
    if results["compoundAvg"] > 0:
        results["overallsentiment"] = "Positive"
        results["sentimentcolor"] = "text-success"
    elif results["compoundAvg"] < 0:
        results["overallsentiment"] = "Negative"
        results["sentimentcolor"] = "text-danger"

    return results


