|     | SMBOP: |                      | Semi-autoregressive |     |     |     | Bottom-up |                     | Semantic |     | Parsing |     |     |
| --- | ------ | -------------------- | ------------------- | --- | --- | --- | --------- | ------------------- | -------- | --- | ------- | --- | --- |
|     |        |                      | OhadRubin           |     |     |     |           | JonathanBerant      |          |     |         |     |     |
|     |        | TelAvivUniversity    |                     |     |     |     |           | TelAvivUniversity   |          |     |         |     |     |
|     |        | ohadr@mail.tau.ac.il |                     |     |     |     |           | AllenInstituteforAI |          |     |         |     |     |
joberant@cs.tau.ac.il
|     |     |     | Abstract |     |     |     | top-downmanner(YinandNeubig,2017;Krishna- |     |     |     |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
murthyetal.,2017;Rabinovichetal.,2017).
Thede-factostandarddecodingmethodforse-
Bottom-updecodinginsemanticparsinghasre-
manticparsinginrecentyearshasbeentoau-
|                |     |        |     |          |             |     | ceived | little attention |     | (Cheng | et  | al., 2019; | Odena |
| -------------- | --- | ------ | --- | -------- | ----------- | --- | ------ | ---------------- | --- | ------ | --- | ---------- | ----- |
| toregressively |     | decode | the | abstract | syntax tree |     |        |                  |     |        |     |            |       |
ofthetargetprogramusingatop-downdepth- etal.,2020). Inthiswork,weproposeabottom-up
first traversal. In this work, we propose an semantic parser, and demonstrate that equipped
alternative approach: a Semi-autoregressive with recent developments in Transformer-based
| Bottom-up |          | Parser                            | (SMBOP)        | that | constructs |     |                   |         |                               |                |            |              |             |
| --------- | -------- | --------------------------------- | -------------- | ---- | ---------- | --- | ----------------- | ------- | ----------------------------- | -------------- | ---------- | ------------ | ----------- |
|           |          |                                   |                |      |            |     | (Vaswani          | et al., | 2017)                         | architectures, |            | it           | offers sev- |
| at        | decoding | step                              | t the top-K    |      | sub-trees  | of  |                   |         |                               |                |            |              |             |
|           |          |                                   |                |      |            |     | eral advantages.  |         | From                          | an             | efficiency | perspective, |             |
| height≤   |          | t. Ourparserenjoysseveralbenefits |                |      |            |     |                   |         |                               |                |            |              |             |
|           |          |                                   |                |      |            |     | bottom-up         | parsing |                               | can naturally  |            | be           | done semi-  |
| compared  |          | to top-down                       | autoregressive |      | parsing.   |     |                   |         |                               |                |            |              |             |
|           |          |                                   |                |      |            |     | autoregressively: |         | ateachdecodingstept,theparser |                |            |              |             |
| From      | an       | efficiency                        | perspective,   |      | bottom-up  |     |                   |         |                               |                |            |              |             |
parsingallowstodecodeallsub-treesofacer- generatesinparallelthetop-K programsub-trees
|      |        |              |         |     |             |     | ofdepth≤ | t(akintobeamsearch). |     |     |     |             |     |
| ---- | ------ | ------------ | ------- | --- | ----------- | --- | -------- | -------------------- | --- | --- | --- | ----------- | --- |
| tain | height | in parallel, | leading | to  | logarithmic |     |          |                      |     |     |     | Thisleadsto |     |
runtime complexity rather than linear. From runtimecomplexitythatislogarithmicinthetree
a modeling perspective, a bottom-up parser size,ratherthanlinear,contributingtotherocket-
| learns | representations |     | for | meaningful | seman- |     |     |     |     |     |     |     |     |
| ------ | --------------- | --- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
inginterestinefficientandgreenerartificialintelli-
| tic                  | sub-programs |     | at each step, | rather | than     | for |                                        |     |     |     |     |     |      |
| -------------------- | ------------ | --- | ------------- | ------ | -------- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ---- |
|                      |              |     |               |        |          |     | gencetechnologies(Schwartzetal.,2020). |     |     |     |     |     | From |
| semantically-vacuous |              |     | partial       | trees. | We apply |     |                                        |     |     |     |     |     |      |
amodelingperspective,neuralbottom-upparsing
| SMBOP    |     | on SPIDER, | a challenging |     | zero-shot |     |          |         |                 |     |     |     |            |
| -------- | --- | ---------- | ------------- | --- | --------- | --- | -------- | ------- | --------------- | --- | --- | --- | ---------- |
|          |     |            |               |     |           |     | provides | learned | representations |     |     | for | meaningful |
| semantic |     | parsing    | benchmark,    | and | show that |     |          |         |                 |     |     |     |            |
(andexecutable)sub-programs,whicharesub-trees
| SMBOP |     | leadstoa2.2xspeed-upindecoding |     |     |     |     |     |     |     |     |     |     |     |
| ----- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
timeanda∼5xspeed-upintrainingtime,com- computedduringthesearchprocedure,incontrast
paredtoasemanticparserthatusesautoregres- totop-downparsing,wherehiddenstatesrepresent
| sive | decoding. | SMBOP | obtains |     | 71.1 denota- |     |     |     |     |     |     |     |     |
| ---- | --------- | ----- | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
partialtreeswithoutclearsemantics.
| tion                                     | accuracy | on                 | SPIDER, | establishing | a new  |     |             |               |           |          |        |                 |           |
| ---------------------------------------- | -------- | ------------------ | ------- | ------------ | ------ | --- | ----------- | ------------- | --------- | -------- | ------ | --------------- | --------- |
|                                          |          |                    |         |              |        |     | Figure      | 1 illustrates |           | a single |        | decoding        | step of   |
| state-of-the-art,                        |          | and69.5exactmatch, |         |              | compa- |     |             |               |           |          |        |                 |           |
|                                          |          |                    |         |              |        |     | our parser. | Given         | a         | beam     | Z with | K               | = 4 trees |
| rabletothe69.6exactmatchoftheautoregres- |          |                    |         |              |        |     |             |               |           |          | t      |                 |           |
|                                          |          |                    |         |              |        |     | of height   | t (blue       | vectors), |          | we use | cross-attention |           |
siveRAT-SQL+GRAPPA.
|     |     |     |     |     |     |     | to contextualize |     | the | trees | with information |     | from |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ----- | ---------------- | --- | ---- |
1 Introduction the input question (orange). Then, we score the
|     |     |     |     |     |     |     | frontier, | that | is, the | set of | all trees | of  | height t + |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---- | ------- | ------ | --------- | --- | ---------- |
Semanticparsing,thetaskofmappingnaturallan-
|     |     |     |     |     |     |     | 1 that can | be  | constructed |     | using | a grammar | from |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | ----- | --------- | ---- |
guageutterancesintoprograms(ZelleandMooney,
|     |     |     |     |     |     |     | the current | beam, | and | the | top-K | trees | are kept |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | --- | ----- | ----- | -------- |
1996;ZettlemoyerandCollins,2005;Clarkeetal.;
|     |     |     |     |     |     |     | (purple). | Last,arepresentationforeachofthenew |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------------------------------- | --- | --- | --- | --- | --- |
Liangetal.,2011),hasconvergedinrecentyearson
K treesisgeneratedandplacedinthenewbeam
| astandardencoder-decoderarchitecture. |     |     |     |     | Recently, |     |           |     |          |        |     |        |         |
| ------------------------------------- | --- | --- | --- | --- | --------- | --- | --------- | --- | -------- | ------ | --- | ------ | ------- |
|                                       |     |     |     |     |           |     | Z . After | T   | decoding | steps, | the | parser | returns |
t+1
meaningfuladvancesemergedontheencoderside,
|                                             |     |     |     |     |     |     | thehighest-scoringtreeinZ |     |         |     | thatcorrespondsto |      |          |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | ------- | --- | ----------------- | ---- | -------- |
| includingdevelopmentsinTransformer-basedar- |     |     |     |     |     |     |                           |     |         |     | T                 |      |          |
|                                             |     |     |     |     |     |     | a full program.           |     | Because |     | we have           | gold | trees at |
chitectures(Wangetal.,2020a)andnewpretrain-
|     |     |     |     |     |     |     | training | time, | the entire | model |     | is trained | jointly |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ---------- | ----- | --- | ---------- | ------- |
ingtechniques(Yinetal.,2020;Herzigetal.,2020;
usingmaximumlikelihood.
Yuetal.,2020;Dengetal.,2020;Shietal.,2021).
|     |     |     |     |     |     |     | We  | evaluate | our | model, | SMBOP1 |     | (SeMi- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------ | ------ | --- | ------ |
Conversely,thedecoderhasremainedroughlycon-
autoregressiveBottom-upsemanticParser),onSPI-
| stant for | years, | where | the abstract |     | syntax tree | of  |     |     |     |     |     |     |     |
| --------- | ------ | ----- | ------------ | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
thetargetprogramisautoregressivelydecodedina
1Rhymeswith‘MMMBop’.
311
Proceedingsofthe2021ConferenceoftheNorthAmericanChapterofthe
AssociationforComputationalLinguistics:HumanLanguageTechnologies,pages311–324
June6–11,2021.©2021AssociationforComputationalLinguistics

