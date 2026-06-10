|     |     |     |     | A Survey | on In-context |     | Learning |     |     |     |
| --- | --- | --- | --- | -------- | ------------- | --- | -------- | --- | --- | --- |
QingxiuDong1,LeiLi1,DamaiDai1,CeZheng1,JingyuanMa1,RuiLi1,HemingXia2,
JingjingXu3,ZhiyongWu4,BaobaoChang1,XuSun1,LeiLi5 andZhifangSui1
1 PekingUniversity2
TheHongKongPolytechnicUniversity
|     |     | 3 ByteDance4 |     |     | ShanghaiAILab5 |     |     |     |     |     |
| --- | --- | ------------ | --- | --- | -------------- | --- | --- | --- | --- | --- |
CarnegieMellonUniversity
dqx@stu.pku.edu.cn,szf@pku.edu.cn
|     |     | Abstract |     |     |     |     |                | Review: Delicious food!                        | Sentiment: Positive |     |
| --- | --- | -------- | --- | --- | --- | --- | -------------- | ---------------------------------------------- | ------------------- | --- |
|     |     |          |     |     |     |     | kDemonstration | Review: The food is awful. Sentiment: Negative |                     |     |
Examples
|       |                |         |              |     |               |     |                    | …                         | …                   |     |
| ----- | -------------- | ------- | ------------ | --- | ------------- | --- | ------------------ | ------------------------- | ------------------- | --- |
|       |                |         |              |     |               |     |                    | Review: Terrible dishes!  | Sentiment: Negative |     |
| With  | the increasing |         | capabilities |     | of large lan- |     | Template           | New                       |                     |     |
|       |                |         |              |     |               |     | Review: [Text]     | Query  Review: Good meal! | Sentiment:          |     |
| guage | models         | (LLMs), | in-context   |     | learning      |     |                    |                           |                     |     |
|       |                |         |              |     |               |     | Sentiment: [Label] |                           | Input               |     |
(ICL)hasemergedasanewparadigmfornat-
|     |     |     |     |     |     |     | Text Label | Large Language Model |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------------------- | --- | --- |
urallanguageprocessing(NLP),whereLLMs Delicious food!   1 Parameter Freeze
|                                         |             |     |                       |         |             |        | T h e   f o o d  i s   a w ful. 0 |               |           |         |
| --------------------------------------- | ----------- | --- | --------------------- | ------- | ----------- | ------ | --------------------------------- | ------------- | --------- | ------- |
| makepredictionsbasedoncontextsaugmented |             |     |                       |         |             |        |                                   |               | Output    |         |
|                                         |             |     |                       |         |             |        | Te r r i b l e  d i s h e s!      | 0             |           |         |
| withafewexamples.                       |             |     | Ithasbeenasignificant |         |             |        | … …                               |               | Positive  |         |
| trend                                   | to explore  | ICL | to evaluate           |         | and extrap- |        |                                   |               |           |         |
|                                         |             |     |                       |         |             | Figure | 1: Illustration                   | of in-context | learning. | ICL re- |
| olate                                   | the ability | of  | LLMs.                 | In this | paper, we   |        |                                   |               |           |         |
quiresapromptcontextcontainingafewdemonstration
aimtosurveyandsummarizetheprogressand
|            |     |         |          |         |          | exampleswritteninnaturallanguagetemplates. |              |              |                       | Taking |
| ---------- | --- | ------- | -------- | ------- | -------- | ------------------------------------------ | ------------ | ------------ | --------------------- | ------ |
| challenges |     | of ICL. | We first | present | a formal |                                            |              |              |                       |        |
|            |     |         |          |         |          | this                                       | prompt and a | query as the | input, large language |        |
definitionofICLandclarifyitscorrelationto
modelsareresponsibleformakingpredictions.
| relatedstudies. |     | Then,weorganizeanddiscuss |     |     |     |     |     |     |     |     |
| --------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
advancedtechniques,includingtrainingstrate-
gies,promptdesigningstrategies,andrelated
pieceofpromptcontexttogethertoformtheinput,
| analysis. | Additionally,weexplorevariousICL |     |     |     |     |     |     |     |     |     |
| --------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
applicationscenarios,suchasdataengineering whichisthenfedintothelanguagemodelforpre-
diction. Differentfromsupervisedlearning,which
| andknowledgeupdating. |     |     | Finally,weaddress |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
thechallengesofICLandsuggestpotentialdi- requires a training stage that uses backward gra-
rectionsforfurtherresearch. Wehopethatour dients to update model parameters, ICL does not
workcanencouragemoreresearchonuncover- performparameterupdates. Themodelisexpected
inghowICLworksandimprovingICL.
tolearnthepatternhiddeninthedemonstrationand
accordinglymaketherightprediction.
1 Introduction
Asanewparadigm,ICLhasmultipleattractive
Withthescalingofmodelsizeanddatasize(Brown advantages. First,sincethedemonstrationiswrit-
teninnaturallanguage,itprovidesaninterpretable
etal.,2020;Chowdheryetal.,2023;OpenAI,2023;
Touvron et al., 2023a,b), large language models interfacetocommunicatewithLLMs(Brownetal.,
(LLMs)demonstratethein-contextlearning(ICL) 2020). Thisparadigmmakesitmucheasiertoin-
corporatehumanknowledgeintoLLMsbychang-
| ability, | that is, | learning | from | a few | examples in |     |     |     |     |     |
| -------- | -------- | -------- | ---- | ----- | ----------- | --- | --- | --- | --- | --- |
thecontext. ManystudieshaveshownthatLLMs ing the demonstration and templates (Liu et al.,
can perform a series of complex tasks through 2022;Luetal.,2022;Weietal.,2022c;Wuetal.,
ICL,suchassolvingmathematicalreasoningprob- 2023b). Second, in-context learning is similar to
thedecisionprocessofhumanbeingsbylearning
| lems (Wei | et  | al., 2022c). | These |     | strong abilities |     |     |     |     |     |
| --------- | --- | ------------ | ----- | --- | ---------------- | --- | --- | --- | --- | --- |
havebeenwidelyverifiedasemergingabilitiesfor from analogy (Winston, 1980). Third, compared
largelanguagemodels(Weietal.,2022b). tosupervisedtraining,ICLisatraining-freelearn-
|     |          |               |     |          |             | ingframework. | Thiscouldnotonlygreatlyreduce |     |     |     |
| --- | -------- | ------------- | --- | -------- | ----------- | ------------- | ----------------------------- | --- | --- | --- |
| The | key idea | of in-context |     | learning | is to learn |               |                               |     |     |     |
fromanalogy. Figure1givesanexamplethatde- the computational costs for adapting the model
scribeshowlanguagemodelsmakedecisionsvia tonewtasks,butalsomakelanguage-model-as-a-
ICL. First, ICL requires a few demonstration ex- service(Sunetal.,2022)possibleandcanbeeasily
appliedtolarge-scalereal-worldtasks.
| amplestoformapromptcontext. |     |     |     |     | Theseexamples |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- |
areusuallywritteninnaturallanguagetemplates. Despitebeingpromising,therearealsointerest-
Then,ICLconcatenatesaqueryquestionandthe ingquestionsandintriguingpropertiesthatrequire
1107
Proceedingsofthe2024ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,pages1107–1128
November12-16,2024©2024AssociationforComputationalLinguistics

|     | Pre-training(§3.1) | PICL(Guetal.,2023),MEND(Lietal.,2024c),ICLM(Shietal.,2024) |     |     |     |     |
| --- | ------------------ | ---------------------------------------------------------- | --- | --- | --- | --- |
gniniarT
MetaICL(Minetal.,2022b),OPT-IML(Iyeretal.,2022),Super-NaturalInstructions(Wangetal.,2022b),
Warmup(§3.2) FLAN(Weietal.,2022a),ScalingInstruction(Chungetal.,2022),Self-supervisedICL(Chenetal.,2022),
SymbolTuning(Weietal.,2023a),RICL(Chuetal.,2023),ICLMarkup(Brunetetal.,2023)
KATE(Liuetal.,2022),SG-ICL(Kimetal.,2022),Self-Adaptive
(Wuetal.,2023b),PPL(Gonenetal.,2023),MI(Sorensenetal.,2022),
Unsupervised
InformativeScore(LiandQiu,2023),IDS(Qinetal.,2023),
|     |     | Selection |     | Votek(Suetal.,2023) |     |     |
| --- | --- | --------- | --- | ------------------- | --- | --- |
(§4.1.1)
EPR(Rubinetal.,2022),Q-Learning(Zhangetal.,2022a),
|     |     |     | Supervised | AdaICL(Mavromatisetal.,2023),Topic(Wangetal.,2023e), |     |     |
| --- | --- | --- | ---------- | ---------------------------------------------------- | --- | --- |
UDR(Lietal.,2023d)
Demonstration
(§4.1) Reformatting SG-ICL(Kimetal.,2022),StructruredPrompting(Haoetal.,2022b),
gninraeLtxetnoc-nI
|     |     | (§4.1.2) | AutoICL(Yangetal.,2023a),WICL(Yangetal.,2023b),ICV(Liuetal.,2024a) |     |     |     |
| --- | --- | -------- | ------------------------------------------------------------------ | --- | --- | --- |
Ordering
| ecnerefnI |     |     | GlobalE&LocalE(Luetal.,2022),ICCL(Liuetal.,2024b) |     |     |     |
| --------- | --- | --- | ------------------------------------------------- | --- | --- | --- |
(§4.1.3)
InstructionInduction(Honovichetal.,2023),Self-Instruct(Wangetal.,2023f),APE(Zhouetal.,2023c),
Instruction(§4.2)
Grimoire(Chenetal.,2024)
Scoring
Function(§4.3) Calibrate(Zhaoetal.,2021),ChannelModels(Minetal.,2022a),kNN-Prompting(Xuetal.,2023a)
|     |     |     | Pre-Training | Distribution(Chanetal.,2022;Wiesetal.,2023),Domain             |     |     |
| --- | --- | --- | ------------ | -------------------------------------------------------------- | --- | --- |
|     |     |     | Data         | (Shinetal.,2022;Hanetal.,2023b),Diversity(Yadlowskyetal.,2023) |     |     |
Pre-training
Stage(§5.1.1)
|     |     |     | Modeland | Architecture (Dingetal.,2024),Pre-trainingsteps(Weietal.,2022b), |     |     |
| --- | --- | --- | -------- | ---------------------------------------------------------------- | --- | --- |
|     |     |     | Training | Parameters(Brownetal.,2020;Weietal.,2022b)                       |     |     |
Influencing
Factors(§5.1) Mapping(Yooetal.,2022;Panetal.,2023a;Tangetal.,2023a),
InputLabels
Settings(Minetal.,2022c)
Inference
Stage(§5.1.2)
DiversityandSimplicity(Anetal.,2023),QuerySimilarity
sisylanA Demonstration (Liuetal.,2022;Anetal.,2023),Featurebias(Sietal.,2023),
Examples
Order(Luetal.,2022;Zhangetal.,2022b;Liuetal.,2023b)
Functional
InductionHeads(Olssonetal.,2022;Biettietal.,2023),
|     |     | Modules | ComputationalLayers(Wangetal.,2023b),AttentionModules(Lietal.,2023c) |     |     |     |
| --- | --- | ------- | -------------------------------------------------------------------- | --- | --- | --- |
(§5.2.1)
Learning
Mechanism(§5.2)
|     |     | Theoretical    | BayesianFramework                                                     | (Xieetal.,2022;Wangetal.,2023e;Jiang,2023), |     |     |
| --- | --- | -------------- | --------------------------------------------------------------------- | ------------------------------------------- | --- | --- |
|     |     | Interpretation | GradientDescent(Daietal.,2023a;Irieetal.,2022;Mahankalietal.,2023),   |                                             |     |     |
|     |     | (§5.2.2)       | Others(Gargetal.,2022;Akyüreketal.,2023;Lietal.,2023e;Panetal.,2023b) |                                             |     |     |
|     |     | Figure2:       | Taxonomyofin-contextlearning.                                         |                                             |     |     |
furtherinvestigationinICL.Althougharangeof delveintoanin-depthdiscussionofrelatedstudies,
vanillaGPTmodelsshowexcellentICLcapability, andwesummarizethetaxonomyinFigure2and
severalstudieshavefoundthatthiscapabilitycan thekeyfindingsinAppendixA.Wehighlightthe
besignificantlyimprovedthroughadaptationdur- challenges and potential directions and hope our
ingpretraining(Minetal.,2022b;Lietal.,2024c). workprovideausefulroadmapforbeginnersinter-
Moreover, theperformanceofICLissensitiveto estedinthisareaandshedlightonfutureresearch.
specificsettings,includingtheprompttemplate,the
selectionandorderofdemonstrationexamples,and 2 DefinitionandFormulation
otherfactors(Wangetal.,2023e;Liuetal.,2024b).
FollowingBrownetal.(2020),wehereprovidea
Additionally,optimizingtheconcisenessofdemon-
formaldefinitionofin-contextlearning:
strationexamplesandimprovingthecomputational
| efficiency  | of ICL arecritical | areas of     | ongoingre- |                     |                 |       |
| ----------- | ------------------ | ------------ | ---------- | ------------------- | --------------- | ----- |
|             |                    |              |            | In-context learning | is a paradigm   | that  |
| search (Liu | et al., 2024a).    | Furthermore, | despite    |                     |                 |       |
|             |                    |              |            | allows language     | models to learn | tasks |
preliminaryexplanations(Daietal.,2023a;Jiang,
givenonlyafewexamplesintheformof
2023),theunderlyingworkingmechanismofICL
demonstration.
remainsunclearandrequiresfurtherinvestigation.
WiththerapidgrowthofstudiesinICL,oursur- Formally, given a query input text x and a set
vey aims to sensitize the community toward the of candidate answers Y = y ,...,y , a pre-
|     |     |     |     |     | 1   | m   |
| --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | {   | }   |
current progress. In the following sections, we trainedlanguagemodel takesthecandidatean-
M
1108

| swerwiththemaximumscoreastheprediction,1 |     |               |     |     |          |       | Pre-training    |     |     |     | Warmup         |     |
| ---------------------------------------- | --- | ------------- | --- | --- | -------- | ----- | --------------- | --- | --- | --- | -------------- | --- |
|                                          |     |               |     | C.  | C        |       | Original Corpus |     |     |     | Different task |     |
| conditioned                              | a   | demonstration |     | set | contains |       |                 |     |     |     |                |     |
|                                          |     |               |     |     |          | T e x | t               |     |     |     | Prompts        |     |
anoptionaltaskinstructionI andk demonstration a b o u t Topic1 Topic2 Topic1Topic2
|                |       |           |        |                  |           |         |          | Retrieve |              |     | Instruction |        |
| -------------- | ----- | --------- | ------ | ---------------- | --------- | ------- | -------- | -------- | ------------ | --- | ----------- | ------ |
| examples,thusC |       | =         | I,s(x  | ,y ),...,s(x     | ,y )      |         |          |          |              |     |             |        |
|                |       |           | {      | 1 1              | k k }     | T e x t |          | T        | e x t Topic2 |     | x y         | x y x* |
|                |       |           |        |                  |           | a b o u | t Topic1 | a b      | o u t        |     | 1 1         | 2 2    |
| or C =         | s(x ′ | 1 ,y 1 ,I | ),..., | s(x ′ k ,y k ,I) | , wh er e |         |          |          |              |     |             |        |
|                | {     |           |        |                  | }         |         |          |          |              |     |             |        |
s (x ,y ,I) is an example written in natural lan- x x ··· Xn-1 LM x Pretrained LM y*
| ′ i                      | i             |     |          |                    |        | 1        | 2                                       |     |     | n   |     |     |
| ------------------------ | ------------- | --- | -------- | ------------------ | ------ | -------- | --------------------------------------- | --- | --- | --- | --- | --- |
| guageaccordingtothetask. |               |     |          | Dependingonwhether |        |          |                                         |     |     |     |     |     |
|                          |               |     |          |                    |        | Figure3: | Illustrationofmodeltrainingmethodstoen- |     |     |     |     |     |
| k and the                | demonstration |     | examples | belong             | to the |          |                                         |     |     |     |     |     |
hanceICLcapabilitiesthroughtwodifferentstages:pre-
sametask,itcanbecategorizedastask-specificICL
trainingandwarmup.
andcross-taskICL.Inthelatter,differentexamples
| have their       | own | instructions.               |     | The likelihood | of a |     |     |     |     |     |     |     |
| ---------------- | --- | --------------------------- | --- | -------------- | ---- | --- | --- | --- | --- | --- | --- | --- |
| candidateanswery |     | j comesfromascoringfunction |     |                |      |     |     |     |     |     |     |     |
makingmodelslearntoreasonacrosspriordemon-
f onthewholeinputsequence:
|     |     |     |     |          |     | strations.                                 | Differently,Lietal.(2024c)introduced |     |             |     |          |           |
| --- | --- | --- | --- | -------- | --- | ------------------------------------------ | ------------------------------------ | --- | ----------- | --- | -------- | --------- |
|     |     |     |     |          |     | a meta-distillation                        |                                      |     | pretraining |     | process, | which al- |
|     | P(y | x)  | f   | (y ,C,x) | (1) |                                            |                                      |     |             |     |          |           |
|     |     | j   | ≜   | j        |     |                                            |                                      |     |             |     |          |           |
|     |     | |   | M   |          |     | lowsLLMstoreasonwithdistilleddemonstration |                                      |     |             |     |          |           |
vectors,therebyenhancingICLefficiencywithout
Thefinalpredictedlabelyˆisthecandidateanswer
compromisingitseffectiveness.
withthehighestprobability:
|     | yˆ= | argmaxP(y |       | x). | (2) |         |        |            |     |     |         |             |
| --- | --- | --------- | ----- | --- | --- | ------- | ------ | ---------- | --- | --- | ------- | ----------- |
|     |     |           |       | j   |     | 3.2     | Warmup |            |     |     |         |             |
|     |     |           | yj∈ Y | |   |     |         |        |            |     |     |         |             |
|     |     |           |       |     |     | Another | way    | to enhance |     | ICL | ability | is adding a |
Accordingtothedefinition,wecanseethatICL
differsfromrelatedconceptsasfollows: (1)Prompt continual training stage between pretraining and
|           |                                     |     |     |     |     | ICL inference, |        | which | we          | call | model warmup | for      |
| --------- | ----------------------------------- | --- | --- | --- | --- | -------------- | ------ | ----- | ----------- | ---- | ------------ | -------- |
| Learning: | promptscanbediscretetemplatesorsoft |     |     |     |     |                |        |       |             |      |              |          |
|           |                                     |     |     |     |     | short.         | Warmup | is    | an optional |      | procedure    | for ICL, |
parametersthatencouragethemodeltopredictthe
desiredoutput. ICLcanberegardedasasubclass whichadjustsLLMsbeforeinferencebymodifying
of prompt tuning where the demonstration exam- oraddingparameters.
plesarepartoftheprompt. Liuetal.(2023c)made As most pretraining data are not tailored for
athoroughsurveyonpromptlearning,butICLwas ICL (Chen et al., 2022), researchers have intro-
notincludedintheirstudy. (2)Few-shotLearning: duced various warmup strategies to bridge the
few-shotlearningisageneralmachinelearningap- gapbetweenpretrainingandICLinference. Both
proachthatinvolvesadaptingmodelparametersto Min et al. (2022b) and Wang et al. (2022b) pro-
performataskwithalimitednumberofsupervised
|     |     |     |     |     |     | posed | to continually |     | finetune |     | LLMs | on a broad |
| --- | --- | --- | --- | --- | --- | ----- | -------------- | --- | -------- | --- | ---- | ---------- |
examples(WangandYao,2019). Incontrast,ICL rangeoftaskswithmultipledemonstrationexam-
doesnotrequireparameterupdatesandisdirectly ples, which boosts ICL abilities. To encourage
performedonpretrainedLLMs. themodeltolearninput-labelmappingsfromthe
|     |     |     |     |     |     | context, | Wei | et al. | (2023a) | proposed | symbol | tun- |
| --- | --- | --- | --- | --- | --- | -------- | --- | ------ | ------- | -------- | ------ | ---- |
3 ModelTraining ing,whichsubstitutesnaturallanguagelabels(e.g.,
“positive/negativesentiment”)witharbitrarysym-
AlthoughLLMshavedemonstratedpromisingICL
|     |     |     |     |     |     | bols(e.g.,“foo/bar”). |     |     | Chenetal.(2022)proposed |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ----------------------- | --- | --- | --- |
capabilitydirectly,manystudiesrevealedthatthese
|     |     |     |     |     |     | a self-supervised |     |     | method | to  | align raw | text with |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | ------ | --- | --------- | --------- |
ICLcapabilitiescanbefurtherenhancedthrough
|     |     |     |     |     |     | ICL formats |     | in downstream |     | tasks. | Besides, | mul- |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------------- | --- | ------ | -------- | ---- |
specializedtrainingbeforeinference(Chenetal.,
tiplestudieshaveindicatedthepotentialvalueof
2022;Guetal.,2023;Shietal.,2024).
instructions(Mishraetal.,2021;Weietal.,2022a).
|     |     |     |     |     |     | Tuning | the | 137B | LaMDA-PT |     | (Thoppilan | et al., |
| --- | --- | --- | --- | --- | --- | ------ | --- | ---- | -------- | --- | ---------- | ------- |
3.1 Pretraining
|     |     |     |     |     |     | 2022) | on over | 60  | datasets | verbalized |     | via natural |
| --- | --- | --- | --- | --- | --- | ----- | ------- | --- | -------- | ---------- | --- | ----------- |
OnestraightforwarddirectiontoboosttheICLca-
languageinstructiontemplates,FLAN(Weietal.,
| pability | of LLMs | is  | through | pretraining | or con- |     |     |     |     |     |     |     |
| -------- | ------- | --- | ------- | ----------- | ------- | --- | --- | --- | --- | --- | --- | --- |
2022a)improvestheabilityofLLMstofollowin-
| tinual pretraining. |     | For | instance, | Gu  | et al. (2023) |     |     |     |     |     |     |     |
| ------------------- | --- | --- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
structions,boostingboththezero-shotandfew-shot
| and Shi  | et al.  | (2024) | proposed    | to reorganize | pre-      |                 |     |     |                         |     |     |     |
| -------- | ------- | ------ | ----------- | ------------- | --------- | --------------- | --- | --- | ----------------------- | --- | --- | --- |
|          |         |        |             |               |           | ICLperformance. |     |     | Chungetal.(2022)andWang |     |     |     |
| training | corpora | by     | aggregating | related       | contexts, |                 |     |     |                         |     |     |     |
etal.(2022b)proposedtofurtherscaleupinstruc-
1Y couldbeclasslabelsorasetoffree-textphrases. tiontuningwithmorethan1000+taskinstructions.
1109

