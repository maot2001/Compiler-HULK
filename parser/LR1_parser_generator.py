from cmp.pycompiler import *
from cmp.utils import ContainerSet
from cmp.automata import State, multiline_formatter



class ShiftReduceParser:

    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G: Grammar, verbose: bool = False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w: list[Terminal], get_shift_reduce = False) -> list[Production]:
        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        actions = self.action.keys()
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])

            for e in actions:
                try:
                    if state == e[0] and lookahead.Name == e[1].Name:                        
                        lookahead = e[1]
                        break
                except:
                    print(e)
                    
              
            if (state, lookahead) not in self.action:
                return None
            
            action, tag = self.action[state, lookahead]
            match action:
                case self.SHIFT:
                    stack.append(lookahead)
                    stack.append(tag)
                    cursor += 1
                    operations.append(self.SHIFT)
                case self.REDUCE:
                    head, body = tag
                    for i in range(2 * len(body)):
                        stack.pop()
                    next_state = self.goto[stack[-1],head]
                    stack.append(head.Name)
                    stack.append(next_state)
                    output.append(tag)
                    operations.append(self.REDUCE)
                case self.OK:
                    if get_shift_reduce:
                        return output, operations 
                    return output
                case _:
                    raise ValueError
                


class LR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = self.build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:                
                if item.IsReduceItem:
                    production = item.production
                    if production.Left == G.startSymbol:
                        self._register(self.action,(idx,G.EOF),(self.OK,None))
                    else:
                        for symbol in item.lookaheads:
                            self._register(self.action,(idx,symbol),(self.REDUCE,production))
                else:
                    symbol = item.NextSymbol
                    goto_node = node[symbol.Name][0]
                    if symbol.IsTerminal:
                        self._register(self.action,(idx,symbol),(self.SHIFT,goto_node.idx))
                    else:
                        self._register(self.goto,(idx,symbol),goto_node.idx)
        
    @staticmethod
    def _register(table: dict, key: tuple[int,Symbol], value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        # if not (key not in table or table[key] == value):
        #     print(node)
        #     print(item)
        #     print(table[key])
        #     raise Exception
        table[key] = value



    @staticmethod
    def build_LR1_automaton(G: Grammar) -> State:
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
        firsts = compute_firsts(G)
        firsts[G.EOF] = ContainerSet(G.EOF)
    
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=(G.EOF,))
        start = frozenset([start_item])
    
        closure = LR1Parser.closure_lr1(start, firsts)
        automaton = State(frozenset(closure), True)
    
        pending = [ start ]
        visited = { start: automaton }
    
        while pending:
            current = pending.pop()
            current_state = visited[current]
        
            for symbol in G.terminals + G.nonTerminals:
                next_items = LR1Parser.goto_lr1(current_state.state, symbol, just_kernel=True)
                if not next_items:
                    continue
                try:
                    next_state = visited[next_items]
                except KeyError:                    
                    closure = LR1Parser.closure_lr1(next_items, firsts)
                    next_state = visited[next_items] = State(frozenset(closure), True)
                    pending.append(next_items)                               
            
                current_state.add_transition(symbol.Name, next_state)
    
        automaton.set_formatter(multiline_formatter)
        return automaton
    

    
    @staticmethod 
    def closure_lr1(items, firsts):
        closure = ContainerSet(*items)
    
        changed = True
        while changed:
            changed = False
        
            new_items = ContainerSet()
            for item in closure:
                new_items.extend(LR1Parser.expand(item, firsts))        

            changed = closure.update(new_items)
        
        return LR1Parser.compress(closure)
    
    
    @staticmethod
    def expand(item: Item, firsts: dict[Symbol: ContainerSet]) -> list[Item]:
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        for preview in item.Preview():
            lookaheads.hard_update(compute_local_first(firsts, preview))

        assert not lookaheads.contains_epsilon

        child_items = []
        for production in next_symbol.productions:
            child_items.append(Item(production, 0, lookaheads))
        return child_items
    
    @staticmethod 
    def compress(items: list[Item]) -> set[Item]:
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
    
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }
    

    def goto_lr1(items, symbol: Symbol, firsts: dict[Sentence:ContainerSet] = None, just_kernel: bool = False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else LR1Parser.closure_lr1(items, firsts)
    




def compute_firsts(G: Grammar) -> dict[Sentence: ContainerSet]:
    firsts = {}
    change = True
    
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
                
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            local_first = compute_local_first(firsts, alpha)
            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts


def compute_local_first(firsts: dict[Sentence: ContainerSet], alpha: Sentence) -> ContainerSet:
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    if alpha_is_epsilon:
        first_alpha.set_epsilon()    
    else:        
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha
    



    