name actor
|     |     |     |     |     | actor 60 age | 60  |     |     |     |
| --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- |
Represent-beam
Prune frontier
...
Score-frontier
Cross Attention
...
|     |     |                                       |     | name | actor | age |     |     |     |
| --- | --- | ------------------------------------- | --- | ---- | ----- | --- | --- | --- | --- |
|     |     | What are the names of actors over 60? |     |      |       |     | 60  |     |     |
Figure1: AnoverviewofthedecodingprocedureofSMBOP.Z isisthebeamatstept,Z (cid:48) isthecontextualized
|     |     |     |     |     | t   |     |     | t   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
beamaftercross-attention,F isthefrontier(κ,σ,≥arelogicaloperationsappliedontrees,asexplainedbelow),
t+1
F(cid:48)
istheprunedfrontier, andZ t+1 isthenewbeam. Atthetopweseethenewtreescreatedinthisstep. For
t+1
t=0(depictedhere),thebeamcontainsthepredictedschemaconstantsandDBvalues.
DER (Yu et al., 2018), a challenging zero-shot (x,S)tothecorrectSQLqueryy. ADBschemaS
text-to-SQL dataset. We implement the RAT- includes: (a)asetoftables,(b)asetofcolumnsfor
SQL+GRAPPAencoder(Yuetal.,2020),currently eachtable,and(c)asetofforeignkey-primarykey
thebestmodelon SPIDER,andreplacetheautore- column pairs describing relations between table
gressivedecoderwiththesemi-autoregressive SM- columns. Schematablesandcolumnsaretermed
BOP. SMBOP obtains an exact match accuracy schemaconstants,anddenotedbyS.
| of 69.5, comparable |     | to the autoregressive |     | RAT- |     |     |     |     |     |
| ------------------- | --- | --------------------- | --- | ---- | --- | --- | --- | --- | --- |
SQL+GRAPPAat69.6exactmatch,andtocurrent RAT-SQLencoder Thisworkisfocusedonde-
state-of-the-art at 69.8 exact match (Zhao et al., coding,andthusweimplementthestate-of-the-art
| 2021),whichappliesadditionalpretraining. |     |     |     | More- |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
RAT-SQLencoder(Wangetal.,2020b),ontopof
over,SMBOP substantiallyimprovesstate-of-the- GRAPPA (Yu et al., 2020), a pre-trained encoder
artindenotationaccuracy,improvingperformance forsemanticparsing. Wenowbrieflyreviewthis
| from 68.3 | → 71.1. | Importantly, | compared | to au- |     |     |     |     |     |
| --------- | ------- | ------------ | -------- | ------ | --- | --- | --- | --- | --- |
encoderforcompleteness.
toregressivesemanticparsing,weobserveanaver-
|     |     |     |     |     | The | RAT-SQL | encoder is | based on | two main |
| --- | --- | --- | --- | --- | --- | ------- | ---------- | -------- | -------- |
agespeed-upof2.2xindecodingtime,wherefor
ideas. First,itprovidesajointcontextualizedrep-
longSQLqueries,speed-upisbetween5x-6x,and
|     |     |     |     |     | resentation | of the | utterance and | schema. | Specif- |
| --- | --- | --- | --- | --- | ----------- | ------ | ------------- | ------- | ------- |
atrainingspeed-upof∼5x.2
|     |     |     |     |     | ically, | the utterance | x is concatenated |     | to a lin- |
| --- | --- | --- | --- | --- | ------- | ------------- | ----------------- | --- | --------- |
earizedformoftheschemaS,andtheyarepassed
2 Background
|     |     |     |     |     | through | a stack of | Transformer | (Vaswani | et al., |
| --- | --- | --- | --- | --- | ------- | ---------- | ----------- | -------- | ------- |
Problem definition We focus in this work on 2017)layers. Then,tokensthatcorrespondtoasin-
text-to-SQLsemanticparsing. Givenatrainingset gleschemaconstantareaggregated,whichresults
{(x(i),y(i),S(i))}N x(i) in a final contextualized representation (x,s) =
|     |     | , where | is an | utterance, |     |     |     |     |     |
| --- | --- | ------- | ----- | ---------- | --- | --- | --- | --- | --- |
i=1
y(i) isitstranslationtoaSQLquery,andS(i) isthe (x ,...,x ,s ,...,s ),wheres isavectorrep-
|     |     |     |     |     | 1   | |x| 1 | |s| | i   |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
schemaofthetargetdatabase(DB),ourgoalisto resentingasingleschemaconstant. Thiscontextu-
learnamodelthatmapsnewquestion-schemapairs alizationofxandS leadstobetterrepresentation
andalignmentbetweentheutteranceandschema.
| 2Our code | is available | at https://github.com/ |     |     |         |         |                       |     |       |
| --------- | ------------ | ---------------------- | --- | --- | ------- | ------- | --------------------- | --- | ----- |
|           |              |                        |     |     | Second, | RAT-SQL | uses relational-aware |     | self- |
OhadRubin/SmBop
312