4 PromptDesigning tasks,theyareheuristicandsub-optimalduetothe
|     |     |     |     |     |     | lack of | task-specific | supervision. |     | To  | address | this |
| --- | --- | --- | --- | --- | --- | ------- | ------------- | ------------ | --- | --- | ------- | ---- |
Inthissection,wefocusontheprinciplesofICL
issue,numeroussupervisedmethodshavebeende-
duringinference,includingdemonstrationorgani-
veloped(Rubinetal.,2022;Yeetal.,2023;Wang
zation(§4.1)andinstructionformatting(§4.2).
|     |     |     |     |     |     | et al., 2023e; | Zhang | et  | al., 2022a). |     | EPR | (Rubin |
| --- | --- | --- | --- | --- | --- | -------------- | ----- | --- | ------------ | --- | --- | ------ |
etal.,2022)introducedatwo-stagemethodtotrain
4.1 DemonstrationOrganization
|     |     |     |     |     |     | adenseretrieverfordemonstrationselection. |     |     |     |     |     | Fora |
| --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | ---- |
Manystudieshaveshownthattheperformanceof
specificinput,itfirstutilizedunsupervisedmethods
ICLstronglyreliesonthedemonstrationsurface,
|           |     |            |             |     |          | (e.g., BM25) | to  | recall similar |     | examples | as  | candi- |
| --------- | --- | ---------- | ----------- | --- | -------- | ------------ | --- | -------------- | --- | -------- | --- | ------ |
| including | the | selection, | formatting, | and | ordering |              |     |                |     |          |     |        |
datesandthenusedthisdatatobuildasupervised
ofdemonstrationexamples(Zhaoetal.,2021;Lu
|              |     |                                 |     |     |     | denseretriever. | FollowingEPR,Lietal.(2023d) |     |     |     |     |     |
| ------------ | --- | ------------------------------- | --- | --- | --- | --------------- | --------------------------- | --- | --- | --- | --- | --- |
| etal.,2022). |     | Inthissubsection,wesurveydemon- |     |     |     |                 |                             |     |     |     |     |     |
adoptedaunifieddemonstrationretrievertoselect
| stration | organization |     | strategies | and classify | them |                                     |     |     |     |     |             |     |
| -------- | ------------ | --- | ---------- | ------------ | ---- | ----------------------------------- | --- | --- | --- | --- | ----------- | --- |
|          |              |     |            |              |      | demonstrationsacrossdifferenttasks. |     |     |     |     | Unlikeprior |     |
intothreecategories,asshowninTable1.
workthatretrievesindividualdemonstrations,Ye
4.1.1 DemonstrationSelection
etal.(2023)proposedretrievingentiredemonstra-
tionsetstomodelinter-relationshipsbetweenex-
Demonstrationsselectionaimstoanswerafunda-
mental question: Which samples are good exam- amples. Additionally, Mavromatis et al. (2023)
plesforICL? Wecategorizetherelatedstudiesinto introducedAdaICL,amodel-adaptivemethodthat
twoapproaches: unsupervisedmethodsbasedon employs LLM to predict the unlabeled data set,
predefinedmetricsandsupervisedmethods. generatinganuncertaintyscoreforeachinstance.
|              |              |        |                   |     |           | Based  | on prompt | tuning,      | Wang |      | et al.    | (2023e) |
| ------------ | ------------ | ------ | ----------------- | --- | --------- | ------ | --------- | ------------ | ---- | ---- | --------- | ------- |
|              |              |        | A straightforward |     | ap-       |        |           |              |      |      |           |         |
| Unsupervised |              | Method |                   |     |           |        |           |              |      |      |           |         |
|              |              |        |                   |     |           | viewed | LLMs as   | topic models |      | that | can infer | con-    |
| proach       | to selecting |        | ICL examples      | is  | to choose |        |           |              |      |      |           |         |
ceptsθ
fromafewdemonstrationsandgenerateto-
thenearestneighborsofinputinstancesbasedon
|                    |     |      |               |        |         | kensbasedontheseconcepts. |     |     | Theyrepresentlatent |     |     |     |
| ------------------ | --- | ---- | ------------- | ------ | ------- | ------------------------- | --- | --- | ------------------- | --- | --- | --- |
| their similarities |     | (Liu | et al., 2022; | Tanwar | et al., |                           |     |     |                     |     |     |     |
conceptswithtask-relatedconcepttokens,which
| 2023; Qin      | et  | al., 2023). | Distance   | metrics, | such    |             |             |     |     |       |            |     |
| -------------- | --- | ----------- | ---------- | -------- | ------- | ----------- | ----------- | --- | --- | ----- | ---------- | --- |
|                |     |             |            |          |         | are learned | to maximize |     | P(y | x,θ). | Demonstra- |     |
| as L2 distance |     | or cosine   | similarity | based    | on sen- |             |             |     |     | |     |            |     |
tionsareselectedbasedontheirlikelihoodtoinfer
tenceembeddings,arecommonlyusedforthispur-
|       |              |     |            |        |          | theconceptvariableusingP(θ |     |     |     | x,y). | Additionally, |     |
| ----- | ------------ | --- | ---------- | ------ | -------- | -------------------------- | --- | --- | --- | ----- | ------------- | --- |
| pose. | For example, |     | Liu et al. | (2022) | proposed |                            |     |     |     |       |               |     |
|
|     |     |     |     |     |     | reinforcement | learning |     | was introduced |     | by  | Zhang |
| --- | --- | --- | --- | --- | --- | ------------- | -------- | --- | -------------- | --- | --- | ----- |
KATE,thefirstkNN-basedunsupervisedretriever
|                                 |     |     |     |                |     | etal.(2022a)forexampleselection. |     |     |     |     | Theyformu- |     |
| ------------------------------- | --- | --- | --- | -------------- | --- | -------------------------------- | --- | --- | --- | --- | ---------- | --- |
| forselectingin-contextexamples. |     |     |     | Similarly,k-NN |     |                                  |     |     |     |     |            |     |
lateddemonstrationselectionasaMarkovdecision
cross-lingualdemonstrationscanberetrievedfor
process(Bellman,1957)andselecteddemonstra-
multi-lingualICLtostrengthensource-targetlan-
|       |           |         |         |        |           | tions via | Q-learning. | The | action | is  | choosing | an  |
| ----- | --------- | ------- | ------- | ------ | --------- | --------- | ----------- | --- | ------ | --- | -------- | --- |
| guage | alignment | (Tanwar | et al., | 2023). | Su et al. |           |             |     |        |     |          |     |
example,andtherewardisdefinedastheaccuracy
(2023)proposedtocombinegraphsandconfidence
ofalabeledvalidationset.
scorestoselectdiverseandrepresentativeexamples.
Inordertohaveamoreintuitivecomparisonof
| In addition | to  | distance | metrics, | mutual | informa- |     |     |     |     |     |     |     |
| ----------- | --- | -------- | -------- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
theperformanceofseveralunsupervisedmethods,
tion(Sorensenetal.,2022)andperplexity(Gonen
|               |     |             |          |     |            | we select  | topk (Liu | et al.,        | 2022), | votek      | (Su | et al., |
| ------------- | --- | ----------- | -------- | --- | ---------- | ---------- | --------- | -------------- | ------ | ---------- | --- | ------- |
| et al., 2023) |     | have proven | valuable | for | prompt se- |            |           |                |        |            |     |         |
|               |     |             |          |     |            | 2023), mdl | (Wu       | et al., 2023b) |        | to conduct |     | experi- |
lectionwithoutlabeledexamplesorspecificLLMs.
|     |     |     |     |     |     | ments. TheresultisshowninTable2. |     |     |     |     | Thedetails |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | ---------- | --- |
Furthermore,usingoutputscoresofLLMsasunsu-
oftheexperimentcanbefoundinAppendixB.
pervisedmetricshasshowneffectivenessindemon-
| stration | selection | (Wu | et al., 2023b; | Nguyen | and |     |     |     |     |     |     |     |
| -------- | --------- | --- | -------------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
4.1.2 DemonstrationReformatting
| Wong,2023;LiandQiu,2023). |     |     |     | Particularly,Wu |     |             |             |     |           |          |     |      |
| ------------------------- | --- | --- | --- | --------------- | --- | ----------- | ----------- | --- | --------- | -------- | --- | ---- |
|                           |     |     |     |                 |     | In addition | to directly |     | selecting | examples |     | from |
etal.(2023b)selectedthebestsubsetpermutation
trainingdata,anotherresearchtrendinvolvesutiliz-
ofkNNexamplesbasedonthecodelengthfordata
ingLLMstoreformattherepresentationofexist-
| transmission |     | to compress | label | y given | x and C. |     |     |     |     |     |     |     |
| ------------ | --- | ----------- | ----- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- |
ingdemonstrations(Kimetal.,2022;Yangetal.,
| Li and | Qiu (2023) |     | used infoscore, | i.e., | the aver- |     |     |     |     |     |     |     |
| ------ | ---------- | --- | --------------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
2023a;Haoetal.,2022b;Yangetal.,2023b;Liu
|        | P(y x | ,y ,x)P(y | x)  | (x,y) |          |                             |     |     |     |                 |     |     |
| ------ | ----- | --------- | --- | ----- | -------- | --------------------------- | --- | --- | --- | --------------- | --- | --- |
| age of |       | i i       | for | all   | pairs in |                             |     |     |     |                 |     |     |
|        | |     |           | |   |       |          | etal.,2024a;Lietal.,2024a). |     |     |     | Forinstance,Kim |     |     |
avalidationsetwithadiversityregularization.
etal.(2022)proposedgeneratingdemonstrations
Supervised Method Though off-the-shelf re- directlyfromLLMstoreducetherelianceonexter-
trieversofferconvenientservicesforextensiveNLP naldemonstrationdata. StructuredPrompting(Hao
1110

| Category |     |                        | Methods |     | DemonstrationAcquisition |     |     | LLMs  |     | Features          |     |
| -------- | --- | ---------------------- | ------- | --- | ------------------------ | --- | --- | ----- | --- | ----------------- | --- |
|          |     | KATE(Liuetal.,2022)    |         |     | Humandesign              |     |     | GPT-3 |     | KNNSelection      |     |
|          |     | MI(Sorensenetal.,2022) |         |     | Humandesign              |     |     | GPT-3 |     | MutualInformation |     |
Demonstration EPR(Rubinetal.,2022) Humandesign GPT-{J,3}/CodeX Score-basedRetrieval
Selection IDS(Qinetal.,2023) Humandesign GPT-3.5 IterativeSelection
AdaICL(Mavromatisetal.,2023) Humandesign GPT-{J,Neo} SelectiveDemonstration
|     |     | UDR(Lietal.,2023d) |     |     | Humandesign |     | GPT-Neo-2.7B |     |     | UnifiedRetrieval |     |
| --- | --- | ------------------ | --- | --- | ----------- | --- | ------------ | --- | --- | ---------------- | --- |
SG-ICL(Kimetal.,2022) LMgenerated GPT-J AutoDemonstrationGeneration
Demonstration AutoICL(Yangetal.,2023a) LMgenerated GPT-3.5-Turbo-0301 ReasoningPathGeneration
Reformatting MSP(Yangetal.,2023b) Humandesign GPTseries AdjustingDemonstrationWeight
ICV(Liuetal.,2024a) Humandesign Falcon-7b/Llama-7b DemonstrationEmbedding
Demonstration GlobalE&LocalE(Luetal.,2022) Humandesign GPT-{2,3} BestOrderSelection
Ordering ICCL(Liuetal.,2024b) Humandesign Llama2/Mixtral/Qwen OrderingfromSimpletoComplex
|     |     |     | Table1: Summaryofrepresentativedemonstrationdesigningmethods. |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Model Method SST5 SST2 CQA SNLI News Avg 4.1.3 DemonstrationOrdering
topk 40.1 74.9 30.2 39.7 62.7 49.5 Ordering the selected demonstration examples is
| GPT2 | votek | 32.4 | 51.0 29.8 | 35.8 | 25.5 34.9 |     |     |     |     |     |     |
| ---- | ----- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- |
alsoanimportantaspectofdemonstrationorgani-
|     | mdl | 43.3 | 86.7 32.7 | 41.4 | 68.0 54.4 |     |     |     |     |     |     |
| --- | --- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- |
zation. Luetal.(2022)haveproventhatordersen-
topk 46.9 84.6 58.4 60.7 69.1 63.9 sitivityisacommonproblemandalwaysexistsfor
| GPT-J | votek | 33.8 | 87.3 63.4 | 43.1 | 25.3 50.6 |                |         |                              |         |               |          |
| ----- | ----- | ---- | --------- | ---- | --------- | -------------- | ------- | ---------------------------- | ------- | ------------- | -------- |
|       |       |      |           |      |           | variousmodels. |         | Tohandlethisproblem,previous |         |               |          |
|       | mdl   | 37.6 | 87.9 64.1 | 59.8 | 68.2 63.5 |                |         |                              |         |               |          |
|       |       |      |           |      |           | studies        | have    | proposed                     | several | training-free | meth-    |
|       | topk  | 54.1 | 83.3 76.3 | 68.2 | 64.9 69.4 |                |         |                              |         |               |          |
|       |       |      |           |      |           | ods for        | sorting | demonstration                |         | examples.     | Particu- |
| Qwen2 | votek | 55.3 | 86.9 76.1 | 51.6 | 65.3 67.0 |                |         |                              |         |               |          |
larly,Liuetal.(2022)arrangedexamplesbasedon
|     | mdl | 54.6 | 86.1 77.1 | 65.0 | 63.2 69.2 |     |     |     |     |     |     |
| --- | --- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- |
theirproximitytotheinput,positioningtheclosest
|     | topk | 53.0 | 90.3 76.1 | 64.0 | 74.0 71.5 |     |     |     |     |     |     |
| --- | ---- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- |
Llama3 votek 54.9 88.9 72.6 57.7 70.5 exampleastherightmostdemonstration. Luetal.
78.3
(2022)introducedglobalandlocalentropymetrics,
|     | mdl | 54.4 | 89.1 76.5 | 59.9 | 74.6 70.9 |     |     |     |     |     |     |
| --- | --- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- |
findingapositivecorrelationbetweenthesemetrics
| Table 2: | Fair | comparison | of demonstration |     | selection |                       |     |     |                       |     |     |
| -------- | ---- | ---------- | ---------------- | --- | --------- | --------------------- | --- | --- | --------------------- | --- | --- |
|          |      |            |                  |     |           | andtheICLperformance. |     |     | Consequently,theyuti- |     |     |
methods.CQAandNewsareabbreviationsofCommon-
lizedtheentropymetrictodeterminetheoptimal
| senseQAandAGNews,respectively. |                                      |     |     | Thebestresults |     |                        |        |           |                       |                |     |
| ------------------------------ | ------------------------------------ | --- | --- | -------------- | --- | ---------------------- | ------ | --------- | --------------------- | -------------- | --- |
|                                |                                      |     |     |                |     | demonstrationordering. |        |           | Additionally,ICCL(Liu |                |     |
| arebolded.                     | Ourexperimentsontopk(Liuetal.,2022), |     |     |                |     |                        |        |           |                       |                |     |
|                                |                                      |     |     |                |     | et al.,                | 2024b) | suggested | ranking               | demonstrations |     |
votek(Suetal.,2023),mdl(Wuetal.,2023b)showthat
theeffectivenessofICLexampleselectionmethodsare fromsimpletocomplex,therebygraduallyincreas-
ingthecomplexityofdemonstrationexamplesdur-
| model-dependent. |     | OnGPT-2,themdlmethodperforms |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
thebest,whileontheotherthreemodels,topkperforms ingtheinferenceprocess.
thebest.
4.2 InstructionFormatting
|     |     |     |     |     |     | A common   |          | way to format                     | demonstrations |     | is con-  |
| --- | --- | --- | --- | --- | --- | ---------- | -------- | --------------------------------- | -------------- | --- | -------- |
|     |     |     |     |     |     | catenating | examples | (x                                | ,y ),...,(x    | ,y  | ) with a |
|     |     |     |     |     |     |            |          |                                   | 1 1            | k   | k        |
|     |     |     |     |     |     | template   |          | directly. However,insometasksthat |                |     |          |
T
et al., 2022b) proposed to encode demonstration need complex reasoning (e.g., math word prob-
examplesseparatelywithspecialpositionalembed- lems and commonsense reasoning), it is not easy
dings,whicharethenprovidedtothetestexamples to learn the mapping from x to y with only k
i i
usingarescaledattentionmechanism. Diverging demonstrations. Although template engineering
from these methods, other approaches focus on hasbeenstudiedinprompting(Liuetal.,2023c),
modifyingthelatentrepresentationofdemonstra- someresearchersaimtodesignabetterformatof
tions(Liuetal.,2024a;Lietal.,2024a). Specifi- demonstrations for ICL by describing tasks with
cally,Liuetal.(2024a)developedIn-ContextVec- theinstructionI. Honovichetal.(2023)foundthat
tors(ICVs)derivedfromthelatentembeddingsof givenseveraldemonstrationexamples,LLMscan
demonstrationexamplesinLLMs. TheseICVsare generate task instructions themselves. Consider-
usedduringinferencetoadjustthelatentstatesof ing the generation abilities of LLMs, Zhou et al.
theLLM,therebyenhancingthemodel’sabilityto (2023c)proposedanAutomaticPromptEngineer
followthedemonstrationsmoreeffectively. forautomaticinstructiongenerationandselection.
1111

Method Target Efficiency Coverage Stability thein-contextlearningabilityiseasilyaffectedby
| Direct | (y  | C,x) +++ |     | +   | +   | changesinthedemonstrationexamples. |     |     |     |     |     |
| ------ | --- | -------- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | --- |
M j |
| PPL | PPL(S | )   | +   | +++ | +   |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j
| Channel | (x  | C,y ) | +   | +   | ++  |     |     |     |     |     |     |
| ------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
M | j
5 Analysis
| Table3: Summaryofdifferentscoringfunctions. |     |     |     |     | Cov- |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
erage refers to task coverage. The qualitative results TounderstandICL,recentstudiesattempttoinves-
for‘Efficiency’and‘Stability’metricsareelaboratedin tigatewhatinfluenceICLperformance(Shinetal.,
Table4andTable5,respectively.
|     |     |     |     |     |     | 2022; Yoo | et al., | 2022; | Kossen | et al., | 2023) and |
| --- | --- | --- | --- | --- | --- | --------- | ------- | ----- | ------ | ------- | --------- |
whyICLworks(Daietal.,2023a;Irieetal.,2022).
|     |     |     |     |     |     | In this | section, | we present | a detailed |     | elaboration |
| --- | --- | --- | --- | --- | --- | ------- | -------- | ---------- | ---------- | --- | ----------- |
Tofurtherimprovethequalityoftheautomatically
|     |     |     |     |     |     | of influencing |     | factors (§5.1) | and | learning | mecha- |
| --- | --- | --- | --- | --- | --- | -------------- | --- | -------------- | --- | -------- | ------ |
generatedinstructions,severalstrategieshavepro-
nisms(§5.2)ofICL,asillustratedinFigure4.
posedusingLLMstobootstrapoffitsowngenera-
| tions(Wangetal.,2023f;Chenetal.,2024). |     |     |     |     | Addi- |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
tionally,chain-of-thought(CoT)(Weietal.,2022c) 5.1 InfluencingFactors
| introduces | intermediate | reasoning |     | steps | between |     |     |     |     |     |     |
| ---------- | ------------ | --------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
Wediscussrelevantresearchaddressingwhatinflu-
inputsandoutputstoenhanceproblem-solvingand
encesICLperformance,includingfactorsbothin
| comprehension. |     | Recent | advancements |     | have also |     |     |     |     |     |     |
| -------------- | --- | ------ | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- |
thepretrainingstageandintheinferencestage.
emphasizedtheprocessofenhancingstep-by-step
| reasoning | in models | (Zhang | et  | al., 2023c; | Wang |     |     |     |     |     |     |
| --------- | --------- | ------ | --- | ----------- | ---- | --- | --- | --- | --- | --- | --- |
5.1.1 PretrainingStage
etal.,2022a;Zhouetal.,2023a).
|     |     |     |     |     |     | We first | introduce | factors | that | influence | the pre- |
| --- | --- | --- | --- | --- | --- | -------- | --------- | ------- | ---- | --------- | -------- |
4.3 ScoringFunction
|     |     |     |     |     |     | training | stage. | The diversity |     | of pretraining | cor- |
| --- | --- | --- | --- | --- | --- | -------- | ------ | ------------- | --- | -------------- | ---- |
Thescoringfunctiondetermineshowtotransform porasignificantlyimpactsICLperformance(Shin
etal.,2022;Yadlowskyetal.,2023;Raventósetal.,
thepredictionsofalanguagemodelintoanestima-
2023). Inparticular,Shinetal.(2022)foundthat
| tionofthelikelihoodofaspecificanswer. |     |     |     |     | TheDi- |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
rectmethodusestheconditionalprobabilityofcan- thesourcedomainismoreimportantthanthecor-
didateanswersrepresentedbytokensinthemodel’s pussize, suggestingthatcombiningmultiplecor-
|                              |     |     |     |               |     | pora may | lead | to the | emergence | of  | ICL ability. |
| ---------------------------- | --- | --- | --- | ------------- | --- | -------- | ---- | ------ | --------- | --- | ------------ |
| vocabulary(Brownetal.,2020). |     |     |     | Theanswerwith |     |          |      |        |           |     |              |
the highest probability is selected as the final an- Similarly,Raventósetal.(2023)empiricallyidenti-
swer,butthismethodrestrictstemplatedesignby fiedataskdiversitythresholdbeyondwhichLLMs
|           |        |        |          |         |          | exhibitstrongICLcapabilitiesinunseentasks. |     |     |     |     | An- |
| --------- | ------ | ------ | -------- | ------- | -------- | ------------------------------------------ | --- | --- | --- | --- | --- |
| requiring | answer | tokens | to be at | the end | of input |                                            |     |     |     |     |     |
otherlineofresearchinvestigatestheimpactofdata
| sequences. | Perplexity(PPL)isanothercommonly |     |     |     |     |     |     |     |     |     |     |
| ---------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
usedmetricthatcomputesthesentenceperplexity distributiononICL(Chanetal.,2022;Wiesetal.,
|                           |     |     |     |           |     | 2023). | For instance, | Chan | et  | al. (2022) | demon- |
| ------------------------- | --- | --- | --- | --------- | --- | ------ | ------------- | ---- | --- | ---------- | ------ |
| oftheentireinputsequenceS |     |     |     | = C,s(x,y | ,I) | ,      |               |      |     |            |        |
|                           |     |     | j   | {         | j } |        |               |      |     |            |        |
stratedthatICLcapabilityemergeswhenthetrain-
whichincludestokensfromdemonstrationexam-
ples C, the input query x, and the candidate la- ingdataexhibitsspecificdistributionalproperties,
bel y . PPL evaluates the probability of the sen- suchasburstiness,whereinitemsappearinclusters
j
ratherthanbeinguniformlydistributedovertime.
| tence, eliminating |     | token | position | limitations | but |     |     |     |     |     |     |
| ------------------ | --- | ----- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
requiring additional computation time. Min et al. Beyondtheseworks,severalstudieshaveinvesti-
(2022a)proposedusingchannelmodels(Channel) gatedtheimpactofmodelarchitectureandtraining
tocomputetheconditionalprobabilityinreverse, process on ICL performance (Wei et al., 2022b;
estimatingthelikelihoodoftheinputquerygiven Brown et al., 2020; Ding et al., 2024). Wei et al.
thelabel. Thisapproachrequireslanguagemodels (2022b)investigatedtheemergentabilitiesofmany
to generate every token in the input, potentially large-scale models on multiple tasks. They sug-
boosting performance under imbalanced training gestedthatapretrainedmodelacquiressomeemer-
data. Wesummarizeallthreescoringfunctionsin gent ICL abilities when it reaches a large scale
Table 3. Note that in Table 3, ‘Efficiency’ refers of pretraining steps or model parameters. Ding
to the language model inference latency; ‘Cover- et al. (2024) pointed out that the in-context sam-
age’reflectswhetherthemethodutilizestheoutput plesshouldattendtoeachotherduringinference,
probabilityofthelocaloralltokenpositionsinthe indicating that current causal LLMs may lead to
inputsequence; and‘Stability’indicateswhether suboptimalICLperformance.
1112

