# -*- coding: cp950 -*-
'''
Created on 11/4/2013

@Authors: Charles Wang, Alice Man

@Description: Code modified from dog_chat.py (Strout et al), the MathBot is not only trained to answer simple
number problems like addition, subtraction, multiplication, and division, but can solve questions related to
mathematical definitions, large number algebra operations, or statistics.

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
''' mainly from http://www.mathsisfun.com/algebra/definitions.html '''
dictionary = {'equation': 'An equation says that two things are equal.',
              'variable': 'A Variable is a symbol for a number we don\'t know yet. It is usually a letter like x or y.',
              'constant': 'A number on its own is called a Constant.',
              'coefficient': 'A Coefficient is a number used to multiply a variable (4x means 4 times x, so 4 is a coefficient)',
              'operator': 'An Operator is a symbol (such as +, etc) that represents an operation (ie you want to do something with the values).',
              'term': 'A Term is either a single number or a variable, or numbers and variables multiplied together.',
              'expression': 'An Expression is a group of terms (the terms are separated by + or - signs)',
              'exponent': 'The exponent (such as the 2 in x^2) says how many times to use the value in a multiplication.',
              'polynomial': 'Example of a Polynomial: 3x^2 + x - 2',
              'mean': 'The mean/average is obtained by dividing the sum of observed values by the number of observations.',
              'median': 'The median is the middle value of a set of data containing an odd number of values, or the average of the two middle values for even numbers of data.',
              'mode': 'The mode of a set of data is the value that occurs most frequently.',
              'standard deviation': 'The standard deviation gives an idea of how close the entire set of data is to the average value.'
              }

# defintion Q-A pairs
definition_pairs = []
for term in dictionary.keys():
    def_tuple = tuple([dictionary[term]])
    definition_pairs.append((r"%s|(.*)what is %s" % (term,term), def_tuple, "definition", ""))
definition_pairs = tuple(definition_pairs)

# introduction pairs
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

# basic statistics
statistics_pairs = (
    (
        r"(.*)\s*mean\sof\s([\d.,\s]+)", # mean
        (
            "The mean of , result is ...",
        ) ,
        "statistics",
        "mean"
    ),
    
    (
        r"(.*)\s*median\sof\s([\d.,\s]+)", # median
        (
            "The median of , result is ...",
        ) ,
        "statistics",
        "median"
    ),
    
    (
        r"(.*)\s*average\sof\s([\d.,\s]+)", # average
        (
            "The average of , result is ...",
        ) ,
        "statistics",
        "average"
    ),
    
    (
        r"(.*)\s*mode\sof\s([\d.,\s]+)", # mode
        (
            "The mede of , result is ...",
        ) ,
        "statistics",
        "mode"
    ),
    
    (
        r"(.*)\s*sd\sof\s([\d.,\s]+)", # sd
        (
            "The sd of , result is ...",
        ) ,
        "statistics",
        "sd"
    ),
    
    (
        r"(.*)\s*standard\sdeviation\sof\s([\d.,\s]+)", # standard deviation
        (
            "The standard deviation of , result is ...",
        ) ,
        "statistics",
        "sd"
    ),
)

# reverse Q&A
QnA_pairs = (

    (
        r"(q1-sol\s*=\s*)(\d+)",
        (
            "The answer of q1: 2 + 9 is 11"
        ),
        "qna",
        "q1-answer"
    ),
    
    (
        r"(q2-sol\s*=\s*)(\d+)",
        (
            "The answer of q2: 15 + 19 is 34"
        ),
        "qna",
        "q2-answer"
    ),
    
    (
        r"(q3-sol\s*=\s*)(\d+)",
        (
            "The answer of q3: 42 + 28 is 70"
        ),
        "qna",
        "q3-answer"
    ),
    
    (
        r"(q4-sol\s*=\s*)(\d+)",
        (
            "The answer of q4: 98 + 67 is 165"
        ),
        "qna",
        "q4-answer"
    ),
    
    (
        r"(q5-sol\s*=\s*)(\d+)",
        (
            "The answer of q5: 9 - 2 is 7"
        ),
        "qna",
        "q5-answer"
    ),
    
    (
        r"(q6-sol\s*=\s*)(\d+)",
        (
            "The answer of q6: 19 - 15 is 4"
        ),
        "qna",
        "q6-answer"
    ),
    
    (
        r"(q7-sol\s*=\s*)(\d+)",
        (
            "The answer of q7: 42 - 28 is 14"
        ),
        "qna",
        "q7-answer"
    ),
    
    (
        r"(q8-sol\s*=\s*)(\d+)",
        (
            "The answer of q8: 98 - 67 is 31"
        ),
        "qna",
        "q8-answer"
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
        "extra",
        ""
    ),
)

pairs = intro_pairs + definition_pairs
pairs = pairs + arithmetic_pairs
pairs = pairs + arithmetic_pairs_1
pairs = pairs + statistics_pairs
pairs = pairs + QnA_pairs
pairs = pairs + extra_pairs

math_chatbot = chatbotUtils.Chat(pairs, reflections)

def math_chat():
    print "I'm a nerdy mathbot that only answers math questions ... Enter 'quit' to exit"
    math_chatbot.converse()

def demo():
    math_chat()

if __name__ == "__main__":
    demo()
