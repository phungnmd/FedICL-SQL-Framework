|     | Spider: |     | A            | Large-Scale |          |               | Human-Labeled |         |            | Dataset           | for             | Complex             | and           |     |
| --- | ------- | --- | ------------ | ----------- | -------- | ------------- | ------------- | ------- | ---------- | ----------------- | --------------- | ------------------- | ------------- | --- |
|     |         |     | Cross-Domain |             |          | Semantic      |               | Parsing |            | and Text-to-SQL   |                 | Task                |               |     |
|     |         |     | TaoYu        |             | RuiZhang |               |               | KaiYang |            | MichihiroYasunaga |                 |                     |               |     |
|     |         |     |              | DongxuWang  |          |               | ZifanLi       |         | JamesMa    |                   | IreneLi         |                     |               |     |
|     |         |     |              |             |          |               |               |         | ID         | department_code   |                 | course_description  | course_credit |     |
|     |         |     | QingningYao  |             |          | ShanelleRoman |               |         | ZilinZhang |                   | DragomirR.Radev |                     |               |     |
DepartmentofComputerScience,YaleUniversity
course_codedepartment_code course_description course_credit
{tao.yu,r.zhang,k.yang,michihiro.yasunaga,dragomir.radev}@yale.edu
Annotators check database schema    (e.g., database: college)
Annotators check database schema   (e.g., database: college)
| Table name |                                        |     | ColumAnsbstract |     |                         |     |         |     |     |            |     |         |     |     |
| ---------- | -------------------------------------- | --- | --------------- | --- | ----------------------- | --- | ------- | --- | --- | ---------- | --- | ------- | --- | --- |
|            |                                        |     |                 |     |                         |     |         |     |     | Table name |     | Columns |     |     |
|            | WIDenapmeresdeenpatrtSmpeindte_rn,amea |     |                 |     | slaalragrey- s.c...ale, |     | complex |     |     |            |     |         |     |     |
Table 1 instructor
|     |     |     |     |     |     |     |     |     | Table 1 | instructor |     |     | salary .... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---------- | --- | --- | ----------- | --- |
and cross-domaifnoresiegmn kaenytic parsing and text- idname department_id
9102 beF 2  ]LC.sc[  5v78880.9081:viXra to - S Q L d a t a s e t anno ta te d by.....1..1 college stu- foreign key
| Table 2 department | n a | m e b | u i l d i n g | bu dg | e t  |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | ----- | ------------- | ----- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
pd rie mn a rt sy  . k e y I t c o n s i s t s o f 1 0 ,1 8 1 q u e s t i o n s an d Tab le 2 department i d name building budget  .......
......
|     | 5 , 6 | 9 3 u n | i q u e c o | m p l e x | S Q L | q u e r i e | s o n 2 | 0 0 | ...... |     | pr  | i m ar y |     |     |
| --- | ----- | ------- | ----------- | --------- | ----- | ----------- | ------- | --- | ------ | --- | --- | -------- | --- | --- |
k e y
| Tab le n | d a t | a b a s e s | w i t h m | u lt i p le | t a b le | s , c o v e | r i n g 1 | 3 8 |     |     |     |     |     |     |
| -------- | ----- | ----------- | --------- | ----------- | -------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
Table n
| Annotators create:                                                      | different |           | domains.    | We            | define      | a new    | complex   |     |                    |     |     |     |     |     |
| ----------------------------------------------------------------------- | --------- | --------- | ----------- | ------------- | ----------- | -------- | --------- | --- | ------------------ | --- | --- | --- | --- | --- |
|                                                                         | a n d     | c r o s s | - d o m a i | n s e m       | a n ti c p  | a r sing | and text- |     | Annotators create: |     |     |     |     |     |
| Complex What are the                                                    |   n am    | e   a n d |  b u d ge t |   of t h e  d | e pa r tm e | nt s     |           |     |                    |     |     |     |     |     |
| with averageto in-SstQruLctort assaklaryw ghreearteer dthiaffne trheent |           |           |             |               |             | complex  | SQL       |     |                    |     |     |     |     |     |
question Complex What are the name and budget of the departments
overall averaqguee?ries with average instructor salary greater than the
|     |     | and | databases |     | appear | in train | and test |     | question |     |     |     |     |     |
| --- | --- | --- | --------- | --- | ------ | -------- | -------- | --- | -------- | --- | --- | --- | --- | --- |
overall average?
| Complex SELECT T1.sdeetpsa.rtInmetnhti_snwamaey,, Tth2e.btuadsgketrequires |     |     |     |     |     | the | model |     |     |     |     |     |     |     |
| -------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
SQL
FROM instructor as T1 JOIN department as Complex SELECT T2.name, T2.budget
|     | t o g | e n e r a | l i z e w e | l l to b | o t h new | SQL | queries |     | SQL |     |     |     |     |     |
| --- | ----- | --------- | ----------- | -------- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
T2 ON T1.d e pa r t m e n t _ n a me   =   T2 .n am e   FROM instructor as T1 JOIN department as
GROUP BY Ta1n.ddenpeawrtmdeantta_bnaasmeeschemas. Spider is distinct T2 ON T1.department_id = T2.id
HAVING avgf(rTo1m.samlaorsyt)o >f the previous semantic parsing GROUP BY T1.department_id
     (SELECT avg(salary) FROM instructor) HAVING avg(T1.salary) >
|     | tasks | because | they | all | use a | single | database |     |     |     |     |     |     |     |
| --- | ----- | ------- | ---- | --- | ----- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
    (SELECT avg(salary) FROM instructor)
|     | and | the exact | same | programs |            | in the | train | set |          |                                       |     |     |     |     |
| --- | --- | --------- | ---- | -------- | ---------- | ------ | ----- | --- | -------- | ------------------------------------- | --- | --- | --- | --- |
|     |     |           |      |          |            |        |       |     | Figure1: | Ourcorpusannotatescomplexquestionsand |     |     |     |     |
|     | and | the test  | set. | We       | experiment | with   | vari- |     |          |                                       |     |     |     |     |
SQLs.Theexamplecontainsjoiningofmultipletables,
ousstate-of-the-artmodelsandthebestmodel
|     |          |      |            |       |          |          |       |     | aGROUP | BYcomponent,andanestedquery. |     |     |     |     |
| --- | -------- | ---- | ---------- | ----- | -------- | -------- | ----- | --- | ------ | ---------------------------- | --- | --- | --- | --- |
|     | achieves |      | only 12.4% |       | exact    | matching | accu- |     |        |                              |     |     |     |     |
|     | racy     | on a | database   | split | setting. | This     | shows |     |        |                              |     |     |     |     |
thatSpiderpresentsastrongchallengeforfu- ratherthansemanticparsing. Existingdatasetsfor
|     |      |           |     |         |     |      |          |     | SP have | two | shortcomings. | First, | those that have |     |
| --- | ---- | --------- | --- | ------- | --- | ---- | -------- | --- | ------- | --- | ------------- | ------ | --------------- | --- |
|     | ture | research. | Our | dataset | and | task | are pub- |     |         |     |               |        |                 |     |
Database Collectionli calnyd aCvraeilaatbiolen at https://yQaluees-tlioinl ayn.d SQL Ancnoomtaptiloenx  programs (Zelle and Mooney, 1996; Li
200 databasgesi (tDhBu) b.io/spider. 20-50 examples pear nDdB Jagadish,
|                |     |     |     |     |     |     |                |     |     |     | 2014; | Yaghmazadeh | et al., 2017a; |     |
| -------------- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- | ----- | ----------- | -------------- | --- |
| 150 man-hours  |     |     |     |     |     |     | 500 man-hours  |     |     |     |       |             |                |     |
Iyeretal.,2017)aretoosmallintermsofthenum-
1 Introduction
berofprogramsfortrainingmoderndata-intensive
Semanticparsing(SP)isoneofthemostimportant models and have only a single dataset, meaning
SQL Review  taQskusesintionna tRuervailelwa nagnuda Pgaerapprhorcaesses ing (NFiLnPal) .RIetvrieew- andt hPartoctheesssinagm e database is used for both training
150 man-hours  quires both15u0n dmearns-thaonudrisn g the meaning of nat1u5r0a lman-haonudrste stingthemodel. Moreimportantly,thenum-
language sentences and mapping them to mean- ber of logic forms or SQL labels is small and
ingful executable queries such as logical forms, each program has about 4-10 paraphrases of nat-
SQLqueries,andPythoncode. ural language problem to expand the size of the
| Database Collection  |     | Question and SQL |     |     |     |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Recently, some state-of-the-art methods with dataset. Therefore,theexactsametargetprograms
| & Creation  |     | Annotation  |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Seq2Seq architectures are able to achieve over appear in both the train and test sets. The mod-
| 200 databases (DB)  |     | 20-50 examples per DB  |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
150 man-hours  80%exact5m00a tmchanin-hgoaucrsc uracyevenonsomecom- elscanachievedecentperformancesevenonvery
plex benchmarks such as ATIS and GeoQuery. complex programs by memorizing the patterns of
These models seem to have already solved most questionandprogrampairsduringtrainingandde-
Questiporno RbelevmiewsinthisFifineall dR.eview & coding the programs exactly the same way as it
SQL Review
& Paraphrase  However,previoustasksinthisfieldhaveasim- Processing  saw in the training set during testing. Finegan-
150 man-hours
| 150 man-hours  |     |     | 150 man-hours  |     |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
plebutproblematictaskdefinitionbecausemostof Dollak et al. (2018) split the dataset by programs
theseresultsarepredictedbysemantic“matching” sothatnotwoidenticalprogramswouldbeinboth

