from flask import Flask, request, render_template, redirect, flash, json, abort, jsonify, make_response
# from random import choice, sample
import requests
# import json
import os

app = Flask(__name__)


# We will use os.environ to get at the secret URL as an environmental variable
#
# Note: you must run `source secrets.sh` before running this file
# to make sure these environmental variables are set.

#######################################################################

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>welcome</body></html>'
    return html


@app.route('/api/1/send_messages', methods=['POST'])
def send_messages():
    if not request.json:
        abort(400)

    url = 'https://hooks.slack.com/services/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'

    # Send a JSONified version of your payload to the URL Slack provides
    r = requests.post(url, data=json.dumps(request.json))
    status_code = r.status_code

    # Check the status code of the respond you receive from Slack.
    #  If it's an error, flash a message about it at the bottom of the page.
    if status_code == 200:
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})


@app.route('/api/1/test')
def index():
    main_text = 'Test'

    # Build the JSON to send
    payload = {
        'text': main_text,
        # 'attachments' : [
        #     {
        # "color" :
        #     },
        # ]
    }
    # Your secret URL sourced in from secrets.sh
    # url = os.environ['WEBHOOK_URL']
    url = 'https://hooks.slack.com/services/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'

    # Send a JSONified version of your payload to the URL Slack provides
    r = requests.post(url, data=json.dumps(payload))
    status_code = r.status_code

    # Check the status code of the respond you receive from Slack.
    #  If it's an error, flash a message about it at the bottom of the page.
    if status_code == 200:
        flash('You did it!')
        return redirect("/")
    else:
        flash('Oh no, something went wrong. You are getting a %s  status code error.' % (status_code))

    return redirect("/")


#######################################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

