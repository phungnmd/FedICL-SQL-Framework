TheThirty-SeventhAAAIConferenceonArtificialIntelligence(AAAI-23)
RESDSQL: Decoupling Schema Linking and Skeleton Parsing for Text-to-SQL
HaoyangLi1,2,3,JingZhang1,2,3*,CuipingLi1,2,3,HongChen1,2,3
1KeyLaboratoryofDataEngineeringandKnowledgeEngineeringofMinistryofEducation,RenminUniversityofChina
2EngineeringResearchCenterofMinistryofEducationonDatabaseandBI
3InformationSchool,RenminUniversityofChina
{lihaoyang.cs,zhang-jing,licuiping,chong}@ruc.edu.cn
|     |     |     | Abstract |     |     |     |     | Question |     |     |     |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
What are flight numbers of flights departing from City
| One of | the recent | best | attempts | at Text-to-SQL |     | is  | the pre- | "Aberdeen"? |     |     |     |     |     |     |
| ------ | ---------- | ---- | -------- | -------------- | --- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- |
trainedlanguagemodel.Duetothestructuralpropertyofthe
Database schema (including tables and columns)
| SQL queries, |     | the seq2seq | model | takes | the responsibility |     | of  |     |     |     |     |     |     |     |
| ------------ | --- | ----------- | ----- | ----- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
airlines (airlines)
parsingboththeschemaitems(i.e.,tablesandcolumns)and
|     |     |     |     |     |     |     |     |     | uid | airline |     | abbreviation | country |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------------ | ------- | --- |
the skeleton (i.e., SQL keywords). Such coupled targets in- (airline id) (airline name) (abbreviation) (country)
| crease | the difficulty | of  | parsing | the correct | SQL | queries | es- |     |     |     |     |     |     |     |
| ------ | -------------- | --- | ------- | ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
airports (airports)
pecially when they involve many schema items and logic city airportcode airportname country
operators. This paper proposes a ranking-enhanced encod- (city) (airport code) (airport name) (country)
| ingandskeleton-awaredecodingframeworktodecouplethe |     |     |     |     |     |     |     |     | countryabbrev |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- |
(country abbrev)
| schema   | linking        | and the     | skeleton  | parsing.    | Specifically, |             | for a |     |                   |                 |     |                  |     |     |
| -------- | -------------- | ----------- | --------- | ----------- | ------------- | ----------- | ----- | --- | ----------------- | --------------- | --- | ---------------- | --- | --- |
| seq2seq  | encoder-decode |             | model,    | its encoder |               | is injected | by    |     | flights (flights) |                 |     |                  |     |     |
|          |                |             |           |             |               |             |       |     | airline           | flightno        |     | sourceairport    |     |     |
| the most | relevant       | schema      | items     | instead     | of            | the whole   | un-   |     |                   |                 |     |                  |     |     |
|          |                |             |           |             |               |             |       |     | (airline)         | (flight number) |     | (source airport) |     |     |
| ordered  | ones,          | which could | alleviate | the         | schema        | linking     | ef-   |     | destairport       |                 |     |                  |     |     |
fort during SQL parsing, and its decoder first generates the (destination airport)
skeleton and then the actual SQL query, which could im- Serialize schema items.
| plicitly | constrain | the | SQL parsing. |     | We evaluate | our | pro- | Schema sequence |     |     |     |     |     |     |
| -------- | --------- | --- | ------------ | --- | ----------- | --- | ---- | --------------- | --- | --- | --- | --- | --- | --- |
posed framework on Spider and its three robustness vari- airlines: uid, airline, abbreviation, county|airports:
ants: Spider-DK, Spider-Syn, and Spider-Realistic. The ex- city, airportcode, airportname, county, countyabbrev|
perimentalresultsshowthatourframeworkdeliverspromis- flights: airline, flightno, sourceairport, destairport
| ing performance |     | and | robustness. | Our | code | is available | at  |     |     |     |     |     |     |     |
| --------------- | --- | --- | ----------- | --- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Question + Schema sequence
https://github.com/RUCKBReasoning/RESDSQL.
Seq2seq PLM (such as BART and T5)
SQL query
Introduction
select flights.flightno from flights join airports on
flights.sourceairport = airports.airportcode where
| Relational | databases | that | are | used to | store | heterogeneous |     |     |     |     |     |     |     |     |
| ---------- | --------- | ---- | --- | ------- | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
airports.city = “Aberdeen”
datatypesincludingtext,integer,float,etc.,areomnipresent
| in modern | data | management |     | systems. | However, |     | ordinary |          |                                             |     |     |     |     |     |
| --------- | ---- | ---------- | --- | -------- | -------- | --- | -------- | -------- | ------------------------------------------- | --- | --- | --- | --- | --- |
|           |      |            |     |          |          |     |          | Figure1: | IllustrationofaText-to-SQLinstancesolvedbya |     |     |     |     |     |
users usually cannot make the best use of databases be- seq2seqPLM.Inthedatabaseschema,eachschemaitemis
cause they are not good at translating their requirements to denotedbyits“originalname(semanticname)”.
| the database | language—i.e., |       | the              | structured |       | query | language |     |     |     |     |     |     |     |
| ------------ | -------------- | ----- | ---------------- | ---------- | ----- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
| (SQL). To    | assist         | these | non-professional |            | users | in    | querying |     |     |     |     |     |     |     |
thedatabases,researchersproposetheText-to-SQLtask(Yu
|     |     |     |     |     |     |     |     | volvesmanycomplexSQLoperators(suchasGROUP |     |     |     |     |     | BY, |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
et al. 2018a; Cai et al. 2018), which aims to automati- ORDER BY,andHAVING,etc.)andnestedSQLqueries.
| cally translate |        | users’ natural | language |            | questions |     | into SQL |     |                 |          |     |             |          |      |
| --------------- | ------ | -------------- | -------- | ---------- | --------- | --- | -------- | --- | --------------- | -------- | --- | ----------- | -------- | ---- |
|                 |        |                |          |            |           |     |          |     | With the recent | advances | in  | pre-trained | language | mod- |
| queries.        | At the | same time,     | related  | benchmarks |           | are | becom-   |     |                 |          |     |             |          |      |
els(PLMs),manyexistingworksformulatetheText-to-SQL
| ing increasingly |     | complex, | from | the | single-domain |     | bench- |      |               |         |         |         |                |     |
| ---------------- | --- | -------- | ---- | --- | ------------- | --- | ------ | ---- | ------------- | ------- | ------- | ------- | -------------- | --- |
|                  |     |          |      |     |               |     |        | task | as a semantic | parsing | problem | and use | a sequence-to- |     |
markssuchasATIS(Iyeretal.2017)andGeoQuery(Zelle
|     |     |     |     |     |     |     |     | sequence | (seq2seq) | model | to solve | it (Scholak, | Schucher, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --------- | ----- | -------- | ------------ | --------- | --- |
andMooney1996)tothecross-domainbenchmarkssuchas
andBahdanau2021;Shietal.2021;Shawetal.2021).Con-
WikiSQL(Zhong,Xiong,andSocher2017)andSpider(Yu
cretely,asshowninFigure1,givenaquestionandadatabase
| et al. 2018c). | Most | of  | the recent | works | are | done | on Spi- |         |            |       |                |      |          |     |
| -------------- | ---- | --- | ---------- | ----- | --- | ---- | ------- | ------- | ---------- | ----- | -------------- | ---- | -------- | --- |
|                |      |     |            |       |     |      |         | schema, | the schema | items | are serialized | into | a schema | se- |
derbecauseitisthemostchallengingbenchmarkwhichin-
quencewheretheorderoftheschemaitemsiseitherdefault
|     |     |     |     |     |     |     |     | or  | random. Then, | a seq2seq | PLM, | such as | BART | (Lewis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --------- | ---- | ------- | ---- | ------ |
*JingZhangisthecorrespondingauthor.
Copyright©2023,AssociationfortheAdvancementofArtificial etal.2020)andT5(Raffeletal.2020),isleveragedtogen-
Intelligence(www.aaai.org).Allrightsreserved. eratetheSQLquerybasedontheconcatenationoftheques-
13067

