from cmp.pycompiler import Grammar
from parser.LR1_parser_generator import LR1Parser
from lexer.lexer_generator import Lexer
from semantic_checker.ast import *



H = Grammar()
Program = H.NonTerminal('Program', True)

DeclList, Decl, Stat, Expr, SimpleExpr = H.NonTerminals('DeclList Decl Stat Expr SimpleExpr')
ArithExpr, Disj, Conj, Neg, DynTest, Comp, NumExpr, Term, Factor, Sign, Atom = H.NonTerminals('ArithExpr Disj Conj Neg DynTest Comp NumExpr Term Factor Sign Atom')
ExprBlock, StatList, ExprList, ExprTail, AssignList, VarDecl, ElifBranch = H.NonTerminals('ExprBlock StatList ExprList ExprTail AssignList VarDecl ElifBranch')
FuncDecl, Body, ArgList, ArgTail, TypeDecl, FeatureList = H.NonTerminals('FuncDecl Body ArgList ArgTail TypeDecl FeatureList')
ProtDecl, ProtMethods, FullyTypedArgs, FullyTypedTail, TypeList = H.NonTerminals('ProtDecl ProtMethods FullyTypedArgs FullyTypedTail TypeList')

num, str, bool, const, id, type_id = H.Terminals('num str bool const id type_id')
leT, iN, iF, eliF, elsE, whilE, foR, aS, iS, neW = H.Terminals('let in if elif else while for as is new')
function, type, inherits, protocol, extends = H.Terminals('function type inherits protocol extends')
plus, minus, star, div, mod, pow, starstar = H.Terminals('+ - * / % ^ **')
eq, coloneq, eqeq, noteq, less, greater, leq, geq = H.Terminals('= := == != < > <= >=')
anD, oR, noT, oror = H.Terminals('& | ! ||')
dot, comma, colon, semi, at, atat, arrow = H.Terminals('. , : ; @ @@ =>')
opar, cpar, obrack, cbrack, obrace, cbrace = H.Terminals('( ) [ ] { }')





Program %= DeclList + Stat, lambda h,s: ProgramNode(s[1],s[2])

DeclList %= Decl + DeclList, lambda h,s: [s[1]] + s[2]
DeclList %= H.Epsilon, lambda h,s: []

Decl %= FuncDecl, lambda h,s: s[1]
Decl %= TypeDecl, lambda h,s: s[1]
Decl %= ProtDecl, lambda h,s: s[1]



Stat %= SimpleExpr + semi, lambda h,s: s[1]
Stat %= ExprBlock, lambda h,s: s[1]
Stat %= ExprBlock + semi, lambda h,s: s[1]

Expr %= SimpleExpr, lambda h,s: s[1]
Expr %= ExprBlock, lambda h,s: s[1]

SimpleExpr %= leT + AssignList + iN + SimpleExpr, lambda h,s: LetNode(s[2],s[4])
SimpleExpr %= iF + opar + Expr + cpar + Expr + ElifBranch + elsE + SimpleExpr, lambda h,s: IfNode(s[3],s[5],s[6],s[8])
SimpleExpr %= whilE + opar + Expr + cpar + SimpleExpr, lambda h,s: WhileNode(s[3],s[5])
SimpleExpr %= foR + opar + id + iN + Expr + cpar + SimpleExpr, lambda h,s: ForNode(s[3],s[5],s[7])
SimpleExpr %= id + coloneq + SimpleExpr, lambda h,s: DestrAssign(s[1],s[3])
SimpleExpr %= id + dot + id + coloneq + SimpleExpr, lambda h,s: DestrAssign(s[3],s[5],True)
SimpleExpr %= ArithExpr, lambda h,s: s[1]



ExprBlock %= obrace + StatList + cbrace, lambda h,s: ExprBlockNode(s[2])
ExprBlock %= leT + AssignList + iN + ExprBlock, lambda h,s: LetNode(s[2],s[4])
ExprBlock %= iF + opar + Expr + cpar + Expr + ElifBranch + elsE + ExprBlock, lambda h,s: IfNode(s[3],s[5],s[6],s[8])
ExprBlock %= whilE + opar + Expr + cpar + ExprBlock, lambda h,s: WhileNode(s[3],s[5])
ExprBlock %= foR + opar + id + iN + Expr + cpar + ExprBlock, lambda h,s: ForNode(s[3],s[5],s[7])
ExprBlock %= id + coloneq + ExprBlock, lambda h,s: DestrAssign(s[1],s[3])
ExprBlock %= id + dot + id + coloneq + ExprBlock, lambda h,s: DestrAssign(s[3],s[5],True)