attention(Shawetal.,2018)toencodethestructure Algorithm1:SMBOP
oftheschemaandotherpriorknowledgeonrela-
1 input:utterancex,schemaS
tionsbetweenencodedtokens. Specifically,given 2 x,s←Encode RAT (x,S)
asequenceoftokenrepresentations(u ,...,u ), 3 Z 0 ←Top-KschemaconstantsandDBvalues
1 |u| 4 fort←0...T −1do
relational-aware self-attention computes a scalar 5 Z t (cid:48) ←Attention(Z t ,x,x)
similarityscorebetweenpairsoftokenrepresenta- 6 F t+1 ←Score-frontier(Z t (cid:48))
tionse ij ∝ u i W Q (u j W K +rK ij ). Thisisidentical 7 F t (cid:48) +1 ←argmax K (F t+1 )
to standard self-attention (W and W are the 8 Z t+1 ←Represent-beam(Z t ,F t (cid:48) +1 )
Q K
queryandkeyparametermatrices),exceptforthe 9 returnargmax z (Z T )
term rK, which is an embedding that represents
ij
arelationbetweenu andu fromaclosedsetof
i j
possible relations. For example, if both tokens videsaradicallydifferentapproachfordecodingin
correspond to schema tables, an embedding will semanticparsing.
represent whether there is a primary-foreign key
relationbetweenthetables. Ifoneofthetokensis
3 The SMBOP parser
an utterance word and another is a table column,
arelationwilldenoteifthereisastringmatchbe-
Wefirstprovideahigh-leveloverviewofSMBOP
tween them. The same principle is also applied
(see Algorithm 1 and Figure 1). As explained in
forrepresentingtheself-attentionvalues,wherean-
§2, we encode the utterance and schema with a
otherrelationembeddingmatrixisused. Werefer
RAT-SQLencoder. Weinitializethebeam(line3)
thereadertotheRAT-SQLpaperfordetails.
withtheK highestscoringtreesofheight0,which
Overall,RAT-SQLjointlyencodestheutterance,
includeeitherschemaconstantsorDBvalues. All
schema,thestructureoftheschemaandalignments
treesarescoredindependentlyandinparallel,ina
between the utterance and schema, and leads to
procedureformallydefinedin§3.3.
state-of-the-artresultsintext-to-SQLparsing.
Next, we start the search procedure. At every
RAT-SQL layers are typically stacked on top
step t, attention is used to contextualize the trees
of a pre-trained language model, such as BERT
with information from input question representa-
(Devlinetal.,2019). Inthiswork,weuseGRAPPA
tion (line 5). This representation is used to score
(Yu et al., 2020), a recent pre-trained model that
every tree on the frontier: the set of sub-trees of
hasobtainedstate-of-the-artresultsintext-to-SQL
depth ≤ t+1 that can be constructed from sub-
parsing. GRAPPAisbasedonROBERTA(Liuetal.,
treesonthebeamwithdepth≤ t(lines6-7). After
2019), but is further fine-tuned on synthetically
choosingthetop-K treesforstept+1,wecompute
generatedutterance-querypairsusinganobjective
anewrepresentationforthem(line8). Finally,we
foraligningtheutteranceandquery.
returnthetop-scoringtreefromthefinaldecoding
step, T. Steps in our model operate on tree rep-
Autoregressive top-down decoding The pre-
resentations independently, and thus each step is
vailing method for decoding in semantic parsing
efficientlyparallelized.
hasbeengrammar-basedautoregressivetop-down
decoding(YinandNeubig,2017;Krishnamurthy SMBOP resemblesbeamsearchasineachstep
etal.,2017;Rabinovichetal.,2017),whichguar- itholdsthetop-K treesofafixedheight. Itisalso
antees decoding of syntactically valid programs. relatedto(pruned)chartparsing,sincetreesatstep
Specifically,thetargetprogramisrepresentedasan t+1arecomputedfromtreesthatwerefoundat
abstractsyntaxtreeunderthegrammarofthefor- stept. Thisisunlikesequence-to-sequencemodels
mallanguage,andlinearizedtoasequenceofrules whereitemsonthebeamarecompetinghypotheses
(oractions)usingatop-downdepth-firsttraversal. withoutanyinteraction.
Once the program is represented as a sequence, Wenowprovidethedetailsofourparser. First,
it can be decoded using a standard sequence-to- we describe the formal language (§3.1), then we
sequencemodelwithencoderattention(Dongand provide precise details of our model architecture
Lapata,2016),oftencombinedwithbeamsearch. (§3.2)includingbeaminitialization(§3.3, wede-
Wereferthereadertotheaforementionedpapers scribe the training procedure (§3.4), and last, we
forfurtherdetailsongrammar-baseddecoding. discussthepropertiesofSMBOPcomparedtoprior
Wenowturntodescribeourmethod,whichpro- work(§3.5).
313

Operation Notation Input→Output Π Π
SetUnion ∪ R×R→R
SetIntersection ∩ R×R→R name σ κ σ
Setdifference \ R×R→R
Selection σ P ×R→R ≥ actor κ ≥ κ
Cartesianproduct × R×R→R
Projection Π C(cid:48)×R→R age 60 name age 60 actor
And ∧ P ×P →P (a)Unbalancedtree (b)Balancedtree
Or ∨ P ×P →P
Comparison {≤,≥,=,(cid:54)=} C×C →P Figure 2: An unbalanced and balanced relational al-
ConstantUnion (cid:116) C(cid:48)×C(cid:48)→C(cid:48) gebra tree (with the unary KEEP operation) for the
Orderby τ asc/dsc C×R→R utterance “What are the names of actors older than
Groupby γ C×R→R 60?”,wherethecorrespondingSQLqueryisSELECT
Limit λ C×R→R name FROM actor WHERE age ≥ 60.
In/NotIn ∈,(cid:54)∈ C×R→P
Like/NotLike ∼,(cid:54)∼ C×C →P
lationalalgebratreewiththecorrespondingSQL
Aggregation G C →C
agg
Distinct δ C →C query. More examples illustrating the correspon-
Keep κ Any→Any dence between SQL and relational algebra (e.g.,
for the SQL JOIN operation) are in Appendix B.
Table 1: Our relational algebra grammar, along with
Whileourrelationalalgebragrammarcanalsobe
the input and output semantic types of each opera-
tion. P: Predicate, R: Relation, C: schema con- adaptedforstandardtop-downautoregressivepars-
stant or DB value, C(cid:48): A set of constants/values, and ing,weleavethisendeavourforfuturework.
agg∈{sum,max,min,count,avg}.
Tree balancing Conceptually, at each step SM-
BOP shouldgeneratenewtreesofheight≤ t+1
3.1 RepresentationofQueryTrees andkeepthetop-K treescomputedsofar. Inprac-
tice, it is convenient to assume that trees are bal-
Relational algebra Guo et al. (2019) have
anced. Thus, we want the beam at step t to only
shown recently that the mismatch between natu-
havetreesthatareofheightexactlyt(t-hightrees).
rallanguageandSQLleadstoparsingdifficulties.
Toachievethis,weintroduceaunaryKEEPoper-
Therefore,theyproposedSemQL,aformalquery
ationthatdoesnotchangethesemanticsofthesub-
languagewithbetteralignmenttonaturallanguage.
tree it is applied on. Hence, we can always grow
In this work, we follow their intuition, but in-
the height of trees in the beam without changing
stead of SemQL, we use the standard query lan-
theformalquery. Fortraining(whichweelaborate
guagerelationalalgebra(Codd,1970). Relational
onin§3.4),webalanceallrelationalalgebratrees
algebra describes queries as trees, where leaves
inthetrainingsetusingthe KEEP operation,such
(terminals)areschemaconstantsorDBvalues,and
thatthedistancefromtheroottoallleavesisequal.
inner nodes (non-terminals) are operations (see
For example, in Figure 2, two KEEP operations
Table 1). Similar to SemQL, its alignment with
areusedtobalancethecolumnactor.name. Af-
naturallanguageisbetterthanSQL.However,un-
ter tree balancing, all constants and values are at
likeSemQL,itisanexistingquerylanguage,com-
height 0, and the goal of the parser at step t is to
monly used by SQL execution engines for query
generatethegoldsetoft-hightrees.
planning.
Wewriteagrammarforrelationalalgebra,aug- 3.2 ModelArchitecture
mentedwithSQLoperatorsthataremissingfrom
TofullyspecifyAlg.1,weneedtodefinethefol-
relationalalgebra. Wethenimplementatranspiler
lowingcomponents: (a)scoringoftreesonthefron-
thatconvertsSQLqueriestorelationalalgebrafor
tier(lines5-6),(b)representationoftrees(line8),
parsing, and then back from relational algebra to
and(c)representingandscoringofconstantsand
SQLforevaluation. Table1showsthefullgram-
DBvaluesduringbeaminitialization(leaves). We
mar,includingtheinputandoutputsemantictypes
now describe these components. Figure 3 illus-
of all operations. A relation (R) is a tuple (or tu-
trates the scoring and representation of a binary
ples),apredicate(P)isaBooleancondition(eval-
operation.
uating to True or False), a constant (C) is a
schemaconstantorDBvalue,and(C(cid:48))isasetof Scoring with contextualized beams SMBOP
constants/values. Figure 2 shows an example re- maintains at each decoding step a beam Z =
t
314

|     | (t) (t) |          | (t) | (t)    |       | (t) |           |     |     |     |     |     |     |
| --- | ------- | -------- | --- | ------ | ----- | --- | --------- | --- | --- | --- | --- | --- | --- |
| ((z | ,z      | ),...,(z |     | ,z )), | where | z   | is a sym- |     |     |     |     |     |     |
|     | 1 1     |          | K   | K      |       | i   |           |     |     |     |     |     |     |
(t)
| bolicrepresentationofthequerytree,andz |     |     |     |     |     |     | isits |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
i
| correspondingvectorrepresentation. |     |     |     |     |     | Unlikestan- |     |     |     | age | 60  |     |     |
| ---------------------------------- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
dardbeamsearch,treesonourbeamsdonotonly
competewithoneanother,butalsocomposewith
| each | other | (similar | to  | chart | parsing). |     | For exam- |     |     |     |     |     |     |
| ---- | ----- | -------- | --- | ----- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
ple, in Fig. 1, the beam Z 0 contains the column  Transformer(          ,            ,           )     FF B (           ;           ;           ;           )
)
| age | and | the | value 60, | which | compose |     | using the |     |     |     |     |     |     |
| --- | --- | --- | --------- | ----- | ------- | --- | --------- | --- | --- | --- | --- | --- | --- |
≥operatortoformtheage ≥ 60tree. Represent-beam Score-frontier
|          | We contextualize |                  |          | tree   | representations |            | on the    |     |     |     |      |     |     |
| -------- | ---------------- | ---------------- | -------- | ------ | --------------- | ---------- | --------- | --- | --- | --- | ---- | --- | --- |
| beam     | using            | cross-attention. |          |        | Specifically,   |            | we use    |     |     |     |      |     |     |
| standard |                  | attention        | (Vaswani |        | et              | al., 2017) | to give   |     |     |     |      |     |     |
| tree     | representations  |                  |          | access | to the          | input      | question: |     |     | age |   60 |     |     |
Z(cid:48)
|     | ← Attention(Z |     | t ,x,x),wherethetreerepresen- |     |     |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t
|     |     | (t) | (t) |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tations(z ,...,z )arethequeries,andtheinput Figure3:Illustrationofourtreescoringandrepresenta-
|          |     | 1      | K                     |     |     |     |     |                 |     |                                  |     |     |     |
| -------- | --- | ------ | --------------------- | --- | --- | --- | --- | --------------- | --- | -------------------------------- | --- | --- | --- |
| tokens(x |     | ,...,x | )arethekeysandvalues. |     |     |     |     |                 |     |                                  |     |     |     |
|          |     | 1      | |x|                   |     |     |     |     | tionmechanisms. |     | z isthesymbolictree,zisitsvector |     |     |     |
Next, we compute scores for all (t + 1)-high representation,andz(cid:48)itscontextualizedrepresentation.
| trees | on  | the frontier. |     | Trees | can | be generated | by  |     |     |     |     |     |     |
| ----- | --- | ------------- | --- | ----- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
applyingeitheraunary(includingKEEP)operation
contextualizedtrees,representationsarenotcontex-
| u     | ∈ U | or binary    | operation    |        | b ∈    | B on      | beam trees. |                      |                                      |     |          |                     |     |
| ----- | --- | ------------ | ------------ | ------ | ------ | --------- | ----------- | -------------------- | ------------------------------------ | --- | -------- | ------------------- | --- |
|       |     |              |              |        |        |           |             | tualized.            | Weempiricallyfoundthatcontextualized |     |          |                     |     |
| Let   | w   | be a scoring |              | vector | for a  | unary     | operation   |                      |                                      |     |          |                     |     |
|       | u   |              |              |        |        |           |             | tree representations |                                      |     | slightly | reduce performance, |     |
| (such | as  | w κ ,        | w δ , etc.), | let    | w b be | a scoring | vector      |                      |                                      |     |          |                     |     |
possiblyduetooptimizationissues.
| forabinaryoperation(suchasw |     |                                       |     |     |     | ,w  | ,etc.),and |                                           |        |       |        |                |       |
| --------------------------- | --- | ------------------------------------- | --- | --- | --- | --- | ---------- | ----------------------------------------- | ------ | ----- | ------ | -------------- | ----- |
|                             |     |                                       |     |     |     | σ Π |            | WerepresenttreeswithanotherstandardTrans- |        |       |        |                |       |
| letz(cid:48),z(cid:48)      |     | becontextualizedtreerepresentationson |     |     |     |     |            |                                           |        |       |        |                |       |
|                             | i j |                                       |     |     |     |     |            | former                                    | layer. | Let z | be the | representation | for a |
new
| thebeam.                        |          | Wedefineascoringfunctionforfrontier |              |     |        |     |           |                                            |     |                                      |     |                      |     |
| ------------------------------- | -------- | ----------------------------------- | ------------ | --- | ------ | --- | --------- | ------------------------------------------ | --- | ------------------------------------ | --- | -------------------- | --- |
|                                 |          |                                     |              |     |        |     |           | newtree,lete                               |     | (cid:96) beanembeddingforaunaryorbi- |     |                      |     |
| trees,wherethescoreforanewtreez |          |                                     |              |     |        |     | generated |                                            |     |                                      |     |                      |     |
|                                 |          |                                     |              |     |        | new |           | naryoperation,andletz                      |     |                                      | ,z  | benon-contextualized |     |
|                                 |          |                                     |              |     |        |     |           |                                            |     |                                      | i j |                      |     |
| by                              | applying | a                                   | unaryruleuon |     | atreez |     | isdefined |                                            |     |                                      |     |                      |     |
|                                 |          |                                     |              |     |        |     | i         | treerepresentationsfromthebeamweareextend- |     |                                      |     |                      |     |
asfollows:
ing. Wecomputeanewrepresentationasfollows:
|     |     |     |     | w(cid:62) |     | ;z(cid:48) |     |     |     |               |     |                    |     |
| --- | --- | --- | --- | --------- | --- | ---------- | --- | --- | --- | ------------- | --- | ------------------ | --- |
|     |     | s(z | ) = | FF        | ([z | ]),        |     |     |    |               |     |                    |     |
|     |     |     | new | u         | U   | i i        |     |     |     | Transformer(e |     | ,z ) unary(cid:96) |     |
|     |     |     |     |           |     |            |     |     |    |               |     | (cid:96) i         |     |
whereFF isa2-hiddenlayerfeed-forwardlayer z = Transformer(e ,z ,z ) binary(cid:96)
|     |     | U   |     |     |     |     |     | new |     |     | (cid:96) | i j |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |

withreluactivations,and[·;·]denotesconcatena- z i (cid:96) = KEEP
| tion.                           | Similarly |     | the score |     | for a tree | generated | by     |       |         |       |      |            |           |
| ------------------------------- | --------- | --- | --------- | --- | ---------- | --------- | ------ | ----- | ------- | ----- | ---- | ---------- | --------- |
|                                 |           |     |           |     |            |           |        | where | for the | unary | KEEP | operation, | we simply |
| applyingabinaryrulebonthetreesz |           |     |           |     |            |           | ,z is: |       |         |       |      |            |           |
|                                 |           |     |           |     |            | i         | j      |       |         |       |      |            |           |
copytherepresentationfromthepreviousstep.
|     |     | s(z | ) = w(cid:62)FF |     | ([z ;z(cid:48);z | ;z(cid:48)]), |     |        |       |     |            |            |         |
| --- | --- | --- | --------------- | --- | ---------------- | ------------- | --- | ------ | ----- | --- | ---------- | ---------- | ------- |
|     |     | new | b               | B   | i                | i j           | j   |        |       |     |            |            |         |
|     |     |     |                 |     |                  |               |     | Return | value | As  | mentioned, | the parser | returns |
whereFF isanother2-hiddenlayerfeed-forward thehighest-scoringtreeinZ . Moreprecisely,we
|     |     | B   |     |     |     |     |     |     |     |     |     | T   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
layerwithreluactivations. return the highest-scoring returnable tree, where
Weusesemantictypestodetectinvalidruleap- areturnabletreeisatreethathasavalidsemantic
| plications |     | and | fix their | score | to  | s(z | ) = −∞. |                          |     |     |     |     |     |
| ---------- | --- | --- | --------- | ----- | --- | --- | ------- | ------------------------ | --- | --- | --- | --- | --- |
|            |     |     |           |       |     | new |         | type,thatis,Relation(R). |     |     |     |     |     |
ThisguaranteesthatthetreesSMBOPgeneratesare
3.3 Beaminitialization
well-formed,andtheresultingSQLisexecutable.
Overall,thetotalnumberoftreesonthefrontieris As described in Line 3 of Alg. 1, the beam Z is
0
≤ K|U|+K2|B|. Becausescoresofdifferenttrees initializedwithK schemaconstants(e.g.,actor,
onthefrontierareindependent,theyareefficiently age) and DB values (e.g., 60, “France”). In
computedinparallel. Notethatwescorenewtrees particular, we independently score schema con-
fromthefrontierbeforecreatingarepresentation stants and choose the top-K, and similarly score
2
forthem,whichwedescribenext. DB values and choose the top-K, resulting in a
2
totalbeamofsizeK.
| Recursivetreerepresentation |     |     |     |     |     | afterscoringthe |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- |
frontier,wegeneratearecursivevectorrepresenta- Schemaconstants Weuseasimplescoringfunc-
tionforthetop-K trees. Whilescoringisdonewith tionf (·). Recallthats isarepresentationofa
|     |     |     |     |     |     |     |     |     | const |     | i   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
315

