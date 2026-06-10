Towards Robustness of Text-to-SQL Models Against Natural and Realistic
|     |     |     |     | Adversarial |     | Table | Perturbation |     |     |     |     |     |
| --- | --- | --- | --- | ----------- | --- | ----- | ------------ | --- | --- | --- | --- | --- |
XinyuPi1∗,BingWang2∗,YanGao3,JiaqiGuo4,ZhoujunLi2,Jian-GuangLou3
1 UniversityofIllinoisUrbana-Champaign,Urbana,USA,
2 StateKeyLabofSoftwareDevelopmentEnvironment,BeihangUniversity
3 MicrosoftResearchAsia
4
Xi’anJiaotongUniversity,Xi’an,China
|     |     |                                | xinyupi2@illinois.edu; |     |     | {bingwang, |           | lizj}@buaa.edu.cn |                     |     |     |     |
| --- | --- | ------------------------------ | ---------------------- | --- | --- | ---------- | --------- | ----------------- | ------------------- | --- | --- | --- |
|     |     | jasperguo2013@stu.xjtu.edu.cn; |                        |     |     |            | {yan.gao, |                   | jlou}@microsoft.com |     |     |     |
|     |     |                                | Abstract               |     |     |            |           | Original Table    |                     |     |     |     |
Student
|     |     |     |     |     |     |     |     |     | Citizenship |     | Score Semester |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------------- | --- |
Name
|     | TherobustnessofText-to-SQLparsersagainst |     |     |     |     |     |     |     | A Country X |     | 92 Fall |     |
| --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | --- |
Student
adversarialperturbationsplaysacrucialrolein NBationalitCyountrSy cYore Se9m0ester Spring
Name
| 2202 ceD 02  ]LC.sc[  1v49990.2122:viXra | delivering | highly | reliable | applications. | Previ- |     |     |     |                       |     |        |     |
| ---------------------------------------- | ---------- | ------ | -------- | ------------- | ------ | --- | --- | --- | --------------------- | --- | ------ | --- |
|                                          |            |        |          |               |        |     |     | A   | ACountry XCountry X92 |     | 89Fall |     |
ous studies along this line primarily focused St B udent  CBCitoizuenntrsyh YiCpounStrcyo Y9re0 Seme8S5pstreinrg Instru F c a t ll or  Grade
|     |                  |     |        |                  |       |     |      | Name |                                  |     | Name                 |     |
| --- | ---------------- | --- | ------ | ---------------- | ----- | --- | ---- | ---- | -------------------------------- | --- | -------------------- | --- |
|     | on perturbations |     | in the | natural language | ques- |     |      |      |                                  |     |                      |     |
|     |                  |     |        |                  |       |     | e lb | AA   | CCCoouunnttrryy  XXCountr9y 2Z89 |     | Fa9Sl7plring DSpring | 6   |
tion side, neglecting the variability of tables. a T BB CCoouunnttrryy  YY 9085 SprinFgall E 6
 d
Motivatedbythis,weproposetheAdversarial e CA CCoouunnttrryy  XZ 8997 SprSinpgring E 6
b ru
Table Perturbation (ATP) as a new attacking B Country Y 85 Fall D 5
tre
|     |          |            |     |                |          |     | P e    | C   | Country Z | 97  | Spring F | 5   |
| --- | -------- | ---------- | --- | -------------- | -------- | --- | ------ | --- | --------- | --- | -------- | --- |
|     | paradigm | to measure |     | the robustness | of Text- |     |  LP lb |     |           |     |          |     |
a
to-SQL models. Following this proposition, R T List namesandcitizenshipsof studentswho
 d
|     |           |         |     |                      |       |     | e b | achieved top 3 scores. |     |     |     |     |
| --- | --------- | ------- | --- | -------------------- | ----- | --- | --- | ---------------------- | --- | --- | --- | --- |
|     | we curate | ADVETA, |     | the first robustness | eval- |     | ru  |                        |     |     |     |     |
tre
uation benchmark featuring natural and real- SELECT Student Name, Citizenship FROM Student
|     |             |     |        |                  |      |     | P   | ORDER BY Score desc LIMIT 3 |     |     |     |     |
| --- | ----------- | --- | ------ | ---------------- | ---- | --- | --- | --------------------------- | --- | --- | --- | --- |
|     | istic ATPs. | All | tested | state-of-the-art | mod- |     |  D  |                             |     |     |     |     |
D
A
elsexperiencedramaticperformancedropson SELECT Student Name FROM Student
|     |         |           |         |               |     |     |     | ORDER BY Score desc LIMIT 3 |     |     | (Missing Nationality) |     |
| --- | ------- | --------- | ------- | ------------- | --- | --- | --- | --------------------------- | --- | --- | --------------------- | --- |
|     | ADVETA, | revealing | models’ | vulnerability | in  |     |     |                             |     |     |                       |     |
real-world practices. To defend against ATP, SELECT Student Name, Instructor Name, Citizenship
we build a systematic adversarial training ex- FROM Student ORDER BY Gradedesc LIMIT 3
|     | ample generation      |     | framework | tailored      | for bet- |     |                               |                |          |     |                   |         |
| --- | --------------------- | --- | --------- | ------------- | -------- | --- | ----------------------------- | -------------- | -------- | --- | ----------------- | ------- |
|     |                       |     |           |               |          |     | Figure                        | 1: Adversarial | examples |     | based on table    | pertur- |
|     | ter contextualization |     | of        | tabular data. | Experi-  |     |                               |                |          |     |                   |         |
|     |                       |     |           |               |          |     | bationsforaText-to-SQLparser. |                |          |     | LeavingtheNLques- |         |
mentsshowthatourapproachnotonlybrings
|     |     |     |     |     |     |     | tion | unchanged, | both replacement |     | of column | names |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---------- | ---------------- | --- | --------- | ----- |
thebestrobustnessimprovementagainsttable-
|     |                    |     |     |                    |     |     | (e.g., | replace | “Citizenship” | with | “Nationality”) | and |
| --- | ------------------ | --- | --- | ------------------ | --- | --- | ------ | ------- | ------------- | ---- | -------------- | --- |
|     | side perturbations |     | but | also substantially | em- |     |        |         |               |      |                |     |
powers models against NL-side perturbations. addition of associated columns (e.g., add “Instructor
|     |            |     |           |     |          |     | Name” | basedon | “Student | Name”; | add “Grade” | based |
| --- | ---------- | --- | --------- | --- | -------- | --- | ----- | ------- | -------- | ------ | ----------- | ----- |
|     | We release | our | benchmark | and | code at: |     |       |         |          |        |             |       |
on“Score”)misleadtheparsertoincorrectpredictions.
https://github.com/microsoft/ContextualSP.
1 Introduction
questionwhilekeepingitsmeaningunchanged,and
The goal of Text-to-SQL is to generate an exe- observedasignificantperformancedropofaText-
cutableSQLquerygivenanaturallanguage(NL) to-SQL parser. Gan et al. (2021) also observed
question and corresponding tables as inputs. By a dramatic performance drop when the schema-
helping non-experts interact with ever-growing relatedtokensinquestionsarereplacedwithsyn-
databases,thistaskhasmanypotentialapplications onyms. Theyinvestigatedbothmulti-annotations
inreallife,therebyreceivingconsiderableinterest for schema items and adversarial training to im-
frombothindustryandacademia(LiandJagadish,
proveparsers’robustnessagainstpermutationsin
2016;Zhongetal.,2017;Affolteretal.,2019). NLquestions. However,previousworksonlystud-
Recently, existing Text-to-SQL parsers have iedtherobustnessofparsersfromtheperspective
beenfoundvulnerabletoperturbationsinNLques- of NL questions, neglecting variability from the
tions (Gan et al., 2021; Zeng et al., 2020; Deng othersideofparserinput–tables.
et al., 2021). For example, Deng et al. (2021) re- Wearguethatareliableparsershouldalsobe
movedtheexplicitmentionsofdatabaseitemsina robust against table-side perturbations since they
∗EqualcontributionsduringtheinternshipatMicrosoft areinevitablymodifiedinthehuman-machinein-
|     |     |     |     |     |     |     | teractionprocess. |     | Inbusinessscenarios,tablemain- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------------------------ | --- | --- | --- |
ResearchAsia.

tainersmay(i)renamecolumnsduetobusinessde- • We design CTA, a systematic adversarial
mandsanduserpreferences. (ii)addnewcolumns training example generation framework tai-
intoexistingtableswhenbusinessdemandschange. lored for better contextualization of tabular
Consequently, the extra lexicon diversity intro- data. Experiments show that our approach
duced by such modifications could harm perfor- brings model best robustness gain and low-
mances of unrobust Text-to-SQL parsers. To for- estoriginalperformanceloss,comparedwith
malizethesescenarios,weproposeanewattacking various baselines. Moreover, we show that
paradigm,AdversarialTablePerturbation(ATP), adversarialrobustnessbroughtbyCTAgener-
tomeasureparsers’robustnessagainstnaturaland alizeswelltoNL-sideperturbations.
| realisticATPs. | Inaccordancewiththetwoscenar- |     |     |     |     |     |     |
| -------------- | ----------------------------- | --- | --- | --- | --- | --- | --- |
2 AdversarialTablePerturbation
iosabove,weconsiderbothREPLACE(RPL)and
| ADDperturbationsinthiswork. |     |     | Figure1conveys |            |                 |                    |     |
| --------------------------- | --- | --- | -------------- | ---------- | --------------- | ------------------ | --- |
|                             |     |     |                | We propose | the Adversarial | Table Perturbation |     |
anintuitiveunderstandingofATP. (ATP)paradigmtomeasurerobustnessofText-to-
Ideally,ATPshouldbeconductedbasedontwo SQLmodels. Foraninputtableanditsassociated
criteria: (i)Humanexpertsconsistentlywritecor- NL questions, the goal of ATP is to fool Text-to-
rect SQL queries before and after table perturba- SQLparsersbyperturbingtablesnaturallyandre-
tions,yetparsersfail;(ii)Perturbedtableslooknat- alistically. Morespecifically,humanSQLexperts
uralandgrammatical,andarefreefrombreakage canconsistentlymaintaintheircorrecttranslations
| ofhumanlanguageconventions. |     |     | Accordingly,we |     |     |     |     |
| --------------------------- | --- | --- | -------------- | --- | --- | --- | --- |
fromNLquestionstoSQLwiththeirunderstand-
carefullydesignprinciplesforRPL/ADDandman- ingoflanguageandtablecontext. Formally,ATP
uallycuratetheADVErsarialTableperturbAtion consistsoftwoapproaches: REPLACE(RPL)and
(ADVETA) benchmark based on three existing ADD. In the rest of this section, we first discuss
datasets. Allevaluatedstate-of-the-artText-to-SQL ourconsiderationoftablecontext,thenintroduce
models experience drastic performance drops on conductionprinciplesofRPLandADD.
ADVETA:OnADVETA-RPL,theaveragerelative
|            |      |               |                | 2.1 TableContext |     |     |     |
| ---------- | ---- | ------------- | -------------- | ---------------- | --- | --- | --- |
| percentage | drop | is as high as | 53.1%, whereas | on               |     |     |     |
ADVETA-ADDis25.6%,revealingmodels’lack Tables consist of explicit and implicit elements –
ofrobustnessagainstATPs. botharenecessaryforunderstandingtablecontext.
“Explicitelements”refertotablecaptions,columns,
Empirically,modelrobustnesscanbeimproved
by adversarial training, i.e. re-train models with and cell values. “Implicit elements”, in our con-
training set augmented with adversarial exam- sideration, contains Table Primary Entity (TPE)
ples (Jin et al., 2020). However, due to the dif- and domain. (Relational) Tables are structured
ferent natures of structured tables and unstruc- datarecordingdomain-specificattributes(columns)
turedtext,well-establishedtextadversarialexam- aroundsomecentralentities(TPE)(Sumathiand
ple generation approaches are not readily appli- Esakkirajan,2007). Withouttheexplicitannotation,
cable. Motivated by this, we propose an effec- humanscouldstillmakecorrectguessesonthem.
tive Contextualized Table Augmentation (CTA) Forexample,it’sintuitivethattablesinFigure1can
approach that better leverages tabular context in- beclassifiedas“education”domain,andallofthe
formation and carries out ablation analysis. To columns center around the TPE “student”. Com-
summarize,thecontributionsofourworkarethree- biningbothexplicitandimplicitelements,people
| fold: |     |     |     | achieveanunderstandingoftablecontext, |     |     | which |
| ----- | --- | --- | --- | ------------------------------------- | --- | --- | ----- |
becomesthesourceoflexicondiversityincolumn
| • To | the best | of our knowledge, | we are | the |     |     |     |
| ---- | -------- | ----------------- | ------ | --- | --- | --- | --- |
descriptions.
| first       | to propose | definitions        | and principles | of                         |     |     |     |
| ----------- | ---------- | ------------------ | -------------- | -------------------------- | --- | --- | --- |
| Adversarial |            | Table Perturbation | (ATP)          | as a                       |     |     |     |
|             |            |                    |                | 2.2 REPLACE(RPL)Principles |     |     |     |
newattackingparadigmforText-to-SQL.
Givenatargetcolumn,thegoalofRPListoseek
• WecontributeADVETA,thefirstbenchmark an alternative column name that makes sense to
to evaluate the robustness of Text-to-SQL humansbutmisleadsunrobustmodels. GoldSQL,
models. Significant performance drops of as illustrated in Figure 1, should be correspond-
state-of-the-art models reveals that there is inglyadaptedbymappingtheoriginalcolumnto
much more to explore beyond high leader- its new name. In light of this, RPL should fulfill
| boardscores. |     |     |     | thefollowingtwoprinciples: |     |     |     |
| ------------ | --- | --- | --- | -------------------------- | --- | --- | --- |

|     |     |                  |     |     |       | Spider |     |       | WTQ |           | WikiSQL |     |     |
| --- | --- | ---------------- | --- | --- | ----- | ------ | --- | ----- | --- | --------- | ------- | --- | --- |
|     |     | ADVETAStatistics |     |     | Orig. | RPL    | ADD | Orig. | RPL | ADD Orig. | RPL     | ADD |     |
BasicStatistics
|     | #Totaltables         |     |     |     |      | 81 81 | 81  | 327  | 327 | 327 2,716 | 2,716 | 2,716 |     |
| --- | -------------------- | --- | --- | --- | ---- | ----- | --- | ---- | --- | --------- | ----- | ----- | --- |
|     | #Avg.columnspertable |     |     |     | 5.45 | –     | –   | 6.31 | –   | – 6.41    |       | –     | –   |
#Avg.perturbedcolumnspertable – 2.62 3.64 – 2.65 3.27 – 3.70 4.44
|     | #Avg.candidatespercolumn |     |     |     |     | – 3.33 | 3.97 | –   | 2.90 | 3.55 | – 3.32 | 3.97 |     |
| --- | ------------------------ | --- | --- | --- | --- | ------ | ---- | --- | ---- | ---- | ------ | ---- | --- |
#Uniquecolumns 211 911 1,061 527 1,656 2,976 2,414 10,787 10,474
|     | #Uniquevocab |     |     |     | 199 | 598 | 782 | 596 | 1,156 | 1,459 2,414 | 4,147 | 5,099 |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | ----- | ----------- | ----- | ----- | --- |
AnalyticalStatistics
#Uniquesemanticmeanings 144 144 683 156∗ 156∗ 702∗ 203∗ 203∗ 818∗
#Avg.colnamepersemanticmeaning 1.35 6.33 1.55 1.59∗ 5.87∗ 1.64∗ 1.67∗ 6.12∗ 1.52∗
Table1: ADVETAstatisticscomparisonbetweenoriginalandRPL/ADD-perturbeddevset. The∗ markdenotes
thatresultsarebasedonatmost100randomlysampledtablesandobtainedbymanualcount.
| Semantic |     | Equivalency: |     |     |     |     |     |     |     |     |     |     |     |
| -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Under the table con- columns should be irreplaceable with any origi-
textoftargetcolumn,substitutedcolumnnamesare naltablecolumns. Inotherwords,ADDrequires
expected to convey equivalent semantic meaning semanticequivalencytobefilteredoutfromhighly
astheoriginalname. semanticassociations. Otherwise,theoriginalgold
PhraseologyCorrectness: ATPaimstobenat- SQL will not be the single correct output, which
ural and realistic and does not target worst-case makestheperturbationunreasonable.
| attacks. | Therefore, |     | replaced |     | column | names | are |     |     |     |     |     |     |
| -------- | ---------- | --- | -------- | --- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- |
3 ADVETABenchmark
expectedtofollowlinguisticphraseologyconven-
| tions: | (i) Grammar |             | Correctness: |           | Substituted |         | col- |             |     |                                 |             |              |          |
| ------ | ----------- | ----------- | ------------ | --------- | ----------- | ------- | ---- | ----------- | --- | ------------------------------- | ----------- | ------------ | -------- |
|        |             |             |              |           |             |         |      | Following   | RPL | and ADD                         | principles, |              | we manu- |
| umn    | names       | should      | be           | free from | grammar     | errors. |      |             |     |                                 |             |              |          |
|        |             |             |              |           |             |         |      | ally curate | the | ADVErsarial                     | Table       | perturbAtion |          |
| (ii)   | Proper      | Collocation |              | with      | TPE: New    | column  |      |             |     |                                 |             |              |          |
|        |             |             |              |           |             |         |      | (ADVETA)    |     | benchmarkbasedonthreemainstream |             |              |          |
namesshouldcollocateproperlywithTPE.Forex-
|     |     |     |     |     |     |     |     | Text-to-SQL |     | datasets, | Spider | (Yu et | al., 2018), |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --------- | ------ | ------ | ----------- |
ample,heightandtallnessbothcollocatewellwith
|                                            |     |                               |     |     |     |     |       | WikiSQL | (Zhong      | et al., | 2017)      | and WTQ | (Paper-    |
| ------------------------------------------ | --- | ----------------------------- | --- | --- | --- | --- | ----- | ------- | ----------- | ------- | ---------- | ------- | ---------- |
| student(TPE),butconventionallynotaltitude. |     |                               |     |     |     |     | (iii) |         |             |         |            |         |            |
|                                            |     |                               |     |     |     |     |       | not et  | al., 2017). | For     | each table | from    | the origi- |
| Idiomaticity:                              |     | Newcolumnnamesshouldsoundnat- |     |     |     |     |       |         |             |         |            |         |            |
naldevelopmentset,weconductRPL/ADDanno-
uraltoanativespeakertoaddresstargetcolumns.
|     |     |     |     |     |     |     |     | tation | separately, | perturbing | only | table | columns. |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----------- | ---------- | ---- | ----- | -------- |
Forexample,runner-upmeanssecondplace,and
ForitsassociatedNL-SQLpairs,weleavetheNL
| racer-up | is  | a bad | replacement |     | despite | runner | is  |     |     |     |     |     |     |
| -------- | --- | ----- | ----------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
questionsunchangedandadaptgoldSQLsaccord-
synonymoustoracer.
|     |               |     |     |     |     |     |     | ingly.                                | As a | result, ADVETA |     | consists | of 3 (Spi- |
| --- | ------------- | --- | --- | --- | --- | --- | --- | ------------------------------------- | ---- | -------------- | --- | -------- | ---------- |
| 2.3 | ADDPrinciples |     |     |     |     |     |     | der/WTQ/WikiSQL)∗2(RPL/ADD)=6subsets. |      |                |     |          |            |
Wenextintroduceannotationdetailsandcharacter-
| ADD | perturbs |     | tables with | introductions |     | of  | new |     |     |     |     |     |     |
| --- | -------- | --- | ----------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
isticsofADVETA.
| columns. |     | Insteadofaddingrandomcolumnsthat |     |     |     |     |     |     |     |     |     |     |     |
| -------- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fitwellintothetabledomain, wepertinentlyadd 3.1 AnnotationSteps
adversarialcolumnswithrespecttoatargetcolumn
|     |          |     |             |             |     |      |     | Fivevendorsjointheannotationprocess. |     |     |     |     | Eachbase |
| --- | -------- | --- | ----------- | ----------- | --- | ---- | --- | ------------------------------------ | --- | --- | --- | --- | -------- |
| for | the sake | of  | adversarial | efficiency. |     | Gold | SQL |                                      |     |     |     |     |          |
devsetissplitintosmallchunksandismanually
shouldremainunchangedafterADDperturbations
annotatedbyonevendorandreviewedbyanother,
1. BelowstatesADDprinciples:
withaninter-annotatoragreementtoresolveanno-
| Semantic-association |     |     |     | &   | Domain-relevancy: |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tationinconsistency.
Givenatargetcolumnanditstablecontext,newly
|     |     |     |     |     |     |     |     | Beforeannotation, |     |     | vendorsarefirsttrainedto |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | ------------------------ | --- | --- |
addedcolumnsareexpectedto(i)fitnicelyintothe
understandtablecontextasdescribedin§2,then
tablecontext;(ii)havehighsemanticassociations
arefurtherinstructedofthefollowingdetails.
| with | the target |     | column | yet low | semantic | equiva- |     |     |     |     |     |     |     |
| ---- | ---------- | --- | ------ | ------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
RPL:RPLprinciplesarethemandatoryrequire-
| lency(e.g.  |     | salesvs. | profits,editorvs. |     | author). |         |     |        |                   |         |                |          |            |
| ----------- | --- | -------- | ----------------- | --- | -------- | ------- | --- | ------ | ----------------- | ------- | -------------- | -------- | ---------- |
|             |     |          |                   |     |          |         |     | ments. | Duringannotation, |         | vendors        | aregiven | full       |
| Phraseology |     |          | Correctness:      |     | Same     | as RPL, |     |        |                   |         |                |          |            |
|             |     |          |                   |     |          |         |     | Google | access            | to ease | the conception |          | of synony- |
columnsshouldobeyhumanlanguageconventions.
|                   |     |     |     |        |      |           |     | mousnamesforatargetcolumn.       |     |     |     | ADD:ADDprin- |     |
| ----------------- | --- | --- | --- | ------ | ---- | --------- | --- | -------------------------------- | --- | --- | --- | ------------ | --- |
| Irreplaceability: |     |     |     | Unlike | RPL, | any added |     |                                  |     |     |     |              |     |
|                   |     |     |     |        |      |           |     | cipleswillbetheprimaryguideline. |     |     |     | Unlikefree-  |     |
styleRPLannotations,vendorsareprovidedwith
1WeomitcellvaluealignmentinADDforsimplicity.

Template:{TPE} {Col Name} ({ColType})
|     |     |     | Primary Entity Predictor |     |     |           |     |     |     |     | Final DecisionMaker |          |     |
| --- | --- | --- | ------------------------ | --- | --- | --------- | --- | --- | --- | --- | ------------------- | -------- | --- |
|     |     |     |                          |     |     | “Student” |     |     |     |     |                     | NLIModel |     |
NLI Model
Target
|                                   |                      |         |                      |                    | Dictionary              | Candidate Column Names |         |                           |                |                     |                            |                 |          |
| --------------------------------- | -------------------- | ------- | -------------------- | ------------------ | ----------------------- | ---------------------- | ------- | ------------------------- | -------------- | ------------------- | -------------------------- | --------------- | -------- |
| S tu d e nt                       |                      |         |                      |                    | Matching                |                        |         | P r e m                   | i s e          | H y p o th          | e s is e                   | 1 e             | 2        |
| N a m e C it iz e                 | n s h ip Sc o re Sem | e s ter |                      |                    |                         | Acade mi               | c Year  |                           |                |                     |                            |                 |          |
|                                   |                      |         |                      |                    |                         |                        |         | Stud e n t  s             | e m ester      | Stude nt   a c a    | d e m ic year 0            | .6 5 0          | .8 5 RPL |
| A C o u n                         | tr y  X 9 2 Fa       | l l     |                      |                    |                         | …                      | .       | ( T e x                   | t ) .          | (T e                | x t ) .                    |                 |          |
|                                   |                      |         |                      | Synonym Dictionary |                         |                        |         | Student semester          |                | Student school term |                            |                 |          |
| B Country Y                       | 89 Spring            |         |                      |                    |                         | Enroll Year            |         |                           |                |                     | 0.94                       | 0.71            | RPL      |
|                                   |                      |         |                      |                    | Contextualization       |                        |         | (Text).                   |                | (Text).             |                            |                 |          |
|                                   |                      |         |                      |                    |                         | School Term            |         | Student semester          |                | Student season      |                            |                 |          |
|                                   |                      |         |                      |                    | Matching                |                        |         | (Text).                   |                | (Text).             | 0.35                       | 0.55            | ADD      |
| Caption: School Scores Statistics |                      |         |                      | Reranker           |                         | Age                    |         |                           |                |                     |                            |                 |          |
|                                   |                      |         |                      | Number-batch       | (Top 20 )               |                        |         | Stude n t  s              | e m ester      | Stu d e n           | t   a ge 0.05              | 0.21            |          |
| Student from country Y?           |                      |         |                      |                    |                         | …                      |         | ( T e x                   | t) .           | ( T e               | x t ) .                    |                 | ADD      |
| Students with score > 90?         |                      |         |                      |                    | Column Names            |                        |         | …                         |                | …                   |                            |                 |          |
| Student A’s score?                |                      |         | Top K Similar Tables |                    |                         |                        |         |                           |                |                     |                            |                 |          |
|                                   |                      |         |                      | ... ...            | ... ...                 |                        |         |                           |                |                     |                            |                 |          |
|                                   |                      |         |                      |                    |                         |                        | S t u d | e nt C i t i z e n s h ip | S c o re S c h | o o l   T erm       | S t u d e nt C i t i z e n | s h ip S c o re | A g e    |
|                                   |                      |         |                      | Sc h o o l         | N a t i o n S e a s o n | M e d a l              | N a m   | e                         |                |                     | N a m e                    |                 |          |
Dense   R e t rieval T o m P P s y c h o l o g y 2 0 1 8 S c h o o l   S tu d e n A t C it iz C e o n u s n h t r i py   X Sc o r 9 e 2 A c a d e F m a i l c l   S tu d e eA n t C it iz C e o n u s nh t ri p y   X Sc o r e9 2 E n r o l 1 l 9
|     |     |     |     | CT oo m u r s e |  I D P T i t l e P s y Icn h s o0 t l r o u g c y to | r 2 0 1 T 8 e r m | N a m e |     | Y e | a r | N a m |     | Y e a r |
| --- | --- | --- | --- | --------------- | ---------------------------------------------------- | ----------------- | ------- | --- | --- | --- | ----- | --- | ------- |
T A P A S L il y F S ta t is t i c s 2 1 6 E n r o ll A B C o u C n o t ur y n   tX r y   Y 9 2 8 9 F Sa l pl r i n g A B C o u C n o t u r y n   tX r y   Y 9 2 8 9 2 0 1 8 2 1
|     |     |     |     | L il y T S o t mu d | e n t   ID F P A g eS tP a s t i y s Dc t i h ce o sp l oa | grt ym e 2n 0 t 1 2 6 0 1 8 Y e a r |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------------------- | ---------------------------------------------------------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Candidate Tables B C o u n t r y   Y 8 9 S p r i n g B C o u n t r y   Y 8 9 2 0 1 6
| WDC |     |     |     | Lily1 | 0 0 8 6 F 1 9 StaPti ssy t icc hs | o l o g y20162 0 1 8 |     |               |     |     |               |     |     |
| --- | --- | --- | --- | ----- | --------------------------------- | -------------------- | --- | ------------- | --- | --- | ------------- | --- | --- |
|     |     |     |     |       |                                   |                      |     | RPL Perturbed |     |     | ADD Perturbed |     |     |
|     |     |     |     | 1     | 2 3 1 9 2 1 S t a t               | is t i c s 2 0 1 6   |     |               |     |     |               |     |     |
Figure2:OverviewofourCTAframework.InrarecaseswhereTPEismissing,weapplyPrimaryEntityPredictor(addressed
inB.2).Otherwise,wesimplyuseannotatedTPE.e isobtainedwithpremise-hypothesisasinput;e withhypothesis-premise.
|     |     |     |     |     | 1   |     |     |     |     |     | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
alistof20candidatecolumnsfromwheretheyse- augmentedRPL/ADDlexicondistributionscloser
lect3-5basedonsemantic-association2 Noticethat tohuman-agreeableRPL/ADDdistributions. This
weonlyconsidercolumnsmentionedatleastonce requires maximization of lexicon diversity under
across NL questions to avoid vain efforts. In Ap- theconstraintsofdomainrelevancyandcleardiffer-
pendixA,Wedisplaysomerepresentativebench- entiationbetweensemanticassociation&semantic
markannotationcases. equivalency,asstatedinADDprinciplefrom§2.
Well-establishedtextadversarialexamplegen-
3.2 ADVETAStatisticsandAnalysis
erationapproaches,suchasTextFooler(Jinetal.,
| We present | comprehensive |     | benchmark |     | statistics |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
2020)andBertAttack(Lietal.,2020),mightfailto
| andanalysisresultsinTable1. |     |     |     | Noticethatwelimit |     |                           |     |     |     |     |                   |     |     |
| --------------------------- | --- | --- | --- | ----------------- | --- | ------------------------- | --- | --- | --- | --- | ----------------- | --- | --- |
|                             |     |     |     |                   |     | meetthisobjectivebecause: |     |     |     |     | (i)Theyrelyonsyn- |     |     |
the scope of statistics only to perturbed columns tacticinformation(e.g. POS-tag,dependency,se-
| (asmarkedby#Avg. |     | perturbedcolpertable). |     |     |     |                                          |     |     |     |     |     |     |      |
| ---------------- | --- | ---------------------- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | ---- |
|                  |     |                        |     |     |     | manticrole)toperformtexttransformations. |     |     |     |     |     |     | How- |
BasicStatisticsreflectselementaryinformation
ever,suchinformationisnotavailableinstructured
of ADVETA. Analytical Statistics illustrate high- tabulardata,leadingtopoor-qualityadversarialex-
lightedfeaturesofADVETAcomparedwithorig-
|               |                               |     |     |     |     | amples | generated |     | by  | these approaches. |     | (ii) | They |
| ------------- | ----------------------------- | --- | --- | --- | --- | ------ | --------- | --- | --- | ----------------- | --- | ---- | ---- |
| inaldev-sets: | (i)Diversecolumnnamesforasin- |     |     |     |     |        |           |     |     |                   |     |      |      |
performsequentialword-by-wordtransformations,
| gle semantic | meaning: |     | each table | from | the RPL |       |       |        |         |     |           |       |       |
| ------------ | -------- | --- | ---------- | ---- | ------- | ----- | ----- | ------ | ------- | --- | --------- | ----- | ----- |
|              |          |     |            |      |         | which | could | narrow | lexicon |     | diversity | (e.g. | writ- |
subsetcontainsapproximatelyfivetimesmorelexi- tenbywillnotbereplacedbyauthor). (iii)They
conswhichareusedtoexpressasinglesemantic
cannotleveragetabularcontexttoensuredomain
| meaning3. | (ii)Tableconceptrichness: |     |     |     | eachtable |            |     |      |                |     |         |             |     |
| --------- | ------------------------- | --- | --- | --- | --------- | ---------- | --- | ---- | -------------- | --- | ------- | ----------- | --- |
|           |                           |     |     |     |           | relevancy. |     | (iv) | They generally |     | fail to | distinguish |     |
fromADDsubsetcontainsroughlyfivetimesmore semantic equivalency from high semantic associ-
columnswithuniquesemanticmeanings.
|     |     |     |     |     |     | ation               | according |     | to our    | observations |     | (e.g., | fail to |
| --- | --- | --- | --- | --- | --- | ------------------- | --------- | --- | --------- | ------------ | --- | ------ | ------- |
|     |     |     |     |     |     | distinguishsalesvs. |           |     | profits). |              |     |        |         |
4 ContextualizedTableAugmentation
|     |     |     |     |     |     |     | To tackle | these | challenges, |     | we  | construct | the |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ----------- | --- | --- | --------- | --- |
In this section, we introduce our Contextualized CTAframework. Givenatargetcolumnfromata-
| Table Augmentation |     | (CTA) | framework |     | as an | ad- |     |     |     |     |     |     |     |
| ------------------ | --- | ----- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
blewithNLquestions,(i)adensetableretriever
versarialtrainingexamplegenerationapproachtai-
properlycontextualizestheinputtable,therebypin-
loredfortabulardata. Thephilosophyofadversar- pointing top-k most domain-related tables (and
| ialexamplegenerationisstraightforward: |     |     |     |     | Pushing |     |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
columns)fromalarge-scaledatabasewhileboost-
2Wegeneratethecandidatelistwitharetriever-reranker ing lexicon diversity. (ii) A reranker further
narrowsdownsemantic-associationandproduces
combofrom§4.
3Forexample,columnnames{Lastname,Familyname, coarse-grainedADD/RPLcandidates. (iii)NLIde-
Surname}expressasinglesemanticmeaning.Inpractice,we
cisionmakerdistinguishessemanticequivalency
randomsampleatmost100tablesfromeachsplit,andobtain
fromsemanticassociationandallocatescandidate
thenumberofuniquesemanticmeaningsbymanualcount.

columnstoRPL/ADDbuckets. Adetailedillustra- arealreadyguaranteed. Thefinalstageistodeter-
tionofourCTAframeworkisshowninFigure2. minewhichoneofRPL/ADDcandidatesismore
WenextintroduceeachcomponentofCTA. suitableforbasedonitssemanticequivalentagainst
|     |     |     |     |     |     | targetcolumn. | Therefore,weleverageRoBERTa- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | ---------------------------- | --- | --- | --- | --- | --- |
4.1 DenseRetrievalforSimilarTables MNLI(Liuetal.,2019;Williamsetal.,2017),the
|     |     |     |     |     |     | expertin | differentiatingsemanticequivalencyfrom |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | -------------------------------------- | --- | --- | --- | --- | --- |
Theentireframeworkstartswithadenseretrieval
|        |           |      |                |     |           | semantic | association4. |     | Practically, |     | we construct |     |
| ------ | --------- | ---- | -------------- | --- | --------- | -------- | ------------- | --- | ------------ | --- | ------------ | --- |
| module | to gather | most | domain-related |     | tables of |          |               |     |              |     |              |     |
user queries. We utilize the Tapas-based (Herzig premise-hypothesisbycontextualizedcolumnsand
judgesemanticequivalencybasedonoutputbidi-
etal.,2020)denseretrieverinthismodule(Herzig
|                                                 |     |     |                |           |       | rectionalentailmentscorese |     |     |     | ande         | .   |     |
| ----------------------------------------------- | --- | --- | -------------- | --------- | ----- | -------------------------- | --- | --- | --- | ------------ | --- | --- |
| etal.,2021),duetoitsbettertabularcontextualiza- |     |     |                |           |       |                            |     |     | 1   |              | 2   |     |
| tion expressiveness                             |     |     | over classical | retrieval | meth- |                            |     |     |     |              |     |     |
|                                                 |     |     |                |           |       | NLI Premise-Hypothesis     |     |     |     | Construction |     | The |
odssuchasWord2Vec(Mikolovetal.,2013)and
|                       |     |     |                      |             |        | Quality              | of premise-hypothesis |                            |     | plays | a key | factor |
| --------------------- | --- | --- | -------------------- | ----------- | ------ | -------------------- | --------------------- | -------------------------- | --- | ----- | ----- | ------ |
| BM25(Robertson,2009). |     |     | Followingtheoriginal |             |        |                      |                       |                            |     |       |       |        |
|                       |     |     |                      |             |        | forNLI’sfunctioning. |                       | Weidentifythreepotentially |     |       |       |        |
| usage proposed        |     | by  | Herzig et            | al. (2020), | we re- |                      |                       |                            |     |       |       |        |
usefulelementsforcontextualizingcolumnswith
trievethetop100mostdomain-relatedtablesfrom
|     |     |     |     |     |     | surroundingtablecontext: |     |     | TPE,columntype,and |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------------ | --- | --- | --- |
thebackendWebDataCommons(WDC)(Lehm-
|     |     |     |     |     |     | columncellvalue. |     | Throughmanualexperiments, |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ------------------------- | --- | --- | --- | --- |
bergetal.,2016)databaseconsistingof600knon- weobservethat: (i)Addingcellvaluesignificantly
repetitivetableswithatmostfivecolumns.
|     |     |     |     |     |     | hurtdecisionaccuracyofNLImodels. |     |     |     |     | (ii)TPEis |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --------- | --- |
themostimportantcontextinformationandcannot
4.2 NumberbatchReranker
|     |     |     |     |     |     | be ablated. | (iii) | Column | type | information |     | can be |
| --- | --- | --- | --- | --- | --- | ----------- | ----- | ------ | ---- | ----------- | --- | ------ |
From these retrieved domain-related tables, we adesirablesourceforword-sensedisambiguation.
further narrow down the range of most semanti- Thusthefinaltemplateforpremise-hypothesiscon-
| callyassociatedcandidatecolumns. |     |     |     |     | Thisisdone |           |           |           |     |        |              |     |
| -------------------------------- | --- | --- | --- | --- | ---------- | --------- | --------- | --------- | --- | ------ | ------------ | --- |
|                                  |     |     |     |     |            | struction | as python | formatted |     | string | is expressed |     |
by a ConceptNet Numberbatch word embedding as: f“{TPE} {CN} ({CT}).”, where CN is
(Speer et al., 2017) reranker, who computes the columnname,andCTiscolumntype.
| cosinesimilarityscoreforagivencolumnpair. |     |     |     |     | We  |         |          |           |     |     |           |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | ------- | -------- | --------- | --- | --- | --------- | --- |
|                                           |     |     |     |     |     | RPL/ADD | Decision | Criterion |     | In  | practice, | we  |
chooseConceptNetNumberbatchduetoitsadvan-
|     |     |     |     |     |     | observe | a discrepancy |     | in  | output | entailment |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------- | --- | --- | ------ | ---------- | --- |
tageoffarricher(520k)in-vocabularymulti-grams
|     |     |     |     |     |     | scores | between | premise-hypothesis |     |     | score | e 1 and |
| --- | --- | --- | --- | --- | --- | ------ | ------- | ------------------ | --- | --- | ----- | ------- |
comparedwithWord2Vec(Mikolovetal.,2013),
|                                |             |         |                |              |               | hypothesis-premisescoree |             |        | .              | Thuswetakescores |      |           |
| ------------------------------ | ----------- | ------- | -------------- | ------------ | ------------- | ------------------------ | ----------- | ------ | -------------- | ---------------- | ---- | --------- |
| GloVe                          | (Pennington |         | et al., 2014), |              | and Counter-  |                          |             |        | 2              |                  |      |           |
|                                |             |         |                |              |               | from both                | direction   | into   | consideration. |                  | For  | RPL,      |
| fitting                        | (Mrkšic´    | et al., | 2016),         | which        | is especially |                          |             |        |                |                  |      |           |
|                                |             |         |                |              |               | we empirically           |             | choose | min(e          | ,e               | ) >= | 0.65      |
| desirableformulti-gramcolumns. |             |         |                | Wekeepthetop |               |                          |             |        |                | 1                | 2    |           |
|                                |             |         |                |              |               | (Figure                  | 2) as the   | final  | RPL            | acceptance       |      | criterion |
| 20 similar                     | among       | them    | as RPL/ADD     |              | candidates    |                          |             |        |                |                  |      |           |
|                                |             |         |                |              |               | to reduce                | occurrences |        | of false       | positive         |      | entail-   |
foreachcolumnoftheoriginaltable.
|     |     |     |     |     |     | ment decision. | For | ADD, | the | criterion | is  | instead |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ---- | --- | --------- | --- | ------- |
4.3 Word-levelReplacementviaDictionary max(e 1 ,e 2 ) <= 0.45toreducefalsenegativeen-
tailmentdecisions5.
| Aside | from candidates |     | obtained | from | retriever- |     |     |     |     |     |     |     |
| ----- | --------------- | --- | -------- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
rerankerforwhole-columnlevelRPL,weconsider 5 ExperimentsandAnalysis
| word-level | RPL | for | a target column |     | as a comple- |     |     |     |     |     |     |     |
| ---------- | --- | --- | --------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
5.1 ExperimentalSetup
| ment. | Specifically, |     | we replace | each | word in a |     |     |     |     |     |     |     |
| ----- | ------------- | --- | ---------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
giventargetcolumnwithitssynonymsrecordedin DatasetsandModels ThefiveoriginalText-to-
theOxfordDictionary(noiseismorecontrollable SQLdatasetsinvolvesinourexperimentsare: Spi-
comparedwithsynonymsgatheredbyembedding). der (Yu et al., 2018), WikiSQL (Zhong et al.,
Withaprobability25%foreachoriginalwordto 2017),WTQ(Shietal.,2020)6,CoSQL(Yuetal.,
remain unchanged, we sample until the max pre- 2019a)andSParC(Yuetal.,2019b). Theircorre-
definednumber(20)ofcandidatesisreachedor5 spondingperturbedtablesarefromourADVETA
consecutivelyrepeatedcandidatesareproduced.
4WehighlyrecommendreadingourpilotstudyinB.1.
5Toavoidsemanticconflictbetweenanewcolumnc˜and
4.4 NLIasFinalDecisionMaker
|     |     |     |     |     |     | originalcolumnsc | 1 ,··· | ,c n | ,weapplytoeachpairof(c˜,c |     |     | i ). |
| --- | --- | --- | --- | --- | --- | ---------------- | ------ | ---- | ------------------------- | --- | --- | ---- |
6NotethatweusetheversionwithSQLannotationspro-
| So far | we have | pinpointed |     | candidate | columns |     |     |     |     |     |     |     |
| ------ | ------- | ---------- | --- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- |
videdbyShietal.(2020)here,sincetheoriginalWTQ(Pasu-
whosedomainrelevancyandsemanticassociation
patandLiang,2015)onlycontainsanswerannotations.

Dataset Baseline Dev RPL ADD ual candidate from ADVETA. For performance
69.9 23.8±2.1 36.4±1.3 stability and statistical significance, we run five
DuoRAT
| Spider |     |     |     | (-46.1) |     | (-33.5) |     |     |     |     |     |     |     |
| ------ | --- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
attackswithrandomseedsforeachNL-SQLpair.
|     | ETA | 70.8 | 27.6±1.8 |         |     | 39.9±0.9 |     |     |     |     |     |     |     |
| --- | --- | ---- | -------- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
|     |     |      |          | (-43.2) |     | (-30.9)  |     |     |     |     |     |     |     |
AttackResults
|     | SQLova | 81.6 | 27.2±1.3 |     |     | 66.2±2.3 |     |     | Table2presentstheperformance |     |     |     |     |
| --- | ------ | ---- | -------- | --- | --- | -------- | --- | --- | ---------------------------- | --- | --- | --- | --- |
WikiSQL (-54.4) (-15.4) ofmodelsonoriginaldevsets,ADVETA-RPLand
|     | CESQL | 84.3 | 52.2±0.9 |         |     | 71.2±1.5 |                                         |     |     |     |     |     |     |
| --- | ----- | ---- | -------- | ------- | --- | -------- | --------------------------------------- | --- | --- | --- | --- | --- | --- |
|     |       |      |          | (-32.1) |     | (-13.1)  | ADVETA-ADD.Acrossvarioustaskformats,do- |     |     |     |     |     |     |
WTQ SQUALL 44.1 22.8±0.5 32.9±0.8 mains, and model designs, state-of-the-art Text-
|       |         |      |          | (-21.3) |     | (-11.2)  | to-SQLparsersexperiencedramaticperformance |                |     |     |                    |     |     |
| ----- | ------- | ---- | -------- | ------- | --- | -------- | ------------------------------------------ | -------------- | --- | --- | ------------------ | --- | --- |
|       | EditSQL | 39.9 | 13.3±0.7 |         |     | 30.5±1.1 |                                            |                |     |     |                    |     |     |
|       |         |      |          |         |     |          | drop on                                    | our benchmark: |     | by  | RPL perturbations, |     |     |
| CoSQL |         |      |          | (-26.6) |     | (-9.4)   |                                            |                |     |     |                    |     |     |
IGSQL 44.1 16.4±1.2 32.8±2.1 the relative percentage drop is as high as 53.1%,
|       |         |      |          | (-27.7) |     | (-11.3)  |                                               |        |     |         |       |              |     |
| ----- | ------- | ---- | -------- | ------- | --- | -------- | --------------------------------------------- | ------ | --- | ------- | ----- | ------------ | --- |
|       |         |      |          |         |     |          | whereas                                       | on ADD | the | drop is | 25.6% | on average7. |     |
|       | EditSQL | 47.2 | 30.5±0.9 |         |     | 40.2±1.2 |                                               |        |     |         |       |              |     |
| SParC |         |      |          |         |     |          | AnotherinterestingobservationisthatRPLconsis- |        |     |         |       |              |     |
|       |         |      |          | (-16.7) |     | (-7.0)   |                                               |        |     |         |       |              |     |
|       | IGSQL   | 50.7 | 34.2±0.5 |         |     | 42.9±1.7 |                                               |        |     |         |       |              |     |
tentlyleadstohigherperformancedropsthanADD.
|     |     |     |     | (-16.5) |     | (-7.8) |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Thisisperhapsduetomodels’heavyrelianceon
Table 2: Results on original dev and ADVETA (RPL lexicalmatching,insteadoftrueunderstandingof
andADDsubsets). Redfontsdenoteabsolutepercent- languageandtablecontext. Conclusively,Text-to-
ageperformancedropcomparedwithoriginaldev.
|     |     |     |     |     |     |     | SQL models | are | still | far less | robust | than | desired |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----- | -------- | ------ | ---- | ------- |
againstvariabilityfromthetableinputside.
| benchmark. |     | WikiSQLandWTQaresingle-table, |     |     |     |     |        |          |     |            |     |         |     |
| ---------- | --- | ----------------------------- | --- | --- | --- | --- | ------ | -------- | --- | ---------- | --- | ------- | --- |
|            |     |                               |     |     |     |     | Attack | Analysis | To  | understand | the | reasons | for |
whileSpider,CoSQL,andSParChavemulti-tables.
parsers’vulnerability,wespecificallyanalyzetheir
CoSQLandSParCareknownasmulti-turnText-to-
schemalinkingmoduleswhichareresponsiblefor
SQLdatasets,sharingthesametableswithSpider.
recognizingtableelementsmentionedinNLques-
DatasetstatisticsareshowninAppendixTable11.
|     |     |     |     |     |     |     | tions. This | module | is  | considered | a   | vital | compo- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | --- | ---------- | --- | ----- | ------ |
Weevaluateopen-sourceText-to-SQLmodels
nentforText-to-SQL(Wangetal.,2020;Scholak
| that reach         | competitive |     | performance               |     | on  | the afore- |               |     |         |        |     |          |     |
| ------------------ | ----------- | --- | ------------------------- | --- | --- | ---------- | ------------- | --- | ------- | ------ | --- | -------- | --- |
|                    |             |     |                           |     |     |            | et al., 2021; | Liu | et al., | 2021). | We  | leverage | the |
| mentioneddatasets. |             |     | DuoRAT(Scholaketal.,2021) |     |     |            |               |     |         |        |     |          |     |
oracleschemalinkingannotationsonSpider(Lei
andETA(Liuetal.,2021)arebaselinesforSpider;
etal.,2020)andtestETAmodelonADVETAus-
SQUALL(Shietal.,2020)isthebaselineforWTQ;
|        |        |     |            |     |       |      | ing the | oracle | linkings. | Note | that we | update | the |
| ------ | ------ | --- | ---------- | --- | ----- | ---- | ------- | ------ | --------- | ---- | ------- | ------ | --- |
| SQLova | (Hwang | et  | al., 2019) | and | CESQL | (Guo |         |        |           |      |         |        |     |
oraclelinkingsaccordinglywhentestingonRPL.
andGao,2019)arebaselinesforWikiSQL.Forthe
Table4comparestheperformanceofETAwithor
| two multi-turn |     | datasets | (CoSQL |     | & SParC), | base- |     |     |     |     |     |     |     |
| -------------- | --- | -------- | ------ | --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- |
withouttheoraclelinkings,fromwhichwemake
linesareEditSQL(Zhangetal.,2019)andIGSQL
|      |          |        |       |       |      |        | twoobservations: |     | (i)Whenguidedwiththeoracle |     |     |     |     |
| ---- | -------- | ------ | ----- | ----- | ---- | ------ | ---------------- | --- | -------------------------- | --- | --- | --- | --- |
| (Cai | and Wan, | 2020). | Exact | Match | (EM) | is em- |                  |     |                            |     |     |     |     |
linkings,ETAperformsmuchbetteronbothRPL
ployed for evaluation metric across all settings. (27.6% → 55.7%) (39.9% → 71.3%).
|     |     |     |     |     |     |     |     |     | and | ADD |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TrainingdetailsareshowninC.2.
Therefore,thefailureinschemalinkingisoneof
|     |     |     |     |     |     |     | the essential | causes | for | the vulnerability |     | of  | Text- |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ------ | --- | ----------------- | --- | --- | ----- |
5.2 Attack
|        |         |                  |          |        |          |             | to-SQLparsers.  |     | (ii)Evenwiththeoraclelinkings, |     |         |     |       |
| ------ | ------- | ---------------- | -------- | ------ | -------- | ----------- | --------------- | --- | ------------------------------ | --- | ------- | --- | ----- |
| Attack | Details | All              | baseline | models |          | are trained |                 |     |                                |     |         |     |       |
|        |         |                  |          |        |          |             | the performance |     | of ETA                         | on  | RPL and | ADD | still |
| from   | scratch | on corresponding |          |        | original | training    |                 |     |                                |     |         |     |       |
lagsbehinditsperformanceontheoriginaldevset,
| sets, | and then | independently |     | evaluated |     | on origi- |     |     |     |     |     |     |     |
| ----- | -------- | ------------- | --- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
especiallyonRPL.Throughacarefulanalysison
naldevsets,ADVETA-RPLandADVETA-ADD.
failurecases,wefindthatETAstillgeneratestable
| Since | columns | have | around | three | manual | candi- |     |     |     |     |     |     |     |
| ----- | ------- | ---- | ------ | ----- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
elementsthathaveahighdegreeoflexicalmatch-
datesinADVETA-RPL/ADD,thenumberofpossi-
|     |     |     |     |     |     |     | ing with | NL questions, |     | even | though | the | correct |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | ---- | ------ | --- | ------- |
bleperturbedtablesscalesexponentiallywithcol-
tableelementsarespecifiedintheoraclelinkings.
umnnumbersforagiventablefromtheoriginaldev
| set. Therefore,modelsareevaluatedonADVETA- |      |                |     |           |     |           | 5.3 Defense  |         |        |       |         |             |     |
| ------------------------------------------ | ---- | -------------- | --- | --------- | --- | --------- | ------------ | ------- | ------ | ----- | ------- | ----------- | --- |
| RPL/ADDbysamplingperturbedtables.          |      |                |     |           |     | Foreach   |              |         |        |       |         |             |     |
|                                            |      |                |     |           |     |           | Defense      | Details | We     | carry | defense | experiments |     |
| NL-SQL                                     | pair | and associated |     | table(s), |     | we sample |              |         |        |       |         |             |     |
|                                            |      |                |     |           |     |           | with SQLova, |         | SQUALL | and   | ETA     | on WikiSQL, |     |
oneRPL-perturbedtableandoneADD-perturbed
|                    |     |     |                         |     |     |     | WTQandSpider,respectively. |     |     |     | WecompareCTA |     |     |
| ------------------ | --- | --- | ----------------------- | --- | --- | --- | -------------------------- | --- | --- | --- | ------------ | --- | --- |
| tableineachattack. |     |     | Eachcolumnmentionedfrom |     |     |     |                            |     |     |     |              |     |     |
goldSQLisperturbedbyarandomlysampledman-
7AveragerelativeperformancepresentedinAppendixC.3.

|     |     |     | WikiSQL |     |     |     | WTQ |     |     | Spider |     |     |
| --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
Approach
|     |     | Dev | RPL | ADD |     | Dev | RPL | ADD | Dev | RPL |     | ADD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Orig. 81.6 27.2±1.3 66.2±2.3 44.1 22.8±0.5 32.9±0.8 70.8 27.6±1.8 39.9±0.9
BA 80.1±0.2 56.8±0.8 77.9±0.5 43.9±0.3 33.6±0.4 42.8±0.7 68.1±0.5 26.9±1.1 43.1±0.7
TF 80.5±0.3 57.7±0.7 77.7±0.4 43.7±0.4 35.2±0.5 42.6±0.6 67.9±0.6 28.4±1.2 42.2±0.6
W2V 80.8±0.1 60.7±1.1 78.2±0.6 43.4±0.1 36.8±0.6 42.2±0.9 68.3±0.2 30.1±1.3 43.3±1.4
| MAS |     | –   | –   |     | –   | –   | –   | –   | 69.1±0.3 | 27.3±0.7 | 35.3±0.5 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | -------- | -------- | --- |
CTA 81.2±0.1 69.2±0.5 79.9±0.3 44.1±0.1 41.8±0.3 44.6±0.5 69.8±0.1 35.8±0.5 50.6±0.1
w/oRetriver 81.0±0.2 68.1±0.2 78.1±0.5 44.0±0.2 40.6±0.2 42.1±0.3 69.7±0.3 34.7±0.5 43.0±0.8
w/oMNLI 80.6±0.3 61.3±0.5 78.6±0.2 43.8±0.1 36.9±0.3 43.1±0.2 69.6±0.2 29.8±0.2 47.8±0.2
Table3: DefenseresultsonADVETA(RPLandADDsubsets). Avg. EMandfluctuationsof5runsarereported.
Orig. denotesperformancewithoutdefensefromTable2.
SchemaLinking Dev RPL ADD Method ColP ColR ColF TabP TabR TabF
|     | w/ooracle |     | 70.8 | 27.6    | 39.9    |     | ETA    | 85.4 | 36.8 51.4 | 61.3 | 63.4 62.3 |     |
| --- | --------- | --- | ---- | ------- | ------- | --- | ------ | ---- | --------- | ---- | --------- | --- |
|     |           |     |      | (-43.2) | (-30.9) |     | W2VRPL | 86.1 | 40.2 54.8 | 70.4 | 72.6 71.5 |     |
|     | w/oracle  |     | 75.2 | 55.7    | 71.3    |     | CTARPL | 88.1 | 50.8 64.4 | 80.1 | 85.4 82.7 |     |
|     |           |     |      | (-19.5) | (-3.9)  |     |        |      |           |      |           |     |
|     |           |     |      |         |         |     | ETA    | 86.3 | 60.2 70.9 | 71.2 | 75.8 73.4 |     |
|     |           |     |      |         |         |     | W2VADD | 86.5 | 63.7 73.4 | 75.9 | 82.1 78.9 |     |
Table4: SchemalinkinganalysisofETAonSpider. CTAADD 88.1 70.2 78.2 83.6 89.5 86.4
|     |     |     |     |     |     |     | Table5: | Theschemalinkinganalysisofattackingwith |             |        |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------------------------------- | ----------- | ------ | --- | --- |
|     |     |     |     |     |     |     | ETA and | two defense                             | approaches, | namely | W2V | and |
withthreebaselineadversarialtrainingapproaches:
CTAonSpider;ColascolumnandTabastable.P,R,F
| Word2Vec | (W2V), |     | TextFooler | (TF) | (Jin | et al., |     |     |     |     |     |     |
| -------- | ------ | --- | ---------- | ---- | ---- | ------- | --- | --- | --- | --- | --- | --- |
isshortforprecision,recallandF1score,respectively.
| 2020),   | and BERT-Attack |         | (BA)   | (Li | et al., | 2020) |     |     |     |     |     |     |
| -------- | --------------- | ------- | ------ | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
| (details | found           | in D.). | Models | are | trained | from  |     |     |     |     |     |     |
scratchoncorrespondingaugmented trainingsets. (ii)CTAfailstobringmodelsbacktotheirorig-
| Specifically, |     | for each | NL-SQL | pair, | we keep | the |          |              |      |            |      |       |
| ------------- | --- | -------- | ------ | ----- | ------- | --- | -------- | ------------ | ---- | ---------- | ---- | ----- |
|               |     |          |        |       |         |     | inal dev | performance. | Even | if trained | with | high- |
original table while generating one RPL and one qualitydataaugmentedbyCTA,modelscouldstill
ADDadversarialexample. Asaresult,augmented befarworsethantheiroriginalperformance. This
| training | data | is three | times | as large | in the | sense |     |     |     |     |     |     |
| -------- | ---- | -------- | ----- | -------- | ------ | ----- | --- | --- | --- | --- | --- | --- |
gapishighlysubjectedtothesimilarityoflexicon
| that each | NL-SQL |     | pair is | now trained |     | against |                                    |     |     |     |             |     |
| --------- | ------ | --- | ------- | ----------- | --- | ------- | ---------------------------------- | --- | --- | --- | ----------- | --- |
|           |        |     |         |             |     |         | distributionbetweentrainanddevset. |     |     |     | Concretely, |     |
three tables: original, RPL-perturbed, and ADD- on WikiSQL and WTQ where train and dev set
perturbed. In addition to the adversarial training haveasimilardomain,bothRPLperformanceand
defenseparadigm,wealsoincludethemanualver-
ADDperformancearebroughtbackclosertoorigi-
sionofMulti-AnnotationSelection(MAS)byGan naldevperformancewhenaugmentedwithCTA.
et al. (2021) on Spider, using their released data. Onthecontrary,onSpiderwheretrain-devdomains
Therestevaluationprocessissameasattack.
overlapless,thereisstillanotablegapbetweenper-
formanceafteradversarialtrainingandtheoriginal
DefenseResults Table3presentsmodelperfor- dev performance. In conclusion, more effective
mancethroughvariousdefenseapproaches. Weget defenseparadigmsareyettobeinvestigated.
| twoobservations: |     | (i)CTAconsistentlybringsbet- |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
terrobustness. Comparedwithotherapproaches, DefenseAnalysis Followingattackanalysis,we
conductschemalinkinganalysiswithETAmodel
CTA-augmentedmodelshavethebestperformance
across all ADVETA-RPL/ADD settings, as well augmented with top 2 approaches (i.e. W2V &
as on all original dev sets. These results demon- CTA)onSpider. Wefollowmetriccalculationof
strateCTAcaneffectivelyimprovetherobustness (Liu et al., 2021) and details are shown in §C.4.
AsshowninTable5,bothapproachesimprovethe
| of models | against | RPL | and | ADD | perturbations |     |     |     |     |     |     |     |
| --------- | ------- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
whileintroducingfewernoisesintooriginaltrain- schemalinkingF . Specifically,CTAimprovescol-
1
ingsets. Interestingly,weobservethattextualad- umnF by3% ∼ 8%,andtableF by13% ∼ 20%,
|     |     |     |     |     |     |     | 1   |     |     | 1   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
comparedwithvanillaETA.Thisrevealsthatim-
versarialexamplegenerationapproaches(BA,TF)
are outperformed by the simple W2V approach. provementofrobustnesscanbeprimarilyattributed
Thisverifiesouranalysisstatedin§4. Weinclude tobetterschemalinking.
acasestudyinAppendixB.3oncharacteristicsof Some might worry about the validity of the
variousbaselines. CTA’s effectiveness due to data leakage risks in-

| Model |     |     | Spider | Spider-Syn |     | 5.5 GeneralizationtoNLPerturbations |     |     |     |     |     |     |
| ----- | --- | --- | ------ | ---------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- |
RAT-SQL (Wangetal.,2020) 69.7 48.2 BeyondCTA’seffectivenessagainsttable-sideper-
BERT
| RAT-SQL            | BERT +MAS(Ganetal.,2021) |     |     | 67.4 | 62.6 |             |           |     |          |          |     |           |
| ------------------ | ------------------------ | --- | --- | ---- | ---- | ----------- | --------- | --- | -------- | -------- | --- | --------- |
|                    |                          |     |     |      |      | turbations, | a natural |     | question | follows: |     | could re- |
| ETA(Liuetal.,2021) |                          |     |     | 70.8 | 50.6 |             |           |     |          |          |     |           |
ETA+CTA 69.8 60.4 trainingwithadversarialtableexamplesimprove
|     |     |     |     |     |     | model | robustness | against |     | perturbations |     | from the |
| --- | --- | --- | --- | --- | --- | ----- | ---------- | ------- | --- | ------------- | --- | -------- |
Table6: EMonSpider/Spider-Syndev-sets. other side of Text-to-SQL input (i.e., NL ques-
|     |     |     |     |     |     | tions)? | Toexplorethis,wedirectlyevaluateETA |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ----------------------------------- | --- | --- | --- | --- | --- |
(trainedwithCTA-augmentedSpidertrain-set)on
| curred by | the annotation |     | design that | vendors | are |            |         |      |     |             |     |           |
| --------- | -------------- | --- | ----------- | ------- | --- | ---------- | ------- | ---- | --- | ----------- | --- | --------- |
|           |                |     |             |         |     | Spider-Syn | dataset | (Gan | et  | al., 2021), |     | which re- |
givenCTA-retrievedcandidatelistforADDanno-
placesschema-relatedtokensinNLquestionwith
(i)RPLhave
tations. However,weemphasizethat:
|     |     |     |     |     |     | itssynonym. | Weobserveanencouraging9.8%EM |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | ---------------------------- | --- | --- | --- | --- | --- |
NOvulnerabilitytodataleakagesinceitisentirely
improvementcomparedwithvanillaETA(trained
independentofCTA.(ii)TheleakageriskinADD
|                 |                                |          |            |     |          | with Spider | train-set). |     | This           | verifies | CTA’s | gener- |
| --------------- | ------------------------------ | -------- | ---------- | --- | -------- | ----------- | ----------- | --- | -------------- | -------- | ----- | ------ |
| isnegligible.   | Ontheonehand,ourvast-size(600k |          |            |     |          |             |             |     |                |          |       |        |
|                 |                                |          |            |     |          | alizability | to NL-side  |     | perturbations, |          | with  | compa- |
| tables) backend | DB                             | supplies | tremendous |     | data di- |             |             |     |                |          |       |        |
rableeffectivenessasthepreviousSOTAdefense
versity,maximallyreducingmultipleretrievalsof
approachMAS,whichfailstogeneralizetotable-
| asingletable; | Ontheotherhand, |     |     | CTA’ssuperior |     |     |     |     |     |     |     |     |
| ------------- | --------------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
sideperturbationsonADVETAinTable3.
performanceonSpider,therepresentativefeature
ofwhichiscross-domain&cross-databaseacross
|     |     |     |     |     |     | 6 RelatedWork |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- |
train-testsplits(thusmakesperformancegainfrom
data leakage hardly possible), further testifies its RobustnessofText-to-SQL Asdiscussedin§1,
authenticeffectiveness.
previousworks(Ganetal.,2021;Zengetal.,2020;
Dengetal.,2021)exclusivelystudyrobustnessof
5.4 CTAAblationStudy Text-to-SQL parsers against perturbations in NL
|          |                 |     |          |            |     | questioninputs. |     | Ourworkinsteadfocusesonvari- |     |     |     |     |
| -------- | --------------- | --- | -------- | ---------- | --- | --------------- | --- | ---------------------------- | --- | --- | --- | --- |
| We carry | out an ablation |     | study to | understand | the |                 |     |                              |     |     |     |     |
abilityfromthetableinputsideandrevealsparsers’
| roles of two | core | components | of  | CTA: dense | re- |     |     |     |     |     |     |     |
| ------------ | ---- | ---------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
vulnerabilitytotableperturbations.
trieverandRoBERTa-MNLI.Resultsareshownin
| Table3. |     |     |     |     |     | Adversarial |     | Example |     | Generation |     | Existing |
| ------- | --- | --- | --- | --- | --- | ----------- | --- | ------- | --- | ---------- | --- | -------- |
worksonadversarialtextexamplegenerationscan
| CTA w/o | Retriever | RPL | candidates | are | gener- |               |      |       |             |     |     |           |
| ------- | --------- | --- | ---------- | --- | ------ | ------------- | ---- | ----- | ----------- | --- | --- | --------- |
|         |           |     |            |     |        | be classified | into | three | categories: |     | (1) | Sentence- |
atedmerelyfromthedictionary;ADDgeneration Level. This line of work generates adversarial
isthesameasW2Vbaseline. Comparedwithcom- examples by introducing distracting sentences or
plete CTA, models augmented with this setting paraphrasingsentences(JiaandLiang,2017;Iyyer
experience 1.1% ∼ 1.2% and 1.8% ∼ 7.6% per- et al., 2018). (2) Word-Level. This dimension of
formancedroponRPLandADD,respectively. We work generates adversarial examples by flipping
attribute RPL drops to loss of real-world lexicon words in a sentence, replacing words with their
| diversity | and ADD | drops | to loss | of domain | rele- |             |     |            |         |      |             |             |
| --------- | ------- | ----- | ------- | --------- | ----- | ----------- | --- | ---------- | ------- | ---- | ----------- | ----------- |
|           |         |       |         |           |       | synonyms,   | and | deleting   | random  |      | words       | (Li et al., |
| vancy.    |         |       |         |           |       | 2020; Ren   | et  | al., 2019; | Jin     | et   | al., 2020). | (3)         |
|           |         |       |         |           |       | Char-Level. |     | This       | line of | work | flips,      | deletes,    |
CTA w/o MNLI RPL and ADD candidates are and inserts random chars in a word to generate
generated in the same way as CTA, but without adversarial examples (Belinkov and Bisk, 2018;
denoising of MNLI. RPL/ADD decisions solely Gao et al., 2018). All the three categories of
rely on ranked semantic similarity. Compared approaches have been widely used to reveal
with complete CTA, models augmented by this vulnerabilitiesofhigh-performanceneuralmodels
setting experience significant performance drops on various tasks, including text classification
(4.9% ∼ 7.9%)onallRPLsubsets,andmoderate (Ren et al., 2019; Morris et al., 2020), natural
drops (1.5% ∼ 2.8%) on all ADD subsets. We language inference (Li et al., 2020) and question
attributethesedropstotheinaccuratedifferentia- answering(Ribeiroetal.,2018). Previousworkon
tion between semantic equivalency and semantic robustness of Text-to-SQL and semantic parsing
associationduetolackofMNLI,whichresultsin models primarily adopt word-level perturbations
noisyRPL/ADDadversarialexamples. to generate adversarial examples (Huang et al.,

2021). For example, the Spider-Sync adversarial sionalannotatorstofindsuitableRPL/ADDcandi-
benchmark (Gan et al., 2021) is curated by datesfortargetcolumns. Wepaytheannotatorsat
replacingschema-relatedwordsinquestionswith apriceof10dollarsperhour. Thetotaltimecost
| theirsynonyms. |     |     |     |     |     |     | forannotatingourbenchmarkis253hours. |     |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- |
Despitethesemethods’effectivenessingenerat- Alltheexperimentsinthispapercanberunon
ingadversarialtextexamples,theyarenotreadily asingleTeslaV100GPU.Ourbenchmarkwillbe
applicable for structural tabular data, as we dis- releasedalongwiththepaper.
| cussedin§4.                              | Apartfromthis,table-sideperturba- |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------------------------------------- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tionsenjoymuchhigherattackingefficiency: |                                   |     |     |     |     | the |     |     |     |     |     |     |     |
References
| attack coverage |     | of a | single | table modification |     | in- |     |     |     |     |     |     |     |
| --------------- | --- | ---- | ------ | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cludes all affiliated SQLs, whereas one NL-side Katrin Affolter, Kurt Stockinger, and Abraham Bern-
|     |     |     |     |     |     |     | stein.2019. |     | Acomparativesurveyofrecentnatural |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --------------------------------- | --- | --- | --- | --- |
perturbationonlyaffectsasingleSQL.Combined
with the lighter cognitive efforts of tabular con- languageinterfacesfordatabases. TheVLDBJour-
nal,28:793–819.
textunderstandingthanNL-understanding,ATPis
arguablylowerinannotationcosts. Vincent Ballet, Xavier Renard, Jonathan Aigrain,
Previousworkontableperturbations(Cartella Thibault Laugel, Pascal Frossard, and Marcin De-
|               |         |       |            |         |       |       | tyniecki.      | 2019. | Imperceptible        |     | adversarial |     | attacks |
| ------------- | ------- | ----- | ---------- | ------- | ----- | ----- | -------------- | ----- | -------------------- | --- | ----------- | --- | ------- |
| et al., 2021; | Ballet  | et    | al., 2019) | focuses | on    | table |                |       |                      |     |             |     |         |
|               |         |       |            |         |       |       | ontabulardata. |       | CoRR,abs/1911.03274. |     |             |     |         |
| cell values;  | another | work, | (Ma        | and     | Wang, | 2020) |                |       |                      |     |             |     |         |
study impacts of naively (i.e., without considera- Yonatan Belinkov and Yonatan Bisk. 2018. Synthetic
tion of table context information and without hu- andnaturalnoisebothbreakneuralmachinetrans-
|     |     |     |     |     |     |     | lation. | ArXiv,abs/1711.02173. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------------- | --- | --- | --- | --- | --- |
manguarantee)renamingirrelevantcolumnsand
addingirrelevantcolumns. Inthiswork,wefocus Samuel R. Bowman, Gabor Angeli, Christopher Potts,
| on table | columns | and | propose | an  | effective | CTA |                 |     |     |          |       |         |       |
| -------- | ------- | --- | ------- | --- | --------- | --- | --------------- | --- | --- | -------- | ----- | ------- | ----- |
|          |         |     |         |     |           |     | and Christopher |     | D.  | Manning. | 2015. | A large | anno- |
frameworkthatbetterleveragestabularcontextin- tatedcorpusforlearningnaturallanguageinference.
CoRR,abs/1508.05326.
| formation | for | adversarial | example |     | generation, | as  |     |     |     |     |     |     |     |
| --------- | --- | ----------- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
wellasmanuallyannotateADVETAbenchmark. Yitao Cai and Xiaojun Wan. 2020. IGSQL: Database
|              |     |     |     |     |     |     | schema            | interaction |        | graph       | based neural | model | for    |
| ------------ | --- | --- | --- | --- | --- | --- | ----------------- | ----------- | ------ | ----------- | ------------ | ----- | ------ |
| 7 Conclusion |     |     |     |     |     |     | context-dependent |             |        | text-to-SQL | generation.  |       | In     |
|              |     |     |     |     |     |     | Proceedings       |             | of the | 2020        | Conference   | on    | Empir- |
We introduce Adversarial Table Perturbation ical Methods in Natural Language Processing
(ATP), a new paradigm for evaluating model ro- (EMNLP), pages 6903–6912, Online. Association
forComputationalLinguistics.
bustnessonText-to-SQLanddefineitsconduction
principles. WecuratetheADVETAbenchmark,on Francesco Cartella, Orlando Anunciação, Yuki Fun-
which all state-of-the-art models experience dra- abiki, Daisuke Yamaguchi, Toru Akishita, and
maticperformancedrop. Fordefensepurposes,we OlivierElshocht.2021. Adversarialattacksfortab-
|     |     |     |     |     |     |     | ular data: | Application |     | to  | fraud detection |     | and im- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | --- | --- | --------------- | --- | ------- |
designtheCTAframeworktailoredfortabularad-
|     |     |     |     |     |     |     | balanceddata. |     | InProceedingsoftheWorkshopon |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ---------------------------- | --- | --- | --- | --- |
versarialtrainingexamplegeneration. WhileCTA ArtificialIntelligenceSafety2021(SafeAI2021)co-
outperformsallbaselinemethodsinrobustnessen-
|     |     |     |     |     |     |     | located | with | the Thirty-Fifth |     | AAAI | Conference | on  |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---- | ---------------- | --- | ---- | ---------- | --- |
hancement, there is still an unfilled gap from the Artificial Intelligence (AAAI 2021), Virtual, Febru-
ary8,2021,volume2808ofCEURWorkshopPro-
| originalperformance. |     |     | Thiscallsforfutureexplo- |     |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ceedings.CEUR-WS.org.
| ration of   | the robustness |     | of  | Text-to-SQL | parsers |     |                                           |           |       |             |     |         |         |
| ----------- | -------------- | --- | --- | ----------- | ------- | --- | ----------------------------------------- | --------- | ----- | ----------- | --- | ------- | ------- |
| againstATP. |                |     |     |             |         |     | IdoDagan,DanRoth,MarkSammons,andFabioMas- |           |       |             |     |         |         |
|             |                |     |     |             |         |     |                                           |           |       | Recognizing |     | Textual | Entail- |
|             |                |     |     |             |         |     | simo                                      | Zanzotto. | 2013. |             |     |         |         |
EthicalConsiderations ment: Models and Applications. Synthesis Lec-
|     |     |     |     |     |     |     | tures | on Human | Language |     | Technologies. |     | Morgan |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | -------- | --- | ------------- | --- | ------ |
&ClaypoolPublishers.
OurADVETAbenchmarkpresentedinthisworkis
afreeandopenresourceforthecommunitytostudy
|     |     |     |     |     |     |     | Xiang Deng, | Ahmed | Hassan |     | Awadallah, | Christopher |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ------ | --- | ---------- | ----------- | --- |
the robustness of Text-to-SQL models. We col- Meek,OleksandrPolozov,HuanSun,andMatthew
lectedtablesfromthreemainstreamText-to-SQL Richardson. 2021. Structure-grounded pretraining
datasets,Spider(Yuetal.,2018),WikiSQL(Zhong for text-to-SQL. In Proceedings of the 2021 Con-
|               |     |     |           |     |         |        | ference   | of the | North         | American | Chapter      | of  | the As- |
| ------------- | --- | --- | --------- | --- | ------- | ------ | --------- | ------ | ------------- | -------- | ------------ | --- | ------- |
| et al., 2017) | and | WTQ | (Papernot |     | et al., | 2017), |           |        |               |          |              |     |         |
|               |     |     |           |     |         |        | sociation | for    | Computational |          | Linguistics: |     | Human   |
whicharealsofreeandopendatasetsforresearch LanguageTechnologies,pages1337–1350,Online.
use. Forthetableperturbationstep,wehireprofes-
AssociationforComputationalLinguistics.

NingDing,GuangweiXu,YulinChen,XiaobinWang, for Computational Linguistics: Human Language
XuHan,PengjunXie,Hai-TaoZheng,andZhiyuan Technologies,Volume1(LongPapers),pages1875–
Liu. 2021. Few-nerd: A few-shot named entity 1885, New Orleans, Louisiana. Association for
recognitiondataset. CoRR,abs/2105.07464. ComputationalLinguistics.
Yujian Gan, Xinyun Chen, Qiuping Huang, Matthew Robin Jia and Percy Liang. 2017. Adversarial ex-
Purver, John R. Woodward, Jinxia Xie, and Peng- amples for evaluating reading comprehension sys-
shengHuang.2021. Towardsrobustnessoftext-to- tems. In Proceedings of the 2017 Conference on
SQLmodelsagainstsynonymsubstitution. InPro- Empirical Methods in Natural Language Process-
ceedingsofthe59thAnnualMeetingoftheAssocia- ing,pages2021–2031,Copenhagen,Denmark.As-
tionforComputationalLinguisticsandthe11thIn- sociationforComputationalLinguistics.
ternationalJointConferenceonNaturalLanguage
Processing(Volume1: LongPapers), pages2505– Di Jin, Zhijing Jin, Joey Tianyi Zhou, and Peter
2515, Online. Association for Computational Lin- Szolovits. 2020. Is bert really robust? a strong
| guistics. |     |     |     |     |     | baselinefornaturallanguageattackontextclassifi- |     |     |                        |     |     |
| --------- | --- | --- | --- | --- | --- | ----------------------------------------------- | --- | --- | ---------------------- | --- | --- |
|           |     |     |     |     |     | cationandentailment.                            |     |     | InProceedingsoftheAAAI |     |     |
Ji Gao, Jack Lanchantin, Mary Lou Soffa, and Yan- conference on artificial intelligence, volume 34,
| jun Qi. | 2018. Black-box |     | generation |     | of adversar- |     |     |     |     |     |     |
| ------- | --------------- | --- | ---------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
pages8018–8025.
ialtextsequencestoevadedeeplearningclassifiers.
2018IEEESecurityandPrivacyWorkshops(SPW), Oliver Lehmberg, Dominique Ritze, Robert Meusel,
| pages50–56. |     |     |     |     |     | andChristianBizer.2016. |            |     | Alargepubliccorpusof |             |           |
| ----------- | --- | --- | --- | --- | --- | ----------------------- | ---------- | --- | -------------------- | ----------- | --------- |
|             |     |     |     |     |     | web tables              | containing |     | time                 | and context | metadata. |
Tianyu Gao, Xingcheng Yao, and Danqi Chen. 2021. In Proceedings of the 25th International Confer-
Simcse: Simple contrastive learning of sentence ence Companion on World Wide Web, WWW ’16
| embeddings. | CoRR,abs/2104.08821. |     |     |     |     |            |     |             |          |     |               |
| ----------- | -------------------- | --- | --- | --- | --- | ---------- | --- | ----------- | -------- | --- | ------------- |
|             |                      |     |     |     |     | Companion, |     | page 75–76, | Republic |     | and Canton of |
Geneva,CHE.InternationalWorldWideWebCon-
| Tong Guo | and Huilin | Gao. | 2019. | Content | enhanced |     |     |     |     |     |     |
| -------- | ---------- | ---- | ----- | ------- | -------- | --- | --- | --- | --- | --- | --- |
ferencesSteeringCommittee.
| bert-based | text-to-sql |     | generation. | arXiv | preprint |     |     |     |     |     |     |
| ---------- | ----------- | --- | ----------- | ----- | -------- | --- | --- | --- | --- | --- | --- |
arXiv:1910.07179.
|     |     |     |     |     |     | Wenqiang | Lei, Weixin | Wang, |     | Zhixin   | Ma, Tian Gan, |
| --- | --- | --- | --- | --- | --- | -------- | ----------- | ----- | --- | -------- | ------------- |
|     |     |     |     |     |     | Wei Lu,  | Min-Yen     | Kan,  | and | Tat-Seng | Chua. 2020.   |
JonathanHerzig,ThomasMüller,SyrineKrichene,and
Re-examiningtheroleofschemalinkingintext-to-
| Julian | Martin Eisenschlos. |     | 2021. |     | Open domain |      |                |     |        |      |               |
| ------ | ------------------- | --- | ----- | --- | ----------- | ---- | -------------- | --- | ------ | ---- | ------------- |
|        |                     |     |       |     |             | SQL. | In Proceedings |     | of the | 2020 | Conference on |
questionansweringovertablesviadenseretrieval.
|                  |       |           |     |        |        | Empirical    | Methods | in    | Natural    | Language | Process- |
| ---------------- | ----- | --------- | --- | ------ | ------ | ------------ | ------- | ----- | ---------- | -------- | -------- |
|                  |       |           |     |        |        | ing (EMNLP), |         | pages | 6943–6954, | Online.  | Associa- |
| Jonathan Herzig, | Pawel | Krzysztof |     | Nowak, | Thomas |              |         |       |            |          |          |
tionforComputationalLinguistics.
| Müller,          | Francesco | Piccinno, |                   | and | Julian Mar-   |                                            |       |           |       |               |       |
| ---------------- | --------- | --------- | ----------------- | --- | ------------- | ------------------------------------------ | ----- | --------- | ----- | ------------- | ----- |
| tin Eisenschlos. |           | 2020.     | TAPAS:            |     | weakly super- |                                            |       |           |       |               |       |
|                  |           |           |                   |     |               | Fei Li and                                 | H. V. | Jagadish. | 2016. | Understanding | natu- |
| vised table      | parsing   |           | via pre-training. |     | CoRR,         |                                            |       |           |       |               |       |
|                  |           |           |                   |     |               | rallanguagequeriesoverrelationaldatabases. |       |           |       |               | SIG-  |
abs/2004.02349.
MODRecord,45:6–13.
| Felix Hill, | Kyunghyun | Cho, | Sebastien |     | Jean, Coline |     |     |     |     |     |     |
| ----------- | --------- | ---- | --------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
LinyangLi,RuotianMa,QipengGuo,XiangyangXue,
| Devin, | and Yoshua | Bengio. |     | 2015a. | Embedding |                    |     |     |                       |     |     |
| ------ | ---------- | ------- | --- | ------ | --------- | ------------------ | --- | --- | --------------------- | --- | --- |
|        |            |         |     |        |           | andXipengQiu.2020. |     |     | BERT-ATTACK:Adversar- |     |     |
wordsimilaritywithneuralmachinetranslation.
|     |     |     |     |     |     | ial attack | against | BERT | using | BERT. | In Proceed- |
| --- | --- | --- | --- | --- | --- | ---------- | ------- | ---- | ----- | ----- | ----------- |
ingsofthe2020ConferenceonEmpiricalMethods
| Felix Hill, | Roi Reichart, | and | Anna | Korhonen. | 2015b. |     |     |     |     |     |     |
| ----------- | ------------- | --- | ---- | --------- | ------ | --- | --- | --- | --- | --- | --- |
SimLex-999: Evaluating semantic models with in Natural Language Processing (EMNLP), pages
(genuine) similarity estimation. Computational 6193–6202,Online.AssociationforComputational
| Linguistics,41(4):665–695. |     |     |     |     |     | Linguistics. |     |     |     |     |     |
| -------------------------- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
ShuoHuang,ZhuangLi,LizhenQu,andLeiPan.2021. Qian Liu, Dejian Yang, Jiahui Zhang, Jiaqi Guo, Bin
|               |     |        |          |          |         | Zhou, | and Jian-Guang |     | Lou. | 2021. | Awakening la- |
| ------------- | --- | ------ | -------- | -------- | ------- | ----- | -------------- | --- | ---- | ----- | ------------- |
| On robustness | of  | neural | semantic | parsers. | In Pro- |       |                |     |      |       |               |
tentgroundingfrompretrainedlanguagemodelsfor
| ceedings | of the | 16th Conference |     | of  | the European |     |     |     |     |     |     |
| -------- | ------ | --------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Chapter of the Association for Computational Lin- semantic parsing. In Findings of the Association
guistics: Main Volume, pages 3333–3342, Online. forComputationalLinguistics:ACL-IJCNLP2021,
AssociationforComputationalLinguistics. pages1174–1189,Online.AssociationforCompu-
tationalLinguistics.
WonseokHwang,JinyeongYim,SeunghyunPark,and
YinhanLiu,MyleOtt,NamanGoyal,JingfeiDu,Man-
| MinjoonSeo.2019. |     | Acomprehensiveexploration |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
onwikisqlwithtable-awarewordcontextualization. dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
arXivpreprintarXiv:1902.01069. Luke Zettlemoyer, and Veselin Stoyanov. 2019.
|     |     |     |     |     |     | Roberta: | A robustly |     | optimized | BERT | pretraining |
| --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | --------- | ---- | ----------- |
Mohit Iyyer, John Wieting, Kevin Gimpel, and Luke approach. CoRR,abs/1907.11692.
| Zettlemoyer. | 2018. | Adversarial |     | example | genera- |     |     |     |     |     |     |
| ------------ | ----- | ----------- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
tion with syntactically controlled paraphrase net- Pingchuan Ma and Shuai Wang. 2020. Mt-teql: Eval-
works. In Proceedings of the 2018 Conference uating and augmenting consistency of text-to-sql
of the North American Chapter of the Association modelswithmetamorphictesting.

TomasMikolov,IlyaSutskever,KaiChen,GregSCor- ial rules for debugging NLP models. In Proceed-
rado, and Jeff Dean. 2013. Distributed representa- ingsofthe56thAnnualMeetingoftheAssociation
tionsofwordsandphrasesandtheircompositional- forComputationalLinguistics(Volume1: LongPa-
ity. In Advances in neural information processing pers),pages856–865,Melbourne,Australia.Asso-
| systems,pages3111–3119. |     |     |     |     |     | ciationforComputationalLinguistics. |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- |
John Morris, Eli Lifland, Jin Yong Yoo, Jake Grigsby, S. Robertson. 2009. The Probabilistic Relevance
DiJin,andYanjunQi.2020. TextAttack: Aframe- Framework: BM25andBeyond. Foundationsand
work for adversarial attacks, data augmentation, Trends®inInformationRetrieval,3(4):333–389.
| and adversarial |     | training | in NLP. | In  | Proceedings |     |     |     |     |     |     |
| --------------- | --- | -------- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
of the 2020 Conference on Empirical Methods in Torsten Scholak, Raymond Li, Dzmitry Bahdanau,
|                            |     |     |     |                  |     | Harm | de Vries, | and | Chris | Pal. 2021. | DuoRAT: |
| -------------------------- | --- | --- | --- | ---------------- | --- | ---- | --------- | --- | ----- | ---------- | ------- |
| NaturalLanguageProcessing: |     |     |     | SystemDemonstra- |     |      |           |     |       |            |         |
tions,pages119–126,Online.AssociationforCom- Towards simpler text-to-SQL models. In Proceed-
putationalLinguistics. ings of the 2021 Conference of the North Ameri-
|     |     |     |     |     |     | can Chapter |     | of the Association |     | for | Computational |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------------------ | --- | --- | ------------- |
Nikola Mrkšic´, Diarmuid Ó Séaghdha, Blaise Thom- Linguistics: HumanLanguageTechnologies,pages
son, Milica Gašic´, Lina M. Rojas-Barahona, Pei- 1313–1321,Online.AssociationforComputational
| Hao Su,      | David | Vandyke, | Tsung-Hsien     |     | Wen, and     | Linguistics. |     |     |     |     |     |
| ------------ | ----- | -------- | --------------- | --- | ------------ | ------------ | --- | --- | --- | --- | --- |
| Steve Young. |       | 2016.    | Counter-fitting |     | word vectors |              |     |     |     |     |     |
to linguistic constraints. In Proceedings of the Tianze Shi, Chen Zhao, Jordan Boyd-Graber, Hal
2016ConferenceoftheNorthAmericanChapterof DauméIII,andLillianLee.2020. Onthepotential
theAssociationforComputationalLinguistics: Hu- oflexico-logicalalignmentsforsemanticparsingto
man Language Technologies, SQL queries. In Findings of the Association for
|              |             |             |     | pages | 142–148, San  |                                              |     |              |     |       |             |
| ------------ | ----------- | ----------- | --- | ----- | ------------- | -------------------------------------------- | --- | ------------ | --- | ----- | ----------- |
|              |             |             |     |       |               | Computational                                |     | Linguistics: |     | EMNLP | 2020, pages |
| Diego,       | California. | Association |     | for   | Computational |                                              |     |              |     |       |             |
| Linguistics. |             |             |     |       |               | 1849–1864,Online.AssociationforComputational |     |              |     |       |             |
Linguistics.
| Nikola Mrksic, | Diarmuid |     | Ó Séaghdha, |     | Blaise Thom- |     |     |     |     |     |     |
| -------------- | -------- | --- | ----------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
son,MilicaGasic,LinaMariaRojas-Barahona,Pei- RobynSpeer,JoshuaChin,andCatherineHavasi.2017.
|                    |       |          |                            |     |          | ConceptNet |            | 5.5: An | open    | multilingual | graph of    |
| ------------------ | ----- | -------- | -------------------------- | --- | -------- | ---------- | ---------- | ------- | ------- | ------------ | ----------- |
| Hao Su,            | David | Vandyke, | Tsung-Hsien                |     | Wen, and |            |            |         |         |              |             |
|                    |       |          |                            |     |          | general    | knowledge. |         | In AAAI | 2017,        | pages 4444– |
| SteveJ.Young.2016. |       |          | Counter-fittingwordvectors |     |          |            |            |         |         |              |             |
4451.
| tolinguisticconstraints. |     |     | CoRR,abs/1603.00892. |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Nicolas Papernot, Patrick McDaniel, Ian Goodfellow, Sai Sumathi and S Esakkirajan. 2007. Fundamentals
Somesh Jha, Z Berkay Celik, and Ananthram of relational database management systems, vol-
| Swami. | 2017. | Practical | black-box |     | attacks against | ume47. | Springer. |     |     |     |     |
| ------ | ----- | --------- | --------- | --- | --------------- | ------ | --------- | --- | --- | --- | --- |
InProceedingsofthe2017ACM
machinelearning.
|         |            |     |          |     |            | Bailin Wang, | Richard | Shin,   | Xiaodong    |     | Liu, Oleksandr |
| ------- | ---------- | --- | -------- | --- | ---------- | ------------ | ------- | ------- | ----------- | --- | -------------- |
| on Asia | conference | on  | computer | and | communica- |              |         |         |             |     |                |
|         |            |     |          |     |            | Polozov,     | and     | Matthew | Richardson. |     | 2020. RAT-     |
tionssecurity,pages506–519.
SQL:Relation-awareschemaencodingandlinking
Panupong Pasupat and Percy Liang. 2015. Composi- fortext-to-SQLparsers. InProceedingsofthe58th
tional semantic parsing on semi-structured tables. Annual Meeting of the Association for Computa-
In Proceedings of the 53rd Annual Meeting of the tionalLinguistics,pages7567–7578,Online.Asso-
Association for Computational Linguistics and the ciationforComputationalLinguistics.
7thInternationalJointConferenceonNaturalLan-
JohnWieting,MohitBansal,KevinGimpel,andKaren
| guageProcessing(Volume1: |     |     |     | LongPapers),pages |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
1470–1480, Beijing, China. Association for Com- Livescu. 2015. From paraphrase database to com-
putationalLinguistics. positional paraphrase model and back. Transac-
tionsoftheAssociationforComputationalLinguis-
| Jeffrey Pennington, |           | Richard                       | Socher, | and        | Christopher | tics,3:345–358. |                                   |        |         |            |         |
| ------------------- | --------- | ----------------------------- | ------- | ---------- | ----------- | --------------- | --------------------------------- | ------ | ------- | ---------- | ------- |
| Manning.            | 2014.     | GloVe:                        | Global  | vectors    | for word    |                 |                                   |        |         |            |         |
|                     |           |                               |         |            |             | Adina Williams, |                                   | Nikita | Nangia, | and Samuel | R. Bow- |
| representation.     |           | InProceedingsofthe2014Confer- |         |            |             |                 |                                   |        |         |            |         |
|                     |           |                               |         |            |             | man.2017.       | Abroad-coveragechallengecorpusfor |        |         |            |         |
| ence on             | Empirical | Methods                       |         | in Natural | Language    |                 |                                   |        |         |            |         |
Processing (EMNLP), pages 1532–1543, Doha, sentence understanding through inference. CoRR,
| Qatar.AssociationforComputationalLinguistics. |     |     |     |     |     | abs/1704.05426. |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
ShuhuaiRen,YiheDeng,KunHe,andWanxiangChe. Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
2019. Generating natural language adversarial ex- Chaumond,ClementDelangue,AnthonyMoi,Pier-
ricCistac,TimRault,RemiLouf,MorganFuntow-
amplesthroughprobabilityweightedwordsaliency.
icz,JoeDavison,SamShleifer,PatrickvonPlaten,
| In Proceedings |     | of the | 57th Annual |     | Meeting of the |     |     |     |     |     |     |
| -------------- | --- | ------ | ----------- | --- | -------------- | --- | --- | --- | --- | --- | --- |
Association for Computational Linguistics, pages Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu,
1085–1097, Florence, Italy. Association for Com- Teven Le Scao, Sylvain Gugger, Mariama Drame,
putationalLinguistics. QuentinLhoest,andAlexanderRush.2020. Trans-
|     |     |     |     |     |     | formers: | State-of-the-art |     | natural | language | process- |
| --- | --- | --- | --- | --- | --- | -------- | ---------------- | --- | ------- | -------- | -------- |
Marco Tulio Ribeiro, Sameer Singh, and Carlos ing. InProceedingsofthe2020ConferenceonEm-
Guestrin. 2018. Semantically equivalent adversar- pirical Methods in Natural Language Processing:

System Demonstrations, pages 38–45, Online. As- Victor Zhong, Caiming Xiong, and Richard Socher.
sociationforComputationalLinguistics. 2017. Seq2sql: Generating structured queries
|     |     |     |     |     |     |     | from | natural | language | using | reinforcement |     | learn- |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------- | -------- | ----- | ------------- | --- | ------ |
ing. arXivpreprintarXiv:1709.00103.
| Wenpeng              | Yin,       | Jamaal    | Hay, | and Dan    | Roth.           | 2019. |                     |     |     |     |     |     |     |
| -------------------- | ---------- | --------- | ---- | ---------- | --------------- | ----- | ------------------- | --- | --- | --- | --- | --- | --- |
| Benchmarking         |            | zero-shot |      | text       | classification: |       |                     |     |     |     |     |     |     |
| Datasets,            | evaluation |           | and  | entailment | approach.       |       |                     |     |     |     |     |     |     |
| CoRR,abs/1909.00161. |            |           |      |            |                 |       | A BenchmarkExamples |     |     |     |     |     |     |
Tao Yu, Rui Zhang, Heyang Er, Suyi Li, Eric Xue, Wedisplaysomerepresentativebenchmarkannota-
| Bo Pang, | Xi  | Victoria | Lin, | Yi Chern | Tan, | Tianze |     |     |     |     |     |     |     |
| -------- | --- | -------- | ---- | -------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
tioncasesfortoconveyreadersaintuitivefeeling
| Shi,       | Zihan   | Li, Youxuan |       | Jiang,          | Michihiro | Ya-    |                        |          |     |           |                   |     |     |
| ---------- | ------- | ----------- | ----- | --------------- | --------- | ------ | ---------------------- | -------- | --- | --------- | ----------------- | --- | --- |
|            |         |             |       |                 |           |        | onourRPLandADDsubsets. |          |     |           | AsreflectedinFig- |     |     |
| sunaga,    | Sungrok | Shim,       | Tao   | Chen, Alexander |           | Fab-   |                        |          |     |           |                   |     |     |
|            |         |             |       |                 |           |        | ure 3, RPL             | reflects | the | following | characteristics   |     |     |
| bri, Zifan | Li,     | Luyao       | Chen, | Yuwen           | Zhang,    | Shreya |                        |          |     |           |                   |     |     |
Dixit, Vincent Zhang, Caiming Xiong, Richard beyond RPL principles: (i) Abbreviation of com-
Socher, Walter Lasecki, and Dragomir Radev. monwords. e.g. Cellnumbervs. Tel. (ii)Idiomatic
| 2019a. | CoSQL:Aconversationaltext-to-SQLchal- |     |     |     |     |     |                    |     |            |     |                  |     |     |
| ------ | ------------------------------------- | --- | --- | --- | --- | --- | ------------------ | --- | ---------- | --- | ---------------- | --- | --- |
|        |                                       |     |     |     |     |     | transformatione.g. |     | Airdatevs. |     | Releasetime(iii) |     |     |
lengetowardscross-domainnaturallanguageinter-
|                   |     |                            |     |     |     |     | Partofspeechstructuretransformatione.g. |     |     |     |     |     | Written |
| ----------------- | --- | -------------------------- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ------- |
| facestodatabases. |     | InProceedingsofthe2019Con- |     |     |     |     |                                         |     |     |     |     |     |         |
|                   |     |                            |     |     |     |     | byvs. Author.                           |     |     |     |     |     |         |
ferenceonEmpiricalMethodsinNaturalLanguage ADDperturbationsfaithfullyobey
Processing and the 9th International Joint Confer- ADD principles and additions demonstrate high
| ence | on Natural | Language |     | Processing | (EMNLP- |     |     |     |     |     |     |     |     |
| ---- | ---------- | -------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
coherencywithrespecttooriginaldomain.
| IJCNLP), | pages | 1962–1979, |     | Hong | Kong, | China. |     |     |     |     |     |     |     |
| -------- | ----- | ---------- | --- | ---- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- |
AssociationforComputationalLinguistics.
|                                              |            |          |       |           |           |          | B CTADetails                              |     |     |     |     |     |     |
| -------------------------------------------- | ---------- | -------- | ----- | --------- | --------- | -------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
| Tao Yu,                                      | Rui Zhang, | Kai      | Yang, | Michihiro | Yasunaga, |          |                                           |     |     |     |     |     |     |
|                                              |            |          |       |           |           |          | B.1 NLI-basedSubstitutabilityVerification |     |     |     |     |     |     |
| Dongxu                                       | Wang,      | Zifan    | Li,   | James     | Ma, Irene | Li,      |                                           |     |     |     |     |     |     |
| Qingning                                     | Yao,       | Shanelle |       | Roman,    | Zilin     | Zhang,   |                                           |     |     |     |     |     |     |
| and Dragomir                                 |            | Radev.   | 2018. | Spider:   |           | A large- |                                           |     |     |     |     |     |     |
|                                              |            |          |       |           |           |          | Approach                                  |     | e   | e   | ∆   | ∆   |     |
| scalehuman-labeleddatasetforcomplexandcross- |            |          |       |           |           |          |                                           |     | 1   | 2   |     | e1  | e2  |
| domainsemanticparsingandtext-to-SQLtask.     |            |          |       |           |           | In       |                                           |     |     |     |     |     |     |
Roberta-RTE
| Proceedings               |     | of the 2018 | Conference |             | on Empirical |       |           |     |      |      |      |      |     |
| ------------------------- | --- | ----------- | ---------- | ----------- | ------------ | ----- | --------- | --- | ---- | ---- | ---- | ---- | --- |
|                           |     |             |            |             |              |       | human     |     | 48.5 | 48.1 | 0.65 | 0.46 |     |
| Methods                   | in  | Natural     | Language   | Processing, |              | pages |           |     |      |      |      |      |     |
|                           |     |             |            |             |              |       | embedding |     | 45.7 | 45.6 | 0.26 | 0.30 |     |
| 3911–3921,                |     | Brussels,   | Belgium.   | Association |              | for   |           |     |      |      |      |      |     |
| ComputationalLinguistics. |     |             |            |             |              |       | ranodm    |     | 43.0 | 42.8 | 0.53 | 0.70 |     |
Roberta-SNLI
| Tao Yu, | Rui Zhang,  | Michihiro |      | Yasunaga,  | Yi  | Chern |       |     |      |      |      |      |     |
| ------- | ----------- | --------- | ---- | ---------- | --- | ----- | ----- | --- | ---- | ---- | ---- | ---- | --- |
|         |             |           |      |            |     |       | human |     | 74.5 | 74.1 | 0.48 | 0.61 |     |
| Tan,    | Xi Victoria | Lin,      | Suyi | Li, Heyang | Er, | Irene |       |     |      |      |      |      |     |
Li, Bo Pang, Tao Chen, Emily Ji, Shreya Dixit, embedding 56.7 66.0 0.75 0.37
DavidProctor,SungrokShim,JonathanKraft,Vin-
|                      |     |         |                       |         |         |     | ranodm       |     | 31.2 | 30.9 | 0.78 | 0.64 |     |
| -------------------- | --- | ------- | --------------------- | ------- | ------- | --- | ------------ | --- | ---- | ---- | ---- | ---- | --- |
| cent Zhang,          |     | Caiming | Xiong,                | Richard | Socher, | and |              |     |      |      |      |      |     |
| DragomirRadev.2019b. |     |         | SParC:Cross-domainse- |         |         |     | Roberta-MNLI |     |      |      |      |      |     |
mantic parsing in context. In Proceedings of the human 77.1 76.4 0.86 0.36
| 57th | Annual | Meeting | of the | Association | for | Com- |           |     |      |      |      |      |     |
| ---- | ------ | ------- | ------ | ----------- | --- | ---- | --------- | --- | ---- | ---- | ---- | ---- | --- |
|      |        |         |        |             |     |      | embedding |     | 52.2 | 58.7 | 0.34 | 0.69 |     |
putationalLinguistics,pages4511–4523,Florence,
|     |     |     |     |     |     |     | ranodm |     | 16.5 | 14.8 | 0.50 | 0.49 |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ---- | ---- | ---- | ---- | --- |
Italy.AssociationforComputationalLinguistics.
Jichuan Zeng, Xi Victoria Lin, Caiming Xiong, Table7:Averagefowardentailmentscoree ,backward
1
Richard Socher, Michael R Lyu, Irwin King, entaile ,andcorrespondingstandarddeviationsacross
2
and Steven CH Hoi. 2020. Photon: A robust 9settings. Inallhumanannotationcases,higherentail-
cross-domain text-to-sql system. arXiv preprint mentisbetter. Inallrandomreplacementcases,lower
arXiv:2007.15280.
isbetter.
| Rui Zhang, | Tao           | Yu,      | Heyang | Er, Sungrok  |            | Shim,  |                |     |           |         |      |              |         |
| ---------- | ------------- | -------- | ------ | ------------ | ---------- | ------ | -------------- | --- | --------- | ------- | ---- | ------------ | ------- |
| Eric       | Xue, Xi       | Victoria | Lin,   | Tianze       | Shi,       | Caim-  |                |     |           |         |      |              |         |
|            |               |          |        |              |            |        | Implementation |     | Details   | For     | each | pair         | of tar- |
| ing Xiong, | Richard       | Socher,  |        | and Dragomir |            | Radev. |                |     |           |         |      |              |         |
|            |               |          |        |              |            |        | get column     | and | candidate | column, |      | we contextu- |         |
| 2019.      | Editing-based |          | SQL    | query        | generation | for    |                |     |           |         |      |              |         |
cross-domaincontext-dependentquestions. InPro- alizeeachcolumnwiththetemplatedescribedin
ceedings of the 2019 Conference on Empirical Premise-HypothesisConstructionfromsection§4.
Methods in Natural Language Processing and the Thenwiththecontextualizedtargetcolumnasthe
9thInternationalJointConferenceonNaturalLan-
premiseandthecontextualizedRPLcandidateas
guageProcessing(EMNLP-IJCNLP),pages5338–
5349, Hong Kong, China. Association for Compu- thehypothesis,theNLImodelcomputesbothfor-
|     |     |     |     |     |     |     | ward entailment |     | score | e1 and | backward | score | e2. |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ----- | ------ | -------- | ----- | --- |
tationalLinguistics.

|     |     |     | RPL Annotations  |     |     |     |     | ADD Annotations  |     |     |     |
| --- | --- | --- | ---------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- |
Date of birth Abandoned yes or no Date arrived Date departed Singer name Album name Citizenship Net work millions
Birthday Abandoned ? When reached Time left Composer name Song name Issue region Total downloads
Born day Time of arrival Time of Departure Director name Genre name Home address Best sale amounts
|     | Born time |     | Is abandoned | Arrived at |     | Left at |                     |             |               |             |     |
| --- | --------- | --- | ------------ | ---------- | --- | ------- | ------------------- | ----------- | ------------- | ----------- | --- |
|     |           |     |              |            |     |         | Artist manager name | Song number | Passport type | Total works |     |
First name Last name Cell number Homepage Country Code Continent Population GNP
|     |            |     |             | Tel.     |     | Website | Government code | Industry | Households | Currency |     |
| --- | ---------- | --- | ----------- | -------- | --- | ------- | --------------- | -------- | ---------- | -------- | --- |
|     | Given name |     | Family name | Mobile # |     | Webpage |                 |          |            |          |     |
Forename Surname State name Geographical measure Density Total oil consumption
|     |     |     |     | Phone No. | Personal site URL |     | Zipcode | Longitude | Core city population | Net oil export |     |
| --- | --- | --- | --- | --------- | ----------------- | --- | ------- | --------- | -------------------- | -------------- | --- |
Movie name Air date Directed by Written by Venue Home team Opponent High points
|     |     |     | Release time | Director |     | Author |     |     |     |     |     |
| --- | --- | --- | ------------ | -------- | --- | ------ | --- | --- | --- | --- | --- |
Movie Title Country Home or away Opponent score Point per game
Title Initial release day Conductor Authored by Final position Home team score Opponent avg. rank Average points
|     |     |     | First show time | Conducted by |     | Writer | Round | Home stadium | Champion | Goal per game |     |
| --- | --- | --- | --------------- | ------------ | --- | ------ | ----- | ------------ | -------- | ------------- | --- |
Figure3: RPLandADDannotationexamplesfromourATPbenchmark. Rowswithshallowcolorsareoriginal
headers,whereasthosedeep-shadedonesareourhumanannotations.
Noticethate2computationtakesthecontextualized surpassesothermodelsinverbaldexterity: theen-
RPLcandidateaspremiseandthecontextualized tailmentscorecorrelatesbestwithtruedegreesof
| target column |     | as hypothesis |     | in input. | We  | obtain | substitutability. |     |     |     |     |
| ------------- | --- | ------------- | --- | --------- | --- | ------ | ----------------- | --- | --- | --- | --- |
entailmentscoresfrombothdirectionsbecauseof
theobservedscorefluctuationcausedbyreversion
|     |     |     |     |     |     |     | Approach |     |     |     | ρ   |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
inpracticablecases.
|     |     |     |     |     |     |     | Word2Vec(Mikolovetal.,2013) |     |     |     | 0.37 |
| --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | ---- |
|     |     |     |     |     |     |     | Glove(Penningtonetal.,2014) |     |     |     | 0.41 |
Pilot Study for Model Ability We carry out a Glove+Counter-fitting(Mrksicetal.,2016) 0.58
|             |     |          |         |            |     |         | NMTEmedding(Hilletal.,2015a)     |     |     |     | 0.58 |
| ----------- | --- | -------- | ------- | ---------- | --- | ------- | -------------------------------- | --- | --- | --- | ---- |
| pilot study | to  | test NLI | models’ | capability |     | of dif- |                                  |     |     |     |      |
|             |     |          |         |            |     |         | aragram-SL999(Wietingetal.,2015) |     |     |     | 0.69 |
ferentiatingsemanticequivalencyandsimilarityin
|              |                                |     |     |     |     |     | RoBERTa-MNLI(ours) |     |     |     | 0.70 |
| ------------ | ------------------------------ | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | ---- |
| thissection. | RoBERTa(Liuetal.,2019)ischosen |     |     |     |     |     |                    |     |     |     |      |
asthebackbonemodelduetoitsoutstandingperfor- Table 8: Results on SimLex-999. ρ ( Perason correla-
tion)isusedastheprimarymetric.
manceandcomputationalefficiencyacrossvarious
| NLIdatasets. |               | Fine-tunedRoBERTaonthreewell- |     |        |         |        |                         |     |     |                 |     |
| ------------ | ------------- | ----------------------------- | --- | ------ | ------- | ------ | ----------------------- | --- | --- | --------------- | --- |
|              |               |                               |     |        |         |        | PerformanceonSimLex-999 |     |     | SimLex-999(Hill |     |
| known        | NLI datasets: |                               | RTE | (Dagan | et al., | 2013), |                         |     |     |                 |     |
etal.,2015b)isagoldstandardresourceformea-
SNLI(Bowmanetal.,2015),andMNLI(Williams
et al., 2017) are compared to demonstrate model suringhowwellmodelscapturesimilarity,rather
thanrelatednessorassociationbetweenainputpair
abilitydifferenceduetotrainingdata,.
|              |          |            |        |                      |     |           | ofwords(e.g.              | cold | andhotarecloselyassociated |                         |     |
| ------------ | -------- | ---------- | ------ | -------------------- | --- | --------- | ------------------------- | ---- | -------------------------- | ----------------------- | --- |
| We           | consider | three      | levels | of substitutability, |     |           |                           |      |                            |                         |     |
|              |          |            |        |                      |     |           | butdefinitelynotsimilar). |      |                            | Thusitisespeciallysuit- |     |
| from highest |          | to lowest: | human  | manual               |     | substitu- |                           |      |                            |                         |     |
ableforourpurposeoffurthertestingRoBERTa-
tion(human-annotatedreplacementssampledfrom
|           |     |           |     |                 |     |      | MNLI’s | ability of | semantic | discrimination. | We  |
| --------- | --- | --------- | --- | --------------- | --- | ---- | ------ | ---------- | -------- | --------------- | --- |
| benchmark | RPL | subsets), |     | embedding-based |     | sub- |        |            |          |                 |     |
treattheentailmentscoreproducedbythemodel
| stitution | (top-10 | similar | multi-grams |     | from | Con- |     |     |     |     |     |
| --------- | ------- | ------- | ----------- | --- | ---- | ---- | --- | --- | --- | --- | --- |
asitsjudgmentofsemanticsimilarityandreportits
| ceptNet | Numberbatch |     | word | embedding |     | (Speer |     |     |     |     |     |
| ------- | ----------- | --- | ---- | --------- | --- | ------ | --- | --- | --- | --- | --- |
Pearsoncorrelationagainstthegroundtruthsimi-
etal.,2017)),andrandomsubstitution(randomly
|         |         |        |                 |     |     |         | larityscore. | ResultssuggestthatRoBERTa-MNLI |     |     |     |
| ------- | ------- | ------ | --------------- | --- | --- | ------- | ------------ | ------------------------------ | --- | --- | --- |
| sampled | columns | across | benchmark(Speer |     |     | et al., |              |                                |     |     |     |
isquitecompetitiveatdiscriminatingassociation
| 2017)). | Practically, |     | we randomly |     | sample | 1000 |     |     |     |     |     |
| ------- | ------------ | --- | ----------- | --- | ------ | ---- | --- | --- | --- | --- | --- |
andrelatednessfromsimilarity.
pairsofdataeachtimeandrepeateachsettingfive
times.
|     |     |     |     |     |     |     | CaseStudy | Totestthehardcaseperformanceof |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------------------------------ | --- | --- | --- |
Wereportthebothaverageforwarde andback- RoBERTa-MNLI, we come up with some tricky
1
ward entailment scores e , as well their standard examplesasshowninTable9. Theupperhalfof
2
deviations for each setting across five runs (table thetablepresentshardreplaceablecasesthatem-
7). ItisimmediatelyobviousthatRoBERTa-MNLI phasize idiomatic transformations or word-sense

disambiguation. The lower half contains hard ir- Humanevaluation Werandomlysample100ta-
replaceable cases in which phrases have a high blesfromourbenchmarkandaskthreevendorsto
degree of conceptual association, yet still not se- ratethereasonabilityofeachpredictedTPEfroma
mantically equivalent. Results reveal the surpris- scaleof1−5. 1astotallyunreasonable,3asmildly
ingly abundant and accurate lexicon knowledge acceptable,and5asperfectlyparallelwithhuman
condensedinRoBERTa-MNLI. guesses. Weaverageouttheratingfromallthree
|         |     |     |            |     |     |         | vendorsandgetaresultof4.13. |     |     |     | Thisindicatesthe |     |
| ------- | --- | --- | ---------- | --- | --- | ------- | --------------------------- | --- | --- | --- | ---------------- | --- |
| Premise |     |     | Hypothesis |     | ENT | NON-ENT |                             |     |     |     |                  |     |
practicabilityofzero-shotTPEclassification.
Replaceable
| Runner-up. |     |     | Secondplace. |     | 97.1 | 2.9 |     |     |     |     |     |     |
| ---------- | --- | --- | ------------ | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
B.3 PerturbationCaseStudy
| Firstname.      |     |     | Givenname.          |     | 93.7 | 6.3  |                 |             |         |           |        |           |
| --------------- | --- | --- | ------------------- | --- | ---- | ---- | --------------- | ----------- | ------- | --------- | ------ | --------- |
| Airlinecode.    |     |     | Airlinenumber.      |     | 82.3 | 17.7 |                 |             |         |           |        |           |
|                 |     |     |                     |     | 91.4 | 8.6  | In this         | section, we | present | a case    | study  | on adver- |
| Cartoonairdate. |     |     | Cartoonreleasetime. |     |      |      |                 |             |         |           |        |           |
| Bookauthor.     |     |     | Bookwrittenby.      |     | 97.8 | 2.2  |                 |             |         |           |        |           |
|                 |     |     |                     |     |      |      | sarial training | examples    |         | generated | by CTA | and       |
Irreplaceable
|                |     |     |                  |     |      |      | baselineapproachesinTable10. |               |     |         | Wecanmakethe |         |
| -------------- | --- | --- | ---------------- | --- | ---- | ---- | ---------------------------- | ------------- | --- | ------- | ------------ | ------- |
| Studentheight. |     |     | Studentaltitude. |     | 26.9 | 73.1 |                              |               |     |         |              |         |
|                |     |     |                  |     |      |      | following                    | observations: |     | (i) CTA | tend to      | produce |
| Companysales.  |     |     | Companyprofits.  |     | 1.9  | 98.1 |                              |               |     |         |              |         |
|                |     |     |                  |     | 2.1  | 97.9 |                              |               |     |         |              |         |
Peoplekilled. Peopleinjured. lesslow-frequencywords(e.g. padrone,neosurre-
| Populationnumber. |     |     | Populationcode. |     | 37.1 | 62.9 |     |     |     |     |     |     |
| ----------------- | --- | --- | --------------- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
Politicalparty. Politicalcelebration. 27.5 72.5 alist)inbothRPLandADDi.e. lowerperplexity.
(ii)CTA-generatedsamplesfitbetterwiththespeci-
Table 9: Hard cases we come up with to explore ficity level of table columns. For example, RPL
| upper-boundsofRoberta-MNLIability. |     |     |     |     | ENTasentai- |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
pair(region,sphere)isoverlybroadened,whereas
mentscore,NON-ENTascontradiction+neutralscore.
namessuchballadsdenomination,supermanager,
Scoreofexpectedlabelisbolded.
|     |     |     |     |     |     |     | thespian     | might | be overly | specified    | to fit   | into ta- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | --------- | ------------ | -------- | -------- |
|     |     |     |     |     |     |     | ble headers. | (iii) | CTA       | incurs least | semantic | drift    |
B.2 Zero-shotTPEClassification in RPL. In all baseline methods, there is a good
chancetoobservesemantic-distinctivepairssuch
Webuildthepreviouspremise-hypothesisconstruc-
|     |     |     |     |     |     |     | as (region, | member), | (type, | number), | (type, | guy). |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | ------ | -------- | ------ | ----- |
tionin§4.4basedontheassumptionofavailability
WithCTA,suchriskisminimal.
| of TPE, | which      | is  | frequently | not        | true. | Thus our |     |     |     |     |     |     |
| ------- | ---------- | --- | ---------- | ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- |
| goal    | is to make | a   | reasonable | prediction |       | on TPE   |     |     |     |     |     |     |
C ExperimentalDetails
| forthosemissingcases. |     |     |     | Practically,wemakeuse |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
HuggingFace (Wolf et al., 2020) implementation C.1 OriginalDatasetsstatistics
| of zero-shot |         | text | classification | (Yin    | et          | al., 2019) |                    |            |     |                     |     |          |
| ------------ | ------- | ---- | -------------- | ------- | ----------- | ---------- | ------------------ | ---------- | --- | ------------------- | --- | -------- |
|              |         |      |                |         |             |            | The detail         | statistics | of  | five Text-to-SQL    |     | datasets |
| to classify  | missing |      | TPE            | into 48 | pre-defined | cate-      |                    |            |     |                     |     |          |
|              |         |      |                |         |             |            | areshowninTable11. |            |     | AccordingtoCoSQL(Yu |     |          |
gorieswiththeinputofconcatenatedtablecaption,
etal.,2019a)andSParC(Yuetal.,2019b)paper,
columns,andcellvalues.
thetwomulti-turnText-to-SQLdatasetssharethe
ImplementationDetails Basedonthe60+fine- sametableswithSpider(Yuetal.,2018).
| grained | categories |     | defined | in Few-NERD |     | (Ding |     |     |     |     |     |     |
| ------- | ---------- | --- | ------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
et al., 2021), We modify and integrate them into C.2 BaselineDetails
48classesascandidatelabels(|L| = 48). Witha SQLova ForalldefenseresultsoftheWikiSQL
Roberta-MNLIastheworkhorsemodel,ouroverall dataset,weemploytheSQLovamodel,whoseof-
modelingprocessismodeledas
|     |     |     |     |     |     |     | ficial codes | are     | released   | in (Hwang | et al.,      | 2019). |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | ---------- | --------- | ------------ | ------ |
|     |     |     |     |     |     |     | We use       | uncased | BERT-large | as        | the encoder. | The    |
exp(f (L |d;c;v;d) ) learning rate is 1×10−3 and the learning rate of
|      |        |          | θ   | i   |     | ent |     |     |     |     |     |     |
| ---- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c˜ = | argmax | (cid:80) |     |     |     |     |     |     |     |     |     |     |
t exp(f (L |d;c;v) ) BERT-largeis1×10−5. Thetrainingepochis30
|     | i   |     | j∈|L| | θ   | j   | ent |                     |     |     |                         |     |     |
| --- | --- | --- | ----- | --- | --- | --- | ------------------- | --- | --- | ----------------------- | --- | --- |
|     |     |     |       |     |     |     | withabatchsizeof12. |     |     | Thetrainingprocesslasts |     |     |
whereciscolumnnames,visarandomlyselected
12hoursonasingle16GBTeslaV100GPU.
columnvalueaffiliatedwithagivencolumn,andd
istablecaptionsforagiventable. Roberta-MNLI SQUALL WeemploytheSQUALLmodel,fol-
(annotated as f θ ) outputs raw logits of contradic- lowing(Shietal.,2020),togetalldefenseresults
tion,neutral,andentailmentscores. Softmaxisfi- oftheWTQdataset. Thetrainingepochis20with
nallyappliedentailmentlogitsacross48categories, a batch size of 30; The dropout rate is 0.2; The
withthetop1labelasfinaltheprimaryentitypre- training process lasts 9 hours on a single 16GB
| diction. |     |     |     |     |     |     | TeslaV100GPU. |     |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- |

|     | Perturbation |     | TableContext |     | BA       |     | TF        |     | W2V       |     | CTA      |     |
| --- | ------------ | --- | ------------ | --- | -------- | --- | --------- | --- | --------- | --- | -------- | --- |
|     |              |     | clubid       |     | member   |     | districts |     | regionary |     | place    |     |
|     |              |     | region       |     | regional |     | zones     |     | location  |     | location |     |
|     |              |     | name         |     | district |     | sphere    |     | regions   |     | district |     |
RPL
|     |     |     | authorid |     | types      |     | guy                 |     | typeful    |     | category  |     |
| --- | --- | --- | -------- | --- | ---------- | --- | ------------------- | --- | ---------- | --- | --------- | --- |
|     |     |     | type     |     | number     |     | genus               |     | example    |     | genre     |     |
|     |     |     | title    |     | style      |     | categories          |     | sort       |     | kind      |     |
|     |     |     | singerid |     | songstitle |     | balladsdenomination |     | name       |     | musicname |     |
|     |     |     | songname |     | singername |     | balladsappointments |     | polynymous |     | songtitle |     |
country chorusname songdesignation folk-songname musicdesignation
|     |     |     | courseid  |     | classes |     | sophomore |     | studential    |     | school     |     |
| --- | --- | --- | --------- | --- | ------- | --- | --------- | --- | ------------- | --- | ---------- | --- |
|     |     |     | semester  |     | honors  |     | majoring  |     | intersession  |     | enrollment |     |
|     |     |     | sectionid |     | session |     | freshman  |     | undergraduate |     | university |     |
ADD
|     |     |     | artistid |     | composition |     | musicianship |     | tachiste        |     | publisher |     |
| --- | --- | --- | -------- | --- | ----------- | --- | ------------ | --- | --------------- | --- | --------- | --- |
|     |     |     | artist   |     | creator     |     | thespian     |     | neosurrealist   |     | album     |     |
|     |     |     | age      |     | design      |     | arranger     |     | creativeperson  |     | genre     |     |
|     |     |     | movieid  |     | designer    |     | officers     |     | corporateleader |     | producer  |     |
|     |     |     | director |     | operator    |     | padrone      |     | supermanager    |     | scenarist |     |
|     |     |     | year     |     | composer    |     | guide        |     | executive       |     | writer    |     |
Table10:AdversarialtrainingexamplesgeneratedbyCTAandbaselineapproaches. Wordswithredcolorfontare
targetcolumns.
|     |     |     | Train |     |     | Dev |     | Dataset | Baseline | Dev | RPL | ADD |
| --- | --- | --- | ----- | --- | --- | --- | --- | ------- | -------- | --- | --- | --- |
Datasets
|     |     | #T  | #Q  | #Avg.Col | #T  | #Q  | #Avg.Col |     |        |      |          |          |
| --- | --- | --- | --- | -------- | --- | --- | -------- | --- | ------ | ---- | -------- | -------- |
|     |     |     |     |          |     |     |          |     | DuoRAT | 69.9 | 23.8±2.1 | 36.4±1.3 |
Spider
WTQ 1,290 9,030 6.39 327 2,246 6.41 (-46.1/-65.9%) (-33.5/-47.9%)
|         |     |        |        |      |       |       |      |     | ETA | 70.8 | 27.6±1.8       | 39.9±0.9       |
| ------- | --- | ------ | ------ | ---- | ----- | ----- | ---- | --- | --- | ---- | -------------- | -------------- |
| WikiSQL |     | 18,590 | 56,355 | 6.40 | 2,716 | 8,421 | 6.31 |     |     |      |                |                |
|         |     |        |        |      |       |       |      |     |     |      | (-43.2/-61.0%) | (-30.9/-43.6%) |
| Spider  |     | 795    | 6,997  | 5.52 | 81    | 1,034 | 5.45 |     |     |      |                |                |
CoSQL 795 9,478 5.52 81 1,299 5.45 SQLova 81.6 27.2±1.3 66.2±2.3
| SParC |     | 795      | 12,011   | 5.52        | 81  | 1,625         | 5.45 | WikiSQL |       |      |                |                |
| ----- | --- | -------- | -------- | ----------- | --- | ------------- | ---- | ------- | ----- | ---- | -------------- | -------------- |
|       |     |          |          |             |     |               |      |         |       |      | (-54.4/-66.7%) | (-15.4/-18.9%) |
|       |     |          |          |             |     |               |      |         | CESQL | 84.3 | 52.2±0.9       | 71.2±1.5       |
|       |     |          |          |             |     |               |      |         |       |      | (-32.1/-38.1%) | (-13.1/-15.5%) |
| Table | 11: | Original | datasets | statistics. |     | #T represents |      |         |       |      |                |                |
total number of tables in a dataset (#Q for questions). WTQ SQUALL 44.1 22.8±0.5 32.9±0.8
|     |     |     |     |     |     |     |     |     |     |     | (-21.3/-48.3%) | (-11.2/-25.4%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | -------------- |
#Avg. Colstandsforavg.
numberofcolumnspertable.
|     |     |     |     |     |     |     |     |     | EditSQL | 39.9 | 13.3±0.7 | 30.5±1.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---- | -------- | -------- |
Spider,CoSQLandSParCsharethesametables.
|     |     |     |     |     |     |     |     | CoSQL |     |      | (-26.6/-66.7%) | (-9.4/-23.6%) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ---- | -------------- | ------------- |
|     |     |     |     |     |     |     |     |       |     | 44.1 | 16.4±1.2       | 32.8±2.1      |
IGSQL
|     |     |     |     |     |     |     |     |     |     |     | (-27.7/-62.8%) | (-11.3/-25.6%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | -------------- |
ETA We implement the ETA model following EditSQL 47.2 30.5±0.9 40.2±1.2
|     |     |     |     |     |     |     |     | SParC |     |     | (-16.7/-35.4%) | (-7.0/-14.8%) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | -------------- | ------------- |
(Liuetal.,2021). WeuseanuncasedBERT-large IGSQL 50.7 34.2±0.5 42.9±1.7
wholewordmaskingversionastheencoder. The (-16.5/-32.5%) (-7.8/-15.4%)
| learningrateis5×10−5 |     |     |     | andthetrainingepochis |     |     |     |           |           |       |          |               |
| -------------------- | --- | --- | --- | --------------------- | --- | --- | --- | --------- | --------- | ----- | -------- | ------------- |
|                      |     |     |     |                       |     |     |     | Table 12: | The Exact | Match | Accuracy | on the devel- |
50. Thebatchsizeandgradientaccumulationsteps
|     |     |     |     |     |     |     |     | opment | set and ADVETA. |     | Red font | denotes the abso- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --------------- | --- | -------- | ----------------- |
are6and4. Thetrainingprocesslasts24hourson lute(left)andrelative(right)performancedroppercent-
asingle32GBTeslaV100GPU.
agecomparedwithoriginaldevaccuracy.
C.3 AttackPerformanceCalculationDetails
relativepercentagedrop(25.6%)forADDpertur-
Table12showstheattackperformanceofRPLand
bation.
| ADD         | perturbations. |         |     | In this      | section, | we show | the      |     |                          |     |     |     |
| ----------- | -------------- | ------- | --- | ------------ | -------- | ------- | -------- | --- | ------------------------ | --- | --- | --- |
| calculation |                | details | of  | the average  |          | attack  | relative |     |                          |     |     |     |
|             |                |         |     |              |          |         |          | C.4 | SchemaLinkingCalculation |     |     |     |
| performance |                | drop.   |     | For example, |          | on the  | Spider   |     |                          |     |     |     |
dataset,therelativeperformancedropoftheDuo- WefollowtheworkofLiuetal.(2021)tomeasure
RATmodelagainstRPLperturbationis65.9%,and the performance of ETA schema linking predic-
61.0%fortheETAmodel. ForRPLperturbation, tions. LetΩ beaset{(c,q) |1 ≤ i ≤ N}which
|     |     |     |     |     |     |     |     |     | col |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
weaverageouttherelativeperformancedropof9 contains N gold (column-question token) tuples.
modelsandreporttheaveragerelativepercentage Let Ω be a set {(c,q) |1 ≤ j ≤ M} which
|     |     |     |     |     |     |     |     |     | col |     | j   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
drop (53.1%). Same as RPL, we get the average containsM predicted(column-questiontoken)tu-

ples. Wedefinetheprecision(Col ),recall(Col ),
P R
F1-score(Col )as:
F
|Γ | |Γ | 2Col Col
col col P R
, ,
(cid:12) (cid:12)
(cid:12)Ω col(cid:12) |Ω col | Col P +Col R
(cid:84)
whereΓ = Ω Ω . ThedefinitionsofTab ,
col col col P
Tab ,Tab aresimilar.
R F
D BaselineApproachDetails
W2V Togeneratecandidatesforagivencolumn,
W2Vrandomlysamplesfivecandidatesfromthe
top15cosine-similar(Numberbatchwordembed-
dings)forRPLand15-50forADD.Textfoolerand
BERT-Attackalsofollowthishyper-parameterset-
ting. For both TextFooler and BERT-Attack, we
skiptheirwordimportanceranking(WIR)modules
whileonlykeepingthewordtransformermodules
forcandidategeneration8.
TextFooler TextFoolerisoneofthestate-of-the-
artattackingframeworksfordiscriminativetasks
onunstructuredtext. Weskipitswordimportance
ranking (WIR) step since our target column has
already been located. Its word transformer mod-
ule is faithfully re-implemented to generate can-
didates for a target column. Counter-fitted word
embedding(Mrksicetal.,2016)areusedforsim-
ilarity computation, and modified sentences are
constrainedbybothPOS-tagconsistencyandSim-
CSE(Gaoetal.,2021)similarityscore.
BERT-Attack BERT-Attackisanotherrepresen-
tative text attacking framework. Similar to our
adaptation of TextFooler, we skip WIR and only
keepthecoremaskedlanguagemodel-basedword
transformation. Following original work, low-
quality or sub-word tokens predicted by BERT-
Large are discarded; perturbed sentence similari-
tiescomparedwiththeoriginalareguaranteedby
Sim-CSE.
8Wecontextualizecolumnswithtemplatesthataddition-
allyconsiderscellvaluesandPOS-tagconsistency.