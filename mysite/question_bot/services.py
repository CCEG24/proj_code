import random
import time
from .models import Answer, Question
import sympy

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

def handle_question(question_text):
    if 'calculate' in question_text.lower():
        a, b, expr = question_text.partition('calculate')
        expr = expr.strip()
        try:
            result = sympy.sympify(expr).evalf()
            result_float = float(result)
            if result_float.is_integer():
                print("RAW expr:", repr(expr))
                return str(int(result_float))
            else:
                rounded = round(result_float, 5)
                print("RAW expr:", repr(expr))
                return str(rounded).rstrip('0').rstrip('.')
        except Exception:
            return "That isn't a maths question >:("
    answer = random.choice(possibleAnswers)
    if april_fools:
        answer = answer[::-1]
    return answer