Pretraining Stage Factor Output Functional Modules
+ + Induction Heads
Large Language Model
Self-Attention
Corpus Architecture Train
Inference Stage Factor Theoretical Interpretation
Demonstration Order & Diversity Demonstrations Bayes Gradient Descent
Input 1 Input 2 ··· Inputk Posterior
Input-Label Distribution & Mapping Prior
Label 1 Label 2 ··· Label k
Likelihood
Demonstration-Query Similarity Query
Figure4: SummaryoffactorsthathavearelativelystrongcorrelationtoICLperformanceanddifferentperspectives
toexplainwhyICLworks.
5.1.2 InferenceStage isafocalpointinthestudyofICLmechanism(Ols-
sonetal.,2022;Biettietal.,2023;Daietal.,2023a;
During inference, there are also multiple proper-
Irieetal.,2022;Lietal.,2023c;Gaoetal.,2023;
tiesofdemonstrationexamplesthatinfluenceICL
Zhang et al., 2023b). Particularly, Olsson et al.
performance. Minetal.(2022c)provedthatinput-
(2022)identifiedspecificattentionheads,referred
labelsettingssuchasthepairingformat,theexpo-
toas“inductionheads”,thatcanreplicateprevious
sureoflabelspace,andtheinputdistributioncon-
patterns for next-token prediction, thus progres-
tributesubstantiallytoICLperformance. However,
sively developing ICL capabilities. Additionally,
contrary to the conclusion in Min et al. (2022c)
Wang et al. (2023b) focused on the information
thatinput-labelmappingmatterslittletoICL,latter
flow in Transformers and found that during the
studiesshowedthattheaccuratemappinginfluence
ICL process, demonstration label words serve as
ICL performance significantly (Yoo et al., 2022;
anchors,whichaggregateanddistributekeyinfor-
Pan et al., 2023a; Tang et al., 2023a). Wei et al.
mationforthefinalprediction.
(2023b)furtherpointedthatflippedorsemantically-
unrelatedinput-labelmappingalsocanbelearned.
5.2.2 TheoreticalInterpretation
Fromtheperspectiveofdemonstrationconstruc-
Inthissubsection,weintroducethetheoreticalin-
tion,recentliteraturefocusesonthediversityand
terpretationsofICLfromdifferentviews.
simplicityofdemonstrations(Anetal.,2023),the
order of samples (Lu et al., 2022; Zhang et al.,
BayesianView IntheBayesianframework,ICL
2022b; Liu et al., 2023b), and the similarity be-
isexplainedasimplicitBayesianinference,where
tweendemonstrationsandqueries(Liuetal.,2022).
modelsperformICLbyidentifyingasharedlatent
Forexample, Liuetal.(2022)foundthatdemon-
concept among examples (Xie et al., 2022; Wies
strationsampleswithembeddingsclosertothose
etal.,2023;Ahujaetal.,2023;Jiang,2023;Wang
ofthequerysamplestypicallyyieldbetterperfor-
etal.,2023e). Additionalperspectivessuggestthat
mance than those with more distant embeddings.
LLMs encode the Bayesian Model Averaging al-
Notably,despiteeffortstorefinedemonstrationsto
gorithmviatheattentionmechanism(Zhangetal.,
optimizetheperformance,therestillremainclear
2023b). Asthenumberofin-contextexamplesin-
featurebiasesduringICLinference(Sietal.,2023).
creases,implicitBayesianinferencebecomesanal-
Overcoming strong prior biases and ensuring the
ogoustokernelregression(Hanetal.,2023a).
modelgivesequalweighttoallcontextualinforma-
tionremainchallenges(Kossenetal.,2023). GradientDescentView Gradientdescentoffers
anothervaluablelensforunderstandingICL. Dai
5.2 LearningMechanism
etal.(2023a)identifiedadualformbetweenTrans-
Fromalearningmechanismperspective,wedelve formerattentionandgradientdescent,findingthat
intotheresearchaddressingwhyICLiseffective. GPT-basedICLbehavessimilarlytoexplicitfine-
tuning from multiple perspectives. Other studies
5.2.1 FunctionalModules
have attempted to establish connections between
TheICLcapabilityisintimatelyconnectedtospe- ICLandgradientdescentinsimplifiedregression
cificfunctionalmoduleswithinTransformers. As settings(vonOswaldetal.,2023;Ahnetal.,2023;
oneofthecorecomponents,theattentionmodule Mahankali et al., 2023; Li et al., 2023c). For in-
1113

stance,vonOswaldetal.(2023)showedthatlinear annotation, ICL generates relatively high-quality
attention-only Transformers with manually con- data at a lower cost, leading to improved perfor-
structed parameters are closely related to models mance.(Wangetal.,2021;Khorashadizadehetal.,
learnedbygradientdescent. Lietal.(2023c)found 2023;Dingetal.,2023). 2)ModelAugmentation:
thatself-attention-onlyTransformersexhibitsim- Thecontext-flexiblenatureofICLshowspromise
ilaritieswithmodelstrainedviagradientdescent. in model augmentation. It can enhance retrieval-
However,thesimplifiedsettingsusedinthesestud- augmentedmethodsbyprependinggroundingdoc-
ieshaveledtodebatesaboutthedirectapplicability umentstotheinput(Rametal.,2023). Addition-
oftheseconnectionsinreal-worldcontexts(Shen ally, ICL for retrieval demonstrates potential in
et al., 2024). Fu et al. (2023) argued that Trans- steeringmodelstowardsaferoutputs(Pandaetal.,
formers perform ICL on linear regression using 2023; Meade et al., 2023). 3) Knowledge Up-
higher-order optimization techniques rather than dating: LLMsoftencontainoutdatedorincorrect
gradientdescent. knowledge (Dong et al., 2023). ICL has demon-
stratedefficacyinrevisingsuchknowledgethrough
| OtherViews     | BeyondconnectingICLwithasin- |     |      |          |         |                   |                 |                   |          |        |
| -------------- | ---------------------------- | --- | ---- | -------- | ------- | ----------------- | --------------- | ----------------- | -------- | ------ |
|                |                              |     |      |          |         | carefully crafted | demonstrations, |                   | yielding | higher |
| gle algorithm, | researchers                  |     | have | analyzed | it from |                   |                 |                   |          |        |
|                |                              |     |      |          |         | success rates     | compared        | to gradient-based |          | meth-  |
variousperspectives,includingabilitydecoupling,
ods(DeCaoetal.,2021).
| algorithmiclearning,andinformationtheory. |     |     |     |     | Pan |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Asmentionedabove,ICLhasyieldedsignificant
etal.(2023b)decoupledICLcapabilitiesintotask
benefitsonbothtraditionalandemergentNLPap-
| recognitionabilityandtasklearningability, |       |           |             |     | each    |             |                                |     |     |     |
| ----------------------------------------- | ----- | --------- | ----------- | --- | ------- | ----------- | ------------------------------ | --- | --- | --- |
|                                           |       |           |             |     |         | plications. | ThetremendoussuccessofICLinNLP |     |     |     |
| manifesting                               | under | different | conditions. |     | Another |             |                                |     |     |     |
hasinspiredresearcherstoexploreitspotentialin
typicaltheoryabstractsICLasanalgorithmiclearn-
variousmodalitiesbeyondtext(elaboratedinAp-
| ing problem | (Akyürek |        | et al., | 2023;        | Garg et al., |                          |     |                     |     |     |
| ----------- | -------- | ------ | ------- | ------------ | ------------ | ------------------------ | --- | ------------------- | --- | --- |
|             |          |        |         |              |              | pendixD),includingvision |     | (Baretal.,2022;Wang |     |     |
| 2022; Li    | et al.,  | 2023e; | Bai et  | al., 2023b), | where        |                          |     |                     |     |     |
etal.,2023c),vision-language(Tsimpoukellietal.,
Transformersdynamicallyselectalgorithms,such
2021;Alayracetal.,2022),aswellasspeechappli-
asgradientdescentandridgeregression,tailoredto
cations(Wangetal.,2023a;Zhangetal.,2023d).
| differentICLinstances. |             |     | Moreover,HahnandGoyal |     |                |     |     |     |     |     |
| ---------------------- | ----------- | --- | --------------------- | --- | -------------- | --- | --- | --- | --- | --- |
| (2023) utilized        | information |     | theory                |     | to show an er- |     |     |     |     |     |
7 ChallengesandFutureDirections
| ror bound | for ICL | under | linguistically |     | motivated |     |     |     |     |     |
| --------- | ------- | ----- | -------------- | --- | --------- | --- | --- | --- | --- | --- |
assumptions,explaininghownext-tokenprediction Inthissection,wereviewexistingchallengesand
| canbringabouttheICLability. |            |         |      |       |           | discussfuturedirectionsforICL. |     |     |     |     |
| --------------------------- | ---------- | ------- | ---- | ----- | --------- | ------------------------------ | --- | --- | --- | --- |
| These                       | analytical | studies | have | taken | an essen- |                                |     |     |     |     |
tial step to explain ICL. However, most of them EfficiencyandScalability Theuseofdemonstra-
|                                     |     |     |     |     |         | tionsinICLintroducestwochallenges: |     |     |     | (1)higher |
| ----------------------------------- | --- | --- | --- | --- | ------- | ---------------------------------- | --- | --- | --- | --------- |
| focusedonsimpletasksandsmallmodels. |     |     |     |     | Extend- |                                    |     |     |     |           |
computationalcostswithanincreasingnumberof
| ing analysis | on  | extensive | tasks | and | large models |                |               |     |           |        |
| ------------ | --- | --------- | ----- | --- | ------------ | -------------- | ------------- | --- | --------- | ------ |
|              |     |           |       |     |              | demonstrations | (efficiency), | and | (2) fewer | learn- |
maybethenextsteptobeconsidered.
ablesamplesduetothemaximuminputlengthof
| 6 Application |     |     |     |     |     | LLMs(scalability). | Priorresearchhasattemptedto |     |     |     |
| ------------- | --- | --- | --- | --- | --- | ------------------ | --------------------------- | --- | --- | --- |
mitigatetheseissuesbydistillinglengthydemon-
| Given its | user-friendly |     | interface | and | lightweight |     |     |     |     |     |
| --------- | ------------- | --- | --------- | --- | ----------- | --- | --- | --- | --- | --- |
strationsintocompactvectors(Lietal.,2024d,c)or
promptingmethod,ICLhasbroadapplicationson
expeditingLLMinferencetimes(Liuetal.,2023d).
traditionalNLPtasks(Kimetal.,2022;Minetal.,
However,thesemethodsofteninvolveatrade-offin
| 2022b; | Zhu et al., | 2023b). | Particularly, |     | by using |     |     |     |     |     |
| ------ | ----------- | ------- | ------------- | --- | -------- | --- | --- | --- | --- | --- |
performanceornecessitateaccesstomodelparam-
demonstrationsthatexplicitlyguidethereasoning eters,whichisimpracticalforclosed-sourcemod-
process,ICLmanifestsremarkableeffectsontasks
elslikeChatGPTandClaude(Zhouetal.,2023b).
requiringcomplexreasoning(Weietal.,2022c;Li
|     |     |     |     |     |     | Thus, enhancing | the scalability |     | and efficiency | of  |
| --- | --- | --- | --- | --- | --- | --------------- | --------------- | --- | -------------- | --- |
etal.,2023b;Zhouetal.,2022)andcompositional
|     |     |     |     |     |     | ICL with | more demonstrations |     | remains | a signifi- |
| --- | --- | --- | --- | --- | --- | -------- | ------------------- | --- | ------- | ---------- |
generalization(Zhouetal.,2023a).
cantchallenge.
| We explore |     | several | emerging |     | and prevalent |     |     |     |     |     |
| ---------- | --- | ------- | -------- | --- | ------------- | --- | --- | --- | --- | --- |
applications of ICL, including data engineering, Generalization ICL heavily relies on high-
modelaugmentation,andknowledgeupdating. 1) qualitydemonstrationsselectedfromannotatedex-
Data Engineering: Unlike traditional methods amples, which are often scarce in low-resource
such as human annotation and noisy automatic languages and tasks. This scarcity poses a chal-
1114

| lengetothegeneralizationabilityofICL(Heetal., |     |     |     |     |     |     | References |     |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
2024). Giventhatthereisasubstantialdiscrepancy Rishabh Agarwal, Avi Singh, Lei M. Zhang, Bernd
intheavailabilityofannotatedhigh-resourcedata
Bohnet,LuisRosias,StephanieChan,BiaoZhang,
and low-resource data, the potential to leverage AnkeshAnand,ZaheerAbbas,AzadeNova,JohnD.
Co-Reyes,EricChu,FeryalBehbahani,Aleksandra
high-resourcedatatoaddresslow-resourcetasksis
|     |     |     |     |     |     |     | Faust, | and Hugo | Larochelle. |     | 2024. | Many-shot | in- |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------- | ----------- | --- | ----- | --------- | --- |
highlyappealing(Chatterjeeetal.,2024;Tanwar
|     |     |     |     |     |     |     | contextlearning. |     | Preprint,arXiv:2404.11018. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | -------------------------- | --- | --- | --- | --- |
etal.,2023).
KwangjunAhn,XiangCheng,HadiDaneshmand,and
Recentadvancesincontext- SuvritSra.2023. Transformerslearntoimplement
Long-contextICL
preconditionedgradientdescentforin-contextlearn-
| extended | LLMs | have | spurred | research | into | the |     |     |     |     |     |     |     |
| -------- | ---- | ---- | ------- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
ing. InAdvancesinNeuralInformationProcessing
impact of ICL when using an increasing number Systems36: AnnualConferenceonNeuralInforma-
tionProcessingSystems2023,NeurIPS2023,New
ofdemonstrationexamples(Agarwaletal.,2024;
Bertsch et al., 2024). However, researchers have Orleans,LA,USA,December10-16,2023.
foundthatincreasingthenumberofdemonstrations KabirAhuja,MadhurPanwar,andNavinGoyal.2023.
doesnotnecessarilyenhanceperformanceandmay In-context learning through the bayesian prism.
evenbedetrimental. Theseperformancedeclines CoRR,abs/2306.04891.
| indicateaneedforfurtherinvestigation. |                |     |           |               | Addition- |     |               |     |                  |     |                  |     |     |
| ------------------------------------- | -------------- | --- | --------- | ------------- | --------- | --- | ------------- | --- | ---------------- | --- | ---------------- | --- | --- |
|                                       |                |     |           |               |           |     | AI@Meta.2024. |     | Llama3modelcard. |     | Technicalreport, |     |     |
| ally, Li                              | et al. (2024b) |     | developed | LongICLBench, |           |     | Meta.         |     |                  |     |                  |     |     |
whichincludesdiverseextreme-labelclassification
|                  |     |         |            |     |         |     | Ekin Akyürek, |     | Dale Schuurmans, |       | Jacob | Andreas, |        |
| ---------------- | --- | ------- | ---------- | --- | ------- | --- | ------------- | --- | ---------------- | ----- | ----- | -------- | ------ |
| tasks, revealing |     | further | weaknesses |     | of LLMs | in  |               |     |                  |       |       |          |        |
|                  |     |         |            |     |         |     | Tengyu        | Ma, | and Denny        | Zhou. | 2023. | What     | learn- |
comprehendingextendeddemonstrations. ingalgorithmisin-contextlearning? investigations
|     |     |     |     |     |     |     | with linear | models. | In  | The Eleventh |     | International |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --- | ------------ | --- | ------------- | --- |
ConferenceonLearningRepresentations,ICLR2023,
8 Conclusion
Kigali,Rwanda,May1-5,2023.OpenReview.net.
In this paper, we comprehensively review the ex- Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc,
istingliteratureonICL,examiningadvancedtech- Antoine Miech, Iain Barr, Yana Hasson, Karel
Lenc,ArthurMensch,KatherineMillican,Malcolm
| niques, | conducting | analytical |     | studies, | discussing |     |                     |     |           |     |                 |     |     |
| ------- | ---------- | ---------- | --- | -------- | ---------- | --- | ------------------- | --- | --------- | --- | --------------- | --- | --- |
|         |            |            |     |          |            |     | Reynolds,etal.2022. |     | Flamingo: |     | avisuallanguage |     |     |
relevantapplications,andidentifyingcriticalchal-
|     |     |     |     |     |     |     | model | for few-shot | learning. |     | Advances | in  | Neural |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------------ | --------- | --- | -------- | --- | ------ |
lengesandpotentialdirectionsforfutureresearch. InformationProcessingSystems,35:23716–23736.
Toourknowledge,thisisthefirstcomprehensive
ShengnanAn,ZeqiLin,QiangFu,BeiChen,Nanning
surveydedicatedtoICL.Weaimtohighlightthe
Zheng,Jian-GuangLou,andDongmeiZhang.2023.
currentstateofresearchinICLandprovideinsights How do in-context examples affect compositional
toguidefutureworkinthispromisingarea. generalization? InProceedingsofthe61stAnnual
|     |     |     |     |     |     |     | Meeting | of the | Association | for | Computational |     | Lin- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ----------- | --- | ------------- | --- | ---- |
guistics(Volume1:LongPapers),ACL2023,Toronto,
Limitations
Canada,July9-14,2023,pages11027–11052.Asso-
ciationforComputationalLinguistics.
Thispaperoffersacomprehensiveexaminationand
JinzeBai,ShuaiBai,YunfeiChu,ZeyuCui,KaiDang,
summaryofcurrentmethodologiesandanalysesin
XiaodongDeng,YangFan,WenbinGe,YuHan,Fei
the area of In-Context Learning (ICL). However, Huang,BinyuanHui,LuoJi,MeiLi,JunyangLin,
| given the | extensive | body | of  | related | work, | partic- |     |     |     |     |     |     |     |
| --------- | --------- | ---- | --- | ------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
RunjiLin,DayihengLiu,GaoLiu,ChengqiangLu,
ularly in demonstration design and the principle KemingLu,JianxinMa,RuiMen,XingzhangRen,
XuanchengRen,ChuanqiTan,SinanTan,Jianhong
| analysis | of ICL, | we may | have | overlooked |     | some |          |       |        |       |     |       |        |
| -------- | ------- | ------ | ---- | ---------- | --- | ---- | -------- | ----- | ------ | ----- | --- | ----- | ------ |
|          |         |        |      |            |     |      | Tu, Peng | Wang, | Shijie | Wang, | Wei | Wang, | Sheng- |
equally valuable contributions. Additionally, we guangWu,BenfengXu,JinXu,AnYang,HaoYang,
outlineseveralfuturedirectionsforresearchinICL,
|     |     |     |     |     |     |     | Jian Yang, | Shusheng | Yang, | Yang | Yao, | Bowen | Yu, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ----- | ---- | ---- | ----- | --- |
includinglong-contextICL,efficiencyandscalabil- HongyiYuan,ZhengYuan,JianweiZhang,Xingx-
uanZhang,YichangZhang,ZhenruZhang,Chang
| ityinICL,etc. |     | Weplantoleavetheseaspectsfor |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Zhou,JingrenZhou,XiaohuanZhou,andTianhang
| futurework. | Furthermore,manypaperscoveredby |     |     |     |     |     |            |     |                      |     |     |               |     |
| ----------- | ------------------------------- | --- | --- | --- | --- | --- | ---------- | --- | -------------------- | --- | --- | ------------- | --- |
|             |                                 |     |     |     |     |     | Zhu.2023a. |     | Qwentechnicalreport. |     |     | arXivpreprint |     |
thissurveydidnotutilizethemostup-to-datemod-
arXiv:2309.16609.
| els while | running | experiments. |     | We  | advocate | for |         |           |      |       |         |        |     |
| --------- | ------- | ------------ | --- | --- | -------- | --- | ------- | --------- | ---- | ----- | ------- | ------ | --- |
|           |         |              |     |     |          |     | Yu Bai, | Fan Chen, | Huan | Wang, | Caiming | Xiong, | and |
morethoroughandup-to-dateresearchtoprovide
|     |     |     |     |     |     |     | Song | Mei. 2023b. | Transformers |     | as  | statisticians: |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | ----------- | ------------ | --- | --- | -------------- | --- |
actionableinsightsforpractitioners.
|     |     |     |     |     |     |     | Provable        | in-context | learning                      |     | with in-context |     | algo- |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ---------- | ----------------------------- | --- | --------------- | --- | ----- |
|     |     |     |     |     |     |     | rithmselection. |            | InAdvancesinNeuralInformation |     |                 |     |       |
1115

