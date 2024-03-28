import cmp.visitor as visitor

class Node:
   pass

class ProgramNode:
    def __init__(self, declarations, functions):
        self.dec_class = declarations
        self.functions = functions

class ClassNode(Node):
    def __init__(self, name, parent, constructs, attributes, methods):
        self.name = name
        self.parent = parent
        self.constructs = constructs
        self.attributes = attributes
        self.methods = methods

class VarNode(Node):
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value

class ParamNode(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class FunctionNode(Node):
    def __init__(self, name, type, params, instructions):
        self.name = name
        self.return_type = type
        self.params = params
        self.instructions = instructions

class CallFuncNode(Node):
    def __init__(self, name, params):
        self.name = name
        self.params = params

class PrintFuncNode(CallFuncNode):
    pass    

class ConstructNode(FunctionNode):
    pass

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node: ProgramNode):
            dec_class = '\n\n'.join(self.visit(t) for t in node.dec_class)
            functions = '\n\n'.join(self.visit(t) for t in node.functions)
            if len(dec_class) > 0:
                dec_class = '\n\n' + dec_class

            return f'#include <iostream>\nusing namespace std;{dec_class}\n\n{functions}'

        @visitor.when(ClassNode)
        def visit(self, node: ClassNode):
            attributes = ';\n\t'.join(self.visit(x) for x in node.attributes)
            constructs = '\n\t'.join(self.visit(x) for x in node.constructs)
            methods = '\n\n\t'.join(self.visit(x) for x in node.methods)
            parent = f' : public {node.parent.name}' if node.parent else ''
            public = f'public:\n\t{constructs}\n\n\t{methods};\n' if len(node.methods)>0 or len(node.constructs)>0 else ''

            return f'class {node.name}{parent}\n' + '\{' + f'\n\t{attributes};\n{public}' + '\};'

        @visitor.when(VarNode)
        def visit(self, node: VarNode):
            value = f'= {node.value}' if node.value else ''
            return f'{node.type} {node.name}{value};\n'
        
        @visitor.when(ParamNode)
        def visit(self, node: ParamNode):
            return f'{node.type} {node.name}'
        
        @visitor.when(FunctionNode)
        def visit(self, node: FunctionNode):
            params = ', '.join(self.visit(x) for x in node.params)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'{node.return_type} {node.name}({params})\n' + '{' + f'\n\t{instructions}\n' + '}\n\n'

        @visitor.when(CallFuncNode)
        def visit(self, node: CallFuncNode):
            params = ', '.join(x for x in node.params)
            return f'{node.name}({params});'
        
        @visitor.when(PrintFuncNode)
        def visit(self, node: PrintFuncNode):
            params = ' '.join(x for x in node.params)
            return f'cout << {params} << endl;'
            
        
        @visitor.when(ConstructNode)
        def visit(self, node: ConstructNode):
            params = ', '.join(self.visit(x) for x in node.params)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'{node.name}({params})\n' + '\{' + f'\n\t{instructions}\n' + '\}\n\n'

        @visitor.when(AssignNode)
        def visit(self, node: AssignNode):
            return f'{node.dest} = {node.source};\n'

        @visitor.when(PlusNode)
        def visit(self, node: PlusNode):
            return f'{node.dest} = {node.left} + {node.right};'

        @visitor.when(MinusNode)
        def visit(self, node: MinusNode):
            return f'{node.dest} = {node.left} - {node.right};\n'

        @visitor.when(StarNode)
        def visit(self, node: StarNode):
            return f'{node.dest} = {node.left} * {node.right};\n'

        @visitor.when(DivNode)
        def visit(self, node: DivNode):
            return f'{node.dest} = {node.left} / {node.right};\n'

        @visitor.when(ReturnNode)
        def visit(self, node: ReturnNode):
            if not node.value is None:
                return f'return {node.value};'
            else: pass

        
    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))