StatList %= Stat, lambda h,s: [s[1]]
StatList %= Stat + StatList, lambda h,s: [s[1]] + s[2]

ExprList %= Expr + ExprTail, lambda h,s: [s[1]] + s[2]
ExprList %= H.Epsilon, lambda h,s: []

ExprTail %= comma + Expr + ExprTail, lambda h,s: [s[2]] + s[3]
ExprTail %= H.Epsilon, lambda h,s: []

AssignList %= VarDecl + eq + Expr, lambda h,s: [AssignNode(s[1],s[3])]
AssignList %= VarDecl + eq + Expr + comma + AssignList, lambda h,s: [AssignNode(s[1],s[3])] + []

VarDecl %= id, lambda h,s: VarDefNode(s[1])
VarDecl %= id + colon + type_id, lambda h,s: VarDefNode(s[1],s[3])

ElifBranch %= eliF + opar + Expr + cpar + Expr + ElifBranch, lambda h,s: [(s[3],s[5])] + s[6]
ElifBranch %= H.Epsilon, lambda h,s: []




ArithExpr %= Disj, lambda h,s: s[1]
ArithExpr %= ArithExpr + at + Disj, lambda h,s: ConcatNode(s[1],s[3])
ArithExpr %= ArithExpr + atat + Disj, lambda h,s: ConcatWithSpaceNode(s[1],s[3])

Disj %= Conj, lambda h,s: s[1]
Disj %= Disj + oR + Conj, lambda h,s: OrNode(s[1],s[3])

Conj %= Neg, lambda h,s: s[1]
Conj %= Conj + anD + Neg, lambda h,s: AndNode(s[1],s[3])

Neg %= DynTest, lambda h,s: s[1]
Neg %= noT + DynTest, lambda h,s: NotNode(s[2])

DynTest %= Comp, lambda h,s: s[1]
DynTest %= Comp + iS + type_id, lambda h,s: DynTestNode(s[1],s[3])

Comp %= NumExpr, lambda h,s: s[1]
Comp %= NumExpr + eqeq + NumExpr, lambda h,s: EqualNode(s[1],s[3])
Comp %= NumExpr + noteq + NumExpr, lambda h,s: NotEqualNode(s[1],s[3])
Comp %= NumExpr + less + NumExpr, lambda h,s: LessNode(s[1],s[3])
Comp %= NumExpr + greater + NumExpr, lambda h,s: GreaterNode(s[1],s[3])
Comp %= NumExpr + leq + NumExpr, lambda h,s: LeqNode(s[1],s[3])
Comp %= NumExpr + geq + NumExpr, lambda h,s: GeqNode(s[1],s[3])

NumExpr %= Term, lambda h,s: s[1]
NumExpr %= NumExpr + plus + Term, lambda h,s: PlusNode(s[1],s[3])
NumExpr %= NumExpr + minus + Term, lambda h,s: MinusNode(s[1],s[3])

Term %= Factor, lambda h,s: s[1]
Term %= Term + star + Factor, lambda h,s: StarNode(s[1],s[3])
Term %= Term + div + Factor, lambda h,s: DivNode(s[1],s[3])
Term %= Term + mod + Factor, lambda h,s: ModNode(s[1],s[3])

Factor %= Sign, lambda h,s: s[1]
Factor %= Sign + pow + Factor, lambda h,s: PowNode(s[1],s[3])
Factor %= Sign + starstar + Factor, lambda h,s: PowNode(s[1],s[3])

Sign %= Atom, lambda h,s: s[1]
Sign %= minus + Atom, lambda h,s: NegativeNode(s[2])

