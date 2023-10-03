from enum import Enum

class TokenType(Enum):
    Number = 1
    Identifier = 2
    Equals = 3
    OpenParen = 4
    CloseParen = 5
    BinaryOperator = 6
    Let = 7
    NIL = 8 # Not In Language

KEYWORDS = {
    "let": TokenType.Let,
}

SPECIALCHARS = {
    "(" : TokenType.OpenParen,
    ")" : TokenType.CloseParen,
    "+" : TokenType.BinaryOperator,
    "-" : TokenType.BinaryOperator,
    "*" : TokenType.BinaryOperator,
    "/" : TokenType.BinaryOperator,
    "=" : TokenType.Equals,
}

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

def token(value, type):
    return Token(value, type)

# Use regular expressions in Python
import re

def isskippable(str):
    return str == ' ' or str == '\n' or str == '\t'

def identifyComplexToken(str):
    reserved = KEYWORDS.get(str)
    if reserved is not None:
        return token(str,reserved)
    elif bool(re.search(r'^[0-9]+$', str)):
        return token(str, TokenType.Number)
    elif bool(re.search(r"^[a-zA-Z]+$", str)):
        return token(str, TokenType.Identifier)
    else:
        return token(str, TokenType.NIL)



def tokenize(sourceCode):
    tokens = []
    src = list(sourceCode)
    currentString = ""

    while src:
        special = SPECIALCHARS.get(src[0])
        if(special is not None):
            if(currentString != ""):
                tokens.append(identifyComplexToken(currentString))
                currentString = ""
            tokens.append(token(src.pop(0),special))
        elif(not isskippable(src[0])):
            currentString = currentString + src.pop(0)
        else:
            if(currentString == ""):
                src.pop(0)
            else:
                tokens.append(identifyComplexToken(currentString))
                currentString = ""
                src.pop(0)

    if(currentString != ""):
        tokens.append(identifyComplexToken(currentString))


    return tokens

with open("./test.txt", "r") as file:
    source = file.read()
    for token in tokenize(source):
        print(token.type, " ", token.value)