constant,contextualizedbytherestoftheschema
Size
andtheutterance. Thefunctionf (·)isafeed-
const 700 Depth
forwardnetworkthatscoreseachschemaconstant
600
independently: f (s ) = w tanh(W s ),
const i const const i
andthetop-K constantsareplacedinZ . 500
2 0
400
DBvalues Becausethenumberofvaluesinthe
300
DB is potentially huge, we do not score all DB
values. Instead, we learn to detect spans in the 200
questionthatcorrespondtoDBvalues. Thisleads 100
toasetupthatissimilartoextractivequestionan-
0
0 20 40 60 80 100
swering(Rajpurkaretal.,2016),wherethemodel
outputsadistributionoverinputspans,andthuswe
Figure 4: A histogram showing the distribution of the
adoptthearchitecturecommonlyusedinextractive height of relational algebra trees in SPIDER, and the
questionanswering. Concretely, wecompute the sizeofequivalentSQLquerytrees.
probabilitythatatokenisthestarttokenofaDB
value,P (x ) ∝ exp(w(cid:62) x ),andsimilarlythe
start i start i thegoldtree. Becauseofteacherforcing,thefron-
probability that a token is the end token of a DB
tier F is guaranteed to contain all gold trees
value, P (x ) ∝ exp(w(cid:62) x ), where w and t+1
end i end i start Zgold . We first apply a softmax over all frontier
w areparametervectors. Wedefinetheprobabil- t+1
end
trees p(z ) = softmax{s(z )} and
ityofaspan(x ,...,x )tobeP (x )·P (x ), new new znew∈Ft+1
i j start i end j
thenmaximizetheprobabilitiesofgoldtrees:
and place in the beam Z the top-K input spans,
0 2
where the representation of a span (x ,x ) is the
i j T
1 (cid:88) (cid:88)
averageofx i andx j . logp(z t )
C
gen
A
er
c
a
u
t
r
e
re
D
n
B
tl
v
im
al
i
u
ta
e
t
s
io
th
n
a
o
t
f
do
SM
no
B
t
O
ap
P
p
i
e
s
a
t
r
h
i
a
n
t
t
i
h
t
e
ca
i
n
n
n
p
o
u
t
t
t=0zt∈Z
t
gold
question. Thiswouldrequireaddingamechanism wherethelossisnormalizedbyC,thetotalnumber
suchas “BRIDGE” proposedbyLinetal.(2020). of summed terms. In the initial beam, Z , the
0
probability of an input span is the product of the
3.4 Training
startandendprobabilities,asexplainedin§3.3.
To specify the loss function, we need to define
thesupervisionsignal. Recallthatgiventhegold 3.5 Discussion
SQLprogram,weconvertitintoagoldbalanced
Toourknowledge,thisworkisthefirsttopresent
relationalalgebratreezgold, asexplainedin§3.1
asemi-autoregressivebottom-upsemanticparser.
andFigure2. Thisletsusdefineforeverydecoding
Wediscussthebenefitsofourapproach.
step the set of t-high gold sub-trees Zgold . For
t SMBOP hastheoreticalruntimecomplexitythat
exampleZgold
includesallgoldschemaconstants
0 islogarithmicinthesizeofthetreeinsteadoflin-
andinputspansthatmatchagoldDBvalue,3 Z 1 gold earforautoregressivemodels. Figure4showsthe
includesall1-highgoldtrees,etc. distribution over the height of relational algebra
Duringtraining,weapply“bottom-upTeacher trees in SPIDER, and the size of equivalent SQL
Forcing”(WilliamsandZipser,1989),thatis,we querytrees. Clearly,theheightofmosttreesisat
populate4 the beam Z t with all trees from Z t gold most 10, while the size is 30-50, illustrating the
andthenfilltherestofthebeam(ofsizeK)with potentialofthisapproach. In§4,wedemonstrate
thetop-scoringnon-goldpredictedtrees. Thisguar- that indeed semi-autoregressive parsing leads to
antees that we will be able to compute a loss at substantialempiricalspeed-up.
eachdecodingstep,asdescribedbelow. Unlike top-down autoregressive models, SM-
Lossfunction Duringsearch,ourgoalistogive
BOP naturally computes representations z for all
sub-treesconstructedatdecodingtime,whichare
high scores to the possibly multiple sub-trees of
well-defined semantic objects. These representa-
3InSpider,in98.2%ofthetrainingexamples,allgoldDB
tionscanbeusedinsetupssuchascontextualse-
valuesappearasinputspans.
manticparsing,whereasemanticparseranswers
4Wecomputethisthroughanefficienttreehashingproce-
dure.SeeAppendixA. a sequence of questions. For example, given the
316

|           |      |            |          |       |               |        | Model             |     |     |     | EM    | Exec |
| --------- | ---- | ---------- | -------- | ----- | ------------- | ------ | ----------------- | --- | --- | --- | ----- | ---- |
| questions | “How | many       | students | are   | living        | in the |                   |     |     |     |       |      |
|           |      |            |          |       |               |        | RAT-SQL+GP+GRAPPA |     |     |     | 69.8% | n/a  |
| dorms?”   | and  | then “what | are      | their | last names?”, |        |                   |     |     |     |       |      |
|           |      |            |          |       |               |        | RAT-SQL+GAP       |     |     |     | 69.7% | n/a  |
the pronoun “their” refers to a sub-tree from the RAT-SQL+GRAPPA 69.6% n/a
|           |     |                |           |        |        |        | RAT-SQL+STRUG         |     |     |     | 68.4% | n/a  |
| --------- | --- | -------------- | --------- | ------ | ------ | ------ | --------------------- | --- | --- | --- | ----- | ---- |
| SQL tree  | of  | the first      | question. | Having | a      | repre- |                       |     |     |     |       |      |
|           |     |                |           |        |        |        | BRIDGE+BERT(ensemble) |     |     |     | 67.5% | 68.3 |
| sentation | for | such sub-trees |           | can be | useful | when   |                       |     |     |     |       |      |
|           |     |                |           |        |        |        | RAT-SQLv3+BERT        |     |     |     | 65.6% | n/a  |
parsingthesecondquestion,inbenchmarkssuch SMBOP+GRAPPA 69.5% 71.1%
| as SPARC | (Yuetal.,2019). |     |     |     |     |     |         |     |                            |     |     |     |
| -------- | --------------- | --- | --- | --- | --- | --- | ------- | --- | -------------------------- | --- | --- | --- |
|          |                 |     |     |     |     |     | Table2: |     | ResultsontheSPIDERtestset. |     |     |     |
Anotherpotentialbenefitofbottom-upparsing
isthatsub-queriescanbeexecutedwhileparsing
(Berantetal.,2013;Liangetal.,2017),whichcan anonymized queries, where DB values are con-
guidethesearchprocedure. Recently,Odenaetal. vertedtoaspecialvaluetoken. Inaddition, for
(2020)proposedsuchanapproachforprogramsyn-
modelsthatoutputDBvalues,theevaluationscript
thesis,andshowedthatconditioningontheresults computesdenotationaccuracy,thatis,whetherex-
ofexecutioncanimproveperformance. Wedonot ecuting the output SQL query results in the right
explorethisadvantageofbottom-upparsinginthis denotation (answer). As SMBOP generates DB
work,sinceexecutingqueriesattrainingtimeleads
values,weevaluateusingbothEManddenotation
| toaslow-downduringtraining. |     |             |     |                     |     |     | accuracy |     |     |     |     |     |
| --------------------------- | --- | ----------- | --- | ------------------- | --- | --- | -------- | --- | --- | --- | --- | --- |
| SMBOP                       | is  | a bottom-up |     | semi-autoregressive |     |     |          |     |     |     |     |     |
parser, but it could potentially be modified to be Models We compare SMBOP to the best non-
anonymousmodelsontheSPIDERleaderboardat
| autoregressivebydecodingonetreeatatime. |     |     |     |     |     | Past |          |             |     |       |         |          |
| --------------------------------------- | --- | --- | --- | --- | --- | ---- | -------- | ----------- | --- | ----- | ------- | -------- |
|                                         |     |     |     |     |     |      | the time | of writing. | Our | model | is most | compara- |
work(Chengetal.,2019)hasshownthattheperfor-
|     |     |     |     |     |     |     | ble to RAT-SQL+GRAPPA, |     |     | which | has | the same |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | ----- | --- | -------- |
manceofbottom-upandtop-downautoregressive
parsersissimilar,butitispossibletore-examine encoder,butanautoregressivedecoder.
Inaddition,weperformthefollowingablations
thisgivenrecentadvancesinneuralarchitectures.
andoracleexperiments:
4 ExperimentalEvaluation • NO X-ATTENTION: Weremovethecrossatten-
|     |     |     |     |     |     |     | tion that | computes |     | Z(cid:48) and uses | the | representa- |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ------------------ | --- | ----------- |
t
WeconductourexperimentalevaluationonSPIDER
|     |     |     |     |     |     |     | tionsinZ | directlytoscorethefrontier. |     |     |     | Inthis |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------------------------- | --- | --- | --- | ------ |
t
(Yuetal.,2018),achallenginglarge-scaledataset
setup,thedecoderonlyobservestheinputques-
| for text-to-SQL |           | parsing. |     | SPIDER     | has become |     |                              |      |       |        |                    |     |
| --------------- | --------- | -------- | --- | ---------- | ---------- | --- | ---------------------------- | ---- | ----- | ------ | ------------------ | --- |
|                 |           |          |     |            |            |     | tionthroughthe0-hightreesinZ |      |       |        | 0 .                |     |
| a common        | benchmark |          | for | evaluating | semantic   |     |                              |      |       |        |                    |     |
|                 |           |          |     |            |            |     | • WITH                       | CNTX | REP.: | We use | the contextualized |     |
parsersbecauseitincludescomplexSQLqueries
representationsnotonlyforscoring,butalsoas
| and a realistic |     | zero-shot | setup, | where | schemas | at  |     |     |     |     |     |     |
| --------------- | --- | --------- | ------ | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
testtimearedifferentfromtrainingtime. inputforcreatingthenewtreesZ t+1 . Thistestsif
contextualizedrepresentationsonthebeamhurt
| 4.1 Experimentalsetup |     |     |     |     |     |     | orimproveperformance. |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- |
WeencodetheinpututterancexandtheschemaS
|     |     |     |     |     |     |     | • NODBVALUES: |     | WeanonymizeallSQLqueries |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ------------------------ | --- | --- | --- |
with GRAPPA,consistingof24Transformerlayers, by replacing DB values with value, as de-
followedbyanother8RAT-SQLlayers,whichwe scribedabove,andevaluate SMBOP usingEM.
implementinsideAllenNLP(Gardneretal.,2018).
ThistestswhetherlearningfromDBvaluesim-
| Our beam | size | is K | = 30, | and | the number | of  |     |     |     |     |     |     |
| -------- | ---- | ---- | ----- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
provesperformance.
| decodingstepsisT |     |     | = 9atinferencetime,which |     |     |     |              |     |                          |     |     |     |
| ---------------- | --- | --- | ------------------------ | --- | --- | --- | ------------ | --- | ------------------------ | --- | --- | --- |
|                  |     |     |                          |     |     |     | • Z -ORACLE: |     | AnoracleexperimentwhereZ |     |     | is  |
|                  |     |     |                          |     |     |     | 0            |     |                          |     |     | 0   |
isthemaximaltreedepthonthedevelopmentset.
|     |     |     |     |     |     |     | populated | with | the | gold schema | constants | (but |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---- | --- | ----------- | --------- | ---- |
Thetransformerusedfortreerepresentationshas
|            |     |        |                    |     |      |     | predictedDBvalues). |     |     | Thisshowsresultsgiven |     |     |
| ---------- | --- | ------ | ------------------ | --- | ---- | --- | ------------------- | --- | --- | --------------------- | --- | --- |
| one layer, | 8   | heads, | and dimensionality |     | 256. | We  |                     |     |     |                       |     |     |
perfectschemamatching.
trainfor60Kstepswithbatchsize60,andperform
earlystoppingbasedonthedevelopmentset.
|     |     |     |     |     |     |     | 4.2 Results |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
Evaluation We evaluate performance with the Table2showstestresultsof SMBOP comparedto
officialSPIDERevaluationscript,whichcomputes thetop(non-anonymous)entriesontheleaderboard
exactmatch(EM),i.e.,whetherthepredictedSQL (Zhaoetal.,2021;Shietal.,2021;Yuetal.,2020;
query is identical to the gold query after some Deng et al., 2020; Lin et al., 2020; Wang et al.,
query normalization. The evaluation script uses 2020a). SMBOP obtains an EM of 69.5%, only
317

