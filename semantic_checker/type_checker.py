from cmp.semantic import *
import cmp.visitor as visitor
from semantic_checker.ast import *
from semantic_checker.types import *

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        # Your code here!!!
        self.context.types['int'] = NumType() 
        self.context.types['string'] = StrType()        
        self.context.types['bool'] = BoolType()        
        self.context.types['error'] = ErrorType()
        for class_declaration in node.decl_list:
            self.visit(class_declaration)
        
    @visitor.when(TypeDeclNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)   
        except SemanticError as ex:
            self.errors.append(ex.text)