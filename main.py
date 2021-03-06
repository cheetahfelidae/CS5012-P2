from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

ugrammar = FeatureGrammar.fromstring("""\
    ######################################################################################################
    ################################################# SENTENCE ###########################################
    ######################################################################################################
    S[NUM=?n] -> NP[NUM=?n] VP[NUM=?n] | PP S[NUM=?n]
    S[NUM=?n] -> VP[NUM=?n]
    S[NUM=?n] -> WH_NP AUX[FORM=?f, NUM=?n] NP[NUM=?n] VP[NUM=?n]
    S[NUM=?n] -> WH_NP VP[NUM=?n]
    S[NUM=?n] ->       AUX[FORM=?f, NUM=?n] NP[NUM=?n] VP[NUM=?n]
    
    ######## WH-Question ###########
    WH_NP -> WH | WH ARG[CAT=?arg] 
    WH    -> 'when' | 'what' | 'where' | 'whom'
    
    ######################################################################################################
    ############################################## NOUN PHRASE ###########################################
    ######################################################################################################
    NP[NUM=?n]   -> PRE_DET NP[NUM=plur] | PROP_N[NUM=?n] | PROP_N[NUM=?n] GER_P | DET[NUM=?n] NOM[NUM=?n] | NOM[NUM=?n]
    NP[NUM=plur] -> NP CONJ NP
    
    NOM[NUM=?n]  -> ADJ_P NOM[NUM=?n] | QUAN NOM[NUM=plur] | NOM[NUM=?n] REL_CL[NUM=?n] | N[NUM=?n] | GER_P | NOM[NUM=?n] N[NUM=?n] | NOM[NUM=?n] PP
    
    ########## Predeterminer ##########
    PRE_DET -> 'all' | 'most'
    
    ########## Quantifier ##########
    QUAN -> 'some' | 'many'
    
    ############# Pronoun #############
    PROP_N[NUM=sing] -> 'Homer' | 'Bart' | 'Lisa'
    
    ######## Relative Clause ##########
    REL_CL[NUM=?n] -> S[NUM=?n] | COMP S[NUM=?n] | COMP VP[NUM=?n]
    COMP   -> 'that' | 'who'
    
    ############# Gerund ##############
    GER_P -> GER NP | GER NOM
    GER   -> V[FORM=prespart, SUBCAT=nil]
    
    ########### Noun Lexicon ##########
    N[NUM=sing] -> 'salad'  | 'midnight' | 'kitchen' | 'table'   | 'plane'  | 'house' | 'milk' | 'morning' | 'midnight' | 'Edinburgh' | 'London' | '8' |'9' | '10' | 'breakfast'
    N[NUM=plur] -> 'shoes'  | 'tables'   | 'trains'  | 'flights' | 'people' | 'airlines'
    
    ######################################################################################################
    ############################################## VERB PHRASE ###########################################
    ######################################################################################################
    VP[SUBCAT=?rest, NUM=?n] -> VP[TENSE=?t, NUM=?n, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg] | V[NUM=?n, SUBCAT=?rest]
    VP[SUBCAT=?rest, NUM=?n] -> ADV_P V[NUM=?n, SUBCAT=?rest] | V[NUM=?n, SUBCAT=?rest] ADV_P 
    VP[SUBCAT=?rest, NUM=?n] -> MODP VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest, NUM=?n] -> VTB[NUM=?n] VP[SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest, NUM=?n] -> VTB[NUM=?n] VP[SUBCAT=?rest, NUM=?n]
    VP[SUBCAT=?rest, NUM=?n] -> VP[FORM=pres, NUM=plur, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=nil, NUM=?n]   -> VTB[NUM=?n] ADJ_P
    
    MODP -> MOD AUX[FORM=?f, NUM=plur] |  MOD 'not' AUX[FORM=?f, NUM=plur]
    
    PP -> P NP | P S | P NOM
    
    ARG[CAT=np] -> NP
    ARG[CAT=pp] -> PP
    ARG[CAT=nom] -> NOM
    ARG[CAT=cl] -> REL_CL
    
    #########################################################################
    ############################## PRESENT ##################################
    #########################################################################
    ############## Intransitive ###############
    V[FORM=pres, NUM=sing, SUBCAT=nil]-> 'laughs' | 'smiles' | 'walks' | 'serves' | 'drinks' | 'leaves' 
    V[FORM=pres, NUM=plur, SUBCAT=nil] -> 'laugh' | 'smile' | 'walk' | 'serve' |'drink' | 'leave'
    V[FORM=pres, NUM=sing, SUBCAT=[HEAD=pp, TAIL=nil]] -> 'leaves' | 'lives' | 'flies'
    V[FORM=pres, NUM=plur, SUBCAT=[HEAD=pp, TAIL=nil]] -> 'leave'  | 'live' | 'fly'
    
    ############## Transitive ################
    V[FORM=pres, NUM=sing, SUBCAT=[HEAD=cl,TAIL=nil]] -> 'thinks' | 'believes'
    V[FORM=pres, NUM=plur, SUBCAT=[HEAD=cl,TAIL=nil]] -> 'think'  | 'believe'
    
    V[FORM=pres, NUM=sing, SUBCAT=[HEAD=np,TAIL=nil]] ->'serves' | 'drinks' 
    V[FORM=pres, NUM=plur, SUBCAT=[HEAD=np,TAIL=nil]] ->'serve'  | 'drink' 
    
    V[FORM=pres, NUM=sing, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walks' 
    V[FORM=pres, NUM=plur, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walk' 
    
    V[FORM=pres, NUM=plur, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drink' | 'wear' | 'serve' | 'like'
    V[FORM=pres, NUM=sing, SUBCAT=[HEAD=nom,TAIL=nil]] ->'drinks' | 'wears' | 'serves' | 'likes'
    
    #########################################################################
    ################################ Past ###################################
    #########################################################################
    
    ############## Intransitive ###############
    V[FORM=past, SUBCAT=nil] -> 'laughed' | 'smiled' | 'walked'
    
    ############### Transitive ################
    V[FORM=past,     SUBCAT=[HEAD=np, TAIL=nil]] -> 'drank' | 'wore' | 'served'
    V[FORM=past,     SUBCAT=[HEAD=nom,TAIL=nil]] -> 'drank' | 'wore' | 'served'
    V[FORM=pastpart, SUBCAT=[HEAD=np, TAIL=nil]] -> 'drunk' | 'worn' | 'served' | 'seen'
    V[FORM=pastpart, SUBCAT=[HEAD=nom,TAIL=nil]] -> 'drunk' | 'worn' | 'served' | 'seen'
    
    #########################################################################
    ############################## PRESENT CONT #############################
    #########################################################################
    V[FORM=prespart, SUBCAT=[HEAD=nom, TAIL=nil]]   -> 'drinking' | 'wearing'  | 'using' | 'fighting'
    V[FORM=prespart, SUBCAT=[HEAD=np,  TAIL=nil]]   -> 'drinking' | 'wearing'  | 'using' | 'fighting'
    V[FORM=prespart, SUBCAT=[HEAD=pp,  TAIL=nil]]   -> 'drinking' | 'fighting' | 'walking'
    
    #########################################################################
    ################################## Gerund ###############################
    #########################################################################
    V[FORM=prespart, SUBCAT=nil] -> 'drinking' | 'smiling' | 'wearing' | 'crying' | 'flying'
    
    #########################################################################
    ################################## Clause ###############################
    #########################################################################
    V[FORM=base,      SUBCAT=[HEAD=cl, TAIL=nil]]    -> 'say'    | 'claim'
    V[FORM=pres,      SUBCAT=[HEAD=cl, TAIL=nil]]    -> 'says'   | 'claims'
    V[FORM=vbz,       SUBCAT=[HEAD=cl, TAIL=nil]]    -> 'said'   | 'claimed'
    V[FORM=pastpart,  SUBCAT=[HEAD=cl, TAIL=nil]]    -> 'said'   | 'claimed'
    V[FORM=prespart,  SUBCAT=[HEAD=cl, TAIL=nil]]    -> 'saying' | 'claiming'
    
    ################# Verb To Be ###############
    VTB[NUM=sing] -> 'is'
    VTB[NUM=plur] -> 'are'
    
    ################## Modal ##################
    MOD -> 'may'
    
    ################ Determiner ###############
    DET[NUM=sing] -> 'a'   | 'the'   | 'that'
    DET[NUM=plur] -> 'the' | 'these' | 'those'
    
    ################ Conjunction ##############
    CONJ -> 'and'
    
    ################# Adjective ###############
    ADJ_P -> ADJ | ADJ ADJ_P
    ADJ   -> 'blue' | 'healthy' | 'green' | 'same' | 'friendly'
    
    ################# Adverb ##################
    ADV_P -> ADV | ADV ADV_P
    ADV   -> 'always' | 'never' | 'intensely'
    
    ############## Preposition ################
    P -> 'in' | 'before' | 'after' | 'when' | 'on' | 'beyond' | 'from' | 'to' | 'at'
    
    ######## Auxiliary #################
    AUX[FORM=base, NUM=plur]     -> 'do'
    AUX[FORM=vbz, NUM=sing]      -> 'does'
    AUX[FORM=pret]               -> 'did'
    AUX[FORM=pastpart, NUM=sing] -> 'has'
    AUX[FORM=pastpart, NUM=plur] -> 'have'
    
   
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

did the plane leave
whom does Homer serve salad
all the morning trains from Edinburgh to London leave before 10
most flights that serve breakfast leave at 9
some flights leave before 8
these people who live in the house are friendly
Lisa claims that Bart always leaves before 8
what airlines fly from Edinburgh to London

Bart laugh
when do Homer drinks milk
Bart laughs the kitchen

does the trains leave
Lisa likes drink milk
Lisa and Bart likes drinking milk
the morning flights from Edinburgh leave milk

many flights that serves breakfast leave after 10

Bart laughs in the kitchen
Bart serves
milk are healthy
"""
sents = text.splitlines()
for sent in sents:
    parses = uparser.parse(sent.split())
    print(sent + ":")
    for tree in parses:
        print(tree)
    print("")
