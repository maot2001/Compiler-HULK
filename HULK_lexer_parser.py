from cmp.pycompiler import Grammar
from parser.LR1_parser_generator import LR1Parser
from lexer.lexer_generator import Lexer



H = Grammar()
Program = H.NonTerminal('Program', True)

DeclList, Decl, Stat, Expr, SimpleExpr = H.NonTerminals('DeclList Decl Stat Expr SimpleExpr')
ArithExpr, Disj, Conj, Neg, DynTest, Comp, NumExpr, Term, Factor, Sign, Atom = H.NonTerminals('ArithExpr Disj Conj Neg DynTest Comp NumExpr Term Factor Sign Atom')
ExprBlock, StatList, ExprList, ExprTail, AssignList, VarDecl, ElifBranch = H.NonTerminals('ExprBlock StatList ExprList ExprTail AssignList VarDecl ElifBranch')
FuncDecl, Body, ArgList, ArgTail, TypeDecl, FeatureList = H.NonTerminals('FuncDecl Body ArgList ArgTail TypeDecl FeatureList')
ProtDecl, ProtMethods, FullyTypedArgs, FullyTypedTail, TypeList = H.NonTerminals('ProtDecl ProtMethods FullyTypedArgs FullyTypedTail TypeList')

num, str, bool, id, type_id = H.Terminals('num str bool id type_id')
leT, iN, iF, eliF, elsE, whilE, foR, aS, iS, neW = H.Terminals('let in if elif else while for as is new')
function, type, inherits, protocol, extends = H.Terminals('function type inherits protocol extends')
plus, minus, star, div, mod, pow, starstar = H.Terminals('+ - * / % ^ **')
eq, coloneq, eqeq, noteq, less, greater, leq, geq = H.Terminals('= := == != < > <= >=')
anD, oR, noT, oror = H.Terminals('& | ! ||')
dot, comma, colon, semi, at, atat, arrow = H.Terminals('. , : ; @ @@ =>')
opar, cpar, obrack, cbrack, obrace, cbrace = H.Terminals('( ) [ ] { }')





Program %= DeclList + Stat

DeclList %= Decl + DeclList
DeclList %= H.Epsilon

Decl %= function + FuncDecl
Decl %= type + TypeDecl
Decl %= protocol + ProtDecl



Stat %= SimpleExpr + semi
Stat %= ExprBlock
Stat %= ExprBlock + semi

Expr %= SimpleExpr
Expr %= ExprBlock

SimpleExpr %= leT + AssignList + iN + SimpleExpr
SimpleExpr %= iF + opar + Expr + cpar + Expr + ElifBranch + elsE + SimpleExpr
SimpleExpr %= whilE + opar + Expr + cpar + SimpleExpr
SimpleExpr %= foR + opar + id + iN + Expr + cpar + SimpleExpr
SimpleExpr %= id + coloneq + SimpleExpr
SimpleExpr %= id + dot + id + coloneq + SimpleExpr
SimpleExpr %= ArithExpr



ArithExpr %= Disj
ArithExpr %= ArithExpr + at + Disj
ArithExpr %= ArithExpr + atat + Disj

Disj %= Conj
Disj %= Disj + oR + Conj

Conj %= Neg
Conj %= Conj + anD + Neg

Neg %= DynTest
Neg %= noT + DynTest

DynTest %= Comp
DynTest %= Comp + iS + type_id

Comp %= NumExpr
Comp %= NumExpr + eqeq + NumExpr
Comp %= NumExpr + noteq + NumExpr
Comp %= NumExpr + less + NumExpr
Comp %= NumExpr + greater + NumExpr
Comp %= NumExpr + leq + NumExpr
Comp %= NumExpr + geq + NumExpr

NumExpr %= Term
NumExpr %= NumExpr + plus + Term
NumExpr %= NumExpr + minus + Term

Term %= Factor
Term %= Term + star + Factor
Term %= Term + div + Factor
Term %= Term + mod + Factor

Factor %= Sign
Factor %= Sign + pow + Factor
Factor %= Sign + starstar + Factor

Sign %= Atom
Sign %= minus + Atom

