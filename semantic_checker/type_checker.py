import cmp.visitor as visitor
from semantic_checker.ast import *
from semantic_checker.types import *

class Collector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Hulk_Context()
        self.context.types['Num'] = NumType() 
        self.context.types['Str'] = StringType()        
        self.context.types['Bool'] = BoolType()        
        self.context.types['<error>'] = ErrorType()
        for class_declaration in node.decl_list:
            self.visit(class_declaration)
        
    @visitor.when(TypeDeclNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)   
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FuncDeclNode)
    def visit(self, node):
        try:
            self.context.create_func(node.id,node.args,[],node.return_type)   
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtDeclNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.id,node.parents)   
        except SemanticError as ex:
            self.errors.append(ex.text)


