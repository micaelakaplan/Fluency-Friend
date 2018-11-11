"""
Jamie Brandon
David Rubio Vallejo
ASR PA5
11/09/2018
"""

# ! /usr/bin/env python3
import os
import sys
from flask import Flask, request, jsonify, make_response
from GrammarChecker import GrammarChecker

app = Flask(__name__)

gc = GrammarChecker()


def get_intent(req):
    """Returns the intent name as defined in the DialogFlow app"""
    return req.get('queryResult').get('intent').get('displayName')


def get_utterance(req):
    return req.get('originalDetectionConfidence').get('payload').get('inputs')[0].get('rawInputs')[0].get('query')


def give_grammatical_utterance(intent):
    if intent ==
    pass


@app.route("/", methods=['POST'])
def manage_request():
    """Main method that determines how to proceed based on the kind of intent detected"""

    response = "You're in llc.py!"
    try:
        req = request.get_json(silent=True, force=True)
        print((req), file=sys.stdout)
        intent = get_intent(req)
        user_utterance = get_utterance(req)
        print("INTENT: ", intent, file=sys.stdout)
        print("USER UTT: ", user_utterance, file=sys.stdout)

        if gc.is_grammatical(user_utterance):
            response = handle_intent(intent) #todo
        else:
            response = give_grammatical_utterance(intent)

    except:  # in case something goes wrong, give a response to let the user know to try again
        response = "Hmm. Something went wrong. What would you like to do?"
    dct = {
          "fulfillmentText": response,
          "source": "example.com",
          "payload": {
            "google": {
              "richResponse": {
                "items": [
                  {
                    "simpleResponse": {
                      "textToSpeech": response
                    }
                  }
                ]
              }
            }
          }
        }
    return make_response(jsonify(dct))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", '8080')))