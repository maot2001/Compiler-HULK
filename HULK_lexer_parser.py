from cmp.pycompiler import Grammar
from parser.LR1_parser_generator import LR1Parser
from lexer.lexer_generator import Lexer



H = Grammar()
Program = H.NonTerminal('Program', True)

StatementList, Statement, Expression, SimpleExpr = H.NonTerminals('StatementList Statement Expression SimpleExpr')
ArithExpr, Disj, Conj, Comp, Expr, Term, Factor, Atom = H.NonTerminals('ArithExpr Disj Conj Comp Expr Term Factor Atom')
ExprBlock, BlockExprList, LetExprBlock, AssignList, VarDecl = H.NonTerminals('ExprBlock BlockExprList LetExprBlock AssignList VarDecl')
ExprList, ExprTail, ElifBranches = H.NonTerminals('ExprList ExprTail ElifBranches')
FuncDef, Body, ArgList, ArgTail = H.NonTerminals('FuncDef Body ArgList ArgTail')
TypeDecl, AttrDef, AttrDefTail, MethodDef, MethodDefTail = H.NonTerminals('TypeDecl AttrDef ArrrDefTail MethodDef MethodDefTail')
ProtocolDef, ProtocolMethods, ProtocolMethodsTail, FullyTipedArgs, FullyTipedTail = H.NonTerminals('ProtocolDef ProtocolMethods ProtocolMethodsTail FullyTipedArgs FullyTipedTail')

num, str, bool, id = H.Terminals('num str bool id')
leT, iN, iF, eliF, elsE, whilE, foR, aS, iS, neW = H.Terminals('let in if elif else while for as is new')
function, type, inherits, protocol, extends = H.Terminals('function type inherits protocol extends') 
plus, minus, star, div, mod, pow = H.Terminals('+ - * / % ^')
eq, coloneq, eqeq, noteq, less, greater, leq, geq = H.Terminals('= := == != < < <= >=')
anD, oR, noT, doubleor = H.Terminals('& | ! ||')
dot, comma, colon, semicolon, at, doubleat, arrow = H.Terminals('. , : ; @ @@ =>')
opar, cpar, obrack, cbrack, obrace, cbrace = H.Terminals('( ) [ ] { }')

Program %= StatementList
StatementList %= Statement | Statement + StatementList
Statement %= SimpleExpr + semicolon | ExprBlock | ExprBlock + semicolon | LetExprBlock | LetExprBlock + semicolon | FuncDef | TypeDecl | ProtocolDef

Expression %= SimpleExpr | ExprBlock | LetExprBlock
SimpleExpr %= ArithExpr | leT+AssignList+iN+SimpleExpr | leT+AssignList+iN+LetExprBlock | Atom+coloneq+Expression | neW+id+opar+ExprList+cpar
SimpleExpr %= iF+opar+Expression+cpar+Expression+ElifBranches+elsE+Expression | whilE+opar+Expression+cpar+Expression | foR+opar+id+iN+Expression+cpar+Expression
SimpleExpr %= obrack + ExprList + cbrack | ArithExpr + aS + id | ArithExpr + iS + id | obrack + Expr + doubleor + id + iN + Expression + cbrack

ArithExpr %= Disj | ArithExpr + at + Atom | ArithExpr + doubleat + Atom
Disj %= Conj | Disj + oR + Conj
Conj %= Comp | Conj + anD + Comp
Comp %= Expr | Expr+eqeq+Expr | Expr+noteq+Expr | Expr+less+Expr | Expr+greater+Expr | Expr+leq+Expr | Expr+geq+Expr 
Expr %= Term | Expr + plus + Term | Expr + minus + Term
Term %= Factor | Term + star + Factor | Term + div + Factor | Term + mod + Factor
Factor %= Atom | Atom + pow + Factor
Atom %= num | str | bool | noT + Atom | opar + Expression + cpar
Atom %= id | id + opar + ExprList + cpar | id + dot + id | id + dot + id + opar + ExprList + cpar
Atom %= id + obrack + Expression + cbrack

