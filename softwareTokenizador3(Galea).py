from enum import Enum
import re
from tabulate import tabulate

# Definición de Tabla Hash
class Node:
    def __init__(self, key, value): 
        self.key = key 
        self.value = value 
        self.next = None
  
class HashTable:
    def __init__(self, capacity): 
        self.capacity = capacity 
        self.size = 0
        self.table = [None] * capacity 
  
    def _hash(self, key):
        return hash(key) % self.capacity 
  
    def insert(self, key, value):
        index = self._hash(key) 
  
        if self.table[index] is None: 
            self.table[index] = Node(key, value) 
            self.size += 1
        else: 
            current = self.table[index] 
            while current: 
                if current.key == key: 
                    current.value = value 
                    return
                current = current.next
            new_node = Node(key, value) 
            new_node.next = self.table[index] 
            self.table[index] = new_node 
            self.size += 1
  
    def search(self, key):
        index = self._hash(key) 
  
        current = self.table[index] 
        while current: 
            if current.key == key: 
                return current.value 
            current = current.next
  
        raise KeyError(key) 
  
    def remove(self, key):
        index = self._hash(key) 
  
        previous = None
        current = self.table[index] 
  
        while current: 
            if current.key == key: 
                if previous: 
                    previous.next = current.next
                else: 
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current 
            current = current.next
  
        raise KeyError(key) 
  
    def __len__(self):
        return self.size 
  
    def __contains__(self, key):
        try: 
            self.search(key) 
            return True
        except KeyError: 
            return False
        
    def printProperties(self):
        print("Length: " + str(self.size))
      
# Definición de los tipos de tokens usando una enumeración
class TokenType(Enum):
    Identifier = 1
    Keyword = 2
    Operator = 3
    Constant = 4
    String = 5
    BlockStart = 6
    BlockEnd = 7
    Comment = 8
    EndOfStatement = 9
    OpenParen = 10
    CloseParen = 11
    BinaryOperator = 12
    Equals = 13

# Palabras clave y caracteres especiales junto con su tipo correspondiente
KEYWORDS = {
    "int": TokenType.Keyword,
    "float": TokenType.Keyword,
    "char": TokenType.Keyword,
    "if": TokenType.Keyword,
    "else": TokenType.Keyword,
    "while": TokenType.Keyword,
    "for": TokenType.Keyword,
    "return": TokenType.Keyword,
    "switch": TokenType.Keyword,
    "case": TokenType.Keyword,
    "break": TokenType.Keyword,
    "continue": TokenType.Keyword,
    "default": TokenType.Keyword,
}

SPECIALCHARS = {
    "{": TokenType.BlockStart,
    "}": TokenType.BlockEnd,
    ";": TokenType.EndOfStatement,
    "(": TokenType.OpenParen,
    ")": TokenType.CloseParen,
    "+": TokenType.BinaryOperator,
    "-": TokenType.BinaryOperator,
    "*": TokenType.BinaryOperator,
    "/": TokenType.BinaryOperator,
    "=": TokenType.Equals,
}

# Clase para representar un token
class Token:
    def __init__(self, value, type, scope):
        self.value = value
        self.type = type
        self.scope = scope


# Función para crear un objeto Token
def token(value, type, scope):
    return Token(value, type, scope)


# Función para determinar si un carácter es ignorado (espacio, tabulación, salto de línea)
def isskippable(char):
    return char == " " or char == "\n" or char == "\t"


# Función para identificar un token complejo (puede ser una palabra reservada, constante, cadena o identificador)
def identifyComplexToken(token_str):
    reserved = KEYWORDS.get(token_str)
    if reserved is not None:
        return token(token_str, reserved)
    elif bool(re.match(r"^[0-9]+(\.[0-9]+)?$", token_str)):
        return token(token_str, TokenType.Constant)
    elif bool(re.match(r'^"[^"]*"$', token_str)):
        return token(token_str, TokenType.String)
    elif bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", token_str)):
        return token(token_str, TokenType.Identifier)
    else:
        return token(token_str, None)  # Token no válido


# Función para tokenizar el código
def tokenize(source_code):
    tokens = []
    currentScope = 0
    src = list(source_code)
    current_token_str = ""

    in_multiline_comment = False
    in_string = False


    while src:
        if in_multiline_comment:
            if src[0:2] == ["*", "/"]:
                in_multiline_comment = False
                src.pop(0)  # Pop '*'
                src.pop(0)  # Pop '/'
            else:
                src.pop(0)  # Saltar caracteres dentro de un comentario multilinea
        elif in_string:
            current_token_str = current_token_str + src.pop(0)
            if src[0] == '"':
                in_string = False
                current_token_str = current_token_str + src.pop(
                    0
                )  # Incluir comillas de cierre
                tokens.append(token(current_token_str, TokenType.String, currentScope))
                current_token_str = ""
        else:
            special_char = SPECIALCHARS.get(src[0])
            if special_char is not None:
                if current_token_str != "":
                    tokens.append(identifyComplexToken(current_token_str))
                    current_token_str = ""
                if src[0] == "/":
                    if src[1] == "/":
                        # Comentario de una línea
                        current_token_str = current_token_str + src.pop(0)  # '/'
                        while src and src[0] != "\n":
                            current_token_str = current_token_str + src.pop(0)
                        tokens.append(token(current_token_str, TokenType.Comment))
                        current_token_str = ""
                        continue  # Continuar con el siguiente carácter
                    elif src[1] == "*":
                        # Comentario multilinea
                        in_multiline_comment = True
                        src.pop(0)  # Pop '/'
                        src.pop(0)  # Pop '*'
                        continue  # Continuar con el siguiente carácter
                elif src[0] == '"':
                    # Cadena
                    in_string = True
                    current_token_str = src.pop(0)  # Incluir comilla de apertura
                else:
                    tokens.append(token(src.pop(0), special_char))
            elif not isskippable(src[0]):
                current_token_str = current_token_str + src.pop(0)
            else:
                if current_token_str == "":
                    src.pop(0)
                else:
                    tokens.append(identifyComplexToken(current_token_str))
                    current_token_str = ""
                    src.pop(0)

    if current_token_str != "":
        tokens.append(identifyComplexToken(current_token_str))

    return tokens


# Función para imprimir los tokens en una tabla
def print_tokens(tokens):
    table_data = []
    for token in tokens:
        if token.type is not None:
            table_data.append([token.type.name, token.value])

    headers = ["Tipo de Token", "Valor"]
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))

# Función para imprimir tabla hash de datos
def print_tokens_hash_table(tokens):
    counter = 1
    table = HashTable(len(tokens))

    keys = []
    for i in range(0, len(tokens)):
        key = i + 1
        keys.append(str(key))
        table.insert(str(key), tokens[i])

    formattedData = []
    for key in keys:
        token = table.search(key)
        formattedData.append([key, token.type, token.value, 0])

    print("\nHashed symbols table")
    headers = ["Key", "Tipo de Token", "Valor", "Ámbito"]
    print(tabulate(formattedData, headers, tablefmt="fancy_grid"))


# Lee el código fuente desde un archivo
with open("test.cs", "r") as file:
    source_code = file.read()
    tokens = tokenize(source_code)
    print_tokens(tokens)
    print_tokens_hash_table(tokens)