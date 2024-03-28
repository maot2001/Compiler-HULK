import cmp.visitor as visitor
from semantic_checker.ast import *
from semantic_checker.types import *

def check_parents(initial_type,parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
       return check_parents(initial_type,parent.parent)
    else: return False

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
        self.context.types['None'] = NoneType()        
        self.context.types['<error>'] = ErrorType()
        for class_declaration in node.decl_list:
            self.visit(class_declaration)
        
    @visitor.when(TypeDeclNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)   
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtDeclNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.id,node.parents)   
        except SemanticError as ex:
            self.errors.append(ex.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_declaration in node.decl_list:
            self.visit(class_declaration)

    @visitor.when(TypeDeclNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        if node.parent:            
            try:
                parent_type = self.context.get_type(node.parent)
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
            except SemanticError as ex:
                self.errors.append(ex.text)
            if check_parents(self.current_type.name,self.current_type.parent):
                raise SemanticError("Cyclic inheritance is not allowed.")
        for feature in node.features:
            self.visit(feature)

    @visitor.when(ProtDeclNode)
    def visit(self, node:ProtDeclNode):
        self.current_type = self.context.get_type(node.id)
        if node.parents:  
            for parent in node.parents:        
                try:
                    parent_type = self.context.get_type(parent)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                if check_parents(self.current_type.name,parent_type):
                    raise SemanticError("Cyclic inheritance is not allowed.")
        for feature in node.methods:
            self.visit(feature)

    @visitor.when(ProtMethodNode)
    def visit(self, node:ProtMethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)
                
        try:
            type = self.context.get_type(node.return_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id,param_names,param_types,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node:MethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)
                
        try:
            type = self.context.get_type(node.return_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id,param_names,param_types,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(AssignNode)
    def visit(self,node:AssignNode):
        type_node=node.expr.type
        try:
            type = self.context.get_type(type_node)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_attribute(node.var.id,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)   

        