ExprBlock %= obrace + BlockExprList + cbrace
BlockExprList %= SimpleExpr+semicolon | SimpleExpr+semicolon+BlockExprList
BlockExprList %= ExprBlock+semicolon | ExprBlock+semicolon+BlockExprList | ExprBlock | ExprBlock+BlockExprList
BlockExprList %= LetExprBlock+semicolon | LetExprBlock+semicolon+BlockExprList | LetExprBlock | LetExprBlock+BlockExprList
LetExprBlock %= leT + AssignList + iN + ExprBlock
AssignList %= VarDecl + eq + Expression | VarDecl + eq + Expression + comma + AssignList
VarDecl %= id | id + colon + id        
ExprList %= Expression + ExprTail | H.Epsilon
ExprTail %= comma + Expression + ExprTail | H.Epsilon
ElifBranches %= eliF + opar + Expression + cpar + Expression + ElifBranches | H.Epsilon

FuncDef %= function + id + opar + ArgList + cpar + Body | function + id + opar + ArgList + cpar + colon + id + Body
Body %= arrow+SimpleExpr+semicolon  | arrow+LetExprBlock | ExprBlock+semicolon | ExprBlock  | arrow+LetExprBlock+semicolon
ArgList %= VarDecl + ArgTail | H.Epsilon
ArgTail %= comma + VarDecl + ArgTail | H.Epsilon

TypeDecl %= type + id + obrace + AttrDef + MethodDef + cbrace | type + id + opar + ArgList + cpar + obrace + AttrDef + MethodDef + cbrace
TypeDecl %= type+id+inherits+id+obrace+AttrDef+MethodDef+cbrace | type+id+opar+ArgList+cpar+inherits+id+opar+ExprList+cpar+obrace+AttrDef+MethodDef+cbrace
AttrDef %= VarDecl + eq + Expression + semicolon + AttrDefTail | H.Epsilon
AttrDefTail %= VarDecl + eq + Expression + semicolon + AttrDefTail | H.Epsilon
MethodDef %= FuncDef + MethodDefTail | H.Epsilon 
MethodDefTail %= FuncDef + MethodDefTail | H.Epsilon       

ProtocolDef %= protocol + id + obrace + ProtocolMethods + cbrace | protocol + id + extends + id + obrace + ProtocolMethods + cbrace
ProtocolMethods %= id + opar + FullyTipedArgs + cpar + colon + id + semicolon + ProtocolMethodsTail | H.Epsilon
ProtocolMethodsTail %= id + opar + FullyTipedArgs + cpar + colon + id + semicolon + ProtocolMethodsTail | H.Epsilon
FullyTipedArgs %= id + colon + id + FullyTipedTail | H.Epsilon
FullyTipedTail %= comma + id + colon + id + FullyTipedTail | H.Epsilon



class HulkParser(LR1Parser):    
    def __init__(self):        
        super().__init__(H)




table = [ (num, '(0|[1-9][0-9]*)(.[0-9]+)?'),
          (str, '\"([\x00-!]|[#-\x7f])*\"'),
          (bool, 'true|false')               ]

table.extend((H[lex], lex) for lex in 'let in if elif else while for as is new'.split())
table.extend((H[lex], lex) for lex in 'function type inherits protocol extends'.split())
table.extend((H[lex], lex) for lex in '/ % ^ = := == != < < <= >= & !'.split())
table.extend((H[lex], lex) for lex in '. , : ; @ @@ => { }'.split())
table.extend([(star, '\*'),(oR, '\|'),(doubleor,'\|\|'),(opar,'\('),(cpar,'\)')])
table.extend([(plus, '\+'), (minus, '\-'), (obrack,'\['), (cbrack,'\]')])
table.append(('space', '  *'))
table.append(('endofline', '\n'))
table.append((id, '[_a-zA-Z]|[_a-zA-Z0-9]*'))


class HulkLexer(Lexer):
    def __init__(self):
        super().__init__(table, H.EOF)

    def __call__(self, text):
        tokens = super().__call__(text)
        return [token for token in tokens if token.token_type not in ['space', 'endofline']]



 


