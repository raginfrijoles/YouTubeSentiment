from flask import Flask, request, render_template
from urllib.parse import urlparse
from urllib.parse import parse_qs
import ytcomment

app = Flask(__name__)

#add username, add about page


@app.route("/", methods=('POST', 'GET'))
def index():
    return render_template('index.html')


@app.route("/results/", methods=('POST', 'GET'))
def results():
    url = request.args.get('ytURL')
    maxComments = request.args.get('maxComments')

    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)

    if "v" in captured_value:
        commentList = ytcomment.getcomments(captured_value["v"][0], maxComments)
        if commentList:
            ytresults = ytcomment.sentimentanalysis(commentList)
            return render_template('results.html', comments=ytresults["comments"], yturl=url)
        else:
            return render_template('results.html', error="No available comments. Please try another video.")
    else:
        return render_template('results.html', error="Not a valid Youtube video.")