6
0.7
|     | 5   |     |     |     |     | 0.6 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.5
pudeepS 4
0.4
ME
|     | 3   |     |     |     |     | 0.3 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.2
2
SmBoP-GraPPa
|     |     |     |     |     |     | 0.1 |     |     |     |     | RATSQL-GraPPa |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |
|     | 1   |     |     |     |     | 0.0 |     |     |     |     | RATSQL-BERT   |     |
20 40 60 80 100 120 140 0 100k200k300k400k500k600k700k800k900k 1m 1.1m
|     |     |     |     | Size |     |     |     |     | # Examples |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---------- | --- | --- | --- |
Figure 5: Speed-up on the development set compared Figure7: EMasafunctionofthenumberofexamples
to autoregressive decoding, w.r.t the size of the SQL onthedevelopmentsetofSPIDERduringtraining.
query.
|     |     |     |     |     |     | Model          |     | Exec  | EM    |       | BEM | Z 0REC. |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ----- | ----- | ----- | --- | ------- |
|     |     |     |     |     |     | RAT-SQL+GRAPPA |     | n/a   | 73.9% | n/a   |     | n/a     |
|     |     |     |     |     |     | SMBOP          |     | 75.0% | 74.7% | 82.6% |     | 98.3%   |
|     |     |     |     |     |     | -NOX-ATT       |     | 74.8% | 72.7% | 81.1% |     | 96.6%   |
0.7
|     |     |     |     |     |     | -WITHCNTXREP. |     | 73.4% | 72.4% | 81.9% |     | 97.3% |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ----- | ----- | ----- | --- | ----- |
0.6
|     |     |     |     |     |     | -NODBVALUES |          | n/a   | 71.3% | 80.0% |     | 98.1% |
| --- | --- | --- | --- | --- | --- | ----------- | -------- | ----- | ----- | ----- | --- | ----- |
|     | 0.5 |     |     |     |     | SMBOP-Z     | 0-ORACLE | 77.4% | 79.1% | 85.8% |     | n/a   |
ME 0.4
|     |     |     |     |     |     | Table 3:                             | Development | set | EM, | beam | EM (BEM) | and       |
| --- | --- | --- | --- | --- | --- | ------------------------------------ | ----------- | --- | --- | ---- | -------- | --------- |
|     | 0.3 |     |     |     |     | recallonschemaconstantsandDBvalues(Z |             |     |     |      |          | rec.) for |
0
0.2
allmodels.
SmBoP-GraPPa
0.1
RATSQL-GraPPa
RATSQL-BERT
0.0
|     |     |       |     |       |       | much faster | training |     | and convergence. |     | We  | com- |
| --- | --- | ----- | --- | ----- | ----- | ----------- | -------- | --- | ---------------- | --- | --- | ---- |
|     | 0   | 10 20 | 30  | 40 50 | 60 70 |             |          |     |                  |     |     |      |
Wall Clock Time (hours)
|     |     |     |     |     |     | pare the | learning | curves | of  | SMBOP | and | RAT- |
| --- | --- | --- | --- | --- | --- | -------- | -------- | ------ | --- | ----- | --- | ---- |
Figure 6: EM as a function of wall clock time on the SQLv3+BERT,bothtrainedonanRTX3090,and
developmentsetofSPIDERduringtraining.
alsotoRAT-SQLv3+GRAPPAusingperformance
|     |     |     |     |     |     | as a function | of  | the number |     | of examples, |     | sent to |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ---------- | --- | ------------ | --- | ------- |
usinapersonalcommunicationfromtheauthors.
| 0.3% | lower | than the | best | model, | and 0.1% lower |       |           |      |        |      |         |     |
| ---- | ----- | -------- | ---- | ------ | -------------- | ----- | --------- | ---- | ------ | ---- | ------- | --- |
|      |       |          |      |        |                | SMBOP | converges | much | faster | than | RAT-SQL |     |
than RAT-SQL+GRAPPA,whichhasthesameen-
|        |         |                   |         |          |              | (Fig.7).    | E.g.,after120Kexamples,theEMof |     |                |     |     | SM-  |
| ------ | ------- | ----------------- | ------- | -------- | ------------ | ----------- | ------------------------------ | --- | -------------- | --- | --- | ---- |
| coder, | but     | an autoregressive |         | decoder. | Moreover,    |             |                                |     |                |     |     |      |
|        |         |                   |         |          |              | BOP is67.5, | whilefor                       |     | RAT-SQL+GRAPPA |     |     | itis |
| SMBOP  | outputs | DB                | values, | unlike   | other models |             |                                |     |                |     |     |      |
47.6. Moreover,SMBOPprocessesattrainingtime
thatoutputanonymizedqueriesthatcannotbeex-
20.4examplespersecond,comparedtoonly3.8for
ecuted. SMBOPestablishesanewstate-of-the-art
|     |     |     |     |     |     | theofficialRAT-SQLimplementation. |     |     |     |     | Combining |     |
| --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --------- | --- |
indenotationaccuracy,surpassinganensembleof
thesetwofactsleadstomuchfastertrainingtime
| BRIDGE+BERT |     |     | modelsby2.9denotationaccu- |     |     |     |     |     |     |     |     |     |
| ----------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(Fig.6),slighlymorethanonedayforSMBOPvs.
racypoints,and2EMpoints.
|                                 |     |     |     |     |       | 5-6daysfor | RAT-SQL. |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ----- | ---------- | -------- | --- | --- | --- | --- | --- |
| Turningtodecodingtime,wecompare |     |     |     |     | SMBOP |            |          |     |     |     |     |     |
to RAT-SQLv3+BERT,sincethecodefor RAT- Ablations Table3showsresultsofablationson
| SQLv3+GRAPPA |     |     | was not | available. | To the best |                    |     |     |                       |     |     |     |
| ------------ | --- | --- | ------- | ---------- | ----------- | ------------------ | --- | --- | --------------------- | --- | --- | --- |
|              |     |     |         |            |             | thedevelopmentset. |     |     | ApartfromEM,wealsore- |     |     |     |
ofourknowledgethedecoderinbothisidentical, port: (a)beamEM(BEM):whetheracorrecttree
so this should not affect decoding time. We find wasfoundanywhereduringtheT decodingsteps,
that the decoder of SMBOP is on average 2.23x and(b)Z 0 recall: thefractionofexampleswhere
fasterthantheautoregressivedecoderonthedevel- the parser placed all gold schema constants and
opmentset. Figure5showstheaveragespeed-up DBvaluesinZ . Thisestimatestheabilityofour
0
fordifferentquerytreesizes,whereweobservea models to perform schema matching in a single
| clear | linear | speed-up | as  | a function | of query size. |     |     |     |     |     |     |     |
| ----- | ------ | -------- | --- | ---------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
non-autoregressivestep.
For long queries the speed-up factor reaches 4x- We observe that ablating cross-attention leads
6x. Whenincludingalsotheencoder,theaverage toasmallreductioninEM.Thisrathersmalldrop
speed-upobtainedby SMBOP is1.55x. is surprising since it means that all information
In terms of training time, SMBOP leads to aboutthequestionispassedtothedecoderthrough
318

