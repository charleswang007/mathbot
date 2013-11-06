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

import string
import re
import random
#from nltk import compat
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

        self._pairs = [(re.compile(x, re.IGNORECASE),y,z) for (x,y,z) in pairs]
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
            for (pattern, response, response_type) in self._pairs:
                match = pattern.match(str)

                # did the pattern match?
                if match:
                    if response_type == "intro" or response_type == "extra" or response_type == "definition":
                        resp = random.choice(response)    # pick a random response
                        resp = self._wildcards(resp, match) # process wildcards
                        # fix munged punctuation at the end
                        if resp[-2:] == '?.': resp = resp[:-2] + '.'
                        if resp[-2:] == '??': resp = resp[:-2] + '?'
                    
                    if response_type == "addition":
                        strEval = match.group(2) + '+' + match.group(3)
                        resp = eval(strEval)
			print ("The sum of " + match.group(2) + " and " + match.group(3) + " is") 
			#resp = "The result is" + str(eval(strEval))
                    
                    if response_type == "subtraction":
                        strEval = match.group(2) + '-' + match.group(3)
			print ("The subtraction of " + match.group(3) + " from " + match.group(2) + " is")
                        resp = eval(strEval)
                    
                    if response_type == "multiplication":
                        strEval = match.group(2) + "*" + match.group(3)
			print("The multiplication of " + match.group(2) + " and " + match.group(3) + " is")
                        resp = eval(strEval)
                    
                    if response_type == "division":
                        strEval = match.group(2) + "/" + match.group(3)
			print ("The division of " + match.group(2) + " by " + match.group(3) + " is")
                        resp = eval(strEval)
                    
                    if response_type == "exponentiation":
                        strEval = match.group(2) + "**" + match.group(3)
			print (match.group(2) + " to the power of "+  match.group(3) + " is")
                        resp = eval(strEval)
                    
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
                    print(self.respond(input))
