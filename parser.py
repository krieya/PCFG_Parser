import numpy as np
from nltk.tree import Tree
from nltk.grammar import Nonterminal
from collections import defaultdict
from nltk import CFG,PCFG


def create_table(sent_len):
    '''Create a table appropriate for CYK parsing. Returns a list of lists of empty lists'''
    
    outer_l = []
    
    for i in range(sent_len):
        outer_l.append([[] for j in range(i + 1)])
    
    return outer_l


def _create_parse_trees(current_node, current_parse, parse_pointers, sentence):
    '''Helper function that does recursion to create parse trees'''
    
    for pointers in parse_pointers[current_node]:
        parse = Tree(str(current_node[2]), [])
        for pointer in pointers:
            if pointer[0] == pointer[1]:
                parse.append(Tree(str(pointer[2]), [sentence[len(sentence) - 1 - pointer[0]]]))
            else:
                _create_parse_trees(pointer, parse, parse_pointers, sentence)
            
        current_parse.append(parse)
            
    return current_parse
            
            
def create_parse_trees(parse_pointers, sentence, grammar):
    '''
    Return a list of possible parse trees for the sentence
    '''
    for lookup in parse_pointers:
        if lookup == (len(sentence) - 1, 0, Nonterminal('S')):
            return _create_parse_trees(lookup, [], parse_pointers, sentence)


class PCYKParser(object):
    
    def __init__(self, grammar, trace = 0):
        '''
        Convert the grammar into CNF and create a LHS lookup dictionary;
        If trace = 1, the internal steps will be printed out
        '''
        
        self.LHS_lookup = defaultdict(list)
        self.grammar = grammar
        self.trace = trace
        self.parses = []
        
        temp_grammar = CFG.binarize(self.grammar)
        self.grammar = CFG.remove_unitary_rules(temp_grammar)
        
        for g in self.grammar.productions():
            self.LHS_lookup[g.rhs()].append(g.lhs())
        
    
    def parse(self,sentence):
        '''
        Return a dictionary to look up for labels and back pointers in the parse table
        '''
        pointers = defaultdict(list)
        
        length = len(sentence)
        
        if any(self.LHS_lookup[(word, )] is None for word in sentence):
            return False
        else:
            table = create_table(length)
        
        
        for i in reversed(range(length)):
            for j in range(length - i):
                if i == i + j:
                    lookup = self.LHS_lookup[(sentence[length - i - 1], )]
                    table[i][i + j] = lookup
                    if self.trace == 1:
                        print(f"adding {lookup} to table at position {i}, {i+j}.")
  
        for i in reversed(range(length)):
            for j in range(length - i):
                if i != i + j:
                    for k in range(j):
                            
                        b1s = table[i + j][i + j -k]
                        b2s = table[i + j - k - 1][i]
                        for b1 in b1s:
                            for b2 in b2s:    
                                if self.LHS_lookup[(b1, b2)]:
                                        
                                    tup1 = (i+j, i+j-k, b1)
                                    tup2 = (i+j-k-1, i, b2)

                                    for l in self.LHS_lookup[(b1, b2)]:
                                        cell = (i+j, i, l)
                                        pointers[cell].append((tup1, tup2))

                                    table[i + j][i].extend(self.LHS_lookup[(b1, b2)]) 
                                    if self.trace == 1:
                                        print(f"adding {self.LHS_lookup[(b1, b2)]} to table at position {i + j}, {i}.")
        
        if any(s == Nonterminal("S") for s in table[length-1][0]):            
            self.parses = create_parse_trees(pointers, sentence, self.grammar)
        
        
    def best_parse(self):
        '''
        Return the best parse tree among the parses and the corresponding probability
        '''
        parses = self.parses
        pcfg_grammar = self.grammar
        prob = np.ones(len(parses))
        prob_lookup = dict()
        for pcfg_production in pcfg_grammar.productions():
            prob_lookup[str(pcfg_production).split("[")[0].strip()] = pcfg_production.prob()
        for i, parse in enumerate(parses):
            for prod in parse.productions():
                prod_prob =  prob_lookup[str(prod)]
                if prod_prob:
                    prob[i] *= prod_prob
                    print(f"multiplying probability {prod_prob} from the rule {str(prod)}")
    
        return parses[np.argmax(prob)], prob[np.argmax(prob)]
    

# Test case

if __name__ == '__main__':
    
    S = ['time', 'flies', 'like', 'an', 'arrow']

    pcfg_grammar = PCFG.fromstring("""
    S -> NP VP [1.0] 
    NN -> 'flies' [0.1] | 'arrow' [0.6] | 'time' [0.3]
    NP -> NN NN [0.1] | DT NN [0.6] | 'time' [0.3]
    DT -> 'an' [1.0]
    VP -> VB NP [0.3] | VB PP [0.7]
    VB -> 'flies' [0.9] | 'like' [0.1]
    PP -> IN NP [1.0]
    IN -> 'like' [1.0]
    """)

    pcykparser = PCYKParser(pcfg_grammar, trace = 1)
    pcykparser.parse(S)

    print("Best Parse:")
    print(pcykparser.best_parse()[0])