the train and test sets. They show that the models defines a new semantic parsing task in which the
built on this question-splitting data setting fail to model needs to generalize not only to new pro-
generalize to unseen programs. Second, existing grams but also to new databases. Models have to
datasets that are large in terms of the number of takequestionsanddatabaseschemasasinputsand
programsanddatabasessuchasWikiSQL(Zhong predictunseenqueriesonnewdatabases.
etal.,2017)containonlysimpleSQLqueriesand Toassessthetaskdifficulty,weexperimentwith
single tables. In order to test a model’s real se- several state-of-the-art semantic parsing models.
mantic parsing performance on unseen complex Allofthemstrugglewiththistask. Thebestmodel
programs and its ability to generalize to new do- achieves only 12.4% exact matching accuracy in
mains, an SP dataset that includes a large amount the database split setting. This suggests that there
ofcomplexprogramsanddatabaseswithmultiple isalargeroomforimprovement.
tablesisamust.
2 RelatedWorkandExistingDatasets
However, compared to other large, realistic
datasets such as ImageNet for object recognition
Several semantic parsing datasets with different
(Deng et al., 2009) and SQuAD for reading com-
queries have been created. The output can be in
prehension (Rajpurkar et al., 2016), creating such
many formats, e.g., logic forms. These datasets
SPdatasetisevenmoretime-consumingandchal-
includeATIS(Price,1990;Dahletal.,1994),Geo-
lenging in some aspects due to the following rea-
Query(ZelleandMooney,1996),andJOBS(Tang
sons. First, it is hard to find many databases
and Mooney, 2001a). They have been studied ex-
with multiple tables online. Second, given a
tensively (Zelle and Mooney, 1996; Zettlemoyer
database, annotators have to understand the com-
and Collins, 2005; Wong and Mooney, 2007; Das
plex database schema to create a set of questions
et al., 2010; Liang et al., 2011; Banarescu et al.,
such that their corresponding SQL queries cover
2013; Artzi and Zettlemoyer, 2013; Reddy et al.,
all SQL patterns. Moreover, it is even more chal-
2014; Berant and Liang, 2014; Dong and Lapata,
lenging to write different complex SQL queries.
2016). However, they are domain specific and
Additionally, reviewing and quality-checking of
there is no standard label guidance for multiple
questionandSQLpairstakesasignificantamount
SQLqueries.
of time. All of these processes require very spe-
Recently, more semantic parsing datasets using
cificknowledgeindatabases.
SQL as programs have been created. Iyer et al.
Toaddresstheneedforalargeandhigh-quality
(2017) and Popescu et al. (2003a) labeled SQL
dataset for a new complex and cross-domain se-
queries for ATIS and GeoQuery datasets. Other
mantic parsing task, we introduce Spider, which
existingtext-to-SQLdatasetsalsoincludeRestau-
consists of 200 databases with multiple tables,
rants (Tang and Mooney, 2001b; Popescu et al.,
10,181 questions, and 5,693 corresponding com-
2003a), Scholar (Iyer et al., 2017), Academic
plex SQL queries, all written by 11 college stu-
(Li and Jagadish, 2014), Yelp and IMDB (Yagh-
dents spending a total of 1,000 man-hours. As
mazadehetal.,2017b),Advising(Finegan-Dollak
Figure1illustrates,givenadatabasewithmultiple
et al., 2018), and WikiSQL (Zhong et al., 2017).
tables including foreign keys, our corpus creates
These datasets have been studied for decades in
andannotatescomplexquestionsandSQLqueries
both the NLP community (Warren and Pereira,
including different SQL clauses such as joining
1982;Popescuetal.,2003b,2004;Lietal.,2006;
and nested query. In order to generate the SQL
Giordani and Moschitti, 2012; Wang et al., 2017;
querygiventheinputquestion,modelsneedtoun-
Iyer et al., 2017; Zhong et al., 2017; Xu et al.,
derstand both the natural language question and
2017; Yu et al., 2018; Huang et al., 2018; Wang
relationships between tables and columns in the
et al., 2018; Dong and Lapata, 2018; McCann
databaseschema.
etal.,2018)andtheDatabasecommunity(Liand
In addition, we also propose a new task for Jagadish, 2014; Yaghmazadeh et al., 2017b). We
the text-to-SQL problem. Since Spider contains provide detailed statistics on these datasets in Ta-
200 databases with foreign keys, we can split the ble1.
dataset with complex SQL queries in a way that Most of the previous work train their models
nodatabaseoverlapsintrainandtest,whichover- withoutschemasasinputsbecausetheyuseasin-
comesthetwoshortcomingsofpriordatasets,and gle database for both training and testing. Thus,

ID department_code course_description course_credit
course_codedepartment_code course_description course_credit
Annotators check database schema (e.g., database: college)
Table name Columns
Table 1 instructor IDname department_name salary ....
foreign key
Table 2 department name building budget .......
...... primary key
Table n
Annotators create:
Complex What are the name and budget of the departments
question with average instructor salary greater than the
overall average?
Complex SELECT T1.department_name, T2.budget
SQL FROM instructor as T1 JOIN department as
T2 ON T1.department_name = T2.name
GROUP BY T1.department_name
HAVING avg(T1.salary) >
(SELECT avg(salary) FROM instructor)
Database Collection and Creation Question and SQL Annotation
200 databases (DB) 20-50 examples per DB
150 man-hours 500 man-hours
SQL Review Question Review and Paraphrase Final Review and Processing
150 man-hours 150 man-hours 150 man-hours
they do not need to generalize to new domains. Database Collection Question and SQL
Most importantly, these datasets have a limited & Creation Annotation
200 databases (DB) 20-50 examples per DB
number of labeled logic forms or SQL queries. 150 man-hours 500 man-hours
In order to expand the size of these datasets and
applyneuralnetworkapproaches,eachlogicform
Question Review Final Review &
or SQL query has about 4-10 paraphrases for the SQL Review
& Paraphrase Processing
150 man-hours
naturallanguageinput. Mostpreviousstudiesfol- 150 man-hours 150 man-hours
lowthestandardquestion-basedtrainandtestsplit
Figure2: TheannotationprocessofourSpidercorpus.
(ZettlemoyerandCollins,2005). Thisway,theex-
act same target queries (with similar paraphrases) into a more general-purpose programming lan-
in the test appear in training set as well. Utiliz- guagesuchasPython(Allamanisetal.,2015;Ling
ing this assumption, existing models can achieve etal.,2016;Rabinovichetal.,2017;YinandNeu-
decent performances even on complex programs big,2017).
by memorizing database-specific SQL templates.
However, this accuracy is artificially inflated be- 3 CorpusConstruction
cause the model merely needs to decide which
All questions and SQL queries were written and
template to use during testing. Finegan-Dollak
reviewed by 11 computer science students. Some
etal.(2018)showthattemplate-basedapproaches
of them were native English speakers. As illus-
can get even higher results. To avoid getting this
trated in Figure 2, we develop our dataset in five
inflated result, Finegan-Dollak et al. (2018) pro-
steps, spending around 1,000 hours of human la-
pose a new, program-based splitting evaluation,
bor in total: §3.1 Database Collection and Cre-
where the exact same queries do not appear in
ation, §3.2 Question and SQL Annotation, §3.3
both training and testing. They show that un-
SQL Review, §3.4 Question Review and Para-
der this framework, the performance of all the
phrase,§3.5FinalQuestionandSQLReview.
current state-of-the-art semantic parsing systems
dropsdramaticallyevenonthesamedatabase,in-
3.1 DatabaseCollectionandCreation
dicatingthatthesemodelsfailtogeneralizetoun-
Collecting databases with complex schemas is
seenqueries. Thisindicatesthatcurrentstudiesin
hard. Although relational databases are widely
semanticparsinghavelimitations.
used in industry and academia, most of them are
We also want the model to generalize not only not publicly available. Only a few databases with
to unseen queries but also to unseen databases. multipletablesareeasilyaccessibleonline.
Zhong et al. (2017) published the WikiSQL Our 200 databases covering 138 different do-
dataset. In their problem definition, the databases mains are collected from three resources. First,
in the test set do not appear in the train or devel- wecollectedabout70complexdatabasesfromdif-
opment sets. Also, the task needs to take differ- ferentcollegedatabasecourses,SQLtutorialweb-
enttableschemasasinputs. Therefore, themodel sites,onlinecsvfiles,andtextbookexamples. Sec-
has to generalize to new databases. However, in ond, we collected about 40 databases from the
order to generate 80654 questions and SQL pairs DatabaseAnswers1wherecontainsover1,000data
for 24241 databases, Zhong et al. (2017) made modelsacrossdifferentdomains. Thesedatamod-
simplifiedassumptionsabouttheSQLqueriesand els contain only database schemas. We converted
databases. Their SQL labels only cover single them into SQLite, populated them using an on-
SELECT column and aggregation, and WHERE line database population tool2, and then manu-
conditions. Moreover, all the databases only con- allycorrectedsomeimportantfieldssothattheta-
tain single tables. No JOIN, GROUP BY, and ble contents looked natural. Finally, we created
ORDER BY,etc. areincluded. the remaining 90 databases based on WikiSQL.
To ensure the domain diversity, we select about
Recently, researchers have constructed some
500 tables in about 90 different domains to cre-
datasets for code generation including IFTTT
ate these 90 databases. To create each database,
(Quirk et al., 2015), DJANGO (Oda et al., 2015),
we chose several related tables from WikiSQL
HEARTHSTONE (Ling et al., 2016), NL2Bash
(Lin et al., 2018), and CoNaLa (Yin et al., 2018). 1http://www.databaseanswers.org/
These tasks parse natural language descriptions 2http://filldb.info/

