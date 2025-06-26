import random
import time
from .models import Answer, Question
import sympy
import logging
logger = logging.getLogger(__name__)

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
        _, _, expr = question_text.partition('calculate')
        expr = expr.strip()
        expr = expr.replace('x', '*').replace('X', '*').replace('÷', '/')
        try:
            result = sympy.sympify(expr).evalf()
            logger.info(f"expr: {expr}, result: {result}, type: {type(result)}")
            try:
                result_float = float(result)
                if result_float.is_integer():
                    logger.info(f"Returning integer: {result_float}")
                    return str(int(result_float))
                else:
                    rounded = round(result_float, 5)
                    logger.info(f"Returning rounded: {rounded}")
                    return str(rounded).rstrip('0').rstrip('.')
            except Exception as e:
                logger.error(f"Float conversion failed: {e}, result: {result}")
                return str(result)
        except Exception as e:
            logger.error(f"Sympy evaluation failed: {e}, expr: {expr}")
            return "That isn't a maths question >:("
    answer = random.choice(possibleAnswers)
    if april_fools:
        answer = answer[::-1]
    return answer