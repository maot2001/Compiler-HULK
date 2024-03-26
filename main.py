from HULK_lexer_parser import HulkParser, HulkLexer
import sys
import dill
import os

def load_src():
    route = os.getcwd()
    route = os.path.join(route, 'resources')
    
    try:
        with open(os.path.join(route, 'lexer.pkl'), 'rb') as lexer_file:
            lexer = dill.load(lexer_file)

        with open(os.path.join(route, 'parser.pkl'), 'rb') as parser_file:
            parser = dill.load(parser_file)

        return lexer, parser
    except:
        lexer = HulkLexer()
        parser = HulkParser()

        with open(os.path.join(route, 'lexer.pkl'), 'wb') as lexer_file:
            dill.dump(lexer, lexer_file)

        with open(os.path.join(route, 'parser.pkl'), 'wb') as parser_file:
            dill.dump(parser, parser_file)

        return lexer, parser
    
def exec_file():
    lexer, parser = load_src()
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