ProcessingSystems36: AnnualConferenceonNeu- SamuelR.Bowman,GaborAngeli,ChristopherPotts,
ralInformationProcessingSystems2023,NeurIPS and Christopher D. Manning. 2015. A large anno-
2023, New Orleans, LA, USA, December 10 - 16, tatedcorpusforlearningnaturallanguageinference.
| 2023. |     |     |     |     |     |     | Proceedings |     | of the 2015 | Conference |     | on Empiri- |     |
| ----- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----------- | ---------- | --- | ---------- | --- |
In
calMethodsinNaturalLanguageProcessing,pages
| Amir Bar, | Yossi | Gandelsman, |     | Trevor | Darrell, | Amir |     |     |     |     |     |     |     |
| --------- | ----- | ----------- | --- | ------ | -------- | ---- | --- | --- | --- | --- | --- | --- | --- |
632–642,Lisbon,Portugal.AssociationforCompu-
| Globerson,andAlexeiEfros.2022. |     |     |                        |     | Visualprompt- |     | tationalLinguistics. |     |     |     |     |     |     |
| ------------------------------ | --- | --- | ---------------------- | --- | ------------- | --- | -------------------- | --- | --- | --- | --- | --- | --- |
| ingviaimageinpainting.         |     |     | AdvancesinNeuralInfor- |     |               |     |                      |     |     |     |     |     |     |
mationProcessingSystems,35:25005–25017. TomB.Brown,BenjaminMann,NickRyder,Melanie
|     |     |     |     |     |     |     | Subbiah, | Jared | Kaplan, | Prafulla | Dhariwal, | Arvind |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------- | -------- | --------- | ------ | --- |
RichardBellman.1957. Amarkoviandecisionprocess. Neelakantan,PranavShyam,GirishSastry,Amanda
Journalofmathematicsandmechanics,pages679– Askell, Sandhini Agarwal, Ariel Herbert-Voss,
684.
|     |     |     |     |     |     |     | Gretchen | Krueger, | Tom    | Henighan,   | Rewon |         | Child, |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | ------ | ----------- | ----- | ------- | ------ |
|     |     |     |     |     |     |     | Aditya   | Ramesh,  | Daniel | M. Ziegler, |       | Jeffrey | Wu,    |
AmandaBertsch,MaorIvgi,UriAlon,JonathanBerant,
ClemensWinter,ChristopherHesse,MarkChen,Eric
Matthew R. Gormley, and Graham Neubig. 2024. Sigler,MateuszLitwin,ScottGray,BenjaminChess,
In-context learning with long-context models: An Jack Clark, Christopher Berner, Sam McCandlish,
| in-depthexploration. |        | CoRR,abs/2405.00200. |     |       |              |     |                                          |     |                 |     |           |         |       |
| -------------------- | ------ | -------------------- | --- | ----- | ------------ | --- | ---------------------------------------- | --- | --------------- | --- | --------- | ------- | ----- |
|                      |        |                      |     |       |              |     | Alec Radford,                            |     | Ilya Sutskever, |     | and Dario | Amodei. |       |
|                      |        |                      |     |       |              |     | 2020. Languagemodelsarefew-shotlearners. |     |                 |     |           |         | InAd- |
| Alberto Bietti,      | Vivien | Cabannes,            |     | Diane | Bouchacourt, |     |                                          |     |                 |     |           |         |       |
vancesinNeuralInformationProcessingSystems33:
| Hervé Jégou, | and | Léon | Bottou. | 2023. | Birth | of a |     |     |     |     |     |     |     |
| ------------ | --- | ---- | ------- | ----- | ----- | ---- | --- | --- | --- | --- | --- | --- | --- |
AnnualConferenceonNeuralInformationProcess-
| transformer:                          | Amemoryviewpoint. |     |     |     | InAdvancesin |        |             |       |         |       |          |     |       |
| ------------------------------------- | ----------------- | --- | --- | --- | ------------ | ------ | ----------- | ----- | ------- | ----- | -------- | --- | ----- |
|                                       |                   |     |     |     |              |        | ing Systems | 2020, | NeurIPS | 2020, | December |     | 6-12, |
| NeuralInformationProcessingSystems36: |                   |     |     |     |              | Annual |             |       |         |       |          |     |       |
2020,virtual.
ConferenceonNeuralInformationProcessingSys-
tems2023, NeurIPS2023, NewOrleans, LA,USA, Marc-EtienneBrunet,AshtonAnderson,andRichardS.
December10-16,2023.
|     |     |     |     |     |     |     | Zemel.  | 2023.    | ICL   | markup:    | Structuring |     | in-   |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ----- | ---------- | ----------- | --- | ----- |
|     |     |     |     |     |     |     | context | learning | using | soft-token | tags.       |     | CoRR, |
RishiBommasani,DrewA.Hudson,EhsanAdeli,Russ
abs/2312.07405.
Altman,SimranArora,SydneyvonArx,MichaelS.
Bernstein,JeannetteBohg,AntoineBosselut,Emma
|     |     |     |     |     |     |     | Stephanie | C. Y. | Chan, Adam | Santoro, |     | Andrew | K.  |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ---------- | -------- | --- | ------ | --- |
Brunskill,ErikBrynjolfsson,S.Buch,DallasCard, Lampinen,JaneX.Wang,AadityaK.Singh,PierreH.
Rodrigo Castellon, Niladri S. Chatterji, Annie S. Richemond, James L. McClelland, and Felix Hill.
Chen, Kathleen A. Creel, Jared Davis, Dora Dem- 2022. Datadistributionalpropertiesdriveemergent
szky,ChrisDonahue,MoussaDoumbouya,EsinDur- in-contextlearningintransformers. InAdvancesin
mus,StefanoErmon,JohnEtchemendy,KawinEtha-
|     |     |     |     |     |     |     | NeuralInformationProcessingSystems35: |     |     |     |     | Annual |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | ------ | --- |
yarajh,LiFei-Fei,ChelseaFinn,TrevorGale,Lau- ConferenceonNeuralInformationProcessingSys-
ren E. Gillespie, Karan Goel, Noah D. Goodman, tems2022, NeurIPS2022, NewOrleans, LA,USA,
ShelbyGrossman,NeelGuha,TatsunoriHashimoto, November28-December9,2022.
PeterHenderson,JohnHewitt,DanielE.Ho,Jenny
Hong,KyleHsu,JingHuang,ThomasF.Icard,Saahil AnwoyChatterjee,EshaanTanwar,SubhabrataDutta,
|           |           |           |     |          |           |     | andTanmoyChakraborty.2024. |            |            |     | Languagemodels |     |       |
| --------- | --------- | --------- | --- | -------- | --------- | --- | -------------------------- | ---------- | ---------- | --- | -------------- | --- | ----- |
| Jain, Dan | Jurafsky, | Pratyusha |     | Kalluri, | Siddharth |     |                            |            |            |     |                |     |       |
|           |           |           |     |          |           |     | can exploit                | cross-task | in-context |     | learning       | for | data- |
Karamcheti,GeoffKeeling,FereshteKhani,O.Khat-
tab,PangWeiKoh,MarkS.Krass,RanjayKrishna, scarcenoveltasks. CoRR,abs/2405.10548.
| Rohith Kuditipudi, |     | Ananya | Kumar, |     | Faisal | Ladhak, |     |     |     |     |     |     |     |
| ------------------ | --- | ------ | ------ | --- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
DingChen,ShichaoSong,QingchenYu,ZhiyuLi,Wen-
MinaLee,TonyLee,JureLeskovec,IsabelleLevent,
Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Ma- jinWang,FeiyuXiong,andBoTang.2024. Grimoire
isallyouneedforenhancinglargelanguagemodels.
lik,ChristopherD.Manning,SuvirP.Mirchandani,
CoRR,abs/2401.03385.
EricMitchell,ZaneleMunyikwa,SurajNair,Avanika
| Narayan, | Deepak | Narayanan, |     | Benjamin | Newman, |     |     |     |     |     |     |     |     |
| -------- | ------ | ---------- | --- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
MingdaChen,JingfeiDu,RamakanthPasunuru,Todor
AllenNie,JuanCarlosNiebles,HamedNilforoshan,
|     |     |     |     |     |     |     | Mihaylov, | Srini | Iyer, Veselin |     | Stoyanov, | and | Zor- |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ------------- | --- | --------- | --- | ---- |
J.F.Nyarko,GirayOgut,LaurelOrr,IsabelPapadim-
|     |     |     |     |     |     |     | nitsaKozareva.2022. |     | Improvingin-contextfew-shot |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --------------------------- | --- | --- | --- | --- |
itriou,JoonSungPark,ChrisPiech,EvaPortelance, learningviaself-supervisedtraining. InProceedings
Christopher Potts, Aditi Raghunathan, Robert Re- ofthe2022ConferenceoftheNorthAmericanChap-
| ich, HongyuRen, |     | FriedaRong, |     | YusufH.Roohani, |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ----------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
teroftheAssociationforComputationalLinguistics:
| Camilo | Ruiz, Jack | Ryan, | Christopher |     | R’e, | Dorsa |     |     |     |     |     |     |     |
| ------ | ---------- | ----- | ----------- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- |
HumanLanguageTechnologies,pages3558–3573,
| Sadigh, | Shiori | Sagawa, | Keshav | Santhanam, |     | Andy |     |     |     |     |     |     |     |
| ------- | ------ | ------- | ------ | ---------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Seattle,UnitedStates.AssociationforComputational
| Shih,KrishnaParasuramSrinivasan,AlexTamkin, |       |     |         |     |         |         | Linguistics. |     |     |     |     |     |     |
| ------------------------------------------- | ----- | --- | ------- | --- | ------- | ------- | ------------ | --- | --- | --- | --- | --- | --- |
| Rohan Taori,                                | Armin | W.  | Thomas, |     | Florian | Tramèr, |              |     |     |     |     |     |     |
Rose E. Wang, William Wang, Bohan Wu, Jiajun AakankshaChowdhery,SharanNarang,JacobDevlin,
Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Ya- Maarten Bosma, Gaurav Mishra, Adam Roberts,
sunaga, Jiaxuan You, Matei A. Zaharia, Michael Paul Barham, Hyung Won Chung, Charles Sutton,
Zhang, Tianyi Zhang, Xikun Zhang, Yuhui Zhang, Sebastian Gehrmann, Parker Schuh, Kensen Shi,
LuciaZheng,KaitlynZhou,andPercyLiang.2021. Sasha Tsvyashchenko, Joshua Maynez, Abhishek
Ontheopportunitiesandrisksoffoundationmodels. Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vin-
| ArXiv. |     |     |     |     |     |     | odkumar | Prabhakaran, |     | Emily | Reif, Nan | Du, | Ben |
| ------ | --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | ----- | --------- | --- | --- |
1116

Hutchinson, Reiner Pope, James Bradbury, Jacob ACL2023,Toronto,Canada,July9-14,2023,pages
Austin,MichaelIsard,GuyGur-Ari,PengchengYin, 11173–11195. Association for Computational Lin-
| Toju Duke, | Anselm Levskaya,         | Sanjay Ghemawat, |         | guistics. |                  |     |            |           |
| ---------- | ------------------------ | ---------------- | ------- | --------- | ---------------- | --- | ---------- | --------- |
| Sunipa     | Dev, Henryk Michalewski, | Xavier           | Garcia, |           |                  |     |            |           |
|            |                          |                  |         | Nan Ding, | Tomer Levinboim, |     | Jialin Wu, | Sebastian |
VedantMisra,KevinRobinson,LiamFedus,Denny
Zhou,DaphneIppolito,DavidLuan,HyeontaekLim, Goodman, and Radu Soricut. 2024. CausalLM is
Barret Zoph, Alexander Spiridonov, Ryan Sepassi, notoptimalforin-contextlearning. InTheTwelfth
DavidDohan,ShivaniAgrawal,MarkOmernick,An- International Conference on Learning Representa-
| drew M. | Dai, Thanumalayan | Sankaranarayana | Pil- | tions. |     |     |     |     |
| ------- | ----------------- | --------------- | ---- | ------ | --- | --- | --- | --- |
lai,MariePellat,AitorLewkowycz,EricaMoreira,
QingxiuDong,JingjingXu,LingpengKong,Zhifang
| Rewon | Child, Oleksandr | Polozov, Katherine | Lee, |     |     |     |     |     |
| ----- | ---------------- | ------------------ | ---- | --- | --- | --- | --- | --- |
ZongweiZhou,XuezhiWang,BrennanSaeta,Mark Sui,andLeiLi.2023. Statisticalknowledgeassess-
Diaz,OrhanFirat,MicheleCatasta,JasonWei,Kathy ment for large language models. In Advances in
Meier-Hellstern,DouglasEck,JeffDean,SlavPetrov, NeuralInformationProcessingSystems,volume36,
pages29812–29830.CurranAssociates,Inc.
| andNoahFiedel.2023. | Palm:Scalinglanguagemod-    |     |     |     |     |     |     |     |
| ------------------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- |
| elingwithpathways.  | J.Mach.Learn.Res.,24:240:1– |     |     |     |     |     |     |     |
DeqingFu,Tian-QiChen,RobinJia,andVatsalSharan.
240:113.
2023. Transformerslearnhigher-orderoptimization
Timothy Chu, Zhao Song, and Chiwun Yang. 2023. methodsforin-contextlearning: Astudywithlinear
Fine-tunelanguagemodelstoapproximateunbiased models. CoRR,abs/2310.17086.
| in-contextlearning. | CoRR,abs/2310.03331. |     |     |           |            |     |               |           |
| ------------------- | -------------------- | --- | --- | --------- | ---------- | --- | ------------- | --------- |
|                     |                      |     |     | Yeqi Gao, | Zhao Song, | and | Shenghao Xie. | 2023. In- |
HyungWonChung,LeHou,ShayneLongpre,Barret context learning for attention scheme: from single
Zoph,YiTay,WilliamFedus,YunxuanLi,Xuezhi softmax regression to multiple softmax regression
Wang, Mostafa Dehghani, Siddhartha Brahma, Al- viaatensortrick. CoRR,abs/2307.02419.
| bert Webson, | Shixiang | Shane Gu, Zhuyun | Dai, |     |     |     |     |     |
| ------------ | -------- | ---------------- | ---- | --- | --- | --- | --- | --- |
MiracSuzgun,XinyunChen,AakankshaChowdh- ShivamGarg,DimitrisTsipras,PercyLiang,andGre-
ery,AlexCastro-Ros,MariePellat,KevinRobinson, goryValiant.2022. Whatcantransformerslearnin-
|     |     |     |     | context? | Acasestudyofsimplefunctionclasses. |     |     | In  |
| --- | --- | --- | --- | -------- | ---------------------------------- | --- | --- | --- |
DashaValter,SharanNarang,GauravMishra,Adams
AdvancesinNeuralInformationProcessingSystems
| Yu, Vincent | Zhao, Yanping | Huang, Andrew | Dai, |     |     |     |     |     |
| ----------- | ------------- | ------------- | ---- | --- | --- | --- | --- | --- |
HongkunYu,SlavPetrov,EdH.Chi,JeffDean,Ja- 35: AnnualConferenceonNeuralInformationPro-
cobDevlin,AdamRoberts,DennyZhou,QuocV.Le, cessingSystems2022,NeurIPS2022,NewOrleans,
andJasonWei.2022. Scalinginstruction-finetuned LA,USA,November28-December9,2022.
languagemodels.
HilaGonen,SriniIyer,TerraBlevins,NoahA.Smith,
|     |     |     |     | andLukeZettlemoyer.2023. |     |     | Demystifyingprompts |     |
| --- | --- | --- | --- | ------------------------ | --- | --- | ------------------- | --- |
DamaiDai,YutaoSun,LiDong,YaruHao,Shuming
Ma, Zhifang Sui, and Furu Wei. 2023a. Why can in language models via perplexity estimation. In
GPTlearnin-context? languagemodelssecretlyper- FindingsoftheAssociationforComputationalLin-
formgradientdescentasmeta-optimizers. InFind- guistics: EMNLP2023,Singapore,December6-10,
ingsoftheAssociationforComputationalLinguistics: 2023,pages10136–10148.AssociationforComputa-
tionalLinguistics.
ACL2023,Toronto,Canada,July9-14,2023,pages
4005–4019.AssociationforComputationalLinguis-
| tics. |     |     |     | YuxianGu,LiDong,FuruWei,andMinlieHuang.2023. |          |             |                |     |
| ----- | --- | --- | --- | -------------------------------------------- | -------- | ----------- | -------------- | --- |
|       |     |     |     | Pre-training                                 | to learn | in context. | In Proceedings | of  |
Wenliang Dai, Junnan Li, Dongxu Li, Anthony the61stAnnualMeetingoftheAssociationforCom-
Meng Huat Tiong, Junqi Zhao, Weisheng Wang, putationalLinguistics(Volume1:LongPapers),ACL
Boyang Li, Pascale Fung, and Steven C. H. Hoi. 2023,Toronto,Canada,July9-14,2023,pages4849–
4870.AssociationforComputationalLinguistics.
| 2023b.   | Instructblip: Towardsgeneral-purposevision- |         |        |     |     |     |     |     |
| -------- | ------------------------------------------- | ------- | ------ | --- | --- | --- | --- | --- |
| language | models with instruction                     | tuning. | In Ad- |     |     |     |     |     |
vances in Neural Information Processing Systems Michael Hahn and Navin Goyal. 2023. A theory of
36: AnnualConferenceonNeuralInformationPro- emergent in-context learning as implicit structure
cessingSystems2023,NeurIPS2023,NewOrleans, induction. CoRR,abs/2303.07971.
LA,USA,December10-16,2023.
|                                           |     |     |       | Chi Han, Ziqi | Wang,    | Han Zhao,  | and Heng | Ji. 2023a. |
| ----------------------------------------- | --- | --- | ----- | ------------- | -------- | ---------- | -------- | ---------- |
|                                           |     |     |       | Explaining    | emergent | in-context | learning | as kernel  |
| NicolaDeCao,WilkerAziz,andIvanTitov.2021. |     |     | Edit- |               |          |            |          |            |
ingfactualknowledgeinlanguagemodels. InProc. regression. Preprint,arXiv:2305.12766.
| of EMNLP, | pages 6491–6506, | Online | and Punta |     |     |     |     |     |
| --------- | ---------------- | ------ | --------- | --- | --- | --- | --- | --- |
Cana, Dominican Republic. Association for Com- XiaochuangHan,DanielSimig,TodorMihaylov,Yulia
putationalLinguistics. Tsvetkov,AsliCelikyilmaz,andTianluWang.2023b.
Understandingin-contextlearningviasupportivepre-
Bosheng Ding, Chengwei Qin, Linlin Liu, Yew Ken training data. In Proceedings of the 61st Annual
Chia,BoyangLi,ShafiqJoty,andLidongBing.2023. Meeting of the Association for Computational Lin-
Is GPT-3 a good data annotator? In Proceedings guistics(Volume1:LongPapers),ACL2023,Toronto,
of the 61st Annual Meeting of the Association for Canada,July9-14,2023,pages12660–12673.Asso-
ComputationalLinguistics(Volume1: LongPapers), ciationforComputationalLinguistics.
1117

