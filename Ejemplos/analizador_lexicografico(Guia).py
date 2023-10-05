
# Analizador lexicográfico de C++ v.14
import ply.lex as lex
from tabulate import tabulate

# Lista de tokens
tokens = (
    'IDENTIFIER',
    'KEYWORD',
    'ARITHMETIC_OPERATOR',
    'COMPARISON_OPERATOR',
    'LOGICAL_OPERATOR',
    'ASSIGNMENT_OPERATOR',
    'CONSTANT',
    'STRING',
    'BLOCK_START',
    'BLOCK_END',
    'COMMENT', 
    'END_OF_STATEMENT'
)

# Expresiones regulares para tokens
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_KEYWORD = r'main|int|float|char|string|if|else|while|for|return|switch|case|break|continue|default'
t_ARITHMETIC_OPERATOR = r'[+\-*/%]|(\+\+|--)'
t_COMPARISON_OPERATOR = r'==|!=|<|>|<=|>='
t_LOGICAL_OPERATOR = r'&&|\|\||!'
t_ASSIGNMENT_OPERATOR = r'='
t_CONSTANT = r'(\'[^\']\'|\d+(\.\d*)?)'
t_STRING = r'"[^"]*"'
t_BLOCK_START = r'\{'
t_BLOCK_END = r'\}'
t_END_OF_STATEMENT = r';' 

# Regla para comentarios de una línea
def t_COMMENT(t):
    r'//.*'
    pass

# Regla para comentarios de múltiples líneas
def t_COMMENT_MULTILINE(t):
    r'/\*.*?\*/'
    pass

# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = ' \t\n'

# Función para manejar errores
def t_error(t):
    # print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el analizador léxico
lexer = lex.lex()

symbol_table = {}

# Pila de ámbitos
scope_stack = [0]
def add_to_symbol_table(token, current_type, current_value=None):
    if token.type == 'IDENTIFIER':
        identifier = token.value
        if identifier not in symbol_table:
            symbol_table[identifier] = {
                'type': current_type,
                'value': current_value,
                'scope': scope_stack[-1]  # Asignar el ámbito actual
            }
        else:
            # Si el identificador ya existe, actualizar su tipo de dato si es necesario
            if current_type:
                symbol_table[identifier]['type'] = current_type
    elif token.type == 'CONSTANT':
        last_identifier = list(symbol_table.keys())[-1]
        symbol_table[last_identifier]['value'] = token.value
    elif token.type == 'STRING':
        last_identifier = list(symbol_table.keys())[-1]

        if symbol_table[last_identifier]['value'] is None:
            symbol_table[last_identifier]['value'] = token.value[1:-1]
        else:
            symbol_table[last_identifier]['value'] += token.value[1:-1]

# Tipo de dato actual
current_type = None
current_value = None

# Ejemplo de uso
input_text = """
int xdasda = 21;
int main() {
    int x = 5;
    string str = "Hello, world!";
    float y = 6;
    char letter = 'a';
    int p = 11;

    if (x > 0) {
        x = x - 1;
    } else {
        int a = 33;
        int last = 0;
        x = x + 1;
    }
    // Este es un comentario
    return 0;
}
"""

lexer.input(input_text)

# Lista para almacenar los tokens encontrados
tokens_found = []

for token in lexer:
    if token.type != 'COMMENT':
        if token.type == 'KEYWORD':
            current_type = token.value
        tokens_found.append((token.type, token.value))
        add_to_symbol_table(token, current_type)

        # Actualizar el ámbito al encontrar una apertura de bloque
        if token.type == 'BLOCK_START':
            scope_stack.append(scope_stack[-1] + 1)

        # Disminuir el ámbito al encontrar un cierre de bloque
        elif token.type == 'BLOCK_END':
            scope_stack.pop()

print("\nLISTADO DE ELEMENTOS LEXICOGRÁFICOS:")
# Lista para almacenar los tokens encontrados por tipo
tokens_by_type = {token_type: [] for token_type in tokens}
seen_tokens = set()

for token in tokens_found:
    token_type, token_value = token
    if token_type != 'COMMENT' and (token_type, token_value) not in seen_tokens:
        tokens_by_type[token_type].append(token_value)
        seen_tokens.add((token_type, token_value))

# Crear una lista de tuplas para la tabla
table_data = []
for token_type, token_values in tokens_by_type.items():
    values_str = ' '.join(token_values)
    token_count = len(token_values) 
    table_data.append((token_type, values_str, token_count))

# Imprimir la tabla de elementos léxicos
headers = ["Tipo de Token", "Valores", "Coincidencias"]
print(tabulate(table_data, headers, tablefmt="fancy_grid"))

# Mostrar la tabla de símbolos con tipo de dato, valor y ámbito
print("\nTABLA DE SÍMBOLOS:")
symbol_table_data = []
for identifier, data in symbol_table.items():
    symbol_table_data.append([identifier, data['type'], data['value'], data['scope']])

headers = ["Identificador", "Tipo de dato", "Valor", "Ámbito"]
print(tabulate(symbol_table_data, headers, tablefmt="fancy_grid"))