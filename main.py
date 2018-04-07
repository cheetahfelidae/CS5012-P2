from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    # Sentence
    S -> NP[NUM=?n] VP[NUM=?n] | WH AUX[NUM=?n] NP[NUM=?n] VP | WH NP[NUM=?n] VP S
    
    # WH-questions
    WH -> 'when'
    
    # Auxiliary
    AUX[NUM=sing] -> 'does' | 'has'
    AUX[NUM=plur] -> 'do'   | 'have'
    
    # Modal
    MODP[NUM=plur] -> MOD AUX[NUM=plur]
    MOD -> 'may'
    
    # Noun
    NP[NUM=?n]   -> NOM | DET[NUM=?n] NOM | PROP_N[NUM=?n]
    NP[NUM=plur] -> PROP_N[NUM=?n] CONJ NP[NUM=?n]
    # Nominal
    NOM -> NOM PP
    NOM -> ADJ NOM | N[NUM=?n] | GER
    
    # Gerund
    GER -> IV[FORM=pastpart] | TV[FORM=prespart] NP
    
    # Adjective
    ADJ -> 'blue' | 'healthy' | 'green'
    
    # Preposition
    PP  -> P NP
    P   -> 'in' | 'before' | 'on'
    
    # Conjunction
    CONJ -> 'and'
    
    # Verb
    VP[FORM=?t, NUM=?n] -> ADV VP[FORM=?t, NUM=?n] | MODP[NUM=plur] VP[FORM=?t, NUM=plur]
    VP[FORM=?t, NUM=?n] -> IV[FORM=?t, NUM=?n]
    VP[FORM=?t, NUM=?n] -> TV[FORM=?t, NUM=?n] NP | TV[FORM=?t, NUM=?n] NP NP | TV[FORM=?t, NUM=?n] S 
    
    # Adverb
    ADV -> 'always' | 'never'
    
    # Lexical
    DET[NUM=sing] -> 'a'
    DET[NUM=plur] -> 'these'
    DET -> 'the'
    PROP_N[NUM=sing]-> 'Bart' | 'Homer' | 'Lisa'
    N[NUM=sing] -> 'shoe'   | 'kitchen'     | 'table'   | 'salad'
    N[NUM=plur] -> 'shoes'  | 'kitchens'    | 'tables'  | 'salad'
    N -> 'milk' | 'midnight'
    
    IV[FORM=base, NUM=plur]     -> 'laugh'
    TV[FORM=base, NUM=plur]     -> 'drink'      | 'wear'    | 'serve'   | 'think' | 'like'
    IV[FORM=vbz,  NUM=sing]     -> 'laughs'
    TV[FORM=vbz,  NUM=sing]     -> 'drinks'     | 'wears'   | 'serves'  | 'thinks' | 'likes'
    IV[FORM=pret]               -> 'laughed'
    TV[FORM=pret]               -> 'drank'      | 'wore'    | 'served'  | 'thought' | 'liked'
    IV[FORM=pastpart]           -> 'laughed'
    TV[FORM=pastpart]           -> 'drunk'      | 'worn'    | 'served'  | 'thought' | 'liked'
    IV[FORM=prespart]           -> 'laughing'
    TV[FORM=prespart]           -> 'drinking'   | 'wearing'    | 'serving'  | 'thinking' | 'liking'
""")

uparser = FeatureChartParser(ugrammar)

text = """\
Bart laughs
Homer laughed
Bart and Lisa drink milk
Bart wears blue shoes
Lisa serves Bart a healthy green salad
Homer serves Lisa
Bart always drinks milk
Lisa thinks Homer thinks Bart drinks milk
Homer never drinks milk in the kitchen before midnight
when Homer drinks milk Bart laughs
when does Lisa drink the milk on the table
when do Lisa and Bart wear shoes
Bart likes drinking milk
Lisa may have drunk milk
Lisa may have seen Bart drinking milk
Lisa may not have seen Bart drinking milk
what does Homer drink
what salad does Bart serve
whom does Homer serve salad
whom do Homer and Lisa serve
what salad does Bart think Homer serves Lisa
"""
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
