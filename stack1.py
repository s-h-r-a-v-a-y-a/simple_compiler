import ply.yacc as yacc
from stack import lexer,tokens  # Import tokens from lexer

# Symbol Table to store variable values
symbol_table = {}

# Abstract Syntax Tree (AST) classes
class AssignNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"AssignNode({self.identifier}, {self.value})"

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class AddNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"AddNode({self.left}, {self.right})"

# List of precedence rules (just a placeholder for addition)
precedence = (
    ('left', 'PLUS'),
)

# Grammar rules
def p_statement_assign(p):
    'statement : IDENTIFIER ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])
    symbol_table[p[1]] = p[3]  # Add the variable to the symbol table

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumberNode(int(p[1]))

def p_expression_addition(p):
    'expression : expression PLUS expression'
    p[0] = AddNode(p[1], p[3])

# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Sample input to test the lexer and parser
data = """x = 5 + 10"""

lexer.input(data)
for tok in lexer:
    print(tok)

# Parse input
result = parser.parse(data)
print(result)

# Display the symbol table
print("Symbol Table:", symbol_table)