dev or test splits, and then created a relational First, ambiguous questions refer to the ques-
database schema with foreign keys based on the tionsthatdonothaveenoughcluestoinferwhich
tables we selected. We had to create some inter- columns to return and which conditions to con-
section tables in order to link several tables to- sider. For example, we would not ask “What is
gether. For most other cases, we did not need to the most popular class at University X?” because
populate these databases since tables in WikiSQL the definition of “popular” is not clear: it could
arefromWikipedia,whichalreadyhadrealworld mean the rating of the class or the number of stu-
| datastored. |     |     |     |     |     | dentstakingthecourse. |     |     | Instead,wechoosetoask |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --------------------- | --- | --- | --- |
Wemanuallycorrectedsomedatabaseschemas “What is the name of the class which the largest
|     |     |     |     |     |     | number | of students |     | are taking | at  | University | X?”. |
| --- | --- | --- | --- | --- | --- | ------ | ----------- | --- | ---------- | --- | ---------- | ---- |
iftheyhadsomecolumnnamesthatdidnotmake
sense or missed some foreign keys. For table and Here, “popular” refers to the size of student en-
column names, it is common to use abbreviations rollment. Thus, the “student enrollment” column
in databases. For example, ‘student id’ might be can be used in condition to answer this question.
representedby‘stu id’. Forourtaskdefinition,we We recognize that ambiguous questions appear in
manuallychangedeachcolumnnamebacktoreg- real-worldnaturallanguagedatabaseinterfaces.
ularwordssothatthesystemonlyhandledseman- Weagreethatfutureworkneedstoaddressthis
ticparsingissues. issue by having multi-turn interactions between
|     |     |     |     |     |     | the system | and | users | for clarification. |     |     | However, |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ----- | ------------------ | --- | --- | -------- |
3.2 QuestionandSQLAnnotation ourmainaimhereistodevelopacorpustotackle
theproblemofhandlingcomplexqueriesandgen-
Foreachdatabase,weaskeightcomputerscience
|               |            |          |        |            |             | eralizing               | across    | databases |                  | without     | multi-turn | in-      |
| ------------- | ---------- | -------- | ------ | ---------- | ----------- | ----------------------- | --------- | --------- | ---------------- | ----------- | ---------- | -------- |
| students      | proficient | in       | SQL to | create     | 20-50 natu- |                         |           |           |                  |             |            |          |
|               |            |          |        |            |             | teractions              | required, |           | which            | no existing |            | semantic |
| ral questions | and        | their    | SQL    | labels. To | make our    |                         |           |           |                  |             |            |          |
|               |            |          |        |            |             | parsingdatasetscoulddo. |           |           | Moreover,        |             | thelowper- |          |
| questions     | diverse,   | natural, | and    | reflective | of how      |                         |           |           |                  |             |            |          |
|               |            |          |        |            |             | formances               | of        | current   | state-of-the-art |             | models     | al-      |
humansactuallyusedatabases,wedidnotuseany
|          |           |             |     |          |         | ready show | that      | our | task is    | challenging |           | enough, |
| -------- | --------- | ----------- | --- | -------- | ------- | ---------- | --------- | --- | ---------- | ----------- | --------- | ------- |
| template | or script | to generate |     | question | and SQL |            |           |     |            |             |           |         |
|          |           |             |     |          |         | without    | ambiguous |     | questions. | In          | addition, | ques-   |
queries. Ourannotationprocedureensuresthefol-
|     |     |     |     |     |     | tions are | required | to  | contain | the specific |     | informa- |
| --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ------- | ------------ | --- | -------- |
lowingthreeaspects.
|        |         |           |     |     |             | tion to    | return.    | Otherwise, | we     | don’t    | know  | if class |
| ------ | ------- | --------- | --- | --- | ----------- | ---------- | ---------- | ---------- | ------ | -------- | ----- | -------- |
|        |         |           |     |     |             | id is also | acceptable |            | in the | previous | case. | Most     |
| A) SQL | pattern | coverage. |     | We  | ensure that |            |            |            |        |          |       |          |
our corpus contains enough examples for all of the questions in the existing semantic parsing
|                |     |           |     |                |            | datasetsareambiguous. |     |            | Thisisnotaseriousprob- |         |     |         |
| -------------- | --- | --------- | --- | -------------- | ---------- | --------------------- | --- | ---------- | ---------------------- | ------- | --- | ------- |
| common         | SQL | patterns. | For | each database, | we         |                       |     |            |                        |         |     |         |
|                |     |           |     |                |            | lem if we             | use | one single | dataset                | because |     | we have |
| ask annotators |     | to write  | SQL | queries        | that cover |                       |     |            |                        |         |     |         |
all the following SQL components: SELECT enough data domain specific examples to know
with multiple columns and aggregations, WHERE, whichcolumnsarethedefault. However,itwould
|       |     |         |       |     |        | be a serious | problem |     | in cross | domain | tasks | since |
| ----- | --- | ------- | ----- | --- | ------ | ------------ | ------- | --- | -------- | ------ | ----- | ----- |
| GROUP | BY, | HAVING, | ORDER | BY, | LIMIT, |              |         |     |          |        |       |       |
JOIN, INTERSECT, EXCEPT, UNION, NOT the default return values differ cross domain and
| IN, OR, | AND, | EXISTS, | LIKE | as well | as nested | people. |     |     |     |     |     |     |
| ------- | ---- | ------- | ---- | ------- | --------- | ------- | --- | --- | --- | --- | --- | --- |
queries. The annotators made sure that each table Second, humans sometimes ask questions that
|     |     |     |     |     |     | require | common | sense | knowledge |     | outside | the |
| --- | --- | --- | --- | --- | --- | ------- | ------ | ----- | --------- | --- | ------- | --- |
inthedatabaseappearsinatleastonequery.
|     |     |     |     |     |     | given database. |     | For | instance, | when | people | ask |
| --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --------- | ---- | ------ | --- |
B) SQLconsistency. Somequestionshavemul- “Display the employee id for the employees who
tiple acceptable SQL queries with the same re- reporttoJohn”,thecorrectSQLis
| sult. However, |           | giving | totally | different    | SQL labels |        |     |          |     |     |     |     |
| -------------- | --------- | ------ | ------- | ------------ | ---------- | ------ | --- | -------- | --- | --- | --- | --- |
|                |           |        |         |              |            | SELECT |     | employee |     | id  |     |     |
| to similar     | questions | can    | hinder  | the training | of se-     |        |     |          |     |     |     |     |
mantic parsing models. To avoid this issue, we FROM employees
designed the annotation protocol so that all anno- WHERE manager id = (
tators choose the same SQL query pattern if mul- SELECT employee id
|     |     |     |     |     |     | FROM | employees |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --------- | --- | --- | --- | --- | --- |
tipleequivalentqueriesarepossible.
|             |     |          |     |         |              | WHERE |     | first | name | = ‘John’) |     |     |
| ----------- | --- | -------- | --- | ------- | ------------ | ----- | --- | ----- | ---- | --------- | --- | --- |
| C) Question |     | clarity. | We  | did not | create ques- |       |     |       |      |           |     |     |
tions that are (1) vague or too ambiguous, or (2) which requires the common knowledge that “X
requireknowledgeoutsidethedatabasetoanswer. reports to Y” corresponds to an “employee-

