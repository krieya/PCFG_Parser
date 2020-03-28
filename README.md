# PCFG_Parser

An end-to-end PCFG parser. 

## Dependencies

- Python (>=3.6)
- NLTK
- collections

## Description

This parser uses [CYK Parsing Algorithm](https://en.wikipedia.org/wiki/CYK_algorithm) for context-free grammars. It takes a raw senetence and grammars in the format of  [Probabilistic  Context-Free Grammars](https://en.wikipedia.org/wiki/Probabilistic_context-free_grammar) and returns the best parsing tree based on probabilities.

## Example

For a raw sentence:

```
S = ['time', 'flies', 'like', 'an', 'arrow']
```

and given PCFG grammars:

```
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
```

it returns the best parse tree based on maximum probabilities:

```
(S (NP time) (VP (VB flies) (PP (IN like) (NP (DT an) (NN arrow)))))
```


## Credits

This task is mentored by my instructor [Julian Brooke](https://linguistics.ubc.ca/person/julian-brooke/) in my class COLX 535 Parsing in UBC. 