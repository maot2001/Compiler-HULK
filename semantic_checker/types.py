from cmp.semantic import Type


class NumType(Type):
    def __init__(self):
        Type.__init__(self, 'Num')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, NumType)

class StrType(Type):
    def __init__(self):
        Type.__init__(self, 'Str')
    
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StrType)
    
class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')
    
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)