manager” relation. we do not include such ques- (LIMIT) and GROUP BY (HAVING) compo-
tionsandleavethemasafutureresearchdirection. nents than the total of previous text-to-SQL
datasets. Spider has 200 distinct databases cov-
Annotation tools We open each database on a
ering138differentdomainssuchascollege,club,
web-based interface powered by the sqlite web3
TV show, government, etc. Most domains have
tool. It allows the annotators to see the schema
onedatabase,thuscontaining20-50questions,and
and content of each table, execute SQL queries,
a few domains such as flight information have
and check the returned results. This tool was ex-
multiple databases with more than 100 questions
tremely helpful for the annotators to write exe-
in total. On average, each database in Spider
cutable SQL queries that reflect the true meaning
has 27.6 columns and 8.8 foreign keys. The av-
ofthegivenquestionsandreturncorrectanswers.
erage question length and SQL length are about
13 and 21 respectively. Our task uses different
3.3 SQLReview
databases for training and testing, evaluating the
Once the database is labeled with question-query cross-domain performance. Therefore, Spider is
pairs, we ask a different annotator to check if the theonlyonetext-to-SQLdatasetthatcontainsboth
questions are clear and contain enough informa- databaseswithmultipletablesindifferentdomains
tion to answer the query. For a question with and complex SQL queries It tests the ability of a
multiple possible SQL translations, the reviewers systemtogeneralizetonotonlynewSQLqueries
double check whether the SQL label is correctly anddatabaseschemasbutalsonewdomains.
chosen under our protocol. Finally, the reviewers
checkifalltheSQLlabelsinthecurrentdatabase 5 TaskDefinition
coverallthecommonSQLclauses.
On top of the proposed dataset, we define a text-
to-SQLtaskthatismorerealisticthanpriorwork.
3.4 QuestionReviewandParaphrase
Unlike most of the previous semantic parsing or
After SQL labels are reviewed, native English
text-to-SQL tasks, models will be tested on both
speakers review and correct each question. They
different complex SQL queries and different com-
firstcheckifthequestionisgrammaticallycorrect
plexdatabasesindifferentdomainsinourtask. It
andnatural. Next,theymakesurethatthequestion
aimstoensurethatmodelscanonlymakethecor-
reflects the meaning of its corresponding SQL la-
rectpredictionwhentheytrulyunderstandthese-
bel. Finally,toimprovethediversityinquestions,
mantic meaning of the questions, rather than just
weaskannotatorstoaddaparaphrasedversionto
memorization. Also, because our databases con-
somequestions.
tain different domains, our corpus tests model’s
abilitytogeneralizetonewdatabases. Inthisway,
3.5 FinalReview
modelperformanceonthistaskcanreflectthereal
Finally, we ask the most experienced annotator to semanticparsingability.
conduct the final question and SQL review. This In order to make the task feasible and to focus
annotator makes the final decision if multiple re- onthemorefundamentalpartofsemanticparsing,
viewersarenotsureaboutsomeannotationissues. wemakethefollowingassumptions:
Also,werunascripttoexecuteandparseallSQL
labelstomakesuretheyarecorrect. • In our current task, we do not evaluate model
performance on generating values. Predicting
4 DatasetStatisticsandComparison correctSQLstructuresandcolumnsismorere-
alistic and critical at this stage based on the
We summarize the statistics of Spider and other
low performances of various current state-of-
text-to-SQL datasets in Table 1. Compared with
the-artmodelsonourtask. Inarealworldsitu-
other datasets, Spider contains databases with
ation,peopleneedtodoublecheckwhatcondi-
multiple tables and contains SQL queries in-
tion values are and finalize them after multiple
cluding many complex SQL components. For
times. It is unrealistic to predict condition val-
example, Spider contains about twice more
ues without interacting with users. In reality,
nested queries and 10 times more ORDER BY
mostpeopleknowwhatvaluestoaskbutdonot
knowtheSQLlogic. Amorereasonablewayis
3https://github.com/coleifer/
sqlite-web to ask users to use an interface searching the

Dataset #Q #SQL #DB #Domain #Table/DB ORDER BY GROUP BY NESTED HAVING
ATIS 5,280 947 1 1 32 0 5 315 0
GeoQuery 877 247 1 1 6 20 46 167 9
Scholar 817 193 1 1 7 75 100 7 20
Academic 196 185 1 1 15 23 40 7 18
IMDB 131 89 1 1 16 10 6 1 0
Yelp 128 110 1 1 7 18 21 0 4
Advising 3,898 208 1 1 10 15 9 22 0
Restaurants 378 378 1 1 3 0 0 4 0
WikiSQL 80,654 77,840 26,521 - 1 0 0 0 0
Spider 10,181 5,693 200 138 5.1 1335 1491 844 388
Table 1: Comparisons of text-to-SQL datasets. Spider is the only one text-to-SQL dataset that contains both
databaseswithmultipletablesindifferentdomainsandcomplexSQLqueries. Itwasdesignedtotesttheabilityof
asystemtogeneralizetonotonlynewSQLqueriesanddatabaseschemasbutalsonewdomains.
values,thenaskmorespecificquestions. Also, along with our corpus so that the research com-
otherpreviousworkwithvaluepredictionuses munitycansharethesameevaluationplatform.
onesingledatabaseinbothtrainandtestwhich
Component Matching To conduct a detailed
makes it vulnerable to overfitting. However,
analysis of model performance, we measure the
SQLqueriesmustincludevaluesinordertoex-
average exact match between the prediction and
ecute them. For value prediction in our task, a
ground truth on different SQL components. For
list of gold values for each question is given.
eachofthefollowingcomponents:
Models need to fill them into the right slots in
• SELECT •WHERE •GROUP BY
theirpredictedSQL.
• ORDER BY • KEYWORDS (including all
• As mentioned in the previous sections, we ex- SQL keywords without column names and
cludesomequeriesthatrequireoutsideknowl- operators)
edge such as common sense inference and we decompose each component in the prediction
math calculation. For example, imagine a ta- and the ground truth as bags of several sub-
ble with birth and death year columns. To components, and check whether or not these two
answer the questions like “How long is X’s sets of components match exactly. To evaluate
life length?”, we use SELECT death year each SELECT component, for example, con-
- birth year. Even though this example sider SELECT avg(col1), max(col2),
is easy for humans, it requires some common min(col1), we first parse and decompose into
knowledge of the life length definition and the a set (avg, min, col1), (max, col2),
useofamathoperation,whichisnotthefocus andseeifthegoldandpredictedsetsarethesame.
ofourdataset. Previous work directly compared decoded SQL
with gold SQL. However, some SQL components
• We assume all table and column names in the do not have order constraints. In our evaluation,
database are clear and self-contained. For ex- we treat each component as a set so that for ex-
ample, some databases use database specific ample, SELECT avg(col1), min(col1),
short-cut names for table and column names max(col2) and SELECT avg(col1),
suchas“stu id”,whichwemanuallyconverted max(col2), min(col1) would be treated
to“studentid”inourcorpus. as the same query. To report a model’s overall
performance on each component, we compute F1
6 EvaluationMetrics scoreonexactsetmatching.
Our evaluation metrics include Component Exact Matching We measure whether the pre-
Matching, Exact Matching, and Execution Ac- dicted query as a whole is equivalent to the gold
curacy. In addition, we measure the system’s query. We first evaluate the SQL clauses as de-
accuracyasafunctionofthedifficultyofaquery. scribed in the last section. The predicted query
Since our task definition does not predict value is correct only if all of the components are cor-
string, our evaluation metrics do not take value rect. Becauseweconductasetcomparisonineach
stringsintoaccount. clause, this exact matching metric can handle the
We will release the official evaluation script “orderingissue”(Xuetal.,2017).

