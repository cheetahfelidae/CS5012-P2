from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    # Sentence
    S -> NP[NUM=?n] VP[NUM=?n] 
    S -> WH AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP | WH NP[NUM=?n] AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP | WH NP[NUM=?n] VP S
    S ->    AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP
    
    # WH-questions
    WH -> 'what' | 'when' | 'where' | 'why' | 'whom'
    
    ######################################################################################
    ################################### Noun Phrase ######################################
    ######################################################################################
    NP[NUM=?n]   -> PRE_DET NP[NUM=?n]| DET[NUM=?n] NOM | NOM
    NP[NUM=plur] -> PROP_N[NUM=?n] CONJ NP[NUM=?n]
    
    ######### Predeterminers #########
    PRE_DET       -> 'all'
    
    ######### Determiners #############
    DET[NUM=sing] -> 'a' | 'that'
    DET[NUM=plur] -> 'these'
    DET -> 'the'
    
    ######### Adjective ###############
    ADJ -> 'blue' | 'healthy' | 'green'
    
    ######### Nominal #################
    NOM -> NOM PP | NOM REL_CL | NOM GER_P | NOM N[NUM=?n]
    NOM -> ADJ NOM | PROP_N[NUM=?n] | N[NUM=?n] | GER_P
    
    ######### Gerund Phrase ############
    GER_P -> GER PP | GER
    GER -> IV[FORM=prespart] | TV[FORM=prespart] NP
    
    ######### Preposition Phrase #######
    PP  -> P NP
    P   -> 'in' 'on' | 'at' | 'before' | 'after' | 'from' | 'to'
    
    ######## Relative Clause ###########
    REL_CL -> DET[NUM=sing] VP
    
    # Conjunction
    CONJ -> 'and'
    
    # Adverb
    ADV -> 'always' | 'never'
    
    
    
    
    PROP_N[NUM=sing]-> 'Bart' | 'Homer' | 'Lisa'
    
    N[NUM=sing] -> 'shoe'   | 'kitchen'     | 'table'   | 'salad' | 'plane'  | 'flight' | 'train'
    N[NUM=plur] -> 'shoes'  | 'kitchens'    | 'tables'  | 'salad' | 'planes' | 'flights'| 'trains'
    N -> 'milk' | 'morning' | 'midnight' | 'Edinburgh' | 'London' | '9' | '10' | 'breakfast'
    
    # Auxiliary
    AUX[FORM=base, NUM=sing]     -> 'does'
    AUX[FORM=base, NUM=plur]     -> 'do'
    AUX[FORM=pret]               -> 'did'
    AUX[FORM=pastpart, NUM=sing] -> 'has'
    AUX[FORM=pastpart, NUM=plur] -> 'have'
    
    # Not
    NOT -> 'not'
    
    # Modal
    MODP[NUM=plur] -> MOD AUX[NUM=plur] | MOD NOT AUX[NUM=plur]
    MOD -> 'may'
    
    # Verb
    VP[FORM=?t, NUM=?n] -> ADV VP[FORM=?t, NUM=?n] | MODP[NUM=plur] VP[FORM=?t, NUM=plur]
    VP[FORM=?t, NUM=?n] -> IV[FORM=?t, NUM=?n] | IV[FORM=?t, NUM=?n] PP
    VP[FORM=?t, NUM=?n] -> TV[FORM=?t, NUM=?n] NP | TV[FORM=?t, NUM=?n] NP NP | TV[FORM=?t, NUM=?n] S 
    
    IV[FORM=base, NUM=plur]     -> 'drink'      | 'serve'   | 'laugh'    | 'leave'
    TV[FORM=base, NUM=plur]     -> 'drink'      | 'wear'    | 'serve'    | 'think' | 'like' | 'see'
    IV[FORM=vbz,  NUM=sing]     -> 'drinks'     | 'serves'  | 'laughs'   | 'leaving'
    TV[FORM=vbz,  NUM=sing]     -> 'drinks'     | 'wears'   | 'serves'   | 'thinks' | 'likes' | 'sees'
    IV[FORM=pret]               -> 'drank'      | 'served'  | 'laughed'  | 'left'
    TV[FORM=pret]               -> 'drank'      | 'wore'    | 'served'   | 'thought' | 'liked' | 'saw'
    IV[FORM=pastpart]           -> 'drunk'      | 'served'  | 'laughed'  | 'left'
    TV[FORM=pastpart]           -> 'drunk'      | 'worn'    | 'served'   | 'thought' | 'liked' | 'seen'
    IV[FORM=prespart]           -> 'drinking'   | 'serving' | 'laughing' | 'leaving'
    TV[FORM=prespart]           -> 'drinking'   | 'wearing' | 'serving'  | 'thinking' | 'liking' | 'seeing'
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
did the plane leave
all the morning trains from Edinburgh to London leave before 10
all flights that serve breakfast leave at 9
"""
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
