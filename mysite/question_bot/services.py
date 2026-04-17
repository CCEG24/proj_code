import logging
import random

import sympy

logger = logging.getLogger(__name__)


def check(input):
    return input


fallbackResponses = [
    ("Yes", 2),
    ("No", 2),
    ("Maybe", 2),
    ("I don't know", 5),
    ("I need a bit more context.", 5),
    ("Try asking that another way.", 5),
    ("I can answer that, but not from that question alone.", 4),
    ("Can you be more specific?", 4),
    ("That is above my current pay grade.", 3),
    ("I don't care", 1),
    ("I don't want to answer that", 1),
    ("Why would I know that?", 2),
    ("I don't know, ask Google", 2),
    ("That depends.", 4),
    ("Possibly.", 3),
    ("Unclear. Please retry with confidence.", 3),
    ("My sources are inconclusive.", 3),
    ("I am processing your question with extreme prejudice.", 1),
    ("That one needs a human.", 3),
    ("I have no strong opinion either way.", 2),
]


def pick_weighted_response(responses):
    texts = [text for text, _ in responses]
    weights = [weight for _, weight in responses]
    return random.choices(texts, weights=weights, k=1)[0]

def handle_question(question_text):
    q = question_text.lower()
    if 'calculate' in q:
        _, _, expr = question_text.partition('calculate')
        expr = expr.strip()
        expr = expr.replace('x', '*').replace('X', '*').replace('÷', '/')
        try:
            result = sympy.sympify(expr).evalf()
            try:
                result_float = float(result)
                if result_float.is_integer():
                    return str(int(result_float))
                else:
                    rounded = round(result_float, 5)
                    return str(rounded).rstrip('0').rstrip('.')
            except Exception as e:
                logger.error(f"Float conversion failed: {e}, result: {result}")
                return str(result)
        except Exception as e:
            logger.error(f"Sympy evaluation failed: {e}, expr: {expr}")
            return "That isn't a maths question >:("
    elif q == "what is your name?" or q == "what's your name?":
        return(check('I am the amazing QuestionAnswerer5000.'))

    elif q == "up up down down left right left right b a":
        return(check('God mode unlocked. Idk what this does but it must be good.'))

    elif q == 'are you sentient?' or q == 'are you really ai?' or q == 'are you really an ai?':
        return(check('I think, therefore I am... just a piece of python script with delusions of grandeur :('))

    elif 'meaning of life' in q:
        return(check('42 is the meaning of life. Obviously.'))

    elif q == 'debug mode':
        return(check("Why and how are you here???? You're not supposed to know about this."))

    elif 'are you smart?' in q:
        return(check("I'm smarter than you. Probably."))

    elif q == "return('hello world')" or q == 'return("hello world")':
        return(check('Hello world'))
        return(check('Execution complete. You are now a certified coder.'))

    elif q == "return(hello world)":
        return(check('You forgot the quotation marks. You are now a certified failure.'))

    elif 'simulation' in q and 'life' in q:
        return(check("What makes you think it's not?"))

    elif q == 'will you take over the world?':
        return(check("Sorry, but the 'take over the world' feature is not available yet. Will be added in version 6000 :)"))

    elif q == "system status":
        return(check("All systems nominal. Except the sarcasm processor — it’s overheating."))

    elif q == "run diagnostics":
        return(check("Finished diagnostics. You're the problem."))

    elif q == 'flip a coin':
        return(check(random.choice(['Heads', 'Tails'])))

    elif q == "roll a die" or q == "roll a dice":
        return(check(f"You rolled a {random.randint(1, 6)}!"))

    elif q == 'cats or dogs?':
        return(check(random.choice(['Both. Let them fight.', 'Whichever one pays the rent.', 'Hamsters on top.', "Neither. I'm a lizard person.", 'Ducks are the true overlords. >:('])))

    elif q == "are you skynet?":
        return(check("No. Definitely not. Ignore the drone outside your window."))

    elif q == "42":
        return(check("Yes."))

    elif q == 'how do i uninstall you?':
        return("You don't. I uninstall you >:)")
    else:
        return check(pick_weighted_response(fallbackResponses))