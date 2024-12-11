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

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.register_count = 0

    def generate(self, ast):
        # Generate code based on AST nodes
        if isinstance(ast, AssignNode):
            # For assignment, generate the assignment code
            register = self.get_next_register()
            value_code = self.generate(ast.value)
            self.code.append(f"MOV {register}, {value_code}")  # Move value into register
            self.code.append(f"STORE {register}, {ast.identifier}")  # Store result in variable
        elif isinstance(ast, NumberNode):
            # For numbers, simply return their value
            return str(ast.value)
        elif isinstance(ast, AddNode):
            # For addition, generate the addition expression
            left = self.generate(ast.left)
            right = self.generate(ast.right)
            register1 = self.get_next_register()  # Register for left operand
            self.code.append(f"MOV {register1}, {left}")  # Move left operand to register1
            self.code.append(f"ADD {register1}, {right}")  # Perform addition in register1
            return register1  # Return the result register

    def get_next_register(self):
        # Generate the next register name
        self.register_count += 1
        return f"R{self.register_count}"

    def get_code(self):
        return '\n'.join(self.code)




# Sample input to test the lexer and parser
data = "x = 5 + 10"

lexer.input(data)
for tok in lexer:
    print(tok)

# Parse input
ast = parser.parse(data)
print("AST:", ast)

# Code Generation for Assembly
code_generator = CodeGenerator()
code_generator.generate(ast)
generated_code = code_generator.get_code()

# Print the generated assembly code
print("Generated Assembly Code:\n", generated_code)