tion and the schema sequence. We observe that the target ProblemDefinition
| SQL query | contains | not | only | the skeleton |     | that reveals | the |          |        |     |            |          |     |            |     |
| --------- | -------- | --- | ---- | ------------ | --- | ------------ | --- | -------- | ------ | --- | ---------- | -------- | --- | ---------- | --- |
|           |          |     |      |              |     |              |     | Database | Schema | A   | relational | database |     | is denoted | as  |
logic of the question but also the required schema items. D. The database schema S of D includes (1) a set of
Forinstance,foraSQLquery:“SELECTpetidFROMpets N T = {t ,t ,··· ,t },
|     |     |     |     |     |     |     |     | tables |     | 1   | 2   | N   | (2) a | set of | columns |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | ----- | ------ | ------- |
WHERE pet age = 1”, its skeleton is “SELECT FROM {c1,··· ,c1 ,c2,··· ,c2 ,cN,··· ,cN
|     |     |     |     |     |     |     |     | C = |     |     |     | ,··· |     |     | } associ- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --------- |
WHERE ” and its required schema items are “petid”, 1 n1 1 n2 1 nN
|                |     |       |     |     |     |     |     | ated with       | the tables, | where | n        | is the  | number  | of columns | in  |
| -------------- | --- | ----- | --- | --- | --- | --- | --- | --------------- | ----------- | ----- | -------- | ------- | ------- | ---------- | --- |
| “pets”,and“pet |     | age”. |     |     |     |     |     |                 |             |       | i        |         |         |            |     |
|                |     |       |     |     |     |     |     | the i-th table, | (3)         | and   | a set of | foreign | key     | relations  | R = |
|                |     |       |     |     |     |     |     | {(ci,cj)|ci,cj  |             |       |          |         | (ci,cj) |            |     |
SinceText-to-SQLneedstoperformnotonlytheschema ∈ C}, where each denotes a for-
|     |     |     |     |     |     |     |     | k h | k h |     |     |     | k h |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
linking which aligns the mentioned entities in the question eignkeyrelationbetweencolumnci andcolumncj.Weuse
|                                                   |            |     |        |     |         |        |        |          |                                       |     |          | k    |     |     | h       |
| ------------------------------------------------- | ---------- | --- | ------ | --- | ------- | ------ | ------ | -------- | ------------------------------------- | --- | -------- | ---- | --- | --- | ------- |
| toschemaitemsinthedatabaseschema,butalsotheskele- |            |     |        |     |         |        |        | PN       |                                       |     |          |      |     |     |         |
|                                                   |            |     |        |     |         |        |        | M =      | n todenotethetotalnumberofcolumnsinD. |     |          |      |     |     |         |
| tonparsingwhichparsesouttheskeletonoftheSQLquery, |            |     |        |     |         |        |        | i=1      | i                                     |     |          |      |     |     |         |
| the major                                         | challenges | are | caused | by  | a large | number | of re- |          |                                       |     |          |      |     |     |         |
|                                                   |            |     |        |     |         |        |        | Original | Name                                  | and | Semantic | Name | We  | use | “schema |
quiredschemaitemsandthecomplexcompositionofopera- items” to uniformly refer to tables and columns in the
torssuchasGROUP BY,HAVING,andJOIN ONinvolved database.Eachschemaitemcanberepresentedbyanorigi-
inaSQLquery.Theintertwiningoftheschemalinkingand nalnameandasemanticname.Thesemanticnamecanin-
theskeletonparsingcomplicateslearningevenmore. dicatethesemanticsoftheschemaitemmoreprecisely.As
To investigate whether the Text-to-SQL task could be- showninFigure1,itisobviousthatthesemanticnames“air-
come easier if the schema linking and the skeleton pars- line id” and “destination airport” are more clear than their
|         |            |     |         |               |     |            |     | original names |     | “uid” and | “destairport”. |     | Sometimes |     | the se- |
| ------- | ---------- | --- | ------- | ------------- | --- | ---------- | --- | -------------- | --- | --------- | -------------- | --- | --------- | --- | ------- |
| ing are | decoupled, | we  | conduct | a preliminary |     | experiment |     |                |     |           |                |     |           |     |         |
manticnameisthesameastheoriginalname.
| on Spider’s | dev      | set. Concretely, |                | we  | fine-tune | a   | T5-Base   |                 |     |                                   |     |     |     |     |     |
| ----------- | -------- | ---------------- | -------------- | --- | --------- | --- | --------- | --------------- | --- | --------------------------------- | --- | --- | --- | --- | --- |
| model to    | generate | the              | pure skeletons |     | based     | on  | the ques- |                 |     |                                   |     |     |     |     |     |
|             |          |                  |                |     |           |     |           | Text-to-SQLTask |     | Formally,givenaquestionqinnatural |     |     |     |     |     |
tions(i.e.,skeletonparsingtask).Weobservethattheexact
|     |     |     |     |     |     |     |     | language | and a | database | D with | its | schema | S, the | Text-to- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | -------- | ------ | --- | ------ | ------ | -------- |
matchaccuracyonsuchataskachievesabout80%usingthe
|     |     |     |     |     |     |     |     | SQLtaskaimstotranslateq |     |     | intoaSQLquerylthatcanbe |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | ----------------------- | --- | --- | --- | --- |
fine-tuned T5-Base. However, even the T5-3B model only executedonDtoanswerthequestionq.
| achieves  | about | 70% accuracy |        | (Shaw | et al.         | 2021; | Scholak, |     |     |     |     |     |     |     |     |
| --------- | ----- | ------------ | ------ | ----- | -------------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Schucher, | and   | Bahdanau     | 2021). | This  | pre-experiment |       | indi-    |     |     |     |     |     |     |     |     |
Methodology
catesthatdecouplingsuchtwoobjectivescouldbeapoten-
tialwayofreducingthedifficultyofText-to-SQL. In this section, we first give an overview of the proposed
frameworkandthendelveintoitsdesigndetails.
| To realize |     | the above | decoupling |     | idea, | we  | propose |     |     |     |     |     |     |     |     |
| ---------- | --- | --------- | ---------- | --- | ----- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
a Ranking-enhanced Encoding plus a Skeleton-aware ModelOverview
| Decoding | framework |     | for Text-to-SQL |     | (RESDSQL). |     | The |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | --------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
FollowingShawetal.(2021);Scholak,Schucher,andBah-
| former | injects | a few but | most | relevant | schema | items | into |               |     |       |             |     |      |             |       |
| ------ | ------- | --------- | ---- | -------- | ------ | ----- | ---- | ------------- | --- | ----- | ----------- | --- | ---- | ----------- | ----- |
|        |         |           |      |          |        |       |      | danau (2021), | we  | treat | Text-to-SQL |     | as a | translation | task, |
theseq2seqmodel’sencoderinsteadofallschemaitems.In
otherwords,theschemalinkingisconductedbeforehandto which can be solved by an encoder-decoder transformer
|     |     |     |     |     |     |     |     | model. Facing | the | above | problems, |     | we extend | the | existing |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----- | --------- | --- | --------- | --- | -------- |
filteroutmostoftheirrelevantschemaitemsinthedatabase
seq2seqText-to-SQLmethodsbyinjectingthemostrelevant
| schema, | which | can alleviate |     | the difficulty |     | of the | schema |              |     |           |          |     |         |     |          |
| ------- | ----- | ------------- | --- | -------------- | --- | ------ | ------ | ------------ | --- | --------- | -------- | --- | ------- | --- | -------- |
|         |       |               |     |                |     |        |        | schema items | in  | the input | sequence |     | and the | SQL | skeleton |
linkingfortheseq2seqmodel.Forsuchpurpose,wetrainan
intheoutputsequence,whichresultsinaranking-enhanced
| additional | cross-encoder |     | to classify |     | the tables | and | columns |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | ----------- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
simultaneously based on the input question, and then rank encoderandaskeleton-awaredecoder.Weprovidethehigh-
|            |      |           |        |                |     |               |     | level overview |             | of the | proposed | RESDSQL |       | framework | in  |
| ---------- | ---- | --------- | ------ | -------------- | --- | ------------- | --- | -------------- | ----------- | ------ | -------- | ------- | ----- | --------- | --- |
| and filter | them | according | to the | classification |     | probabilities |     |                |             |        |          |         |       |           |     |
|            |      |           |        |                |     |               |     | Figure 2.      | The encoder |        | of the   | seq2seq | model | receives  | the |
toformarankedschemasequence.Thelatterdoesnotadd
|     |     |     |     |     |     |     |     | ranked schema |     | sequence, | such | that | the schema | linking | ef- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | ---- | ---- | ---------- | ------- | --- |
anynewmodulesbutsimplyallowstheseq2seqmodel’sde-
fortcouldbealleviatedduringSQLparsing.Toobtainsuch
codertofirstgeneratetheSQLskeleton,andthentheactual
SQLquery.SinceskeletonparsingismucheasierthanSQL a ranked schema sequence, an additional cross-encoder is
proposedtoclassifytheschemaitemsaccordingtothegiven
| parsing, | the first | generated | skeleton |     | could | implicitly | guide |     |     |     |     |     |     |     |     |
| -------- | --------- | --------- | -------- | --- | ----- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
question,andthenwerankandfilterthembasedontheclas-
| the subsequent |     | SQL parsing |     | via the | masked | self-attention |     |            |                |     |             |     |        |         |       |
| -------------- | --- | ----------- | --- | ------- | ------ | -------------- | --- | ---------- | -------------- | --- | ----------- | --- | ------ | ------- | ----- |
|                |     |             |     |         |        |                |     | sification | probabilities. |     | The decoder |     | of the | seq2seq | model |
mechanisminthedecoder.
|     |     |     |     |     |     |     |     | first parses | out  | the SQL | skeleton   | and | then   | the actual | SQL  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ---- | ------- | ---------- | --- | ------ | ---------- | ---- |
|     |     |     |     |     |     |     |     | query, such  | that | the SQL | generation |     | can be | implicitly | con- |
Contributions (1) We investigate a potential way of de- strainedbythepreviouslyparsedskeleton.Bydoingthis,to
couplingtheschemalinkingandtheskeletonparsingtore- acertainextent,theschemalinkingandtheskeletonparsing
arenotintertwinedbutdecoupled.
ducethedifficultyofText-to-SQL.Specifically,wepropose
| a ranking-enhanced |     | encoder |     | to alleviate | the | effort | of the |     |     |     |     |     |     |     |     |
| ------------------ | --- | ------- | --- | ------------ | --- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Ranking-EnhancedEncoder
| schema | linking | and a skeleton-aware |     |     | decoder | to  | implicitly |     |     |     |     |     |     |     |     |
| ------ | ------- | -------------------- | --- | --- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
guidetheSQLparsingbytheskeleton.(2)Weconductex- Instead of injecting all schema items, we only consider the
tensiveevaluationandanalysisandshowthatourframework mostrelevantschemaitemsintheinputoftheencoder.For
not only achieves the new state-of-the-art (SOTA) perfor- thispurpose,wedeviseacross-encodertoclassifythetables
manceonSpiderbutalsoexhibitsstrongrobustness. and columns simultaneously and then rank them based on
13068

