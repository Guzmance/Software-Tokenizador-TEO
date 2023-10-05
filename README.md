# Software-Tokenizador-TEO

Este es un analizador léxico simple para el lenguaje de programación C#. El objetivo de este analizador léxico es dividir el código fuente de C# en una secuencia de tokens, donde cada token tiene un tipo y un valor asociados. Esto es útil como paso inicial en el proceso de compilación o interpretación de código C#.

## Uso

1. Asegúrate de tener Python 3.x instalado en tu sistema.

2. Instala las dependencias necesarias ejecutando el siguiente comando:

   ```bash
   pip install tabulate
   ```

## Tipos de Tokens

El analizador léxico reconoce los siguientes tipos de tokens:

1. Identifier: Identificadores de variables y funciones.
2. Keyword: Palabras clave de C# como if, while, return, etc.
3. Operator: Operadores matemáticos y de comparación.
4. Constant: Constantes numéricas como enteros y flotantes.
5. String: Cadenas de texto.
6. BlockStart y BlockEnd: Inicio y fin de bloques de código (llaves { y }).
7. Comment: Comentarios de una línea (//) o comentarios multilineales (/\* \*/).
8. EndOfStatement: Fin de una declaración (punto y coma ;).
9. OpenParen y CloseParen: Paréntesis de apertura y cierre.
10. BinaryOperator: Operadores binarios como +, -, \*, /.
11. Equals: Operador de asignación (=).

## Resumen Código

Un analizador léxico es una parte esencial de un compilador o intérprete que se encarga de dividir el código fuente en una secuencia de "tokens" o "lexemas". Cada token representa una unidad léxica en el código fuente, como palabras clave, identificadores, operadores, números, cadenas, etc. El analizador léxico también asigna un tipo a cada token para que el compilador o intérprete pueda entender su significado.

1. Definición de tipos de tokens (TokenType):
   Se define una enumeración TokenType para representar los tipos de tokens posibles, como identificadores, palabras clave, operadores, constantes, cadenas, etc.

2. Palabras clave y caracteres especiales:
   Se definen dos diccionarios: KEYWORDS para palabras clave y SPECIALCHARS para caracteres especiales. Cada palabra clave o carácter especial se asocia con un tipo de token correspondiente.

3. Clase Token:
   Se define una clase Token que tiene dos atributos: value (el valor del token) y type (el tipo del token).

4. Funciones token e isskippable:
   Se define una función token para crear objetos Token de manera más conveniente.
   Se define una función isskippable para determinar si un carácter debe ser ignorado (espacio, tabulación o salto de línea).

5. Función identifyComplexToken:
   Esta función toma un token como entrada (token_str) y lo identifica como palabra clave, constante, cadena o identificador, según su contenido. Devuelve un objeto Token con el valor y el tipo correspondientes.

6. Función tokenize:
   La función principal que toma el código fuente de C# como entrada y produce una lista de tokens.
   Itera a través de cada carácter del código fuente y procesa de acuerdo con las reglas definidas:
   Detecta comentarios de una línea (//) y comentarios multilineales (/\* \*/).
   Detecta cadenas de texto (" ") y las maneja como un token separado.
   Reconoce caracteres especiales y los asigna al tipo de token correspondiente.
   Construye tokens complejos (palabras clave, constantes, identificadores) y los añade a la lista de tokens.

7. Función print_tokens:
   Esta función toma una lista de tokens y los imprime en una tabla para una mejor visualización. Solo muestra los tokens con un tipo definido.

8. Lectura del código fuente desde un archivo:
   Abre y lee un archivo llamado "test.cs".
   Llama a la función tokenize para dividir el código en tokens.
   Llama a la función print_tokens para imprimir los tokens.
