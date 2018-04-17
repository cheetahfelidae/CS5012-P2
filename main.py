from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    S -> NP[NUM=?n] VP[NUM=?n]
    S -> PP S
    S -> WH-NP AUX[FORM=?f, NUM=?n] NP VP
    S -> AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP
    
    ######################################################################################################
    ############################################## NOUN PHRASE ###########################################
    ######################################################################################################
    NP[NUM=?n] -> PRE_DET NP[NUM=?n] | PROP_N[NUM=?n] | DET[NUM=?n] NOM[NUM=?n] | PROP_N[NUM=?n] GER_P | NOM
    NP[NUM=plur] -> NP[NUM=?n] CONJ NP[NUM=?n]
    
    NOM[NUM=?n] -> ADJ_P NOM[NUM=?n] | NOM REL_CL | N[NUM=?n] | N[NUM=?n] PP | GER_P | NOM N[NUM=?n] | NOM[NUM=?n] PP
    
    ######## Relative Clause ###########
    REL_CL -> REL_P VP | 'that' S
    REL_P  -> 'that' | 'who'
    
    VP[SUBCAT=?rest] -> VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg] | V[NUM=?n, SUBCAT=?rest]
    VP[SUBCAT=?rest] -> ADV_P V[NUM=?n, SUBCAT=?rest] | V[NUM=?n, SUBCAT=?rest] ADV_P 
    VP[SUBCAT=?rest] -> MODP VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest] -> VTB VP[SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest] -> VTB VP[SUBCAT=?rest]
    
    
    
    GER_P -> GER NP | GER NOM
    GER -> V[FORM=prespart, SUBCAT=nil]
    
    MODP -> MOD AUX[FORM=?f, NUM=plur] |  MOD 'not' AUX[FORM=?f, NUM=plur]
    
    ADJ_P -> ADJ | ADJ ADJ_P
    ADV_P -> ADV | ADV ADV_P
    PP -> P NP | P S | P NOM
    WH-NP -> WH | WH ARG[CAT=?arg] 
    
    ARG[CAT=np] -> NP
    ARG[CAT=pp] -> PP
    ARG[CAT=nom] -> NOM
    ARG[CAT=s] -> S
    ARG[CAT=cl] -> REL_CL
    
    ################# Lexicon #################
    
    ################# VERB ####################
    ###########################################
    
    ############### PRESENT ###################
    #########----- Intransitive -----##########
    V[TENSE=pres, NUM=sing, SUBCAT=nil]-> 'laughs' | 'smiles' | 'walks' | 'serves' | 'drinks' | 'leaves'
    V[TENSE=pres, NUM=plur, SUBCAT=nil] -> 'laugh' | 'smile' | 'walk' | 'serve' |'drink' | 'leave'
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=pp, TAIL=nil]] -> 'leave'
    
    #########----- Transitive ------###########
    V[TENSE=pres, NUM=sing, SUBCAT=[HEAD=s,TAIL=nil]] -> 'thinks' | 'believes'
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=s,TAIL=nil]] -> 'think' | 'believe'
    
    
    V[TENSE=pres, NUM=sing, SUBCAT=[HEAD=np,TAIL=nil]] ->'serves' | 'drinks' 
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=np,TAIL=nil]] ->'serve' | 'drink' 
    
    V[TENSE=pres, NUM=sing, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walks' | 'teaches' 
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walk' | 'teach' 
    
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drink' | 'wear' | 'serve' | 'like'
    V[TENSE=pres, NUM=sing, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drinks' | 'wears' | 'serves' | 'likes'
    
    ######### primary & secondary ########
    V[TENSE=pres, NUM=sing, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serves'
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serve'
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=nom, TAIL=[HEAD=np,TAIL=nil]]] -> 'serve'
    V[TENSE=pres, NUM=plur, SUBCAT=[HEAD=s, TAIL=[HEAD=np,TAIL=nil]]] -> 'think' | 'believe'
    
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
    PROP_N[NUM=sing] -> 'Homer' | 'Bart' | 'Lisa'
    N[NUM=sing] -> 'milk'   | 'salad'   | 'midnight' | 'kitchen' | 'table' | 'robot' | 'sky' | 'plane'
    N[NUM=plur] -> 'shoes'  | 'tables'  | 'robots' | 'trains' | 'flights' | 'people'
    N -> 'milk' | 'morning' | 'midnight' | 'Edinburgh' | 'London' | '8' |'9' | '10' | 'breakfast'
    
    ################## Modal ##################
    MOD -> 'may'
    
    ######### Predeterminers ##########
    PRE_DET -> 'all' | 'most'
    
    ################ Determiner ###############
    DET[NUM=sing] -> 'a' | 'the' | 'that'
    DET[NUM=plur] -> 'the' | 'these' | 'those'
    
    ################ Conjunction ##############
    CONJ -> 'and'
    
    ############ Adverb & Adjective ############
    ADJ -> 'blue' | 'healthy' | 'green' | 'same'
    ADV -> 'always' | 'never' | 'intensely'
    
    ############## Preposition ##################
    P -> 'in' | 'before' | 'when' | 'on' | 'beyond' | 'from' | 'to' | 'at'
    
    ######## Auxiliary #################
    AUX[FORM=base]               -> 'do'
    AUX[FORM=vbz]                -> 'does'
    AUX[FORM=pret]               -> 'did'
    AUX[FORM=pastpart, NUM=sing] -> 'has'
    AUX[FORM=pastpart, NUM=plur] -> 'have'
    
    VTB[NUM=sing] -> 'is'
    VTB[NUM=plur] -> 'are'
    
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

did the plane leave
whom does Homer serve salad
whom do Homer and Lisa serve
what salad does Bart think Homer serves Lisa
all the morning trains from Edinburgh to London leave before 10
most flights that serve breakfast leave at 9
"""
'''
    the people who live in the house are friendly
    Lisa claims that Bart always leaves before 8
'''
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