|     | 1.0 |     |     |     |     | thefirstgoldtreethatisdroppedfromthebeam(if |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- |
thereismorethanone,wechooseonerandomly).
0.8
Wethenlookatthechildrenoft,andseewhether
llaceR tZ 0.6 at least one was expanded in some later step in
decoding,orwhetherthechildrenwerecompletely
0.4
|     |     |     |     |     |     | abandonedbythesearchprocedure. |        |       |        |     | Wefindthat |          |
| --- | --- | --- | --- | --- | --- | ------------------------------ | ------ | ----- | ------ | --- | ---------- | -------- |
|     | 0.2 |     |     |     |     | in 62%                         | of the | cases | indeed | one | of the     | children |
wasincorrectlyexpanded,indicatingacomposition
0.0
|     |     | 0 2 | 4   | 6   | 8   | error. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
Decoding Step
|     |          |                              |     |     |     | In this | work, | we used | beam | size | K = | 30. Re- |
| --- | -------- | ---------------------------- | --- | --- | --- | ------- | ----- | ------- | ---- | ---- | --- | ------- |
|     | Figure8: | Z Recallacrossdecodingsteps. |     |     |     |         |       |         |      |      |     |         |
t
|     |     |     |     |     |     | ducing                     | K to 20 | leads | to a drop | of              | less than | point |
| --- | --- | --- | --- | --- | --- | -------------------------- | ------- | ----- | --------- | --------------- | --------- | ----- |
|     |     |     |     |     |     | (74.7→73.8),andincreasingK |         |       |           | to40reducesper- |           |       |
Z . Wehypothesizethatthisispossible,because formanceby(74.7→72.6). Inallcases,decoding
0
the number of decoding steps is small, and thus timedoesnotdramaticallychange.
utterance information can propagate through the Last, we randomly sample 50 errors from SM-
decoder. Usingcontextualizedrepresentationsfor BOPandcategorizethemintothefollowingtypes:
trees also leads to a small drop in performance. • Search errors (52%): we find that most search
Last,weseethatfeedingthemodelwithactualDB errorsareduetoeitherextraormissingJOINor
values rather than an anonymized value token WHEREconditions.
improvesperformanceby3.4EMpoints.
|      |            |                            |          |        |           | • Schemaencodingerrors(34%):        |     |         |        |           | Missingorextra |            |
| ---- | ---------- | -------------------------- | -------- | ------ | --------- | ----------------------------------- | --- | ------- | ------ | --------- | -------------- | ---------- |
|      | LookingatZ | RECALL,weseethatmodelsper- |          |        |           |                                     |     |         |        |           |                |            |
|      |            | 0                          |          |        |           | schemaconstantsinthepredictedquery. |     |         |        |           |                |            |
| form | well       | at detecting               | relevant | schema | constants |                                     |     |         |        |           |                |            |
|      |            |                            |          |        |           | • Equivalent                        |     | queries | (12%): | Predicted |                | trees that |
andDBvalues(96.6%-98.3%),despitethefactthat
areequivalenttothegoldtree,buttheautomatic
| thisstepisfullynon-autoregressive. |     |     |     |     | However,an |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
evaluationscriptdoesnothandle.
oraclemodelthatplacesallgoldschemaconstants
| andonlygoldschemaconstantsinZ |     |     |     |     | furtherim- |               |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | ---------- | ------------- | --- | --- | --- | --- | --- | --- |
|                               |     |     |     |     | 0          | 5 Conclusions |     |     |     |     |     |     |
provesEM(74.7→79.1%),withaBEMof85.8%.
|     |     |     |     |     |     | In this | work | we  | present | the | first | semi- |
| --- | --- | --- | --- | --- | --- | ------- | ---- | --- | ------- | --- | ----- | ----- |
Thisshowsthatbetterschemamatchingandsearch
|                              |     |     |     |     |         | autoregressive |             | bottom-up |             | semantic |          | parser |
| ---------------------------- | --- | --- | --- | --- | ------- | -------------- | ----------- | --------- | ----------- | -------- | -------- | ------ |
| canstillimproveperformanceon |     |     |     |     | SPIDER. |                |             |           |             |          |          |        |
|                              |     |     |     |     |         | that enjoys    | logarithmic |           | theoretical |          | runtime, | and    |
BEMis8%-9%higherthanEM,showingthat,
|     |     |     |     |     |     | show that | it  | leads to | a 2.2x | speed-up |     | in decod- |
| --- | --- | --- | --- | --- | --- | --------- | --- | -------- | ------ | -------- | --- | --------- |
similartopastfindingsinsemanticparsing(Gold-
|     |     |     |     |     |     | ing and | ∼5x | faster | taining, | while | maintaining |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------ | -------- | ----- | ----------- | --- |
manetal.,2018;YinandNeubig,2019),addinga
re-rankerontopofthetreescomputedby SMBOP state-of-the-art performance. Our work shows
|     |             |         |              |     |          | that bottom-up  |     | parsing, | where        | the | model      | learns |
| --- | ----------- | ------- | ------------ | --- | -------- | --------------- | --- | -------- | ------------ | --- | ---------- | ------ |
| can | potentially | improve | performance. |     | We leave |                 |     |          |              |     |            |        |
|     |             |         |              |     |          | representations |     | for      | semantically |     | meaningful |        |
thisforfuturework.
|     |          |     |     |     |     | sub-trees      | is a | promising | research |     | direction, | that    |
| --- | -------- | --- | --- | --- | --- | -------------- | ---- | --------- | -------- | --- | ---------- | ------- |
| 4.3 | Analysis |     |     |     |     | can contribute |      | in the    | future   | to  | setups     | such as |
contextualsemanticparsing,wheresub-treesoften
| WeextendthenotionofZ |     |     |     | recalltoalldecoding |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
0
repeat, andcanenjoythebenefitsofexecutionat
| steps, | where | Z t recall | is whether |     | all gold t-high |     |     |     |     |     |     |     |
| ------ | ----- | ---------- | ---------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- |
sub-treesweregeneratedatstept. WeseeZ recall trainingtime. Futureworkcanalsoleveragework
t
|                                |     |     |     |     |              | on learning | tree | representations |     | (Shiv | and | Quirk, |
| ------------------------------ | --- | --- | --- | --- | ------------ | ----------- | ---- | --------------- | --- | ----- | --- | ------ |
| acrossdecodingstepsinFigure8.5 |     |     |     |     | Thedropafter |             |      |                 |     |       |     |        |
2019)tofurtherimproveparserperformance.
step0andsubsequentriseindicatethatthemodel
maintainsinthebeam,usingtheKEEPoperation,
Acknowledgments
treesthataresub-treesofthegoldtree,andexpands
theminlatersteps. Thismeansthattheparsercan We thank Tao Yu, Ben Bogin, Jonathan Herzig,
InbarOren,EladSegalandAnkitGuptafortheir
recoverfromerrorsinearlydecodingstepsaslong
astherelevanttreesarekeptonthebeam. usefulcomments. Thisresearchwaspartiallysup-
To better understand search errors we perform portedbyTheYandexInitiativeforMachineLearn-
|                       |     |     |                       |     |     | ing, and | the | European | Research |     | Council | (ERC) |
| --------------------- | --- | --- | --------------------- | --- | --- | -------- | --- | -------- | -------- | --- | ------- | ----- |
| thefollowinganalysis. |     |     | Foreachexample,wefind |     |     |          |     |          |          |     |         |       |
undertheEuropeanUnionHorizons2020research
5Thismetricchecksforexactsub-treematch,unlikeEM
|     |     |     |     |     |     | and innovation |     | programme |     | (grant | ERC | DELPHI |
| --- | --- | --- | --- | --- | --- | -------------- | --- | --------- | --- | ------ | --- | ------ |
thatdoesmorenormalization,sonumbersarenotcomparable
802800).
toEM.
319