Yaru Hao, Haoyu Song, Li Dong, Shaohan Huang, SrinivasanIyer,XiVictoriaLin,RamakanthPasunuru,
ZewenChi,WenhuiWang,ShumingMa,andFuru TodorMihaylov,DanielSimig,PingYu,KurtShuster,
Wei.2022a. Languagemodelsaregeneral-purpose TianluWang,QingLiu,PunitSinghKoura,XianLi,
arXivpreprintarXiv:2206.06336.
| interfaces. |     |     |     |     |     |     | BrianO’Horo,GabrielPereyra,JeffWang,Christo- |      |              |      |              |
| ----------- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | ---- | ------------ | ---- | ------------ |
|             |     |     |     |     |     |     | pher Dewan,                                  | Asli | Celikyilmaz, | Luke | Zettlemoyer, |
YaruHao,YutaoSun,LiDong,ZhixiongHan,Yuxian andVesStoyanov.2022. Opt-iml: Scalinglanguage
Gu, and Furu Wei. 2022b. Structured prompting: modelinstructionmetalearningthroughthelensof
| Scalingin-contextlearningto1,000examples. |     |     |     |     |     | ArXiv | generalization. |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | ----- | --------------- | --- | --- | --- | --- |
preprint,abs/2212.06713.
|     |     |     |     |     |     |     | Hui Jiang.     | 2023. | A latent | space theory     | for emer- |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ----- | -------- | ---------------- | --------- |
|     |     |     |     |     |     |     | gent abilities |       | in large | language models. | CoRR,     |
JiabangHe,LeiWang,YiHu,NingLiu,HuiLiu,Xing
| Xu,andHengTaoShen.2023. |      |         |                | ICL-D3IE:in-context |          |     | abs/2304.09960. |     |     |     |     |
| ----------------------- | ---- | ------- | -------------- | ------------------- | -------- | --- | --------------- | --- | --- | --- | --- |
| learning                | with | diverse | demonstrations |                     | updating | for |                 |     |     |     |     |
documentinformationextraction. InIEEE/CVFIn- Hanieh Khorashadizadeh, Nandana Mihindukula-
|     |     |     |     |     |     |     | sooriya, | Sanju | Tiwari, | Jinghua Groppe, | and Sven |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------- | --------------- | -------- |
ternationalConferenceonComputerVision,ICCV
|     |     |     |     |     |     |     | Groppe.2023. |     | Exploringin-contextlearningcapabil- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----------------------------------- | --- | --- |
2023,Paris,France,October1-6,2023,pages19428–
itiesoffoundationmodelsforgeneratingknowledge
19437.IEEE.
|                 |     |          |       |       |       |        | graphsfromtext. |     | arXivpreprintarXiv:2305.08804. |     |     |
| --------------- | --- | -------- | ----- | ----- | ----- | ------ | --------------- | --- | ------------------------------ | --- | --- |
| Wei He, Shichun |     | Liu, Jun | Zhao, | Yiwen | Ding, | Yi Lu, |                 |     |                                |     |     |
HyuhngJoonKim,HyunsooCho,JunyeobKim,Taeuk
ZhihengXi,TaoGui,QiZhang,andXuanjingHuang.
|                  |             |           |          |                      |     |       | Kim, Kang                         | Min | Yoo, | and Sang-goo    | Lee. 2022. |
| ---------------- | ----------- | --------- | -------- | -------------------- | --- | ----- | --------------------------------- | --- | ---- | --------------- | ---------- |
| 2024.            | Self-demos: | Eliciting |          | out-of-demonstration |     |       |                                   |     |      |                 |            |
|                  |             |           |          |                      |     |       | Self-generatedin-contextlearning: |     |      | Leveragingauto- |            |
| generalizability |             | in large  | language | models.              |     | CoRR, |                                   |     |      |                 |            |
regressivelanguagemodelsasademonstrationgen-
abs/2404.00884.
|     |     |     |     |     |     |     | erator. | ArXivpreprint,abs/2206.08082. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------------------------- | --- | --- | --- |
Clyde Highmore. 2024. In-context learning in large Jannik Kossen, Tom Rainforth, and Yarin Gal. 2023.
languagemodels: Acomprehensivesurvey. In-contextlearninginlargelanguagemodelslearns
labelrelationshipsbutisnotconventionallearning.
| Or Honovich, | Uri | Shaham, | Samuel | R.  | Bowman, | and |     |     |     |     |     |
| ------------ | --- | ------- | ------ | --- | ------- | --- | --- | --- | --- | --- | --- |
CoRR,abs/2307.12375.
| OmerLevy.2023. |     | Instructioninduction: |     |     | Fromfew |     |     |     |     |     |     |
| -------------- | --- | --------------------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
examplestonaturallanguagetaskdescriptions. In BoLi,YuanhanZhang,LiangyuChen,JinghaoWang,
Proceedings of the 61st Annual Meeting of the As- Jingkang Yang, and Ziwei Liu. 2023a. Otter: A
sociationforComputationalLinguistics(Volume1: multi-modalmodelwithin-contextinstructiontuning.
LongPapers),ACL2023,Toronto,Canada,July9-14, arXivpreprintarXiv:2305.03726.
2023,pages1935–1952.AssociationforComputa-
|     |     |     |     |     |     |     | Jia Li, Yunfei | Zhao, | Yongmin | Li, Ge Li, | and Zhi Jin. |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ----- | ------- | ---------- | ------------ |
tionalLinguistics.
|     |     |     |     |     |     |     | 2023b. | Towardsenhancingin-contextlearningfor |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------------------------------- | --- | --- | --- |
QianHuang,HongyuRen,PengChen,GregorKrzmanc, codegeneration. arXivpreprintarXiv:2303.17780.
DanielZeng,PercyLiang,andJureLeskovec.2023a.
PRODIGY:enablingin-contextlearningovergraphs. Jiahao Li, Quan Wang, Licheng Zhang, Guoqing
InAdvancesinNeuralInformationProcessingSys- Jin, and Zhendong Mao. 2024a. Feature-adaptive
|         |                                     |     |     |     |     |     | and data-scalable |     | in-context | learning. | Preprint, |
| ------- | ----------------------------------- | --- | --- | --- | --- | --- | ----------------- | --- | ---------- | --------- | --------- |
| tems36: | AnnualConferenceonNeuralInformation |     |     |     |     |     |                   |     |            |           |           |
arXiv:2405.10738.
| Processing | Systems | 2023, | NeurIPS | 2023, | New | Or- |     |     |     |     |     |
| ---------- | ------- | ----- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
leans,LA,USA,December10-16,2023.
|                 |     |            |        |             |      |      | Shuai Li,                              | Zhao Song, | Yu                               | Xia, Tong Yu, | and Tianyi |
| --------------- | --- | ---------- | ------ | ----------- | ---- | ---- | -------------------------------------- | ---------- | -------------------------------- | ------------- | ---------- |
|                 |     |            |        |             |      |      | Zhou.2023c.                            |            | Theclosenessofin-contextlearning |               |            |
| Shaohan Huang,  |     | Li Dong,   | Wenhui | Wang,       | Yaru | Hao, |                                        |            |                                  |               |            |
|                 |     |            |        |             |      |      | andweightshiftingforsoftmaxregression. |            |                                  |               | CoRR,      |
| SakshamSinghal, |     | ShumingMa, |        | TengchaoLv, |      | Lei  |                                        |            |                                  |               |            |
abs/2304.13276.
Cui,OwaisKhanMohammed,BarunPatra,Qiang
Liu, KritiAggarwal,ZewenChi,NilsJohanBertil
|     |     |     |     |     |     |     | Tianle Li, | Ge Zhang, | Quy | Duc Do, | Xiang Yue, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | ------- | ---------- |
Bjorck,VishravChaudhary,SubhojitSom,XiaSong,
|                   |            |     |                          |         |     |        | and Wenhu       | Chen. | 2024b.          | Long-context | llms   |
| ----------------- | ---------- | --- | ------------------------ | ------- | --- | ------ | --------------- | ----- | --------------- | ------------ | ------ |
| andFuruWei.2023b. |            |     | Languageisnotallyouneed: |         |     |        |                 |       |                 |              |        |
|                   |            |     |                          |         |     |        | struggle        | with  | long in-context | learning.    | ArXiv, |
| Aligning          | perception |     | with language            | models. |     | In Ad- | abs/2404.02060. |       |                 |              |        |
vancesinNeuralInformationProcessingSystems36:
AnnualConferenceonNeuralInformationProcess- XiaonanLi,KaiLv,HangYan,TianyangLin,WeiZhu,
ingSystems2023,NeurIPS2023,NewOrleans,LA,
YuanNi,GuotongXie,XiaolingWang,andXipeng
USA,December10-16,2023.
|     |     |     |     |     |     |     | Qiu.2023d.       | Unifieddemonstrationretrieverforin- |                              |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | ----------------------------------- | ---------------------------- | --- | --- |
|     |     |     |     |     |     |     | contextlearning. |                                     | InProceedingsofthe61stAnnual |     |     |
KazukiIrie,RóbertCsordás,andJürgenSchmidhuber. Meeting of the Association for Computational Lin-
2022. The dual form of neural networks revisited: guistics(Volume1:LongPapers),ACL2023,Toronto,
Connectingtesttimepredictionstotrainingpatterns
Canada,July9-14,2023,pages4644–4668.Associa-
| viaspotlightsofattention. |     |     | InInternationalConfer- |     |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tionforComputationalLinguistics.
enceonMachineLearning,ICML2022,17-23July
2022, Baltimore, Maryland, USA, volume 162 of Xiaonan Li and Xipeng Qiu. 2023. Finding sup-
ProceedingsofMachineLearningResearch,pages porting examples for in-context learning. CoRR,
| 9639–9659.PMLR. |     |     |     |     |     |     | abs/2302.13539. |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- |
1118

Yichuan Li, Xiyao Ma, Sixing Lu, Kyumin Lee, Xi- YaoLu,MaxBartolo,AlastairMoore,SebastianRiedel,
aohu Liu, and Chenlei Guo. 2024c. MEND: meta and Pontus Stenetorp. 2022. Fantastically ordered
demonstrationdistillationforefficientandeffective promptsandwheretofindthem: Overcomingfew-
|                     | CoRR,abs/2403.06914. |     |     |                             |     |     |     | InProceedingsofthe |     |     |
| ------------------- | -------------------- | --- | --- | --------------------------- | --- | --- | --- | ------------------ | --- | --- |
| in-contextlearning. |                      |     |     | shotpromptordersensitivity. |     |     |     |                    |     |     |
60thAnnualMeetingoftheAssociationforCompu-
YingcongLi,MuhammedEmrullahIldiz,DimitrisPa-
|     |     |     |     | tationalLinguistics(Volume1: |     |     |     | LongPapers),ACL |     |     |
| --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --------------- | --- | --- |
pailiopoulos,andSametOymak.2023e. Transform- 2022,Dublin,Ireland,May22-27,2022,pages8086–
ers as algorithms: Generalization and stability in 8098.AssociationforComputationalLinguistics.
| in-contextlearning. | InInternationalConferenceon |     |     |     |     |     |     |     |     |     |
| ------------------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Machine Learning, ICML 2023, 23-29 July 2023, ArvindMahankali,TatsunoriB.Hashimoto,andTengyu
Honolulu,Hawaii,USA,volume202ofProceedings Ma.2023. Onestepofgradientdescentisprovably
ofMachineLearningResearch,pages19565–19594. theoptimalin-contextlearnerwithonelayeroflinear
| PMLR. |     |     |     | self-attention. |     | CoRR,abs/2307.03576. |     |     |     |     |
| ----- | --- | --- | --- | --------------- | --- | -------------------- | --- | --- | --- | --- |
Yinheng Li. 2023. A practical survey on zero-shot Costas Mavromatis, Balasubramaniam Srinivasan,
promptdesignforin-contextlearning. arXivpreprint Zhengyuan Shen, Jiani Zhang, Huzefa Rangwala,
arXiv:2309.13205. Christos Faloutsos, and George Karypis. 2023.
|     |     |     |     | Which | examples | to  | annotate | for in-context |     | learn- |
| --- | --- | --- | --- | ----- | -------- | --- | -------- | -------------- | --- | ------ |
ZhuoweiLi,ZihaoXu,LigongHan,YunheGao,Song ing? towardseffectiveandefficientselection. CoRR,
Wen,DiLiu,HaoWang,andDimitrisN.Metaxas.
abs/2310.20046.
| 2024d. | Implicit in-context | learning. | Preprint, |     |     |     |     |     |     |     |
| ------ | ------------------- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:2405.14660. NicholasMeade,SpandanaGella,DevamanyuHazarika,
|     |     |     |     | Prakhar | Gupta, | Di Jin, | Siva Reddy, |     | Yang | Liu, and |
| --- | --- | --- | --- | ------- | ------ | ------- | ----------- | --- | ---- | -------- |
HaotianLiu,ChunyuanLi,QingyangWu,andYongJae Dilek Hakkani-Tur. 2023. Using in-context learn-
Lee.2023a. Visualinstructiontuning. arXivpreprint ing to improve dialogue safety. In Findings of the
arXiv:2304.08485. AssociationforComputationalLinguistics: EMNLP
2023,Singapore,December6-10,2023,pages11882–
JiachangLiu,DinghanShen,YizheZhang,BillDolan,
11910.AssociationforComputationalLinguistics.
| Lawrence                             | Carin, and Weizhu | Chen. | 2022. What |            |      |        |          |     |             |     |
| ------------------------------------ | ----------------- | ----- | ---------- | ---------- | ---- | ------ | -------- | --- | ----------- | --- |
| makesgoodin-contextexamplesforgpt-3? |                   |       | InPro-     |            |      |        |          |     |             |     |
|                                      |                   |       |            | Sewon Min, | Mike | Lewis, | Hannaneh |     | Hajishirzi, | and |
ceedingsofDeepLearningInsideOut:The3rdWork- LukeZettlemoyer.2022a. Noisychannellanguage
shoponKnowledgeExtractionandIntegrationfor modelpromptingforfew-shottextclassification. In
DeepLearningArchitectures,DeeLIO@ACL2022, Proc.ofACL,pages5316–5330,Dublin,Ireland.As-
Dublin, Ireland and Online, May 27, 2022, pages sociationforComputationalLinguistics.
100–114.AssociationforComputationalLinguistics.
SewonMin,MikeLewis,LukeZettlemoyer,andHan-
NelsonF.Liu,KevinLin,JohnHewitt,AshwinParan- nanehHajishirzi.2022b. MetaICL:Learningtolearn
jape,MicheleBevilacqua,FabioPetroni,andPercy
|     |     |     |     | incontext. | InProceedingsofthe2022Conferenceof |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | ---------------------------------- | --- | --- | --- | --- | --- |
Liang. 2023b. Lost in the middle: How language theNorthAmericanChapteroftheAssociationfor
modelsuselongcontexts. CoRR,abs/2307.03172. ComputationalLinguistics: HumanLanguageTech-
|     |     |     |     | nologies, | pages | 2791–2809, |     | Seattle, | United | States. |
| --- | --- | --- | --- | --------- | ----- | ---------- | --- | -------- | ------ | ------- |
PengfeiLiu,WeizheYuan,JinlanFu,ZhengbaoJiang, AssociationforComputationalLinguistics.
| HiroakiHayashi,andGrahamNeubig.2023c. |     |     | Pre- |     |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
train, prompt, and predict: A systematic survey of SewonMin,XinxiLyu,AriHoltzman,MikelArtetxe,
promptingmethodsinnaturallanguageprocessing.
MikeLewis,HannanehHajishirzi,andLukeZettle-
ACMComput.Surv.,55(9):195:1–195:35. moyer.2022c. Rethinkingtheroleofdemonstrations:
|     |     |     |     | Whatmakesin-contextlearningwork? |     |     |     |     | InProceed- |     |
| --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | ---------- | --- |
ShengLiu,HaotianYe,LeiXing,andJamesZou.2024a. ingsofthe2022ConferenceonEmpiricalMethods
In-contextvectors: Makingincontextlearningmore inNaturalLanguageProcessing,EMNLP2022,Abu
effectiveandcontrollablethroughlatentspacesteer- Dhabi,UnitedArabEmirates,December7-11,2022,
ing. Preprint,arXiv:2311.06668.
pages11048–11064.AssociationforComputational
Linguistics.
YinpengLiu,JiaweiLiu,XiangShi,QikaiCheng,and
| WeiLu.2024b. | Let’slearnstepbystep: |     | Enhancing |         |         |        |           |        |        |     |
| ------------ | --------------------- | --- | --------- | ------- | ------- | ------ | --------- | ------ | ------ | --- |
|              |                       |     |           | Swaroop | Mishra, | Daniel | Khashabi, | Chitta | Baral, | and |
in-contextlearningabilitywithcurriculumlearning.
|     |     |     |     | Hannaneh | Hajishirzi. |     | 2021. | Cross-task | generaliza- |     |
| --- | --- | --- | --- | -------- | ----------- | --- | ----- | ---------- | ----------- | --- |
Preprint,arXiv:2402.10738. tionvianaturallanguagecrowdsourcinginstructions.
arXivpreprintarXiv:2104.08773.
ZichangLiu,JueWang,TriDao,TianyiZhou,Binhang
Yuan,ZhaoSong,AnshumaliShrivastava,CeZhang, Tai Nguyen and Eric Wong. 2023. In-context ex-
Yuandong Tian, Christopher Ré, and Beidi Chen. ample selection with influences. arXiv preprint
| 2023d. Deja | vu: Contextual | sparsity | for efficient |     |     |     |     |     |     |     |
| ----------- | -------------- | -------- | ------------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:2302.11042.
| llmsatinferencetime. | InInternationalConference |     |     |     |     |     |     |     |     |     |
| -------------------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
onMachineLearning,ICML2023,23-29July2023, CatherineOlsson,NelsonElhage,NeelNanda,Nicholas
Honolulu,Hawaii,USA,volume202ofProceedings Joseph,NovaDasSarma,TomHenighan,BenMann,
ofMachineLearningResearch,pages22137–22176. AmandaAskell,YuntaoBai,AnnaChen,TomCon-
| PMLR. |     |     |     | erly,DawnDrain,DeepGanguli,ZacHatfield-Dodds, |     |     |     |     |     |     |
| ----- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
1119

DannyHernandez,ScottJohnston,AndyJones,Jack- AbulhairSaparovandHeHe.2023. Languagemodels
son Kernion, Liane Lovitt, Kamal Ndousse, Dario aregreedyreasoners: Asystematicformalanalysis
Amodei,TomBrown,JackClark,JaredKaplan,Sam ofchain-of-thought. InTheEleventhInternational
ConferenceonLearningRepresentations,ICLR2023,
| McCandlish,andChrisOlah.2022. |     | In-contextlearn- |     |     |     |     |     |
| ----------------------------- | --- | ---------------- | --- | --- | --- | --- | --- |
ingandinductionheads. CoRR,abs/2209.11895. Kigali,Rwanda,May1-5,2023.OpenReview.net.
OpenAI. 2023. GPT-4 technical report. CoRR, LingfengShen,AayushMishra,andDanielKhashabi.
abs/2303.08774. 2024. Dopretrainedtransformerslearnin-contextby
|     |     |     |     | gradientdescent? | Preprint,arXiv:2310.08540. |     |     |
| --- | --- | --- | --- | ---------------- | -------------------------- | --- | --- |
JanePan,TianyuGao,HowardChen,andDanqiChen.
FredaShi,MiracSuzgun,MarkusFreitag,XuezhiWang,
| 2023a. Whatin-contextlearning"learns"in-context: |     |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
Disentanglingtaskrecognitionandtasklearning. In SurajSrivats,SoroushVosoughi,HyungWonChung,
AnnualMeetingoftheAssociationforComputational Yi Tay, Sebastian Ruder, Denny Zhou, et al. 2022.
| Linguistics. |     |     |     | Languagemodelsaremultilingualchain-of-thought |                               |     |     |
| ------------ | --- | --- | --- | --------------------------------------------- | ----------------------------- | --- | --- |
|              |     |     |     | reasoners.                                    | ArXivpreprint,abs/2210.03057. |     |     |
JanePan,TianyuGao,HowardChen,andDanqiChen.
WeijiaShi,SewonMin,MariaLomeli,ChuntingZhou,
| 2023b. Whatin-contextlearning"learns"in-context: |     |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
MargaretLi,XiVictoriaLin,NoahA.Smith,Luke
| Disentanglingtaskrecognitionandtasklearning. |     |     | In  |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
FindingsoftheAssociationforComputationalLin- Zettlemoyer, Wen tau Yih, and Mike Lewis. 2024.
|           |                    |         |            | In-contextpretraining: |     | Languagemodelingbeyond    |     |
| --------- | ------------------ | ------- | ---------- | ---------------------- | --- | ------------------------- | --- |
| guistics: | ACL 2023, Toronto, | Canada, | July 9-14, |                        |     |                           |     |
|           |                    |         |            | documentboundaries.    |     | InTheTwelfthInternational |     |
2023,pages8298–8319.AssociationforComputa-
ConferenceonLearningRepresentations.
tionalLinguistics.
SeongjinShin,Sang-WooLee,HwijeenAhn,Sungdong
AshwineePanda,TongWu,JiachenT.Wang,andPra-
Kim,HyoungSeokKim,BoseopKim,Kyunghyun
| teekMittal.2023. | Differentiallyprivatein-context |     |     |     |     |     |     |
| ---------------- | ------------------------------- | --- | --- | --- | --- | --- | --- |
Cho,GichangLee,WoomyoungPark,Jung-WooHa,
| learning. | CoRR,abs/2305.01639. |     |     |                   |     |                          |     |
| --------- | -------------------- | --- | --- | ----------------- | --- | ------------------------ | --- |
|           |                      |     |     | andNakoSung.2022. |     | Ontheeffectofpretraining |     |
corporaonin-contextlearningbyalarge-scalelan-
ChengweiQin,AstonZhang,AnirudhDagar,andWen-
|          |                  |               |           | guagemodel. | InProceedingsofthe2022Conference |     |     |
| -------- | ---------------- | ------------- | --------- | ----------- | -------------------------------- | --- | --- |
| ming Ye. | 2023. In-context | learning with | iterative |             |                                  |     |     |
oftheNorthAmericanChapteroftheAssociationfor
| demonstrationselection. | CoRR,abs/2310.09881. |              |       |                           |                  |                    |                |
| ----------------------- | -------------------- | ------------ | ----- | ------------------------- | ---------------- | ------------------ | -------------- |
|                         |                      |              |       | ComputationalLinguistics: |                  | HumanLanguageTech- |                |
|                         |                      |              |       | nologies,                 | pages 5168–5186, | Seattle,           | United States. |
| Alec Radford,           | Jeff Wu, Rewon       | Child, David | Luan, |                           |                  |                    |                |
AssociationforComputationalLinguistics.
| DarioAmodei,andIlyaSutskever.2019.      |     |     | Language |          |                   |               |           |
| --------------------------------------- | --- | --- | -------- | -------- | ----------------- | ------------- | --------- |
| modelsareunsupervisedmultitasklearners. |     |     | Techni-  |          |                   |               |           |
|                                         |     |     |          | Chenglei | Si, Dan Friedman, | Nitish Joshi, | Shi Feng, |
calreport,OpenAi. Danqi Chen, and He He. 2023. Measuring induc-
tivebiasesofin-contextlearningwithunderspecified
| Pranav Rajpurkar, | Robin Jia, | and Percy Liang. | 2018. |                 |                              |     |     |
| ----------------- | ---------- | ---------------- | ----- | --------------- | ---------------------------- | --- | --- |
|                   |            |                  |       | demonstrations. | InProceedingsofthe61stAnnual |     |     |
Knowwhatyoudon’tknow:Unanswerablequestions
|           |                                   |     |     | Meeting | of the Association | for Computational | Lin- |
| --------- | --------------------------------- | --- | --- | ------- | ------------------ | ----------------- | ---- |
| forsquad. | InProceedingsofthe56thAnnualMeet- |     |     |         |                    |                   |      |
guistics(Volume1:LongPapers),ACL2023,Toronto,
ingoftheAssociationforComputationalLinguistics,
Canada,July9-14,2023,pages11289–11310.Asso-
ACL2018,Melbourne,Australia,July15-20,2018,
ciationforComputationalLinguistics.
| Volume2: | ShortPapers,pages784–789.Association |     |     |     |     |     |     |
| -------- | ------------------------------------ | --- | --- | --- | --- | --- | --- |
forComputationalLinguistics.
|     |     |     |     | Richard | Socher, Alex Perelygin, | Jean | Wu, Jason |
| --- | --- | --- | --- | ------- | ----------------------- | ---- | --------- |
Chuang,ChristopherD.Manning,AndrewNg,and
OriRam,YoavLevine,ItayDalmedigos,DorMuhlgay,
|     |     |     |     | ChristopherPotts.2013a. |     | Recursivedeepmodelsfor |     |
| --- | --- | --- | --- | ----------------------- | --- | ---------------------- | --- |
Amnon Shashua, Kevin Leyton-Brown, and Yoav semanticcompositionalityoverasentimenttreebank.
Shoham.2023. In-contextretrieval-augmentedlan- In Proceedings of the 2013 Conference on Empiri-
| guagemodels. | CoRR,abs/2302.00083. |     |     |     |     |     |     |
| ------------ | -------------------- | --- | --- | --- | --- | --- | --- |
calMethodsinNaturalLanguageProcessing,pages
1631–1642,Seattle,Washington,USA.Association
AllanRaventós,MansheejPaul,FengChen,andSurya
forComputationalLinguistics.
| Ganguli. | 2023. Pretraining | task diversity | and the |     |     |     |     |
| -------- | ----------------- | -------------- | ------- | --- | --- | --- | --- |
emergenceofnon-bayesianin-contextlearningfor Richard Socher, Alex Perelygin, Jean Wu, Jason
regression. InAdvancesinNeuralInformationPro- Chuang, Christopher D. Manning, Andrew Y. Ng,
cessingSystems36: AnnualConferenceonNeural andChristopherPotts.2013b. Recursivedeepmod-
InformationProcessingSystems2023,NeurIPS2023,
elsforsemanticcompositionalityoverasentiment
NewOrleans,LA,USA,December10-16,2023. treebank. InProceedingsofthe2013Conferenceon
EmpiricalMethodsinNaturalLanguageProcessing,
Ohad Rubin, Jonathan Herzig, and Jonathan Berant. EMNLP 2013, 18-21 October 2013, Grand Hyatt
2022. Learning to retrieve prompts for in-context Seattle,Seattle,Washington,USA,AmeetingofSIG-
| learning.                                  | InProceedingsofthe2022Conferenceof |                    |     |                |                  |              |            |
| ------------------------------------------ | ---------------------------------- | ------------------ | --- | -------------- | ---------------- | ------------ | ---------- |
|                                            |                                    |                    |     | DAT, a         | Special Interest | Group of the | ACL, pages |
| theNorthAmericanChapteroftheAssociationfor |                                    |                    |     | 1631–1642.ACL. |                  |              |            |
| ComputationalLinguistics:                  |                                    | HumanLanguageTech- |     |                |                  |              |            |
nologies, pages 2655–2671, Seattle, United States. Taylor Sorensen, Joshua Robinson, Christopher Ryt-
AssociationforComputationalLinguistics. ting,AlexanderShaw,KyleRogers,AlexiaDelorey,
1120

