import random
import time
from .models import Answer, Question

testForAprilFools = False

if testForAprilFools or time.strftime("%m-%d") == "04-01":
     april_fools = True
else:
        april_fools = False

possibleAnswers = [
      "Yes",
      "No",
      "Maybe",
      "I don't know",
      "I don't care",
      "I don't want to answer that",
      "Why would I know that?",
      "I don't know, ask Google",
      "I don't know, ask Bing",
      "I don't know, ask DuckDuckGo",
      "I don't know, ask Yahoo",
      "I don't know, ask Ask Jeeves",
      "I don't know, ask AltaVista",
]

def handle_question():
    answer = random.choice(possibleAnswers)
    if april_fools:
          answer = answer[::-1]
    return answer