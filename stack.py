import ply.lex as lex

# List of token names.
tokens = (
    'NUMBER',
    'ASSIGN',
    'IDENTIFIER',
    'PLUS',
)

# Regular expression rules for simple tokens
t_ASSIGN = r'='
t_PLUS = r'\+'


# Regular expression rule for IDENTIFIER (variable names)
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Regular expression rule for NUMBER (integer values)
t_NUMBER = r'\d+'

# A rule for skipping whitespace
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