MahmoudKhalil,NancyFulda,andDavidWingate. EshaanTanwar,SubhabrataDutta,ManishBorthakur,
2022. Aninformation-theoreticapproachtoprompt andTanmoyChakraborty.2023. Multilingualllms
engineeringwithoutgroundtruthlabels. InProc.of arebettercross-lingualin-contextlearnerswithalign-
| ACL, |       |          |         |          |             |     | InProceedingsofthe61stAnnualMeetingof |     |     |     |     |     |
| ---- | ----- | -------- | ------- | -------- | ----------- | --- | ------------------------------------- | --- | --- | --- | --- | --- |
|      | pages | 819–862, | Dublin, | Ireland. | Association |     | ment.                                 |     |     |     |     |     |
forComputationalLinguistics. theAssociationforComputationalLinguistics(Vol-
|     |     |     |     |     |     |     | ume1: LongPapers),ACL2023,Toronto,Canada, |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, July9-14,2023,pages6292–6307.Associationfor
AbuAwalMdShoeb,AbubakarAbid,AdamFisch, ComputationalLinguistics.
AdamRBrown,AdamSantoro,AdityaGupta,Adrià
Garriga-Alonso, et al. 2022. Beyond the imitation Romal Thoppilan, Daniel De Freitas, Jamie Hall,
game: Quantifyingandextrapolatingthecapabilities Noam Shazeer, Apoorv Kulshreshtha, Heng-Tze
ArXivpreprint,abs/2206.04615.
oflanguagemodels. Cheng,AliciaJin,TaylorBos,LeslieBaker,YuDu,
|     |     |     |     |     |     |     | YaGuang | Li, Hongrae |     | Lee, Huaixiu | Steven | Zheng, |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------- | --- | ------------ | ------ | ------ |
HongjinSu,JungoKasai,ChenHenryWu,WeijiaShi,
AminGhafouri,MarceloMenegali,YanpingHuang,
TianluWang,JiayiXin,RuiZhang,MariOstendorf, MaximKrikun,DmitryLepikhin,JamesQin,Dehao
LukeZettlemoyer,NoahA.Smith,andTaoYu.2023. Chen,YuanzhongXu,ZhifengChen,AdamRoberts,
Selectiveannotationmakeslanguagemodelsbetter MaartenBosma,YanqiZhou,Chung-ChingChang,
| few-shotlearners. |     |     | InTheEleventhInternationalCon- |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
IgorKrivokon,WillRusch,MarcPickett,KathleenS.
| ference |     | on Learning | Representations, |     | ICLR | 2023, |                  |     |          |        |         |        |
| ------- | --- | ----------- | ---------------- | --- | ---- | ----- | ---------------- | --- | -------- | ------ | ------- | ------ |
|         |     |             |                  |     |      |       | Meier-Hellstern, |     | Meredith | Ringel | Morris, | Tulsee |
Kigali,Rwanda,May1-5,2023.OpenReview.net.
Doshi,RenelitoDelosSantos,TojuDuke,JohnnySo-
raker,BenZevenbergen,VinodkumarPrabhakaran,
| Tianxiang |     | Sun, Yunfan | Shao, | Hong  | Qian,     | Xuanjing |            |     |             |     |         |             |
| --------- | --- | ----------- | ----- | ----- | --------- | -------- | ---------- | --- | ----------- | --- | ------- | ----------- |
|           |     |             |       |       |           |          | Mark Diaz, | Ben | Hutchinson, |     | Kristen | Olson, Ale- |
| Huang,    |     | and Xipeng  | Qiu.  | 2022. | Black-box | tuning   |            |     |             |     |         |             |
jandraMolina,ErinHoffman-John,JoshLee,Lora
| for | language-model-as-a-service. |     |     |     | ArXiv | preprint, |             |            |     |       |          |         |
| --- | ---------------------------- | --- | --- | --- | ----- | --------- | ----------- | ---------- | --- | ----- | -------- | ------- |
|     |                              |     |     |     |       |           | Aroyo, Ravi | Rajakumar, |     | Alena | Butryna, | Matthew |
abs/2201.03514.
Lamm,ViktoriyaKuzmina,JoeFenton,AaronCo-
hen,RachelBernstein,RayKurzweil,BlaiseAguera-
YanpengSun,QiangChen,JianWang,JingdongWang,
|                   |     |     |                              |     |     |     | Arcas, Claire | Cui, | Marian | Croak, | Ed  | H. Chi, and |
| ----------------- | --- | --- | ---------------------------- | --- | --- | --- | ------------- | ---- | ------ | ------ | --- | ----------- |
| andZechaoLi.2023. |     |     | Exploringeffectivefactorsfor |     |     |     |               |      |        |        |     |             |
improvingvisualin-contextlearning. arXivpreprint QuocLe.2022. Lamda: Languagemodelsfordialog
arXiv:2304.04748. applications. ArXivpreprint,abs/2201.08239.
Mirac Suzgun, Nathan Scales, Nathanael Schärli, Se- HugoTouvron,ThibautLavril,GautierIzacard,Xavier
bastian Gehrmann, Yi Tay, Hyung Won Chung, Martinet,Marie-AnneLachaux,TimothéeLacroix,
BaptisteRozière,NamanGoyal,EricHambro,Faisal
| Aakanksha |     | Chowdhery, |     | Quoc | V. Le, Ed | H. Chi, |     |     |     |     |     |     |
| --------- | --- | ---------- | --- | ---- | --------- | ------- | --- | --- | --- | --- | --- | --- |
Azhar,AurélienRodriguez,ArmandJoulin,Edouard
| Denny     | Zhou, | and       | Jason   | Wei. 2023.       | Challenging |     |                                 |     |     |     |     |             |
| --------- | ----- | --------- | ------- | ---------------- | ----------- | --- | ------------------------------- | --- | --- | --- | --- | ----------- |
|           |       |           |         |                  |             |     | Grave,andGuillaumeLample.2023a. |     |     |     |     | Llama: Open |
| big-bench |       | tasks and | whether | chain-of-thought |             | can |                                 |     |     |     |     |             |
solvethem. InFindingsoftheAssociationforCom- and efficient foundation language models. CoRR,
| putationalLinguistics: |     |     | ACL2023,Toronto,Canada, |     |     |     | abs/2302.13971. |     |     |     |     |     |
| ---------------------- | --- | --- | ----------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
July9-14,2023,pages13003–13051.Associationfor
|     |     |     |     |     |     |     | Hugo Touvron, | Louis | Martin, | Kevin | Stone, | Peter Al- |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ----- | ------- | ----- | ------ | --------- |
ComputationalLinguistics.
|     |     |     |     |     |     |     | bert, Amjad | Almahairi, |     | Yasmine | Babaei, | Nikolay |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | ------- | ------- | ------- |
Bashlykov,SoumyaBatra,PrajjwalBhargava,Shruti
| Alon | Talmor, | Jonathan | Herzig, | Nicholas | Lourie, | and |     |     |     |     |     |     |
| ---- | ------- | -------- | ------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
Bhosale,DanBikel,LukasBlecher,CristianCanton-
| JonathanBerant.2019. |     |     |     | CommonsenseQA:Aques- |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Ferrer,MoyaChen,GuillemCucurull,DavidEsiobu,
| tion | answering | challenge |     | targeting | commonsense |     |     |     |     |     |     |     |
| ---- | --------- | --------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
knowledge. InProceedingsofthe2019Conference JudeFernandes,JeremyFu,WenyinFu,BrianFuller,
oftheNorthAmericanChapteroftheAssociationfor CynthiaGao,VedanujGoswami,NamanGoyal,An-
thonyHartshorn,SagharHosseini,RuiHou,Hakan
| ComputationalLinguistics: |     |     |     | HumanLanguageTech- |     |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Inan,MarcinKardas,ViktorKerkez,MadianKhabsa,
nologies,Volume1(LongandShortPapers),pages
IsabelKloumann,ArtemKorenev,PunitSinghKoura,
4149–4158,Minneapolis,Minnesota.Associationfor
ComputationalLinguistics. Marie-AnneLachaux,ThibautLavril,JenyaLee,Di-
anaLiskovich,YinghaiLu,YuningMao,XavierMar-
RuixiangTang,DehanKong,LongtaoHuang,andHui tinet,TodorMihaylov,PushkarMishra,IgorMoly-
Xue. 2023a. Large language models can be lazy bog, Yixin Nie, Andrew Poulton, Jeremy Reizen-
learners: Analyze shortcuts in in-context learning. stein,RashiRungta,KalyanSaladi,AlanSchelten,
In Findings of the Association for Computational Ruan Silva, Eric Michael Smith, Ranjan Subrama-
Linguistics: ACL2023,Toronto,Canada,July9-14, nian, Xiaoqing Ellen Tan, Binh Tang, Ross Tay-
2023,pages4645–4657.AssociationforComputa- lor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
tionalLinguistics. ZhengYan,IliyanZarov,YuchenZhang,AngelaFan,
|     |     |     |     |     |     |     | Melanie | Kambadur, | Sharan | Narang, |     | Aurélien Ro- |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ------ | ------- | --- | ------------ |
YutingTang,RatishPuduppully,ZhengyuanLiu,and
driguez,RobertStojnic,SergeyEdunov,andThomas
| NancyChen.2023b. |     |     | In-contextlearningoflargelan- |     |     |     |          |        |       |         |            |     |
| ---------------- | --- | --- | ----------------------------- | --- | --- | --- | -------- | ------ | ----- | ------- | ---------- | --- |
|                  |     |     |                               |     |     |     | Scialom. | 2023b. | Llama | 2: Open | foundation | and |
guagemodelsforcontrolleddialoguesummarization:
|                                         |     |     |     |     |     |        | fine-tunedchatmodels. |     |     | CoRR,abs/2307.09288. |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | ------ | --------------------- | --- | --- | -------------------- | --- | --- |
| Aholisticbenchmarkandempiricalanalysis. |     |     |     |     |     | InPro- |                       |     |     |                      |     |     |
ceedingsofthe4thNewFrontiersinSummarization Maria Tsimpoukelli, Jacob Menick, Serkan Cabi,
Workshop,pages56–67,Singapore.Associationfor S.M.AliEslami,OriolVinyals,andFelixHill.2021.
ComputationalLinguistics. Multimodalfew-shotlearningwithfrozenlanguage
1121

models. In Advances in Neural Information Pro- Xinlong Wang, Wen Wang, Yue Cao, Chunhua Shen,
cessingSystems34: AnnualConferenceonNeural andTiejunHuang.2023c. Imagesspeakinimages:
InformationProcessingSystems2021,NeurIPS2021, Ageneralistpainterforin-contextvisuallearning. In
December6-14,2021,virtual,pages200–212. ProceedingsoftheIEEE/CVFConferenceonCom-
puterVisionandPatternRecognition,pages6830–
| KarthikValmeekam,AlbertoOlmo,SarathSreedharan, |     |     |               |     | 6839. |     |     |     |     |
| ---------------------------------------------- | --- | --- | ------------- | --- | ----- | --- | --- | --- | --- |
| andSubbaraoKambhampati.2022.                   |     |     | Largelanguage |     |       |     |     |     |     |
modelsstillcan’tplan(abenchmarkforllmsonplan- XinlongWang,XiaosongZhang,YueCao,WenWang,
ningandreasoningaboutchange). ArXivpreprint, Chunhua Shen, and Tiejun Huang. 2023d. Seg-
abs/2206.10498. gpt: Towardssegmentingeverythingincontext. In
|     |     |     |     |     | IEEE/CVF International |     | Conference | on Computer |     |
| --- | --- | --- | --- | --- | ---------------------- | --- | ---------- | ----------- | --- |
JohannesvonOswald,EyvindNiklasson,EttoreRan- Vision,ICCV2023,Paris,France,October1-6,2023,
dazzo,JoãoSacramento,AlexanderMordvintsev,An- pages1130–1140.IEEE.
| dreyZhmoginov,andMaxVladymyrov.2023. |     |     |     | Trans- |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
formerslearnin-contextbygradientdescent. InIn- XinyiWang,WanrongZhu,andWilliamYangWang.
ternationalConferenceonMachineLearning,ICML 2023e. Large language models are implicitly
2023,23-29July2023,Honolulu,Hawaii,USA,vol- topicmodels: Explainingandfindinggooddemon-
ume 202 of Proceedings of Machine Learning Re- strations for in-context learning. arXiv preprint
| search,pages35151–35174.PMLR. |     |     |     |     | arXiv:2301.11916. |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- |
AlexWang,YadaPruksachatkun,NikitaNangia,Aman- YaqingWangandQuanmingYao.2019. Few-shotlearn-
preetSingh,JulianMichael,FelixHill,OmerLevy, ing: Asurvey. CoRR,abs/1904.05046.
| andSamuelR.Bowman.2019. |     | Superglue:Astickier |     |     |     |     |     |     |     |
| ----------------------- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
YizhongWang,YeganehKordi,SwaroopMishra,Alisa
benchmarkforgeneral-purposelanguageunderstand-
Liu,NoahA.Smith,DanielKhashabi,andHannaneh
| ing systems. | In Advances | in Neural | Information |     |     |     |     |     |     |
| ------------ | ----------- | --------- | ----------- | --- | --- | --- | --- | --- | --- |
ProcessingSystems32: AnnualConferenceonNeu- Hajishirzi.2023f. Self-instruct: Aligninglanguage
ralInformationProcessingSystems2019,NeurIPS modelswithself-generatedinstructions. InProceed-
2019,December8-14,2019,Vancouver,BC,Canada, ingsofthe61stAnnualMeetingoftheAssociation
|     |     |     |     |     | forComputationalLinguistics(Volume1: |     |     | LongPa- |     |
| --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | ------- | --- |
pages3261–3275.
pers),ACL2023,Toronto,Canada,July9-14,2023,
Ben Wang and Aran Komatsuzaki. 2021. GPT-J- pages13484–13508.AssociationforComputational
| 6B: A 6     | Billion Parameter              | Autoregressive |     | Lan- | Linguistics. |     |     |     |     |
| ----------- | ------------------------------ | -------------- | --- | ---- | ------------ | --- | --- | --- | --- |
| guageModel. | https://github.com/kingoflolz/ |                |     |      |              |     |     |     |     |
mesh-transformer-jax. Yizhong Wang, Swaroop Mishra, Pegah Alipoormo-
labashi,YeganehKordi,AmirrezaMirzaei,Atharva
BoshiWang,XiangDeng,andHuanSun.2022a. Itera- Naik,ArjunAshok,ArutSelvanDhanasekaran,An-
|     |     |     |     |     | jana Arunkumar, | David | Stap, Eshaan | Pathak, | Gi- |
| --- | --- | --- | --- | --- | --------------- | ----- | ------------ | ------- | --- |
tivelypromptpre-trainedlanguagemodelsforchain
ofthought. InProceedingsofthe2022Conference annisKaramanolakis,HaizhiGaryLai,IshanPuro-
onEmpiricalMethodsinNaturalLanguageProcess- hit, Ishani Mondal, Jacob Anderson, Kirby Kuz-
ing,EMNLP2022,AbuDhabi,UnitedArabEmirates, nia,KrimaDoshi,KuntalKumarPal,MaitreyaPa-
December7-11,2022,pages2714–2730.Association tel,MehradMoradshahi,MihirParmar,MiraliPuro-
|     |     |     |     |     | hit, Neeraj | Varshney, | Phani Rohitha | Kaza, | Pulkit |
| --- | --- | --- | --- | --- | ----------- | --------- | ------------- | ----- | ------ |
forComputationalLinguistics.
Verma,RavsehajSinghPuri,RushangKaria,Savan
ChengyiWang,SanyuanChen,YuWu,ZiqiangZhang, Doshi, Shailaja Keyur Sampat, Siddhartha Mishra,
Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu, Sujan Reddy A, Sumanta Patro, Tanay Dixit, and
HuamingWang,JinyuLi,etal.2023a. Neuralcodec Xudong Shen. 2022b. Super-naturalinstructions:
languagemodelsarezero-shottexttospeechsynthe- Generalizationviadeclarativeinstructionson1600+
sizers. arXivpreprintarXiv:2301.02111. NLPtasks. InProceedingsofthe2022Conference
onEmpiricalMethodsinNaturalLanguageProcess-
LeanWang,LeiLi,DamaiDai,DeliChen,HaoZhou, ing,EMNLP2022,AbuDhabi,UnitedArabEmirates,
FandongMeng,JieZhou,andXuSun.2023b. Label December7-11,2022,pages5085–5109.Association
wordsareanchors: Aninformationflowperspective forComputationalLinguistics.
| for understanding | in-context | learning. | In  | Proceed- |     |     |     |     |     |
| ----------------- | ---------- | --------- | --- | -------- | --- | --- | --- | --- | --- |
ingsofthe2023ConferenceonEmpiricalMethods ZhendongWang,YifanJiang,YadongLu,YelongShen,
inNaturalLanguageProcessing,EMNLP2023,Sin-
|     |     |     |     |     | Pengcheng | He, Weizhu | Chen, Zhangyang |     | (Atlas) |
| --- | --- | --- | --- | --- | --------- | ---------- | --------------- | --- | ------- |
gapore,December6-10,2023,pages9840–9855.As- Wang,andMingyuanZhou.2023g. In-contextlearn-
sociationforComputationalLinguistics. ingunlockedfordiffusionmodels. InAdvancesin
|     |     |     |     |     | NeuralInformationProcessingSystems36: |     |     |     | Annual |
| --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | ------ |
ShuohangWang, YangLiu, YichongXu, Chenguang ConferenceonNeuralInformationProcessingSys-
Zhu, and Michael Zeng. 2021. Want to reduce la- tems2023, NeurIPS2023, NewOrleans, LA,USA,
| beling cost? | GPT-3 can | help. In | Findings | of the |     |     |     |     |     |
| ------------ | --------- | -------- | -------- | ------ | --- | --- | --- | --- | --- |
December10-16,2023.
| AssociationforComputationalLinguistics: |     |     |     | EMNLP |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
2021, Virtual Event / Punta Cana, Dominican Re- JasonWei, MaartenBosma, VincentY.Zhao, Kelvin
public, 16-20 November, 2021, pages 4195–4205. Guu, Adams Wei Yu, Brian Lester, Nan Du, An-
AssociationforComputationalLinguistics. drew M. Dai, and Quoc V. Le. 2022a. Finetuned
1122

