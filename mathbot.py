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
              'operator': 'An Operator is a symbol (such as +, ×, etc) that represents an operation (ie you want to do something with the values).',
              'term': 'A Term is either a single number or a variable, or numbers and variables multiplied together.',
              'expression': 'An Expression is a group of terms (the terms are separated by + or - signs)',
              'exponent': 'The exponent (such as the 2 in x^2) says how many times to use the value in a multiplication.',
              'polynomial': 'Example of a Polynomial: 3x^2 + x - 2',
              }
definition_pairs = []
for term in dictionary.keys():
    def_tuple = tuple([dictionary[term]])
    definition_pairs.append((r"%s|(.*)what is %s" % (term,term), def_tuple))
definition_pairs = tuple(definition_pairs)

# introduction
intro_pairs = (
    (
        r"math|(.*)what is math",
        (
            "A mathematician is a blind man in a dark room looking for a black cat which isn't there. (Charles Darwin)",
        ) 
    ),
    (
        r"(.*)math",
        (
            "Did you just say Math? It is my favorite subject!",
            "Math makes me the sexist chatbot in the world!",
            "Please challenge me with any math questions. I'm hungry!"
        ) 
    ),
)

# basic arithmetic (not sure how to do operations on the numbers, since I don't know how to parse %0)
arithmetic_pairs = (
    (
        r"(.*)\s*(\d+)\s*plus\s*(\d+)", # addition(plus)
        (
            "[addition] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*\+\s*(\d+)", # addition(+)
        (
            "[addition] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*minus\s*(\d+)", # subtraction(minus)
        (
            "[subtraction] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*\-\s*(\d+)", # subtraction(-)
        (
            "[subtraction] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*times\s*(\d+)", # multiplication(times)
        (
            "[multiplication] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*\*\s*(\d+)", # multiplication(*)
        (
            "[multiplication] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*divided by\s*(\d+)", # division(divided by)
        (
            "[division] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*\/\s*(\d+)", # division(/)
        (
            "[division] the two numbers are: %2 and%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*\*\*\s*(\d+)", # Exponentiation(**)
        (
            "[Exponentiation] the base is%2 and the exponent is%3, result is ...",
        ) 
    ),
    (
        r"(.*)\s*(\d+)\s*to the power of\s*(\d+)", # Exponentiation(to the power of)
        (
            "[Exponentiation] the base is%2 and the exponent is%3, result is ...",
        ) 
    ),
)

# anything else
extra_pairs = (
    (
        r'(.*)',
        (
            "(Looking sad) I want to talk about math...",
            "Please don't count on me answer this kind of question"
        )
    ),
)

pairs = intro_pairs + definition_pairs
pairs = pairs + arithmetic_pairs
pairs = pairs + extra_pairs


math_chatbot = nltk.chat.Chat(pairs, reflections)

def math_chat():
    print "I'm a nerdy mathbot that only answers questions related to Math ..."
    math_chatbot.converse()

def demo():
    #print dictionary.keys()
    math_chat()

if __name__ == "__main__":
    demo()