|     | Seq2seq Pre-trained Language Model |     |     |     | SQL skeleton |     |     |     |     | SQL query |     |     |
| --- | ---------------------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- | --------- | --- | --- |
select  _  from _ where _ | select flights.flightno from … where …
… …
|     |     | RankingT-e5n ehnacnocdeedr encoder |     |     |     |     | Skeleton-aware decoder |     |     |     |     |     |
| --- | --- | ---------------------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- |
…
<BOS> select _ from _ where …
What are … City "Aberdeen"?|flights: flights.flightno, flights.sourceairport, …|airports:
airports.city, airports.airportcode, …|flights.destairport = airports.airportcode …
Question + Ranked schema sequence + Optional foreign keys.
flights: flights.flightno, flights.sourceairport, …|airports: airports.city, airports.airportcode, …
Rank and filter schema items.  (using original names)
|     |     |     |     | 0.03 |     | 0.02 | 0.01 |     | … 0.94 | 0.99 | 0.95 … |     |
| --- | --- | --- | --- | ---- | --- | ---- | ---- | --- | ------ | ---- | ------ | --- |
Cross-encoder
What are … City "Aberdeen"?|airlines: airline id, airline name, …|airports: city, airport code, …
|     |     | Question |     |     | Serialize schema items in default order. (using semantic names) |     |     |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Figure2: Anoverviewoftheranking-enhancedencodingandskeleton-awaredecodingframework.Wetrainacross-encoder
forclassifyingtheschemaitems.Thenwetakethequestion,therankedschemasequence,andoptionalforeignkeysastheinput
oftheranking-enhancedencoder.Theskeleton-awaredecoderfirstdecodestheSQLskeletonandthentheactualSQLquery.
theirprobabilities.Basedontherankingorder,ononehand, a table could be identified even if the question only men-
wefilterouttheirrelevantschemaitems.Ontheotherhand, tions its columns. Concretely, for the i-th table, we inject
weusetherankedschemasequenceinsteadoftheunordered thecolumninformationCi ∈ Rni×d intothetableembed-
:
schema sequence, so that the seq2seq model could capture ding T by stacking a multi-head scaled dot-product atten-
i
potentialpositioninformationforschemalinking. tionlayer(Vaswanietal.2017)andafeaturefusionlayeron
As for the input of the cross-encoder, we flatten the thetopoftheencodingmodule:
| schema | items | into a schema | sequence | in their | default | or- |     |     |                  |     |            |     |
| ------ | ----- | ------------- | -------- | -------- | ------- | --- | --- | --- | ---------------- | --- | ---------- | --- |
|        |       |               |          |          |         |     |     | TC  | =MultiHeadAttn(T |     | ,Ci,Ci,h), | (1) |
der and concatenate it with the question to form an input i i : :
| sequence:X |     | =q|t :c1 | ,··· ,c1 |···|t | :cN | ,··· ,cN | ,   |     | Tˆ  |         | C).  |     |     |
| ---------- | --- | -------- | --------------- | --- | -------- | --- | --- | --- | ------- | ---- | --- | --- |
|            |     | 1 1      | n1              | N   | 1        | nN  |     | i   | =Norm(T | i +T |     |     |
i
where|isthedelimiter.Tobetterrepresentthesemanticsof
i
schema items, instead of their original names, we use their Here, T i acts as the query and C acts as both the key and
:
semanticnameswhichareclosertothenaturalexpression. thevalue,histhenumberofheads,andNorm(·)isarow-
|     |     |     |     |     |     |     | wiseL | normalizationfunction.TC |     |     | representsthecolumn- |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------------------------ | --- | --- | -------------------- | --- |
|     |     |     |     |     |     |     |       | 2                        |     |     | i                    |     |
Encoding Module We feed X into RoBERTa (Liu et al. attentive table embedding. We fuse the original table em-
2019), an improved version of BERT (Devlin et al. 2019). beddingT andthecolumn-attentivetableembeddingTC to
|     |     |     |     |     |     |     |     | i   |     |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Sinceeachschemaitemwillbetokenizedintooneormore obtainthecolumn-enhancedtableembeddingTˆ
∈R1×d.
i
tokensbyPLM’stokenizer(e.g.,thecolumn“airlineid”will
|     |     |     |     |     |     |     | LossFunctionofCross-Encoder |     |     |     | Cross-entropylossisa |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | -------------------- | --- |
besplitintotwotokens:“airline”and“id”),andourtargetis
torepresenteachschemaitemasawholeforclassification, well-adoptedlossfunctioninclassificationtasks.However,
we need to pool the output embeddings belonging to each since a SQL query usually involves only a few tables and
schema item. To achieve this goal, we use a pooling mod- columns in the database, the label distribution of the train-
ingsetishighlyimbalanced.Asaresult,thenumberofnega-
| ule that | consists | of a two-layer | BiLSTM | (Hochreiter |     | and |     |     |     |     |     |     |
| -------- | -------- | -------------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
tiveexamplesismanytimesthatofpositiveexamples,which
Schmidhuber1997)andanon-linearfully-connectedlayer.
willinduceserioustrainingbias.Toalleviatethisissue,we
| Afterpooling,eachtableembeddingcanbedenotedbyT |     |     |     |     |     | ∈   |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i
R1×d (i ∈ {1,...,N})andeachcolumnembeddingcanbe employ the focal loss (Lin et al. 2017) as our classification
denoted by Ci ∈ R1×d (i ∈ {1,...,N},k ∈ {1,...,n }), loss.Then,weformthelossfunctionofthecross-encoderin
|     |     | k   |     |     |     | i   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
whereddenotesthehiddensize. a multi-task learning way, which consists of both the table
classificationlossandthecolumnclassificationloss,i.e.,
| Column-Enhanced |     | Layer | We observe | that | some | ques- |     |     |     |     |      |     |
| --------------- | --- | ----- | ---------- | ---- | ---- | ----- | --- | --- | --- | --- | ---- | --- |
|                 |     |       |            |      |      |       |     | 1   | N   | 1   | N ni |     |
tions only mention the column name rather than the table X X X FL(yi,yˆi),
|     |     |     |     |     |     |     | L 1 | =   | FL(y | i ,yˆ)+ i |     | (2) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --------- | --- | --- |
name. For example in Figure 1, the question mentions a N M k k
columnname“city”,butitscorrespondingtablename“air- i=1 i=1k=1
ports” is ignored. This table name missing issue may com- where FL denotes the focal loss function and y is the
i
promisethetableclassificationperformance.Therefore,we ground truth label of the i-th table. y = 1 indicates the
i
tableisreferencedbytheSQLqueryand0otherwise.yi
| proposeacolumn-enhancedlayertoinjectthecolumninfor- |     |     |     |     |     |     |     |     |     |     |     | is  |
| --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
k
mationintothecorrespondingtableembedding.Inthisway, the ground truth label of the k-th column in the i-th table.
13069

Similarly,yi = 1indicatesthecolumnisreferencedbythe List the duration, file size and format of songs
k Q
SQLqueryand0otherwise.yˆ andyˆi arepredictedproba- whosegenreispop,orderedbytitle?
i k
bilities,whichareestimatedbytwodifferentMLPmodules SELECT T1.duration, T1.file size, T1.formats
basedonthetableandcolumnembeddingsTˆ i andC k i: SQL o F T R 2. O f M id fi W le H s E A R S E T T 1 2 J . O ge IN nre so i n s g = A “ S po T p 2 ” O O N RD T1 E . R f i B d Y =
yˆ = σ((TˆUt+bt)Ut+bt), (3) T2.song name
i i 1 1 2 2 select files.duration, files.file size, files.formats
yˆi = σ((CiUc+bc)Uc+bc), SQL fromfilesjoinsongonfiles.f id=song.f idwhere
k k 1 1 2 2 n
song.genre is=‘pop’orderbysong.song nameasc
whereU 1 t,U 1 c ∈Rd×w,bt 1 ,bc 1 ∈Rw,U 2 t,U 2 c ∈Rw×2,bt 2 , SQL s select from where orderby asc
bc ∈R2aretrainableparameters,andσ(·)denotesSoftmax.
2
Table 1: An example from Spider. Here, Q, SQL , SQL ,
PrepareInputforRanking-EnhancedEncoder During o n
and SQL denote the question, the original SQL query, the
inference, for each Text-to-SQL instance, we leverage the s
normalizedSQLquery,andtheSQLskeleton,respectively.
above-trained cross-encoder to compute a probability for
each schema item. Then, we only keep top-k tables in the
1
database and top-k columns for each remained table to
2
skeleton.Now,theobjectiveoftheseq2seqmodelis:
form a ranked schema sequence. k and k are two impor-
1 2
tanthyper-parameters.Whenk ork istoosmall,aportion
1 2 1 X G
oftherequiredtablesorcolumnsmaybeexcluded,whichis L = p(ls,l |S ), (4)
fatalforthesubsequentseq2seqmodel.Ask ork becomes 2 G i i i
1 2 i=1
larger, more and more irrelevant tables or columns may be
introduced as noise. Therefore, we need to choose appro- where G is the number of Text-to-SQL instances, S i is the
priate values for k and k to ensure a high recall while input sequence of the i-th instance which consists of the
1 2
preventing the introduction of too much noise. The input question,therankedschemasequence,andoptionalforeign
sequence for the ranking-enhanced encoder (i.e., seq2seq keyrelations.l i denotesthei-thtargetSQLqueryandl i s is
model’sencoder)isformedastheconcatenationoftheques- theskeletonextractedfroml i .Wewillpresentsomeneces-
tion,therankedschemasequence,andoptionalforeignkey sary details on how to normalize SQL queries and how to
relations (see Figure 2). Foreign key relations contain rich extracttheirskeletons.
informationaboutthestructureofthedatabase,whichcould SQL Normalization The Spider dataset is manually cre-
promote the generation of the JOIN ON clauses. In the
atedby11annotatorswithdifferentannotationhabits,which
rankedschemasequence,weusetheoriginalnamesinstead
resultsinslightlydifferentstylesamongthefinalannotated
ofthesemanticnamesbecausetheschemaitemsintheSQL
SQLqueries,suchasuppercaseversuslowercasekeywords.
queries are represented by their original names, and using
Although different styles have no impact on the execution
the former will facilitate the decoder to directly copy re-
results, the model requires some extra effort to learn and
quiredschemaitemsfromtheinputsequence.
adapttothem.Toreducethelearningdifficulty,wenormal-
izetheoriginalSQLqueriesbeforetrainingby(1)unifying
Skeleton-AwareDecoder
the keywords and schema items into lowercase, (2) adding
Mostseq2seqText-to-SQLmethodstellthedecodertogen- spacesaroundparenthesesandreplacingdoublequoteswith
erate the target SQL query directly. However, the apparent singlequotes,(3)addinganASCkeywordaftertheORDER
gapbetweenthenaturallanguageandtheSQLquerymakes BY clause if it does not specify the order, and (4) remov-
itdifficulttoperformthecorrectgeneration.Toalleviatethis ing the AS clause and replacing all table aliases with their
problem, we would like to decompose the SQL generation originalnames.WepresentanexampleinTable1.
into two steps: (1) generate the SQL skeleton based on the
SQLSkeletonExtraction BasedonthenormalizedSQL
semantics of the question, and then (2) select the required
queries, we can extract their skeletons which only contain
“data”(i.e.,tables,columns,andvalues)fromtheinputse-
SQL keywords and slots. Specifically, given a normalized
quencetofilltheslotsintheskeleton.
SQLquery,wekeepitskeywordsandreplacetherestparts
To realize the above decomposition idea without adding
withslots.NotethatwedonotkeeptheJOIN ONkeyword
additionalmodules,weproposeanewgenerationobjective
because it is difficult to find a counterpart from the ques-
based on the intrinsic characteristic of the transformer de-
tion (Gan et al. 2021b). As shown in Table 1, although the
coder,whichgeneratesthet-thtokendependingonnotonly
originalSQLquerylookscomplex,itsskeletonissimpleand
theoutputoftheencoderbutalsotheoutputofthedecoder
eachkeywordcanfindacounterpartfromthequestion.For
before the t-th time step (Vaswani et al. 2017). Concretely,
example, “order by asc” in the skeleton can be inferred
instead of decoding the target SQL directly, we encourage
from“orderedbytitle?”inthequestion.
the decoder to first decode the skeleton of the SQL query,
andbasedonthis,wecontinuetodecodetheSQLquery. Execution-Guided SQL Selector Since we do not con-
By parsing the skeleton first and then parsing the SQL strainthedecoderwithSQLgrammar,themodelmaygen-
query,ateachdecodingstep,SQLgenerationwillbeeasier eratesomeillegalSQLqueries.Toalleviatethisproblem,we
becausethedecodercouldeithercopya“data”fromthein- followSuhretal.(2020)touseanexecution-guidedSQLse-
putsequenceoraSQLkeywordfromthepreviouslyparsed lectorwhichperformsthebeamsearchduringthedecoding
13070

procedureandthenselectsthefirstexecutableSQLqueryin =32,lr=5e-5),andRESDSQL-3B(bs=96,lr=5e-5).For
thebeamasthefinalresult. both stages of training, we adopt linear warm-up (the first
10%trainingsteps)andcosinedecaytoadjustthelearning
|     |     | Experiments |     |     |     |     | rate.Wesetthebeamsizeto8duringdecoding.Moreover, |     |     |     |     |     |     |
| --- | --- | ----------- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
followingLin,Socher,andXiong(2020),weextractpoten-
ExperimentalSetup
tiallyusefulcontentsfromthedatabasetoenrichthecolumn
| Datasets | WeconductextensiveexperimentsonSpiderand |     |     |     |     |     | information. |     |     |     |     |     |     |
| -------- | ---------------------------------------- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
itsthreevariantswhichareproposedtoevaluatetherobust-
ness of the Text-to-SQL parser. Spider (Yu et al. 2018c) is Environments We conduct all experiments on a server
the most challenging benchmark for the cross-domain and withoneNVIDIAA100(80G)GPU,oneIntel(R)Xeon(R)
Silver4316CPU,256GBmemoryandUbuntu20.04.2LTS
multi-tableText-to-SQLtask.Spidercontainsatrainingset
operatingsystem.
| with 7,000 | samples1, | a   | dev set with | 1,034 | samples, | and a |     |     |     |     |     |     |     |
| ---------- | --------- | --- | ------------ | ----- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
hiddentestsetwith2,147samples.Thereisnooverlapbe-
tween the databases in different splits. For robustness, we ResultsonSpider
| train the | model | on Spider’s | training | set | but evaluate | it on |         |         |        |     |         |            |         |
| --------- | ----- | ----------- | -------- | --- | ------------ | ----- | ------- | ------- | ------ | --- | ------- | ---------- | ------- |
|           |       |             |          |     |              |       | Table 2 | reports | EM and | EX  | results | on Spider. | Notice- |
Spider-DK (Gan, Chen, and Purver 2021) with 535 sam- ably, we observe that RESDSQL-Base achieves better per-
ples, Spider-Syn (Gan et al. 2021a) with 1034 samples, formance than the bare T5-3B, which indicates that our
and Spider-Realistic (Deng et al. 2021) with 508 samples. decoupling idea can substantially reduce the learning dif-
These evaluation sets are derived from Spider by modify- ficulty of Text-to-SQL. Then, RESDSQL-3B outperforms
| ing questions | to  | simulate | real-world | application |     | scenarios. |          |          |         |     |          |     |            |
| ------------- | --- | -------- | ---------- | ----------- | --- | ---------- | -------- | -------- | ------- | --- | -------- | --- | ---------- |
|               |     |          |            |             |     |            | the best | baseline | by 1.6% | EM  | and 1.3% | EX  | on the dev |
Concretely, Spider-DK incorporates some domain knowl- set. Furthermore, when combined with NatSQL (Gan et al.
edge to paraphrase questions. Spider-Syn replaces schema- 2021b),anintermediaterepresentationofSQL,RESDSQL-
relatedwordswithsynonymsinquestions.Spider-Realistic Large achieves competitive results compared to powerful
removesexplicitlymentionedcolumnnamesinquestions. baselines on the dev set, and RESDSQL-3B achieves new
Evaluation Metrics To evaluate the performance of the SOTA performance on both the dev set and the test set.
Specifically,onthedevset,RESDSQL-3B+NatSQLbrings
| Text-to-SQL | parser, | following     | Yu       | et al.    | 2018c;          | Zhong, Yu, |             |             |            |          |                  |     |               |
| ----------- | ------- | ------------- | -------- | --------- | --------------- | ---------- | ----------- | ----------- | ---------- | -------- | ---------------- | --- | ------------- |
|             |         |               |          |           |                 |            | 4.2% EM     | and         | 3.6% EX    | absolute | improvements.    |     | On the        |
| and Klein   | 2020,   | we adopt      | two      | metrics:  | Exact-set-Match |            |             |             |            |          |                  |     |               |
|             |         |               |          |           |                 |            | hidden test | set,        | RESDSQL-3B |          | + NatSQL         |     | achieves com- |
| accuracy    | (EM)    | and EXecution | accuracy |           | (EX).           | The former |             |             |            |          |                  |     |               |
|             |         |               |          |           |                 |            | petitive    | performance | on         | EM       | and dramatically |     | increases     |
| measures    | whether | the predicted |          | SQL query | can             | be exactly |             |             |            |          |                  |     |               |
matched with the gold SQL query by converting them into EX from 75.5% to 79.9% (+4.4%), showing the effective-
|           |                |         |            |           |     |             | ness of        | our approach. | The       | reason     | for | the     | large gap be- |
| --------- | -------------- | ------- | ---------- | --------- | --- | ----------- | -------------- | ------------- | --------- | ---------- | --- | ------- | ------------- |
| a special | data structure |         | (Yu et al. | 2018c).   | The | latter com- |                |               |           |            |     |         |               |
|           |                |         |            |           |     |             | tween EM       | (72.0%)       | and       | EX (79.9%) |     | is that | EM is overly  |
| pares the | execution      | results | of the     | predicted | SQL | query and   |                |               |           |            |     |         |               |
|           |                |         |            |           |     |             | strict (Zhong, | Yu,           | and Klein | 2020).     | For | example | in Spider,    |
thegoldSQLquery.TheEXmetricissensitivetothegen-
|     |     |     |     |     |     |     | given a | question | “Find | id of the | candidate |     | who most re- |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ----- | --------- | --------- | --- | ------------ |
eratedvalues,buttheEMmetricisnot.Inpractice,weuse
thesumofEMandEXtoselectthebestcheckpointofthe cently accessed the course?”, its gold SQL query is “select
|         |        |         |                |     |     |            | candidate | id from | candidate | assessments |     | order | by assess- |
| ------- | ------ | ------- | -------------- | --- | --- | ---------- | --------- | ------- | --------- | ----------- | --- | ----- | ---------- |
| seq2seq | model. | For the | cross-encoder, | we  | use | Area Under |           |         |           |             |     |       |            |
ment datedesclimit1”.Infact,thereisanotherSQLquery
| ROC Curve | (AUC) | to evaluate | its | performance. |     | Since the |                   |     |         |           |             |     |           |
| --------- | ----- | ----------- | --- | ------------ | --- | --------- | ----------------- | --- | ------- | --------- | ----------- | --- | --------- |
|           |       |             |     |              |     |           | “select candidate |     | id from | candidate | assessments |     | where as- |
cross-encoderclassifiestablesandcolumnssimultaneously,
|     |     |     |     |     |     |     | sessment | date = | (select | max(assessment |     | date) | from candi- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------- | -------------- | --- | ----- | ----------- |
weadoptthesumoftableAUCandcolumnAUCtoselect
thebestcheckpointofthecross-encoder. date assessments)” which can also be executed to answer
|     |     |     |     |     |     |     | the question | (i.e., | EX is | positive). | However, |     | EM will judge |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------ | ----- | ---------- | -------- | --- | ------------- |
Implementation Details We train RESDSQL in two thelattertobewrong,whichleadstofalsenegatives.
stages.Inthefirststage,wetrainthecross-encoderforrank-
ing schema items. The number of heads h in the column- ResultsonRobustnessSettings
enhancedlayeris8.WeuseAdamW(LoshchilovandHut-
Recentstudies(Ganetal.2021a;Dengetal.2021)showthat
ter2019)withbatchsize32andlearningrate1e-5foropti- neural Text-to-SQL parsers are fragile to question pertur-
mization.Inthefocalloss,thefocusingparameterγandthe
|          |        |           |          |                    |     |       | bations | because | explicitly | mentioned |     | schema | items are re- |
| -------- | ------ | --------- | -------- | ------------------ | --- | ----- | ------- | ------- | ---------- | --------- | --- | ------ | ------------- |
| weighted | factor | α are set | to 2 and | 0.75 respectively. |     | Then, |         |         |            |           |     |        |               |
movedorreplacedwithsemanticallyconsistentwords(e.g.,
| k andk | aresetto4and5accordingtothestatisticsofthe |     |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 2 synonyms), which increases the difficulty of schema link-
datasets.Fortrainingtheseq2seqmodelinthesecondstage,
|             |       |        |        |              |     |            | ing. Therefore, |     | more and | more | efforts | have | been recently |
| ----------- | ----- | ------ | ------ | ------------ | --- | ---------- | --------------- | --- | -------- | ---- | ------- | ---- | ------------- |
| we consider | three | scales | of T5: | Base, Large, |     | and 3B. We |                 |     |          |      |         |      |               |
devotedtoimprovingtherobustnessofneuralText-to-SQL
fine-tunethemwithAdafactor(ShazeerandStern2018)us- parsers,suchasTKK(Qinetal.2022)andSUN (Gaoetal.
ingdifferentbatchsize(bs)andlearningrate(lr),resultingin
2022).TovalidatetherobustnessofRESDSQL,wetrainour
RESDSQL-Base(bs=32,lr=1e-4),RESDSQL-Large(bs
modelonSpider’strainingsetandevaluateitonthreechal-
lengingSpidervariants:Spider-DK,Spider-Syn,andSpider-
1Spideralsoprovidesadditional1,659trainingsamples,which
|               |      |      |               |           |      |         | Realistic. | Results | are reported |     | in Table | 3. We | can observe |
| ------------- | ---- | ---- | ------------- | --------- | ---- | ------- | ---------- | ------- | ------------ | --- | -------- | ----- | ----------- |
| are collected | from | some | single-domain | datasets, | such | as Geo- |            |         |              |     |          |       |             |
thatinallthreedatasets,RESDSQL-3B+NatSQLsurpris-
| Query (Zelle | and | Mooney | 1996) and | Restaurants | (Giordani | and |     |     |     |     |     |     |     |
| ------------ | --- | ------ | --------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Moschitti2012).Butfollowing(Scholak,Schucher,andBahdanau inglyoutperformsallstrongcompetitorsbyalargemargin,
2021),weignorethispartinourtrainingset. which suggests that our decoupling idea can also improve
13071

|     |     |          |     |     |     |     |     | DevSet | TestSet |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | ------ | ------- | --- | --- | --- |
|     |     | Approach |     |     |     |     |     | EM EX  | EM      | EX  |     |     |
Non-seq2seqmethods
|     |     | RAT-SQL+GRAPPA(Yuetal.2021)         |     |     |     |     |     | 73.4 -    | 69.6 | -    |     |     |
| --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --------- | ---- | ---- | --- | --- |
|     |     | RAT-SQL+GAP+NatSQL(Ganetal.2021b)   |     |     |     |     |     | 73.7 75.0 | 68.7 | 73.3 |     |     |
|     |     | SMBOP+GRAPPA(RubinandBerant2021)    |     |     |     |     |     | 74.7 75.0 | 69.5 | 71.1 |     |     |
|     |     | DT-FixupSQL-SP+RoBERTa(Xuetal.2021) |     |     |     |     |     | 75.0 -    | 70.9 | -    |     |     |
|     |     | LGESQL+ELECTRA(Caoetal.2021)        |     |     |     |     |     | 75.1 -    | 72.0 | -    |     |     |
S2SQL+ELECTRA(Huietal.2022)
|     |     |     |     |     |     |     |     | 76.4 - | 72.1 | -   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ---- | --- | --- | --- |
Seq2seqmethods
|     |     | T5-3B(Scholak,Schucher,andBahdanau2021)        |     |     |     |     |     | 71.5 74.4 | 68.0 | 70.1 |     |     |
| --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --------- | ---- | ---- | --- | --- |
|     |     | T5-3B+PICARD(Scholak,Schucher,andBahdanau2021) |     |     |     |     |     | 75.5 79.3 | 71.9 | 75.1 |     |     |
|     |     | RASAT+PICARD(Qietal.2022)                      |     |     |     |     |     | 75.3 80.5 | 70.9 | 75.5 |     |     |
Ourproposedmethod
|     |     | RESDSQL-Base         |     |     |     |     |     | 71.7 77.9 | -    | -    |     |     |
| --- | --- | -------------------- | --- | --- | --- | --- | --- | --------- | ---- | ---- | --- | --- |
|     |     | RESDSQL-Base+NatSQL  |     |     |     |     |     | 74.1 80.2 | -    | -    |     |     |
|     |     | RESDSQL-Large        |     |     |     |     |     | 75.8 80.1 | -    | -    |     |     |
|     |     | RESDSQL-Large+NatSQL |     |     |     |     |     | 76.7 81.9 | -    | -    |     |     |
|     |     | RESDSQL-3B           |     |     |     |     |     | 78.0 81.8 | -    | -    |     |     |
|     |     |                      |     |     |     |     |     | 80.5 84.1 | 72.0 | 79.9 |     |     |
RESDSQL-3B+NatSQL
Table2:EMandEXresultsonSpider’sdevelopmentsetandhiddentestset(%).Wecompareourapproachwithsomepowerful
baselinemethodsfromthetopoftheofficialleaderboardofSpider.
RelatedWork
therobustnessofseq2seqText-to-SQLparsers.Weattribute
thistothefactthatourproposedcross-encodercanalleviate
|     |     |     |     |     |     |     | Our method | is related | to the encoder-decoder |     | architecture |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ---------------------- | --- | ------------ | --- |
thedifficultyofschemalinkingandthusexhibitsrobustness
|     |     |     |     |     |     |     | designed | for Text-to-SQL, | the schema |     | item classification |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------------- | ---------- | --- | ------------------- | --- |
intermsofquestionperturbations.
task,andtheintermediaterepresentation.
| AblationStudies |     |     |     |     |     |     | Encoder-DecoderArchitecture |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- |
We take a thorough ablation study on Spider’s dev set to The encoder aims to jointly encode the question and
analyzetheeffectofeachdesign.
|           |                 |     |       |     |             |     | database | schema, which      | is generally | divided | into    | sequence |
| --------- | --------------- | --- | ----- | --- | ----------- | --- | -------- | ------------------ | ------------ | ------- | ------- | -------- |
|           |                 |     |       |     |             |     | encoder  | and graph encoder. | The          | decoder | aims to | generate |
| Effect of | Column-Enhanced |     | Layer | We  | investigate | the |          |                    |              |         |         |          |
theSQLqueriesbasedontheoutputoftheencoder.Dueto
| effectiveness | of  | the column-enhanced |     | layer, | which | is de- |     |     |     |     |     |     |
| ------------- | --- | ------------------- | --- | ------ | ----- | ------ | --- | --- | --- | --- | --- | --- |
thespecialformatofSQL,grammar-andexecution-guided
signedtoalleviatethetablemissingproblem.Table4shows
decodersarestudiedtoconstrainthedecodingresults.
thatremovingsuchalayerwillleadtoadecreaseinthetotal
AUC,asitcaninjectthehumanpriorintothecross-encoder.
|     |     |     |     |     |     |     | SequenceEncoder |     | Theinputisasequencethatconcate- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------------------- | --- | --- | --- |
natesthequestionwithserializeddatabaseschema(Yuetal.
| Effect of | Focal | Loss We | also study | the | effect | of focal |     |     |     |     |     |     |
| --------- | ----- | ------- | ---------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- |
2021;Lin,Socher,andXiong2020).Then,eachtokeninthe
| loss by replacing |     | it with the | cross-entropy |     | loss for | schema |     |     |     |     |     |     |
| ----------------- | --- | ----------- | ------------- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- |
item classification. Table 4 shows that cross-entropy leads sequenceisencodedbyaPLMencoder,suchasBERT(De-
vlinetal.2019)andencoderpartofT5(Raffeletal.2020).
toaperformancedropbecauseitcannotalleviatethelabel-
imbalanceprobleminthetrainingdata. GraphEncoder Theinputis oneormoreheterogeneous
Effect of Ranking Schema Items As shown in Table 5, graphs(Wangetal.2020a;Huietal.2022;Caoetal.2021;
|     |     |     |     |     |     |     | Cai et al. | 2021), where | a node represents |     | a question | token, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | ----------------- | --- | ---------- | ------ |
whenwereplacetherankedschemasequencewiththeorig-
|                |        |           |     |     |                  |     | a table | or a column,     | and an edge    | represents | the         | relation |
| -------------- | ------ | --------- | --- | --- | ---------------- | --- | ------- | ---------------- | -------------- | ---------- | ----------- | -------- |
| inal unordered | schema | sequence, | EM  | and | EX significantly |     |         |                  |                |            |             |          |
|                |        |           |     |     |                  |     | between | two nodes. Then, | relation-aware |            | transformer | net-     |
decreaseby4.5%and7.8%respectively.Thisresultproves
|     |     |     |     |     |     |     | works (Shaw, | Uszkoreit, | and Vaswani |     | 2018) or | relational |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---------- | ----------- | --- | -------- | ---------- |
thattheranking-enhancedencodertakesacrucialrole.
|     |     |     |     |     |     |     | graph neural | networks, | such as RGCN |     | (Schlichtkrull | et al. |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | ------------ | --- | -------------- | ------ |
EffectofSkeletonParsing Meanwhile,fromTable5,we 2018) and RGAT (Wang et al. 2020b), are applied to en-
can observe that EM and EX drop 0.7% and 0.8% respec- code each node. Some works also employ PLM encoders
tivelywhenremovingtheSQLskeletonfromthedecoder’s to initialize the representation of nodes on the graph (Cao
output (i.e., without skeleton parsing). This is because the et al. 2021; Wang et al. 2020a; Rubin and Berant 2021). It
seq2seqmodelneedstomakeextraeffortstobridgethegap is undeniable that the graph encoder can flexibly and ex-
betweennaturallanguagequestionsandSQLquerieswhen plicitly represent the relations between any two nodes via
parsingSQLqueriesdirectly. edges (e.g., foreign key relations). However, compared to
13072

|     |     |                                  |     |     |     |     |     | Spider-DK | Spider-Syn |      | Spider-Realistic |      |     |     |     |
| --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --------- | ---------- | ---- | ---------------- | ---- | --- | --- | --- |
|     |     | Approach                         |     |     |     |     |     | EM EX     | EM         | EX   | EM               | EX   |     |     |     |
|     |     | RAT-SQL+BERT(Wangetal.2020a)     |     |     |     |     |     | 40.9 -    | 48.2       |      | - 58.1           | 62.1 |     |     |     |
|     |     | RAT-SQL+GRAPPA(Yuetal.2021)      |     |     |     |     |     | 38.5 -    | 49.1       |      | - 59.3           | -    |     |     |     |
|     |     | T5-3B(Gaoetal.2022)              |     |     |     |     |     | - -       | 59.4       | 65.3 | 63.2             | 65.0 |     |     |     |
|     |     | LGESQL+ELECTRA(Caoetal.2021)     |     |     |     |     |     | 48.4 -    | 64.6       |      | - 69.2           | -    |     |     |     |
|     |     | TKK-3B(Gaoetal.2022)             |     |     |     |     |     | - -       | 63.0       | 68.2 | 68.5             | 71.1 |     |     |     |
|     |     | T5-3B+PICARD(Qietal.2022)        |     |     |     |     |     | - -       | -          |      | - 68.7           | 71.4 |     |     |     |
|     |     | RASAT+PICARD(Qietal.2022)        |     |     |     |     |     | - -       | -          |      | - 69.7           | 71.9 |     |     |     |
|     |     | LGESQL+ELECTRA+SUN(Qinetal.2022) |     |     |     |     |     | 52.7 -    | 66.9       |      | - 70.9           | -    |     |     |     |
|     |     | RESDSQL-3B+NatSQL                |     |     |     |     |     | 53.3 66.0 | 69.1       | 76.9 | 77.4             | 81.9 |     |     |     |
Table3:EvaluationresultsonSpider-DK,Spider-Syn,andSpider-Realistic(%).
SchemaItemClassification
| Modelvariant  |     | TableAUC |        | ColumnAUC |        |     | Total  |        |      |                |     |       |            |     |         |
| ------------- | --- | -------- | ------ | --------- | ------ | --- | ------ | ------ | ---- | -------------- | --- | ----- | ---------- | --- | ------- |
|               |     |          |        |           |        |     |        | Schema | item | classification | is  | often | introduced | as  | an aux- |
| Cross-encoder |     |          | 0.9973 |           | 0.9957 |     | 1.9930 |        |      |                |     |       |            |     |         |
-w/oenh.layer 0.9965 0.9939 1.9904 iliary task to improve the schema linking performance for
-w/ofocalloss 0.9958 0.9943 1.9901 Text-to-SQL. For example, GRAPPA (Yu et al. 2021) and
|     |     |     |     |     |     |     |     | GAP (Shi | et al. | 2021) | further | pre-train | the | PLMs | by using |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ----- | ------- | --------- | --- | ---- | -------- |
Table4:Ablationstudiesofthecross-encoder. theschemaitemclassificationtaskasoneofthepre-training
|     |     |     |     |     |     |     |     | objectives. | Then, | Text-to-SQL |     | can be | viewed | as  | a down- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ----------- | --- | ------ | ------ | --- | ------- |
streamtasktobefine-tuned.Caoetal.(2021)combinethe
| Modelvariant |     |     |     | EM(%) |     | EX(%) |     |        |                     |     |      |      |                 |     |      |
| ------------ | --- | --- | --- | ----- | --- | ----- | --- | ------ | ------------------- | --- | ---- | ---- | --------------- | --- | ---- |
|              |     |     |     |       |     |       |     | schema | item classification |     | task | with | the Text-to-SQL |     | task |
RESDSQL-Base 71.7 77.9 inamulti-tasklearningway.Theabove-mentionedmethods
-w/orankingschemaitems 67.2 70.1 enhancetheencoderbypre-trainingorthemulti-tasklearn-
-w/oskeletonparsing 71.0 77.1 ing paradigm. Instead, we propose an independent cross-
|     |     |     |     |     |     |     |     | encoder | as the | schema | item classifier |     | which | is easier | to be |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ------ | --------------- | --- | ----- | --------- | ----- |
Table5:Theeffectofkeydesigns.
trained.Weusetheclassifiertore-organizetheinputofthe
seq2seqmodel,whichcanproduceamoredirectimpacton
|     |     |     |     |     |     |     |     | schema | linking. | Bogin, | Gardner, | and | Berant | (2019) | calcu- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | -------- | ------ | -------- | --- | ------ | ------ | ------ |
PLMs,graphneuralnetworks(GNNs)usuallycannotbede- late a relevance score for each schema item, which is then
usedasthesoftcoefficientoftheschemaitemsinthesubse-
signedtoodeepduetothelimitationoftheover-smoothing
issue (Chen et al. 2020), which restricts the representation quentgraphencoder.Comparedwiththem,ourmethodcan
ability of GNNs. Then, PLMs have already encoded lan- beviewedasahardfilteringofschemaitemswhichcanre-
guagepatternsintheirparametersafterpre-training(Zhang ducenoisemoreeffectively.
| et al. 2021), | however, |     | the parameters |     | of GNNs | are | usually |     |     |     |     |     |     |     |     |
| ------------- | -------- | --- | -------------- | --- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
IntermediateRepresentation
randomized.Moreover,thegraphencoderreliesheavilyon
the design of relations, which may limit its robustness and Becausethereisahugegapbetweennaturallanguageques-
generalityonotherdatasets(Gaoetal.2022). tionsandtheircorrespondingSQLqueries,someworkshave
|               |             |         |            |           |            |                |         | focused           | on how | to design    | an                 | efficient    | intermediate |         | repre-   |
| ------------- | ----------- | ------- | ---------- | --------- | ---------- | -------------- | ------- | ----------------- | ------ | ------------ | ------------------ | ------------ | ------------ | ------- | -------- |
| Grammar-Based |             | Decoder |            | To inject | the        | SQL            | grammar |                   |        |              |                    |              |              |         |          |
|               |             |         |            |           |            |                |         | sentation         | (IR)   | to bridge    | the aforementioned |              |              | gap (Yu | et al.   |
| into the      | decoder,    | Yin     | and Neubig | (2017);   |            | Krishnamurthy, |         |                   |        |              |                    |              |              |         |          |
|               |             |         |            |           |            |                |         | 2018b;            | Guo et | al. 2019;    | Gan                | et al.       | 2021b).      | Instead | of di-   |
| Dasigi,       | and Gardner |         | (2017)     | propose   | a top-down |                | decoder |                   |        |              |                    |              |              |         |          |
|               |             |         |            |           |            |                |         | rectly generating |        | full-fledged |                    | SQL queries, |              | these   | IR-based |
to generate a sequence of pre-defined actions that can de- methods encourage models to generate IRs, which can be
| scribe the | grammar | tree | of the | SQL | query. | Rubin | and Be- |     |     |     |     |     |     |     |     |
| ---------- | ------- | ---- | ------ | --- | ------ | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
translatedtoSQLqueriesviaanon-trainabletranspiler.
| rant (2021)    | devise | a bottom-up |           | decoder | instead   | of  | the top- |     |     |     |     |     |     |     |     |
| -------------- | ------ | ----------- | --------- | ------- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| down paradigm. |        | PICARD      | (Scholak, |         | Schucher, |     | and Bah- |     |     |     |     |     |     |     |     |
Conclusion
| danau 2021) | incorporates |     | an  | incremental |     | parser | into the |     |     |     |     |     |     |     |     |
| ----------- | ------------ | --- | --- | ----------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Inthispaper,weproposeRESDSQL,asimpleyetpowerful
| auto-regressive |     | decoder | of PLMs | to  | prune | the invalid | par- |             |         |     |          |         |               |     |         |
| --------------- | --- | ------- | ------- | --- | ----- | ----------- | ---- | ----------- | ------- | --- | -------- | ------- | ------------- | --- | ------- |
|                 |     |         |         |     |       |             |      | Text-to-SQL | parser. |     | We first | train a | cross-encoder |     | to rank |
tiallygeneratedSQLqueriesduringbeamsearch.
andfilterschemaitemswhicharetheninjectedintotheen-
Execution-Guided Decoder Some works use an off-the- coderoftheseq2seqmodel.Wealsoletthedecodergenerate
shelf SQL executor such as SQLite to ensure grammatical the SQL skeleton first, which can implicitly guide the sub-
correctness. Wang et al. (2018) leverage a SQL executor sequentSQLgeneration.Toacertainextent,suchaframe-
to check and discard the partially generated SQL queries workdecouplesschemalinkingandskeletonparsing,which
whichraiseerrorsduringdecoding.Toavoidmodifyingthe canalleviatethedifficultyofText-to-SQL.Extensiveexper-
decoder, Suhr et al. (2020) check the executability of each imentsonSpideranditsthreevariantsdemonstratetheper-
candidateSQLquery,whichisalsoadoptedbyourmethod. formanceandrobustnessofRESDSQL.
13073

Acknowledgments Gan, Y.; Chen, X.; Xie, J.; Purver, M.; Woodward, J. R.;
|     |     |     |     |     |     |     |     | Drake, J. | H.; and Zhang, |     | Q. 2021b. | Natural | SQL: Making |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | --------- | ------- | ----------- | --- |
WethankHongjinSuandTaoYufortheireffortsinevaluat-
ingourmodelonSpider’stestset.Wealsothanktheanony- SQLEasiertoInferfromNaturalLanguageSpecifications.
InFindingsofEMNLP2021,2030–2042.
| mous reviewers |     | for their | helpful | suggestions. |     | This | work is |     |     |     |     |     |     |     |
| -------------- | --- | --------- | ------- | ------------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
supportedbyNationalNaturalScienceFoundationofChina Gao,C.;Li,B.;Zhang,W.;Lam,W.;Li,B.;Huang,F.;Si,
(62076245, 62072460, 62172424, 62276270) and Beijing L.;andLi,Y.2022.TowardsGeneralizableandRobustText-
NaturalScienceFoundation(4212022). to-SQLParsing. InFindingsofEMNLP2022.
Giordani,A.;andMoschitti,A.2012.AutomaticGeneration
References and Reranking of SQL-derived Answers to NL Questions.
|            |          |     |     |         |          |        |      | In Proceedings | of  | the Second | International |     | Conference | on  |
| ---------- | -------- | --- | --- | ------- | -------- | ------ | ---- | -------------- | --- | ---------- | ------------- | --- | ---------- | --- |
| Bogin, B.; | Gardner, | M.; | and | Berant, | J. 2019. | Global | Rea- |                |     |            |               |     |            |     |
soning over Database Structures for Text-to-SQL Parsing. Trustworthy Eternal Systems via Evolving Software, Data
| InEMNLP-IJCNLP2019,3657–3662. |     |     |     |     |     |     |     | andKnowledge,59–76. |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
Cai, R.; Xu, B.; Zhang, Z.; Yang, X.; Li, Z.; and Liang, Z. Guo, J.; Zhan, Z.; Gao, Y.; Xiao, Y.; Lou, J.; Liu, T.; and
2018. An Encoder-Decoder Framework Translating Natu- Zhang, D. 2019. Towards Complex Text-to-SQL in Cross-
Proceedings of the DomainDatabasewithIntermediateRepresentation.InPro-
| ral Language | to  | Database | Queries. |     | In  |     |     |     |     |     |     |     |     |     |
| ------------ | --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ceedingsofthe57thConferenceoftheAssociationforCom-
Twenty-SeventhInternationalJointConferenceonArtificial
|     |     |     |     |     |     |     |     | putational | Linguistics, | ACL | 2019, | Florence, | Italy, July | 28- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | --- | ----- | --------- | ----------- | --- |
Intelligence,IJCAI2018,3977–3983.
August2,2019,Volume1:LongPapers,4524–4535.
| Cai, R.; | Yuan, | J.; Xu, | B.; and | Hao, | Z.  | 2021. | SADGA: |     |     |     |     |     |     |     |
| -------- | ----- | ------- | ------- | ---- | --- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- |
Structure-AwareDualGraphAggregationNetworkforText- Hochreiter,S.;andSchmidhuber,J.1997. LongShort-Term
to-SQL. InAdvancesinNeuralInformationProcessingSys- Memory. NeuralComput.,1735–1780.
| tems 34: | Annual | Conference |     | on Neural |     | Information | Pro- |          |           |       |          |         |             |      |
| -------- | ------ | ---------- | --- | --------- | --- | ----------- | ---- | -------- | --------- | ----- | -------- | ------- | ----------- | ---- |
|          |        |            |     |           |     |             |      | Hui, B.; | Geng, R.; | Wang, | L.; Qin, | B.; Li, | Y.; Li, B.; | Sun, |
cessingSystems2021,NeurIPS2021,7664–7676.
|     |     |     |     |     |     |     |     | J.; and Li, | Y. 2022. | S2SQL: | Injecting | Syntax | to Question- |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | ------ | --------- | ------ | ------------ | --- |
Cao, R.; Chen, L.; Chen, Z.; Zhao, Y.; Zhu, S.; and Yu, K. SchemaInteractionGraphEncoderforText-to-SQLParsers.
InFindingsofACL2022,1254–1262.
2021. LGESQL:LineGraphEnhancedText-to-SQLModel
with Mixed Local and Non-Local Relations. In ACL/IJC- Iyer, S.; Konstas, I.; Cheung, A.; Krishnamurthy, J.; and
NLP2021,2541–2555. Zettlemoyer, L. 2017. Learning a Neural Semantic Parser
|           |      |         |     |         |       |         |         | from User | Feedback. | In  | Proceedings | of  | the 55th Annual |     |
| --------- | ---- | ------- | --- | ------- | ----- | ------- | ------- | --------- | --------- | --- | ----------- | --- | --------------- | --- |
| Chen, D.; | Lin, | Y.; Li, | W.; | Li, P.; | Zhou, | J.; and | Sun, X. |           |           |     |             |     |                 |     |
2020. MeasuringandRelievingtheOver-SmoothingProb- Meeting of the Association for Computational Linguistics,
lemforGraphNeuralNetworksfromtheTopologicalView. ACL2017,963–973.
| In The Thirty-Fourth |       | AAAI | Conference    |     | on         | Artificial | Intelli- |                                               |     |     |     |     |     |        |
| -------------------- | ----- | ---- | ------------- | --- | ---------- | ---------- | -------- | --------------------------------------------- | --- | --- | --- | --- | --- | ------ |
|                      |       |      |               |     |            |            |          | Krishnamurthy,J.;Dasigi,P.;andGardner,M.2017. |     |     |     |     |     | Neural |
| gence, AAAI          | 2020, | The  | Thirty-Second |     | Innovative |            | Applica- |                                               |     |     |     |     |     |        |
SemanticParsingwithTypeConstraintsforSemi-Structured
tions of Artificial Intelligence Conference, IAAI 2020, The Tables. InEMNLP2017,1516–1526.
| Tenth AAAI | Symposium |     | on Educational |     | Advances |     | in Artifi- |        |              |        |                    |     |     |     |
| ---------- | --------- | --- | -------------- | --- | -------- | --- | ---------- | ------ | ------------ | ------ | ------------------ | --- | --- | --- |
|            |           |     |                |     |          |     |            | Lewis, | M.; Liu, Y.; | Goyal, | N.; Ghazvininejad, |     | M.; | Mo- |
cialIntelligence,EAAI2020,NewYork,NY,USA,February
|     |     |     |     |     |     |     |     | hamed, | A.; Levy, | O.; Stoyanov, | V.; | and | Zettlemoyer, | L.  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --------- | ------------- | --- | --- | ------------ | --- |
7-12,2020,3438–3445.
2020.BART:DenoisingSequence-to-SequencePre-training
| Deng, X.; | Awadallah, |     | A. H.; | Meek, | C.; Polozov, |     | O.; Sun, |     |     |     |     |     |     |     |
| --------- | ---------- | --- | ------ | ----- | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
forNaturalLanguageGeneration,Translation,andCompre-
| H.;andRichardson,M.2021. |     |     |     | Structure-GroundedPretrain- |     |     |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
hension. InACL2020,7871–7880.
| ing for Text-to-SQL. |       |          | In Proceedings |         | of     | the 2021    | Confer- |          |            |           |        |            |              |      |
| -------------------- | ----- | -------- | -------------- | ------- | ------ | ----------- | ------- | -------- | ---------- | --------- | ------ | ---------- | ------------ | ---- |
|                      |       |          |                |         |        |             |         | Lin, T.; | Goyal, P.; | Girshick, | R. B.; | He, K.;    | and Dolla´r, | P.   |
| ence of the          | North | American |                | Chapter | of the | Association | for     |          |            |           |        |            |              |      |
|                      |       |          |                |         |        |             |         | 2017.    | Focal Loss | for Dense | Object | Detection. | In           | IEEE |
ComputationalLinguistics:HumanLanguageTechnologies,
|     |     |     |     |     |     |     |     | International | Conference |     | on Computer | Vision, | ICCV | 2017, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ---------- | --- | ----------- | ------- | ---- | ----- |
NAACL-HLT2021,Online,June6-11,2021,1337–1350.
2999–3007.
| Devlin, J.; | Chang, | M.; | Lee, | K.; and | Toutanova, |     | K. 2019. |     |     |     |     |     |     |     |
| ----------- | ------ | --- | ---- | ------- | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Lin,X.V.;Socher,R.;andXiong,C.2020.BridgingTextual
BERT:Pre-trainingofDeepBidirectionalTransformersfor
andTabularDataforCross-DomainText-to-SQLSemantic
| LanguageUnderstanding. |     |     | InProceedingsofthe2019Con- |     |     |     |     |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ference of the North American Chapter of the Association Parsing. InFindingsofEMNLP2020,4870–4888.
|     |     |     |     |     |     |     |     | Liu, Y.; | Ott, M.; Goyal, |     | N.; Du, J.; | Joshi, | M.; Chen, | D.; |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --------------- | --- | ----------- | ------ | --------- | --- |
forComputationalLinguistics:HumanLanguageTechnolo-
gies,NAACL-HLT2019,4171–4186. Levy, O.; Lewis, M.; Zettlemoyer, L.; and Stoyanov, V.
2019. RoBERTa:ARobustlyOptimizedBERTPretraining
Gan,Y.;Chen,X.;Huang,Q.;Purver,M.;Woodward,J.R.;
|                          |     |     |     |                          |     |     |     | Approach. | arXivpreprintarXiv:1907.11692. |     |     |     |     |     |
| ------------------------ | --- | --- | --- | ------------------------ | --- | --- | --- | --------- | ------------------------------ | --- | --- | --- | --- | --- |
| Xie,J.;andHuang,P.2021a. |     |     |     | TowardsRobustnessofText- |     |     |     |           |                                |     |     |     |     |     |
to-SQLModelsagainstSynonymSubstitution. InACL/IJC- Loshchilov,I.;andHutter,F.2019. DecoupledWeightDe-
NLP2021,(Volume1:LongPapers),VirtualEvent,August cay Regularization. In 7th International Conference on
| 1-6,2021,2505–2515. |     |     |     |     |     |     |     | LearningRepresentations,ICLR2019. |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- |
Gan,Y.;Chen,X.;andPurver,M.2021. ExploringUnder- Qi,J.;Tang,J.;He,Z.;Wan,X.;Cheng,Y.;Zhou,C.;Wang,
exploredLimitationsofCross-DomainText-to-SQLGener- X.; Zhang, Q.; and Lin, Z. 2022. RASAT: Integrating Re-
alization. InEMNLP2021,VirtualEvent/PuntaCana,Do- lationalStructuresintoPretrainedSeq2SeqModelforText-
minicanRepublic,7-11November,2021,8926–8931. to-SQL. InEMNLP2022.
13074

Qin,B.;Wang,L.;Hui,B.;Li,B.;Wei,X.;Li,B.;Huang,F.; SQL Generation with Execution-Guided Decoding. arXiv
Si,L.;Yang,M.;andLi,Y.2022. SUN:ExploringIntrinsic preprintarXiv:1807.03100.
UncertaintiesinText-to-SQLParsers. InProceedingsofthe Wang, K.; Shen, W.; Yang, Y.; Quan, X.; and Wang, R.
29th International Conference on Computational Linguis- 2020b. Relational Graph Attention Network for Aspect-
tics,COLING2022,Gyeongju,RepublicofKorea,October based Sentiment Analysis. In Proceedings of the 58th An-
12-17,2022,5298–5308.
nualMeetingoftheAssociationforComputationalLinguis-
Raffel, C.; Shazeer, N.; Roberts, A.; Lee, K.; Narang, S.; tics,ACL2020,3229–3238.
| Matena,M.;Zhou,Y.;Li,W.;andLiu,P.J.2020. |     |     |     |     | Exploring |     |                |     |           |         |           |     |        |     |
| ---------------------------------------- | --- | --- | --- | --- | --------- | --- | -------------- | --- | --------- | ------- | --------- | --- | ------ | --- |
|                                          |     |     |     |     |           |     | Xu, P.; Kumar, |     | D.; Yang, | W.; Zi, | W.; Tang, | K.; | Huang, | C.; |
theLimitsofTransferLearningwithaUnifiedText-to-Text
|     |     |     |     |     |     |     | Cheung,J.C.K.;Prince,S.J.D.;andCao,Y.2021. |     |     |     |     |     |     | Opti- |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | ----- |
J.Mach.Learn.Res.,140:1–140:67.
Transformer. mizing Deeper Transformers on Small Datasets. In ACL/I-
Rubin, O.; and Berant, J. 2021. SmBoP: Semi- JCNLP2021,2089–2102.
autoregressiveBottom-upSemanticParsing.InProceedings
|     |     |     |     |     |     |     | Yin,P.;andNeubig,G.2017. |     |     | ASyntacticNeuralModelfor |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------------------ | --- | --- | --- | --- |
of the 2021 Conference of the North American Chapter of General-Purpose Code Generation. In Proceedings of the
theAssociationforComputationalLinguistics:HumanLan- 55th Annual Meeting of the Association for Computational
guageTechnologies,NAACL-HLT2021,311–324. Linguistics,ACL2017,440–450.
Schlichtkrull, M. S.; Kipf, T. N.; Bloem, P.; van den Berg, Yu, T.; Li, Z.; Zhang, Z.; Zhang, R.; and Radev, D. R.
R.; Titov, I.; and Welling, M. 2018. Modeling Relational 2018a. TypeSQL: Knowledge-Based Type-Aware Neural
DatawithGraphConvolutionalNetworks. InTheSemantic Text-to-SQL Generation. In Proceedings of the 2018 Con-
Web-15thInternationalConference,ESWC2018,593–607.
|     |     |     |     |     |     |     | ference of | the North | American | Chapter |     | of the | Association |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | -------- | ------- | --- | ------ | ----------- | --- |
Scholak, T.; Schucher, N.; and Bahdanau, D. 2021. forComputationalLinguistics:HumanLanguageTechnolo-
PICARD: Parsing Incrementally for Constrained Auto- gies,NAACL-HLT,588–594.
Regressive Decoding from Language Models. In EMNLP Yu, T.; Wu, C.; Lin, X. V.; Wang, B.; Tan, Y. C.;
2021,9895–9901. Yang, X.; Radev, D. R.; Socher, R.; and Xiong, C. 2021.
|               |                |              |             |            |     |       | GraPPa:        | Grammar-Augmented |                                      | Pre-Training |     | for | Table | Se- |
| ------------- | -------------- | ------------ | ----------- | ---------- | --- | ----- | -------------- | ----------------- | ------------------------------------ | ------------ | --- | --- | ----- | --- |
| Shaw, P.;     | Chang,         | M.; Pasupat, | P.; and     | Toutanova, | K.  | 2021. |                |                   |                                      |              |     |     |       |     |
|               |                |              |             |            |     |       | manticParsing. |                   | In9thInternationalConferenceonLearn- |              |     |     |       |     |
| Compositional | Generalization |              | and Natural | Language   |     | Vari- |                |                   |                                      |              |     |     |       |     |
ingRepresentations,ICLR2021.
| ation: Can | a Semantic | Parsing | Approach | Handle | Both? | In  |     |     |     |     |     |     |     |     |
| ---------- | ---------- | ------- | -------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ACL/IJCNLP2021,922–938. Yu,T.;Yasunaga,M.;Yang,K.;Zhang,R.;Wang,D.;Li,Z.;
|           |            |     |              |     |       |       | andRadev,D.R.2018b. |     |     | SyntaxSQLNet:SyntaxTreeNet- |     |     |     |     |
| --------- | ---------- | --- | ------------ | --- | ----- | ----- | ------------------- | --- | --- | --------------------------- | --- | --- | --- | --- |
| Shaw, P.; | Uszkoreit, | J.; | and Vaswani, | A.  | 2018. | Self- |                     |     |     |                             |     |     |     |     |
Attention with Relative Position Representations. In works for Complex and Cross-DomainText-to-SQL Task.
| NAACL-HLT,464–468. |     |     |     |     |     |     | arXivpreprintarXiv:1810.05237. |     |           |               |     |           |     |         |
| ------------------ | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --------- | ------------- | --- | --------- | --- | ------- |
|                    |     |     |     |     |     |     | Yu, T.; Zhang,                 |     | R.; Yang, | K.; Yasunaga, |     | M.; Wang, |     | D.; Li, |
Shazeer,N.;andStern,M.2018.Adafactor:AdaptiveLearn-
ing Rates with Sublinear Memory Cost. In Proceedings Z.;Ma,J.;Li,I.;Yao,Q.;Roman,S.;Zhang,Z.;andRadev,
ofthe35thInternationalConferenceonMachineLearning, D.R.2018c.Spider:ALarge-ScaleHuman-LabeledDataset
forComplexandCross-DomainSemanticParsingandText-
ICML2018,4603–4611.
|          |               |     |          |        |           |     | to-SQL | Task. | In Proceedings | of  | the 2018 | Conference |     | on  |
| -------- | ------------- | --- | -------- | ------ | --------- | --- | ------ | ----- | -------------- | --- | -------- | ---------- | --- | --- |
| Shi, P.; | Ng, P.; Wang, | Z.; | Zhu, H.; | Li, A. | H.; Wang, | J.; |        |       |                |     |          |            |     |     |
EmpiricalMethodsinNaturalLanguageProcessing,3911–
| dos Santos, | C. N.; | and Xiang, | B. 2021. | Learning | Contex- |     |     |     |     |     |     |     |     |     |
| ----------- | ------ | ---------- | -------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3921.
tualRepresentationsforSemanticParsingwithGeneration-
|                        |     |     |                              |     |     |     | Zelle, J. | M.; and | Mooney, | R. J. | 1996. | Learning | to  | Parse |
| ---------------------- | --- | --- | ---------------------------- | --- | --- | --- | --------- | ------- | ------- | ----- | ----- | -------- | --- | ----- |
| AugmentedPre-Training. |     |     | InThirty-FifthAAAIConference |     |     |     |           |         |         |       |       |          |     |       |
onArtificialIntelligence,AAAI2021,13806–13814. Database Queries Using Inductive Logic Programming. In
|                                         |                |     |            |                    |           |     | Proceedings           | of  | the Thirteenth | National          |     | Conference   |     | on Ar- |
| --------------------------------------- | -------------- | --- | ---------- | ------------------ | --------- | --- | --------------------- | --- | -------------- | ----------------- | --- | ------------ | --- | ------ |
| Suhr,A.;Chang,M.;Shaw,P.;andLee,K.2020. |                |     |            |                    | Exploring |     |                       |     |                |                   |     |              |     |        |
|                                         |                |     |            |                    |           |     | tificial Intelligence |     | and            | Eighth Innovative |     | Applications |     | of     |
| Unexplored                              | Generalization |     | Challenges | for Cross-Database |           |     |                       |     |                |                   |     |              |     |        |
ArtificialIntelligenceConference,AAAI96,IAAI96,1050–
| SemanticParsing. |     | InProceedingsofthe58thAnnualMeet- |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1055.
| ing of the | Association | for | Computational | Linguistics, |     | ACL |            |           |     |         |             |     |       |       |
| ---------- | ----------- | --- | ------------- | ------------ | --- | --- | ---------- | --------- | --- | ------- | ----------- | --- | ----- | ----- |
|            |             |     |               |              |     |     | Zhang, Y.; | Warstadt, | A.; | Li, X.; | and Bowman, |     | S. R. | 2021. |
2020,8372–8388.
WhenDoYouNeedBillionsofWordsofPretrainingData?
Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, In ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual
L.;Gomez,A.N.;Kaiser,L.;andPolosukhin,I.2017. At- Event,August1-6,2021,1112–1125.
| tentionisAllyouNeed. |     | InAdvancesinNeuralInformation |     |     |     |     |                                 |     |     |     |                    |     |     |     |
| -------------------- | --- | ----------------------------- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | ------------------ | --- | --- | --- |
|                      |     |                               |     |     |     |     | Zhong,R.;Yu,T.;andKlein,D.2020. |     |     |     | SemanticEvaluation |     |     |     |
ProcessingSystems30:AnnualConferenceonNeuralInfor-
forText-to-SQLwithDistilledTestSuites.InEMNLP2020,
mationProcessingSystems2017,5998–6008.
396–411.
| Wang, B.; | Shin, R.; | Liu,           | X.; Polozov, | O.; and | Richardson, |     |                                     |     |     |     |     |              |     |     |
| --------- | --------- | -------------- | ------------ | ------- | ----------- | --- | ----------------------------------- | --- | --- | --- | --- | ------------ | --- | --- |
|           |           |                |              |         |             |     | Zhong,V.;Xiong,C.;andSocher,R.2017. |     |     |     |     | Seq2SQL:Gen- |     |     |
| M. 2020a. | RAT-SQL:  | Relation-Aware |              | Schema  | Encoding    |     |                                     |     |     |     |     |              |     |     |
eratingStructuredQueriesfromNaturalLanguageusingRe-
| andLinkingforText-to-SQLParsers. |         |        |             | InProceedingsofthe |     |     |                      |     |     |                                |     |     |     |     |
| -------------------------------- | ------- | ------ | ----------- | ------------------ | --- | --- | -------------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
|                                  |         |        |             |                    |     |     | inforcementLearning. |     |     | arXivpreprintarXiv:1709.00103. |     |     |     |     |
| 58th Annual                      | Meeting | of the | Association | for Computational  |     |     |                      |     |     |                                |     |     |     |     |
Linguistics,ACL2020,7567–7578.
Wang,C.;Tatwawadi,K.;Brockschmidt,M.;Huang,P.-S.;
| Mao,Y.;Polozov,O.;andSingh,R.2018. |     |     |     | RobustText-to- |     |     |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
13075