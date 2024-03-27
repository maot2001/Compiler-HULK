from cmp.semantic import Type,Context,SemanticError,Method

class NumType(Type):
    def __init__(self):
        Type.__init__(self, 'numerical')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, NumType)

class StringType(Type):
    def __init__(self):
        Type.__init__(self,'string')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

class BoolType(Type):
    def __init__(self):
        Type.__init__(self,'bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
    
class Func:
    def __init__(self,name,args,return_type):
        self.name = name
        self.param_names = args
        self.return_type = return_type

    def __str__(self):
        output = f'func {self.name}'
        output += ' ('
        output += ')'
        return output

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type #and \
            #other.param_types == self.param_types

    
class Protocol:
    def __init__(self,name:str,parent=None):
        self.name=name
        self.parent = parent
        self.methods=[]

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            
    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else ' : '.join(parent for parent in self.parent)
        output +=': '+ parent
        output += ' {'
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output
    

class Hulk_Context(Context):
    def __init__(self):
        Context.__init__(self)
        self.func = {}
        self.prot = {}

    def create_func(self, name, params, params_type, return_type):
        if name in self.func:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.func[name] = Func(name,params,return_type)
        return typex

    def get_func(self, name:str):
        try:
            return self.func[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')
        
    def create_protocol(self,name,parents):
        if name in self.prot:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.prot[name] = Protocol(name,parents)
        return typex
    
    def get_prot(self, name:str):
        try:
            return self.prot[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')
        
    def __str__(self):
        types_str='Types: {\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'
        func_str='Funcs: {\n\t' + '\n\t'.join(y for x in self.func.values() for y in str(x).split('\n')) + '\n}'
        prot_str='Protocols: {\n\t' + '\n\t'.join(y for x in self.prot.values() for y in str(x).split('\n')) + '\n}'
        return types_str+'\n'+func_str+'\n'+prot_str
    