| Execution | Accuracy4 |     | Since | Exact | Matching | is  | Easy |     |     |     |
| --------- | --------- | --- | ----- | ----- | -------- | --- | ---- | --- | --- | --- |
possibletoprovidefalsenegativeevaluationwhen What is the number of cars with more than 4 cylinders?
| the semantic | parser | is  | able to | generate | novel | syn- |     |     |     |     |
| ------------ | ------ | --- | ------- | -------- | ----- | ---- | --- | --- | --- | --- |
SELECT COUNT(*)
| tax structures, |     | we also | consider | Execution |     | Accu- |     |     |     |     |
| --------------- | --- | ------- | -------- | --------- | --- | ----- | --- | --- | --- | --- |
FROM cars_data
racy. ForExecutionAccuracy, thevalueisamust WHERE cylinders > 4
| inordertoexecuteSQLqueries. |         |     |         | Insteadofgener- |     |      |        |     |     |     |
| --------------------------- | ------- | --- | ------- | --------------- | --- | ---- | ------ | --- | --- | --- |
| ating these                 | values, | a   | list of | gold values     | for | each | Meidum |     |     |     |
question is given. Models need to select them For each stadium, how many concerts are there?
| and fill | them into | the | right slots | in  | their predicted |     |     |     |     |     |
| -------- | --------- | --- | ----------- | --- | --------------- | --- | --- | --- | --- | --- |
SELECT T2.name, COUNT(*)
| SQL. We | exclude | value | prediction |     | in Component |     |     |     |     |     |
| ------- | ------- | ----- | ---------- | --- | ------------ | --- | --- | --- | --- | --- |
FROM concert AS T1 JOIN stadium AS T2
and Exact Matching evaluations and do not pro- ON T1.stadium_id = T2.stadium_id
vide Execution Accuracy in the current version. GROUP BY T1.stadium_id
| However,      | it is | also important |       | to note  | that       | Execu- |      |     |     |     |
| ------------- | ----- | -------------- | ----- | -------- | ---------- | ------ | ---- | --- | --- | --- |
| tion Accuracy |       | can create     | false | positive | evaluation |        | Hard |     |     |     |
whenapredictedSQLreturnsthesameresult(for Which countries in Europe have at least 3 car
manufacturers?
example,‘NULL’)asthegoldSQLwhiletheyare
| semanticallydifferent. |     |     | Sowecanusebothtocom- |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
SELECT T1.country_name
| plementeachother. |     |     |     |     |     |     | FROM countries AS T1 JOIN continents |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- |
Finally, our evaluation also considers multiple AS T2 ON T1.continent = T2.cont_id
|            |      | JOIN |     | GROUP |     |        | JOIN car_makers AS T3 ON |     |     |     |
| ---------- | ---- | ---- | --- | ----- | --- | ------ | ------------------------ | --- | --- | --- |
| acceptable | keys | if   | and |       | are | in the |                          |     |     |     |
T1.country_id = T3.country
| query. | For example, |     | suppose | “stu | id” in | one ta- |     |     |     |     |
| ------ | ------------ | --- | ------- | ---- | ------ | ------- | --- | --- | --- | --- |
WHERE T2.continent = 'Europe'
| blerefersto“stu |     | id”inanothertable,GROUP |     |     |     | BY  |     |     |     |     |
| --------------- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
GROUP BY T1.country_name
| eitherisacceptable. |             |          |           |           |               |     | HAVING COUNT(*) >= 3  |     |     |     |
| ------------------- | ----------- | -------- | --------- | --------- | ------------- | --- | --------------------- | --- | --- | --- |
| SQL Hardness        |             | Criteria |           | To better | understand    |     |                       |     |     |     |
| the model           | performance |          | on        | different | queries,      | we  | Extra Hard            |     |     |     |
| divide              | SQL queries | into     | 4 levels: |           | easy, medium, |     |                       |     |     |     |
What is the average life expectancy in the countries
hard, extra hard. We define the difficulty where English is not the official language?
based on the number of SQL components, selec- SELECT AVG(life_expectancy)
| tions, and | conditions, |     | so that | queries | that  | contain | FROM country        |     |     |     |
| ---------- | ----------- | --- | ------- | ------- | ----- | ------- | ------------------- | --- | --- | --- |
| more SQL   | keywords    |     | (GROUP  | BY,     | ORDER | BY,     | WHERE name NOT IN   |     |     |     |
   (SELECT T1.name
| INTERSECT, |     | nested | subqueries, |     | column | selec- |     |     |     |     |
| ---------- | --- | ------ | ----------- | --- | ------ | ------ | --- | --- | --- | --- |
    FROM country AS T1 JOIN
| tions and | aggregators, |     | etc) | are considered |     | to be |     |     |     |     |
| --------- | ------------ | --- | ---- | -------------- | --- | ----- | --- | --- | --- | --- |
    country_language AS T2
harder. Forexample,aqueryisconsideredashard
    ON T1.code = T2.country_code
if it includes more than two SELECT columns,     WHERE T2.language = "English"
|     |     | WHERE |     |     |     | GROUP |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | ----- | --- | --- | --- | --- |
more than two conditions, and       AND T2.is_official = "T")
| BY two | columns, | or  | contains | EXCEPT | or  | nested |     |     |     |     |
| ------ | -------- | --- | -------- | ------ | --- | ------ | --- | --- | --- | --- |
queries. ASQLwithmoreadditionsontopofthat Figure3: SQLqueryexamplesin4hardnesslevels.
| isconsideredasextrahard. |     |     | Figure3showsexam- |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
plesofSQLqueriesin4hardnesslevels.
|             |            |             |            |               |             |      | an input                                    | to all models.    | Also, for each  | model, we |
| ----------- | ---------- | ----------- | ---------- | ------------- | ----------- | ---- | ------------------------------------------- | ----------------- | --------------- | --------- |
| 7 Methods   |            |             |            |               |             |      | limitthecolumnselectionspaceforeachquestion |                   |                 |           |
|             |            |             |            |               |             |      | example                                     | to all column     | of the database | which the |
| In order    | to analyze | the         | difficulty | and           | demonstrate |      |                                             |                   |                 |           |
|             |            |             |            |               |             |      | question                                    | is asking instead | of all column   | names in  |
| the purpose | of         | our corpus, |            | we experiment |             | with |                                             |                   |                 |           |
thewholecorpus.
| several | state-of-the-art |     | semantic | parsing | models. |     |     |     |     |     |
| ------- | ---------------- | --- | -------- | ------- | ------- | --- | --- | --- | --- | --- |
Asourdatasetisfundamentallydifferentfromthe
|     |     |     |     |     |     |     | Seq2Seq | Inspiredbyneuralmachinetranslation |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------------------------------- | --- | --- |
prior datasets such as Geoquery and WikiSQL, (Sutskever et al., 2014), we first apply a basic
we adapted these models to our task as follows. sequence-to-sequencemodel,Seq2Seq. Then,we
| We created | a   | ‘big’ column |     | list by | concatenating |     |     |     |     |     |
| ---------- | --- | ------------ | --- | ------- | ------------- | --- | --- | --- | --- | --- |
alsoexploreSeq2Seq+Attentionfrom(Dongand
columns in all tables of the database together as Lapata, 2016) by adding an attention mechanism
|         |       |             |     |            |         |        | (Bahdanau | et al., 2015). | In addition, | we include |
| ------- | ----- | ----------- | --- | ---------- | ------- | ------ | --------- | -------------- | ------------ | ---------- |
| 4Please | check | our website | for | the latest | updates | on the |           |                |              |            |
taskathttps://yale-lily.github.io/spider Seq2Seq+Copying by adding an attention-based

|     |     |     |     |     |     |     |             | Test           |     |     | Dev |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------------- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | Easy Medium | Hard ExtraHard |     | All | All |     |
ExampleSplit
|     |     |     | Seq2Seq |     |     |     | 22.0 7.8 | 5.5 | 1.3 | 9.4 | 10.3 |     |
| --- | --- | --- | ------- | --- | --- | --- | -------- | --- | --- | --- | ---- | --- |
Seq2Seq+Attention(DongandLapata,2016) 32.3 15.6 10.3 2.3 15.9 16.0
|     |     | Seq2Seq+Copying       |     |     |     |     | 29.3 13.1 | 8.8  | 3.0  | 14.1 | 15.3 |     |
| --- | --- | --------------------- | --- | --- | --- | --- | --------- | ---- | ---- | ---- | ---- | --- |
|     |     | SQLNet(Xuetal.,2017)  |     |     |     |     | 34.1 19.6 | 11.7 | 3.3  | 18.3 | 18.4 |     |
|     |     | TypeSQL(Yuetal.,2018) |     |     |     |     | 47.5 38.4 | 24.1 | 14.4 | 33.0 | 34.4 |     |
DatabaseSplit
|     |     |     | Seq2Seq |     |     |     | 11.9 1.9 | 1.3 | 0.5 | 3.7 | 1.9 |     |
| --- | --- | --- | ------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
Seq2Seq+Attention(DongandLapata,2016) 14.9 2.5 2.0 1.1 4.8 1.8
|     |     | Seq2Seq+Copying       |     |     |     |     | 15.4 3.4  | 2.0 | 1.1 | 5.3  | 4.1  |     |
| --- | --- | --------------------- | --- | --- | --- | --- | --------- | --- | --- | ---- | ---- | --- |
|     |     | SQLNet(Xuetal.,2017)  |     |     |     |     | 26.2 12.6 | 6.6 | 1.3 | 12.4 | 10.9 |     |
|     |     | TypeSQL(Yuetal.,2018) |     |     |     |     | 19.6 7.6  | 3.8 | 0.8 | 8.2  | 8.0  |     |
Table2: AccuracyofExactMatchingonSQLquerieswithdifferenthardnesslevels.
|     |     | Method |     | SELECT |     | WHERE | GROUP BY | ORDER BY | KEYWORDS |     |     |     |
| --- | --- | ------ | --- | ------ | --- | ----- | -------- | -------- | -------- | --- | --- | --- |
ExampleSplit
|     |                   | Seq2Seq |     | 23.3 |     | 4.9  | 15.3 | 9.2  |     | 17.9 |     |     |
| --- | ----------------- | ------- | --- | ---- | --- | ---- | ---- | ---- | --- | ---- | --- | --- |
|     | Seq2Seq+Attention |         |     | 31.1 |     | 9.1  | 28.2 | 20.8 |     | 21.4 |     |     |
|     | Seq2Seq+Copying   |         |     | 28.2 |     | 8.3  | 25.5 | 21.3 |     | 19.0 |     |     |
|     |                   | SQLNet  |     | 59.8 |     | 32.9 | 35.9 | 65.5 |     | 76.1 |     |     |
|     |                   | TypeSQL |     | 77.3 |     | 52.4 | 47.0 | 67.5 |     | 78.4 |     |     |
DatabaseSplit
|     |                   | Seq2Seq |                                                      | 13.0 |     | 1.5  | 3.3  | 5.3  |     | 8.7  |     |     |
| --- | ----------------- | ------- | ---------------------------------------------------- | ---- | --- | ---- | ---- | ---- | --- | ---- | --- | --- |
|     | Seq2Seq+Attention |         |                                                      | 13.6 |     | 3.1  | 3.6  | 9.9  |     | 9.9  |     |     |
|     | Seq2Seq+Copying   |         |                                                      | 12.0 |     | 3.1  | 5.3  | 5.8  |     | 7.3  |     |     |
|     |                   | SQLNet  |                                                      | 44.5 |     | 19.8 | 29.5 | 48.8 |     | 64.0 |     |     |
|     |                   | TypeSQL |                                                      | 36.4 |     | 16.0 | 17.2 | 47.7 |     | 66.2 |     |     |
|     |                   | Table3: | F1scoresofComponentMatchingonallSQLqueriesonTestset. |      |     |      |      |      |     |      |     |     |
copyingoperationsimilarto(JiaandLiang,2016). in the question. In our experiment, we use the
The original model does not take the schema question type info extracted from database con-
into account because it has the same schema in tent. Also,weextendtheirmodulestoORDER BY
bothtrainandtest. Wemodifythemodelsothatit andGROUP BYcomponentsaswell. Itistheonly
considersthetableschemainformationbypassing modelthatusesdatabasecontent.
avocabularymaskthatlimitsthemodeltodecode
the words from SQL keywords, table and column 8 ExperimentalResultsandDiscussion
namesinthecurrentdatabase.
|     |     |     |     |     |     |     | We summarize | the performance |     | of  | all models | on  |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------------- | --- | --- | ---------- | --- |
SQLNet introduced by (Xu et al., 2017) uses our test set including accuracy of exact matching
column attention and employs a sketch-based in Table 2 and F1 scores of component matching
inTable3.
| method     | and           | generates | SQL    | as  | a slot-filling |     |             |         |       |          |          |     |
| ---------- | ------------- | --------- | ------ | --- | -------------- | --- | ----------- | ------- | ----- | -------- | -------- | --- |
| task. This | fundamentally |           | avoids | the | sequence-to-   |     |             |         |       |          |          |     |
|            |               |           |        |     |                |     | Data Splits | For the | final | training | dataset, | we  |
sequencestructurewhenorderingdoesnotmatter
alsoselectandinclude752queriesand1659ques-
| in SQL | query | conditions. | Because |     | it is originally |     |            |                       |     |          |      |     |
| ------ | ----- | ----------- | ------- | --- | ---------------- | --- | ---------- | --------------------- | --- | -------- | ---- | --- |
|        |       |             |         |     |                  |     | tions that | follow our annotation |     | protocol | from | six |
designedforWikiSQL,weextenditsSELECTand
|       |         |          |     |        |       |     | existingdatasets: | Restaurants,GeoQuery,Scholar, |     |                   |     |     |
| ----- | ------- | -------- | --- | ------ | ----- | --- | ----------------- | ----------------------------- | --- | ----------------- | --- | --- |
| WHERE | modules | to ORDER |     | BY and | GROUP | BY  |                   |                               |     |                   |     |     |
|       |         |          |     |        |       |     | Academic,         | IMDB,andYelp.                 |     | Wereportresultson |     |     |
components.
|     |     |     |     |     |     |     | two different | settings | for all | models: | (1) | Exam- |
| --- | --- | --- | --- | --- | --- | --- | ------------- | -------- | ------- | ------- | --- | ----- |
TypeSQL proposed by (Yu et al., 2018) im- ple split where examples are randomly split into
proves upon SQLNet by proposing a different 8659train, 1034dev, 2147test. Questionsforthe
training procedure and utilizing types extracted same database can appear in both train and test.
from either knowledge graph or table content to (2) Database split where 206 databases are split
helpmodelbetterunderstandentitiesandnumbers into 146 train, 20 dev, and 40 test. All questions