languagemodelsarezero-shotlearners. InTheTenth learningasimplicitbayesianinference. InTheTenth
International Conference on Learning Representa- International Conference on Learning Representa-
tions,ICLR2022,VirtualEvent,April25-29,2022. tions,ICLR2022,VirtualEvent,April25-29,2022.
| OpenReview.net. |     |     | OpenReview.net. |     |     |     |     |     |
| --------------- | --- | --- | --------------- | --- | --- | --- | --- | --- |
Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, BenfengXu,QuanWang,ZhendongMao,YajuanLyu,
Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Qiaoqiao She, and Yongdong Zhang. 2023a. k nn
MaartenBosma,DennyZhou,DonaldMetzler,EdH. prompting:Learningbeyondthecontextwithnearest
Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy neighborinference. InInternationalConferenceon
Liang,JeffDean,andWilliamFedus.2022b. Emer- LearningRepresentations.
| gentabilitiesoflargelanguagemodels. |     | Trans.Mach. |     |     |     |     |     |     |
| ----------------------------------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
XinXu,YueLiu,PanupongPasupat,MehranKazemi,
Learn.Res.,2022.
|     |     |     | etal.2024. | In-contextlearningwithretrieveddemon- |     |     |     |     |
| --- | --- | --- | ---------- | ------------------------------------- | --- | --- | --- | --- |
JasonWei,XuezhiWang,DaleSchuurmans,Maarten
|     |     |     | strations | for language |     | models: | A survey. | arXiv |
| --- | --- | --- | --------- | ------------ | --- | ------- | --------- | ----- |
Bosma,BrianIchter,FeiXia,EdH.Chi,QuocV.Le, preprintarXiv:2401.11624.
| andDennyZhou.2022c. | Chain-of-thoughtprompt- |     |     |     |     |     |     |     |
| ------------------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- |
ing elicits reasoning in large language models. In ZhiyangXu,YingShen,andLifuHuang.2023b. Multi-
AdvancesinNeuralInformationProcessingSystems instruct: Improvingmulti-modalzero-shotlearning
35: AnnualConferenceonNeuralInformationPro- viainstructiontuning. InProceedingsofthe61stAn-
nualMeetingoftheAssociationforComputational
cessingSystems2022,NeurIPS2022,NewOrleans,
|     |     |     | Linguistics | (Volume | 1:  | Long Papers), |     | ACL 2023, |
| --- | --- | --- | ----------- | ------- | --- | ------------- | --- | --------- |
LA,USA,November28-December9,2022.
|     |     |     | Toronto, | Canada, | July | 9-14, 2023, | pages | 11445– |
| --- | --- | --- | -------- | ------- | ---- | ----------- | ----- | ------ |
JerryW.Wei,LeHou,AndrewK.Lampinen,Xiangning 11465.AssociationforComputationalLinguistics.
Chen,DaHuang,YiTay,XinyunChen,YifengLu,
Denny Zhou, Tengyu Ma, and Quoc V. Le. 2023a. SteveYadlowsky,LyricDoshi,andNileshTripuraneni.
Symboltuningimprovesin-contextlearninginlan- 2023. Pretrainingdatamixturesenablenarrowmodel
guagemodels. InProceedingsofthe2023Confer- selectioncapabilitiesintransformermodels. CoRR,
abs/2311.00871.
enceonEmpiricalMethodsinNaturalLanguagePro-
cessing,EMNLP2023,Singapore,December6-10,
|     |     |     | Jinghan Yang, | Shuming | Ma, | and | Furu Wei. | 2023a. |
| --- | --- | --- | ------------- | ------- | --- | --- | --------- | ------ |
2023,pages968–979.AssociationforComputational
Linguistics. Auto-icl: In-contextlearningwithouthumansupervi-
sion. CoRR,abs/2311.09263.
JerryW.Wei,JasonWei,YiTay,DustinTran,Albert
Webson, Yifeng Lu, Xinyun Chen, Hanxiao Liu, Zhe Yang, Damai Dai, Peiyi Wang, and Zhifang Sui.
|                 |                  |            | 2023b. Notalldemonstrationexamplesareequally |                                     |     |     |     |     |
| --------------- | ---------------- | ---------- | -------------------------------------------- | ----------------------------------- | --- | --- | --- | --- |
| Da Huang, Denny | Zhou, and Tengyu | Ma. 2023b. |                                              |                                     |     |     |     |     |
|                 |                  |            | beneficial:                                  | Reweightingdemonstrationexamplesfor |     |     |     |     |
Largerlanguagemodelsdoin-contextlearningdif-
|     |     |     | in-contextlearning. |     | InFindingsoftheAssociation |     |     |     |
| --- | --- | --- | ------------------- | --- | -------------------------- | --- | --- | --- |
ferently. CoRR,abs/2303.03846.
|     |     |     | forComputationalLinguistics: |     |     | EMNLP2023, |     | Sin- |
| --- | --- | --- | ---------------------------- | --- | --- | ---------- | --- | ---- |
NoamWies,YoavLevine,andAmnonShashua.2023. gapore,December6-10,2023,pages13209–13221.
Thelearnabilityofin-contextlearning. InAdvances AssociationforComputationalLinguistics.
| in Neural Information | Processing | Systems 36: An- |     |     |     |     |     |     |
| --------------------- | ---------- | --------------- | --- | --- | --- | --- | --- | --- |
nualConferenceonNeuralInformationProcessing JiachengYe,ZhiyongWu,JiangtaoFeng,TaoYu,and
|     |     |     | Lingpeng | Kong. | 2023. | Compositional |     | exemplars |
| --- | --- | --- | -------- | ----- | ----- | ------------- | --- | --------- |
Systems2023,NeurIPS2023,NewOrleans,LA,USA,
|     |     |     | forin-contextlearning. |     | InInternationalConference |     |     |     |
| --- | --- | --- | ---------------------- | --- | ------------------------- | --- | --- | --- |
December10-16,2023.
onMachineLearning,ICML2023,23-29July2023,
PatrickHWinston.1980. Learningandreasoningby Honolulu,Hawaii,USA,volume202ofProceedings
analogy. CommunicationsoftheACM,23(12):689– ofMachineLearningResearch,pages39818–39833.
| 703. |     |     | PMLR. |     |     |     |     |     |
| ---- | --- | --- | ----- | --- | --- | --- | --- | --- |
Zhenyu Wu, YaoXiang Wang, Jiacheng Ye, Jiangtao KangMinYoo,JunyeobKim,HyuhngJoonKim,Hyun-
Feng,JingjingXu,YuQiao,andZhiyongWu.2023a. sooCho,HwiyeolJo,Sang-WooLee,Sang-gooLee,
Openicl: Anopen-sourceframeworkforin-context andTaeukKim.2022. Ground-truthlabelsmatter:
|     |     |     | A deeper | look into | input-label | demonstrations. |     | In  |
| --- | --- | --- | -------- | --------- | ----------- | --------------- | --- | --- |
learning. CoRR,abs/2303.02913.
|     |     |     | Proceedings | of the | 2022 | Conference | on  | Empirical |
| --- | --- | --- | ----------- | ------ | ---- | ---------- | --- | --------- |
ZhiyongWu,YaoxiangWang,JiachengYe,andLing- MethodsinNaturalLanguageProcessing,EMNLP
peng Kong. 2023b. Self-adaptive in-context learn- 2022,AbuDhabi,UnitedArabEmirates,December
ing: Aninformationcompressionperspectiveforin- 7-11,2022,pages2422–2437.AssociationforCom-
| contextexampleselectionandordering. |     | InProceed- | putationalLinguistics. |     |     |     |     |     |
| ----------------------------------- | --- | ---------- | ---------------------- | --- | --- | --- | --- | --- |
ingsofthe61stAnnualMeetingoftheAssociationfor
ComputationalLinguistics(Volume1: LongPapers), XiangZhang,JunboJakeZhao,andYannLeCun.2015.
ACL2023,Toronto,Canada,July9-14,2023,pages Character-levelconvolutionalnetworksfortextclas-
| 1423–1436.AssociationforComputationalLinguis- |     |     | sification. | InNIPS. |     |     |     |     |
| --------------------------------------------- | --- | --- | ----------- | ------- | --- | --- | --- | --- |
tics.
|     |     |     | YimingZhang,ShiFeng,andChenhaoTan.2022a. |     |     |     |     | Ac- |
| --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
Sang Michael Xie, Aditi Raghunathan, Percy Liang, tive example selection for in-context learning. In
andTengyuMa.2022. Anexplanationofin-context Proceedings of the 2022 Conference on Empirical
1123

MethodsinNaturalLanguageProcessing,EMNLP Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han,
2022,AbuDhabi,UnitedArabEmirates,December KeiranPaster,SilviuPitis,HarrisChan,andJimmy
7-11,2022,pages9134–9148.AssociationforCom- Ba.2023c. Largelanguagemodelsarehuman-level
|                        |     |     |     |     |     |     |     |        |            |     | The Eleventh | International |     |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | ------------ | ------------- | --- |
| putationalLinguistics. |     |     |     |     |     |     |     | prompt | engineers. | In  |              |               |     |
ConferenceonLearningRepresentations,ICLR2023,
YimingZhang,ShiFeng,andChenhaoTan.2022b. Ac- Kigali,Rwanda,May1-5,2023.OpenReview.net.
| tive example |     | selection | for | in-context | learning. | In  |     |     |     |     |     |     |     |
| ------------ | --- | --------- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Proceedings of the 2022 Conference on Empirical Yuxiang Zhou, Jiazheng Li, Yanzheng Xiang, Hanqi
MethodsinNaturalLanguageProcessing,EMNLP
|     |     |     |     |     |     |     |     | Yan, Lin | Gui, | and Yulan | He. 2023d. | The | mystery |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---- | --------- | ---------- | --- | ------- |
2022,AbuDhabi,UnitedArabEmirates,December
|     |     |     |     |     |     |     |     | andfascinationofllms: |     |     | Acomprehensivesurveyon |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ---------------------- | --- | --- |
7-11,2022,pages9134–9148.AssociationforCom- theinterpretationandanalysisofemergentabilities.
| putationalLinguistics. |     |     |     |     |     |     |     | arXivpreprintarXiv:2311.00237. |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- |
YuanhanZhang,KaiyangZhou,andZiweiLiu.2023a.
|           |                                   |      |          |     |        |            | DeyaoZhu, |                         | JunChen, | XiaoqianShen, |            | XiangLi, | and       |
| --------- | --------------------------------- | ---- | -------- | --- | ------ | ---------- | --------- | ----------------------- | -------- | ------------- | ---------- | -------- | --------- |
| What      | makes                             | good | examples | for | visual | in-context |           |                         |          |               |            |          |           |
|           |                                   |      |          |     |        |            |           | MohamedElhoseiny.2023a. |          |               | Minigpt-4: |          | Enhancing |
| learning? | InAdvancesinNeuralInformationPro- |      |          |     |        |            |           |                         |          |               |            |          |           |
vision-languageunderstandingwithadvancedlarge
cessingSystems36: AnnualConferenceonNeural languagemodels. arXivpreprintarXiv:2304.10592.
InformationProcessingSystems2023,NeurIPS2023,
NewOrleans,LA,USA,December10-16,2023.
WenhaoZhu,HongyiLiu,QingxiuDong,JingjingXu,
|               |       |          |        |      |         |           |     | Lingpeng     | Kong, | Jiajun                             | Chen, Lei | Li, | and Shujian |
| ------------- | ----- | -------- | ------ | ---- | ------- | --------- | --- | ------------ | ----- | ---------------------------------- | --------- | --- | ----------- |
| Yufeng Zhang, |       | Fengzhuo | Zhang, |      | Zhuoran | Yang, and |     |              |       |                                    |           |     |             |
|               |       |          |        |      |         |           |     | Huang.2023b. |       | Multilingualmachinetranslationwith |           |     |             |
| Zhaoran       | Wang. | 2023b.   |        | What | and how | does in-  |     |              |       |                                    |           |     |             |
context learning learn? bayesian model averag- largelanguagemodels: Empiricalresultsandanaly-
sis. arXivpreprintarXiv:2304.04675.
| ing, parameterization, |     |     | and | generalization. |     | CoRR, |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
abs/2305.19420.
A Takeaway
| Zhuosheng    | Zhang, | Aston                          | Zhang, |     | Mu Li, | and Alex |     |     |     |     |     |     |     |
| ------------ | ------ | ------------------------------ | ------ | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
| Smola.2023c. |        | Automaticchainofthoughtprompt- |        |     |        |          |     |     |     |     |     |     |     |
ThroughacomprehensiveliteraturereviewofICL,
| ing in | large | language | models. |     | In The Eleventh | In- |     |      |            |           |        |     |             |
| ------ | ----- | -------- | ------- | --- | --------------- | --- | --- | ---- | ---------- | --------- | ------ | --- | ----------- |
|        |       |          |         |     |                 |     | we  | have | discovered | takeaways | across |     | several do- |
ternationalConferenceonLearningRepresentations,
|     |     |     |     |     |     |     | mains. |     | Theseincludetraining, |     | demonstrationde- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --------------------- | --- | ---------------- | --- | --- |
ICLR2023,Kigali,Rwanda,May1-5,2023.Open-
| Review.net. |     |     |     |     |     |     | sign,scoringfunctions,analysis,andICLapplica- |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
tionsthatgobeyondtext.
ZiqiangZhang,LongZhou,ChengyiWang,Sanyuan
Chen,YuWu,ShujieLiu,ZhuoChen,YanqingLiu,
| Huaming | Wang, | Jinyu | Li, | et al. | 2023d. | Speak for- | A.1 | Training |     |     |     |     |     |
| ------- | ----- | ----- | --- | ------ | ------ | ---------- | --- | -------- | --- | --- | --- | --- | --- |
eignlanguageswithyourownvoice: Cross-lingual TofurtherenhancedICLcapabilities,methodspro-
| neural | codec | language | modeling. |     | arXiv | preprint |     |     |     |     |     |     |     |
| ------ | ----- | -------- | --------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
posetotraintheLLMsinthestageofpre-training
arXiv:2303.03926.
andwarmupbeforeICLinference.
| Zihao Zhao, | Eric | Wallace, | Shi | Feng, | Dan | Klein, and |     | 3Takeaway: |     |     |     |     |     |
| ----------- | ---- | -------- | --- | ----- | --- | ---------- | --- | ---------- | --- | --- | --- | --- | --- |
(1)Thekeyideaoftrainingbefore
| Sameer | Singh. | 2021. | Calibrate |     | before | use: Im- |     |     |     |     |     |     |     |
| ------ | ------ | ----- | --------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
inferenceistobridgethegapbetweenpretraining
provingfew-shotperformanceoflanguagemodels.
|          |     |       |        |     |                |     | and | downstream |     | ICL | formats by | introducing | ob- |
| -------- | --- | ----- | ------ | --- | -------------- | --- | --- | ---------- | --- | --- | ---------- | ----------- | --- |
| In Proc. | of  | ICML, | volume | 139 | of Proceedings | of  |     |            |     |     |            |             |     |
Machine Learning Research, pages 12697–12706. jectives close to in-context learning. Warmup is
| PMLR.       |           |     |          |     |      |            | optional   |     | for ICL | as many      | pretrained | LLMs     | have   |
| ----------- | --------- | --- | -------- | --- | ---- | ---------- | ---------- | --- | ------- | ------------ | ---------- | -------- | ------ |
|             |           |     |          |     |      |            | manifested |     | the     | ICL ability. | (2)        | Compared | to in- |
| Denny Zhou, | Nathanael |     | Schärli, | Le  | Hou, | Jason Wei, |            |     |         |              |            |          |        |
contextfinetuninginvolvingdemonstration,instruc-
| Nathan | Scales, | Xuezhi | Wang, |     | Dale Schuurmans, |     |     |     |     |     |     |     |     |
| ------ | ------- | ------ | ----- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tionfinetuningwithoutafewexamplesasdemon-
ClaireCui,OlivierBousquet,QuocV.Le,andEdH.
Chi.2023a. Least-to-mostpromptingenablescom- stration is simpler and more popular. All these
| plex reasoning |     | in  | large language |     | models. | In The |        |     |         |         |         |            |     |
| -------------- | --- | --- | -------------- | --- | ------- | ------ | ------ | --- | ------- | ------- | ------- | ---------- | --- |
|                |     |     |                |     |         |        | warmup |     | methods | improve | the ICL | capability | by  |
EleventhInternationalConferenceonLearningRep-
resentations,ICLR2023,Kigali,Rwanda,May1-5, updatingthemodelparameters,whichimpliesthat
theICLcapabilityoftheoriginalLLMshasgreat
2023.OpenReview.net.
|     |     |     |     |     |     |     | potential |     | for improvement. |     | Therefore, |     | although |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------------- | --- | ---------- | --- | -------- |
HattieZhou,AzadeNova,HugoLarochelle,AaronC.
|            |        |     |            |     |           |         | ICL | does | not | strictly require | model | warmup, | we  |
| ---------- | ------ | --- | ---------- | --- | --------- | ------- | --- | ---- | --- | ---------------- | ----- | ------- | --- |
| Courville, | Behnam |     | Neyshabur, |     | and Hanie | Sedghi. |     |      |     |                  |       |         |     |
recommendaddingawarmupstagebeforeICLin-
2022. Teachingalgorithmicreasoningviain-context
learning. CoRR,abs/2211.09066. ference. (3)Theperformanceadvancementmade
bywarmupencountersaplateauwhenincreasingly
WangchunshuZhou,YuchenEleanorJiang,RyanCot-
scalingupthetrainingdata,indicatingthatLLMs
| terell, | and Mrinmaya |     | Sachan. |     | 2023b. | Efficient |     |     |     |     |     |     |     |
| ------- | ------------ | --- | ------- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
onlyneedasmallamountofdatatoadapttolearn
| promptingviadynamicin-contextlearning. |     |     |     |     |     | CoRR, |                             |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | ----- | --------------------------- | --- | --- | --- | --- | --- | --- |
| abs/2305.11170.                        |     |     |     |     |     |       | fromthecontextduringwarmup. |     |     |     |     |     |     |
1124

| A.2 DemonstrationOrganization |     |     |     |     |     |     | A.4 Analysis |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
Numerousanalyticalstudiesinvestigateinfluencing
| The performance |     | of  | ICL | strongly | relies | on the |     |     |     |     |     |     |
| --------------- | --- | --- | --- | -------- | ------ | ------ | --- | --- | --- | --- | --- | --- |
factorsofICLduringboththepretrainingandinfer-
demonstrationsurface,includingtheselection,for-
encestages,andattempttofigureoutthelearning
matting,andorderingofdemonstrationexamples.
mechanismsofICLfromtheperspectiveoffunc-
3 Takeaway: (1) Demonstration selection tionalmodulesandtheoreticalinterpretation.
strategiesimprovetheICLperformance,butmost 3Takeaway: (1)Knowingandconsideringwhy
| of them | are instance |     | level. | Since | ICL | is mainly |     |     |     |     |     |     |
| ------- | ------------ | --- | ------ | ----- | --- | --------- | --- | --- | --- | --- | --- | --- |
ICLworksandwhatfactorsmayinfluencecanhelp
evaluatedunderfew-shotsettings,thecorpus-level
|     |     |     |     |     |     |     | us improve | the | ICL | performance. | (2) | Although |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | ------------ | --- | -------- |
selection strategy is more important yet underex- some analytical studies have taken a preliminary
plored. (2)Theoutputscoreorprobabilitydistri-
|     |     |     |     |     |     |     | step to | explain | ICL, | most of them | are | limited to |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ---- | ------------ | --- | ---------- |
butionofLLMsplaysanimportantroleininstance
|     |     |     |     |     |     |     | simpletasksandsmallmodels. |     |     | Extendinganalysis |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ----------------- | --- | --- |
selecting. (3) For k demonstrations, the size of on extensive tasks and large models may be the
| searchspaceofpermutationsisk!. |             |     |     |        | Howtofindthe |     |           |       |             |     |       |          |
| ------------------------------ | ----------- | --- | --- | ------ | ------------ | --- | --------- | ----- | ----------- | --- | ----- | -------- |
|                                |             |     |     |        |              |     | next step | to be | considered. | (3) | Among | existing |
| best orders                    | efficiently |     | or  | how to | approximate  | the |           |       |             |     |       |          |
work,explainingICLwithgradientdescentseems
optimalrankingbetterisalsoachallengingques- tobeareasonable,general,andpromisingdirection
tion. (4)Addingchain-of-thoughtscaneffectively forfutureresearch. Ifwebuildclearconnections
decomposecomplexreasoningtasksintointermedi-
betweenICLandgradient-descent-basedlearning,
| atereasoningsteps. |     |     | Duringinference,multi-stage |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
wecanborrowideasfromthehistoryoftraditional
demonstrationdesigningstrategiesareappliedto deeplearningtoimproveICL.
| generate | CoTs | better. | How | to  | improve | the CoT |     |     |     |     |     |     |
| -------- | ---- | ------- | --- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
prompting ability of LLMs is also worth explor- A.5 In-contextLearningBeyondText
| ing. (5) | In addition |     | to human-written |     | demonstra- |     |                |     |         |        |        |         |
| -------- | ----------- | --- | ---------------- | --- | ---------- | --- | -------------- | --- | ------- | ------ | ------ | ------- |
|          |             |     |                  |     |            |     | The tremendous |     | success | of ICL | in NLP | has in- |
tions,thegenerativenatureofLLMscanbeutilized spiredresearcherstoexplorein-contextlearningin
| in demonstration |     | designing. |     | LLMs | can | generate |     |     |     |     |     |     |
| ---------------- | --- | ---------- | --- | ---- | --- | -------- | --- | --- | --- | --- | --- | --- |
differentmodalitiesbeyondnaturallanguagewith
| instructions, | demonstrations, |     |     | probing | sets, | chain- |     |     |     |     |     |     |
| ------------- | --------------- | --- | --- | ------- | ----- | ------ | --- | --- | --- | --- | --- | --- |
promisingresults.
| of-thoughts,andsoon. |     |     | ByusingLLM-generated |     |     |     | 3Takeaway: |     |     |     |     |     |
| -------------------- | --- | --- | -------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- |
(1)Properlyformatteddata(e.g.,
demonstrations,ICLcanlargelygetridofhuman
interleavedimage-textdatasetsforvision-language
effortsonwritingtemplates.
|     |     |     |     |     |     |     | tasks) and | architecture |     | designs | are key | factors |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | --- | ------- | ------- | ------- |
foractivatingthepotentialofin-contextlearning.
A.3 ScoringFunction Exploring it in a more complex structured space
suchasforgraphdataischallengingandpromis-
Thescoringfunctiondetermineshowtotransform ing(Huangetal.,2023a). (2)Findingsintextual
the predictions of a language model into an esti- in-contextlearningdemonstrationdesignandselec-
tioncannotbetriviallytransferredtoothermodal-
| mationofthelikelihoodofaspecificanswer. |     |     |     |     |     | The |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ities. Domain-specificinvestigationisrequiredto
answerwiththehighestprobabilityisselectedas
thefinalanswer. fullyleveragethepotentialofin-contextlearning
invariousmodalities.
| 3 Takeaway: |     | (1) | Although |     | directly | adopting |     |     |     |     |     |     |
| ----------- | --- | --- | -------- | --- | -------- | -------- | --- | --- | --- | --- | --- | --- |
theconditionalprobabilityofcandidateanswersis
B ExperimentalDetail
efficient,thismethodstillposessomerestrictions
on the template design. Perplexity is also a sim- In the experiment, we utilize 8 demonstra-
pleandwidelyscoringfunction. Thismethodhas tions and test on gpt2 (Radford et al., 2019),
universalapplications,includingbothclassification gptj (Wang and Komatsuzaki, 2021), LLaMA3-
tasksandgenerationtasks. However,bothmethods 8B-Instruct(AI@Meta, 2024) and Qwen2-7B-
arestillsensitivetodemonstrationsurface,while Instruct (Bai et al., 2023a). All experiments are
Channel is a remedy that especially works under executed on a single NVIDIA A100 (80G). For
imbalanceddataregimes. (2)Existingscoringfunc- datasets we choose sst2 (Socher et al., 2013a),
tions all compute a score straightforwardly from sst5(Socheretal.,2013b),commonsense_qa(Tal-
theconditionalprobabilityofLLMs. Thereislim- mor et al., 2019), ag_news (Zhang et al., 2015)
itedresearchoncalibratingthebiasormitigating and snli (Bowman et al., 2015). For the last two
thesensitivityviascoringstrategies. datasets, weonlyselect1000datafromthetrain-
1125

