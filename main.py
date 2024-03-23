from HULK_lexer_parser import HulkParser, HulkLexer
import sys

def exec_file():
    lexer = HulkLexer()
    parser = HulkParser()
    with open(sys.argv[1]) as opened_file:
        text = opened_file.read()        
        tokens = lexer(text)        
        parse = parser([token.token_type for token in tokens])        
        print(parse is not None) 

if __name__ == "__main__":
    if len(sys.argv) != 1:
        exec_file()        
    else:
        print("Must provide a file to compile and run.")



