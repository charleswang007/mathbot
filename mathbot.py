# -*- coding: cp950 -*-
'''
Created on 11/4/2013

@Authors: Charles Wang, Alice Man

@Description: Code modified from dog_chat.py (Strout et al), the MathBot is not only trained to answer simple
number problems like addition, subtraction, multiplication, and division, but can solve questions related to
calculus, geometry, linear algebra or statistic.

@Reference ChatBot:
http://alice.pandorabots.com/
http://www.jabberwacky.com/
http://nlp-addiction.com/chatbot/mathbot/
'''
import chatbotUtils
from chatbotUtils import *
import nltk

reflections = {
    "am" : "are",
    "was" : "were"
    }

# definitions
''' from http://www.mathsisfun.com/algebra/definitions.html '''
dictionary = {'equation': 'An equation says that two things are equal.',
              'variable': 'A Variable is a symbol for a number we don\'t know yet. It is usually a letter like x or y.',
              'constant': 'A number on its own is called a Constant.',
              'coefficient': 'A Coefficient is a number used to multiply a variable (4x means 4 times x, so 4 is a coefficient)',
              'operator': 'An Operator is a symbol (such as +, etc) that represents an operation (ie you want to do something with the values).',
              'term': 'A Term is either a single number or a variable, or numbers and variables multiplied together.',
              'expression': 'An Expression is a group of terms (the terms are separated by + or - signs)',
              'exponent': 'The exponent (such as the 2 in x^2) says how many times to use the value in a multiplication.',
              'polynomial': 'Example of a Polynomial: 3x^2 + x - 2',
              }
definition_pairs = []
for term in dictionary.keys():
    def_tuple = tuple([dictionary[term]])
    definition_pairs.append((r"%s|(.*)what is %s" % (term,term), def_tuple, "definition", ""))
definition_pairs = tuple(definition_pairs)

# introduction
intro_pairs = (
    (
        r"math|(.*)what is math",
        (
            "A mathematician is a blind man in a dark room looking for a black cat which isn't there. (Charles Darwin)",
        ),
        "intro",
        ""
    ),
    (
        r"(.*)math",
        (
            "Did you just say Math? It is my favorite subject!",
            "Math makes me the sexist chatbot in the world!",
            "Please challenge me with any math questions. I'm hungry!"
        ) ,
        "intro",
        ""
    ),
)

# basic arithmetic 
arithmetic_pairs = (
    (
        r"(\d+\.*\d*)\s*plus\s*(\d+\.*\d*)", # addition(plus)
        (
            "[addition] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "addition"
    ),
    (
        r"(\d+\.*\d*)\s*\+\s*(\d+\.*\d*)", # addition(+)
        (
            "[addition] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "addition"
    ),
    (
        r"(\d+\.*\d*)\s*minus\s*(\d+\.*\d*)", # subtraction(minus)
        (
            "[subtraction] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "subtraction"
    ),
    (
        r"(\d+\.*\d*)\s*-\s*(\d+\.*\d*)", # subtraction(-)
        (
            "[subtraction] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "subtraction"
    ),
    (
        r"(\d+\.*\d*)\s*times\s*(\d+\.*\d*)", # multiplication(times)
        (
            "[multiplication] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "multiplication"
    ),
    (
        r"(\d+\.*\d*)\s*\*\s*(\d+\.*\d*)", # multiplication(*)
        (
            "[multiplication] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "multiplication"
    ),
    (
        r"(\d+\.*\d*)\s*divided by\s*(\d+\.*\d*)", # division(divided by)
        (
            "[division] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "division"
    ),
    (
        r"(\d+\.*\d*)\s*/\s*(\d+\.*\d*)", # division(/)
        (
            "[division] the two numbers are: %1 and%2, result is ...",
        ) ,
        "arithmetic",
        "division"
    ),
    (
        r"(\d+\.*\d*)\s*\*\*\s*(\d+\.*\d*)", # Exponentiation(**)
        (
            "[Exponentiation] the base is%1 and the exponent is%2, result is ...",
        ) ,
        "arithmetic",
        "exponentiation"
    ),
    (
        r"(\d+\.*\d*)\s*to the power of\s*(\d+\.*\d*)", # Exponentiation(to the power of)
        (
            "[Exponentiation] the base is%1 and the exponent is%2, result is ...",
        ) ,
        "arithmetic",
        "exponentiation"
    ),
)

# basic arithmetic (starting with verbal, e.g. what is 1 plus 2?)
arithmetic_pairs_1 = (
    (
        r"(.*)\s(\d+\.*\d*)\s*plus\s*(\d+\.*\d*)", # addition(plus)
        (
            "[addition] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "addition-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*\+\s*(\d+\.*\d*)", # addition(+)
        (
            "[addition] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "addition-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*minus\s*(\d+\.*\d*)", # subtraction(minus)
        (
            "[subtraction] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "subtraction-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*-\s*(\d+\.*\d*)", # subtraction(-)
        (
            "[subtraction] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "subtraction-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*times\s*(\d+\.*\d*)", # multiplication(times)
        (
            "[multiplication] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "multiplication-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*\*\s*(\d+\.*\d*)", # multiplication(*)
        (
            "[multiplication] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "multiplication-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*divided by\s*(\d+\.*\d*)", # division(divided by)
        (
            "[division] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "division-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*/\s*(\d+\.*\d*)", # division(/)
        (
            "[division] the two numbers are: %2 and%3, result is ...",
        ) ,
        "arithmetic",
        "division-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*\*\*\s*(\d+\.*\d*)", # Exponentiation(**)
        (
            "[Exponentiation] the base is%2 and the exponent is%3, result is ...",
        ) ,
        "arithmetic",
        "exponentiation-1"
    ),
    (
        r"(.*)\s(\d+\.*\d*)\s*to the power of\s*(\d+\.*\d*)", # Exponentiation(to the power of)
        (
            "[Exponentiation] the base is%2 and the exponent is%3, result is ...",
        ) ,
        "arithmetic",
        "exponentiation-1"
    ),
)

# anything else
extra_pairs = (
    (
        r'(.*)',
        (
            "(Looking sad) I want to talk about math...",
            "Please don't count on me answer this kind of question"
        ),
        "extra",        ""
    ),
)

pairs = intro_pairs + definition_pairs
pairs = pairs + arithmetic_pairs
pairs = pairs + arithmetic_pairs_1
pairs = pairs + extra_pairs
#print pairs

math_chatbot = chatbotUtils.Chat(pairs, reflections)

def math_chat():
    print "I'm a nerdy mathbot that only answers math questions ... Enter 'quit' to exit"
    math_chatbot.converse()

def demo():
    math_chat()

if __name__ == "__main__":
    demo()
