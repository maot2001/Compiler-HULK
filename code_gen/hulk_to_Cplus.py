import cmp.visitor as visitor
import code_gen.Cplus_lang as Cplus
from semantic_checker.ast import *

class BaseHULKToCplusVisitor:
    def __init__(self):
        self.dec_class = []
        self.functions = []
        self.current_type = None
        self.current_function = None
    
    @property
    def instructions(self):
        return self.current_function.instructions

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def register_function(self, function_name, function_type):
        function_node = Cplus.FunctionNode(function_name, function_type, [], [])
        self.functions.append(function_node)
        return function_node
    
    def register_class(self, name, parent=None):
        class_node = Cplus.ClassNode(name, parent, [], [], [])
        self.dec_class.append(class_node)
        return class_node
   
class HULKToCplusVisitor(BaseHULKToCplusVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope):
        ######################################################
        # node.decl_list -> [  ]
        # node.expr -> 
        ######################################################
        
        for declaration, in node.decl_list:
            self.visit(declaration, scope)

        self.current_function = self.register_function('main', 'int')
        try:
            for expr in node.expr:
                self.visit(expr, scope)
        except Exception as e:
            print(e)
            self.visit(node.expr, scope)
        self.register_instruction(Cplus.ReturnNode(0))
        self.current_function = None

        return Cplus.ProgramNode(self.dec_class, self.functions)
    
    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [  ]
        # node.args -> [  ]
        # node.parent_constructor_args -> [  ]
        ####################################################################
        
        type_node = self.register_class(node.id, node.parent)
        """type_node.constructs.extend([Cplus.ParamNode(attr) for attr in node.args])
        type_node.attributes.extend([self.visit(attr, scope) for attr in self.current_type.attributes])
        type_node.methods.extend([self.visit(func, scope) for func in self.current_type.methods])
        
        func_declarations = (f for f in node.features if isinstance(f, FuncDeclNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)"""
                
        self.current_type = None

    @visitor.when(FuncDeclNode)
    def visit(self, node: FuncDeclNode, scope):
        ###############################
        # node.id -> str
        # node.args -> [  ]
        # node.return_type -> str
        # node.body -> [  ]
        ###############################
        
        self.current_function = self.register_function(node.id, node.return_type)
        self.params.extend([Cplus.ParamNode(p.name, p.type) for p in node.args]) 
        
        value = None
        for instruction in node.body:
            value = self.visit(instruction, scope)
        
        if node.return_type == 'void':
            value = None

        self.register_instruction(Cplus.ReturnNode(value))
        self.current_function = None

    @visitor.when(FuncCallNode)
    def visit(self, node: FuncCallNode, scope):
        ###############################
        # node.id -> str
        # node.args -> [  ]
        ###############################

        params = [p.lex for p in node.args]
        func_call = Cplus.PrintFuncNode(node.id, params) if node.id == 'print' else Cplus.CallFuncNode(node.id, params)
        """for a in node.args:
            if isinstance(a, LiteralNumNode): p_type = 'int'
            elif isinstance(a, LiteralBoolNode): p_type = 'bool'
            elif isinstance(a, LiteralStrNode): p_type = 'string'
            else: p_type = a.id
            params.append(Cplus.ParamNode(a.lex, p_type))"""

        self.register_instruction(func_call)


def hulk_to_Cplus(ast):
    transpiler = HULKToCplusVisitor()
    formatter = Cplus.get_formatter()
    cplus_ast = transpiler.visit(ast, 'a')
    return formatter(cplus_ast)

"""
class DeclNode(Node):
    pass


class ExprNode(Node):
    pass


class ExprBlockNode(ExprNode):
    def __init__(self, expr_list) -> None:
        self.expr_list = expr_list


class LetNode(ExprNode):
    def __init__(self, assign_list, expr) -> None:
        self.assign_list = assign_list
        self.expr = expr


class IfNode(ExprNode):
    def __init__(self, cond, if_expr, elif_branches, else_expr) -> None:
        self.cond = cond
        self.if_expr = if_expr
        self.elif_branches = elif_branches  # lista de tupla de expresiones del tipo (elif_cond, elif_expr)
        self.else_expr = else_expr

class WhileNode(ExprNode):
    def __init__(self, cond, body) -> None:
        self.cond = cond
        self.body = body

class ForNode(ExprNode):
    def __init__(self, id, iterable, body) -> None:
        self.id = id
        self.iterable = iterable
        self.body = body

class DestrAssign(ExprNode):
    def __init__(self, id, expr, is_attr = False) -> None:
        self.id = id
        self.expr = expr 
        self.is_attr = is_attr


class AssignNode(Node):
    def __init__(self, var, expr) -> None:
        self.var = var        
        self.expr = expr

class VarDefNode(Node):
    def __init__(self, id, type = None) -> None:
        self.id = id
        self.type = type


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + str(rvalue)
    

class ConcatWithSpaceNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + " " + str(rvalue)
    

class OrNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue or rvalue


class AndNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue and rvalue
    
class NotNode(UnaryNode):
    @staticmethod
    def operate(value):
        return not value
    
class DynTestNode(ExprNode):
    def __init__(self, expr, type) -> None:
        self.expr = expr
        self.type = type


class EqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue == rvalue    

class NotEqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue != rvalue
    
class LessNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue < rvalue

class GreaterNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue > rvalue

class LeqNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue <= rvalue   

class GeqNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue >= rvalue   
    

class PlusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + rvalue

class MinusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue - rvalue    
    
class StarNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue * rvalue

class DivNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue / rvalue
    
class ModNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue % rvalue
    
class PowNode(BinaryNode):    
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue
    
class NegativeNode(UnaryNode):
    @staticmethod
    def operate(value):
        return - value
    



class LiteralNumNode(AtomicNode):
    pass

class LiteralBoolNode(AtomicNode):
    pass

class LiteralStrNode(AtomicNode):
    pass

class ConstantNode(AtomicNode):
    pass

class VarNode(AtomicNode):
    pass

class VectorNode(ExprNode):
    def __init__(self, expr_list) -> None:
        self.expr_list = expr_list

class ImplicitVector(ExprNode):
    def __init__(self, expr, id, iterable) -> None:
        self.expr = expr
        self.id = id
        self.iterable = iterable

class IndexingNode(ExprNode):
    def __init__(self, vector, index):
        self.vector = vector
        self.expr = index

class InstantiateNode(ExprNode):
    def __init__(self, type, expr_list) -> None:
        self.type = type
        self.expr_list = expr_list

class DowncastNode(ExprNode):
    def __init__(self, obj, type) -> None:
        self.obj = obj
        self.type = type

class FuncCallNode(ExprNode):
    def __init__(self, id, args):
        self.id = id
        self.args = args

class MethodCallNode(ExprNode):
    def __init__(self, obj, id, args):
        self.obj = obj
        self.id = id
        self.args = args

class AttrrCallNode(ExprNode):
    def __init__(self, obj, id) -> None:
        self.obj = obj
        self.id = id



class TypeDeclNode(DeclNode):
    def __init__(self, id, features, args = None, parent = None, parent_constructor_args = None) -> None:
        self.id = id
        self.features = features
        self.args = args
        self.parent = parent
        self.parent_constructor_args = parent_constructor_args

class MethodNode(Node):
    def __init__(self, id, args, body, return_type = None) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type
        self.body = body
              

class ProtDeclNode(DeclNode):
    def __init__(self, id, methods, parents) -> None:
        self.id = id
        self.methods = methods
        self.parents = parents

class ProtMethodNode(Node):
    def __init__(self, id, return_type, args: list[VarDefNode]) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type
"""