| Model | Direct      |              | PPL |              | Channel | Benchmark |     | Tasks      |     |     | #Tasks |
| ----- | ----------- | ------------ | --- | ------------ | ------- | --------- | --- | ---------- | --- | --- | ------ |
| GPT2  | 44.13(1.00) | 114.02(2.58) |     | 157.70(3.57) |         | BIG-Bench |     |            |     |     |        |
|       |             |              |     |              |         |           |     | Mixedtasks |     |     | 204    |
(Srivastavaetal.,2022)
| GPT-J | 611.04(1.00) | 1766.82(2.89) |     | 1793.27(2.93) |     | BBH |     |                  |     |     |     |
| ----- | ------------ | ------------- | --- | ------------- | --- | --- | --- | ---------------- | --- | --- | --- |
|       |              |               |     |               |     |     |     | Unsolvedproblems |     |     | 23  |
(Suzgunetal.,2023)
| Qwen2 | 745.89(1.00) | 1886.63(2.53) |     | 1957.97(2.63) |     |     |     |     |     |     |     |
| ----- | ------------ | ------------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
PRONTOQA
|        |              |               |     |               |     | (SaparovandHe,2023) |     | Questionanswering |     |     | 1   |
| ------ | ------------ | ------------- | --- | ------------- | --- | ------------------- | --- | ----------------- | --- | --- | --- |
| Llama3 | 790.46(1.00) | 1935.04(2.45) |     | 1956.21(2.47) |     |                     |     |                   |     |     |     |
MGSM
|     |     |     |     |     |     |     |     | Mathproblems |     |     | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- |
(Shietal.,2022)
| AVG | 1.00 |     | 2.61 |     | 2.90 |     |     |     |     |     |     |
| --- | ---- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- |
LLMAS
|     |     |     |     |     |     |     |     | Planandreasoningtasks |     |     | 8   |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- |
(Valmeekametal.,2022)
Table4: ThequalitativeresultsoftheEfficiencymet-
OPT-IMLBench
|                                              |            |                          |          |         |           |                  |             | Mixedtasks |            |            | 2000 |
| -------------------------------------------- | ---------- | ------------------------ | -------- | ------- | --------- | ---------------- | ----------- | ---------- | ---------- | ---------- | ---- |
| ricinTable3whichrecordthelanguagemodelinfer- |            |                          |          |         |           | (Iyeretal.,2022) |             |            |            |            |      |
| ence latency                                 | (including | the                      | time for | scoring | with dif- |                  |             |            |            |            |      |
|                                              |            |                          |          |         |           | Table 6: New     | challenging |            | evaluation | benchmarks | for  |
| ferentscoringfunctions,                      |            | withinputdatacontaining8 |          |         |           |                  |             |            |            |            |      |
in-context examples). The unit is milliseconds (ms). ICL.Forshort,weuseLLMAStorepresentLLMAs-
Eachcell’sparenthesescontaintheratioofthelatency sessmentSuite(Valmeekametal.,2022).
forthecurrentcolumnmodelusingthecurrentrowscor-
| ingfunctiontothelatencyusingdirectinference. |     |     |     |     | The |     |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
finalcalculatedaverageistheaverageoftheseratios. 3 can achieve results comparable to state-of-the-
art(SOTA)finetuningperformanceonCOPAand
Model Direct PPL Channel ReCoRD,butstillfallsbehindfinetuningonmost
|      |      |     |      |     |      | NLU tasks. | Hao | et al. | (2022b) | showed | the po- |
| ---- | ---- | --- | ---- | --- | ---- | ---------- | --- | ------ | ------- | ------ | ------- |
| GPT2 | 1.12 |     | 0.85 |     | 3.18 |            |     |        |         |        |         |
tentialofscalingupthenumberofdemonstration
| GPT-J | 1.00 |     | 0.77 |     | 4.06 |            |                                 |     |             |          |     |
| ----- | ---- | --- | ---- | --- | ---- | ---------- | ------------------------------- | --- | ----------- | -------- | --- |
|       |      |     |      |     |      | examples.  | However,theimprovementbroughtby |     |             |          |     |
| Qwen2 | 0.72 |     | 0.70 |     | 2.43 |            |                                 |     |             |          |     |
|       |      |     |      |     |      | scaling is | very limited.                   |     | At present, | compared | to  |
Llama3 0.89 0.78 2.43 finetuning,therestillremainssomeroomforICL
| AVG |      |     |      |     |      | toreachontraditionalNLPtasks. |     |     |     |     |     |
| --- | ---- | --- | ---- | --- | ---- | ----------------------------- | --- | --- | --- | --- | --- |
|     | 0.93 |     | 0.78 |     | 3.03 |                               |     |     |     |     |     |
Table5: ThequalitativeresultsoftheStabilitymetric C.2 NewChallengingTasks
inTable3whichreflectwhetherthein-contextlearning
Intheeraoflargelanguagemodelswithin-context
abilityiseasilyaffectedbychangesindemonstration
examples. Weconductedexperimentsusingatestsetof learning capabilities, researchers are more inter-
estedinevaluatingtheintrinsiccapabilitiesoflarge
| size10kandsetup5differentrandomseeds. |     |     |     |     | Eachtime, |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
8 examples were randomly selected from 5k training languagemodelswithoutdownstreamtaskfinetun-
| examples | for the experiments. |     | The | table | records the |     |     |     |     |     |     |
| -------- | -------------------- | --- | --- | ----- | ----------- | --- | --- | --- | --- | --- | --- |
ing(Bommasanietal.,2021).
varianceofperformance.
ToexplorethecapabilitylimitationsofLLMon
|     |     |     |     |     |     | various tasks, | Srivastava |     | et al. | (2022) | proposed |
| --- | --- | --- | --- | --- | --- | -------------- | ---------- | --- | ------ | ------ | -------- |
ing set for retrieval and the first 1000 data from the BIG-Bench (Srivastava et al., 2022), a large
thetestsetfortesting. Duringtheinferencephase, benchmarkcoveringalargerangeoftasks,includ-
a PPL-based approach is employed. The entire ing linguistics, chemistry, biology, social behav-
|     |     |     |     |     |     | ior, and | beyond. | The best | models | have | already |
| --- | --- | --- | --- | --- | --- | -------- | ------- | -------- | ------ | ---- | ------- |
codeframeworkisbuiltuponOpenICL(Wuetal.,
2023a), for which we extend our gratitude to the outperformed the average reported human-rater
| authors. |     |     |     |     |     | results on             | 65% of | the BIG-Bench |                       | tasks | through |
| -------- | --- | --- | --- | --- | --- | ---------------------- | ------ | ------------- | --------------------- | ----- | ------- |
|          |     |     |     |     |     | ICL(Suzgunetal.,2023). |        |               | Tofurtherexploretasks |       |         |
Table4andTable5showthequantitativeresults
ontheefficiencyandstabilitymetricsfordifferent actually unsolvable by current language models,
scoringfunctionsinTable3. Suzgunetal.(2023)proposedamorechallenging
ICLbenchmark,BIG-BenchHard(BBH).BBHin-
C EvaluationandResources cludes23unsolvedtasks,constructedbyselecting
challengingtaskswherethestate-of-artmodelper-
C.1 TraditionalTasks
formancesarefarbelowthehumanperformances.
| As a general | learning | paradigm, |     | ICL | can be ex- |     |     |     |     |     |     |
| ------------ | -------- | --------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
Besides,researchersaresearchingforinversescal-
aminedonvarioustraditionaldatasetsandbench-
|        |                 |     |       |     |             | ingtasks,2   | thatis,taskswheremodelperformance |     |     |             |      |
| ------ | --------------- | --- | ----- | --- | ----------- | ------------ | --------------------------------- | --- | --- | ----------- | ---- |
| marks, | e.g., SuperGLUE |     | (Wang | et  | al., 2019), |              |                                   |     |     |             |      |
|        |                 |     |       |     |             | reduces when | scaling                           | up  | the | model size. | Such |
SQuAD (Rajpurkar et al., 2018). Implementing tasks also highlight potential issues with the cur-
| ICL with | 32 randomly | sampled |     | examples | on Su- |     |     |     |     |     |     |
| -------- | ----------- | ------- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- |
perGLUE, Brown et al. (2020) found that GPT- 2https://github.com/inverse-scaling/prize
1126

rentparadigmofICL.Tofurtherprobethemodel VisualPromptGridImage
|     |     |     |     |     |     |     |     |     | TaskOutputImage |     |     | OutputImage |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | ----------- | --- | --- |
x x
| generalizationability, |        |            | Iyeretal.(2022)proposed |     |      |             |       |                            |                        | vp vp                                 |     |     |     |     |
| ---------------------- | ------ | ---------- | ----------------------- | --- | ---- | ----------- | ----- | -------------------------- | ---------------------- | ------------------------------------- | --- | --- | --- | --- |
|                        |        |            |                         |     | x    | x y1sk y1   | xq xq | C o n C cQ oa utn e rcny a | aI tm et e an g a te   |                                       |     |     |     |     |
| OPT-IML                | Bench, | consisting |                         | of  | 2000 | N1 L 1 P ta | s     | e                          | e                      |                                       |     |     |     |     |
|                        |        |            |                         |     |      |             |       | i n t o i  ns i t no g  s  | l ie n   g l e         | InInppaIaninipntaitniinnggt iMngo del |     |     |     |     |
|                        |        |            |                         |     |      |             |       | imaigmeage                 |                        | ModMeoldel                            |     |     |     |     |
from8existingbenchmarks,especiallybenchmark
|                             |     |     |     |     |                                                          |     |     | TaskInput |     | f   | f   |     |     |     |
| --------------------------- | --- | --- | --- | --- | -------------------------------------------------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
| forICLonheld-outcategories. |     |     |     |     | TaskT Ianspku Int puTat skT Oasukt pOuutt putQ ueQryuery |     |     | Image     |     |     |     |     |     |     |
ExamExpalempleExamExpalemple
Specifically, a series of studies focus on ex- VisuVails puraol mprpotm impta igmeage OutOpuuttput
TextVisualPrompt
ploringthereasoningabilityofICL.Saparovand
|     |     |     |     |     |     |     |                |     | Ta s k I n put | Tas k O u tput     |               | OutputImage |     | xx v x pvvpp |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------------- | ------------------ | ------------- | ----------- | --- | ------------ |
|     |     |     |     |     |     |     | TaskTextPrompt |     | I xm x1xa g e  | I my ay1yg e Query | xxq I x m age |             |     |              |
He(2023)generatedanexamplefromasynthetic 1 1 11 qq CCoCononcncacataettenenanataette e
|     |     |     |     |     |     |     | “ S e   | g m e n t  t h e  h o r s es |   f r o m   th e   |     | iDniinitnfofttuo oss  isisnoiinngnglgMelle eo  del |     |     | InIInpnpapaianiintnitntiingng g   |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------------------------- | ------------------ | --- | -------------------------------------------------- | --- | --- | --------------------------------- |
|     |     |     |     |     |     |     | re s t  | o f  th e   i m a g e  a n d |   g e n e r a te   |     |                                                    |     |     |                                   |
world model represented in first-order logic and a new image where the horse  imiimmaagagegee MMMoododedelell
|            |     |             |     |      |                                         |        | r e g io      | n s   a r e  w h i t e   a n  | d   th e                                                              |                        |           |                         |            | fff |
| ---------- | --- | ----------- | --- | ---- | --------------------------------------- | ------ | ------------- | ----------------------------- | --------------------------------------------------------------------- | ---------------------- | --------- | ----------------------- | ---------- | --- |
| parsed the | ICL | generations |     | into | symbolic                                | proofs | o th e        | r  r e g i o n s  a r e   b l | a c k .”                                                              |                        |           |                         |            |     |
|            |     |             |     |      |                                         |        |               |                               | TaTTasakssk kI n IInpnpuputu tt  TaTTasakssk kO  OOuutupttpuputu tt   | QQQuueuereyrryy        |           |                         |            |     |
|            |     |             |     |      | thatEdgLeE dLdgeetMe dcetitosenctcionan |        | Crioz la otri | iozna t ion                   | aEIinExn Epxat xiamaanmi mgnppt lpeiln leeg                           | gleemS e egn mta etnio | tna tio n | leS tt yral en  ts rfae | nr s f e r |     |
for formal analysis. They found Colo In p EExE xaxamam mpS pelpel S ty
F i g u r e 5: Ima g e - o n l y an d t e x t u a l a u g ment e d p r o V mViVs iius sup au ala t lpl i prpnorromgommpptp tit m iimmaagagegee OOOuutupttpupututt
make correct individual deduction steps via ICL. forvisualin-contextlearning.
| Shi et al. | (2022)   | constructed |                  | the | MGSM | bench-    |       |      |                     |     |      |        |     |     |
| ---------- | -------- | ----------- | ---------------- | --- | ---- | --------- | ----- | ---- | ------------------- | --- | ---- | ------ | --- | --- |
| mark to    | evaluate | the         | chain-of-thought |     |      | reasoning |       |      |                     |     |      |        |     |     |
|            |          |             |                  |     |      |           | tasks | like | image segmentation. |     | This | method | is  |     |
abilitiesofLLMsinmultilingualsettings,finding
|     |     |     |     |     |     |     | expanded |     | in Pa i n t e | r ( W ang e | t a l . , 2 023c), |     | w h i c h |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------------- | ----------- | ------------------ | --- | --------- | --- |
thatLLMsmanifestcomplexreasoningacrossmul- EEdE dgd gege e d  d edete ettecectc itoti iononn CCoC oloollor oirzri iazz atait otiiono nn InIInp npapaian iintnitn tiing ngg SSeSegegmgmmeenentnattataitotiiononn SStSyttylyelle et r tatrranansnfsseffererr
tiple languages. To further probe more sophisti- incorporates multiple tasks to develop a general-
|                |     |               |     |           |     |          | istmodelwithcompetitiveperformance. |     |     |     |     | SegGPT |     |     |
| -------------- | --- | ------------- | --- | --------- | --- | -------- | ----------------------------------- | --- | --- | --- | --- | ------ | --- | --- |
| cated planning |     | and reasoning |     | abilities |     | of LLMs, |                                     |     |     |     |     |        |     |     |
(Wangetal.,2023d)furtherbuildsonthisbyinte-
| Valmeekam | et  | al. (2022) |     | provided | multiple | test |     |     |     |     |     |     |     |     |
| --------- | --- | ---------- | --- | -------- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
casesforevaluatingvariousreasoningabilitieson grating diverse segmentation tasks and exploring
actions and change, where existing ICL methods ensembletechniquestoenhanceexamplequality.
|     |     |     |     |     |     |     | Additionally, |     | Wang | et al. (2023g) | introduce |     | the |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ---- | -------------- | --------- | --- | --- | --- |
onLLMsshowpoorperformance.
PromptDiffusionmodel,thefirstdiffusion-based
| In addition, |     | Tang | et al. | (2023b) | proposed |     | a   |     |     |     |     |     |     |     |
| ------------ | --- | ---- | ------ | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
benchmark called SAMSum, which is a human- model with ICL abilities, guided by an extra text
promptformorepreciseimagegeneration,asillus-
| annotated | dataset | specifically |     | designed |     | for multi- |     |     |     |     |     |     |     |     |
| --------- | ------- | ------------ | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
tratedinFigure5.
turndialoguesummarization,toevaluatethequal-
ityofdialoguesummariesgeneratedbyLLMsvia SimilartoICLinNLP,theeffectivenessofvisual
| ICL. |     |     |     |     |     |     | in-contextlearninggreatlydependsonthechoice |     |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
ofdemonstrationimages,asshowninresearchby
C.3 Open-sourceTools (Zhang et al., 2023a) and (Sun et al., 2023). To
|     |     |     |     |     |     |     | optimize |     | this, Zhang | et al. (2023a) | examine |     | two |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ----------- | -------------- | ------- | --- | --- | --- |
NoticingthatICLmethodsareoftenimplemented
|     |     |     |     |     |     |     | strategies: |     | usinganunsupervisedretrievertoselect |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------------------------------------ | --- | --- | --- | --- | --- |
differentlyandevaluatedusingdifferentLLMsand
thenearestsampleswithanexistingmodel,anda
| tasks, Wu | et al. | (2023a) | developed |     | OpenICL, | an  |     |     |     |     |     |     |     |     |
| --------- | ------ | ------- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
supervisedapproachtotrainaspecializedretriever
| open-source     | toolkit | enabling |     | flexible  | and           | unified |                        |     |     |                    |     |     |     |     |
| --------------- | ------- | -------- | --- | --------- | ------------- | ------- | ---------------------- | --- | --- | ------------------ | --- | --- | --- | --- |
|                 |         |          |     |           |               |         | toboostICLperformance. |     |     | Theseapproachesim- |     |     |     |     |
| ICL assessment. |         | With     | its | adaptable | architecture, |         |                        |     |     |                    |     |     |     |     |
proveresultsbyensuringsemanticsimilarityand
| OpenICL | facilitates |     | the combination |     |     | of distinct |     |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
betteralignmentinviewpoint,background,andap-
componentsandoffersstate-of-the-artretrievaland
|     |     |     |     |     |     |     | pearance. |     | Beyondretrieval,Sunetal.(2023)also |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------------------------------- | --- | --- | --- | --- | --- |
inferencetechniquestoacceleratetheintegration
|     |     |     |     |     |     |     | investigate |     | a prompt | fusion technique |     | to further |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------- | ---------------- | --- | ---------- | --- | --- |
ofICLintoadvancedresearch.
enhanceoutcomes.
D In-ContextLearningBeyondText
D.2 Multi-ModalIn-ContextLearning
| The tremendous |     | success | of  | ICL | in NLP | has in- |     |                     |     |         |          |         |     |     |
| -------------- | --- | ------- | --- | --- | ------ | ------- | --- | ------------------- | --- | ------- | -------- | ------- | --- | --- |
|                |     |         |     |     |        |         | In  | the vision-language |     | domain, | a vision | encoder |     |     |
spiredresearcherstoexploreitspotentialindiffer- pairedwithafrozenlanguagemodeldemonstrates
entmodalities,includingvisual,vision+language multi-modal few-shot learning capabilities after
andspeechtasksaswell.
trainingonimage-captiondatasets,asshownbythe
|     |     |     |     |     |     |     | Frozenmodel(Tsimpoukellietal.,2021). |     |     |     |     | Extend- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | ------- | --- | --- |
D.1 VisualIn-ContextLearning
ingthis,Flamingointegratesavisionencoderwith
Employingmaskedauto-encoders(MAE)forim- large language models (LLMs) for enhanced in-
agepatchinfilling,themodeltrainedbyBaretal. contextlearningacrossmulti-modaltasks,leverag-
(2022) generates consistent output images at in- inglarge-scalewebcorpora(Alayracetal.,2022).
ference,demonstratingrobustICLcapabilitiesfor Similarly,Kosmos-1exhibitszero-shot,few-shot,
1127

andmulti-modalchain-of-thoughtpromptingabil- andapplications.
ities (Huang et al., 2023b). METALM intro-
ducesasemi-causallanguagemodelingobjective
toachievestrongICLperformanceacrossvision-
language tasks (Hao et al., 2022a). The ICL-
D3IEapproachemploysanovelin-contextlearning
frameworkthatiterativelyupdatesdiversedemon-
strations—including hard, layout-aware, and for-
matting demonstrations to train large language
models(LLMs)forenhanceddocumentinforma-
tion extraction (DIE)(He et al., 2023). Recent
advancements include creating instruction tun-
ing datasets from existing vision-language tasks
or with advanced LLMs like GPT-4, connecting
LLMs with powerful vision foundational models
like BLIP-2 for multi-modal learning (Xu et al.,
2023b;Lietal.,2023a;Liuetal.,2023a;Zhuetal.,
2023a;Daietal.,2023b).
D.3 SpeechIn-ContextLearning
Inthespeecharea, Wangetal.(2023a)treatedtext-
to-speech synthesis as a language modeling task.
Theyuseaudiocodeccodesasanintermediaterep-
resentation and propose the first TTS framework
withstrongin-contextlearningcapability. Subse-
quently,VALLE-X(Zhangetal.,2023d)extendthe
ideatomulti-lingualscenarios,demonstratingsu-
periorperformanceinzero-shotcross-lingualtext-
to-speechsynthesisandzero-shotspeech-to-speech
translationtasks.
D.4 Comparisonwithothersurveypapers
OursurveywasdraftedandpostedontheArxivat
theendof2022,whichis,tothebestofourknowl-
edge,theveryfirsttoreviewin-contextlearningin
thefield. Wealsoregularlyupdatethissurveyina
timelymanner,withfourmajorrevisions.
Startingfrom2023,wenoticetheemergeofsev-
eralrelatedsurveyinthefieldofin-contextlearn-
ing. Xuetal.(2024)madeacomprehensivereview
onthechoicesformodels,trainingproceduresand
inferencealgorithmstoretrievedemonstrativeex-
amplesofin-contextlearning. Li(2023)provided
practicalsuggestionsonpromptengineeringforin-
contextlearning. Zhouetal.(2023d)andHighmore
(2024)focusedonthetheoreticalinterpretationand
analysis of ICL, which corresponds to Section 5
inthissurvey. Alltheabove-mentionedsurveypa-
persdifferwithoursintermsofscopeandtopics.
Thissurveyfocusedonthegeneraldevelopmentof
ICL,includingtheformaldefinitionofICL,train-
ingstrategies,promptdesigningstrategies,analysis
1128