Text-to-SQL Empowered by Large Language Models: A
Benchmark Evaluation
DaweiGao∗ HaibinWang∗ YaliangLi XiuyuSun
AlibabaGroup AlibabaGroup AlibabaGroup AlibabaGroup
gaodawei.gdw@alibaba- binke.whb@alibaba- yaliang.li@alibaba-inc.com xiuyu.sxy@alibaba-
inc.com inc.com inc.com
YichenQian BolinDing JingrenZhou
AlibabaGroup AlibabaGroup AlibabaGroup
yichen.qyc@alibaba- bolin.ding@alibaba- jingren.zhou@alibaba-
inc.com inc.com inc.com
ABSTRACT lacksasystematicstudyforpromptengineeringinLLM-basedText-
Largelanguagemodels(LLMs)haveemergedasanewparadigm to-SQLsolutions.Specifically,forquestionrepresentation,mostex-
forText-to-SQLtask.However,theabsenceofasystematicalbench- istingresearchtextualizestructuredknowledgeasschema,andfur-
markinhibitsthedevelopmentofdesigningeffective,efficientand theraddtaskinstructionsandforeignkeystoformprompts[19,29].
economicLLM-basedText-to-SQLsolutions.Toaddressthischal- Besides,somestudies[7,29]representtablesasseveral“CREATE
lenge,inthispaper,wefirstconductasystematicalandextensive TABLE”SQLstatements,andpromptLLMstoanswerthetarget
comparisonoverexistingpromptengineeringmethods,including questionincomments.However,evenwithsimilarrepresentation,
questionrepresentation,exampleselectionandexampleorganiza- theirdetailedtaskinstructionscanleadtosignificantperformance
tion,andwiththeseexperimentalresults,weelaboratetheirpros gap.Forexample,inOpenAI’sofficialText-to-SQLdemo[33],they
andcons.Basedonthesefindings,weproposeanewintegrated employthepoundsign“#”todifferentiatepromptfromresponse,
solution,namedDAIL-SQL,whichrefreshestheSpiderleaderboard yieldinganimpressiveperformance[26];Ifsuchasignisremoved,
with86.6%executionaccuracyandsetsanewbar. theperformancewillsignificantlydrop.Therefore,therearebur-
Toexplorethepotentialofopen-sourceLLM,weinvestigate geoningdemandsforasystematicstudyoverdifferentrepresenta-
theminvariousscenarios,andfurtherenhancetheirperformance tionsandexaminehowtoworkwellwithLLMs.Regardingexample
withsupervisedfine-tuning.Ourexplorationshighlightopen-source selection,acommonpracticeistoencodethemostsimilarexam-
LLMs’potentialinText-to-SQL,aswellastheadvantagesanddis- plesinthesamerepresentationwiththetargetquestion[7,26,29].
advantagesofthesupervisedfine-tuning.Additionally,towards Nanetal.[29]furtherunderlinetheimportanceofdiversityin
an efficient and economic LLM-based Text-to-SQL solution, we exampleselection.Whilefororganization,mostpriorstudiesrepre-
emphasizethetokenefficiencyinpromptengineeringandcompare sentexampleswithfullinformation,includinginstruction,schema,
thepriorstudiesunderthismetric.Wehopethatourworkprovides questionandgroundtruthSQLqueries.Besides,Guoetal.[14]
adeeperunderstandingofText-to-SQLwithLLMs,andinspires onlykeepSQLqueriesintheselectedexamplestoguidetheLLM
furtherinvestigationsandbroadapplications. withlesstokens.TogetherwithdifferentLLMs’preferences,the
optimalselectionandorganizationstrategiesinLLM-basedText-to-
SQLsolutionremainambiguous.Therefore,asystematicalstudyon
1 INTRODUCTION
promptengineering,spanningdifferentLLMs,questionrepresenta-
Text-to-SQL,asonechallengingtaskinbothnaturallanguagepro- tions,exampleselectionandorganizations,ishighlyanticipated.
cessinganddatabasecommunities,mapsnaturallanguageques- Thepotentialofopen-sourceLLMsisunderexplored.Very
tions on the given relational database into SQL queries [9, 18]. recently,open-sourceLLMsareconstantlyexpandingandshow
Mostpreviousworks[17,22,23,51,60]focusonextractingthe remarkableadvancementinprogramming,mathematicalreasoning,
question-to-SQLpatternsandgeneralizingthembytrainingan andtextgenerationtasks.However,previousText-to-SQLresearch
encoder-decodermodelwithText-to-SQLcorpus.Inrecentyears, primarily focuses on OpenAI LLMs, leaving open-source LLMs
largelanguagemodels(LLMs)haveemergedasanewparadigmfor unstudied. Besides, compared with OpenAI LLMs, open-source
Text-to-SQL[26,41,50].Notably,equippedwithGPT-4[30],Pour- onesgenerallyhavelimitedfunctionalityinunderstandingcontext
rezaetal.[37]achievedthefirstplaceinSpiderleaderboard[3]with andgeneratingcoherentresponse.Thus,acriticalchallengefor
85.3%executionaccuracy.Differentfrompriorstudies,thecore open-sourceLLMsistofurtherenhancetheirperformanceinText-
probleminLLM-basedText-to-SQLsolutionishowtopromptLLM to-SQL,whichcanbeachievedbysupervisedfine-tuning.
togeneratecorrectSQLqueries,namelypromptengineering.Such
Promptefficiencyremainsachallengingopenquestion.
promptengineeringinvolvesquestionrepresentations[7,13,33,37], InLLM-basedText-to-SQL,anothercriticalchallengeisefficiency.
examplesselection[14,28,29],andexampleorganization[14]. ThereasonisthatmostpriorstudiesfocusonOpenAILLMs,and
Text-to-SQLpromptengineeringneedsasystematicstudy. callingtheirAPIsareexpensive,time-consumingandrestricted
Althoughpriorstudieshavemaderemarkableprogress,therestill inratelimits[32],especiallyforin-contextlearningpromptswith
multipleexamples.However,thepriorstudiesmaynotwelltackle
∗Co-firstauthors.
3202
voN
02
]BD.sc[
4v36351.8032:viXra

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
thischallenge.Specifically,basedontheobservedinverted-Ushape andthreeexampleorganizationsonfourLLMs.Thestudy
in execution accuracy with respect to prompt length, Chang et shedslightonidentifyingsuitablequestionrepresentations
al.[7]conjecturesthatLLMsmayhaveasweetspotintermsof andkeypointstoleveragethein-contextlearningcapacity
promptlength,butleavesexploringefficientpromptengineeringa ofLLMsforText-to-SQLtask.
challengingopenquestion. • Tothebestofourknowledge,wearethefirsttoexplore
Inlightofabovechallenges,wefocusonprovidingacomprehen- open-sourceLLMsforbothin-contextlearningandsuper-
sive,systematicalandfairbenchmarkforLLM-basedText-to-SQL. visedfine-tuningforText-to-SQLtask.Weprovideinsights
Specifically,ourbenchmarkdiscussesboththeeffectivenessand intothepotentialoftheopen-sourceLLMsbyemploying
efficiencyofvariouspromptengineeringstrategies,aswellasthe SFTforText-to-SQLtask.
feasibilityofopen-sourceLLMs.Theyaredetailedasfollows. • Wealsoempiricallycomparedifferentpromptsinterms
Toprovideasystematicalandin-depthunderstandingofText-to- ofcostefficiency,whichprovidespracticalguidancefor
SQLpromptengineering,weempiricallyevaluateseveralstrategies real-worldText-to-SQLapplications.
frompriorstudies.First,wecompareseveraltypicalquestionrepre- • Lastbutnotleast,weproposeanewsolution,namedDAIL-
sentationsinzero-shotscenariowithdifferentLLMs,andidentify SQL,whichsuccessesinleveragingthein-contextlearning
theirprosandcons.Afterthat,weinvestigateexampleselectionand capacity of LLMs and achieving a balance between per-
organizationstrategiesinfew-shotscenario.Forexampleselection, formance and token efficiency. Notably, it refreshes the
wecomparedifferentselectionstrategiesandfurtherverifythe Spiderleaderboardwith86.6%executionaccuracy,which
hypothesisthatLLMslearnfromthemappingsbetweenquestion surpassesthebeststate-of-the-artsolutionby1.3%with
andSQLskeleton.Regardingexampleorganization,weexplore muchlesstokencost.
theoptionofdisplayingfullinformation,solelySQLqueriesor
question-SQLpair.
Afterthat,wehighlightthepotentialofopen-sourceLLMsin
bothin-contextlearningandsupervisedfine-tuning.Specifically,
we empirically study various open-source LLMs with different 2 PRELIMINARY
prompt engineering strategies, and observe the significant ben- Text-to-SQL aims at automatically translating natural language
efits of increasing scale of LLMs and having a good alignment questionsintoSQLqueries.Itbridgesthegapbetweennon-expert
[34].Tofurtherenhancetheirperformance,wefine-tuneandeval- usersanddatabasesystems,greatlyimprovestheefficiencyofdata
uateopen-sourceLLMsusingvariousrepresentations.Withthis processing,andcontributestoawiderrangeofapplicationssuchas
comparison,wedemonstratethatsimilartoin-contextlearning, intelligentdatabaseservice,automaticdataanalysisanddatabase
representationstrategyisalsocriticalforsupervisedfine-tuning. question-answering. However, Text-to-SQL is still a quiet chal-
Theseexplorationsunderlinethepotentialofaneffectivesolution lengingtask,duetothedifficultyinfullyunderstandingnatural
for Text-to-SQL. Moreover, after fine-tuning we also observe a languagequestionsandgeneratingcorrectSQLqueries[18,39].
decreaseinin-contextlearningcapability,whichrequiresfurther ExtensivestudiesofText-to-SQLhavebeenconductedinboth
study.WebelievetheseexplorationswillbenefitpracticalText-to- databaseandnaturallanguageprocessingcommunities.Someearly
SQLapplications. studiestackleText-to-SQLtaskwithpre-definedrulesorquery
Towardsamoreeconomicandefficientsolution,wefurthereval- enumeration[4,40,44],ortreatitasasequence-to-sequencetask,
uatedifferentstrategiesintermsoftokenefficiency.Suchevaluation focusingontrainingmachinelearningmodelswithanencoder-
aimsatsearchingforacost-effectivestrategy,whichissupposed decoderarchitecture[6,36,38].Withrapidadvancementofdeep
toachieveconsiderableperformancewithlesstokens.Tofulfill learning,numeroustechniquesareappliedtohelpText-to-SQLtask,
suchgoal,weconsidertokenefficiencyinthewholeprocessof suchasattentionmechanism[27],graphrepresentation[17,23,38,
promptengineering,includingchoicesforquestionrepresentation, 51, 55, 60], syntax parsing [15, 22, 43, 52], etc. One of the most
exampleselectionandorganization. representativeisBERT[11],whichhasbeenwidelyusedinText-to-
Lastbutnotleast,ourintegratedsolution,namedDAIL-SQL, SQLandachievedSOTAperformancesatthattime[5,56]. Besides,
refreshestheSpiderleaderboardwith86.6%executionaccuracy, tonarrowthegapbetweenText-to-SQLresearchanditsreal-world
andwinsthefirstplace.Comparedwithprevioussolutions,DAIL- deployment,numerouslarge-scalebenchmarkdatasetshavebeen
SQLencodesstructureknowledgeasSQLstatements,selectsex- released,includingWikiSQL[62],Spider[57],KaggleDBQA[21],
amples based on their skeleton similarities and removes cross- BIRD[24]etc.Withthesegreatefforts,theresearchcommunities
domainknowledgefromexamplesfortokenefficiency.BeforeDAIL- havemadeimpressiveprogressinText-to-SQL.
SQL,thestate-of-the-artperformanceintheSpiderleaderboardis Recently,largelanguagemodels(LLMs),suchasGPT-4[30]from
85.3%[37].Therefore,oursolutionsetsanewbar,andhopeour OpenAIandLLaMA[48]fromMeta,haveemergedasamilestone
comprehensivestudywillinspiremorefurtherworks. fornaturallanguageprocessingandmachinelearning.Different
ContributionOurmaincontributionsandresultsaresumma- fromgeneralmachinelearningmodel,LLMsarepre-trainedon
rizedasfollows: massivetextcorpus,whichcanperformvariousnaturallanguage
tasks.Thebasicoperatingprincipleistograduallyproducethenext
• WesystematicallystudypromptengineeringforLLM-based wordthathasthehighestprobabilitybasedontheinputprompt[58].
Text-to-SQLmethods,includingfivequestionrepresenta- Therefore,totackleText-to-SQLtaskwithLLMs,thecoreistofind
tions,twopromptcomponents,fourexampleselections, theoptimalprompt,alsoknownaspromptengineering[26,29].

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
Specifically,accordingtonumberofexamplesprovidedinprompt, Question EX
|     |     |     |     |     | INS RI | FK Ref. | LLMs |     |
| --- | --- | --- | --- | --- | ------ | ------- | ---- | --- |
promptengineeringareclassifiedintotwoscenarios:zero-shotsce- Representation (%)
nario and few-shot scenario. In zero-shot scenario, no example BS ✗ ✗ ✗ [37] - -
𝑃
|              |              |                           |             | TR  | ✓ ✗ | ✗ [29] CODE-DAVINCI-002 |     | 69.0 |
| ------------ | ------------ | ------------------------- | ----------- | --- | --- | ----------------------- | --- | ---- |
| is provided, | and the main | challenge is to represent | the natural |     | 𝑃   |                         |     |      |
|              |              |                           |             |     |     | [26] GPT-3.5-TURBO      |     | 70.1 |
languagequestioneffectively,includingincorporatingrelevantin- OD ✓ ✓ ✗
|     |     |     |     |     | 𝑃   | [37] | GPT-4 | 64.9 |
| --- | --- | --- | --- | --- | --- | ---- | ----- | ---- |
formationsuchasthecorrespondingdatabaseschema[7,13,26,50].
|     |     |     |     |     |     | [29] CODE-DAVINCI-002 |     | 75.6 |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | ---- |
Inthispaper,theprocessofrepresentingnaturallanguagequestions
|                                                         |     |     |     | CR  | ✓ ✗ | ✓ [7] CODE-DAVINCI-002 |     | 71.8 |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | ---------------------- | --- | ---- |
| andrelevantinformationisreferredtoasquestionrepresenta- |     |     |     |     | 𝑃   |                        |     |      |
|                                                         |     |     |     |     |     | [7] GPT-3.5-TURBO      |     | 70.7 |
tion.Whileinfew-shotscenario,alimitednumberofexamples
|     |     |     |     | AS  | 𝑃 ✓ ✗ | ✗ [47] | -   | -   |
| --- | --- | --- | --- | --- | ----- | ------ | --- | --- |
areavailable,thusbesidesquestionrepresentation,wealsoneed
to study how to select the most helpful examples and organize Table1:Questionrepresentationsinexistingworks,aswellas
theminthepromptappropriately.Innaturallanguageprocessing, theirreportedexecutionaccuracy(EX)inzero-shotscenario.
theaboveprogressthatLLMslearnfromcontextualexamplesis TheInstruction(INS),RuleImplication(RI)andForeignKey
namedasin-contextlearning[12].ItenablesLLMstoidentify (FK)arepossiblecomponentsinaprompt.INSisthetask
description,suchas“WriteaSQLtoanswerthequestion”.
explicitorinexplicitpatternsfromtheinputprompt,andgenerate
RIistheguidingstatement,suchas“CompletesqliteSQL
correspondingoutputs.Inthisway,LLMsarecapableofnewtasks
duringinferencewithoutanyexplicittask-specifictrainingphase. queryonlyandwithnoexplanation”.FKistheforeignkey
Recentstudies[14,28,37]confirmthesignificantroleofincluding informationofthedatabase.
| examplesforeffectivein-contextlearning. |     | Inthispaper,wewill |     |     |     |     |     |     |
| --------------------------------------- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
discussin-contextlearninginthescopeofexampleselectionand
exampleorganization.
|     |     |     |     | 1 Table continents, | columns | = [ContId, Continent] |     |     |
| --- | --- | --- | --- | ------------------- | ------- | --------------------- | --- | --- |
AlthoughLLMsaredemonstratedtobeeffectiveinbothzero- Table countries, columns = [CountryId, CountryName,
2
| shotandfew-shotscenariosinpriorstudies[7,19,26,29,46],their |     |     |     | ↰ Continent] |     |     |     |     |
| ----------------------------------------------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- |
performancescanbefurtherenhancedbysupervisedfine-tuning 3 Q: How many continents are there?
4 A: SELECT
(SFT),whichenhancesLLMsusingadditionaltask-specifictrain-
Listing1:ExampleofBasicPrompt
ingdatatomakeitmoresuitableforspecificdownstreamtasks.
Inrecentresearches,supervisedfine-tuningisusedasatraining
paradigmsofAlignment,whichalignsLLMs’behaviortoavoid
|                                                             |     |     |     | Given the     | following database | schema: |     |     |
| ----------------------------------------------------------- | --- | --- | --- | ------------- | ------------------ | ------- | --- | --- |
| generatingoffensive,biasedresponsesandhallucinations[31].In |     |     |     | 1             |                    |         |     |     |
|                                                             |     |     |     | 2 continents: | ContId, Continent  |         |     |     |
thispaper,wewillfocusonenhancingLLMs’Text-to-SQLcapabili-
|                                |     |                               |     | 3 countries: | CountryId, CountryName, | Continent |     |     |
| ------------------------------ | --- | ----------------------------- | --- | ------------ | ----------------------- | --------- | --- | --- |
| tieswithsupervisedfine-tuning. |     | Itisworthnotingthatdespitethe |     | 4            |                         |           |     |     |
extensiveresearchonpromptengineeringforText-to-SQL,thereis 5 Answer the following: How many continents are there?
SELECT
| ascarcityofstudiesexploringthesupervisedfine-tuningofLLMs |     |     |     | 6   |     |     |     |     |
| --------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
forText-to-SQL[46],leavingthisareaasanopenquestion. Listing2:ExampleofTextRepresentationPrompt
Insummary,questionrepresentation,in-contextlearning,to-
| getherwithsupervised | fine-tuning | arethreeessentialknobsin |     |     |     |     |     |     |
| -------------------- | ----------- | ------------------------ | --- | --- | --- | --- | --- | --- |
thecorrectSQL𝑠∗asfollows:
largelanguagemodelbasedText-to-SQL.Inthispaper,wewill
provideasystematicalstudyanddiscussionaboutthem. max P (𝑠∗|𝜎(𝑞,D)),
M
𝜎
wherefunction𝜎(·,·)decidesrepresentationfortargetquestion𝑞,
withtheusefulinformationfromtheschemaofdatabaseD.Besides,
3 METHODOLOGY
𝜎(·,·)alsocanincludeinformationsuchasinstructionstatement,
Asstatedabove,inthispaperwefocusonquestionrepresentation,
ruleimplicationandforeignkey.
in-contextlearningandsupervisedfine-tuning.Inthissection,we
Followtheabovedefinition,wesurveydifferentchoicesof𝜎in
provideformaldefinitionsforthesethreeproblems,surveytheir
zero-shotscenarioandchoosefourmostrepresentativeonesfrom
existingsolutionssystematically,andpointoutthepotentialissues
literature.Inaddition,wealsoincludethequestionrepresentation
inexistingtechniques.Toaddresstheseissues,weproposeanew usedinAlpaca[47]sinceit’spopularinsupervisedfine-tuning.
Text-to-SQLpromptengineeringmethod,namedDAIL-SQL,which
Table1summarizesthesefiverepresentationmethodsandlists
refreshesthebestperformanceinSpiderleaderboardwith86.6%
theirreporteddetailsfromtheiroriginalpapers.
executionaccuracy.
|     |     |     |     |     | BasicPrompt(BS | ).BasicPrompt[37]isasimplerepre- |     |     |
| --- | --- | --- | --- | --- | -------------- | -------------------------------- | --- | --- |
|     |     |     |     | •   | 𝑃              |                                  |     |     |
sentationshowninListing1.Itisconsistedoftableschemas,
naturallanguagequestionprefixedby“Q:”andaresponse
3.1 QuestionRepresentation
prefix“A:SELECT”topromptLLMtogenerateSQL.Inthis
Inthissection,wefirstdiscussquestionrepresentationsunderzero- paperwenameditasBasicPromptduetoitsabsenceof
shotscenarioforText-to-SQL.Consideringatargetquestion𝑞in instructions.
natural language on certain database D, the target of question TextRepresentationPrompt(TR ).AsshowninList-
|     |     |     |     | •   |     |     | 𝑃   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
representationistomaximizethepossibilityofLLMMgenerating ing 2, Text Representation Prompt [29] represents both

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
### Complete sqlite SQL query only and with no /* Given the following database schema: */
| 1   |             |     |     |     |     | 1        |                   |     |     |     |
| --- | ----------- | --- | --- | --- | --- | -------- | ----------------- | --- | --- | --- |
|     | explanation |     |     |     |     | 2 CREATE | TABLE continents( |     |     |     |
↰
2 ### SQLite SQL tables, with their properties: 3 ContId int primary key,
| 3 # |     |     |     |     |     | 4 Continent | text, |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | --- | --- |
4 # continents(ContId, Continent) 5 foreign key(ContId) references countries(Continent)
| #   | countries(CountryId, | CountryName, |     | Continent) |     | );  |     |     |     |     |
| --- | -------------------- | ------------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
| 5   |                      |              |     |            |     | 6   |     |     |     |     |
| 6 # |                      |              |     |            |     | 7   |     |     |     |     |
7 ### How many continents are there? 8 CREATE TABLE countries(
| 8 SELECT |     |     |     |     |     | 9 CountryId | int primary | key, |     |     |
| -------- | --- | --- | --- | --- | --- | ----------- | ----------- | ---- | --- | --- |
Listing3:ExampleofOpenAIDemostrationPrompt 10 CountryName text,
|     |     |     |     |     |     | Continent | int, |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | ---- | --- | --- | --- |
11
|     |     |     |     |     |     | 12 foreign | key(Continent) | references | continents(ContId) |     |
| --- | --- | --- | --- | --- | --- | ---------- | -------------- | ---------- | ------------------ | --- |
13 );
14
schemaandquestioninnaturallanguage.Comparedwith
|     |                                                   |     |     |     |     | 15 /* Answer | the following: | How many | continents | are there? |
| --- | ------------------------------------------------- | --- | --- | --- | --- | ------------ | -------------- | -------- | ---------- | ---------- |
|     | BasicPrompt,itaddsinstructionattheverybeginningof |     |     |     |     | */           |                |          |            |            |
↰
|     | prompttoguideLLMs.In[29],itachieves69.0%execution |     |     |     |     | 16 SELECT |     |     |     |     |
| --- | ------------------------------------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
accuracyonSpider-devinzero-shotscenario.
Listing4:ExampleofCodeRepresentationPrompt
|     | • OpenAIDemostrationPrompt(OD |                 |     | 𝑃 ).TheOpenAIDe- |             |     |     |     |     |     |
| --- | ----------------------------- | --------------- | --- | ---------------- | ----------- | --- | --- | --- | --- | --- |
|     | mostration                    | Prompt (Listing | 3)  | is first used    | in OpenAI’s |     |     |     |     |     |
officialText-to-SQLdemo[33],andevaluatedin[26,37]. Below is an instruction that describes a task, paired
1
It’sconsistedofinstruction,tableschemas,andquestion, ↰ with an input that provides further context. Write a
whereallinformationarecommentedbypoundsign“#”. ↰ response that appropriately completes the request.
|     | ComparedwithTextRepresentationPrompt,theinstruc- |     |     |     |     | 2   |     |     |     |     |
| --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3 ### Instruction:
tioninOpenAIDemostrationPromptismorespecificwith 4 Write a sql to answer the question "How many continents
|     | arule,“CompletesqliteSQLqueryonlyandwithnoexpla-   |     |     |        |               | ↰ are              | there?"    |     |     |     |
| --- | -------------------------------------------------- | --- | --- | ------ | ------------- | ------------------ | ---------- | --- | --- | --- |
|     | nation”,whichwewillfurtherdiscussintheSec.4.3along |     |     |        |               | 5                  |            |     |     |     |
|     | withexperimentalresults.                           |     |     |        |               | 6 ### Input:       |            |     |     |     |
|     |                                                    |     |     |        |               | continents(ContId, | Continent) |     |     |     |
|     |                                                    |     |     | (CR ). | The Code Rep- | 7                  |            |     |     |     |
• Code Representation Prompt 𝑃 8 countries(CountryId, CountryName, Continent)
|     | resentation                                         | Prompt [7, | 29] presents | Text-to-SQL | task in  | 9                |     |     |     |     |
| --- | --------------------------------------------------- | ---------- | ------------ | ----------- | -------- | ---------------- | --- | --- | --- | --- |
|     | SQLsyntax.Specifically,asshowninListing4,itdirectly |            |              |             |          | 10 ### Response: |     |     |     |     |
|     | presents “CREAT                                     | TABLE”     | SQLs,        | and prompts | LLM with | 11 SELECT        |     |     |     |     |
naturallanguagequestionincomments.Comparedwith Listing5:ExampleofAlpacaSFTPrompt
|     | otherrepresentations,CR |     | standsoutduetoitsabilityto |     |     |     |     |     |     |     |
| --- | ----------------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- |
𝑃
providecomprehensiveinformationnecessaryfordatabase
creation,suchascolumntypesandprimary/foreignkeys. Therefore,inthissubsection,wediscussthekeysofin-context
Withsucharepresentation,[29]correctlypredictsabout learning,thatareexampleselectionandexampleorganization.We
75.6%SQLswithLLMCODE-DAVINCI-002.
firstgiveaformulationofin-contextlearningtoeasethefurther
|     | AlpacaSFTPrompt(AS |     | ).TheAlpacaSFTPromptisa |     |     |              |     |     |     |     |
| --- | ------------------ | --- | ----------------------- | --- | --- | ------------ | --- | --- | --- | --- |
|     | •                  |     | 𝑃                       |     |     | discussions. |     |     |     |     |
promptdesignedforsupervisedfine-tuning[47].Asshown InText-to-SQL,givenasetoftriplesQ = {(𝑞 ,𝑠 ,D𝑖)},where
𝑖 𝑖
inListing5,itpromptsLLMtofollowinstructionandfinish 𝑞 and𝑠 arenaturallanguagequestionanditscorrespondingSQL
𝑖 𝑖
taskaccordingtotheinputcontextinMarkdownformat. queryondatabaseD𝑖 ,thetargetofin-contextlearningforText-
Weincludeittoexamineitseffectivenessandefficiency to-SQListomaximizethepossibilityofLLMM generatingthe
|     | in both prompt | engineering | and | supervised | fine-tuning |     |     |     |     |     |
| --- | -------------- | ----------- | --- | ---------- | ----------- | --- | --- | --- | --- | --- |
correctSQL𝑠∗onthetargetquestion𝑞anddatabaseDasfollows:
scenarios.
|     |                                                         |     |     |     |     |     | max | P (𝑠∗|𝜎(𝑞,D,Q′)), |     |     |
| --- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- |
|     | AsshowninTable1,differentrepresentationsareexperimented |     |     |     |     |     |     | M                 |     |     |
Q′,𝜎
withdifferentLLMs,andintegratedindifferentframeworks,mak- s.t. |Q′|=𝑘 and Q′ ⊂Q,
ingitdifficulttocomparethemfairlyandeffectively.Additionally,
wherefunction𝜎(·,·,·)decidesrepresentationfortargetquestion𝑞,
thespecificrolesplayedbyindividualcomponentssuchasforeign
keyinformationandruleimplicationremainunclear.Consequently, withtheusefulinformationfromtheschemaindatabaseDand𝑘ex-
itisessentialtoconductasystematicalstudytobetterunderstand amplesselectedfromQ.Inthispaper,wefocusoncross-domainText-
to-SQL,whichmeansthetargetdatabaseDisnotincludedamong
questionrepresentations,andinvestigatetheiradvantagesanddis-
|                                   |     |     |     |     |     | thedatabasesD𝑖 | mentionedinQ.,i.e.,D |     | ∉{D𝑖|(𝑞 | ,𝑠 ,D𝑖) ∈Q}. |
| --------------------------------- | --- | --- | --- | --- | --- | -------------- | -------------------- | --- | ------- | ------------ |
| advantagesthroughafaircomparison. |     |     |     |     |     |                |                      |     |         | 𝑖 𝑖          |
In-contextlearningforText-to-SQLinvolvesselectingthemost
helpfulexamplesQ′anddecidinghowtoorganizetheinformation
3.2 In-ContextLearningforText-to-SQL
oftheseselectedexamplesintoprompt.Nextwediscussthesetwo
TheabovequestionrepresentationmethodsenableLLMstodirectly
sub-tasks:exampleselectionandexampleorganization.
outputdesiredSQLsbyzero-shotlearning.However,LLMscan
perform better for Text-to-SQL through in-context learning, in Wesummarizevariousexampleselection
3.2.1 ExampleSelection.
which only a few examples are provided in the input prompts. strategiesinpriorstudiesasfollows.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
• Random.Thisstrategyrandomlysamples𝑘examplesfrom /* Given the following database schema: */
1
| theavailablecandidates.Previousworks[14,28,29]have |     |     | 2 ${DATABASE_SCHEMA} |     |     |     |
| -------------------------------------------------- | --- | --- | -------------------- | --- | --- | --- |
adopteditasabaselineforexampleselection. 3 /* Answer the following: How many authors are there? */
|                                   |     |                       | 4 SELECT count(*) | FROM | authors |     |
| --------------------------------- | --- | --------------------- | ----------------- | ---- | ------- | --- |
| • QuestionSimilaritySelection(QTS |     | 𝑆 ).QTS 𝑆 [28]chooses |                   |      |         |     |
5
𝑘exampleswiththemostsimilarquestions.Specifically,it /* Given the following database schema: */
6
| embedsbothexamplequestionsinQandthetargetques- |     |     | 7 ${DATABASE_SCHEMA} |     |     |     |
| ---------------------------------------------- | --- | --- | -------------------- | --- | --- | --- |
tion𝑞withapre-trainedlanguagemodel.Thenitapplies 8 /* Answer the following: How many farms are there? */
apre-defineddistancemeasure,suchastheEuclideandis- 9 SELECT count(*) FROM farm
| tanceornegativecosinesimilarity,toeachexample-target |     |     | 10  |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- |
${TARGET_QUESTION}
11
pair.Finally𝑘NNalgorithmisleveragedtoselect𝑘exam-
Listing6:ExampleofFull-InformationOrganization.
plesfromQthatcloselymatchthetargetquestion𝑞.
• MaskedQuestionSimilaritySelection(MQS ).Forcross-
𝑆
| domainText-to-SQL,MQS |     | [14]eliminatesthenegative |           |              |                    |            |
| --------------------- | --- | ------------------------- | --------- | ------------ | ------------------ | ---------- |
|                       |     | 𝑆                         | 1 /* Some | SQL examples | are provided based | on similar |
influenceofdomain-specificinformationbyreplacingta-
|     |     |     | ↰ problems: | */  |     |     |
| --- | --- | --- | ----------- | --- | --- | --- |
blenames,columnnames,andvaluesinallquestionswith 2 SELECT count(*) FROM authors
3
amasktoken,andthencomputethesimilaritiesoftheir
|     |     |     | 4 SELECT count(*) | FROM | farm |     |
| --- | --- | --- | ----------------- | ---- | ---- | --- |
embeddingwith𝑘NNalgorithm.
5
| • QuerySimilaritySelection(QRS |     | ).Insteadofusingthe           |                                         |     |     |     |
| ------------------------------ | --- | ----------------------------- | --------------------------------------- | --- | --- | --- |
|                                |     | 𝑆                             | 6 ${TARGET_QUESTION}                    |     |     |     |
| targetquestion𝑞,QRS            |     | [29]aimstoselect𝑘examplesthat |                                         |     |     |     |
|                                |     | 𝑆                             | Listing7:ExampleofSQL-OnlyOrganization. |     |     |     |
aresimilartotargetSQLquery𝑠∗.Specifically,itemploys
apreliminarymodeltogenerateSQLquery𝑠′usingtarget
question𝑞anddatabase𝐷,wherethisgenerated𝑠′canbe 1 /* Some example questions and corresponding SQL queries
regardedasanapproximationof𝑠∗.Thenitencodesqueries ↰ are provided based on similar problems: */
fromexamplesintobinarydiscretesyntaxvectorsaccord- 2 /* Answer the following: How many authors are there? */
|     |     |     | 3 SELECT count(*) | FROM | authors |     |
| --- | --- | --- | ----------------- | ---- | ------- | --- |
ingtotheirkeywords.Afterthat,itchooses𝑘examplesby
4
consideringbothsimilaritytotheapproximatedquery𝑠′ 5 /* Answer the following: How many farms are there?. */
anddiversityamongselectedexamples. 6 SELECT count(*) FROM farm
7
Abovestrategiesfocusonselectingexamplesusingonlytarget
8 ${TARGET_QUESTION}
questionorquery.However,accordingtopriorstudies[12],in- Listing8:ExampleofDAILOrganization.
contextlearningisessentiallylearningfromanalogy.Inthecase
ofText-to-SQL,theobjectiveistogeneratequeriesthatmatchthe
given questions,thus LLMsare supposedto learnthe mapping withlimitedtokenlength.However,itremovesthemap-
fromquestionstoSQLqueries.Therefore,wepointoutthatduring ping information between questions and corresponding
exampleselection,takingbothquestionandSQLqueriesintocon-
SQLqueries,andsuchinformationcanbeuseful,whichwe
siderationmaybenefitText-to-SQLtask.Wewillfurtherdiscussit willdemonstratelater.
inSec.3.3. In summary, FI includes the full information of examples,
𝑂
|                            |     |                              | whichensuresthequality;whileSO |     | 𝑂 onlykeepsSQLqueriesto |     |
| -------------------------- | --- | ---------------------------- | ------------------------------ | --- | ----------------------- | --- |
| 3.2.2 ExampleOrganization. |     | Theexampleorganizationplaysa |                                |     |                         |     |
accommodatemoreexamples,whichprefersthequantity.Wewon-
pivotalroleindeterminingwhatinformationoftheaboveselected
derifthereexistsabettertrade-offbetweenqualityandquantityin
exampleswillbeorganizedintotheprompt.Wesummarizeexist-
exampleorganization,whichcanfurtherbenefittheText-to-SQL
| ingstrategiesinpriorstudiesintotwocategories,Full-Information |     |     | task. |     |     |     |
| ------------------------------------------------------------- | --- | --- | ----- | --- | --- | --- |
OrganizationandSQL-OnlyOrganization,asdemonstratedinList-
| ing 6 and Listing | 7. In these | examples, ${DATABASE_SCHEMA} |     |     |     |     |
| ----------------- | ----------- | ---------------------------- | --- | --- | --- | --- |
3.3 DAIL-SQL
representsthedatabaseschema,and${TARGET_QUESTION}stands
|     |     |     | To address | the aforementioned | issues in | example selection and |
| --- | --- | --- | ---------- | ------------------ | --------- | --------------------- |
forthequestionrepresentationinListing4.
organization,inthissubsection,wepresentanovelText-to-SQL
• Full-InformationOrganization(FI 𝑂 ).FI 𝑂 [7,29]orga- methodnamedDAIL-SQL.PleaserefertoAppendixA.1forthe
| nizesexamplesinthesamerepresentationwiththetarget |     |     | pseudocodeofDAIL-SQL. |     |     |     |
| ------------------------------------------------- | --- | --- | --------------------- | --- | --- | --- |
question.AsshowninListing6,examplesarestructured Forexampleselection,inspiredbyMQS andQRS ,wepro-
𝑆 𝑆
identicallytothetargetquestion,andtheonlydifference posedDAILSelection(DAIL ),consideringbothquestionsand
𝑆
isthatinsteadofthe“SELECT”tokenattheend,these- queriestoselectcandidates.Specifically,DAILSelectionfirstmasks
lectedexampleshavethecorrespondingSQLqueriesafter domain-specificwordsinbothtargetquestion𝑞andexampleques-
“SELECT”. tions𝑞 inthecandidatesetQ.Itthenranksthecandidateexamples
𝑖
• SQL-OnlyOrganization(SO ).SO [14]includesonly basedontheEuclideandistancebetweentheembeddingsofmasked
𝑂 𝑂
SQLqueriesoftheselectedexampleswithaprefixinstruc- 𝑞and𝑞 .Simultaneously,itcalculatesthequerysimilaritybetween
𝑖
tionintheprompt,asdemonstratedinListing7.Suchor- thepre-predictedSQLquery𝑠′and𝑠 inQ.Finally,theselection
𝑖
ganizationaimsatmaximizingthenumberofexamples criterionprioritizesthesortedcandidatesbyquestionsimilarity

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
withaquerysimilaritygreaterthanapredefinedthreshold𝜏.In supervisedfine-tuningforText-to-SQLcoverstwosub-tasks,in-
thisway,theselectedtop𝑘 exampleshavegoodsimilaritywith cludingfine-tuningthegivenLLMM usingsuperviseddata T
bothquestionandquery. inordertogettheoptimalLLMM∗,andsearchingfortheopti-
Topreservethemappinginformationbetweenquestionsand malquestionrepresentation𝜎.Sincequestionrepresentationshave
SQLqueriesandalsoimprovethetokenefficiency,weproposea beendiscussedinSec.3.1,thissectionwillprimarilyfocusondata
newexampleorganizationstrategyDAILOrganization(DAIL
𝑂
) preparationT andfine-tuning.
totrade-offintermsofqualityandquantity.Specifically,DAIL 𝑂 Forgeneraldomain,eachiteminsuperviseddataT ={(𝑝 𝑖 ,𝑟 𝑖)}
presentsbothquestions𝑞 andcorrespondingSQLqueries𝑠 ,as containsaninputprompt𝑝 andanexpectedrespond𝑟 fromLLM.
𝑖 𝑖 𝑖 𝑖
illustratedinListing8.AsacompromisebetweenFI andSO , Toensureconsistencywiththeinferenceprocess,weemploya
𝑂 𝑂
DAIL reservesthequestion-SQLmapping,andreducesthetoken supervisedfine-tuningandgenerateprompt-responsepairsfroma
𝑂
lengthofexamplesbyremovingtoken-costdatabaseschema. givenText-to-SQLdataset.Specifically,givenaText-to-SQLdata
InDAIL-SQL,weadoptCR
𝑃
asourquestionrepresentation.The setT ={(𝑞
𝑖
,𝑠
𝑖
,D𝑖)},wefine-tunetheLLMsusingthegenerated
reasonisthatcomparedwithotherrepresentations,CR contains tuningdatabyusingtargetquestionandthegivendatabaseas
𝑃
fullinformationofthedatabase,includingprimaryandforeign prompt,andtreatingthedesiredqueryasresponsefromLLM,i.e.,
keys,whichmayoffersmoreusefulinformationforLLMs,such T ={(𝑝 𝑖 =𝜎(𝑞 𝑖 ,D𝑖),𝑟 𝑖 =𝑠 𝑖)}.Oncethedataisready,wecanuse
asforeignkeysforthepredictionof“JOIN”clauses.Besides,pre- existingpackagetofine-tunethegivenLLMMthrougheitherfull
trainedonextensivecodingcorpora,LLMscouldbetterunderstand fine-tuning[34]orparameter-efficientfine-tuning[16]depending
thepromptinCR withouttoomuchadditionaleffort. ontheavailablecomputationalresources.Afterfine-tuning,the
𝑃
Insummary,DAIL-SQLutilizesCR
𝑃
asthequestionrepresen- optimizedLLMM∗canbeusedtodoinference,thatisaskingit
tation,selectsexamplesbasedoninformationfrombothquestion togeneratequeriesthroughnaturallanguagequestions.Notethat
andquery,andorganizesthemtokeepquestion-to-SQLmappings. weutilizethesamequestionrepresentation𝜎inbothfine-tuning
Insuchpromptdesign,LLMscouldworkbetterforText-to-SQL andinferenceprocesses.Wewillconductaseriesofexperiments
task,andinSpiderleaderboard,theproposedDAIL-SQLrefresh anddiscussthegreatpotentialofsupervisedfine-tuningforText-
theperformancewith86.2%executionaccuracy. to-SQL.
NoteDAIL-SQLisaflexibleLLM-basedText-to-SQLsolution,
whichcanbefurtherextendedandintegratedwithothercompo-
nentseasily.Forexample,toimprovetheperformance,weequip 4 EXPERIMENT
DAIL-SQL with self-consistency [53], which achieves a perfor- Inthissection,wefirstintroduceourexperimentalsettings.Then
manceof86.6%executionaccuracy.Althoughself-consistencyim- weconductextensivecomparisonswithexistingsolutionsinques-
provestheexecutionaccuracyby0.4%,itisverytimeconsuming tionrepresentation,in-contextlearningandsupervisedfine-tuning
andyieldsmanytimesthecostoforiginalDAIL-SQL.Therefore,in respectively.Afterthat,wefurthercomparethemintermsoftoken
thispaperwestillfocusonDAIL-SQL. efficiencytoinspiremoreefficientsolutions.
3.4 SupervisedFine-TuningforText-to-SQL
4.1 Setting
ToenhancetheperformanceofLLMsinzero-shotscenario,the
Dataset. We evaluate Text-to-SQL methods on two well recog-
popularoptionforexistingText-to-SQLmethodsisin-contextlearn-
nizeddatasets,Spider[57]andSpider-Realistic[10].Spiderisa
ing,whichisdiscussedinabovesubsections.Asanalternativeyet
large-scalecross-domainText-to-SQLdataset,whichcontains8659
promisingoption,supervisedfine-tuningislessexploredsofar.
instancesintrainingsplitand1034instancesindevelopmentsplit
Similartosupervisedfine-tuningforvariouslanguagetask,we
over200databases.Eachinstanceisconsistedofanaturallanguage
canadoptittothefieldofText-to-SQL,andimproveLLMs’per-
questiononaspecificdatabaseanditscorrespondingSQLquery.In
formanceonthis downstreamtask. Tofurther understandhow
thispaper,weusethedevelopmentsplitSpider-devforthepurpose
supervisedfine-tuningworksforText-to-SQL,wefirstprovidea
ofevaluationasthetestsplitisnotreleased.Spider-Realistic[10]
briefformulationasfollows.
isamorechallengingvariantofSpider.Itselectsasubsetof508
ForText-to-SQL,givenalargelanguagemodelM,asetofText-
examplesfromSpider-devandmanuallyrevisesthequestionswhile
to-SQLtrainingdata T = {(𝑞 𝑖 ,𝑠 𝑖 ,D𝑖)},where𝑞 𝑖 and𝑠 𝑖 arethe keepingtheSQLqueriesunchanged.Forfew-shotscenarios,we
naturallanguagequestionanditscorrespondingqueryondata-
utilizethetrainingsplitofSpiderastheexamplecandidateswhen
baseD𝑖 ,theobjectiveofsupervisedfine-tuningistominimizethe
testingwithbothSpider-devandSpider-Realistic.
followingempiricalloss:
Metric.Tomakeafaircomparison,wefollowpriorstudy[61]
touseexact-set-matchaccuracy(EM)andexecutionaccuracy(EX).
|T|
∑︁ The exact-set-match accuracy measures the matched SQL key-
𝜎
m
,M
in
∗
𝑖=1
L M∗(𝜎(𝑞 𝑖 ,D𝑖),𝑠 𝑖),
words between the predicted SQL query and its corresponding
ground truth. The execution accuracy, on the other hand, com-
whereL isthelossfunctiontomeasurethedifferencebetween parestheexecutionoutputofthepredictedSQLquerywiththat
thegeneratedqueryandthegroundtruhquery.Similartoques- ofthegroundtruthSQLqueryonsomedatabaseinstances.This
tionrepresentation,𝜎decidesquestionrepresentationwithuseful metric provides a more precise estimate of the model’s perfor-
information from the schema in database D. In this definition, mancesincetheremaybemultiplevalidSQLqueriesforasingle

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
)%( .ccA hctam-tes-tcaxE 80
Basic Prompt (BSP) Code Representation Prompt (CRP) 100 Basic Prompt (BSP) Code Representation Prompt (CRP)
|                                  |                         |     | )%( .ccA noitucexE Text Representation Prompt (TRP) |     | Alpaca SFT Prompt (ASP) |     |
| -------------------------------- | ----------------------- | --- | --------------------------------------------------- | --- | ----------------------- | --- |
| Text Representation Prompt (TRP) | Alpaca SFT Prompt (ASP) |     |                                                     |     |                         |     |
| 60                               |                         |     | OpenAI Demostration Prompt (ODP)                    |     | Average                 |     |
| OpenAI Demostration Prompt (ODP) | Average                 |     | 80                                                  |     |                         |     |
| 40                               |                         |     | 60                                                  |     |                         |     |
| 20                               |                         |     | 40                                                  |     |                         |     |
| 0                                |                         |     | 20                                                  |     |                         |     |
GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B
Figure1:ResultsofdifferentquestionrepresentationsonSpider-devunderzero-shotscenario.
)%( .ccA hctam-tes-tcaxE
| 60  | BS  w/ FK   | OD  w/ FK   |                    |     | BS  w/ FK   | OD  w/ FK   |
| --- | ----------- | ----------- | ------------------ | --- | ----------- | ----------- |
|     | P           | P           | )%( .ccA noitucexE |     | P           | P           |
|     | TR P  w/ FK | AS P  w/ FK | 80                 |     | TR P  w/ FK | AS P  w/ FK |
40
60
20
40
0
GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B
Figure2:AblationstudiesofforeignkeysinformationonSpider-dev.Thegreenarrowindicatesanincrease,andredarrow
indicatesadecrease.
)%( .ccA hctam-tes-tcaxE TR  w/ Rule CR  w/ Rule TR  w/ Rule CR  w/ Rule
| 60  | P   | P   |     |     | P   | P   |
| --- | --- | --- | --- | --- | --- | --- |
OD  w/ Rule AS  w/ Rule )%( .ccA noitucexE OD  w/ Rule AS  w/ Rule
|     | P   | P   | 80  |     | P   | P   |
| --- | --- | --- | --- | --- | --- | --- |
40
60
20
40
GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B
Figure3:Ablationstudiesof“withnoexplanation”ruleimplicationonSpider-dev.Thegreenarrowindicatesanincrease,and
redarrowindicatesadecrease.
given question. We use the existing released evaluation scripts Vicuna-33B,necessitatingasuitableLLMtoworkwellwith.Unex-
athttps://github.com/taoyds/test-suite-sql-eval. pectedly,GPT-4exhibitsapreferenceforthesimpleBS 𝑃 derived
LLM.Toensureafaircomparison,forallthemethods,weusethe fromDin-SQL[37],indicatingthatapowerfulLLMcanmitigate
samemaximalcontextlength,thatis4096forOpenAILLMand2048 thecomplexitiesassociatedwithrepresentationdesign.Besides,
foropen-sourceLLM.Duringevaluation,weleave200tokensfor bycomparingtheaverageperformanceforfourLLMs,GPT-4and
responsegeneration.Bydefault,wesettheargumenttemperature GPT-3.5-TURBOaremorecapableinthezero-shotscenario.Dueto
as 0 to eliminate the influence of randomness. Regarding post- theexpensivecostofGPT-4,GPT-3.5-TURBOtogetherwithOD
𝑃
processing,wefollowexistingworktoextractthefirstSQLquery maybe a better choice for the zero-shot scenario. For less pow-
inresponseandremoveadditionaloutput.Formoreimplementation erfulLLMslikeTEXT-DAVINCI-003andVicuna-33B,OD and
𝑃
details,pleaserefertoAppendixA.2. CR arepreferred.Fordetailednumericalresults,pleasereferto
𝑃
AppendixB.1.
|     |     |     | To further investigate | the different | question | representations, |
| --- | --- | --- | ---------------------- | ------------- | -------- | ---------------- |
4.2 QuestionRepresentations
Inthissubsection,weevaluatethequestionrepresentationspre- weconductablationstudytoexploretheeffectsoftheirinvidual
components.
sentedinSec.3.1underzero-shotscenario,employingfourLLMs:
ForeignKey(FK).ForeignKeyimpliestherelationamongdif-
GPT-4,GPT-3.5-TURBO,TEXT-DAVINCI-003,andVicuna-33B.
ferentrelationaltables,whichmightbehelpfulinText-to-SQLtask.
Fig.1presentsthecomparisonofdifferentquestionrepresen-
|                                                            |     |     | Inourevaluation,onlyCR | containsforeignkeyinformation.To |     |     |
| ---------------------------------------------------------- | --- | --- | ---------------------- | -------------------------------- | --- | --- |
| tationsoverSpider-dev.Bycomparingdifferentrepresentations, |     |     |                        | 𝑃                                |     |     |
wecanobservethatOD fitstoallfourLLMsandachieves75.5% examineitseffect,weaddforeignkeyinformationintootherrep-
𝑃
executionaccuracywithGPT-3.5-TURBO.Incontrast,AS exhibits resentationsandevaluatetheminFig.2.ForOpenAILLMs,we
𝑃
poorperformancewithGPT-3.5-TURBO,TEXT-DAVINCI-003,and

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
Question Query GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 Vicuna-33B
Few-shot Selection
Similarity Similarity
EM EX EM EX EM EX EM EX
0-shot - - - 22.1 72.3 34.6 74.4 31.7 71.7 6.9 43.7
Random 0.23 0.47 41.7 77.4 45.9 73.9 38.2 70.6 14.4 47.9
QuestionSimilarityselection 0.39 0.65 53.3 78.8 51.9 74.3 44.1 72.3 16.5 48.5
1-shot MaskedQuestionSimilarityselection 0.57 0.80 58.2 79.1 57.4 76.0 47.9 75.0 21.4 48.7
DAILselection 0.56 0.95 62.1 80.2 59.5 75.5 51.9 76.9 22.8 49.2
UpperLimit 0.56 0.98 63.7 81.0 61.4 77.2 53.1 77.5 22.7 49.4
Random 0.23 0.48 48.9 79.4 49.0 73.6 41.7 71.6 16.8 46.9
QuestionSimilarityselection 0.37 0.63 56.3 79.2 53.8 74.7 52.2 74.1 21.1 47.1
3-shot MaskedQuestionSimilarityselection 0.54 0.78 66.1 81.5 61.1 77.3 59.7 77.0 27.7 52.3
DAILselection 0.53 0.94 69.1 81.7 63.9 77.8 64.4 79.5 30.7 53.6
UpperLimit 0.53 0.98 71.5 83.4 66.2 79.2 66.7 81.1 31.2 54.4
Random 0.23 0.48 51.6 79.5 52.9 75.7 49.0 72.1 - -
QuestionSimilarityselection 0.36 0.61 58.2 79.9 55.9 75.1 54.8 73.2 - -
5-shot MaskedQuestionSimilarityselection 0.52 0.77 66.8 82.0 62.3 77.9 64.7 78.6 - -
DAILselection 0.52 0.94 71.9 82.4 66.7 78.1 67.7 80.5 - -
UpperLimit 0.51 0.97 74.4 84.4 68.8 79.6 70.7 82.4 - -
Table2:EvaluationonSpider-devwithdifferentexampleselections.TheorganizationisfixedtoFull-InformationOrganization.
observethatforeignkeysignificantlyimprovestheexecutionac- 4.3 In-ContextLearningforText-to-SQL
curacyofLLMsby0.6%−2.9%,exceptthecombinationsofTR 𝑃 Infew-shotscenario,weexaminedifferentexampleselectionandor-
withGPT-4(−0.2%)andAS 𝑃 withTEXT-DAVINCI-003(−0.4%). ganizationstrategieswithGPT-4,GPT-3.5-TURBO,TEXT-DAVINCI-
However,theimpactofforeignkeyforVicuna-33Btendstobe 003,andVicuna-33B.Toensureafaircomparison,weadoptCR
𝑃
unstable.Notably,theinclusionofforeignkeysleadstoasurpris- asthequestionrepresentationforalltheexperimentsinthissub-
ingimprovementof5.0%fortheBS 𝑃 ,butadverselyaffectsthe section,duetoitssuperiorperformanceinone-shotpreliminary
performanceoftheOD 𝑃 andAS 𝑃 . experimentinAppendixC.1.
RuleImplication(RI).InspiredbytheoutperformanceofOD
𝑃
,
weexploretheeffectofruleimplication.Specifically,OD implicate
𝑃
LLMstogenerateSQLqueries“withnoexplanation”Toexamine
theeffectof“withnoexplanation”ruleinquestionrepresentation, 4.3.1 ExampleSelection. Toverifytheimportanceofbothques-
we present an ablation study in Fig. 3. Specifically, we plot the tionandqueryforexampleselection,wecalculatequestion’sand
performanceofdifferentrepresentationsafterincludingthe“with query’sJaccardsimilaritiesbetweenchosenexamplesandthetarget
noexplanation"implicationandthechangeofaccuracy.FromFig.3 instance,andreporttheaveragednumbersundercolumnquestion
weobserveaddingthisruleconsistentlyboomstheperformanceof similarityandquerysimilarityinTable2.Specifically,weremove
allLLMsinbothexact-set-matchandexecutionaccuracy,withthe database-specificinformationfromquestions[51]andqueries[22],
mostsignificantimprovementsexceeding6%and3%,respectively. andcalculatetheJaccardsimilaritisoftheremainedtokens.Be-
WhileforOD 𝑃 ,removingthisruleincursabout2.4%−6.2%drop sides,weintroduceUpperLimitforreference,whichissimilar
inexact-set-matchaccuracy,and1.3%−2.4%dropinexecution withDAILSelectionbututilizesthegroundtruthquery𝑠∗rather
accuracy,indicatingtheimportanceofthisruleimplication.Asa thanthequerygeneratedbypreliminarypredictor.Notably,wedo
comparison,wealsotestapopularruleimplication“Let’sthink notdirectlyprovidethegroundtruthSQLtotheLLMs,butjustuse
stepbystep”[20],whichguidesLLMtogenerateresponsewith thegroundtruthqueryasareferenceforselectingexamples.To
analysis.However,itsperformanceishighlyvolatileinText-to-SQL someextent,UpperLimitindicatestheupperboundofperformance
taskasAppendixB.4shows.Duetolimitedresources,weleavethe forsimilaritybasedselectionmethods.
explorationofotherpossibleruleimplicationsasanopenquestion Table2showsthecomparisonsofdifferentexampleselection
forfutureresearch. strategiesin1-,3-and5-shotscenariosonSpider-dev.Bycompar-
In summary, both the foreign key and the “with no explana- ingdifferentselectionstrategies,itisdemonstratedthatDAIL
𝑆
tion”implicationrulearebeneficialforText-to-SQLtask.Inour generallyoutperformsotherstrategies.In5-shotscenario,equipped
evaluation,OD 𝑃 withforeignkeysandGPT-3.5-TURBOarethe withGPT-4,DAIL-SQLachieves82.4%executionaccuracy.Besides,
mosteffectiveandeconomiccombination,whichachieves51.5% inTable2weobservetheincreasingquestionandquerysimilarity
exact-set-matchaccuracyand78.4%executionaccuracy. correspondstohigherexecutionaccuracymostly,indicatingthe
importanceofconsideringbothquestionandquerysimilarity.Note
DAIL ’sexecutionaccuracyisstilllowerthanUpperLimit.This
𝑆
discrepancycanbeattributedtothelowerquerysimilarity,indicat-
ingthegapbetweenthegroundtruthqueryandthatgeneratedby
thepreliminarymodel.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
| 84  |     | 79  |     |     |     | 54  |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
80
82
)%( .ccA noitucexE )%( .ccA noitucexE 78 )%( .ccA noitucexE )%( .ccA noitucexE 52
78
80
50
| 78  |     | 77  |     | 76  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
48
76 Full-Information 76 Full-Information 74 Full-Information Full-Information
46
|     | SQL-Only |     | SQL-Only |     | SQL-Only |     | SQL-Only |
| --- | -------- | --- | -------- | --- | -------- | --- | -------- |
| 74  |          | 75  |          | 72  |          |     |          |
|     | DAIL     |     | DAIL     |     | DAIL     | 44  | DAIL     |
| 72  |          |     |          | 70  |          |     |          |
| 0 2 | 4 6 8    | 0 2 | 4 6 8    | 0 2 | 4 6 8    | 0 2 | 4 6 8    |
|     | k-shot   |     | k-shot   |     | k-shot   |     | k-shot   |
(a)GPT-4onSpider-dev (b)GPT-3.5-TURBOonSpider-dev (c)TEXT-DAVINCI-003onSpider-dev (d)Vicuna-33BonSpider-dev
| 76  |     | 72  |     |     |     | 46  |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
70
|     |     | 71  |     |     |     | 44  |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
)%( .ccA noitucexE )%( .ccA noitucexE )%( .ccA noitucexE )%( .ccA noitucexE
| 74  |     |     |     | 68  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 70  |     |     |     | 42  |     |
66
| 72  |     | 69  |     |     |     | 40  |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 68  |     | 64  |     |     |     |
70 Full-Information Full-Information Full-Information 38 Full-Information
67
|     | SQL-Only |        | SQL-Only | 62  | SQL-Only | 36  | SQL-Only |
| --- | -------- | ------ | -------- | --- | -------- | --- | -------- |
| 68  |          | 66     |          |     |          |     |          |
|     | DAIL     |        | DAIL     | 60  | DAIL     | 34  | DAIL     |
| 0 2 | 4 6 8    | 65 0 2 | 4 6 8    | 0 2 | 4 6 8    | 0 2 | 4 6 8    |
|     | k-shot   |        | k-shot   |     | k-shot   |     | k-shot   |
(e)GPT-4onSpider-Realistic (f)GPT-3.5-TURBOonSpider-Realistic (g)TEXT-DAVINCI-003onSpider-Realistic (h)Vicuna-33BonSpider-Realistic
Figure4:EvaluationonSpider-devwithdifferentexampleorganizations.TheselectionisfixedtoDAILSelection.
4.3.2 ExampleOrganization. Tocomparedifferentexampleorgani- Insummary,forexampleselection,ourfindingsemphasizethe
zationstrategies,weevaluateFull-InformationOrganization,SQL- importanceofthemappingfromquestiontoSQLquery.Consid-
OnlyOrganizationandDAILOrganizationinfew-shotscenarioon eringbothquestionandquerysimilaritiessimultaneously,DAIL
𝑆
bothSpider-devandSpider-Realistic.Fig.4showsthecomparison outperformsotherselectionstrategiesinourevaluation.Forexam-
results,andrefertoAppendixC.2fordetailednumericalresults. pleorganization,weshowtheeffectivenessofDAIL 𝑂 ,andpoint
FromFig.4(a)andFig.4(e),wecanobservethatGPT-4benefits outitsdemandsforpotentLLMs.Finally,inourevaluation,weob-
fromcontextualexamplessteadilyonbothSpider-devandSpider- servethatourapproach,DAIL-SQL,equippedwithGPT-4,achieves
Realistic.WithDAILOrganization,itsexecutionaccuracyincreases thehighestperformancewithanexecutionaccuracyof83.5%on
from72.3%to83.5%onSpider-devandfrom66.5%to76.0%on Spider-devand76.0%onSpider-Realistic.Formorecomparisons
Spider-Realistic.WhileforGPT-3.5-TURBOandTEXT-DAVINCI- withpreviousmethods,pleaserefertoAppendixC.3.
003,addingexamplesmayincurdropinexecutionaccuracydue
tolimitedin-contextlearningcapability.RegardingVicuna-33B,
4.4 SupervisedFine-TuningforText-to-SQL
itsperformanceconsistentlyimprovesasthenumberofexamples
increasesinDAILOrganization.Bycomparingdifferentorganiza- Inthissection,weinvestigatesupervisedfine-tuninginText-to-SQL.
tionstrategies,weobservethatGPT-4showspreferenceforDAIL Duetotheunaffordablecostoffine-tuningOpenAILLMs,wefocus
onopen-sourceLLMs.Giventhefactthatveryfewexistingwork
OrganizationinbothSpider-devandSpider-Realistic,suggesting
adoptopen-sourceLLMsandtheirperformanceremainunknown,
itcaneffectivelylearnthemappingfromquestion-SQLpairs.For
wefirstundertakeathoroughevaluationforopen-sourceLLMs,
GPT-3.5-TURBO(Fig.4(b)andFig.4(f)),comparedwithitszero-shot
performanceinFig.1,itsenhancementinin-contextlearningisthe employingvariousquestionrepresentation,exampleselectionand
smallestamongfourLLMs,duetoitsweaknessinin-contextlearn- organizationstrategies.Afterthat,wefine-tuneopen-sourceLLMs
inText-to-SQLandobservetheirenhancementinbothzero-shot
ing.ForTEXT-DAVINCI-003,Full-InformationOrganizationisfar
andfew-shotscenarios.
beyondtheothertwostrategies,especiallywithincreasingexample
number,asdepictedinFig.4(c)andFig.4(g).Figures4(d)and4(h)
illustratethatinthecaseofVicuna-33B,DAILOrganizationoutper- 4.4.1 Open-sourceLLM. Toinvestigatethepotentialofopen-source
formsSQL-OnlyOrganizationbutfallsshortoftheperformance LLM,wechooseLLaMA[48],anditsalignedvariantsinvarying
scales.Theyaredetailedasfollows.Notethealignedvariantsmeans
achievedbyFull-InformationOrganization.Bycomparingdifferent
theLLMisalignedtobemorehelpful,harmlessandhonest[2],and
LLMs,weinferthatforLLMwithgreaterin-contextlearningcapa-
thesuffix"-7B"meanstheLLMhas7billionsparameters,thesame
bility,likeGPT-4,benefitsfromDAILOrganizationthemost,while
theweakerLLMsrequiremoreinformationtolearnfromexamples. meaningfor"-13B"and"-33B".
However,weemphasizeDAILOrganizationcanbeagoodchoice
LLaMA-7B/13B/33B[48]isacollectionofwidelyrecog-
•
toachievehigherperformance,andthebestexecutionaccuracyin nizedopen-sourceLLMs,whicharepre-trainedonmassive
ourevaluationisachievedbyDAILOrganizationwithGPT-4.
corpusbyMeta.

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
BS TR OD CR AS Average
LLM 𝑃 𝑃 𝑃 𝑃 𝑃
EM EX EM EX EM EX EM EX EM EX EM EX
LLaMA-7B 6.5 9.6 3.1 4.9 3.6 9.0 4.8 16.3 1.3 5.9 3.9 9.1
Pre-trained LLaMA-13B 8.8 18.4 4.5 15.2 8.2 21.8 5.6 25.0 8.9 26.9 7.2 21.5
LLaMA-33B 9.6 26.7 12.0 25.9 13.6 36.4 12.2 42.8 13.8 38.1 12.2 34.0
Falcon-40B 0.3 11.7 0.2 0.9 0.3 7.6 0.1 21.9 0.0 5.0 0.2 9.4
Alpaca-7B 15.1 25.1 13.5 23.8 14.7 25.7 16.0 32.1 8.9 19.9 13.6 25.3
GPT4ALL-7B 7.8 19.4 8.8 24.6 8.1 27.0 8.5 25.9 6.5 21.8 7.9 23.7
Vicuna-7B 7.5 15.6 1.2 9.9 6.2 21.5 5.6 24.0 0.9 5.4 4.3 15.3
Vicuna-13B 8.2 21.7 10.1 24.4 11.2 31.4 5.8 33.5 4.7 20.0 8.0 26.2
Aligned Vicuna-33B 10.8 28.9 18.3 37.1 19.1 42.7 6.9 43.7 8.6 30.6 12.7 36.6
LLaMA-2-CHAT-7B 14.3 23.4 7.2 15.5 6.3 12.3 12.2 25.5 5.0 20.5 9.0 19.4
LLaMA-2-CHAT-13B 18.8 32.6 15.4 30.5 11.1 22.3 20.7 40.0 16.9 36.2 16.6 32.3
LLaMA-2-CHAT-70B 21.8 46.2 11.9 33.9 21.4 45.5 12.4 44.0 8.4 28.6 15.2 39.6
CodeLLaMA-34B 27.8 65.5 15.9 40.3 25.8 65.3 24.3 68.5 22.4 61.5 23.2 60.2
Table3:Zero-shotevaluationresultsonSpider-devwithdifferentopen-sourceLLMs.Thebestperformancesofpre-trainedand
alignedLLMareinbold.
• Falcon-40B[35]ispre-trainedsolelyonmassivecorpus 34.0%onSpider-dev,andVicunashowsasimilarupwardtrendfrom
ofrefinedwebdata. 15.3%to36.6%.Withthemostparametersize,LLaMA-2-CHAT-70B
• Alpaca-7B[47]isanalignedversionofLLaMA-7B,which improvestheaverageperformanceto39.6%.Inthemorechallenging
isfine-tunedwith52kinstruction-followingdatagenerated dataset Spider-Realistic, the same pattern can be observed and
byTEXT-DAVINCI-003. executionaccuracyofLLaMAandVicunarisefrom7.56%to25.4%
• GPT4ALL-7B[1]isanotheralignedversionofLLaMA-7B and12.3%to30.0%.
withabout800kdatadesignedforhelpful,harmlessand EffectofAlignment.FromtheresultsweobservethatLLM
honestAIassistant. alignment can benefit Text-to-SQL. Specifically, with the same
• LLaMA-2-CHAT-7B/13B/70B[49]areup-to-dateversion modelscale,VicunaoutperformsLLaMAbyabout5%inexecution
ofLLaMA.Theyarebothpre-trainedandaligned,andout- accuracyonbothSpider-devandSpider-Realistic.ForFalcon-40B,it
performthepreviousversiononmostbenchmarks. performspoorlywithallrepresentations,attributabletotheabsence
• Vicuna-7/13/33B[8,59]isacollectionofopen-sourcechat- ofdedicatedcodedatainitstrainingdataset.Asacomparison,with
botalignedfromLLaMAwithuser-sharedconversations. carefullycollectedcodedatainthealignmentstage,CodeLLaMA-
Vicuna-13B[8]isdeclaredtoperformsimilartoOpenAI 34BexhibitsasignificantimprovementinText-to-SQLtaskwith
ChatGPTandGoogleBard,andoutperformsLLaMAand similarmodelscale.Notethat,CodeLLaMA-34Balsooutperforms
Alpacainmostscenarios. LLaMA-2-CHAT-70Bbyanaverageof20.6%despitehavingonly
• CodeLLaMA-34B[42]isanalignedversionofLLaMA-2- half the parameter of LLaMA-2-CHAT-70B. This highlights the
34B,whichisfine-tunedwith500Btokensofcodedata. crucialimportanceofthetrainingcorpusinLLMs.
Inconclusion,havingmoreparametersinLLMsmayholdcer-
4.4.2 Zero-shotScenariowithOpen-sourceLLM. Table3shows
tainpotentialbenefitstoText-to-SQL,butthetrainingcorpus(e.g.,
theirzero-shotperformancesonSpider-devwithdifferentquestion
havingtask-specifictrainingdata)playsamorecrucialrole.
representations.Duetolimitedspace,pleaserefertoAppendixD.1
fortheperformanceonSpider-Realistic.Next,weprovideseveral
analysisfromaspectsofquestionrepresentations,modelscaleand
alignmentasfollows. 4.4.3 Few-shotScenariowithOpen-sourceLLM. Forfew-shotsce-
EffectofQuestionRepresentation.Wecanobservethatthe nario,Fig.5showstheperformanceofLLaMA-33BandVicuna-33B
bestperformancesisachievedbyCR with68.5%executionac- with CR . We use DAIL Selection to select example as it is re-
𝑃 𝑃
curacy on Spider-dev. The possible reason is that full database portedasthebeststrategyinSec.4.3.Formoredetails,referto
knowledgeinCR (CodeRepresentationPrompt)compensates AppendixD.2.FromthisFigure,wecanseethatLLaMA-33Bben-
𝑃
theincapabilityofopen-sourceLLMs.Onepossiblereasonisthat efitsmorethanVicuna-33B,andachieves36.4%exact-set-match
CR tendstostimulatethecodingcapabilityofLLMs.Thiseffectis accuracywith5-shotFull-InformationOrganizationexamples.Re-
𝑃
particularlyevidentinCodeLLaMA-34B,whichonlyachieve40.3% gardingexecutionmatchaccuracy,increasingnumberofexamples
executionaccuracywithnaturallanguage-basedTR . benefitsText-to-SQLinmostcases.Besides,amongdifferentor-
𝑃
EffectofModelScale.Fromtheresultsweobserveapositive ganizationstrategies,Full-InformationOrganizationoutperforms
correlationbetweenmodelscaleandperformanceonText-to-SQL otherstrategiesindifferentk-shotscenarios,whichachieves51.5%
forbothLLaMAandVicuna.Specifically,theaverageexecution executionaccuracywithVicuna-33B.PleaserefertoAppendixD.3
matchaccuracyofLLaMAshowsanotableprogressionfrom9.1%to formoreanalysisinfew-shotscenario.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
|                          |     |     |     |     |     |     |     |      | 0-shot   | 1-shot 3-shot | 5-shot |
| ------------------------ | --- | --- | --- | --- | --- | --- | --- | ---- | -------- | ------------- | ------ |
| 35                       |     |     |     |     |     |     | LLM | Org. |          |               |        |
| )%( .ccA hctam-tes-tcaxE |     | 50  |     |     |     |     |     |      |          |               |        |
| 30                       |     |     |     |     |     |     |     |      | EM EX EM | EX EM EX      | EM EX  |
)%( .ccA noitucexE
|     |     |     |     |     |     |     |       | FI   | 3.1 13.0 23.4 | 30.1 23.7 30.3 | 24.7 30.9 |
| --- | --- | --- | --- | --- | --- | --- | ----- | ---- | ------------- | -------------- | --------- |
| 25  |     | 48  |     |     |     |     | LLaMA | 𝑂    |               |                |           |
|     |     |     |     |     |     |     |       | SO   | 3.1 13.0 13.3 | 21.4 15.2 24.1 | 15.3 25.0 |
| 20  |     |     |     |     |     |     | -7B   | 𝑂    |               |                |           |
|     |     | 46  |     |     |     |     |       | DAIL | 3.1 13.0 18.5 | 25.4 22.1 28.1 | 22.6 29.3 |
𝑂
| 15  |     |     |     |     |     |     |      | FI  | 63.9 66.7 59.6 | 61.4 58.7 61.4 | 59.4 61.5 |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | -------------- | -------------- | --------- |
|     |     | 44  |     |     |     |     |      | 𝑂   |                |                |           |
| 10  |     |     |     |     |     |     | +SFT | SO  | 63.9 66.7 59.8 | 62.3 58.8 61.1 | 59.5 62.2 |
𝑂
|     |        |     |     |        |     |     |        | DAIL | 63.9 66.7 58.5 | 61.9 59.8 61.7 | 58.9 60.9 |
| --- | ------ | --- | --- | ------ | --- | --- | ------ | ---- | -------------- | -------------- | --------- |
| 0 1 | 2 3    | 4 5 | 0 1 | 2      | 3 4 | 5   |        |      | 𝑂              |                |           |
|     | k-shot |     |     | k-shot |     |     |        | FI   | 2.4 20.3 21.6  | 33.8 27.3 38.1 | 28.5 38.8 |
|     |        |     |     |        |     |     | LL a M | A 𝑂  |                |                |           |
L L a M A - 3 3 B ,   S O O L L a M A -3 3 B ,  F IO Vicuna-33B, DAILO Vicuna-33B, FIO SO 2.4 20.3 20.7 33.6 23.2 35.9 27.4 36.9
| L L a M A - 3 3 B | ,   D A ILO V ic u na | -3 3 B ,  S O |     |     |     |     | -1 3 | B 𝑂  |               |                |           |
| ----------------- | --------------------- | ------------- | --- | --- | --- | --- | ---- | ---- | ------------- | -------------- | --------- |
|                   |                       | O             |     |     |     |     |      | DAIL | 2.4 20.3 13.2 | 30.0 15.5 32.3 | 16.2 32.4 |
𝑂
|           |                     |      |             |     |      |     |      | FI  | 62.7 67.0 61.9 | 67.1 60.5 65.0 | 60.9 65.0 |
| --------- | ------------------- | ---- | ----------- | --- | ---- | --- | ---- | --- | -------------- | -------------- | --------- |
| Figure 5: | Few-shot evaluation | with | open-source |     | LLMs | on  |      | 𝑂   |                |                |           |
|           |                     |      |             |     |      |     | +SFT | SO  | 62.7 67.0 61.9 | 66.2 60.1 64.6 | 60.2 65.2 |
𝑂
| Spider-dev. |     |     |     |     |     |     |     | DAIL | 62.7 67.0 62.5 | 66.5 60.6 66.0 | 61.3 66.4 |
| ----------- | --- | --- | --- | --- | --- | --- | --- | ---- | -------------- | -------------- | --------- |
𝑂
Table4:Few-shotevaluationresultsofsupervisedfine-tuned
| Notably, | in both zero-shot | and few-shot |     | scenarios, | the | open- |     |     |     |     |     |
| -------- | ----------------- | ------------ | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- |
LLMsonSpider-dev.
sourceLLMsarefarbehindOpenAILLMs.Wewilltrytofurther
enhancetheirperformancewithsupervisedfine-tuning.
| 4.4.4 SupervisedFine-tuningwithOpen-sourceLLM. |     |     |     |     | Tofurther |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
promptsasshowninTable4.Wealsoaddtheevaluationresults
enhanceOpen-sourceLLMs’performances,weexploresupervised
oforiginalLLaMA-7Band13Bforclearcomparison.Unexpectedly,
fine-tuningforText-to-SQL.Similartoin-contextlearning,itmay
thefine-tunedLLMsfailtolearnfromexamples.Specifically,adding
| prefer different | representations. | Thus, | we  | first fine-tune |     | open- |     |     |     |     |     |
| ---------------- | ---------------- | ----- | --- | --------------- | --- | ----- | --- | --- | --- | --- | --- |
sourceLLMsonzero-shottrainingsampleswithdifferentrepre- contextualexamplesintestpromptsincurssuddendecreaseinboth
exact-set-matchandexecutionmatchaccuracy,andaddingmore
sentations.Followingthesettingofsupervisedfine-tuning[34,47],
examplesisalsounhelpful.ApossiblereasonisthatLLMoverfits
weblockthegradientsfrompromptandonlyupdateweightswith
tozero-shotprompt,whichmakesexamplesunuseful.
thosefromresponse(SQLqueries).WeusethetrainsplitinSpider,
Insummary,open-sourceLLMsdemonstratesignificantpoten-
whichcontains8659trainingsamples.Formoretrainingdetails,
pleaserefertoAppendixD.4. tialforText-to-SQLtasks,particularlyinsupervisedfine-tuning.
Zero-shotScenario.Fig.6showstheperformanceofsupervised Specifically,afterfine-tuning,theirperformancesarecomparableto
TEXT-DAVINCI-003inzero-shotscenario.However,unlikeOpenAI
| fine-tuning | with various | LLMs and | question | representations |     | in  |     |     |     |     |     |
| ----------- | ------------ | -------- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- |
LLMs,fine-tunedLLMsfailtolearnfromcontextualexamples.The
zero-shotscenario.Comparedwithzero-shotperformancebefore
questionofpreservingin-contextlearningabilityafterfine-tuning
fine-tuninginTable3,theirperformancesaregreatlyenhanced.
Bycomparingdifferentrepresentations,AlpacaSFTPromptshow remainstobeexploredinfuturestudies.
obviousadvantagesinsupervisedfine-tuningasitisdesignedfor
|     |     |     |     |     |     |     | 4.5 | TokenEfficiency |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- |
suchscenario.
Wealsoobservethegapamongdifferentrepresentationsand Considering OpenAI LLMs are charged by token numbers, and
model scales becomes narrow. The possible reason is that after LLMs’runningtimeareproportionaltotokenlengths,weunder-
fine-tuning,LLMslearntoanswernewText-to-SQLquestionswith- scoretokenefficiencyinpromptengineering,whichaimstoachieve
outtaskinstructionandforeignkeys.Inthisexperiment,thebest higheraccuracywithlesstokens.Inthissection,wereviewour
performanceonSpiderisachievedbythecombinationofLLaMA- experimentsonSpider-devintermsoftokenefficiency.(Formoreef-
13BandAlpacaSFTPrompt,whoseexact-set-matchandexecution ficiencyanalysis,pleaserefertoAppendixE.1andE.2.)Specifically,
accuracyare65.1%and68.6%.Formoredetailednumericalresults, forbothOpenAIandopen-sourceLLMs,weexperimentallystudy
pleaserefertoAppendixD.5.AsforlargerLLM,thecombination thetrade-offbetweenexecutionaccuracyandtokennumbers,and
ofLLaMA-33BandCodeRepresentationPromptachieves69.1% thetokennumberismainlyaffectedbyquestionrepresentationand
executionaccuracyand65.9%exact-set-matchaccuracy.Dueto exampleorganization.Forexampleselection,wefixitasDAIL 𝑆 .Be-
thelimitedresources,weleaveLLMslargerthan33Basourfuture sides,wealsoincludeseveralstate-of-the-artText-to-SQLmethods
| work. |     |     |     |     |     |     | inourcomparison,includingDIN-SQL[37],STRIKE[29]andCBR- |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------ | --- | --- | --- | --- |
Insummary,supervisedfine-tuningisquitebeneficialforopen- ApSQL[14].Wetaketheirreportedhighestexecutionaccuracyas
source LLMs in Text-to-SQL. Compared with OpenAI LLMs, in theirperformances.Fortokencost,weaveragethetokennumber
zero-shotscenario,fine-tunedLLaMA-13Band30Barecomparable of10randomlysampledinstancesforDIN-SQL.ForSTRIKE,the
toTEXT-DAVINCI-003andslightlyweakerthanGPT-4andGPT- optimalperformanceareachievedbymajorityvotingfrom1-shotto
3.5-TURBO. 5-shotresults,resultinginasignificantincreaseintokencost.Fur-
Few-shotScenario.Aftersupervisedfine-tuning,animportant ther,forCBR-ApSQLthetokencostiscalculatedwiththeirquestion
issueis:Canwecontinuetoenhancetheperformanceofopen-source representationand8-shotexamplesinSQL-OnlyOrganization.
LLMbyaddingcontextualexamples?Toanswerthisquestion,we Fig.7showsthecomparisonintermsoftokenefficiency.Inzero-
evaluate fine-tuned LLaMA-7B and 13B with 0, 1, 3 and 5-shot shotscenario,comparedwithruleimplication,promptwithforeign

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
)%( .ccA hctam-tes-tcaxE
Basic Prompt (BSP) Code Representation Prompt (CRP) Basic Prompt (BSP) Code Representation Prompt (CRP)
80 Text Representation Prompt (TRP) Alpaca SFT Prompt (ASP) )%( .ccA noitucexE 80 Text Representation Prompt (TRP) Alpaca SFT Prompt (ASP)
OpenAI Demostration Prompt (ODP) Average OpenAI Demostration Prompt (ODP) Average
| 70  |     |     |     |     |     | 70  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
60
60
50
50
LLaMA-7B LLaMA-2-CHAT-7B LLaMA-13B LLaMA-2-CHAT-13B LLaMA-7B LLaMA-2-CHAT-7B LLaMA-13B LLaMA-2-CHAT-13B
Figure6:Zero-shotevaluationresultsonSpider-devwithdifferentfine-tunedopen-sourceLLMs.
| 84                    |     |     |      |     | 82.8 80               |      | 79.0 |     |      |      |
| --------------------- | --- | --- | ---- | --- | --------------------- | ---- | ---- | --- | ---- | ---- |
|                       |     |     | 83.5 |     |                       | 78.4 |      |     | 78.1 |      |
| )%( .ccA noitucexE 82 |     |     |      |     | )%( .ccA noitucexE 78 |      |      |     |      | 78.6 |
76
80
| 78  |     | BS  | AS          | FI      | 74   |     | BS  | AS          |     | FI     |
| --- | --- | --- | ----------- | ------- | ---- | --- | --- | ----------- | --- | ------ |
|     |     |     | P P         | O       |      |     |     | P P         |     | O      |
| 76  |     | TR  | P zero-shot | SO O    | 72   |     | TR  | P zero-shot |     | SO O   |
|     |     | OD  | FK          | DAIL    |      |     | OD  | FK          |     | DAIL   |
| 74  |     |     | P           |         | O 70 |     |     | P           |     | O      |
|     |     | CR  | RI          | DIN-SQL |      |     | CR  | RI          |     | STRIKE |
|     |     |     | P           |         | 68   |     |     | P           |     |        |
72
200 400 600 800 1737 2560 9126 200 400 600 800 1737 2560 8512
|                       |     | Avg. Token Num. |     |      |                    |                  | Avg. Token Num. |     |     |     |
| --------------------- | --- | --------------- | --- | ---- | ------------------ | ---------------- | --------------- | --- | --- | --- |
|                       |     | (a)GPT-4        |     |      |                    | (b)GPT-3.5-TURBO |                 |     |     |     |
|                       |     |                 |     | 79.5 | 70                 |                  |                 |     |     |     |
|                       |     | 78.2            |     |      | 80.5               |                  |                 |     |     |     |
| )%( .ccA noitucexE 79 |     |                 |     |      | )%( .ccA noitucexE |                  |                 |     |     |     |
60
76
| 73  |     |      |           |           | 50  |     |     | BS P | FI O            |     |
| --- | --- | ---- | --------- | --------- | --- | --- | --- | ---- | --------------- | --- |
|     |     | BS   | AS        | FI        |     |     |     | TR   | SO              |     |
| 70  |     | P    | P         | O         |     |     |     | P    | O               |     |
|     |     | TR   | zero-shot | SO        | 40  |     |     | OD   | DAIL            |     |
| 67  |     | P    |           | O         |     |     |     | P    | O               |     |
|     |     | OD P | FK        | DAIL O    |     |     |     | CR P | Fine-tuned LLM  |     |
| 64  |     | CR   | RI        | CBR-ApSQL | 30  |     |     | AS   | Open-source LLM |     |
|     |     | P    |           |           |     |     |     | P    |                 |     |
61
|     | 200 400             |                 | 600 800 | 1737 | 2560 | 200 600           | 1000            | 1400 |     | 1800 |
| --- | ------------------- | --------------- | ------- | ---- | ---- | ----------------- | --------------- | ---- | --- | ---- |
|     |                     | Avg. Token Num. |         |      |      |                   | Avg. Token Num. |      |     |      |
|     | (c)TEXT-DAVINCI-003 |                 |         |      |      | (d)Open-sourceLLM |                 |      |     |      |
Figure7:TokenefficiencyofdifferentrepresentationsinSpider-devforOpenAILLMs.Weutilizedifferentcolorstorepresent
differentquestionrepresentationsanddifferentshapestodenotedifferentexampleorganizationsaswellastheusageofforeign
keyinformationandruleimplication.Inparticular,theoverlapofshapesisusedtoindicatetheusageofbothforeignkey
informationandruleimplication.Theringsstandforthepromptsinzero-shotscenarioandthestarsstandfortheprevious
SOTAresultsoffew-shotmethodsinLLMs.
keysgenerallyachievehigherexecutionaccuracyattheexpenseof Insummary,tokenefficiencyisacriticalmetricforreal-world
moretokens.Infew-shotscenario,comparingdifferentorganization applicationsofLLMsonText-to-SQL.Inlightofthis,ourapproach,
strategies, FI are very inefficient, whose tokens numbers are DAIL-SQL,offersacompellingsolutionthatcombineshighexecu-
𝑂
severaltimesthatofDAIL andSO .ComparingDAIL and tionaccuracywithimprovedtokenefficiency.Thismakesithighly
|     |     | 𝑂   | 𝑂   | 𝑂   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
SO ,DAIL togetherwithGPT-4achievethehighestaccuracyof practicalandsuitableforreal-worldapplications.
| 𝑂                                                       | 𝑂   |         |                   |     |     |              |     |     |     |     |
| ------------------------------------------------------- | --- | ------- | ----------------- | --- | --- | ------------ | --- | --- | --- | --- |
| 83.5%,yethavingsimilartokencostwithSO                   |     |         | 𝑂 .Therefore,DAIL |     | 𝑂   |              |     |     |     |     |
| aremoreefficientthanSO                                  | 𝑂   | andFI 𝑂 | intermsoftoken.   |     |     |              |     |     |     |     |
| Comparedwithotherstate-of-the-artsolutions,DAIL-SQLout- |     |         |                   |     |     | 5 DISCUSSION |     |     |     |     |
performs DIN-SQL and STRIKE in terms of both accuracy and Basedonourexperiments,wecanhavesomeempiricalinsights
efficiency.WhileforCBR-ApSQL,itachieves78.2%accuracywith andguidelinesasfollows:
TEXT-DAVINCI-003,butstilllowerthantheoptimalperformance
achievedbyDAIL 𝑆 +FI 𝑂 . • Forquestionrepresentation,CodeRepresentationPrompt
Besides,Foropen-sourceLLMinFig.7(d),theLLMsfine-tuned andOpenAIDemostrationPromptarerecommended,and
onText-to-SQLaremuchmoreefficient.However,asdiscussedin otherinformationsuchasforeignkeyandruleimplication
Sec.4.4,addingexamplesisunhelpfulforopen-sourceLLMs,and canbeveryhelpful.
Forexampleselection,thesimilaritiesofbothnaturallan-
| evenreducestheirtokenefficiency. |     |     |     |     |     | •   |     |     |     |     |
| -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
guagequestionandSQLqueryareimportant.Thesetwo

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
similaritiestogetherareagoodindicatorfordesigningef- [5] UrsinBrunnerandKurtStockinger.2021. ValueNet:ANaturalLanguage-to-
fectiveselectionstrategy. SQLSystemthatLearnsfromDatabaseInformation.In37thIEEEInternational
ConferenceonDataEngineering,ICDE2021,Chania,Greece,April19-22,2021.
• Forexampleorganization,iftheadoptedLLMispowerful 2177–2182.
enough, like GPT-4, presenting them question and SQL [6] RuichuCai,BoyanXu,ZhenjieZhang,XiaoyanYang,ZijianLi,andZhihao
querypairsisaneffectiveyetefficientchoice.Otherwise, Liang.2018. AnEncoder-DecoderFrameworkTranslatingNaturalLanguage
toDatabaseQueries.InProceedingsoftheTwenty-SeventhInternationalJoint
presentingthemfullinformationexamplesissuggested. ConferenceonArtificialIntelligence.3977–3983.
• Foropen-sourceLLM,havingmoreparametersinLLMs [7] ShuaichenChangandEricFosler-Lussier.2023.HowtoPromptLLMsforText-
benefitstoText-to-SQLtask,butthetrainingcorpusplays to-SQL:AStudyinZero-shot,Single-domain,andCross-domainSettings.CoRR
abs/2305.11853(2023).
amorecrucialrole.Besides,supervisedfine-tuningisnec- [8] Wei-LinChiang,ZhuohanLi,ZiLin,YingSheng,ZhanghaoWu,HaoZhang,
essaryandhasconsiderablepotentialinText-to-SQLtask. LianminZheng,SiyuanZhuang,YonghaoZhuang,JosephE.Gonzalez,IonStoica,
andEricP.Xing.2023.Vicuna:AnOpen-SourceChatbotImpressingGPT-4with
Therearealsosomelimitationsinthispaper.Duetolimited 90%*ChatGPTQuality. https://lmsys.org/blog/2023-03-30-vicuna/
resources,weonlytesttworuleimplications,andtheexploration [9] NaihaoDeng,YulongChen,andYueZhang.2022.RecentAdvancesinText-to-
SQL:ASurveyofWhatWeHaveandWhatWeExpect.InProceedingsofthe29th
ofmorerulescanfurtherbenefitLLM-basedText-to-SQLsolutions.
InternationalConferenceonComputationalLinguistics.2166–2187.
Wefine-tuneopen-sourceLLMswithonlytheSpidertrainingset, [10] XiangDeng,AhmedHassanAwadallah,ChristopherMeek,OleksandrPolozov,
andadditionalText-to-SQLdatawouldfurtherenhanceLLMs.Be- HuanSun,andMatthewRichardson.2021.Structure-GroundedPretrainingfor
Text-to-SQL.InProceedingsofthe2021ConferenceoftheNorthAmericanChapter
sides,thedatabasesinSpiderandSpider-Realisticmaybenotlarge oftheAssociationforComputationalLinguistics:HumanLanguageTechnologies.
enough,andwebelievesomenewchallengesineffectivenessand 1337–1350.
[11] JacobDevlin,Ming-WeiChang,KentonLee,andKristinaToutanova.2019.BERT:
efficiencywillemergeifthereareamassoftablesinText-to-SQL
Pre-trainingofDeepBidirectionalTransformersforLanguageUnderstanding.In
task.Furthermore,thecurrentevaluationmetricprioritizescor- Proceedingsofthe2019ConferenceoftheNorthAmericanChapteroftheAssociation
rectnessoverefficiency,andpromotingLLMtogenerateefficient forComputationalLinguistics:HumanLanguageTechnologies.4171–4186.
[12] QingxiuDong,LeiLi,DamaiDai,CeZheng,ZhiyongWu,BaobaoChang,Xu
SQLamongcorrectalternativesremainsanimportant,unexplored
Sun,JingjingXu,LeiLi,andZhifangSui.2023.ASurveyforIn-contextLearning.
question. We will keep working on these limitations and open CoRRabs/2301.00234(2023).
questions. [13] XuemeiDong,ChaoZhang,YuhangGe,YurenMao,YunjunGao,LuChen,Jinshu
Lin,andDongfangLou.2023.C3:Zero-shotText-to-SQLwithChatGPT.CoRR
abs/2307.07306(2023).
6 CONCLUSIONS [14] ChunxiGuo,ZhiliangTian,JintaoTang,PanchengWang,ZhihuaWen,Kang
Yang,andTingWang.2023.ACase-BasedReasoningFrameworkforAdaptive
Inthispaper,weconductasystematicalstudyonLLM-basedText- PromptinginCross-DomainText-to-SQL.CoRRabs/2304.13301(2023).
to-SQLfromaspectsofpromptengineeringandsupervisedfine- [15] JiaqiGuo,ZechengZhan,YanGao,YanXiao,Jian-GuangLou,TingLiu,and
DongmeiZhang.2019.TowardsComplexText-to-SQLinCross-DomainDatabase
tuning.Wepointoutthatexistingin-contextlearningtechniquesfor
withIntermediateRepresentation.InProceedingsofthe57thConferenceofthe
Text-to-SQLneglectthemappingbetweenquestionsandqueries,as AssociationforComputationalLinguistics.4524–4535.
wellasthetrade-offbetweenexamplequalityandquantity.Toad- [16] EdwardJ.Hu,YelongShen,PhillipWallis,ZeyuanAllen-Zhu,YuanzhiLi,Shean
Wang,LuWang,andWeizhuChen.2022.LoRA:Low-RankAdaptationofLarge
dresstheseissues,weproposedanewpromptengineeringmethod, LanguageModels.InThe10thInternationalConferenceonLearningRepresenta-
namedDAIL-SQL,whichrefreshestheSpiderleaderboardwith tions.
[17] BinyuanHui,RuiyingGeng,LihanWang,BowenQin,YanyangLi,BowenLi,
86.6%executionaccuracyandranksthefirstplace.Regardingsu-
JianSun,andYongbinLi.2022. S2SQL:InjectingSyntaxtoQuestion-Schema
pervisedfine-tuning,wedemonstratethegreatpotentialsofopen- InteractionGraphEncoderforText-to-SQLParsers.InFindingsoftheAssociation
sourceLLMsforText-to-SQL,underlinetheimportanceoftraining forComputationalLinguistics.1254–1262.
[18] GeorgeKatsogiannis-MeimarakisandGeorgiaKoutrika.2023.ASurveyonDeep
corpus and model scaling, and point out the degeneracy of in-
LearningApproachesforText-to-SQL.VLDBJ.32,4(2023),905–936.
contextlearningcapabilityafterfine-tuning.Further,weconduct [19] AnirudhKhatry,JoyceCahoon,JordanHenkel,ShaleenDeep,K.Venkatesh
anobservationoverexistingsolutionsintermsofefficiency,which Emani,AvriliaFloratou,SumitGulwani,VuLe,MohammadRaza,SherryShi,
MukulSingh,andAshishTiwari.2023.FromWordstoCode:HarnessingData
indicatesDAIL-SQLismuchmoreefficientandemphasizestheim- forProgramSynthesisfromNaturalLanguage.CoRRabs/2305.01598(2023).
portanceoftokenefficiencyinpromptengineering.Alloftheseare [20] TakeshiKojima,ShixiangShaneGu,MachelReid,YutakaMatsuo,andYusuke
Iwasawa.2022.LargeLanguageModelsAreZero-ShotReasoners.Advancesin
openchallengesandopportunitiesforfuturestudy.Wehopethat
neuralinformationprocessingsystems35(2022),22199–22213.
ourworkcanprovideacomprehensivestudyaboutText-to-SQL, [21] Chia-HsuanLee,OleksandrPolozov,andMatthewRichardson.2021.KaggleD-
givesomeguidelinesforreal-worldapplications,andhelppeople BQA:RealisticEvaluationofText-to-SQLParsers.InProceedingsofthe59th
AnnualMeetingoftheAssociationforComputationalLinguisticsandthe11th
advanceitsfrontiers.
InternationalJointConferenceonNaturalLanguageProcessing.2261–2273.
[22] HaoyangLi,JingZhang,CuipingLi,andHongChen.2023.RESDSQL:Decoupling
SchemaLinkingandSkeletonParsingforText-to-SQL.In37thAAAIConference
REFERENCES
onArtificialIntelligence.13067–13075.
[1] YuvaneshAnand,ZachNussbaum,BrandonDuderstadt,BenjaminSchmidt,and [23] JinyangLi,BinyuanHui,ReynoldCheng,BowenQin,ChenhaoMa,NanHuo,Fei
AndriyMulyar.2023.GPT4All:TraininganAssistant-styleChatbotwithLarge Huang,WenyuDu,LuoSi,andYongbinLi.2023.Graphix-T5:MixingPre-trained
ScaleDataDistillationfromGPT-3.5-Turbo.https://github.com/nomic-ai/gpt4all. TransformerswithGraph-AwareLayersforText-to-SQLParsing.In37thAAAI
[2] AmandaAskell,YuntaoBai,AnnaChen,DawnDrain,DeepGanguli,Tom ConferenceonArtificialIntelligence.13076–13084.
Henighan,AndyJones,NicholasJoseph,BenjaminMann,NovaDasSarma,Nel- [24] JinyangLi,BinyuanHui,GeQu,BinhuaLi,JiaxiYang,BowenLi,BailinWang,
sonElhage,ZacHatfield-Dodds,DannyHernandez,JacksonKernion,Kamal BowenQin,RongyuCao,RuiyingGeng,NanHuo,XuanheZhou,ChenhaoMa,
Ndousse,CatherineOlsson,DarioAmodei,TomB.Brown,JackClark,SamMc- GuoliangLi,KevinChen-ChuanChang,FeiHuang,ReynoldCheng,andYongbin
Candlish,ChrisOlah,andJaredKaplan.2021.AGeneralLanguageAssistantas Li.2023. CanLLMAlreadyServeasADatabaseInterface?ABIgBenchfor
aLaboratoryforAlignment.CoRRabs/2112.00861(2021). Large-ScaleDatabaseGroundedText-to-SQLs.CoRRabs/2305.03111(2023).
[3] LILYGroupatYaleUniversity.2018. Spider1.0,YaleSemanticParsingand [25] XiVictoriaLin,RichardSocher,andCaimingXiong.2020.BridgingTextualand
Text-to-SQLChallenge.https://yale-lily.github.io/spider. TabularDataforCross-DomainText-to-SQLSemanticParsing.InFindingsofthe
[4] ChristopherBaik,ZhongjunJin,MichaelJ.Cafarella,andH.V.Jagadish.2020. AssociationforComputationalLinguistics,Vol.EMNLP2020.4870–4888.
Duoquest:ADual-SpecificationSystemforExpressiveSQLQueries.InProceed-
ingsofthe2020InternationalConferenceonManagementofData.2319–2329.

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
[26] AiweiLiu,XumingHu,LijieWen,andPhilipS.Yu.2023. AComprehensive Azhar,AurélienRodriguez,ArmandJoulin,EdouardGrave,andGuillaumeLam-
EvaluationofChatGPT’sZero-ShotText-to-SQLCapability.CoRRabs/2303.13547 ple.2023. LLaMA:OpenandEfficientFoundationLanguageModels. CoRR
(2023). abs/2302.13971(2023).
[27] HuLiu,YuliangShi,JianlinZhang,XinjunWang,HuiLi,andFanyuKong.2023. [49] HugoTouvron,LouisMartin,KevinStone,PeterAlbert,AmjadAlmahairi,Yas-
Multi-hopRelationalGraphAttentionNetworkforText-to-SQLParsing.In mineBabaei,NikolayBashlykov,SoumyaBatra,PrajjwalBhargava,ShrutiBhos-
InternationalJointConferenceonNeuralNetworks.1–8. ale,DanBikel,LukasBlecher,CristianCantonFerrer,MoyaChen,Guillem
[28] JiachangLiu,DinghanShen,YizheZhang,BillDolan,LawrenceCarin,and Cucurull,DavidEsiobu,JudeFernandes,JeremyFu,WenyinFu,BrianFuller,
WeizhuChen.2022.WhatMakesGoodIn-ContextExamplesforGPT-3?.InPro- CynthiaGao,VedanujGoswami,NamanGoyal,AnthonyHartshorn,Saghar
ceedingsofDeepLearningInsideOut:The3rdWorkshoponKnowledgeExtraction Hosseini,RuiHou,HakanInan,MarcinKardas,ViktorKerkez,MadianKhabsa,
andIntegrationforDeepLearningArchitectures.100–114. IsabelKloumann,ArtemKorenev,SinghKoura,Marie-AnneLachaux,Thibaut
[29] LinyongNan,YilunZhao,WeijinZou,NarutatsuRi,JaesungTae,EllenZhang, Lavril,JenyaLee,DianaLiskovich,YinghaiLu,YuningMao,XavierMartinet,
ArmanCohan,andDragomirRadev.2023. EnhancingFew-shotText-to-SQL TodorMihaylov,PushkarMishra,IgorMolybog,YixinNie,AndrewPoulton,
CapabilitiesofLargeLanguageModels:AStudyonPromptDesignStrategies. JeremyReizenstein,RashiRungta,KalyanSaladi,AlanSchelten,RuanSilva,
CoRRabs/2305.12586(2023). EricMichael,SmithRanjan,SubramanianXiaoqing,EllenTan,BinhTang,Ross
[30] OpenAI.2023.GPT-4TechnicalReport.CoRRabs/2303.08774(2023). Taylor,AdinaWilliams,JianXiangKuan,PuxinXu,ZhengYan,IliyanZarov,
[31] OpenAI.2023. IntroducingChatGPT. https://openai.com/blog/chatgpt. Last YuchenZhang,AngelaFan,MelanieKambadur,SharanNarang,AurelienRo-
accessedon2023-07-24. driguez,RobertStojnic,SergeyEdunov,andThomasScialom.2023.LLAMA2:
[32] OpenAI.2023.Ratelimits.https://platform.openai.com/docs/guides/rate-limits/ OpenFoundationandFine-TunedChatModels.CoRR(2023).
overview. Lastaccessedon2023-07-24. [50] ImmanuelTrummer.2022.CodexDB:SynthesizingCodeforQueryProcessing
[33] OpenAI.2023.SQLtranslate.https://platform.openai.com/examples/default-sql- fromNaturalLanguageInstructionsUsingGPT-3Codex.ProceedingsoftheVLDB
translate. Lastaccessedon2023-07-24. Endowment15,11(2022),2921–2928.
[34] LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,CarrollL.Wainwright, [51] BailinWang,RichardShin,XiaodongLiu,OleksandrPolozov,andMatthew
PamelaMishkin,ChongZhang,SandhiniAgarwal,KatarinaSlama,AlexRay, Richardson.2020.RAT-SQL:Relation-AwareSchemaEncodingandLinkingfor
JohnSchulman,JacobHilton,FraserKelton,LukeMiller,MaddieSimens,Amanda Text-to-SQLParsers.InProceedingsofthe58thAnnualMeetingoftheAssociation
Askell,PeterWelinder,PaulF.Christiano,JanLeike,andRyanLowe.2022. forComputationalLinguistics.7567–7578.
TrainingLanguageModelstoFollowInstructionswithHumanFeedback.In [52] LihanWang,BowenQin,BinyuanHui,BowenLi,MinYang,BailinWang,Binhua
NeurIPS. Li,JianSun,FeiHuang,LuoSi,andYongbinLi.2022.Proton:ProbingSchema
[35] GuilhermePenedo,QuentinMalartic,DanielHesslow,RuxandraCojocaru, LinkingInformationfromPre-trainedLanguageModelsforText-to-SQLParsing.
AlessandroCappelli,HamzaAlobeidli,BaptistePannier,EbtesamAlmazrouei, InThe28thACMSIGKDDConferenceonKnowledgeDiscoveryandDataMining.
andJulienLaunay.2023.TheRefinedWebdatasetforFalconLLM:outperforming 1889–1898.
curatedcorporawithwebdata,andwebdataonly.arXivpreprintarXiv:2306.01116 [53] XuezhiWang,JasonWei,DaleSchuurmans,QuocV.Le,EdH.Chi,SharanNarang,
(2023). AakankshaChowdhery,andDennyZhou.2023. Self-ConsistencyImproves
[36] OctavianPopescu,IreneManotas,NgocPhuocAnVo,HanguYeo,ElaheKho- ChainofThoughtReasoninginLanguageModels.InTheEleventhInternational
rashani,andVadimSheinin.2022.AddressingLimitationsofEncoder-Decoder ConferenceonLearningRepresentations.
BasedApproachtoText-to-SQL.InProceedingsofthe29thInternationalConfer- [54] ThomasWolf,LysandreDebut,VictorSanh,JulienChaumond,ClementDe-
enceonComputationalLinguistics.1593–1603. langue,AnthonyMoi,PierricCistac,TimRault,RémiLouf,MorganFuntowicz,
[37] MohammadrezaPourrezaandDavoodRafiei.2023. DIN-SQL:Decomposed andJamieBrew.2019. HuggingFace’sTransformers:State-of-the-artNatural
In-ContextLearningofText-to-SQLwithSelf-Correction.CoRRabs/2304.11015 LanguageProcessing.CoRRabs/1910.03771(2019).
(2023). [55] KunXu,LingfeiWu,ZhiguoWang,YansongFeng,andVadimSheinin.2018.
[38] JiexingQi,JingyaoTang,ZiweiHe,XiangpengWan,YuCheng,ChenghuZhou, SQL-to-TextGenerationwithGraph-to-SequenceModel.InProceedingsofthe
XinbingWang,QuanshiZhang,andZhouhanLin.2022. RASAT:Integrating 2018ConferenceonEmpiricalMethodsinNaturalLanguageProcessing.931–936.
RelationalStructuresintoPretrainedSeq2SeqModelforText-to-SQL.InProceed- [56] PengchengYin,GrahamNeubig,Wen-tauYih,andSebastianRiedel.2020.
ingsofthe2022ConferenceonEmpiricalMethodsinNaturalLanguageProcessing. TaBERT:PretrainingforJointUnderstandingofTextualandTabularData.In
3215–3229. Proceedingsofthe58thAnnualMeetingoftheAssociationforComputationalLin-
[39] BowenQin,BinyuanHui,LihanWang,MinYang,JinyangLi,BinhuaLi,Ruiying guistics,ACL2020,Online,July5-10,2020,DanJurafsky,JoyceChai,Natalie
Geng,RongyuCao,JianSun,LuoSi,FeiHuang,andYongbinLi.2022.ASur- Schluter,andJoelR.Tetreault(Eds.).AssociationforComputationalLinguistics,
veyonText-to-SQLParsing:Concepts,Methods,andFutureDirections.CoRR 8413–8426.
abs/2208.13629(2022). [57] TaoYu,RuiZhang,KaiYang,MichihiroYasunaga,DongxuWang,ZifanLi,
[40] AbdulQuamar,VasilisEfthymiou,ChuanLei,FatmaÖzcan,etal.2022.Natural JamesMa,IreneLi,QingningYao,ShanelleRoman,ZilinZhang,andDragomirR.
languageinterfacestodata.FoundationsandTrends®inDatabases11,4(2022), Radev.2018.Spider:ALarge-ScaleHuman-LabeledDatasetforComplexand
319–414. Cross-DomainSemanticParsingandText-to-SQLTask.InProceedingsofthe2018
[41] NitarshanRajkumar,RaymondLi,andDzmitryBahdanau.2022. Evaluating ConferenceonEmpiricalMethodsinNaturalLanguageProcessing.3911–3921.
theText-to-SQLCapabilitiesofLargeLanguageModels.CoRRabs/2204.00498 [58] WayneXinZhao,KunZhou,JunyiLi,TianyiTang,XiaoleiWang,YupengHou,
(2022). YingqianMin,BeichenZhang,JunjieZhang,ZicanDong,YifanDu,ChenYang,
[42] BaptisteRoziere,JonasGehring,FabianGloeckle,StenSootla,ItaiGat,Xiao- YushuoChen,ZhipengChen,JinhaoJiang,RuiyangRen,YifanLi,XinyuTang,
qingEllenTan,YossiAdi,JingyuLiu,TalRemez,JérémyRapin,etal.2023.Code ZikangLiu,PeiyuLiu,Jian-YunNie,andJi-RongWen.2023.ASurveyofLarge
llama:Openfoundationmodelsforcode.arXivpreprintarXiv:2308.12950(2023). LanguageModels.CoRRabs/2303.18223(2023).
[43] TorstenScholak,NathanSchucher,andDzmitryBahdanau.2021. PICARD: [59] LianminZheng,Wei-LinChiang,YingSheng,SiyuanZhuang,ZhanghaoWu,
ParsingIncrementallyforConstrainedAuto-RegressiveDecodingfromLanguage YonghaoZhuang,ZiLin,ZhuohanLi,DachengLi,EricP.Xing,HaoZhang,
Models.InProceedingsofthe2021ConferenceonEmpiricalMethodsinNatural JosephE.Gonzalez,andIonStoica.2023. JudgingLLM-as-a-judgewithMT-
LanguageProcessing.9895–9901. BenchandChatbotArena.CoRRabs/2306.05685(2023).
[44] JaydeepSen,ChuanLei,AbdulQuamar,FatmaÖzcan,VasilisEfthymiou,Ayushi [60] YanzhaoZheng,HaibinWang,BaohuaDong,XingjunWang,andChangshanLi.
Dalmia,GregStager,AshishR.Mittal,DiptikalyanSaha,andKarthikSankara- 2022.HIE-SQL:HistoryInformationEnhancedNetworkforContext-Dependent
narayanan.2020.ATHENA++:NaturalLanguageQueryingforComplexNested Text-to-SQLSemanticParsing.InFindingsoftheAssociationforComputational
SQLQueries.Proc.VLDBEndow.13,11(2020),2747–2759. Linguistics.2997–3007.
[45] KaitaoSong,XuTan,TaoQin,JianfengLu,andTie-YanLiu.2020.MPNet:Masked [61] RuiqiZhong,TaoYu,andDanKlein.2020.SemanticEvaluationforText-to-SQL
andPermutedPre-trainingforLanguageUnderstanding.InAdvancesinNeural withDistilledTestSuites.InProceedingsofthe2020ConferenceonEmpirical
InformationProcessingSystems33:AnnualConferenceonNeuralInformation MethodsinNaturalLanguageProcessing.396–411.
ProcessingSystems. [62] VictorZhong,CaimingXiong,andRichardSocher.2017.Seq2SQL:Generating
[46] RuoxiSun,SercanÖ.Arik,HootanNakhost,HanjunDai,RajarishiSinha, StructuredQueriesfromNaturalLanguageusingReinforcementLearning.CoRR
PengchengYin,andTomasPfister.2023.SQL-PaLM:ImprovedLargeLanguage abs/1709.00103(2017).
ModelAdaptationforText-to-SQL.CoRRabs/2306.00739(2023).
[47] RohanTaori,IshaanGulrajani,TianyiZhang,YannDubois,XuechenLi,Carlos
Guestrin,PercyLiang,andTatsunoriB.Hashimoto.2023.StanfordAlpaca:An
Instruction-followingLLaMAmodel. https://github.com/tatsu-lab/stanford_
alpaca.
[48] HugoTouvron,ThibautLavril,GautierIzacard,XavierMartinet,Marie-Anne
Lachaux,TimothéeLacroix,BaptisteRozière,NamanGoyal,EricHambro,Faisal

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
A DETAILSOFDAIL-SQL
A.1 Pseudocode
ThepseudocodeofDAIL-SQLisshowninAlg.1.InDAIL-SQL,weinitiallyeliminatethetokensassociatedwithdatabasesinthequestions
andqueriesofboththetargetandcross-domaincandidates(lines1-10).Next,weorderthecandidatesbasedonquestionsimilarityandgive
preferencetothosewithahighquerysimilarity(lines11-20).Lastly,wechoosethetop𝑘candidatesasexamples,representtheirquestions
andqueriesintheCodeRepresentationPrompt,andfeedthepromptintoalargelanguagemodeltogeneratethefinalpredictedSQLquery
(lines21-23).
DAIL-SQLutilizessomefunctionsfromexistingworks.Specifically,weidentifydatabase-relatedtokensinthequestionsusingschema-
linking[51](line2and4),andextractqueryskeletonsbyretainingtheirSQLkeywords[22](line8and10).Inline12,weencodethemasked
questionsusingall-mpnet-base-v2[45].
Input:Targetquestion𝑞anddatabaseD,asetoftriplesQ={(𝑞 ,𝑠 ,D𝑖)},numberofexamples𝑘,largelanuagemodelM,theCode
𝑖 𝑖
Representation𝜎 withDAILOrganization,preliminarypredictorP,sentenceembeddingmodel𝑒,andquerysimilarity
𝐶𝑅𝑃
threshold𝜂.
Output:SQLquery𝑠ofthetargetquestion𝑞
#𝑚𝑎𝑠𝑘𝑡ℎ𝑒𝑡𝑜𝑘𝑒𝑛𝑠𝑟𝑒𝑙𝑎𝑡𝑒𝑑𝑡𝑜𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒𝑠𝑖𝑛𝑏𝑜𝑡ℎ𝑡𝑎𝑟𝑔𝑒𝑡𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛𝑎𝑛𝑑𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛𝑠
1
𝑞′=mask_question(𝑞)
2
| for(𝑞 𝑖 ,𝑠 | 𝑖 ,𝐷 𝑖) ∈Qdo |     |
| ---------- | ------------ | --- |
3
| 𝑞′=mask_question(𝑞 |     | )   |
| ------------------ | --- | --- |
| 4 𝑖                |     | 𝑖   |
5 end
#𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑆𝑄𝐿𝑞𝑢𝑒𝑟𝑦𝑣𝑖𝑎𝑝𝑟𝑒𝑙𝑖𝑚𝑖𝑛𝑎𝑟𝑦𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 P
6
| 𝑠 =P(𝜎 | (𝑞,D)) |     |
| ------ | ------ | --- |
| 7 P    | 𝐶𝑅𝑃    |     |
#𝑒𝑥𝑡𝑟𝑎𝑐𝑡𝑠𝑘𝑒𝑙𝑒𝑡𝑜𝑛𝑠𝑜𝑓
| 8                        | 𝑡ℎ𝑒𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑒𝑑𝑆𝑄𝐿𝑞𝑢𝑒𝑟𝑦𝑎𝑛𝑑𝑞𝑢𝑒𝑟𝑖𝑒𝑠𝑖𝑛𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑠 |     |
| ------------------------ | ------------------------------------------ | --- |
| 𝑠′ =extract_skeleton(𝑠   |                                            | )   |
| 9 P                      | P                                          |     |
| for(𝑞 ,𝑠                 | ,𝐷                                         |     |
| 10 𝑖                     | 𝑖 𝑖) ∈Qdo                                  |     |
| 11 𝑠′=extract_skeleton(𝑠 |                                            | 𝑖 ) |
𝑖
end
12
#𝑠𝑜𝑟𝑡𝑡ℎ𝑒𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑠𝑤𝑖𝑡ℎ𝑡ℎ𝑒𝑚𝑎𝑠𝑘𝑒𝑑𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦
13
sortQbycosine_simlarity(𝑒(𝑞′),𝑒(𝑞′))
| 14       |                                                     | 𝑖   |
| -------- | --------------------------------------------------- | --- |
| #𝑟𝑒𝑜𝑟𝑑𝑒𝑟 | Q𝑏𝑦𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑖𝑧𝑖𝑛𝑔𝑡ℎ𝑒𝑐𝑎𝑛𝑑𝑖𝑑𝑎𝑡𝑒𝑠𝑤𝑖𝑡ℎℎ𝑖𝑔ℎ𝑞𝑢𝑒𝑟𝑦𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦 |     |
15
| 16 Qℎ𝑖𝑔ℎ_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦       | ,Q𝑙𝑜𝑤_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦 | =∅,∅         |
| ----------------------- | -------------- | ------------ |
| for(𝑞 ,𝑠                | ,𝐷 𝑖) ∈Qdo     |              |
| 17 𝑖                    | 𝑖              |              |
| ifJaccard_similarity(𝑠′ |                | ,𝑠 ′)≥𝜂then  |
| 18                      |                | P 𝑖          |
| 19 Qℎ𝑖𝑔ℎ_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦       | ←(𝑞            | 𝑖 ,𝑠 𝑖 ,𝐷 𝑖) |
end
20
21 else
| 22 Q𝑙𝑜𝑤_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦 | ←(𝑞 | 𝑖 ,𝑠 𝑖 ,𝐷 𝑖) |
| ---------------- | --- | ------------ |
end
23
24 end
Q=Qℎ𝑖𝑔ℎ_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦+Q𝑙𝑜𝑤_𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦
25
| #𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒𝑝𝑟𝑜𝑚𝑝𝑡𝑎𝑛𝑑 | 𝑓𝑖𝑛𝑎𝑙𝑆𝑄𝐿𝑞𝑢𝑒𝑟𝑦 |     |
| ------------------ | ------------- | --- |
26
Q𝑠 =Q[0:𝑘]
27
| 𝑠 =M(𝜎 | (𝑞,D,Q𝑠)) |     |
| ------ | --------- | --- |
| 28 M   | 𝐶𝑅𝑃       |     |
𝑠
| 29 return | M   |     |
| --------- | --- | --- |
Algorithm1:DAIL-SQLAlgorithm
A.2 ImplementationDetails
ForquestionsimilarityinQTS ,MQS andDAIL ,wefirstconnectquestionwordstothedatabasewitha𝑛-grammatchingbased
𝑆 𝑆 𝑆
schema-linkingmethod[51].Thentoobtaintheskeleton,wereplacetableandcolumnnameswith“<mask>”,andvalueswith“<unk>”.At
last,weembedthemaskedquestionswithapre-trainedsentenceTransformer,all-mpnet-base-v2[45],tocalculatetheirsimilarities.
ForquerysimilarityinDAIL ,weutilizeGraphix[23]asthepreliminarymodeltogeneratethepredictedquery𝑠′.Thenweobtainits
𝑆
skeletonbyremovingitsdatabase-specificinformation[22],includingcolumnnamesandvalues.Finally,wecalculatetheJaccardsimilarity

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
betweenexamplecandidateandthepredictedquery𝑠′astheirquerysimilarity.Forthequerysimilaritythreshold𝜏 inDAIL ,wesetitas
𝑆
0.9intheexperimentsofthispaper.
ForthesubmissiontotheSpiderleaderboard,weset𝜏 tobe0.85andutilizeGPT-4,withCR ,MQS andDAIL ,asthepreliminary
|     |     |     |     | 𝑃   | 𝑆 𝑂 |
| --- | --- | --- | --- | --- | --- |
modeltoensureonlyonemodelinvolved.Furthermore,weprocesstheself-consistencyvotingon5producedqueriesforeachquestionand
settheargumenttemperatureas1.0forvarietyinvoting.
B QUESTIONREPRESENTATIONS
B.1 DetailedPerformanceofDifferentQuestionRepresentations
Thenumericalresultsofdifferentquestionrepresentationsinzero-shotscenarioareshowinTable5.
|     | GPT-4 | GPT-3.5-TURBO |     | TEXT-DAVINCI-003 |     |
| --- | ----- | ------------- | --- | ---------------- | --- |
Prompt
|                          | EM   | EX EM     | EX   | EM   | EX   |
| ------------------------ | ---- | --------- | ---- | ---- | ---- |
| BasicPrompt              | 48.5 | 74.3 45.5 | 72.5 | 29.9 | 65.5 |
| TextRepresentationPrompt | 41.4 | 72.3 43.2 | 71.9 | 33.7 | 67.4 |
| OpenAIDemostrationPrompt | 47.5 | 73.9 48.8 | 75.5 | 35.5 | 70.5 |
| CodeRepresentationPrompt | 22.1 | 72.3 34.6 | 74.4 | 31.7 |      |
71.7
| AlpacaSFTPrompt | 39.4 | 73.6 37.9 | 69.5 | 23.2 | 63.6 |
| --------------- | ---- | --------- | ---- | ---- | ---- |
Table5:Detailsofzero-shotevaluationonSpider-devwithdifferentquestionrepresentations.
B.2 DetailedPerformanceofDifferentRepresentationswithForeignKeys
ThenumericalresultsoftheablationstudyaboutforeignkeyinformationareshowninTable6.
|     |     | GPT-4 |     | GPT-3.5-TURBO | TEXT-DAVINCI-003 |
| --- | --- | ----- | --- | ------------- | ---------------- |
Prompt
|     |     | EM EX |     | EM EX | EM EX |
| --- | --- | ----- | --- | ----- | ----- |
BasicPromptWithForeignKeys 48.4(-0.1) 76.9(+2.6) 47.9(+2.4) 74.5(+2.0) 32.4(+2.5) 66.3(+0.8)
TextRepresentationPromptWithForeignKeys 41.9(+0.5) 72.1(-0.2) 44.3(+1.1) 73.5(+1.6) 34.1(+0.4) 69.2(+1.8)
OpenAIDemostrationPromptWithForeignKeys 46.1(-1.4) 74.5(+0.6) 51.5(+2.7) 78.4(+2.9) 34.3(-1.2) 72.6(+2.1)
AlpacaSFTPromptWithForeignKeys 39.7(+0.3) 76.2(+2.6) 38.9(+1.0) 70.6(+1.1) 23.0(-0.2) 63.2(-0.4)
Table6:Detailsofzero-shotevaluationonSpider-devwithforeignkeysandcomparisonswiththeresultsobtainedwithout
foreignkeysinTable5.
B.3 DetailedPerformanceofDifferentRepresentationswith/withoutExplanationrule
ThenumericalresultsofablationstudyaboutruleimplicationareshowninTable7.
|     |     | GPT-4 | GPT-3.5-TURBO |     | TEXT-DAVINCI-003 |
| --- | --- | ----- | ------------- | --- | ---------------- |
Prompt
|     | EM  | EX  | EM  | EX  | EM EX |
| --- | --- | --- | --- | --- | ----- |
TextRepresentationPromptWithRule 43.5(+2.1) 72.9(+0.6) 46.4(+3.2) 73.4(+1.5) 36.8(+3.1) 68.9(+1.5)
OpenAIDemostrationPromptWithoutRule 42.7(-4.8) 72.1(-1.8) 42.5(-6.3) 73.5(-2.0) 33.1(-2.4) 69.2(-1.3)
CodeRepresentationPromptWithRule 26.6(+4.5) 73.7(+1.4) 37.9(+3.3) 76.6(+2.2) 36.8(+5.1) 72.6(+0.9)
AlpacaSFTPromptWithRule 43.0(+3.6) 74.8(+1.2) 40.2(+2.3) 70.4(+0.9) 27.1(+3.9)
66.5(+2.9)
Table7:Detailsofzero-shotevaluationonSpider-devwith/withoutruleimplication“withnoexplanation”ininstructionsand
comparisonswiththeiroppositesinTable5.
B.4 QuestionRepresentationswithRuleImplication“Let’sthinkstepbystep”
Thenumericalresultsoftheablationstudywiththerule“Let’sthinkstepbystep”areshowninTable8.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
|     |     |     |     | GPT-3.5-TURBO |     | TEXT-DAVINCI-003 |     |     |
| --- | --- | --- | --- | ------------- | --- | ---------------- | --- | --- |
Prompt
|     |     |                                  |     | EM          | EX          | EM          |             | EX  |
| --- | --- | -------------------------------- | --- | ----------- | ----------- | ----------- | ----------- | --- |
|     |     | TextRepresentationPromptWithRule |     | 20.0(-23.2) | 45.9(-26.0) | 23.0(-10.7) | 46.1(-21.3) |     |
|     |     | CodeRepresentationPromptWithRule |     | 21.7(-12.9) | 52.2(-22.2) | 31.9(+0.2)  | 63.8(-7.9)  |     |
OpenAIDemostrationPromptWithRule 48.4(-0.4) 75.8(+0.3) 41.2(+5.7) 72.4(+1.9)
|     |     | AlpacaSFTPromptWithRule |     | 21.5(-16.4) | 49.3(-20.2) | 27.9(+4.7) | 64.4(+0.8) |     |
| --- | --- | ----------------------- | --- | ----------- | ----------- | ---------- | ---------- | --- |
Table8:Zero-shotevaluationresultsonSpider-devwith"Let’sthinkstepbystep"ruleimplicationininstructionsandcompar-
isonswithTable5.
C IN-CONTEXTLEARNINGFORTEXT-TO-SQL
InFig.8,wepresenttheresultsofourone-shotevaluationfordifferentquestionrepresentations.Specifically,weuseFI 𝑂 exampleswith
DAIL here,andTable9showsthecomparisonswiththezero-shotscenario.Bycomparingzero-shotandone-shotevaluationresults,
𝑆
addingcontextualexampleshowobviousandconsistentimprovementsforallLLMsinexact-set-matchaccuracy.Intermofexecution
accuracy,contextualexamplesbenefitsbothGPT-4andTEXT-DAVINCI-003.However,forGPT-3.5-TURBO,addingcontextualexamples
onlybenefitsTR 𝑃 andCR 𝑃 ,indicatingthein-contextlearningcapabilitybiasindifferentLLMs.Bycomparingdifferentrepresentations,
CR 𝑃 showsobviousadvantageinexecutionaccuracy,astakingtheadvantageofprogramming.
C.1 One-ShotEvaluationonDifferentQuestionRepresentation
95
| )%( .ccA hctam-tes-tcaxE | Baseline Prompt            |     | Code Representation Prompt |                    |                            |     |     |                            |
| ------------------------ | -------------------------- | --- | -------------------------- | ------------------ | -------------------------- | --- | --- | -------------------------- |
|                          |                            |     |                            |                    | Baseline Prompt            |     |     | Code Representation Prompt |
|                          | Text Representation Prompt |     | Alpaca SFT Prompt          | )%( .ccA noitucexE |                            |     |     |                            |
| 80                       |                            |     |                            |                    | Text Representation Prompt |     |     | Alpaca SFT Prompt          |
OpenAI Demostration Prompt Average 85 OpenAI Demostration Prompt Average
60
75
40
65
20
GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003 GPT-4 GPT-3.5-TURBO TEXT-DAVINCI-003
Figure8:Resultsofone-shotevaluationonSpider-devwithdifferentquestionrepresentationsandcomparisonswiththeresults
ofzero-shotevaluationinFig.1.Thegreenarrowindicatesincrease,andredarrowindicatesdecrease.
|     |     |     | GPT-4 |     | GPT-3.5-TURBO |     | TEXT-DAVINCI-003 |     |
| --- | --- | --- | ----- | --- | ------------- | --- | ---------------- | --- |
Prompt
|     |     |     | EM  | EX  | EM  | EX  | EM  | EX  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
BasicPrompt 64.2(+15.7) 79.3(+5.0) 56.5(+11.0) 71.5(-1.0) 53.2(+23.3) 71.6(+6.1)
TextRepresentationPrompt 63.4(+22.0) 79.5(+7.2) 56.5(+13.3) 73.1(+1.2) 57.1(+23.4) 72.3(+4.9)
OpenAIDemostrationPrompt 65.8(+18.3) 80.7(+6.8) 57.7(+8.9) 72.9(-2.6) 56.6(+21.1) 74.7(+4.2)
CodeRepresentationPrompt 62.1(+40.0) 80.2(+7.9) 59.5(+24.9) 75.5(+1.1) 51.9(+20.2) 76.9(+5.2)
AlpacaSFTPrompt 61.9(+22.5) 77.8(+4.2) 53.1(+15.2) 67.6(-1.9) 50.2(+27.0) 69.3(+5.7)
Table9:Detailsofone-shotevaluationonSpider-devwithdifferentquestionrepresentationsandcomparisonswiththeresults
ofzero-shotevaluationinTable5.
C.2 DetailedPerformanceofDifferentExampleOrganizations
Thenumericalresultsofdifferentexampleorganizationstrategiesinfew-shotscenarioareshowninTable10and11.
C.3 ComparisonsbetweenDAIL-SQLandPreviousWorks
Inthissubsection,wecompareDAIL-SQLwithpreviousworks,includingworksbasedonparsingrules,pre-trainedlanguagemodels
(PLM),andlargelanguagemodels(LLM).AsTable12shows,theperformanceofPLM-basedandrule-basemethodshasrecentlybecomeless
competitive.Consequently,LLM-basedmethodshaveemergedasapromisinganddominantapproachforText-to-SQLtasks.Giventhis
shift,inthispaper,wefocusmoreonasystematicallystudyforLLM-basedText-to-SQLmethods.

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
|          |                              | GPT-4 GPT-3.5-TURBO | TEXT-DAVINCI-003 |      |
| -------- | ---------------------------- | ------------------- | ---------------- | ---- |
| Few-shot | Presentation                 |                     |                  |      |
|          |                              | EM EX EM            | EX EM            | EX   |
| 0-shot   | -                            | 22.1 72.3 34.6      | 74.4 31.7        | 71.7 |
|          | Full-InformationOrganization | 62.1 80.2 59.5      | 75.5 51.9        | 76.9 |
| 1-shot   | SQL-OnlyOrganization         | 55.2 79.2 51.2      | 76.3 41.2        | 72.4 |
|          | DAILOrganization             | 62.9 80.9 57.6      | 77.5 46.9        | 73.2 |
|          | Full-InformationOrganization | 69.1 81.7 63.9      | 77.8 64.4        | 79.5 |
| 3-shot   | SQL-OnlyOrganization         | 64.7 80.2 56.2      | 77.9 48.6        | 74.3 |
|          | DAILOrganization             | 69.0 82.4 61.9      | 76.7 54.0        | 74.6 |
|          | Full-InformationOrganization | 71.9 82.4 66.7      | 78.1 67.7        | 80.5 |
| 5-shot   | SQL-OnlyOrganization         | 66.6 80.9 56.2      | 78.8 52.1        | 75.0 |
|          | DAILOrganization             | 70.8 82.5 64.3      | 79.0 58.2        | 75.3 |
|          | SQL-OnlyOrganization         | 67.8 81.1 57.2      | 78.5 52.1        | 74.8 |
7-shot
|     | DAILOrganization     | 72.5 83.5 65.6 | 78.2 59.0 | 74.4 |
| --- | -------------------- | -------------- | --------- | ---- |
|     | SQL-OnlyOrganization | 67.6 81.0 57.7 | 78.0 53.0 | 74.9 |
9-shot
|     | DAILOrganization | 72.8 83.4 65.3 | 77.9 60.3 | 74.4 |
| --- | ---------------- | -------------- | --------- | ---- |
Table10:DetailsofFew-shotevaluationonSpiderdevelopmentsplitwithdifferentorganizations.
|          |                              | GPT-4 GPT-3.5-TURBO | TEXT-DAVINCI-003 |      |
| -------- | ---------------------------- | ------------------- | ---------------- | ---- |
| Few-shot | Presentation                 |                     |                  |      |
|          |                              | EM EX EM            | EX EM            | EX   |
| 0-shot   | -                            | 19.9 66.5 29.3      | 67.3 28.0        | 65.0 |
|          | Full-InformationOrganization | 50.2 73.2 48.6      | 69.1 42.1        | 67.1 |
| 1-shot   | SQL-OnlyOrganization         | 45.3 70.7 42.7      | 68.7 34.6        | 64.4 |
|          | DAILOrganization             | 51.2 72.2 48.4      | 69.3 38.6        | 64.6 |
|          | Full-InformationOrganization | 59.1 73.6 52.6      | 68.3 54.5        | 69.7 |
| 3-shot   | SQL-OnlyOrganization         | 56.9 73.8 48.8      | 70.9 42.7        | 65.9 |
|          | DAILOrganization             | 60.8 74.8 52.8      | 69.1 48.4        | 65.7 |
|          | Full-InformationOrganization | 63.8 75.4 58.7      | 70.1 57.7        | 70.1 |
| 5-shot   | SQL-OnlyOrganization         | 58.9 74.4 49.2      | 71.3 45.3        | 66.1 |
|          | DAILOrganization             | 60.0 75.0 55.3      | 69.3 51.4        | 65.2 |
|          | SQL-OnlyOrganization         | 59.6 74.6 50.0      | 70.1 49.0        | 69.3 |
7-shot
|     | DAILOrganization     | 63.6 75.8 57.1 | 67.9 51.6 | 64.0 |
| --- | -------------------- | -------------- | --------- | ---- |
|     | SQL-OnlyOrganization | 60.0 75.6 49.8 | 70.9 48.8 | 68.7 |
9-shot
|     | DAILOrganization | 63.8 76.0 57.5 | 67.9 53.7 | 65.2 |
| --- | ---------------- | -------------- | --------- | ---- |
Table11:DetailsofFew-shotevaluationonSpider-Realisticdatasetwithdifferentorganizations.
D SUPERVISEDFINE-TUNINGFORTEXT-TO-SQL
D.1 DetailedPerformanceofOpen-sourceLLMsonSpider-Realistic
ThenumericalresultsareshowninTable13.
D.2 DetailedPerformanceofOpen-sourceLLMsonSpider-devinFew-shotScenario
ThenumericalresultsareshowninTable14.
D.3 ExperimentsinFew-shotScenarioforDifferentModelSizesandTrainingCorpusofOpen-source
LLMs
We also evaluate the LLaMA-2-CHAT-70B, Falcon-40B, CodeLLaMA-34B and Vicuna-33B in few-shot scenario, and summarize their
performanceinTable15.Similarwiththesituationinzero-shotscenario,LLaMA-2-CHAT-70outperformsVicuna-33Bwith59.0%execution
accuracy,whereasFalcon-40Breachesonly19.1%thatisoverwhelmedbyCodeLLaMA-34B.Andagain,CodeLLaMA-34Boutperforms
LLaMA-2-CHAT-70Bby12.4%inthefew-shotscenario.Thisfurtherconfirmsthathavingmoreparametersisbeneficial,meanwhile,these
resultsalsounderscorethecriticalimportanceofthetrainingcorpus.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
|     | Classification | Method      |     |     |     | Dev.EX(%) |     | TestEX(%) |     |
| --- | -------------- | ----------- | --- | --- | --- | --------- | --- | --------- | --- |
|     |                | Duoquest[4] |     |     |     | 63.5      |     | 63.5      |     |
rule-based
|     |     | ATHENA++[44]      |     |     |     | 78.82 |     | -    |     |
| --- | --- | ----------------- | --- | --- | --- | ----- | --- | ---- | --- |
|     |     | ValueNet[5]       |     |     |     | 67.0  |     | -    |     |
|     |     | BRIDGEv2+BERT[25] |     |     |     | 68.0  |     | 64.3 |     |
|     |     | T5-Base[43]       |     |     |     | 57.9  |     | -    |     |
|     |     | T5-Large[43]      |     |     |     | 67.2  |     | -    |     |
PLM-based
|     |     | T5-3B[43]                |     |     |     | 74.4 |     | 70.1 |     |
| --- | --- | ------------------------ | --- | --- | --- | ---- | --- | ---- | --- |
|     |     | T5-3B+PICARD[43]         |     |     |     | 79.3 |     | 75.1 |     |
|     |     | RESDSQL-3B+NatSQL[23]    |     |     |     | 84.1 |     | 79.9 |     |
|     |     | Fine-tunedBERT(ours)     |     |     |     | 53.6 |     | -    |     |
|     |     | C3+ChatGPT+Zero-Shot[13] |     |     |     | 81.8 |     | 82.3 |     |
|     |     | DIN-SQL+GPT-4[37]        |     |     |     | 82.8 |     | 85.3 |     |
LLM-based
|     |     | DAIL-SQL+GPT-4                  |     |     |     | 83.1 |     | 86.2 |     |
| --- | --- | ------------------------------- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     | DAIL-SQL+GPT-4+Self-consistency |     |     |     | 83.6 |     | 86.6 |     |
Table12:Reportedexecutionaccuracy(EX)ofvarioussolutionsondevelopmentset(Dev.)andtestset(Test)ofSpider,including
LLM-based,PLM-based,andrule-basedapproaches.
|       |          |     | BS       | TR      | OD  |         | CR   | AS Average  |     |
| ----- | -------- | --- | -------- | ------- | --- | ------- | ---- | ----------- | --- |
| Stage | LLM      |     | 𝑃        | 𝑃       | 𝑃   |         | 𝑃    | 𝑃           |     |
|       |          |     | EM EX EM | EX      | EM  | EX EM   | EX   | EM EX EM    | EX  |
|       | LLaMA-7B |     | 4.7 12.0 | 1.4 4.9 | 1.4 | 5.1 3.1 | 13.0 | 0.2 2.8 2.2 | 7.6 |
Pre-training LLaMA-13B 5.9 15.7 3.3 13.6 4.3 17.9 2.4 20.3 3.1 13.8 3.8 16.3
LLaMA-33B 7.1 17.5 8.3 21.5 9.6 28.3 7.9 34.6 10.8 25.2 8.7 25.4
Alpaca-7B 7.7 22.8 9.6 19.3 11.4 21.7 12.8 26.0 0.8 6.9 8.5 19.3
GPT4ALL-7B 3.5 12.6 7.7 19.3 6.1 18.5 7.5 17.1 1.4 6.5 5.2 14.8
LLaMA-2-CHAT-7B 11.4 21.7 5.1 12.0 7.5 14.4 7.5 17.7 3.7 13.6 7.0 15.9
Aligned LLaMA-2-CHAT-13B 14.4 25.8 12.8 26.4 11.6 22.0 17.9 32.9 15.9 28.3 14.5 27.1
Vicuna-7B 6.7 18.3 0.8 8.1 4.7 16.3 3.9 14.0 0.6 4.9 3.3 12.3
Vicuna-13B 6.9 19.3 4.9 16.1 8.5 25.2 4.3 27.6 4.1 15.0 5.7 20.6
Vicuna-33B 8.1 20.7 13.8 28.7 16.9 5.1 34.3 8.7 27.6 10.5 30.0
37.0
Table13:Zero-shotevaluationresultsonSpider-Realisticwithdifferentopen-sourceLLMs.
|     |                     |     |           | 0-shot |           | 1-shot | 3-shot | 5-shot         |     |
| --- | ------------------- | --- | --------- | ------ | --------- | ------ | ------ | -------------- | --- |
|     | ExampleOrganization |     | LLM       |        |           |        |        |                |     |
|     |                     |     |           | EM     | EX EM     | EX     | EM     | EX EM EX       |     |
|     |                     |     | LLaMA-33B | 12.2   | 42.8 24.0 | 42.5   | 28.2   | 45.7 31.3 46.8 |     |
SQL-OnlyOrganization
|     |     |     | Vicuna-33B | 6.9  | 43.7 13.3 | 46.7 | 17.1 | 49.5 19.5 49.5 |     |
| --- | --- | --- | ---------- | ---- | --------- | ---- | ---- | -------------- | --- |
|     |     |     | LLaMA-33B  | 12.2 | 42.8 28.5 | 46.4 | 34.9 | 47.9 34.5 45.8 |     |
DAILOrganization
|     |     |     | Vicuna-33B | 6.9  | 43.7 18.7 | 45.5 | 26.3 | 49.1 28.6 50.2 |     |
| --- | --- | --- | ---------- | ---- | --------- | ---- | ---- | -------------- | --- |
|     |     |     | LLaMA-33B  | 12.2 | 42.8 30.1 | 46.8 | 35.1 | 48.9 36.4 50.2 |     |
Full-InformationOrganization
|     |     |     | Vicuna-33B | 6.9 | 43.7 22.1 | 49.2 | 27.4 | 49.9 28.0 51.1 |     |
| --- | --- | --- | ---------- | --- | --------- | ---- | ---- | -------------- | --- |
Table14:Detailedperformanceofopen-sourceLLMsonSpider-devinfew-shotscenario.
D.4 DetailsforSupervisedFine-tuning
Fordataset,weusethetrainsplitinSpider,whichtotallycontains8659trainingsamples.Forhyper-parameters,wesetglobalbatchsize
as256,andsearchlearningratein[1𝑒−6,1𝑒−4]andweightdecayin{1,0.1,0.01,0}.Duringfine-tuning,weuseacosinelearningrate
schedulerintransformers[54]withawarmratio0.03.Besides,allLLMsarefine-tunedonaserverwitheight64GA100GPUs.
D.5 DetailedPerformanceofFine-tunedOpen-sourceLLMonSpiderandSpider-Realistic
ThenumericalresultsonSpider-devandSpider-RealisticareallshowninTable16.

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
LLM EM EX
LLaMA-2-CHAT-70B 42.9 59.0
Falcon-40B 4.8 19.1
CodeLLaMA-34B 59.9 71.4
Vicuna-33B 31.3 51.7
Table15:Performancesofdifferentopen-sourceLLMswithDAIL-SQL.
Spider Spider-Realistic
LLM Metric
BS TR OD CR AS Average BS TR OD CR AS Average
𝑃 𝑃 𝑃 𝑃 𝑃 𝑃 𝑃 𝑃 𝑃 𝑃
EM 44.5 60.6 60.0 63.9 59.8 57.8 33.3 45.5 43.9 51.6 46.5 44.2
LLaMA-7B
EX 49.3 63.2 63.4 66.7 64.7 61.5 35.0 48.8 47.4 53.7 46.5 46.3
EM 59.9 60.1 61.5 62.2 65.3 61.8 48.2 45.7 45.3 49.4 52.2 48.2
LLaMA-2-CHAT-7B
EX 62.9 62.9 64.2 65.7 69.6 65.1 51.4 44.5 47.4 49.6 54.9 49.6
EM 48.5 62.1 57.7 62.7 65.1 59.2 39.0 50.4 48.2 48.2 52.2 47.6
LLaMA-13B
EX 53.0 66.0 61.7 67.0 68.6 63.3 44.7 54.1 51.6 52.6 54.7 51.5
EM 62.8 59.0 60.9 60.8 63.8 61.5 53.7 47.0 47.2 49.6 53.7 50.2
LLaMA-2-CHAT-13B
EX 64.9 61.1 63.1 63.8 65.1 63.6 54.5 47.6 48.6 51.2 52.8 50.9
Table16:Performanceofsupervisedfine-tuningonSpiderandSpider-Realisticwithrespecttodifferentrepresentationsand
LLMs.
E EFFICIENCY
E.1 FinancialEfficiency
WeestimatethefinancialexpensesforeachexperimentwithGPT-4andGPT-3.5-TURBObasedontheAPIpricereportedonNovember8,
2023,asillustratedinFigure9.Thetotalcostsamountto323.2$and12.0$forGPT-4andGPT-3.5-TURBO,respectively.
84
82
80
78
76
74
72
5 10 15 20 25 30
Cost ($)
)%(
.ccA
noitucexE
80 83.5
78
76
74 BS AS FI
P P O
TR P zero-shot SO O 72
OD P FK DAIL O 70
CR P RI 68
0.2 0.4 0.6 0.8 1.0
Cost ($)
(a)GPT-4
)%(
.ccA
noitucexE
78.4 79.0 78.1
BS AS FI
P P O
TR P zero-shot SO O
OD P FK DAIL O
CR P RI
(b)GPT-3.5-TURBO
Figure9:PriceofAPIcallingtoinferencequestionsonSpider-devforGPT-4andGPT-3.5-TURBO.Weutilizedifferentcolorsto
representdifferentquestionrepresentationsanddifferentshapestodenotedifferentexampleorganizationsaswellasthe
usageofforeignkeyinformationandruleimplication.Inparticular,theoverlapofshapesisusedtoindicatetheusageofboth
foreignkeyinformationandruleimplication.Theringsstandforthepromptsinzero-shotscenario.
E.2 Time-Consuming
WeestimatethecostofourexperimentsontheVicuna-33Bmodel,asshowninFigure10.UnlikethecostofAPIcalling,thenumberof
outputtokensalsoplaysasignificantroleinthetimeconsumptionofVicuna-33Bduringlocalinference.Forinstance,usingtheOpenAI
DemostrationPrompt(OD )tendstoelicitmoretime-consumingexplanationsaccompaniedbySQLqueries.Notethattheimplication
𝑃
ruleof“withnoexplanation"notonlyimprovesperformancebutalsosavestimebysuppressingVicuna-33Bfromgeneratingunnecessary
explanations,asdemonstratedinFigure10.TheaveragecostofGPUhoursis54.4hoursineachexperiment.

Text-to-SQLEmpoweredbyLargeLanguageModels:ABenchmarkEvaluation
70
)%( .ccA noitucexE 50
60
)h( ruoH UPG
| 45  |     | 50  |     |     |     |
| --- | --- | --- | --- | --- | --- |
40
|                 | BS AS          | FI 40   |                 | BS AS          | FI   |
| --------------- | -------------- | ------- | --------------- | -------------- | ---- |
|                 | P P            | O       |                 | P P            | O    |
| 35              | TR P zero-shot | SO O 30 |                 | TR P zero-shot | SO O |
|                 | OD FK          | DAIL    |                 | OD FK          | DAIL |
| 30              | P              | O       |                 | P              | O    |
|                 | CR RI          | 20      |                 | CR RI          |      |
|                 | P              |         |                 | P              |      |
| 25              |                | 10      |                 |                |      |
| 300 600         | 900 1200       | 1500    | 300 600         | 900 1200       | 1500 |
| Avg. Token Num. |                |         | Avg. Token Num. |                |      |
(a) Averagedtokennumberofeachpromptandtheircorrespondingperformanceon (b)Averagedtokennumberofeachpromptandtheirtime-consumingonSpider-dev.
Spider-dev.
Figure10:ThecostofourexperimentswithVicuna-33B.
F LEADERBOARD
F.1 SpiderLeaderboard
Fig.11showstheperformancerankinSpider[57]leaderboardonSep19,2023.Intheleaderboard,oursolutionDAIL-SQLwithGPT-4is
reportedtoachieve86.2%executionaccuracy;further,withself-consistency,oursolutionachieves86.6%executionaccuracy,rankedasthe
firstplace.
Figure11:CurrentperformancerankinSpiderleaderboard.(Lastaccessedon2023-09-19.)

DaweiGao∗,HaibinWang∗,YaliangLi,XiuyuSun,YichenQian,BolinDing,andJingrenZhou
F.2 BIRDLeaderboard
Fig.12showstheperformancerankinBIRD[24]leaderboardonNov09,2023.WecanobservethatontheBIRDBenchmark,DAIL-SQLalso
outperformsthepreviousstate-of-the-artmethod,DIN-SQL,byaremarkable4.04%inBIRDdevsetand1.51%inBIRDtestsetintermsof
executionaccuracy.
However,theadditionalchallengeofBIRDliesineffectivelyleveragingthespecificdomainknowledgeofferedbythedataset.Asshown
inFigure12,thetop-1andtop-2solutionshaveaSFTprocedure,whileDAIL-SQLhavenosuchprocedureandrequiresfurtherdesignto
incorporateextraknowledgeforamorefaircomparison.
Figure12:TheleaderboardofBIRDatexcutionaccuracy(EX).