Atom %= num, lambda h,s: LiteralNumNode(s[1])
Atom %= str, lambda h,s: LiteralStrNode(s[1])
Atom %= bool, lambda h,s: LiteralBoolNode(s[1])
Atom %= const, lambda h,s: ConstantNode(s[1])
Atom %= id, lambda h,s: VarNode(s[1])
Atom %= obrack + ExprList + cbrack, lambda h,s: VectorNode(s[2])
Atom %= obrack + Expr + oror + id + iN + Expr + cbrack, lambda h,s: ImplicitVector(s[2],s[4],s[6])
Atom %= opar + Expr + cpar, lambda h,s: s[1]
Atom %= neW + type_id + opar + ExprList + cpar, lambda h,s: InstantiateNode(s[2],s[4])
Atom %= id + opar + ExprList + cpar, lambda h,s: FuncCallNode(s[1],s[3])
Atom %= Atom + aS + type_id, lambda h,s: DowncastNode(s[1],s[3])
Atom %= Atom + obrack + Expr + cbrack, lambda h,s: IndexingNode(s[1],s[3])
Atom %= id + dot + id + opar + ExprList + cpar, lambda h,s: MethodCallNode(s[1],s[3],s[5])
Atom %= id + dot + id, lambda h,s: AttrrCallNode(s[1],s[3])





FuncDecl %= function + id + opar + ArgList + cpar + Body, lambda h,s: FuncDeclNode(s[2], s[4], s[6])
FuncDecl %= function + id + opar + ArgList + cpar + colon + type_id + Body, lambda h,s: FuncDeclNode(s[2],s[4],s[8],s[7])

Body %= arrow + Stat, lambda h,s: s[2]
Body %= obrace + StatList + cbrace, lambda h,s: s[2]

ArgList %= VarDecl + ArgTail, lambda h,s: [s[1]] + s[2]
ArgList %= H.Epsilon, lambda h,s: []

ArgTail %= comma + VarDecl + ArgTail, lambda h,s: [s[2]] + s[3]
ArgTail %= H.Epsilon, lambda h,s: []




TypeDecl %= type + type_id + obrace + FeatureList + cbrace, lambda h,s: TypeDeclNode(s[2],s[4])
TypeDecl %= type + type_id + opar + ArgList + cpar + obrace + FeatureList + cbrace, lambda h,s: TypeDeclNode(s[2],s[7],s[4])
TypeDecl %= type + type_id + inherits + type_id + obrace + FeatureList + cbrace, lambda h,s: TypeDeclNode(s[2],s[6],None,s[4])
TypeDecl %= type + type_id + opar + ArgList + cpar + inherits + type_id + opar + ExprList + cpar + obrace + FeatureList + cbrace, lambda h,s: TypeDeclNode(s[2],s[12],s[4],s[7],s[9])

FeatureList %= VarDecl + eq + Stat + FeatureList, lambda h,s: [AssignNode(s[1],s[3])] + s[4]
FeatureList %= id + opar + ArgList + cpar + Body + FeatureList, lambda h,s: [MethodNode(s[1],s[3],s[5])] + s[6]
FeatureList %= id + opar + ArgList + cpar + colon + type_id + Body + FeatureList, lambda h,s: [MethodNode(s[1],s[3],s[7],s[6])] + s[8]
FeatureList %= H.Epsilon, lambda h,s: []




ProtDecl %= protocol + type_id + obrace + ProtMethods + cbrace, lambda h,s: ProtDeclNode(s[2],s[4])
ProtDecl %= protocol + type_id + extends +  TypeList + obrace + ProtMethods + cbrace, lambda h,s: ProtDeclNode(s[2],s[6],s[4])

ProtMethods %= id + opar + FullyTypedArgs + cpar + colon + type_id + semi + ProtMethods, lambda h,s: [ProtMethodNode(s[1],s[3],s[6])] + s[8]
ProtMethods %= H.Epsilon, lambda h,s: []

FullyTypedArgs %= id + colon + type_id + FullyTypedTail, lambda h,s: [VarDefNode(s[1],s[3])] + s[4]
FullyTypedArgs %= H.Epsilon, lambda h,s: []

FullyTypedTail %= comma + id + colon + type_id + FullyTypedTail, lambda h,s: [VarDefNode(s[2],s[4])] + s[5] 
FullyTypedTail %= H.Epsilon, lambda h,s: []

TypeList %= type_id, lambda h,s: [ s[1] ]
TypeList %= type_id + comma + TypeList, lambda h,s: [ s[1] ] + s[3]




class HulkParser(LR1Parser):
    def __init__(self):
        super().__init__(H)





table = [ (str, '"([\x00-!#-\x7f]|\\\\")*"'),
          (num, '(0|[1-9][0-9]*)(.[0-9]+)?'),
          (bool, 'true|false'),          
          (const, 'PI|E')]

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