forthesamedatabaseareinthesamesplit.
| Overall                       | Performance |          |          | The performances |         | of the     |     |     |     |     |     |     |
| ----------------------------- | ----------- | -------- | -------- | ---------------- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
| Seq2Seq-based                 |             | basic    | models   | including        |         | Seq2Seq,   |     |     |     |     |     |     |
| Seq2Seq+Attention,            |             |          | and      | Seq2Seq+Copying  |         | are        |     |     |     |     |     |     |
| very low.                     |             | However, | they     | are able         | to      | generate   |     |     |     |     |     |     |
| nested                        | and complex |          | queries  | because          | of      | their gen- |     |     |     |     |     |     |
| eral decoding                 |             | process. |          | Thus, they       | can     | get a few  |     |     |     |     |     |     |
| hard and                      | extra       | hard     | examples | correct.         |         | But in the |     |     |     |     |     |     |
| vast majority                 |             | of       | cases,   | they predict     | invalid | SQL        |     |     |     |     |     |     |
| querieswithgrammaticalerrors. |             |          |          | Theattentionand  |         |            |     |     |     |     |     |     |
copyingmechanismsdonothelpmucheither.
Figure4: Exactmatchingaccuracyasafunctionofthe
| In  | contrast, | SQLNet |     | and TypeSQL |     | that uti- |     |     |     |     |     |     |
| --- | --------- | ------ | --- | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- |
numberofforeignkeys.
| lize SQL   | structure |     | information   | to            | guide   | the SQL  |            |       |              |        |              |               |
| ---------- | --------- | --- | ------------- | ------------- | ------- | -------- | ---------- | ----- | ------------ | ------ | ------------ | ------------- |
| generation | process   |     | significantly | outperform    |         | other    |            |       |              |        |              |               |
|            |           |     |               |               |         |          | Complexity |       | of Database  | Schema |              | In order to   |
| Seq2Seq    | models.   |     | While         | they can      | produce | valid    |            |       |              |        |              |               |
|            |           |     |               |               |         |          | show how   | the   | complexity   | of     | the database | schema        |
| queries,   | however,  |     | they          | are unable    | to      | generate |            |       |              |        |              |               |
|            |           |     |               |               |         |          | affects    | model | performance, |        | Figure 4     | plots the ex- |
| nested     | queries   | or  | queries       | with keywords |         | such as  |            |       |              |        |              |               |
actmatchingaccuracyasafunctionofthenumber
| EXCEPT   |     | INTERSECT |     |            |             |            |            |        |          |           |      |               |
| -------- | --- | --------- | --- | ---------- | ----------- | ---------- | ---------- | ------ | -------- | --------- | ---- | ------------- |
|          | and |           |     | because    |             | they limit |            |        |          |           |      |               |
|          |     |           |     |            |             |            | of foreign | keys   | in a     | database. | The  | performance   |
| possible | SQL | outputs   | in  | some fixed | pre-defined |            |            |        |          |           |      |               |
|          |     |           |     |            |             |            | decreases  | as the | database | has       | more | foreign keys. |
SQLstructures.
|     |           |     |          |         |     |         | The first | reason | is that | the | model has | to choose |
| --- | --------- | --- | -------- | ------- | --- | ------- | --------- | ------ | ------- | --- | --------- | --------- |
| As  | Component |     | Matching | results | in  | Table 3 |           |        |         |     |           |           |
columnandtablenamesfrommanycandidatesin
shows, all models struggle with WHERE clause a complex database schema. Second, a complex
WHERE
prediction the most. clause is more likely databaseschemapresentsagreatchallengeforthe
| to have | multiple       |     | columns | and operations,   |     | which |                           |         |     |              |                   |         |
| ------- | -------------- | --- | ------- | ----------------- | --- | ----- | ------------------------- | ------- | --- | ------------ | ----------------- | ------- |
|         |                |     |         |                   |     |       | model to                  | capture | the | relationship | between           | differ- |
| makes   | its prediction |     | the     | most challenging. |     | The   |                           |         |     |              |                   |         |
|         |                |     |         |                   |     |       | enttableswithforeignkeys. |         |     |              | SQLanswerstoques- |         |
most number of prediction errors for each com- tionsonthedatabasewithmorenumberofforeign
ponentisfromcolumnprediction.
|     |     |     |     |     |     |     | keys are | more | likely | to join | more tables. | It indi- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ------ | ------- | ------------ | -------- |
Ingeneral,theoverallperformancesofallmod- cates that this task requires more effective meth-
els are low, indicating that our task is challenging ods to encode the relation of tables with foreign
| andthereisstillalargeroomforimprovement. |       |     |          |       |     |           | keys.        |     |     |     |     |     |
| ---------------------------------------- | ----- | --- | -------- | ----- | --- | --------- | ------------ | --- | --- | --- | --- | --- |
| Example                                  | Split | vs  | Database | Split | As  | discussed | 9 Conclusion |     |     |     |     |     |
inSection5,anotherchallengeofthedatasetisto
generalize to new databases. To study this, in Ta- In this paper we introduce Spider, a large, com-
ble2andTable3wecomparemodelperformances plex and cross-domain semantic parsing and text-
under the two settings. For all models, the per- to-SQL dataset, which directly benefits both NLP
formance under database split is much lower than andDBcommunities. BasedonSpider,wedefine
thatunderexamplesplit. Especially,TypeSQLuti- a new challenging and realistic semantic parsing
lizes column names as question types, and it out- task. Experimentalresultsonseveralstate-of-the-
| performs         | other | models       | with                        | a large    | margin | under    |              |     |           |         |        |           |
| ---------------- | ----- | ------------ | --------------------------- | ---------- | ------ | -------- | ------------ | --- | --------- | ------- | ------ | --------- |
|                  |       |              |                             |            |        |          | art models   | on  | this task | suggest | plenty | space for |
| theexamplesplit. |       |              | However,itsperformancedrops |            |        |          | improvement. |     |           |         |        |           |
| the most         | on    | the database |                             | split data | set.   | This in- |              |     |           |         |        |           |
dicatesthatthemodeldoeswelloncomplexSQL
Acknowledgement
predictionbutfailstogeneralizetonewdatabases.
In addition, we observe that all models perform We thank Graham Neubig, Tianze Shi, Catherine
much poorer on column selection under database Finegan-Dollak, and three anonymous reviewers
splitthanexamplesplit.
|     |     |     |     |     |     |     | for their | discussion | and | feedback. | We  | also thank |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | --- | --------- | --- | ---------- |
Overall, the result shows that our dataset BarryWilliamsforprovidingpartofourdatabase
presents a challenge for the model to generalize schemasfromtheDatabaseAnswers.
tonewdatabases.

