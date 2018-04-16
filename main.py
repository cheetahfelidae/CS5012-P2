from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    S -> NP[NUM=?n] VP[NUM=?n]
    S -> PP S
    S -> WH-NP AUX[NUM=?n] NP VP
    NP[NUM=?n] -> PROP_N[NUM=?n] | DET[NUM=?n] NOM[NUM=?n] | PROP_N[NUM=?n] GER_P
    NP[NUM=pl] -> NP[NUM=?n] CONJ NP[NUM=?n]
    
    VP[SUBCAT=?rest] -> VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg] | V[NUM=?n, SUBCAT=?rest]
    VP[SUBCAT=?rest] -> ADV_P V[NUM=?n, SUBCAT=?rest] | V[NUM=?n, SUBCAT=?rest] ADV_P 
    VP[SUBCAT=?rest] -> MODP VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest] -> VTB VP[SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest] -> VTB VP[SUBCAT=?rest]
    
    NOM[NUM=?n] -> ADJ_P NOM[NUM=?n] | N[NUM=?n] | N[NUM=?n] PP | GER_P | NOM N[NUM=?n]
    
    GER_P -> GER NP | GER NOM
    GER -> V[FORM=prespart, SUBCAT=nil]
    
    MODP -> MOD AUX[NUM=pl] |  MOD 'not' AUX[NUM=pl]
    
    ADJ_P -> ADJ | ADJ ADJ_P
    ADV_P -> ADV | ADV ADV_P
    PP -> PREP NP | PREP S | PREP NOM
    WH-NP -> WH | WH ARG[CAT=?arg] 
    
    ARG[CAT=np] -> NP
    ARG[CAT=pp] -> PP
    ARG[CAT=nom] -> NOM
    ARG[CAT=s] -> S
    
    ################# Lexicon #################
    
    ################# VERB ####################
    ###########################################
    
    ############### PRESENT ###################
    #########----- Intransitive -----##########
    V[TENSE=pres, NUM=sg, SUBCAT=nil]-> 'laughs' | 'smiles' | 'walks' | 'serves' | 'drinks'
    V[TENSE=pres, NUM=pl, SUBCAT=nil] -> 'laugh' | 'smile' | 'walk' | 'serve' |'drink'
    
    #########----- Transitive ------###########
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=s,TAIL=nil]] -> 'thinks' | 'believes'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=s,TAIL=nil]] -> 'think' | 'believe'
    
    
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=np,TAIL=nil]] ->'serves' | 'drinks' 
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=np,TAIL=nil]] ->'serve' | 'drink' 
    
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walks' | 'teaches' 
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walk' | 'teach' 
    
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drink' | 'wear' | 'serve' | 'like'
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drinks' | 'wears' | 'serves' | 'likes'
    
    ######### primary & secondary ########
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serves'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serve'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=nom, TAIL=[HEAD=np,TAIL=nil]]] -> 'serve'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=s, TAIL=[HEAD=np,TAIL=nil]]] -> 'think' | 'believe'
    
    ################# Past ####################
    #########----- Intransitive -----##########
    V[TENSE=past, SUBCAT=nil] -> 'laughed' | 'smiled' | 'walked'
    
    #########----- Transitive ------###########
    V[TENSE=past, SUBCAT=[HEAD=np,TAIL=nil]] -> 'drank' | 'wore' | 'served'
    V[TENSE=past, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drank' | 'wore' | 'served'
    V[TENSE=pastpart, SUBCAT=[HEAD=np,TAIL=nil]] ->'drunk' | 'worn' | 'served' | 'seen'
    V[TENSE=pastpart, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drunk' | 'worn' | 'served' | 'seen'
    
    
    ############### PRESENT CONT. #############
    V[TENSE=prescon, FORM=prespart , SUBCAT=[HEAD=nom,TAIL=nil]] -> 'drinking' | 'wearing' | 'using' | 'fighting'
    V[TENSE=prescon, FORM=prespart , SUBCAT=[HEAD=np,TAIL=nil]] -> 'drinking' | 'wearing' | 'using' | 'fighting'
    V[TENSE=prescon, FORM=prespart , SUBCAT=[HEAD=pp,TAIL=nil]] -> 'drinking' | 'fighting' | 'walking'
    
    ################# GERUND #################
    V[FORM=prespart, SUBCAT=nil] -> 'drinking' | 'smiling' | 'wearing' | 'crying' | 'flying'
    
    
    ################## NOUN ###################
    ###########################################
    PROP_N[NUM=sg] -> 'Homer' | 'Bart' | 'Lisa'
    N[NUM=sg] -> 'milk' | 'salad' | 'midnight' | 'kitchen' | 'table' | 'robot' | 'sky'
    N[NUM=pl] -> 'shoes' | 'tables' | 'robots'
    
    ################## Modal ##################
    MOD -> 'may'
    
    ################ Determiner ###############
    DET[NUM=sg] -> 'a' | 'the' | 'that'
    DET[NUM=pl] -> 'the' | 'these' | 'those'
    
    ################ Conjunction ##############
    CONJ -> 'and'
    
    ############ Adverb & Adjective ############
    ADJ -> 'blue' | 'healthy' | 'green' | 'same'
    ADV -> 'always' | 'never' | 'intensely'
    
    ############## Preposition ##################
    PREP -> 'in' | 'before' | 'when' | 'on' | 'beyond'
    
    AUX[NUM=sg] -> 'does' | 'has'
    AUX[NUM=pl] -> 'do' | 'have'
    VTB[NUM=sg] -> 'is'
    VTB[NUM=pl] -> 'are'
    
    WH -> 'when' | 'what' | 'where' | 'whom'
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
    Bart thinks Lisa drinks milk on the table
    
    Bart likes drinking milk
    Lisa may have drunk milk
    Lisa may have seen Bart drinking milk
    Lisa may not have seen Bart drinking milk
    what does Homer drink
    what salad does Bart serve
    whom does Homer serve salad
    whom do Homer and Lisa serve
    what salad does Bart think Homer serves Lisa
    Lisa is drinking milk
    Lisa and Bart are wearing the same blue shoes
    those robots are fighting intensely beyond the sky
    Bart wears milk beyond the healthy kitchen
"""
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