Atom %= num
Atom %= str
Atom %= bool
Atom %= id
Atom %= obrack + ExprList + cbrack
Atom %= obrack + Expr + oror + id + iN + Expr + cbrack
Atom %= opar + Expr + cpar
Atom %= neW + type_id + opar + ExprList + cpar
Atom %= id + opar + ExprList + cpar
Atom %= Atom + aS + type_id
Atom %= Atom + obrack + Expr + cbrack
Atom %= id + dot + id + opar + ExprList + cpar
Atom %= id + dot + id



ExprBlock %= obrace + StatList + cbrace
ExprBlock %= leT + AssignList + iN + ExprBlock
ExprBlock %= iF + opar + Expr + cpar + Expr + ElifBranch + elsE + ExprBlock
ExprBlock %= whilE + opar + Expr + cpar + ExprBlock
ExprBlock %= foR + opar + id + iN + Expr + cpar + ExprBlock
ExprBlock %= id + coloneq + ExprBlock
ExprBlock %= id + dot + id + coloneq + ExprBlock

StatList %= Stat
StatList %= Stat + StatList

ExprList %= Expr + ExprTail
ExprList %= H.Epsilon

ExprTail %= comma + Expr + ExprTail
ExprTail %= H.Epsilon

AssignList %= VarDecl + eq + Expr
AssignList %= VarDecl + eq + Expr + comma + AssignList

VarDecl %= id
VarDecl %= id + colon + type_id

ElifBranch %= eliF + opar + Expr + cpar + Expr + ElifBranch
ElifBranch %= H.Epsilon




FuncDecl %= id + opar + ArgList + cpar + Body
FuncDecl %= id + opar + ArgList + cpar + colon + type_id + Body

Body %= arrow + Stat
Body %= obrace + StatList + cbrace

ArgList %= VarDecl + ArgTail
ArgList %= H.Epsilon

ArgTail %= comma + VarDecl + ArgTail
ArgTail %= H.Epsilon




TypeDecl %= type_id + obrace + FeatureList + cbrace
TypeDecl %= type_id + opar + ArgList + cpar + obrace + FeatureList + cbrace
TypeDecl %= type_id + inherits + type_id + obrace + FeatureList + cbrace
TypeDecl %= type_id + opar + ArgList + cpar + inherits + type_id + opar + ExprList + cpar + obrace + FeatureList + cbrace

FeatureList %= VarDecl + eq + Stat + FeatureList
FeatureList %= FuncDecl + FeatureList
FeatureList %= H.Epsilon




ProtDecl %= type_id + obrace + ProtMethods + cbrace
ProtDecl %= type_id + extends + TypeList + obrace + ProtMethods + cbrace

ProtMethods %= id + opar + FullyTypedArgs + cpar + colon + type_id + semi + ProtMethods
ProtMethods %= H.Epsilon

FullyTypedArgs %= id + colon + type_id + FullyTypedTail
FullyTypedArgs %= H.Epsilon

FullyTypedTail %= comma + id + colon + type_id + FullyTypedTail
FullyTypedTail %= H.Epsilon

TypeList %= type_id
TypeList %= type_id + comma + TypeList




class HulkParser(LR1Parser):
    def __init__(self):
        super().__init__(H)





table = [ (str, '"([\x00-!#-\x7f]|\\\\")*"'),
          (num, '(0|[1-9][0-9]*)(.[0-9]+)?'),
          (bool, 'true|false')               ]

table.extend((H[lex], lex) for lex in 'let in if elif else while for as is new'.split())
table.extend((H[lex], lex) for lex in 'function type inherits protocol extends'.split())
table.extend((H[lex], lex) for lex in '/ % ^ = := == != < > <= >= & !'.split())
table.extend((H[lex], lex) for lex in '. , : ; @ @@ => { }'.split())
table.extend([(star, '\*'),(starstar,'\*\*'),(oR, '\|'),(oror,'\|\|'),(opar,'\('),(cpar,'\)')])
table.extend([(plus, '\+'), (minus, '\-'), (obrack,'\['), (cbrack,'\]')])
table.append(('space', '  *'))
table.append(('endofline', '\n'))
table.append((type_id, '[A-Z][_a-zA-Z0-9]*'))
table.append((id, '[_a-z][_a-zA-Z0-9]*'))


class HulkLexer(Lexer):
    def __init__(self):
        super().__init__(table, H.EOF)

    def __call__(self, text):
        tokens = super().__call__(text)
        return [token for token in tokens if token.token_type not in ['space', 'endofline']]












