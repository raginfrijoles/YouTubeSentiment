from flask import Flask, request, render_template
from urllib.parse import urlparse
from urllib.parse import parse_qs
import ytcomment

app = Flask(__name__)

#add username, add about page

# Loads index template when user requests root
@app.route("/", methods=('POST', 'GET'))
def index():
    return render_template('index.html')

# Loads results template when user requests results
@app.route("/results/", methods=('POST', 'GET'))
def results():
    # Retrieves url variables from form
    url = request.args.get('ytURL')
    maxComments = request.args.get('maxComments')
    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)

    # Check if URL is a valid YouTube video "v" is the variable name of YouTube ids
    if "v" in captured_value and parsed_url.netloc == "www.youtube.com":
        # Create list of comments
        commentList = ytcomment.getcomments(captured_value["v"][0], maxComments)
        # Checks if comments are enabled
        if commentList:
            # Generates sentiment for each comment
            ytresults = ytcomment.sentimentanalysis(commentList)
            # Render results template and return comments and their scores
            return render_template('results.html', comments=ytresults["comments"], yturl=url, compoundAvg=ytresults["compoundAvg"], overall=ytresults["overallsentiment"], sentimentcolor=ytresults["sentimentcolor"])
        else:
            return render_template('results.html', error="No available comments. Please try another video.")
    else:
        return render_template('results.html', error="Not a valid Youtube video.")