References
|     |     |     |     |     |     |     | pages | 4524–4535, | Florence, |     | Italy. Association | for |
| --- | --- | --- | --- | --- | --- | --- | ----- | ---------- | --------- | --- | ------------------ | --- |
ComputationalLinguistics.
| J.Berant,A.Chou,R.Frostig,andP.Liang.2013. |              |             |      |                 |          | Se- |          |         |       |           |        |        |
| ------------------------------------------ | ------------ | ----------- | ---- | --------------- | -------- | --- | -------- | ------- | ----- | --------- | ------ | ------ |
| mantic                                     | parsing      | on Freebase | from | question-answer |          |     |          |         |       |           |        |        |
|                                            |              |             |      |                 |          |     | Jonathan | Herzig, | Pawel | Krzysztof | Nowak, | Thomas |
| pairs.                                     | In Empirical | Methods     |      | in Natural      | Language |     |          |         |       |           |        |        |
Müller,FrancescoPiccinno,andJulianEisenschlos.
Processing(EMNLP).
|          |         |             |          |               |           |      | 2020.         | TaPas: | Weakly         | supervised | table         | parsing via |
| -------- | ------- | ----------- | -------- | ------------- | --------- | ---- | ------------- | ------ | -------------- | ---------- | ------------- | ----------- |
|          |         |             |          |               |           |      | pre-training. |        | In Proceedings |            | of the        | 58th Annual |
| Jianpeng | Cheng,  | Siva Reddy, |          | Vijay         | Saraswat, | and  |               |        |                |            |               |             |
|          |         |             |          |               |           |      | Meeting       | of the | Association    | for        | Computational | Lin-        |
| Mirella  | Lapata. | 2019.       | Learning | an executable |           | neu- |               |        |                |            |               |             |
ral semantic parser. Computational Linguistics, guistics, pages 4320–4333, Online. Association for
| 45(1):59–94. |     |     |     |     |     |     | ComputationalLinguistics. |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- |
JamesClarke,DanGoldwasser,Ming-WeiChang,and JayantKrishnamurthy,PradeepDasigi,andMattGard-
Dan Roth. Driving semantic parsing from the ner. 2017. Neural semantic parsing with type con-
world’sresponse. InProceedingsoftheFourteenth straints for semi-structured tables. In Proceedings
Conference on Computational Natural Language oftheConferenceonEmpiricalMethodsinNatural
| Learning(CoNLL). |       |                                |            |     |             |     | LanguageProcessing(EMNLP). |                         |          |         |                   |            |
| ---------------- | ----- | ------------------------------ | ---------- | --- | ----------- | --- | -------------------------- | ----------------------- | -------- | ------- | ----------------- | ---------- |
| E.F.Codd.1970.   |       | Arelationalmodelofdataforlarge |            |     |             |     |                            |                         |          |         |                   |            |
|                  |       |                                |            |     |             |     | C. Liang,                  | J. Berant,              | Q.       | Le, and | K. D.             | F. N. Lao. |
| shareddatabanks. |       | Commun.ACM,13(6):377–387.      |            |     |             |     |                            |                         |          |         |                   |            |
|                  |       |                                |            |     |             |     | 2017.                      | Neuralsymbolicmachines: |          |         | Learningseman-    |            |
|                  |       |                                |            |     |             |     | tic parsers                | on                      | Freebase | with    | weak supervision. | In         |
| Xiang Deng,      | Ahmed | Hassan                         | Awadallah, |     | Christopher |     |                            |                         |          |         |                   |            |
AssociationforComputationalLinguistics(ACL).
| Meek,           | OleksandrPolozov, |                                | HuanSun, |              | andMatthew  |     |              |                  |         |               |               |              |
| --------------- | ----------------- | ------------------------------ | -------- | ------------ | ----------- | --- | ------------ | ---------------- | ------- | ------------- | ------------- | ------------ |
| Richardson.     | 2020.             | Structure-grounded             |          |              | pretraining |     |              |                  |         |               |               |              |
|                 |                   |                                |          |              |             |     | Percy Liang, | Michael          | Jordan, | and           | Dan           | Klein. 2011. |
| fortext-to-sql. |                   | arXivpreprintarXiv:2010.12773. |          |              |             |     |              |                  |         |               |               |              |
|                 |                   |                                |          |              |             |     | Learning     | dependency-based |         |               | compositional | seman-       |
|                 |                   |                                |          |              |             |     | tics. In     | Proceedings      | of      | the           | 49th Annual   | Meeting      |
| Jacob Devlin,   | Ming-Wei          |                                | Chang,   | Kenton       | Lee,        | and |              |                  |         |               |               |              |
|                 |                   |                                |          |              |             |     | of the       | Association      | for     | Computational |               | Linguistics: |
| Kristina        | Toutanova.        | 2019.                          | BERT:    | Pre-training |             | of  |              |                  |         |               |               |              |
deep bidirectional transformers for language under- Human Language Technologies (ACL-HLT), pages
standing. In Proceedings of the 2019 Conference 590–599, Portland, Oregon, USA. Association for
ComputationalLinguistics.
| of the            | North American |              | Chapter | of the | Association |     |     |     |     |     |     |     |
| ----------------- | -------------- | ------------ | ------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
| for Computational |                | Linguistics: |         | Human  | Language    |     |     |     |     |     |     |     |
Technologies, Volume 1 (Long and Short Papers), Xi Victoria Lin, Richard Socher, and Caiming Xiong.
pages4171–4186,Minneapolis,Minnesota.Associ- 2020. Bridging textual and tabular data for cross-
ationforComputationalLinguistics. domain text-to-SQL semantic parsing. In Findings
|     |     |     |     |     |     |     | of the | Association | for | Computational |     | Linguistics: |
| --- | --- | --- | --- | --- | --- | --- | ------ | ----------- | --- | ------------- | --- | ------------ |
Li Dong and Mirella Lapata. 2016. Language to logi- EMNLP 2020, pages 4870–4888, Online. Associa-
InProceedingsofthe
| calformwithneuralattention. |     |     |     |     |     |     | tionforComputationalLinguistics. |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- |
54thAnnualMeetingoftheAssociationforCompu-
tationalLinguistics(ACL),pages33–43,Berlin,Ger- YinhanLiu,MyleOtt,NamanGoyal,JingfeiDu,Man-
many.AssociationforComputationalLinguistics. dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
|               |      |       |      |          |     |        | Luke     | Zettlemoyer, | and       | Veselin | Stoyanov.        | 2019. |
| ------------- | ---- | ----- | ---- | -------- | --- | ------ | -------- | ------------ | --------- | ------- | ---------------- | ----- |
| Matt Gardner, | Joel | Grus, | Mark | Neumann, |     | Oyvind |          |              |           |         |                  |       |
|               |      |       |      |          |     |        | Roberta: | A robustly   | optimized |         | bert pretraining | ap-   |
Tafjord,PradeepDasigi,NelsonF.Liu,MatthewPe-
|     |     |     |     |     |     |     | proach. | arXivpreprintarXiv:1907.11692. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------------------------ | --- | --- | --- | --- |
ters,MichaelSchmitz,andLukeZettlemoyer.2018.
| AllenNLP:     | A         | deep semantic  | natural     |     | language     | pro- |                |         |            |           |              |             |
| ------------- | --------- | -------------- | ----------- | --- | ------------ | ---- | -------------- | ------- | ---------- | --------- | ------------ | ----------- |
|               |           |                |             |     |              |      | Ralph C.       | Merkle. | 1987. A    | digital   | signature    | based on    |
| cessing       | platform. | In Proceedings |             | of  | Workshop     | for  |                |         |            |           |              |             |
|               |           |                |             |     |              |      | a conventional |         | encryption | function. |              | In Advances |
| NLP Open      | Source    | Software       | (NLP-OSS),  |     | pages        | 1–   |                |         |            |           |              |             |
|               |           |                |             |     |              |      | in Cryptology  |         | - CRYPTO   | ’87,      | A Conference | on          |
| 6, Melbourne, |           | Australia.     | Association |     | for Computa- |      |                |         |            |           |              |             |
theTheoryandApplicationsofCryptographicTech-
tionalLinguistics.
niques,SantaBarbara,California,USA,August16-
20,1987,Proceedings,volume293ofLectureNotes
OmerGoldman,VeronicaLatcinnik,EhudNave,Amir
inComputerScience.
| Globerson, | and      | Jonathan | Berant. | 2018.    | Weakly    | su- |          |        |        |            |         |         |
| ---------- | -------- | -------- | ------- | -------- | --------- | --- | -------- | ------ | ------ | ---------- | ------- | ------- |
| pervised   | semantic | parsing  | with    | abstract | examples. |     |          |        |        |            |         |         |
|            |          |          |         |          |           |     | Augustus | Odena, | Kensen | Shi, David | Bieber, | Rishabh |
InProceedingsofthe56thAnnualMeetingoftheAs-
sociationforComputationalLinguistics(ACL)(Vol- Singh, and Charles Sutton. 2020. Bustle: Bottom-
ume1:LongPapers),pages1809–1819,Melbourne, up program-synthesis through learning-guided ex-
ploration.
| Australia. | Association |     | for Computational |     |     | Linguis- |     |     |     |     |     |     |
| ---------- | ----------- | --- | ----------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
tics.
|     |     |     |     |     |     |     | Maxim Rabinovich, |     | Mitchell | Stern, | and | Dan Klein. |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------- | ------ | --- | ---------- |
Jiaqi Guo, Zecheng Zhan, Yan Gao, Yan Xiao, 2017. Abstract syntax networks for code genera-
Jian-Guang Lou, Ting Liu, and Dongmei Zhang. tion and semantic parsing. In Proceedings of the
2019. Towards complex text-to-SQL in cross- 55thAnnualMeetingoftheAssociationforCompu-
domain database with intermediate representation. tational Linguistics (ACL), pages 1139–1149, Van-
In Proceedings of the 57th Annual Meeting of the couver,Canada.AssociationforComputationalLin-
| Association | for | Computational |     | Linguistics |     | (ACL), | guistics. |     |     |     |     |     |
| ----------- | --- | ------------- | --- | ----------- | --- | ------ | --------- | --- | --- | --- | --- | --- |
320

PranavRajpurkar,JianZhang,KonstantinLopyrev,and PengchengYinandGrahamNeubig.2019. Reranking
PercyLiang.2016. SQuAD:100,000+questionsfor for neural semantic parsing. In Proceedings of the
machine comprehension of text. In Proceedings of 57thAnnualMeetingoftheAssociationforCompu-
the2016ConferenceonEmpiricalMethodsinNatu- tationalLinguistics(ACL).
ralLanguageProcessing,pages2383–2392,Austin,
PengchengYin,GrahamNeubig,Wen-tauYih,andSe-
Texas.AssociationforComputationalLinguistics.
|     |     |     |     |     |     |     | bastianRiedel.2020. |     |     | TaBERT:Pretrainingforjoint |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | -------------------------- | --- | --- | --- |
RoySchwartz,JesseDodge,NoahA.Smith,andOren understanding of textual and tabular data. In Pro-
Etzioni. 2020. Green AI. Communications of the ceedings of the 58th Annual Meeting of the Asso-
| ACM,63.     |       |            |     |     |        |          | ciation | for Computational |             |     | Linguistics, |               | pages 8413– |
| ----------- | ----- | ---------- | --- | --- | ------ | -------- | ------- | ----------------- | ----------- | --- | ------------ | ------------- | ----------- |
|             |       |            |     |     |        |          | 8426,   | Online.           | Association |     | for          | Computational | Lin-        |
| Peter Shaw, | Jakob | Uszkoreit, |     | and | Ashish | Vaswani. |         |                   |             |     |              |               |             |
guistics.
2018. Self-attentionwithrelativepositionrepresen-
|          |                |     |     |          |            |     | Tao Yu, | Chien-Sheng |     | Wu, | Xi Victoria |     | Lin, Bailin |
| -------- | -------------- | --- | --- | -------- | ---------- | --- | ------- | ----------- | --- | --- | ----------- | --- | ----------- |
| tations. | In Proceedings |     | of  | the 2018 | Conference | of  |         |             |     |     |             |     |             |
the North American Chapter of the Association for Wang, YiChernTan, XinyiYang, DragomirRadev,
ComputationalLinguistics: HumanLanguageTech- RichardSocher,andCaimingXiong.2020. Grappa:
nologies (NAACL-HLT), Volume 2 (Short Papers), Grammar-augmentedpre-trainingfortablesemantic
|       |          |     |          |            |     |          | parsing. | arXivpreprintarXiv:2009.13845. |     |     |     |     |     |
| ----- | -------- | --- | -------- | ---------- | --- | -------- | -------- | ------------------------------ | --- | --- | --- | --- | --- |
| pages | 464–468, | New | Orleans, | Louisiana. |     | Associa- |          |                                |     |     |     |     |     |
tionforComputationalLinguistics.
|           |         |     |        |     |       |         | Tao Yu, | Rui Zhang, |       | Kai Yang, | Michihiro |     | Yasunaga, |
| --------- | ------- | --- | ------ | --- | ----- | ------- | ------- | ---------- | ----- | --------- | --------- | --- | --------- |
|           |         |     |        |     |       |         | Dongxu  | Wang,      | Zifan | Li,       | James     | Ma, | Irene Li, |
| Peng Shi, | Patrick | Ng, | Zhiguo |     | Wang, | Henghui |         |            |       |           |           |     |           |
Zhu, Alexander Hanbo Li, Jun Wang, Cicero Qingning Yao, Shanelle Roman, Zilin Zhang,
NogueiradosSantos,andBingXiang.2021. Learn- and Dragomir Radev. 2018. Spider: A large-
ing contextual representations for semantic pars- scale human-labeled dataset for complex and cross-
|          |                      |     |     |               |     |       | domain      | semantic | parsing |      | and text-to-SQL |     | task. In  |
| -------- | -------------------- | --- | --- | ------------- | --- | ----- | ----------- | -------- | ------- | ---- | --------------- | --- | --------- |
| ing with | generation-augmented |     |     | pre-training. |     | arXiv |             |          |         |      |                 |     |           |
|          |                      |     |     |               |     |       | Proceedings |          | of the  | 2018 | Conference      | on  | Empirical |
preprintarXiv:2012.10309.
MethodsinNaturalLanguageProcessing(EMNLP),
VighneshLeonardoShivandChrisQuirk.2019. Novel pages 3911–3921, Brussels, Belgium. Association
positionalencodingstoenabletree-structuredtrans- forComputationalLinguistics.
| formers. | In  | Advances | in  | Neural | Information | Pro- |     |     |     |     |     |     |     |
| -------- | --- | -------- | --- | ------ | ----------- | ---- | --- | --- | --- | --- | --- | --- | --- |
cessingSystems(NeurIPS). Tao Yu, Rui Zhang, Michihiro Yasunaga, Yi Chern
|                 |     |      |          |      |         |       | Tan, Xi  | Victoria | Lin,  | Suyi  | Li, Irene | Li         | Heyang Er, |
| --------------- | --- | ---- | -------- | ---- | ------- | ----- | -------- | -------- | ----- | ----- | --------- | ---------- | ---------- |
|                 |     |      |          |      |         |       | Bo Pang, | Tao      | Chen, | Emily |           | Ji, Shreya | Dixit,     |
| Ashish Vaswani, |     | Noam | Shazeer, | Niki | Parmar, | Jakob |          |          |       |       |           |            |            |
Uszkoreit, Llion Jones, Aidan N Gomez, Ł ukasz David Proctor, Sungrok Shim, Vincent Zhang
Kaiser, and Illia Polosukhin. 2017. Attention is all Jonathan Kraft, Caiming Xiong, Richard Socher,
you need. In I. Guyon, U. V. Luxburg, S. Bengio, and Dragomir Radev. 2019. Sparc: Cross-domain
H.Wallach,R.Fergus,S.Vishwanathan,andR.Gar- semantic parsing in context. In Proceedings of the
57thAnnualMeetingoftheAssociationforCompu-
| nett, editors, |     | Advances | in  | Neural | Information | Pro- |                                    |     |     |     |     |                |     |
| -------------- | --- | -------- | --- | ------ | ----------- | ---- | ---------------------------------- | --- | --- | --- | --- | -------------- | --- |
|                |     |          |     |        |             |      | tationalLinguistics(ACL),Florence, |     |     |     |     | Italy.Associa- |     |
cessingSystems(NeurIPS).
tionforComputationalLinguistics.
| Bailin Wang, | Richard | Shin, | Xiaodong |     | Liu, | Oleksandr |     |     |     |     |     |     |     |
| ------------ | ------- | ----- | -------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
Polozov, and Matthew Richardson. 2020a. RAT- JohnM.ZelleandRaymondJ.Mooney.1996. Learn-
SQL: Relation-aware schema encoding and linking ing to parse database queries using inductive logic
fortext-to-SQLparsers. InProceedingsofthe58th programming. InProceedingsoftheThirteenthNa-
tionalConferenceonArtificialIntelligence(AAAI).
| Annual | Meeting | of  | the Association |     | for | Computa- |     |     |     |     |     |     |     |
| ------ | ------- | --- | --------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
tionalLinguistics(ACL).
|              |         |       |          |     |      |           | LukeS.ZettlemoyerandMichaelCollins.2005. |               |     |     |         |       | Learn-     |
| ------------ | ------- | ----- | -------- | --- | ---- | --------- | ---------------------------------------- | ------------- | --- | --- | ------- | ----- | ---------- |
|              |         |       |          |     |      |           | ing to                                   | map sentences |     | to  | logical | form: | Structured |
| Bailin Wang, | Richard | Shin, | Xiaodong |     | Liu, | Oleksandr |                                          |               |     |     |         |       |            |
Polozov, and Matthew Richardson. 2020b. RAT- classificationwithprobabilisticcategorialgrammars.
SQL: Relation-aware schema encoding and linking In Proceedings of the Twenty-First Conference on
fortext-to-SQLparsers. InProceedingsofthe58th UncertaintyinArtificialIntelligence(UAI).
| Annual | Meeting | of  | the Association |     | for | Computa- |             |       |      |     |         |     |             |
| ------ | ------- | --- | --------------- | --- | --- | -------- | ----------- | ----- | ---- | --- | ------- | --- | ----------- |
|        |         |     |                 |     |     |          | Liang Zhao, | Hexin | Cao, | and | Yunsong |     | Zhao. 2021. |
tionalLinguistics(ACL).
|     |     |     |     |     |     |     | Gp: Context-free |     | grammar |     | pre-training |     | for text-to- |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------- | --- | ------------ | --- | ------------ |
sqlparsers.
| Ronald J. | Williams | and | David | Zipser. | 1989. | A learn- |     |     |     |     |     |     |     |
| --------- | -------- | --- | ----- | ------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
ingalgorithmforcontinuallyrunningfullyrecurrent
| neural | networks. | Neural |     | Computation, |     | 1(2):270– |     |     |     |     |     |     |     |
| ------ | --------- | ------ | --- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
280.
| Pengcheng | Yin    | and Graham  |                     | Neubig.  | 2017.  | A syn-    |     |     |     |     |     |     |     |
| --------- | ------ | ----------- | ------------------- | -------- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
| tactic    | neural | model       | for general-purpose |          |        | code gen- |     |     |     |     |     |     |     |
| eration.  | In     | Proceedings | of                  | the 55th | Annual | Meet-     |     |     |     |     |     |     |     |
ingoftheAssociationforComputationalLinguistics
| (ACL),pages440–450, |     |     | Vancouver, |     | Canada.Associ- |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | ---------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
ationforComputationalLinguistics.
321