| References |            |        |         |        |         | DragomirRadev.2018. |              |     | Improvingtext-to-sqleval- |       |             |     |
| ---------- | ---------- | ------ | ------- | ------ | ------- | ------------------- | ------------ | --- | ------------------------- | ----- | ----------- | --- |
|            |            |        |         |        |         | uation              | methodology. |     | In ACL                    | 2018. | Association | for |
| Miltiadis  | Allamanis, | Daniel | Tarlow, | Andrew | D. Gor- |                     |              |     |                           |       |             |     |
ComputationalLinguistics.
| don,   | and Yi     | Wei. 2015. | Bimodal   | modelling      | of         |             |           |     |            |         |            |         |
| ------ | ---------- | ---------- | --------- | -------------- | ---------- | ----------- | --------- | --- | ---------- | ------- | ---------- | ------- |
| source | code and   | natural    | language. | In             | ICML, vol- |             |           |     |            |         |            |         |
|        |            |            |           |                |            | Alessandra  | Giordani  | and | Alessandro |         | Moschitti. | 2012.   |
| ume    | 37 of JMLR | Workshop   |           | and Conference | Pro-       |             |           |     |            |         |            |         |
|        |            |            |           |                |            | Translating | questions |     | to sql     | queries | with       | genera- |
ceedings,pages2123–2132.JMLR.org. tive parsers discriminatively reranked. In COLING
(Posters),pages401–410.
| Yoav Artzi | and Luke | Zettlemoyer. |     | 2013. | Weakly su- |     |     |     |     |     |     |     |
| ---------- | -------- | ------------ | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- |
pervised learning of semantic parsers for mapping Po-SenHuang,ChenglongWang,RishabhSingh,Wen
instructionstoactions. TransactionsoftheAssocia- tauYih,andXiaodongHe.2018. Naturallanguage
tionforComputationalLinguistics.
|     |     |     |     |     |     | tostructuredquerygenerationviameta-learning. |     |     |     |     |     | In  |
| --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- | --- |
NAACL.
DzmitryBahdanau,KyunghyunCho,andYoshuaBen-
gio. 2015. Neural machine translation by jointly Srinivasan Iyer, Ioannis Konstas, Alvin Cheung,
learningtoalignandtranslate. InICLR. JayantKrishnamurthy,andLukeZettlemoyer.2017.
|     |     |     |     |     |     | Learning | a neural | semantic |     | parser | from | user feed- |
| --- | --- | --- | --- | --- | --- | -------- | -------- | -------- | --- | ------ | ---- | ---------- |
Laura Banarescu, Claire Bonial, Shu Cai, Madalina back. CoRR,abs/1704.08760.
| Georgescu, | Kira | Griffitt, | Ulf | Hermjakob, | Kevin |                             |     |     |     |                   |     |     |
| ---------- | ---- | --------- | --- | ---------- | ----- | --------------------------- | --- | --- | --- | ----------------- | --- | --- |
|            |      |           |     |            |       | RobinJiaandPercyLiang.2016. |     |     |     | Datarecombination |     |     |
Knight,PhilippKoehn,MarthaPalmer,andNathan
|            |       |          |         |                |     | for neural | semantic |     | parsing. | In Proceedings |     | of the |
| ---------- | ----- | -------- | ------- | -------------- | --- | ---------- | -------- | --- | -------- | -------------- | --- | ------ |
| Schneider. | 2013. | Abstract | meaning | representation |     |            |          |     |          |                |     |        |
forsembanking. InProceedingsofthe7thLinguis- 54thAnnualMeetingoftheAssociationforCompu-
tic Annotation Workshop and Interoperability with tationalLinguistics(Volume1: LongPapers).
Discourse.
|          |                   |           |        |             |          | Fei Li and | HV      | Jagadish. | 2014. | Constructing |     | an in-     |
| -------- | ----------------- | --------- | ------ | ----------- | -------- | ---------- | ------- | --------- | ----- | ------------ | --- | ---------- |
|          |                   |           |        |             |          | teractive  | natural | language  |       | interface    | for | relational |
| Jonathan | Berant            | and Percy | Liang. | 2014.       | Semantic |            |         |           |       |              |     |            |
|          |                   |           |        |             |          | databases. | VLDB.   |           |       |              |     |            |
| parsing  | via paraphrasing. |           | In     | Proceedings | of the   |            |         |           |       |              |     |            |
52ndAnnualMeetingoftheAssociationforCompu-
|                              |     |     |     |                   |     | Yunyao | Li, Huahai | Yang, | and | HV  | Jagadish. | 2006. |
| ---------------------------- | --- | --- | --- | ----------------- | --- | ------ | ---------- | ----- | --- | --- | --------- | ----- |
| tationalLinguistics(Volume1: |     |     |     | LongPapers),pages |     |        |            |       |     |     |           |       |
Constructingagenericnaturallanguageinterfacefor
| 1415–1425, | Baltimore, |     | Maryland. | Association | for |        |           |     |          |        |       |       |
| ---------- | ---------- | --- | --------- | ----------- | --- | ------ | --------- | --- | -------- | ------ | ----- | ----- |
|            |            |     |           |             |     | an xml | database. |     | In EDBT, | volume | 3896, | pages |
ComputationalLinguistics.
737–754.Springer.
| Deborah | A. Dahl, | Madeleine | Bates, | Michael | Brown, |           |       |         |     |           |       |        |
| ------- | -------- | --------- | ------ | ------- | ------ | --------- | ----- | ------- | --- | --------- | ----- | ------ |
|         |          |           |        |         |        | P. Liang, | M. I. | Jordan, | and | D. Klein. | 2011. | Learn- |
WilliamFisher,KateHunicke-Smith,DavidPallett,
|                |      |                                 |           |     |           | ing dependency-based |     |               | compositional |             | semantics. | In     |
| -------------- | ---- | ------------------------------- | --------- | --- | --------- | -------------------- | --- | ------------- | ------------- | ----------- | ---------- | ------ |
| Christine      | Pao, | Alexander                       | Rudnicky, | and | Elizabeth |                      |     |               |               |             |            |        |
|                |      |                                 |           |     |           | Association          | for | Computational |               | Linguistics |            | (ACL), |
| Shriberg.1994. |      | Expandingthescopeoftheatistask: |           |     |           |                      |     |               |               |             |            |        |
pages590–599.
|            |         | Proceedings |     | of the | Workshop |     |     |     |     |     |     |     |
| ---------- | ------- | ----------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
| The atis-3 | corpus. | In          |     |        |          |     |     |     |     |     |     |     |
onHumanLanguageTechnology,HLT’94,Strouds- Xi Victoria Lin, Chenglong Wang, Luke Zettlemoyer,
burg,PA,USA.AssociationforComputationalLin-
|     |     |     |     |     |     | andMichaelD.Ernst.2018. |     |     |     | Nl2bash: | Acorpusand |     |
| --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | -------- | ---------- | --- |
guistics.
semanticparserfornaturallanguageinterfacetothe
|          |             |            |     |       |           | linuxoperatingsystem. |     |     | InLREC. |     |     |     |
| -------- | ----------- | ---------- | --- | ----- | --------- | --------------------- | --- | --- | ------- | --- | --- | --- |
| Dipanjan | Das, Nathan | Schneider, |     | Desai | Chen, and |                       |     |     |         |     |     |     |
NoahA.Smith.2010. Probabilisticframe-semantic Wang Ling, Phil Blunsom, Edward Grefenstette,
parsing. InNAACL. Karl Moritz Hermann, Toma´s Kocisky´, Fumin
|     |     |     |     |     |     | Wang, | and Andrew |     | Senior. | 2016. | Latent | predictor |
| --- | --- | --- | --- | --- | --- | ----- | ---------- | --- | ------- | ----- | ------ | --------- |
J.Deng,W.Dong,R.Socher,L.-J.Li,K.Li,andL.Fei- InACL(1).TheAs-
networksforcodegeneration.
| Fei. 2009. | ImageNet: |     | A Large-Scale |     | Hierarchical |     |     |     |     |     |     |     |
| ---------- | --------- | --- | ------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
sociationforComputerLinguistics.
| ImageDatabase. |     | InCVPR09. |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
BryanMcCann,NitishShirishKeskar,CaimingXiong,
| LiDongandMirellaLapata.2016. |     |     |     | Languagetologi- |     |                        |     |     |     |                       |     |     |
| ---------------------------- | --- | --- | --- | --------------- | --- | ---------------------- | --- | --- | --- | --------------------- | --- | --- |
|                              |     |     |     |                 |     | andRichardSocher.2018. |     |     |     | Thenaturallanguagede- |     |     |
calformwithneuralattention. InProceedingsofthe cathlon: Multitask learning as question answering.
54thAnnualMeetingoftheAssociationforCompu- arXivpreprintarXiv:1806.08730.
| tational | Linguistics, | ACL | 2016, | August | 7-12, 2016, |     |     |     |     |     |     |     |
| -------- | ------------ | --- | ----- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
Berlin,Germany,Volume1: LongPapers. Yusuke Oda, Hiroyuki Fudaba, Graham Neubig,
|                              |     |     |     |                   |     | Hideaki | Hata,     | Sakriani | Sakti, | Tomoki   |     | Toda, and |
| ---------------------------- | --- | --- | --- | ----------------- | --- | ------- | --------- | -------- | ------ | -------- | --- | --------- |
| LiDongandMirellaLapata.2018. |     |     |     | Coarse-to-finede- |     |         |           |          |        |          |     |           |
|                              |     |     |     |                   |     | Satoshi | Nakamura. |          | 2015.  | Learning | to  | generate  |
coding for neural semantic parsing. In Proceed- pseudo-code from source code using statistical ma-
ings of the 56th Annual Meeting of the Associa- chine translation (t). In Proceedings of the 2015
tionforComputationalLinguistics(Volume1: Long 30thIEEE/ACMInternationalConferenceonAuto-
Papers), pages 731–742. Association for Computa- matedSoftwareEngineering(ASE),ASE’15.
tionalLinguistics.
|     |     |     |     |     |     | Ana-Maria | Popescu, | Alex | Armanasu, |     | Oren | Etzioni, |
| --- | --- | --- | --- | --- | --- | --------- | -------- | ---- | --------- | --- | ---- | -------- |
Catherine Finegan-Dollak, Jonathan K. Kummer- David Ko, and Alexander Yates. 2004. Modern
feld, Li Zhang, Karthik Ramanathan Dhanalak- natural language interfaces to databases: Compos-
shmiRamanathan,SeshSadasivam,RuiZhang,and ing statistical parsing with semantic tractability. In

