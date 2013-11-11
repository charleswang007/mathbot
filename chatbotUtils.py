# Natural Language Toolkit: Chatbot Utilities
#
# Copyright (C) 2001-2013 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <jez@jezuk.co.uk>.
from __future__ import print_function
from __future__ import division
from collections import defaultdict
from random import randint
from math import *

import string
import re
import random
#from nltk import compat
blWrong = False
reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

count_dict = {
    "intro" : 0,
    "extra" : 0,
    "definition" : 0,
    "arithmetic" : 0,
    "statistics" : 0,
    "qna" : 0
}

question_dict = {
    "intro" : [],
    "extra" : [],
    "definition" : [],
    "arithmetic" : [],
    "statistics" : [],
    "qna" : []
}
count_repeat_dict = defaultdict(int)
number_dict = {
    "one" : "1",
    "two" : "2",
    "three" : "3",
    "four" : "4",
    "five" : "5",
    "six" : "6",
    "seven" : "7",
    "eight" : "8",
    "nine" : "9",
    "ten" : "10",
}

class Chat(object):
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        @type pairs: C{list} of C{pairs}
        @param pairs: The patterns and responses
        @type reflections: C{dict}
        @param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE),y,z,w) for (x,y,z,w) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len,
                reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape,
            sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def respond(self, str):
            """
            Generate a response to the user input.

            :type str: str
            :param str: The string to be mapped
            :rtype: str
            """
            # check each pattern
            # add response_type

            ''' show alert if number of questions of certain type exceeds pre-defined values '''
            def questionAlert(resp_type):    
                if count_dict[response_type] > 5 and response_type!="qna":
                    resp = ("You have been asking questions of "+ response_type.title() + " type over five times! Can you ask me something else such as: ")
                    for type_name in count_dict.keys():
                        if type_name != response_type and response_type!="qna":
                            resp += type_name.upper() + ", "
                    resp = resp[0:-2] + " ???"
                else:
                    resp = None
                return resp
            
            def reverseQnA(sub_type):
                if sub_type == "q1-question":
                    resp = "What is the addition of 2 and 9? Answer the question in this format --> q1-sol = your_answer"
                elif sub_type == "q2-question":
                    resp = "What is the addition of 15 and 19? Answer the question in this format --> q2-sol = your_answer"
                elif sub_type == "q3-question":
                    resp = "What is 42 plus 28? Answer the question in this format --> q3-sol = your_answer"
                elif sub_type == "q4-question":
                    resp = "What is  98 plus 67? Answer the question in this format --> q4-sol = your_answer"
                elif sub_type == "q5-question":
                    resp = "What is 2 subtracted from 9? Answer the question in this format --> q5-sol = your_answer"
                elif sub_type == "q6-question":
                    resp = "What is 15 subtracted from 19? Answer the question in this format --> q6-sol = your_answer"
                elif sub_type == "q7-question":
                    resp = "What is 42 minus 28? Answer the question in this format --> q7-sol = your_answer"
                elif sub_type == "q8-question":
                    resp = "What is 98 minus 67? Answer the question in this format --> q8-sol = your_answer"    
                
                return resp
            
            for (pattern, response, response_type, sub_type) in self._pairs:
                match = pattern.match(str)
                resp = ""
                # did the pattern match?
                if match:
                    if str == "quit":
                        resp = "Good Bye!"
                        pass
                    elif response_type == "intro" or response_type == "extra" or response_type == "definition":
                        resp = random.choice(response)    # pick a random response
                        resp = self._wildcards(resp, match) # process wildcards
                        # fix munged punctuation at the end
                        if resp[-2:] == '?.': resp = resp[:-2] + '.'
                        if resp[-2:] == '??': resp = resp[:-2] + '?'
                        count_dict[response_type] += 1
                        question_dict[response_type].append(match.group(0))
                    
                    elif response_type == "arithmetic":
                        count_dict[response_type] += 1
                        question_dict[response_type].append(match.group(0))
                        strEval = 0
                        
                        if sub_type == "addition":
                            strEval = float(match.group(1)) + float(match.group(2))
                            lenstrA = len(match.group(1))
                            lenstrB = len(match.group(2))
                            if(lenstrA <=3 and lenstrB <=3):
                                count_repeat_dict['add'] += 1
                            resp = ("The sum of " + match.group(1) + " and " + match.group(2) + " is: ") + repr(strEval)

                        elif sub_type == "subtraction":
                            strEval = float(match.group(1)) - float(match.group(2))
                            lenstrA = len(match.group(1))
                            lenstrB = len(match.group(2))
                            if(lenstrA <=3 and lenstrB <=3):
                                count_repeat_dict['sub'] += 1
                            resp = ("The subtraction of " + match.group(1) + " from " + match.group(2) + " is: ") + repr(strEval)

                        elif sub_type == "multiplication":
                            strEval = float(match.group(1)) * float(match.group(2))
                            resp = ("The multiplication of " + match.group(1) + " and " + match.group(2) + " is: ") + repr(strEval)

                        elif sub_type == "division":
                            strEval = float(match.group(1)) / float(match.group(2))
                            resp = ("The division of " + match.group(1) + " by " + match.group(2) + " is: ") + repr(strEval)
                        
                        elif sub_type == "exponentiation":
                            strEval = float(match.group(1)) ** float(match.group(2))
                            resp = (match.group(1) + " to the power of "+  match.group(2) + " is: ") + repr(strEval)

                        elif sub_type == "addition-1":
                            strEval = float(match.group(2)) + float(match.group(3))
                            lenstrA = len(match.group(2))
                            lenstrB = len(match.group(3))
                            if(lenstrA <=3 and lenstrB <=3):
                                count_repeat_dict['add'] += 1
                            resp = ("The sum of " + match.group(2) + " and " + match.group(3) + " is: ") + repr(strEval)

                        elif sub_type == "subtraction-1":
                            strEval = float(match.group(2)) - float(match.group(3))
                            lenstrA = len(match.group(2))
                            lenstrB = len(match.group(3))
                            if(lenstrA <=3 and lenstrB <=3):
                                count_repeat_dict['sub'] += 1
                            resp = ("The subtraction of " + match.group(2) + " from " + match.group(3) + " is: ") + repr(strEval)
                        
                        elif sub_type == "multiplication-1":
                            strEval = float(match.group(2)) * float(match.group(3))
                            resp = ("The multiplication of " + match.group(2) + " and " + match.group(3) + " is: ") + repr(strEval)

                        elif sub_type == "division-1":
                            strEval = float(match.group(2)) / float(match.group(3))
                            resp = ("The division of " + match.group(2) + " by " + match.group(3) + " is: ") + repr(strEval)
                        
                        elif sub_type == "exponentiation-1":
                            strEval = float(match.group(2)) ** float(match.group(3))
                            resp = (match.group(2) + " to the power of "+  match.group(3) + " is: ") + repr(strEval)
                    
                    elif response_type == "statistics":
                        count_dict[response_type] += 1
                        question_dict[response_type].append(match.group(0))
                        
                        if sub_type == "mean" or sub_type == "average":
                            strMean = match.group(2)
                            strMean = strMean.replace(",", " ")
                            splitMean = strMean.split(" ")
                            lsMean = []
                            for item in splitMean:
                                if(item != ""):
                                    flNum = float(item)
                                    lsMean += [flNum]
                            flMean = sum(lsMean) / len(lsMean)
                            resp = ("The mean/average of " + match.group(2) + " is: " + repr(flMean))
                        
                        if sub_type == "median":
                            strMedian = match.group(2)
                            strMedian = strMedian.replace(",", " ")
                            splitMedian = strMedian.split(" ")
                            lsMedian = []
                            for item in splitMedian:
                                if(item !=""):
                                    flNum = float(item)
                                    lsMedian += [flNum]
                            lsMedian.sort()
                            lenMedian = len(lsMedian)
                            if(lenMedian % 2 == 0):
                                index_1 = lenMedian // 2 - 1
                                index_2 = index_1 + 1
                                flMedian = (lsMedian[index_1] + lsMedian[index_2]) / 2
                            else:
                                index = lenMedian // 2
                                flMedian = lsMedian[index]
                            resp = ("The median of " + match.group(2) + " is: " + repr(flMedian))
                        
                        if sub_type == "mode":
                            strMode = match.group(2)
                            strMode = strMode.replace(",", " ")
                            splitMode = strMode.split(" ")
                            dictMode = defaultdict(int)
                            for item in splitMode:
                                dictMode[item] += 1
                            strMaxMode = max(dictMode.iterkeys(), key=(lambda key: dictMode[key]))
                            resp = ("The mode of " + match.group(2) + " is: " + strMaxMode)
                        
                        if sub_type == "sd":
                            strSd = match.group(2)
                            strSd = strSd.replace(",", " ")
                            splitSd = strSd.split(" ")
                            lsSd = []
                            for item in splitSd:
                                if(item != ""):
                                    flNum = float(item)
                                    lsSd += [flNum]
                            flMean = sum(lsSd) / len(lsSd)
                            flsumSd = 0
                            for item in lsSd:
                                flsumSd += (item - flMean) ** 2
                            flSd = (1 / (len(lsSd)-1) * flsumSd) ** (1/2)
                            resp = ("The standard deviation (sd) of " + match.group(2) + " is: " + repr(flSd))
                    
                    elif response_type == "qna":
                        count_dict[response_type] += 1
                        question_dict[response_type].append(match.group(0))
                        strAns = match.group(2)
                        
                        if sub_type == "q1-answer":
                            if(strAns == "11"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q2-answer":
                            if(strAns == "34"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q3-answer":
                            if(strAns == "70"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                                            
                        elif sub_type == "q4-answer":
                            if(strAns == "165"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q5-answer":
                            if(strAns == "7"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q6-answer":
                            if(strAns == "4"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q7-answer":
                            if(strAns == "14"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                        
                        elif sub_type == "q8-answer":
                            if(strAns == "31"):
                                resp = ("Great! Your answer is correct! Let's continue ~")
                            else:
                                resp = ("Your answer is incorrect. Please do more math before asking me, bye ~")
                                count_dict[response_type] += 999999
                    
                    if count_repeat_dict['add'] >= 3:
                        ques_list = ["q1-question", "q2-question", "q3-question", "q4-question"]
                        index = randint(0,3)
                        print ("You have asked me too many simple questions on addition! You should brush up your skills before asking me!")
                        print ("Now, I am going to check if you understand basic addition!")
                        count_repeat_dict['add'] = 0
                        resp = reverseQnA(ques_list[index])
                    
                    elif count_repeat_dict['sub'] >= 3:
                        ques_list = ["q5-question", "q6-question", "q7-question", "q8-question"]
                        index = randint(0,3)
                        print ("You have asked me too many simple questions on subtraction! You should brush up your skills before asking me!")
                        print ("Now, I am going to check if you understand basic subtraction!")
                        count_repeat_dict['sub'] = 0
                        resp = reverseQnA(ques_list[index])
                        
                    elif questionAlert(response_type) != None:
                        resp = questionAlert(response_type)

                    ''' for debug purpose '''
                    '''
                    for key in question_dict.keys():
                        print(key, question_dict[key])
                    '''
                    
                    return resp

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        input = ""
        while input != quit:
            input = quit
            try: input = raw_input(">")
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                
                total_count = 1
                for key in count_dict.keys():
                    total_count = total_count + count_dict[key]
                if(total_count>=999999):
                    print("Sorry, I can't answer you more questions now.")
                    print("Practise more math and I hope you do better next time! Good luck!")
                    input = quit
                    print("===== Summary of Our Q&A Session =====")
                    print("| TYPE | QUESTIONS |")
                    print("--------------------")
                    for key in question_dict.keys():
                        print("|", key.title(), "|", question_dict[key], "|")
                    break
                if total_count > 10:
                    print("You've asked more than 10 questions. I'm tired. Our session has ended today.")
                    input = quit
                    print("===== Summary of Our Q&A Session =====")
                    print("| TYPE | QUESTIONS |")
                    print("--------------------")
                    for key in question_dict.keys():
                        print("|", key.title(), "|", question_dict[key], "|")
                    break
                def replace_all(text, dic):
                    for i, j in dic.iteritems():
                        text = text.replace(i, j)
                    return text
                input = replace_all(input, number_dict)
                print(self.respond(input))
