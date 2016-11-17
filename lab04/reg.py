import re

class RegexMetaclass(type):
    def __new__(cls, name, bases, dct):
        attr = dict((key, re.compile(value) if key == "regex" else value) for key, value in dct.items())
        return super().__new__(cls, name, bases, attr)

class Regex(metaclass = RegexMetaclass):
    regex = "abc*3+2"
#    def __init__(self, regex):
#        self.regex = regex