A Computingsupervisionthroughtree
hashing
Ineverydecodingstept,wewishtocomputefor
| everytreez                      |     | inthefrontierF |     | ifz    | ∈      | Zgold . |
| ------------------------------- | --- | -------------- | --- | ------ | ------ | ------- |
|                                 | new |                |     | t+1    | new    | t       |
| Thisisachievedusingtreehashing. |     |                |     | First, | during |         |
preprocessing,foreveryheightt,wecomputethe
| goldhasheshgold |     | ,thehashvaluesofeverysub-tree |     |     |     |     |
| --------------- | --- | ----------------------------- | --- | --- | --- | --- |
t
ofzgold ofheightt,inarecursivefashionusinga
| Merkletreehash(Merkle,1987). |     |     |     | Specifically,we |     |     |
| ---------------------------- | --- | --- | --- | --------------- | --- | --- |
define:
| hash(z) | =      | g(label(z),hash(z |           | ),hash(z |        | ))  |
| ------- | ------ | ----------------- | --------- | -------- | ------ | --- |
|         |        |                   |           | l        | r      |     |
| Where   | g is a | simple hash       | function, | z        | ,z are | the |
l r
| leftandrightchildrenofz, |     |        | andlabel(·)givesthe |     |     |     |
| ------------------------ | --- | ------ | ------------------- | --- | --- | --- |
| nodetype(suchasσ         |     | andΠ). |                     |     |     |     |
ineachdecodingstept,
| Duringtraining, |          |            |     |              |     | since |
| --------------- | -------- | ---------- | --- | ------------ | --- | ----- |
| the hash        | function | is defined |     | recursively, | we  | can   |
computethefrontierhashesusingthehashvalues
| ofthecurrentbeam. |         | Then,foreveryfrontierhash |     |          |         |     |
| ----------------- | ------- | ------------------------- | --- | -------- | ------- | --- |
| we can            | perform | a lookup                  | to  | check if | hash(z) | ∈   |
| hgold . Both      | the     | hash computation          |     | and      | lookup  | are |
t
doneinparallelforallfrontiertreesusingtheGPU.
B ExamplesforRelationalAlgebraTrees
| We show | multiple | examples |     | of relation | algebra |     |
| ------- | -------- | -------- | --- | ----------- | ------- | --- |
treesalongwiththecorrespondingSQLquery,for
betterunderstandingofthemappingbetweenthe
two.
322

Π
|     | G count |                     |                      |               | σ          |         |          |
| --- | ------- | ------------------- | -------------------- | ------------- | ---------- | ------- | -------- |
|     |         | *                   |                      | ∧             |            |         | ×        |
|     |         |                     | =                    |               | =          | flights | airports |
|     |         | flights.destairport | airports.airportcode | airports.city | ’Aberdeen’ |         |          |
Π
|     |         | κ                     |                      |               | σ          |         |          |
| --- | ------- | --------------------- | -------------------- | ------------- | ---------- | ------- | -------- |
|     |         | κ                     |                      | ∧             |            |         | κ        |
|     | G count |                       | =                    |               | =          |         | ×        |
|     |         | * flights.destairport | airports.airportcode | airports.city | ’Aberdeen’ | flights | airports |
Figure 9: Unbalanced and balanced relational algebra trees for the utterance “How many flights arriving in
Aberdeen city?”, where the corresponding SQL query is SELECT COUNT( * ) FROM flights JOIN
airports ON flights.destairport = airports.airportcode WHERE airports.city
= ’Aberdeen’.
λ
|     | 1   |     |     | τ   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
asc
|     | transcripts.transcript_date |     |                             |     |                           | Π   |             |
| --- | --------------------------- | --- | --------------------------- | --- | ------------------------- | --- | ----------- |
|     |                             |     |                             |     | (cid:116)                 |     | transcripts |
|     |                             |     | transcripts.transcript_date |     | transcripts.other_details |     |             |
λ
|     | κ   |     |     | τ   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
asc
|     | κ   | κ   |     |     |           | Π   |     |
| --- | --- | --- | --- | --- | --------- | --- | --- |
|     | κ   | κ   |     |     | (cid:116) |     | κ   |
1 transcripts.transcript_date transcripts.transcript_date transcripts.other_details transcripts
Figure 10: Unbalanced and balanced relational algebra trees for the utterance “When is the first
transcript released? List the date and details.”, where the corresponding SQL query is SELECT
transcripts.transcript_date , transcripts.other_details FROM transcripts
| ORDER | BY transcripts.transcript_date |     |     | ASC | LIMIT 1. |     |     |
| ----- | ------------------------------ | --- | --- | --- | -------- | --- | --- |
323

Π
| G   |     |     |     |     |     | σ   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
count
| *   |     |     |     | ∧   |     |           | ×       |
| --- | --- | --- | --- | --- | --- | --------- | ------- |
|     |     | ∧   |     |     |     | ∧         | × pets  |
|     | =   |     | =   |     | =   | = student | has_pet |
student.stuid has_pet.stuid has_pet.petid pets.petid student.sex ’F’ pets.pettype ’dog’
Π
| κ   |     |     |     |     |     | σ   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
| κ   |     |     |     | ∧   |     |     | κ   |
| κ   |     | ∧   |     |     |     | ∧   | ×   |
| G   | =   |     | =   |     | =   | =   | × κ |
count
* student.stuid has_pet.stuid has_pet.petid pets.petid student.sex ’F’ pets.pettype ’dog’ student has_pet pets
Figure 11: Unbalanced and balanced relational algebra trees for the utterance “How many dog pets are raised
by female students?”, where the corresponding SQL query is SELECT COUNT( * ) FROM student
JOIN has_pet ON student.stuid = has_pet.stuid JOIN pets ON has_pet.petid =
| pets.petid | WHERE student.sex |     | = ’F’ | AND pets.pettype |     | = ’dog’. |     |
| ---------- | ----------------- | --- | ----- | ---------------- | --- | -------- | --- |
Π
|     |     |     | G   |     | matches |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- |
count
δ
matches.loser_name
Π
|     |     |     | G                  | count | κ       |     |     |
| --- | --- | --- | ------------------ | ----- | ------- | --- | --- |
|     |     |     |                    | δ     | κ       |     |     |
|     |     |     | matches.loser_name |       | matches |     |     |
Figure12: Unbalancedandbalancedrelationalalgebratreesfortheutterance“Findthenumberofdistinctname
oflosers.”,wherethecorrespondingSQLqueryis SELECT COUNT( DISTINCT matches.loser_name
| ) FROM matches. |     |     |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- |
324