Proceedingsofthe20thinternationalconferenceon Chenglong Wang, Po-Sen Huang, Alex Polozov,
Computational Linguistics, page 141. Association Marc Brockschmidt, and Rishabh Singh. 2018.
forComputationalLinguistics. Execution-guided neural program decoding. In
|     |     |     |     |     |     | ICML workshop |     | on Neural | Abstract | Machines | and |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | -------- | -------- | --- |
Ana-Maria Popescu, Oren Etzioni, and Henry Kautz. ProgramInductionv2(NAMPI).
| 2003a. | Towards | a theory | of natural | language | inter- |     |     |     |     |     |     |
| ------ | ------- | -------- | ---------- | -------- | ------ | --- | --- | --- | --- | --- | --- |
facestodatabases. InProceedingsofthe8thInter- DavidHDWarrenandFernandoCNPereira.1982. An
nationalConferenceonIntelligentUserInterfaces. efficienteasilyadaptablesystemforinterpretingnat-
|           |          |               |     |           |        | ural language | queries. | Computational |     |     | Linguistics, |
| --------- | -------- | ------------- | --- | --------- | ------ | ------------- | -------- | ------------- | --- | --- | ------------ |
| Ana-Maria | Popescu, | Oren Etzioni, |     | and Henry | Kautz. |               |          |               |     |     |              |
8(3-4):110–122.
| 2003b.   | Towards       | a theory       | of natural | language | in-         |                                    |     |     |     |     |        |
| -------- | ------------- | -------------- | ---------- | -------- | ----------- | ---------------------------------- | --- | --- | --- | --- | ------ |
| terfaces | to databases. | In Proceedings |            | of       | the 8th in- |                                    |     |     |     |     |        |
|          |               |                |            |          |             | YukWahWongandRaymondJ.Mooney.2007. |     |     |     |     | Learn- |
ternationalconferenceonIntelligentuserinterfaces, ing synchronous grammars for semantic parsing
pages149–157.ACM. with lambda calculus. In Proceedings of the 45th
|     |     |     |     |     |     | Annual Meeting |     | of the | Association | for | Computa- |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | ----------- | --- | -------- |
P. J. Price. 1990. Evaluation of spoken language sys- tional Linguistics (ACL-2007), Prague, Czech Re-
| tems:  | theatisdomain.                     | InSpeechandNaturalLan- |     |     |     | public. |     |     |     |     |     |
| ------ | ---------------------------------- | ---------------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
| guage: | ProceedingsofaWorkshopHeldatHidden |                        |     |     |     |         |     |     |     |     |     |
Valley, Pennsylvania, June 24-27,1990, pages 91– XiaojunXu,ChangLiu,andDawnSong.2017. Sqlnet:
| 95.          |                 |                         |     |        |         | Generatingstructuredqueriesfromnaturallanguage |               |           |     |       |          |
| ------------ | --------------- | ----------------------- | --- | ------ | ------- | ---------------------------------------------- | ------------- | --------- | --- | ----- | -------- |
|              |                 |                         |     |        |         | without                                        | reinforcement | learning. |     | arXiv | preprint |
| Chris Quirk, | Raymond         | Mooney,                 | and | Michel | Galley. | arXiv:1711.04436.                              |               |           |     |       |          |
| 2015.        | Languagetocode: | Learningsemanticparsers |     |        |         |                                                |               |           |     |       |          |
for if-this-then-that recipes. In Proceedings of the Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and
53rdAnnualMeetingoftheAssociationforCompu- Thomas Dillig. 2017a. Sqlizer: query synthesis
tational Linguistics and the 7th International Joint fromnaturallanguage. ProceedingsoftheACMon
| Conference | on  | Natural Language |     | Processing | (Vol- |     |     |     |     |     |     |
| ---------- | --- | ---------------- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- |
ProgrammingLanguages.
| ume1: | LongPapers),volume1,pages878–888. |     |     |     |     |                    |     |         |       |      |             |
| ----- | --------------------------------- | --- | --- | --- | --- | ------------------ | --- | ------- | ----- | ---- | ----------- |
|       |                                   |     |     |     |     | Navid Yaghmazadeh, |     | Yuepeng | Wang, | Isil | Dillig, and |
Maxim Rabinovich, Mitchell Stern, and Dan Klein. Thomas Dillig. 2017b. Sqlizer: Query synthesis
2017. Abstractsyntaxnetworksforcodegeneration fromnaturallanguage. Proc.ACMProgram.Lang.,
andsemanticparsing. InACL(1),pages1139–1149. 1(OOPSLA):63:1–63:26.
AssociationforComputationalLinguistics.
|     |     |     |     |     |     | Pengcheng | Yin, Bowen | Deng, | Edgar | Chen, | Bogdan |
| --- | --- | --- | --- | --- | --- | --------- | ---------- | ----- | ----- | ----- | ------ |
Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, Vasilescu, and Graham Neubig. 2018. Learning to
| and Percy | Liang. | 2016. | Squad: | 100, 000+ | ques- |              |      |             |          |     |            |
| --------- | ------ | ----- | ------ | --------- | ----- | ------------ | ---- | ----------- | -------- | --- | ---------- |
|           |        |       |        |           |       | mine aligned | code | and natural | language |     | pairs from |
tions for machine comprehension of text. CoRR, stackoverflow. InInternationalConferenceonMin-
| abs/1606.05250. |     |     |     |     |     | ingSoftwareRepositories(MSR). |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- |
SivaReddy,MirellaLapata,andMarkSteedman.2014. PengchengYinandGrahamNeubig.2017. Asyntactic
Large-scale semantic parsing without question- neural model for general-purpose code generation.
answer pairs. Transactions of the Association for InACL(1),pages440–450.AssociationforCompu-
| ComputationalLinguistics,2:377–392. |     |     |     |     |     | tationalLinguistics. |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- |
Ilya Sutskever, Oriol Vinyals, and Quoc V Le. 2014. Tao Yu, Zifan Li, Zilin Zhang, Rui Zhang, and
| Sequence | to  | sequence learning |     | with neural | net- |                     |     |          |     |                 |     |
| -------- | --- | ----------------- | --- | ----------- | ---- | ------------------- | --- | -------- | --- | --------------- | --- |
|          |     |                   |     |             |      | DragomirRadev.2018. |     | Typesql: |     | Knowledge-based |     |
works. InAdvancesinneuralinformationprocess- type-aware neural text-to-sql generation. In Pro-
ingsystems,pages3104–3112. ceedingsofNAACL.AssociationforComputational
Linguistics.
| LappoonR.TangandRaymondJ.Mooney.2001a. |     |     |     |     | Us- |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing multiple clause constructors in inductive logic JohnM.ZelleandRaymondJ.Mooney.1996. Learn-
programmingforsemanticparsing. InProceedings ing to parse database queries using inductive logic
ofthe12thEuropeanConferenceonMachineLearn-
|     |     |     |     |     |     | programming. |     | In AAAI/IAAI, |     | pages | 1050–1055, |
| --- | --- | --- | --- | --- | --- | ------------ | --- | ------------- | --- | ----- | ---------- |
ing,pages466–477,Freiburg,Germany. Portland,OR.AAAIPress/MITPress.
LappoonRTangandRaymondJMooney.2001b. Us- Luke S. Zettlemoyer and Michael Collins. 2005.
ing multiple clause constructors in inductive logic Learning to map sentences to logical form: Struc-
programming for semantic parsing. In ECML, vol- tured classification with probabilistic categorial
| ume1,pages466–477.Springer. |     |     |     |     |     | grammars. | UAI. |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --------- | ---- | --- | --- | --- | --- |
ChenglongWang,AlvinCheung,andRastislavBodik. Victor Zhong, Caiming Xiong, and Richard Socher.
| 2017.             | Synthesizing | highly    | expressive     | sql | queries |       |          |            |     |            |         |
| ----------------- | ------------ | --------- | -------------- | --- | ------- | ----- | -------- | ---------- | --- | ---------- | ------- |
|                   |              |           |                |     |         | 2017. | Seq2sql: | Generating |     | structured | queries |
| from input-output |              | examples. | In Proceedings |     | of the  |       |          |            |     |            |         |
fromnaturallanguageusingreinforcementlearning.
38th ACM SIGPLAN Conference on Programming CoRR,abs/1709.00103.
| Language | Design | and Implementation, |     | pages | 452– |     |     |     |     |     |     |
| -------- | ------ | ------------------- | --- | ----- | ---- | --- | --- | --- | --- | --- | --- |
466.ACM.