from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    ###################################################################################### 
    ################################### Sentence #########################################
    ######################################################################################
    S -> NP[NUM=?n] VP[NUM=?n] 
    S -> WH AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP | WH NP[NUM=?n] AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP | WH NP[NUM=?n] VP S
    S ->    AUX[FORM=?t, NUM=?n] NP[NUM=?n] VP
    
    ######### WH-questions ##########
    WH -> 'what' | 'when' | 'where' | 'why' | 'who' | 'whom'
    
    ######################################################################################
    ################################### Noun Phrase ######################################
    ######################################################################################
    NP[NUM=?n]   -> PRE_DET NP[NUM=?n]| DET[NUM=?n] NOM | NOM
    NP[NUM=plur] -> PROP_N[NUM=?n] CONJ NP[NUM=?n]
    
    ######### Predeterminers ##########
    PRE_DET       -> 'all' | 'most'
    
    ######### Determiners #############
    DET[NUM=sing] -> 'a' | 'that'
    DET[NUM=plur] -> 'these'
    DET -> 'the'
    
    ######### Adjective ###############
    ADJ -> 'blue' | 'healthy' | 'green' | 'friendly'
    
    ######### Nominal #################
    NOM -> NOM PP | NOM REL_CL | NOM GER_P | NOM N[NUM=?n]
    NOM -> ADJ NOM | PROP_N[NUM=?n] | N[NUM=?n] | GER_P
    
    ######## Pronouns ##################
    PROP_N[NUM=sing]-> 'Bart' | 'Homer' | 'Lisa'
    
    ######## Nouns #####################
    N[NUM=sing] -> 'shoe'   | 'kitchen'     | 'table'   | 'salad' | 'plane'  | 'flight' | 'train'  | 'house' | 'person'
    N[NUM=plur] -> 'shoes'  | 'kitchens'    | 'tables'  | 'salad' | 'planes' | 'flights'| 'trains' | 'houses'| 'people'
    N -> 'milk' | 'morning' | 'midnight' | 'Edinburgh' | 'London' | '8' |'9' | '10' | 'breakfast'
    
    ######### Gerund Phrase ############
    GER_P -> GER PP | GER
    GER -> V[SUBCAT=intrans,FORM=prespart] | V[SUBCAT=trans, FORM=prespart] NP
    
    ######### Preposition Phrase #######
    PP  ->  P NP
    P   -> 'in' | 'on' | 'at' | 'before' | 'after' | 'from' | 'to'
    
    ######## Relative Clause ###########
    REL_CL -> REL_P VP | 'that' S
    REL_P  -> 'that' | 'who'
    
    ######## Conjunction ###############
    CONJ -> 'and'
    
    ######## Adverb ####################
    ADV -> 'always' | 'never'
    
    ######## Auxiliary #################
    AUX[FORM=base]               -> 'do'
    AUX[FORM=vbz]                -> 'does'
    AUX[FORM=pret]               -> 'did' 
    AUX[FORM=pastpart, NUM=sing] -> 'has'
    AUX[FORM=pastpart, NUM=plur] -> 'have'
    
    ######## Modal ######################
    MODP[NUM=plur] -> MOD AUX[NUM=plur] | MOD 'not' AUX[NUM=plur]
    MOD -> 'may'
    
    ######################################################################################
    ################################### Verb #############################################
    ######################################################################################
    VP[FORM=?t, NUM=?n] -> ADV VP[FORM=?t, NUM=?n] | MODP[NUM=plur] VP[FORM=?t, NUM=plur]
    VP[FORM=?t, NUM=?n] -> V[SUBCAT=intrans, FORM=?t] | V[SUBCAT=intrans,FORM=?t] PP
    VP[FORM=?t, NUM=?n] -> V[SUBCAT=trans, FORM=?t] NP | V[SUBCAT=trans, FORM=?t] NP NP | V[SUBCAT=trans, FORM=?t] S 
    VP[FORM=?t, NUM=?n] -> V[SUBCAT=vtb, FORM=?t, NUM=?n] ADJ
    VP[FORM=?t, NUM=?n] -> V[SUBCAT=clause, TENSE=?t] REL_CL
    
    ######## Verb To Be ################
    V[SUBCAT=vtb, FORM=base, NUM=plur] -> 'are'
    V[SUBCAT=vtb, FORM=base, NUM=sing] -> 'is' | 'am'
    V[SUBCAT=vtb, FORM=vbz, NUM=plur]  -> 'were'
    V[SUBCAT=vtb, FORM=vbz, NUM=sing]  -> 'was'
    V[SUBCAT=vtb, FORM=pret]           -> 'been'
    V[SUBCAT=vtb, FORM=prespart]       -> 'being'
    
    ######## Intransitive Verb #########
    V[SUBCAT=intrans, FORM=base]       -> 'drink'      | 'serve'   | 'laugh'    | 'leave'  | 'live'
    V[SUBCAT=intrans, FORM=vbz]        -> 'drinks'     | 'serves'  | 'laughs'   | 'leaves' | 'lives'    
    V[SUBCAT=intrans, FORM=pret]       -> 'drank'      | 'served'  | 'laughed'  | 'left'   | 'lived'
    V[SUBCAT=intrans, FORM=pastpart]   -> 'drunk'      | 'served'  | 'laughed'  | 'left'   | 'lived'
    V[SUBCAT=intrans, FORM=prespart]   -> 'drinking'   | 'serving' | 'laughing' | 'leaving'| 'living'
    
    ######## Transitive Verb ###########
    V[SUBCAT=trans, FORM=base]         -> 'drink'      | 'wear'    | 'serve'    | 'think'   | 'like'  | 'see'
    V[SUBCAT=trans, FORM=vbz]          -> 'drinks'     | 'wears'   | 'serves'   | 'thinks'  | 'likes' | 'sees'
    V[SUBCAT=trans, FORM=pret]         -> 'drank'      | 'wore'    | 'served'   | 'thought' | 'liked' | 'saw'
    V[SUBCAT=trans, FORM=pastpart]     -> 'drunk'      | 'worn'    | 'served'   | 'thought' | 'liked' | 'seen'
    V[SUBCAT=trans, FORM=prespart]     -> 'drinking'   | 'wearing' | 'serving'  | 'thinking'| 'liking'| 'seeing'
    
    ######## Clause ####################
    V[SUBCAT=clause, TENSE=base]        -> 'say'    | 'claim'
    V[SUBCAT=clause, TENSE=base]        -> 'says'   | 'claims'
    V[SUBCAT=clause, TENSE=vbz]         -> 'said'   | 'claimed'
    V[SUBCAT=clause, TENSE=pastpart]    -> 'said'   | 'claimed'
    V[SUBCAT=clause, TENSE=prespart]    -> 'saying' | 'claiming'
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
most flights that serve breakfast leave at 9
the people who live in the house are friendly
Lisa claims that Bart always leaves before 8
"""
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
