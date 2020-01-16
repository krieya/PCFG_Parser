# test
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

assert pcykparser.best_parse()[0] == Tree.fromstring('''(S
  (NP time)
  (VP
    (VB flies)
    (PP (IN like) (NP (DT an) (NN arrow)))))
''')

print('Success!')