import ply.yacc as yacc
from lexer import tokens  # Assuming lexer is already defined with tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left is None and self.right is None:
            return f'{self.type}({self.value})'
        else:
            return f'({self.left} {self.type} {self.right})'


# Grammar rules and actions
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    # Create an AST node for the binary operation with left and right children
    p[0] = ASTNode(p[2], left=p[1], right=p[3])
    print(f"Creating binary node: {p[0]}")  # Debugging print

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    # Parentheses just return the inner expression
    p[0] = p[2]
    print(f"Creating group node: {p[0]}")  # Debugging print

def p_expression_number(p):
    'expression : NUMBER'
    # A number is a leaf node in the AST (left and right are None)
    p[0] = ASTNode('NUMBER', value=p[1])
    print(f"Creating number node: {p[0]}")  # Debugging print

def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Example Input
input_data = "4 * 5"

# Parse the input
result = parser.parse(input_data)

# Print the AST
print(result)
