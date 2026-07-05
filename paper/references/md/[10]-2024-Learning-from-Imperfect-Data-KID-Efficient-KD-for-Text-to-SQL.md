Learning from Imperfect Data: Towards Efficient Knowledge Distillation of
|     | Autoregressive |     |     | Language |     | Models |     | for | Text-to-SQL |     |     |     |
| --- | -------------- | --- | --- | -------- | --- | ------ | --- | --- | ----------- | --- | --- | --- |
QihuangZhong1,KunfengChen1,LiangDing2,JuhuaLiu1*,BoDu1∗,DachengTao3
1SchoolofComputerScience,NationalEngineeringResearchCenterforMultimediaSoftware,InstituteofArtificialIntelligence
andHubeiKeyLaboratoryofMultimediaandNetworkCommunicationEngineering,WuhanUniversity,China
|     | 2TheUniversityofSydney,Australia |     |     |     |     | 3NanyangTechnologicalUniversity,Singapore |     |     |     |     |     |     |
| --- | -------------------------------- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
{zhongqihuang, chenkunfeng, liujuhua, dubo}@whu.edu.cn,{liangding.liam, dacheng.tao}@gmail.com
|     |     | Abstract |     |     |     |     | 49  |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Ours
GKD
|     |     |     |     |     |     | )%( erocS egarevA | 48  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
-10.4×
LargeLanguageModels(LLMs)haveshown
47
promisingperformanceintext-to-SQL,which
4202 tcO 51  ]LC.sc[  1v17311.0142:viXra + 3.96
| involvestranslatingnaturallanguagequestions |          |          |         |          |     |     | 46  |     |     |        |     |     |
| ------------------------------------------- | -------- | -------- | ------- | -------- | --- | --- | --- | --- | --- | ------ | --- | --- |
| into SQL                                    | queries. | However, | current | text-to- |     |     |     |     |     |        |     |     |
|                                             |          |          |         |          |     |     | 45  |     |     | ImitKD |     |     |
| SQLLLMsarecomputationallyexpensiveand       |          |          |         |          |     |     |     | RKD |     |        |     |     |
f-distill
challenging to deploy in real-world applica- 44 SFT (-w/o KD)
FKD
tions,highlightingtheimportanceofcompress-
| ingthem.  | Toachievethisgoal,knowledgedis- |          |           |       |     |     | 43  |     |     |     |        |     |
| --------- | ------------------------------- | -------- | --------- | ----- | --- | --- | --- | --- | --- | --- | ------ | --- |
|           |                                 |          |           |       |     |     | 1×  | 3×  | 5×  | 7×  | 9× 11× | 13× |
| tillation | (KD) is                         | a common | approach, | which |     |     |     |     |     |     |        |     |
Training Latency
| aims to | distill | the larger | teacher | model | into |     |     |     |     |     |     |     |
| ------- | ------- | ---------- | ------- | ----- | ---- | --- | --- | --- | --- | --- | --- | --- |
a smaller student model. While numerous Figure1: ComparisonsofdifferentKDmethodsfor
KD methods for autoregressive LLMs have distillingthestudentmodel(QWen1.5-0.5B)fromthe
| emerged | recently, | it is | still under-explored |     |     |     |     |     |     |     |     |     |
| ------- | --------- | ----- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
teacher(QWen1.5-4B).Thex-axisdenotesthetraining
whethertheyworkwellincomplextext-to-SQL latency relative to the SFT baseline, while the y-axis
| scenarios. | Tothisend,weconductaseriesof |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
denotestheaverageperformanceofstudentsonseveral
analysesandrevealthattheseKDmethodsgen- populartext-to-SQLbenchmarks.Theevaluationdetails
erallyfallshortinbalancingperformanceand arein§4.Weseethatourmethodachievesthebesttrade-
| efficiency. | Inresponsetothisproblem,wepro- |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
offbetweenperformanceandefficiency.
posetoimprovetheKDwithImperfectData,
namelyKID,whicheffectivelybooststheper-
formance without introducing much training scaling of model size, the inference and deploy-
| budget. | The core | of KID | is to efficiently |     | mit- |     |     |     |     |     |     |     |
| ------- | -------- | ------ | ----------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
mentofLLM-basedtext-to-SQLsystemsbecome
igatethetraining-inferencemismatchbysim-
|                           |               | effect1 |                  |           |     | more     | computationally |     |     | expensive   | and memory    | in- |
| ------------------------- | ------------- | ------- | ---------------- | --------- | --- | -------- | --------------- | --- | --- | ----------- | ------------- | --- |
| ulating                   | the cascading |         | of               | inference | in  |          |                 |     |     |             |               |     |
|                           |               |         |                  |           |     | tensive, | hindering       |     | the | development | of real-world |     |
| theimperfecttrainingdata. |               |         | Extensiveexperi- |           |     |          |                 |     |     |             |               |     |
mentson5text-to-SQLbenchmarksshowthat, industrial applications that require low inference
KIDcannotonlyachieveconsistentandsignifi- latency(Sunetal.,2023b). Hence,itiscrucialand
cantperformancegains(upto+5.83%average
|     |     |     |     |     |     | green | to  | compress | these | text-to-SQL | LLMs | and |
| --- | --- | --- | --- | --- | --- | ----- | --- | -------- | ----- | ----------- | ---- | --- |
score)acrossallmodeltypesandsizes,butalso acceleratetheinference,whilenotlosingmuchper-
effectivelyimprovethetrainingefficiency.
formance(Schwartzetal.,2020;Zhuetal.,2023).
|     |     |     |     |     |     |     | A common |     | model | compression | approach | is  |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ----- | ----------- | -------- | --- |
1 Introduction
knowledgedistillation(KD),whichinvolvescom-
|     |     |     |     |     |     | pressing |     | a large | teacher | model | by distilling | its |
| --- | --- | --- | --- | --- | --- | -------- | --- | ------- | ------- | ----- | ------------- | --- |
Text-to-SQL,whichaimstotranslateauser’snat-
knowledgeintoasmallstudentmodel(Hintonetal.,
urallanguagequestionintoanexecutableandac-
curateSQLquery,isatransformativeapplication 2015; Kim and Rush, 2016). Recently, numer-
of large language models (LLMs) (Katsogiannis- ous KD methods for autoregressive LLMs have
emerged(Guetal.,2023;Agarwaletal.,2024;Xu
MeimarakisandKoutrika,2023;Lietal.,2024a;
|              |         |        |          |      |     | et   | al., 2024),        | but | most | of them    | focus on  | the gen- |
| ------------ | ------- | ------ | -------- | ---- | --- | ---- | ------------------ | --- | ---- | ---------- | --------- | -------- |
| Pourreza and | Rafiei, | 2024). | However, | with | the |      |                    |     |      |            |           |          |
|              |         |        |          |      |     | eral | instruction-tuning |     |      | scenarios. | Different | from     |
* Corresponding Authors: Juhua Liu (e-mail: liu- the general tasks that allow for flexible and di-
juhua@whu.edu.cn),BoDu(e-mail:dubo@whu.edu.cn)
verseoutputs,text-to-SQLismorechallenging,as
1Theerrorattheearlystepwillaffectthefuturepredictions
duringtheautoregressiveinference(Agarwaletal.,2024). it requires the LLMs to precisely output the ta-

ble/columnname. EvenaminorerrorintheSQL effectivelyimprovetherobustnessofstudents.
| querycouldleadtothewrongresult. |     |     |     |     | Unfortunately, |     |                |     |     |                          |     |     |     |
| ------------------------------- | --- | --- | --- | --- | -------------- | --- | -------------- | --- | --- | ------------------------ | --- | --- | --- |
|                                 |     |     |     |     |                |     | Contributions. |     |     | Ourmaincontributionsare: |     |     |     |
itisstillunder-exploredwhethertheseKDmethods
workwellfortext-to-SQLLLMs. • WerevealthatcurrentKDmethodsfortext-to-
Tothisend,weconductpreliminaryexperiments
SQLLLMsgenerallyfallshortinbalancing
byapplying5representativeKDmethodstodistill
performanceandefficiency.
| the QWen-family     |     | LLMs       | (Bai | et al., | 2023)  | on the |     |            |     |                        |     |     |          |
| ------------------- | --- | ---------- | ---- | ------- | ------ | ------ | --- | ---------- | --- | ---------------------- | --- | --- | -------- |
|                     |     |            |      |         |        |        | •   | We propose |     | a simple-yet-effective |     |     | approach |
| popular text-to-SQL |     | benchmark, |      | i.e.,   | Spider | (Yu    |     |            |     |                        |     |     |          |
et al., 2018). We find that the performance gains (KID)toeffectivelyimproveKDperformance
of these KD methods mainly rely on the model- withoutintroducingmuchtrainingbudget.
| generated | data, | which | is effective | but | hard | to ob- |     |     |     |     |     |     |     |
| --------- | ----- | ----- | ------------ | --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
• ExtensiveexperimentsshowthatKIDoutper-
| tain. Specifically, |     | although | the | model-generated |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | -------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
formsthestandardKDbyalargemarginand
datacanalleviatethetraining-inferencemismatch
effectivelyimprovesthestudent’srobustness.
| (i.e., difference |     | between | teacher-forcing |     |     | training |     |     |     |     |     |     |     |
| ----------------- | --- | ------- | --------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
andautoregressiveinference(PangandHe,2020))
|     |     |     |     |     |     |     | 2   | Preliminary |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
andachievesremarkableperformance,itrequires
thestudentmodeltoautoregressivelygeneratein 2.1 TaskFormulation
an online fashion, leading to unbearable training Text-to-SQL aims to convert a natural language
latency. AsillustratedinFigure1,GKD(Agarwal
|               |          |      |                 |     |     |      | question |     | Q into | a SQL      | query    | Y, which | is exe- |
| ------------- | -------- | ---- | --------------- | --- | --- | ---- | -------- | --- | ------ | ---------- | -------- | -------- | ------- |
| et al., 2024) | training | with | model-generated |     |     | data |          |     |        |            |          |          |         |
|               |          |      |                 |     |     |      | cutable  | and | can    | accurately | retrieve | relevant | data    |
performswellbutgreatlysuffersfromtrainingin-
|     |     |     |     |     |     |     | from | a database |     | D. The | database | D usually | con- |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---------- | --- | ------ | -------- | --------- | ---- |
efficiency. Thus,thereraisesaquestion: whether tains the schema (i.e., tables and columns) and
| we can mitigate |     | the training-inference |     |     | mismatch |     |     |     |     |     |     |     |     |
| --------------- | --- | ---------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
metadata,containingcolumntypes/values,primary
moreefficiently?
|     |     |     |     |     |     |     | keys, | foreign | key | relations | and | etc (Zhong | et al., |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------- | --- | --------- | --- | ---------- | ------- |
Motivated by this, we propose a simple-yet- 2017). Specifically,givenanLLMMandaprompt
| effective | approach | to improve |     | KD, | namely | KID, |     |     |     |     |     |     |     |
| --------- | -------- | ---------- | --- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- |
templateP,weenforcetheMtoautoregressively
andachieveabettertrade-offbetweenperformance
|                 |     |          |     |        |          |     | generateanoutputsequenceY |     |     |     |     | conditionedonthe |     |
| --------------- | --- | -------- | --- | ------ | -------- | --- | ------------------------- | --- | --- | --- | --- | ---------------- | --- |
| and efficiency. |     | The core | of  | KID is | to force | the |                           |     |     |     |     |                  |     |
P(Q,D),whichcanbeformulatedas:
| student to | rewrite | the ground-truth |     |     | training | data |     |     |     |     |     |     |     |
| ---------- | ------- | ---------------- | --- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- |
intoimperfectone,andthenlearnhowtocalibrate Y ∼ P (Y | P(Q,D),Y ),
|                                            |     |                    |     |     |             |     |       |     | t    | M t      |     | <t       | (1)         |
| ------------------------------------------ | --- | ------------------ | --- | --- | ----------- | --- | ----- | --- | ---- | -------- | --- | -------- | ----------- |
| these imperfect                            |     | data. Intuitively, |     | by  | introducing |     |       |     |      |          |     |          |             |
|                                            |     |                    |     |     |             |     | where | P   | (Y | | P(Q,D),Y |     | ) is the | probability |
| someerrorsintheimperfectdata,wecansimulate |     |                    |     |     |             |     |       | M   | t    |          | <t  |          |             |
the cascading effect of inference during training forthenexttoken,andY isthet-thtokenofY.
t
| processes, | thus                                  | mitigating | the | training-inference |     |     |     |                             |     |     |     |     |     |
| ---------- | ------------------------------------- | ---------- | --- | ------------------ | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- |
|            |                                       |            |     |                    |     |     | 2.2 | KnowledgeDistillationofLLMs |     |     |     |     |     |
| mismatch.  | Morespecifically,insteadofautoregres- |            |     |                    |     |     |     |                             |     |     |     |     |     |
sivelygeneratingtheon-policydata,thegeneration KnowledgeDistillation(KD)aimstocompressa
processesofimperfectdataonlyrequireone-pass largeteachermodelM bydistillingitsknowledge
p
intoasmallstudentmodelMθ
forward, which is more efficient and affordable. parameterizedbyθ.
q
|     |     |     |     |     |     |     | GivenadivergencefunctionF |     |     |     |     | andatrainingsetG, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | ----------------- | --- |
Moreover,bydoingso,wecanalsoencouragethe
student to learn how to calibrate these imperfect wecantrainthestudentmodelasfollows:
tokensandfurtherimprovetheKDperformance.
|                                           |     |           |            |      |               |         | θ∗       | := argminE |         |         | [F(M              | ∥Mθ)(y|x)], | (2)    |
| ----------------------------------------- | --- | --------- | ---------- | ---- | ------------- | ------- | -------- | ---------- | ------- | ------- | ----------------- | ----------- | ------ |
| We evaluate                               |     | KID on    | a variety  | of   | popular       | text-   |          |            |         | (x,y)∼G |                   | q q         |        |
| to-SQL benchmarks,                        |     | including |            | BIRD | (Li           | et al., |          |            |         |         |                   |             |        |
|                                           |     |           |            |      |               |         | where    | (x,y)      |         | is      | the task-specific |             | input- |
| 2024b), Spider                            |     | (Yu et    | al., 2018) | and  | its variants, |         |          |            |         |         |                   |             |        |
|                                           |     |           |            |      |               |         |          | pair2      |         |         |                   | ∥Mθ)(y|x)   |        |
|                                           |     |           |            |      |               |         | output   |            | of      | G, and  | F(M               | q           | =      |
| upon3typesofautoregressiveLLMs:           |     |           |            |      | QWen(Bai      |         |          |            |         |         |                   | q           |        |
|                                           |     |           |            |      |               |         | (cid:80) | |y |       | (cid:0) |         |                   | (cid:1)     |        |
|                                           |     |           |            |      |               |         | 1        | F          | p(·|x,y |         | )∥qθ(·|x,y        | )           | is the |
| etal.,2023),CodeGen(Nijkampetal.,2022)and |     |           |            |      |               |         | |y |     | t = 1      |         | <t      |                   | <t          |        |
LLaMA(Touvronetal.,2023). Resultsshowthat divergence between the teacher and student
|     |     |     |     |     |     |     |     |     |     |     | p   | qθ, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
KIDcannotonlyachieveabettertrade-offbetween distributions, denoted as and respectively.
|     |     |     |     |     |     |     | The | choices | of  | training | set | G and | divergence |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | --- | ----- | ---------- |
performanceandefficiency,butalsobringconsis-
tent and significant improvements (up to +5.83% function F give rise to different possible KD
| average score) |     | among | all model | types | and | sizes. |     |     |     |     |     |     |     |
| -------------- | --- | ----- | --------- | ----- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
2Fortext-to-SQLtaskin§2.1,xreferstotheinputquestion
Moreover,comparedtothestandardKD,KIDcan P(Q,D)andyreferstotheoutputSQLqueryY.

Method Divergence TrainingDataset Method Divergence 1.8B 4B 7B
| Datatype:Fixeddataset |     |                  |     |     |     |     | Trainingdata:Fixeddataset |     |     |     |      |      |      |
| --------------------- | --- | ---------------- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | ---- | ---- | ---- |
| FKD                   | FKL | Ground-truthdata |     |     |     |     |                           |     |     |     |      |      |      |
|                       |     |                  |     |     |     |     | FKD                       |     | FKL |     | 57.3 | 57.4 | 57.3 |
| RKD                   | RKL | Ground-truthdata |     |     |     |     |                           |     |     |     |      |      |      |
|                       |     |                  |     |     |     |     | RKD                       |     | RKL |     | 62.7 | 60.1 | 61.5 |
Datatype:Model-generateddataset
|           |     | DatageneratedbyMpandMθ |     |     |     |     | Trainingdata:Model-generateddataset |     |     |     |     |     |     |
| --------- | --- | ---------------------- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- |
| f-distill | TVD |                        |     |     | q   |     |                                     |     |     |     |     |     |     |
ImitKD FKL Ground-truth+datageneratedbyMθ f-distill TVD 57.6 58.6 59.6
q
GKD FKL/RKL/JSD On-policydatageneratedbyMθ ImitKD FKL 58.3 59.5 59.1
q
|     |     |                           |     |     |     |     | GKD-FKL |     | FKL |     | 61.1 | 62.1 | 60.7 |
| --- | --- | ------------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | ---- | ---- | ---- |
| KID | RKL | Imperfectground-truthdata |     |     |     |     |         |     |     |     |      |      |      |
|     |     |                           |     |     |     |     | GKD-RKL |     | RKL |     | 62.9 | 63.8 | 64.3 |
Table1:SummaryofvariousKDalgorithmsinterms GKD-JSD JSD 62.8 62.7 64.3
| of training | data | and divergence. | Notably, |     | M and |       |     |             |     |              |     |         |        |
| ----------- | ---- | --------------- | -------- | --- | ----- | ----- | --- | ----------- | --- | ------------ | --- | ------- | ------ |
|             |      |                 |          |     | p     | Table | 2:  | Preliminary |     | experimental |     | results | (%) of |
Mθdenotetheteacherandstudentmodels,respectively.
q
variousKDmethods.Wereporttheexecutionaccuracy
ofQWen1.5-0.5BdistillingfromQWen1.5-{1.8B,4B,
|             |       |         |          |     |         | 7B}ontheSpiderbenchmark. |     |     |     |     | Bestresultsareinbold. |     |     |
| ----------- | ----- | ------- | -------- | --- | ------- | ------------------------ | --- | --- | --- | --- | --------------------- | --- | --- |
| algorithms, | e.g., | Forward | KD (FKD) |     | (Hinton |                          |     |     |     |     |                       |     |     |
etal.,2015),ReverseKD(RKD)(Guetal.,2023),
|           |         |             |        |      |         |     |     | FKD | RKD | f-distill |     | ImitKD | GKD |
| --------- | ------- | ----------- | ------ | ---- | ------- | --- | --- | --- | --- | --------- | --- | ------ | --- |
| f-distill | (Wen et | al., 2023), | ImitKD | (Lin | et al., |     |     |     |     |           |     |        |     |
+11.6×
+10.5×
| 2020) and | GKD | (Agarwal | et al., | 2024). | The |     |                      |       |     |     |     |     |     |
| --------- | --- | -------- | ------- | ------ | --- | --- | -------------------- | ----- | --- | --- | --- | --- | --- |
|           |     |          |         |        |     |     | )×( ycnetaL gniniarT | +8.9× |     |     |     |     |     |
summaryoftheserepresentativeKDalgorithmsis
showninTable1.
| The | common | divergences | for KD | contain | the |     |     |     |     |     |     |     |     |
| --- | ------ | ----------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ForwardKullback-Leibler(FKL)(VanErvenand
| Harremos,      | 2014), | Reverse        | KL (RKL) |            | (Malinin    |                   |     |                                     |     |                            |     |            |     |
| -------------- | ------ | -------------- | -------- | ---------- | ----------- | ----------------- | --- | ----------------------------------- | --- | -------------------------- | --- | ---------- | --- |
|                |        |                |          |            |             |                   |     | Qwen1.5-1.8B                        |     | Qwen1.5-4B                 |     | Qwen1.5-7B |     |
| and Gales,     | 2019), | Jensen–Shannon |          | divergence |             |                   |     |                                     |     |                            |     |            |     |
|                |        |                |          |            |             | Figure2:          |     | Comparisonsoftraininglatencybetween |     |                            |     |            |     |
| (JSD) (Fuglede | and    | Topsoe,        | 2004)    | and        | total vari- |                   |     |                                     |     |                            |     |            |     |
|                |        |                |          |            |             | variousKDmethods. |     |                                     |     | Thex-axisdenotestheteacher |     |            |     |
| ation distance | (TVD)  | (Verdú,        | 2014).   |            | The de-     |                   |     |                                     |     |                            |     |            |     |
models,andthey-axisdenotesthetraininglatencyrel-
tails of these divergences can be found in Ap- ativetotheSFTbaseline. Foreaseofillustration,we
pendix A.3. On the other hand, G may consist onlyreporttheresultsofRKLdivergenceforGKD.
ofinput-outputpairsintheoriginaltrainingset(de-
notedasground-truthdataset),orsequencesgen-
Spider(Yuetal.,2018)isusedastrainingdata,and
| erated from                | teacher | M   | or student       | Mθ  | (denoted |     |        |     |           |     |        |             |      |
| -------------------------- | ------- | --- | ---------------- | --- | -------- | --- | ------ | --- | --------- | --- | ------ | ----------- | ---- |
|                            |         | p   |                  | q   |          |     |        |     |           |     |        |             |      |
|                            |         |     |                  |     |          | the | models | are | evaluated |     | on the | development | set. |
| asmodel-generateddataset). |         |     | Forthedatagener- |     |          |     |        |     |           |     |        |             |      |
WefollowLietal.(2024a)andusethe“Execution
| ated by | M , we | feed the | input into | the | M and |     |     |     |     |     |     |     |     |
| ------- | ------ | -------- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
|         | p      |          |            |     | p     |     |     |     |     |     |     |     |     |
Accuracy”asmetrictoquantifythemodeloutput.
| obtain                   | the teacher’s | output | beforehand            |     | and keep |           |     |     |             |     |         |     |           |
| ------------------------ | ------------- | ------ | --------------------- | --- | -------- | --------- | --- | --- | ----------- | --- | ------- | --- | --------- |
| themfixedduringtraining. |               |        | Conversely,forthedata |     |          |           |     |     |             |     |         |     |           |
|                          |               |        |                       |     |          | Findings. |     | The | comparative |     | results | are | listed in |
generatedbyMθ,sincethestudentiscontinuously
|     | q   |     |     |     |     | Table2,fromwhichweempiricallyfindthat: |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
updated,weobtainthestudent’soutputinanonline
fashion. Suchonlinegenerateddataisalsocalled Reverse KL is more suitable for distilling the
“on-policydata”byAgarwaletal.(2024). text-to-SQLLLMs. Wefirstanalyzetheimpact
ofdifferentdivergencefunctions,andfindthatRKL
2.3 EmpiricalAnalyses generallyoutperformstheotherdivergences,e.g.,
|     |     |     |     |     |     | FKD | (57.4%) |     | v.s. RKD | (60.1%) |     | and | GKD-FKL |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | ------- | --- | --- | ------- |
Asmentionedin§1,itisunder-exploredwhether
theaforementionedKDalgorithmsworkwellfor (62.1%)v.s. GKD-RKL(63.8%). Thisissimilarto
thestatementsofpriorstudies(Guetal.,2023;Wu
| text-to-SQL | LLMs. | Hence, | we conduct |     | prelimi- |     |     |     |     |     |     |     |     |
| ----------- | ----- | ------ | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
etal.,2024),astheyarguethatReverseKLshows
naryexperimentstoinvestigateitinthispart.
mode-seekingbehaviors,i.e.,itdoesnotforcethe
Setting. We conduct experiments by first fine- studenttofitallteacher’sdistributions,butassigns
tuninglargerLLMsontheoriginaltrainingdataset highprobabilitiestoteacher’slargemodesandig-
as teachers. Then, we use different KD methods noresthesmallones. Inthecontextoftext-to-SQL,
todistillasmallerstudentwiththeteacher’sguid- the output tokens (e.g., table/column name and
ance. Here,weusetheQWen1.5-0.5B(Baietal., value) are usually precise and low-diversity, and
2023)asthestudentandusetheotherQWen-family enforcingthestudenttolearnthehigh-probability
models(i.e.,QWen1.5-1.8B/-4B/-7B)asteachers. regionscouldleadtobetterperformance.

𝒑(𝒚|𝒙)
Teacher
|     |     |     | ☃   |     | Prefix𝒙 | 𝒚𝟏  | 𝒚+𝟐 | 𝒚𝟑  | 𝒚+𝟒 𝒚𝟓 | 𝒚𝟔  |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | ------ | --- | --- | --- | --- |
𝒒𝜽
| Ground-truth data(𝑥,𝑦) |     | Student |     | KL Divergence |     |     |     |            |     |     |     |        |     |
| ---------------------- | --- | ------- | --- | ------------- | --- | --- | --- | ---------- | --- | --- | --- | ------ | --- |
|                        |     |         | 🔥   |               |     |     |     | ③Rewriting |     |     |     |        |     |
|                        |     |         |     |               |     |     |     |            |     |     | ☃   | Frozen |     |
(a) KD with ground-truth data
|     |     |     |         |         |     | 𝒚+𝟐 |     | 𝒚+𝟒          |     |     |     |           |     |
| --- | --- | --- | ------- | ------- | --- | --- | --- | ------------ | --- | --- | --- | --------- | --- |
|     |     |     |         | 𝒑(𝒚!|𝒙) |     |     |     | ②Predicating |     |     | 🔥   | Trainable |     |
|     | 𝑥   |     | Teacher |         |     |     |     |              |     |     |     |           |     |
☃
Autoregressive
|         | Inference |                                  |          | 𝒒𝜽            |         |     | Student | ☃                |     |     | 𝒙   | Prefix input        |     |
| ------- | --------- | -------------------------------- | -------- | ------------- | ------- | --- | ------- | ---------------- | --- | --- | --- | ------------------- | --- |
| Student |           | (𝒙,𝒚′)                           | Student🔥 | KL Divergence |         |     |         |                  |     |     |     |                     |     |
|         |           | On-policy data                   |          |               |         |     |         | One-pass Forward |     |     | 𝒚   | Ground-truth output |     |
|         | ☃         | (b) KD with model-generated data |          |               |         |     |         |                  |     |     |     |                     |     |
|         |           |                                  |          |               | Prefix𝒙 |     |         | <s>              |     |     |     |                     |     |
|         |           |                                  |          |               |         | 𝒚𝟏  | <s>     | 𝒚𝟑               | 𝒚𝟓  | 𝒚𝟔  | 𝒚+  | Imperfect output    |     |
𝒑(𝒚+|𝒙)
|         | (𝑥,𝑦)    |            | Teacher |               |         |     |     |          |       |     |     |            |     |
| ------- | -------- | ---------- | ------- | ------------- | ------- | --- | --- | -------- | ----- | --- | --- | ---------- | --- |
|         |          |            | ☃       |               |         |     |     | ①Masking |       |     |     |            |     |
|         | One-pass |            |         |               |         |     |     |          |       |     | <s> | Mask token |     |
|         | Rewrite  |            |         | 𝒒𝜽            |         |     |     |          |       |     |     |            |     |
| Student |          | ( 𝒙 , 𝒚+ ) | Student | KL Divergence | Prefix𝒙 | 𝒚𝟏  | 𝒚𝟐  | 𝒚𝟑       | 𝒚𝟒 𝒚𝟓 | 𝒚𝟔  |     |            |     |
🔥
|     | ☃   | Impe r fe c t  data               |     |     |     |                                           |     |     |     |     |     |     |     |
| --- | --- | --------------------------------- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     | (c) KD with imperfect data (Ours) |     |     |     | (d) Pipeline to obtain the imperfect data |     |     |     |     |     |     |     |
Figure3: IllustrationsofdifferentKDmethods: (a)KDmethodswithground-truthdata,(b)KDmethodswith
model-generateddataand(c)ourKIDmethodwithimperfectdata. Additionally,weshow(d)thepipelinetoobtain
theimperfectdata,whichcontainsthree-stageprocesses: ❶masking,❷predictingand❸rewriting.
Model-generated datasets perform better but IntuitionofKID. Asstatedbypriorstudies(Pang
suffer from training inefficiency. By compar- andHe,2020;Agarwaletal.,2024),thetraining-
ingtheKDresultsbetweenground-truthdatasets inferencemismatchmainlycomesfromthecascad-
andmodel-generateddatasets,wefindthatmodel- ing effect of inference. Specifically, during train-
generated datasets perform better than the fixed ing,LLMsconditiononground-truthtokens. How-
ground-truthones,especiallytheon-policydataset ever,duringinference,theyconditiononthemodel-
generatedbystudents(i.e.,GKD).Thisisbecause generatedtokens,whichmightbewrongandaffect
that student-generated dataset can alleviate the thefuturepredictions. Intuitively,enforcingthestu-
training-inferencemismatch,i.e.,thediscrepancy denttorewritetheground-truthtrainingdatainto
between teacher-forcing training and free-run in- imperfect one, i.e., introducing some errors dur-
ference. Despite its remarkable performance, it ing training, can simulate the cascading effect of
requires the student to autoregressively generate inferenceandthusmitigatethetraining-inference
the output in an online manner, which will lead mismatch. Moreover,byencouragingthestudent
to unaffordable training latency. This can be em- to learn how to calibrate these imperfect tokens,
pirically proven by the results in Figure 2, as the KIDcanfurtherimprovetheperformance.
traininglatencyofGKDismuchhigherthanthose
|     |     |     |     |     |     | PipelinetoObtaintheImperfectData. |     |     |     |     |     | Thekey |     |
| --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | ------ | --- |
trainedonground-truthdatasets.
techniqueofKIDistorewritetheground-truthdata
|     |     |     |     |     |     | intoanimperfectone. |     |     |     | Specifically,thegeneration |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | -------------------------- | --- | --- | --- |
3 ImprovingKnowledgeDistillationwith
ofimperfectdataconsistsofthree-stageprocesses:
| ImperfectData |     |     |     |     |     | ❶   |          | ❷   |            |     | ❸   |            |     |
| ------------- | --- | --- | --- | --- | --- | --- | -------- | --- | ---------- | --- | --- | ---------- | --- |
|               |     |     |     |     |     |     | masking, |     | predicting |     | and | rewriting. | In  |
practice,we❶firstsampleαoftokens3
fromthe
MotivationandOverview. Basedontheobser- ground-truthoutputyandmaskthemwithaspecial
vationin§2,werecognizethatthekeyforimprov-
|     |     |     |     |     |     | token | (e.g., | “<s>”). |     | For sampling |     | the tokens, | we  |
| --- | --- | --- | --- | --- | --- | ----- | ------ | ------- | --- | ------------ | --- | ----------- | --- |
ingtheperformanceKDistoalleviatethetraining-
|     |     |     |     |     |     | design | some | strategies: |     | 1)  | “Random”: | randomly |     |
| --- | --- | --- | --- | --- | --- | ------ | ---- | ----------- | --- | --- | --------- | -------- | --- |
inference mismatch. However, the current KD sampling, 2) “Uniform”: uniformly sampling, 3)
methodsrelyingonmodel-generateddatasetsusu-
“Hard”: samplingαoftokenswiththelowestcon-
allysufferfromtraininginefficiency,i.e.,theyfail
|            |     |             |     |                 |       | fidence;4)“Easy”: |     |             | samplingαoftokenswiththe |      |               |     |        |
| ---------- | --- | ----------- | --- | --------------- | ----- | ----------------- | --- | ----------- | ------------------------ | ---- | ------------- | --- | ------ |
| to balance | the | performance |     | and efficiency. | Thus, |                   |     |             |                          |      |               |     |        |
|            |     |             |     |                 |       | highest           |     | confidence. |                          | More | specifically, | for | 3) and |
there raises a question: whether we can mitigate 4),wefeedtheoriginalsequencey intothestudent
thetraining-inferencemismatchmoreefficiently?
forobtainingpredictionprobabilitiesqθ,andthen
i
Motivatedbythis,weproposetoimproveKDwith computetheentropyofqθ astheconfidence4.
i
| imperfect | data | (KID), | which | effectively | and effi- |     |     |     |     |     |     |     |     |
| --------- | ---- | ------ | ----- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
ciently booststhe performanceby simulating the 3Theanalysisofsamplingratioαcanbefoundin§4.3.
4Intuitively,thetokenswithhighentropyvaluearehard-to-
| cascadingeffectofinferenceduringtraining. |     |     |     |     | The |     |     |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
learn,asthemodelpredictthemwithlowconfidencetowards
illustrationofKIDisshowninFigure3. thegoldlabels(Zhongetal.,2023).

Aftermaskingthespansofy,we❷thengener- EK”)andwith(“w/EK”)externalknowledge. The
ateimperfecttokenstofillinthespans. Specifically, detailsofalltasksareshowninAppendixA.1.
we feed the masked sequence into the student to
Models. WeevaluateKIDonthreetypesofLLMs
generatepredictionswithaone-passforwardpro-
withvarioussizes: QWen1.5(Baietal.,2023)(stu-
cess. Finally,giventhepredictedimperfecttokens
on the masking place, we ❸ rewrite the ground- dent: 0.5B,teachers: 1.8B,4B,7B),CodeGen(Ni-
jkampetal.,2022)(student: 350M,teachers: 2B),
truthy intotheimperfectoneyˆ.
andLLaMA2(student: TinyLLaMA-1.1B(Zhang
TrainingofKID. Duringtraining,givenamini- etal.,2024b),teachers: 7B(Touvronetal.,2023)).
batchofinput-outputpairs(x,y),wefirstperform All models are trained with a popular parameter-
the above processes to obtain the imperfect data efficientfine-tuningmethod,i.e.,LoRA(Huetal.,
(x,yˆ). Then,wecantrainthestudentmodelwith 2021). Thedetailsofalltraininghyper-parameters
the teacher’s guidance. As shown in §2, Reverse canbefoundinAppendixA.2.
KLismoresuitablefortext-to-SQLtask,andwe
Baselines. We consider 5 cutting-edge KD
thus use it as the divergence function in our KID.
baselines in our main experiment: Forward
Moreover,sinceourKIDrequiresamplingfroma
KD (FKD) (Hinton et al., 2015), Reverse KD
student, which may generate poor samples at the
(RKD)(Guetal.,2023),f-distill(Wenetal.,2023),
beginningoftrainingandmakethedistillingmore
ImitKD (Lin et al., 2020) and GKD5 (Agarwal
difficult,wefollowpriorworks(Wenetal.,2023;
et al., 2024). For reference, we also report the
Guetal.,2023)andcombinetheKDlossinEq.2
performance of teachers as the upper bound. We
withanauxiliarymaximumlikelihoodestimation
usethecodebaseofLiuetal.(2023)toimplement
(MLE) loss. Specifically, the MLE loss enforces
thesebaselinesanddistillstudents.
the student to predict the ground-truth target se-
quencesy. Notably,forafaircomparison,wealso
4.2 MainResults
add the auxiliary MLE loss into the baseline KD
KIDachievesabettertrade-offbetweentheKD
methodsthatrelyontheground-truthdata.
performance and efficiency. The main results
on QWen-family models are listed in Table 3.
4 Experiments
As seen, most KD methods outperform the SFT
4.1 Setup baseline,whileintroducingextratrainingbudgets.
Training with the on-policy data, GKD achieves
Tasks and Datasets. We conduct our main ex-
much better performance than the other counter-
perimentsontwopopulartext-to-SQLbenchmarks,
parts. However,thecomputationalbudgetofGKD
i.e., Spider (Yu et al., 2018) and BIRD (Li et al.,
isnotaffordable,asitleadstoupto13.9×training
2024b). For each task, models are trained with
latencyagainsttheSFTbaseline. Conversely,our
theoriginaltrainingsetandevaluatedonthedevel-
KIDcannotonlyachievecomparableorevenbetter
opmentset,denotedasSpider-devandBIRD-dev,
performancethanGKD,butalsoeffectivelyreduce
respectively. Moreover,followingpriorstudies(Li
the training latency. These results can prove the
et al., 2023, 2024a), we also evaluate the mod-
superiorityofourmethod.
els trained with the Spider dataset on three more
challenging robustness benchmarks, i.e., Spider- KID brings consistent and significant perfor-
DK (Gan et al., 2021b), Spider-Realistic (Deng mance gains among all model sizes and types.
etal.,2021)andSpider-Syn(Ganetal.,2021a). In addition to QWen-family models, we also ap-
ForevaluationonSpider-familybenchmarks,we plyourmethodonCodeGenandLLaMAmodels,
utilize two widely-used metrics, i.e., “Execution and report the results in Table 4. Notably, due to
Accuracy”(EX)(Yuetal.,2018)and“Test-Suite thespacelimitation,weonlyreportthecontrastive
Accuracy” (TS) (Zhong et al., 2020). For BIRD, resultsoftwomostrelevantKDcounterparts,i.e.,
wesimplyusetheEXastheevaluationmetric. No- RKDandGKD.FromtheresultsofTable3and4,it
tably,BIRDoffersexternalknowledgeforguiding canbefoundthatourKIDconsistentlyoutperforms
the generation of SQL queries. Considering that the other KD counterparts and brings significant
suchexternalknowledgeisusuallyunavailablein
5AsshowninTable2,GKDwithRKLdivergence(i.e.,
therealworld,wefollowLietal.(2024a)andper-
GKD-RKL)performsbest,andwethusonlyreporttheresults
formtheevaluationintwosettings: without(“w/o ofGKD-RKLforGKDinthefollowingcontent.

|        |         | Spider-dev | BIRD-dev(EX%)  | Spider-DK |     | Spider-Real | Spider-Syn |     |      | Score |
| ------ | ------- | ---------- | -------------- | --------- | --- | ----------- | ---------- | --- | ---- | ----- |
| Method | Latency |            |                |           |     |             |            |     |      |       |
|        |         | EX%        | TS% w/oEK w/EK | EX%       | TS% | EX% TS%     | EX%        | TS% | Avg. | ∆     |
Student:QWen1.5-0.5B
SFT 1.0× 57.8 56.4 16.36 30.51 44.8 46.5 50.6 47.6 44.2 43.7 43.85 *
Teacher:QWen1.5-1.8B
Teacher 1.5× 67.3 66.3 21.71 34.22 54.6 52.3 62.0 60.8 52.7 52.6 52.45 -
FKD 2.1× 57.3 56.5 16.82 28.68 43.7 41.7 50.2 48.0 43.7 43.3 42.99 -0.86
RKD 2.0× 62.7 61.5 16.10 31.81 50.8 49.2 51.2 49.6 48.7 48.3 46.99 +3.14
f-distill 6.0× 57.6 56.3 15.78 27.90 45.0 43.2 52.6 51.0 43.4 43.0 43.58 -0.27
5.9×
ImitKD 58.3 57.2 16.04 28.49 46.2 44.1 52.4 50.8 44.1 43.3 44.09 +0.24
GKD 10.9× 62.9 61.6 18.25 32.99 49.9 47.9 50.6 48.6 48.6 48.1 46.94 +3.09
KID(Ours) 2.0× 63.7 63.1 18.38 33.12 47.6 45.4 53.0 51.4 47.5 47.0 47.02 +3.17
Teacher:QWen1.5-4B
Teacher 3.0× 78.2 77.3 35.27 48.11 61.3 58.7 72.6 70.3 67.4 66.8 63.60 -
FKD 2.2× 57.4 56.5 18.32 29.34 47.1 45.6 50.6 48.6 42.4 41.8 43.77 -0.08
RKD 2.2× 60.1 59.1 17.01 31.75 45.8 43.6 49.6 47.4 46.1 45.6 44.61 +0.76
f-distill 6.3× 58.6 57.3 17.67 31.55 45.8 43.6 50.8 49.2 44.4 43.8 44.27 +0.42
ImitKD 6.3× 59.5 59.4 19.04 30.31 48.6 46.9 49.2 46.9 45.0 44.5 44.94 +1.09
GKD 12.7× 63.8 62.4 20.21 36.11 50.8 48.2 55.5 53.3 47.5 46.9 48.47 +4.62
KID(Ours) 2.3× 65.8 64.7 20.08 33.57 50.5 48.0 55.1 53.3 47.6 47.0 48.57 +4.72
Teacher:QWen1.5-7B
Teacher 3.3× 81.6 80.6 39.44 52.02 67.7 64.9 76.6 74.2 70.1 69.5 67.67 -
FKD 2.4× 57.3 56.4 17.14 31.03 46.4 44.9 50.6 49.0 41.0 40.5 43.43 -0.42
RKD 2.3× 61.5 60.2 16.10 31.81 48.4 46.5 51.0 49.2 46.7 46.0 45.74 +1.89
f-distill 7.2× 59.6 58.2 18.19 32.78 47.7 46.0 49.8 47.6 44.9 44.4 44.92 +1.07
ImitKD 7.2× 59.1 57.9 17.60 30.44 47.3 45.4 48.8 47.2 43.8 43.4 44.09 +0.24
GKD 13.9× 64.3 62.9 20.08 34.62 51.6 49.7 54.1 51.6 46.9 46.2 48.20 +4.35
KID(Ours) 2.3× 64.0 62.6 20.40 34.35 50.7 48.5 52.4 50.8 47.7 47.3 47.88 +4.03
Table3: EvaluationofQWen-familymodelsonseveralpopulartext-to-SQLbenchmarks. Notably,“Latency”
means the average training latency relative to the SFT baseline. “Spider-Real” refers to the Spider-Realistic
benchmark. “Avg.” denotestheaverageperformanceamongallbenchmarksand“∆”denotestheperformancegains
| againsttheSFTbaseline. |     | Bestperformanceineachgroupisemphasizedinbold. |     |     |         |             |     |         |          |        |
| ---------------------- | --- | --------------------------------------------- | --- | --- | ------- | ----------- | --- | ------- | -------- | ------ |
|                        |     |                                               |     | SQL | models. | Contrastive |     | results | on these | bench- |
marksshowthatourKIDexhibitsexceptionalper-
+5.1
formanceandeffectivelyimprovestherobustness
|     |     |     |     | ofdistilledstudents. |     |     | Forexample,whendistilling |     |     |     |
| --- | --- | --- | --- | -------------------- | --- | --- | ------------------------- | --- | --- | --- |
CodeGenmodels,KIDachievesgainsof2.7%on
|     | +5.3 |     |     | Spider-DK(43.7%to46.4%)and2.1%onSpider- |        |     |         |           |     |          |
| --- | ---- | --- | --- | --------------------------------------- | ------ | --- | ------- | --------- | --- | -------- |
|     |      |     |     | Realistic                               | (45.5% | to  | 47.6%), | comparing |     | with the |
bestcounterpart.
|     | CodeGen-350M |     | TinyLLaMA-1.1B |     | AnalysisofKID |     |     |     |     |     |
| --- | ------------ | --- | -------------- | --- | ------------- | --- | --- | --- | --- | --- |
4.3
| Figure 4: | Analysis | of different | masking strategies. |     |     |     |     |     |     |     |
| --------- | -------- | ------------ | ------------------- | --- | --- | --- | --- | --- | --- | --- |
Weevaluatetheimpactofeachcomponentofour
They-axisdenotestheEXperformanceonSpider-dev.
|     |     |     |     | KID, | including | 1) masking |     | strategies, | 2)  | masking |
| --- | --- | --- | --- | ---- | --------- | ---------- | --- | ----------- | --- | ------- |
Forreference,wealsoreporttheresultsofSFT.
ratioα,and3)rewritingapproachforobtainingthe
|     |     |     |     | imperfect |     | data. Additionally, |     | we  | 4) perform | the |
| --- | --- | --- | --- | --------- | --- | ------------------- | --- | --- | ---------- | --- |
performance gains (up to +5.83% average score) in-depthanalysisonthetrainingefficiencyofKID.
againsttheSFTbaselineamongallmodelsizesand
|     |     |     |     | Effectofdifferentmaskingstrategies. |     |     |     |     |     | Asmen- |
| --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | ------ |
types,indicatingitsuniversality.
tionedin§3,weintroduceseveralstrategiestose-
KID effectively improves the robustness of lect the tokens for masking. Here, we conduct
distilled models. Spider-DK, Spider-Syn, and experiments to analyze the impact of different
Spider-Realistic are widely-used challenging masking strategies. Results of CodeGen-350M
benchmarkstoinvestigatetherobustnessoftext-to- and TinyLLaMA-1.1B in Figure 4 show that: 1)

Spider-dev BIRD-dev(EX%) Spider-DK Spider-Real Spider-Syn Score
Method Latency
EX% TS% w/oEK w/EK EX% TS% EX% TS% EX% TS% Avg. ∆
Student:CodeGen-350M,Teacher:CodeGen-2B .
SFT 1.0× 53.1 51.8 9.90 26.01 37.4 36.1 38.4 36.0 35.4 34.9 35.90 *
Teacher 3.7× 72.3 71.3 26.47 35.66 57.9 55.1 63.2 61.6 55.4 54.8 55.37 -
RKD 2.1× 55.1 54.4 10.50 27.18 43.6 40.0 43.1 40.7 37.6 36.8 38.90 +3.00
GKD 14.1× 56.6 54.9 11.44 27.57 43.7 40.4 45.5 43.1 40.1 39.3 40.26 +4.36
KID(Ours) 2.4× 58.4 56.8 10.52 27.57 46.4 44.1 47.6 44.5 41.1 40.3 41.73 +5.83
Student:TinyLLaMA-1.1B,Teacher:LLaMA2-7B .
SFT 1.0× 63.0 61.8 13.40 24.77 49.0 48.0 54.7 52.4 51.4 50.6 46.91 *
Teacher 2.6× 78.8 77.9 35.40 48.63 64.5 61.1 72.4 70.1 67.6 66.4 64.28 -
RKD 1.4× 66.0 64.6 15.45 31.75 48.4 46.9 55.7 54.1 52.9 52.2 48.80 +1.89
GKD 8.3× 64.8 63.2 16.62 33.44 52.1 49.9 54.1 51.0 53.0 51.8 49.00 +2.09
KID(Ours) 1.5× 68.1 66.8 18.97 32.53 52.9 51.8 59.8 57.7 55.0 54.5 51.81 +4.90
Table4: EvaluationofCodeGenandLLaMAmodelsonseveraltext-to-SQLbenchmarks. Duetothespace
constraints,weonlypresentthecontrastiveresultsofmostrelevantKDcounterparts,i.e.,RKDandGKD.
74
70
65
60
55
50
0.1 0.2 0.3 0.4 0.5
Value of
)%(
ved-redipS
no
ecnamrofreP
Method CodeGen TinyLLaMA
TinyLLaMA -- SFT CodeGen -- SFT
TinyLLaMA -- Ours CodeGen -- Ours SFT 53.1 63.0
VanillaKID 55.1 66.0
-w/Masking-only 55.8(↑0.7) 66.5(↑0.5)
-w/Rewriting(Ours) 58.4(↑3.3) 68.1(↑2.1)
Table 5: Impact of rewriting approach of KID. No-
tably,“VanillaKID”meansthatwedonottrainwiththe
imperfectdatainourKID,“-w/Masking-only”denotes
thatwedirectlyusethesequencewithmaskingspans
asfinalimperfectdataduringthetrainingofKID,and
“-w/Rewriting(Ours)”referstothefullKID.
Figure 5: Parameter analysis of masking ratio α.
We report the EX results of TinyLLaMA-1.1B and
Figure 5 illustrates the contrastive results. Com-
CodeGen-350MontheSpider-dev.
paredwiththeSFTbaseline,ourKIDconsistently
brings improvements across a certain range of α
Our KID with various masking strategies consis- (i.e.,0.1to0.3),basicallyindicatingthattheperfor-
tently outperforms the SFT baseline. 2) Perfor- manceofKIDisnotsensitivetoα. 2)Toolargeα
mance of difficulty-driven strategies (i.e., “Easy” values(e.g.,0.5)leadtoperformancedegradation,
and“Hard”)isunstable,aspayingtoomuchatten- astoomanyrewritingtokensmightdistortthese-
tiontotheeasy-to-learn/hard-to-learntokensmight quencemeaningandarechallengingformodelsto
affect the learning of the other tokens and thus calibrate. More specifically, the case of α = 0.2
leads to sub-optimal performance. 3) The “Ran- performsbest,andweusethissettingasdefault.
dom”strategyachievesconsistentlybetterperfor-
Impactofrewritingapproach. Inthestage❸
mance. Weconjecturethatsucharandommasking
of pipeline for obtaining the imperfect data, we
strategy is closer to the errors that are prone to
rewrite the ground-truth data with the predicted
occur during inference, as a model might predict
imperfect tokens. To verify its effectiveness, we
incorrect tokens at any inference step. Thus, we
compareitwithasimplealternative,i.e.,directly
usethe“Random”strategyasourdefaultsetting.
usingthesequencewithmaskingspans(outputof
Parameter analysis on α. The α used to con- stage ❶) as final imperfect data yˆ, denoted as “-
trol the ratio of masking tokens is an important w/masking-only”. Table5showsthecontrastive
hyper-parameter. Here,weanalyzeitsinfluenceby results(EXresultsonSpider-dev),inwhichwesee
evaluating the performance of KID with different that1)thealternativeapproachequippedwithKID
α,spanning{0.1,0.2,0.3,0.4,0.5}onSpider-dev. outperforms the SFT, showing the superiority of

65
|                               |     |     |     |     |     | Method  | Spider-dev                            | Spider-DK |     | Spider-Real | Spider-Syn |      |
| ----------------------------- | --- | --- | --- | --- | --- | ------- | ------------------------------------- | --------- | --- | ----------- | ---------- | ---- |
| )%( ved-redipS no ecnamrofreP |     |     |     |     |     | FKD     | 57.4                                  | 44.7      |     | 52.8        |            | 42.8 |
|                               |     |     |     |     |     | RKD     | 60.3                                  | 50.5      |     | 51.2        |            | 44.6 |
|                               | 60  |     |     |     |     | KID     | 63.7                                  | 50.8      |     | 52.2        |            | 49.2 |
|                               |     |     |     |     |     | Table6: | Performance(EX%)onSpider-familybench- |           |     |             |            |      |
marksofQWen1.5-0.5BdistillingfromQWen1.5-32B.
55
|     |     |     | FKD       | ImitKD     |     | Metric      |     | FKD RKD     | f-distill |       | GKD   | KID   |
| --- | --- | --- | --------- | ---------- | --- | ----------- | --- | ----------- | --------- | ----- | ----- | ----- |
|     | 50  |     | RKD       | GKD        |     |             |     |             |           |       |       |       |
|     |     |     |           |            |     | ExAccErr(↓) |     | 35.4        | 16.2      | 11.3  | 0.8   | 5.3   |
|     |     |     | f-distill | KID (Ours) |     |             |     |             |           |       |       |       |
|     | 48  |     |           |            |     | Performance |     | 31.03 31.81 |           | 32.78 | 34.62 | 34.35 |
|     | 1K  | 2K  | 3K        | 4K         | 5K  |             |     |             |           |       |       |       |
Training Steps
|        |                |     |               |     |          | Table 7:      | Results | of Qwen1.5-0.5B               |     | on  | BIRD-dev | (w/ |
| ------ | -------------- | --- | ------------- | --- | -------- | ------------- | ------- | ----------------------------- | --- | --- | -------- | --- |
| Figure | 6: Performance |     | on Spider-dev | of  | students |               |         |                               |     |     |          |     |
|        |                |     |               |     |          | EK)benchmark. |         | QWen1.5-7Bisusedastheteacher. |     |     |          |     |
(QWen1.5-0.5B)trainedwithdifferentKDmethods
| forthefulltrainingprocess. |     |     | QWen1.5-1.8Bisusedas |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theteacher. WeseethatKIDachievescomparableper- DoesKIDindeedalleviatethetraining-inference
formancewithmostcounterpartsat2Ktrainingsteps.
|     |     |     |     |     |     | mismatch? | To  | verify     | it, we | follow | the | prior |
| --- | --- | --- | --- | --- | --- | --------- | --- | ---------- | ------ | ------ | --- | ----- |
|     |     |     |     |     |     | work (Gu  | et  | al., 2023) | and    | use    | the | ExAc- |
cErr(Aroraetal.,2022)metric(lowerscorerefers
ourKID,andimportantly,2)ourrewritingapproach
|     |     |     |     |     |     | to less | training-inference |     | mismatch) |     | to measure |     |
| --- | --- | --- | --- | --- | --- | ------- | ------------------ | --- | --------- | --- | ---------- | --- |
couldfurtherimprovetheresultsbyalargemargin
|     |     |     |     |     |     | the training-inference |     |     | mismatch. | The | results | of  |
| --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --------- | --- | ------- | --- |
againstthesimplealternative,e.g.,+3.3%gainson
|     |     |     |     |     |     | QWen1.5-0.5B |     | (distilling | from | QWen1.5-7B) |     | on  |
| --- | --- | --- | --- | --- | --- | ------------ | --- | ----------- | ---- | ----------- | --- | --- |
CodeGen-350M,indicatingitseffectiveness.
|     |     |     |     |     |     | BIRD-dev(w/EK)arelistedinTable7. |     |     |     |     | Obviously, |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | ---------- | --- |
Analysisoftrainingefficiency. InTable3, we comparingtotheothermethods,ourKIDachieves
|     |     |     |     |     |     | lower ExAccErr |     | score, | and | there is | a significant |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | --- | -------- | ------------- | --- |
showthatourKIDeffectivelyreducesthetraining
|         |          |          |              |     |          | correlation | between | the | ExAccErr |     | score and | the |
| ------- | -------- | -------- | ------------ | --- | -------- | ----------- | ------- | --- | -------- | --- | --------- | --- |
| latency | compared | to those | counterparts |     | based on |             |         |     |          |     |           |     |
model-generateddata. Here, tofurtherverifythe distillation performance, i.e., a lower mismatch
training efficiency of KID, we present the perfor- leads to better performance. These results show
theeffectivenessofKID,andconfirmourstatement
manceofstudentstrainedwithvariousKDmethods
acrossdifferenttrainingsteps. QWen1.5-0.5Band thatalleviatingthetraining-inferencemismatchcan
1.8B models are used as student and teacher, re- enhancethedistillationoftext-to-SQLmodels.
| spectively.                                | The | results | are illustrated | in  | Figure 6. |               |     |     |     |     |     |     |
| ------------------------------------------ | --- | ------- | --------------- | --- | --------- | ------------- | --- | --- | --- | --- | --- | --- |
| Asseen,KIDcanachievecomparableorevenbetter |     |         |                 |     |           | 5 RelatedWork |     |     |     |     |     |     |
performancethanmostKDcounterpartswithmuch
|     |     |     |     |     |     | LLM-basedText-to-SQL. |     |     |     | Recently,autoregres- |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | -------------------- | --- | --- |
fewertrainingsteps,i.e.,effectivelyimprovingthe
|     |     |     |     |     |     | sive LLMs | (OpenAI, |     | 2023; | Ouyang | et al., | 2022; |
| --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ----- | ------ | ------- | ----- |
training efficiency. We attribute it to the higher Touvronetal.,2023;Aniletal.,2023;Zhaoetal.,
dataefficiency,sincetheimperfectdataiscloserto
|     |     |     |     |     |     | 2023) have | shown | their | superior | performance |     | by  |
| --- | --- | --- | --- | --- | --- | ---------- | ----- | ----- | -------- | ----------- | --- | --- |
inferencescenariosandcanhelpthestudentbetter
solvingvariousNLPtasksinagenerativemanner.
adapttodownstreamgeneration.
Inthefieldoftext-to-SQL,researchersareincreas-
inglyinterestedinleveragingthepowerfulcapabili-
4.4 Discussion
tiesofLLMstocreatetext-to-SQLsystems,which
Does KID still work under larger model size canbeclassifiedintotwogroups: 1)prompt-based
gaps? Here,tofurtherprovetheeffectivenessof text-to-SQLandtraining-basedtext-to-SQL.The
ourKID,weattempttoapplyittodistillthelarger formerinvolvesdesigningsomeeffectiveprompts
LLMs. In practice, we use our method to distill toinstructtheclosed-sourceLLMsforbettertext-
theQwen1.5-32BteachermodelintotheQwen1.5- to-SQL parsing (Pourreza and Rafiei, 2024; Sun
0.5Bstudentmodel,andreportthecontrastivere- etal.,2023a;Chenetal.,2024;Dongetal.,2023).
sultsonSpider-familybenchmarksinTable6. As Ontheotherhand,thetraining-basedmethodsaim
seen,comparedwiththeKDbaselines,KIDcanstill toimprovethetext-to-SQLperformanceofopen-
achievemuchbetterperformanceamongallbench- source LLMs by tuning them on the supervised
marks. Theseresultsindicatethatourmethodcan input-outputpairs(Sunetal.,2023a;Zhangetal.,
workwellinthelargerteachermodels. 2024a),orcontinuingpretrainingtheLLMsonthe

relateddatabase-relateddata(Roziereetal.,2023; performance across all model architectures, and
Lietal.,2024a). Whileachievingremarkableper- reducesthetraininglatencybyalargemargin.
formance,theabovemethodsusuallysufferfrom
Limitations
unbearableinferencelatency(Zhongetal.,2024;
Leviathanetal.,2023),hinderingtheapplications
|     |     |     |     | Our work | has several | potential | limitations. |     | First, |
| --- | --- | --- | --- | -------- | ----------- | --------- | ------------ | --- | ------ |
inreal-worldscenarios.
|           |              |                    |     | given the | limited computational |       | budget, | we     | only |
| --------- | ------------ | ------------------ | --- | --------- | --------------------- | ----- | ------- | ------ | ---- |
|           |              |                    |     | validate  | our KID on up         | to 7B | LLMs    | in the | main |
| Knowledge | Distillation | for Autoregressive |     |           |                       |       |         |        |      |
LLMs. KD, as a common approach for com- experiments. Itwillbemoreconvincingifscaling
uptosuper-largemodelsize,e.g.,70B.Secondly,
| pressing | LLMs, has attracted | great attention | re- |             |             |     |           |     |      |
| -------- | ------------------- | --------------- | --- | ----------- | ----------- | --- | --------- | --- | ---- |
|          |                     |                 |     | in our KID, | we leverage | an  | auxiliary | MLE | loss |
cently(Guetal.,2023;Agarwaletal.,2024;Zhong
etal.,2024;Raoetal.,2024;Xuetal.,2024). Inthe to ensure the stable training. In our preliminary
|     |     |     |     | experiments, | we found | that | the MLE | loss | plays |
| --- | --- | --- | --- | ------------ | -------- | ---- | ------- | ---- | ----- |
contextoftext-to-SQL,Sunetal.(2023b)isfirstto
animportroleinKID.However,thebettercombi-
applytheKDfordistillingthetext-to-SQLmodels,
nationofthedistillationlossandMLElossisstill
| but they     | mainly focus                   | on the encoder-only | (De- |                                        |     |     |     |     |         |
| ------------ | ------------------------------ | ------------------- | ---- | -------------------------------------- | --- | --- | --- | --- | ------- |
|              |                                |                     |      | under-explored,whichisinourfuturework. |     |     |     |     | Lastly, |
| vlin et al., | 2019) and sequence-to-sequence |                     | mod- |                                        |     |     |     |     |         |
besidesthedistillationfortext-to-SQL,webelieve
| els (Raffel | et al., 2020). | It is still under-explored |     |     |     |     |     |     |     |
| ----------- | -------------- | -------------------------- | --- | --- | --- | --- | --- | --- | --- |
thatourmethodhasthegreatpotentialtoexpand
whetherthesemethodsworkwellfordistillingau-
| toregressivetext-to-SQLLLMs. |     | Inthispaper,we |     | tomorescenarios. |     |     |     |     |     |
| ---------------------------- | --- | -------------- | --- | ---------------- | --- | --- | --- | --- | --- |
conductaseriesofpreliminaryexperimentstoex-
EthicsStatements
ploreitandrevealthattraining-inferencemismatch
isoneofthemainfactorshinderingtheKDperfor-
Wetakeethicalconsiderationsveryseriouslyand
manceinautoregressiveLLMs. Hence,wepropose strictlyadheretotheACLEthicsPolicy. Thispaper
an effective and efficient KD method to alleviate proposesanefficientknowledgedistillationalgo-
thetraining-inferencemismatch. Notably,ourmo- rithmfortext-to-SQLLLMs. Itaimstocompress
tivationissimilartotheschedulesampling(Ben- theexistinglargerLLMsintosmallerones,instead
gio et al., 2015), but there are significant differ- of encouraging them to learn privacy knowledge
encesbetweenthetwo. Wedepartfromtheprior thatmaycausetheethicalproblem. Moreover,all
| schedulesamplingandoursasfollows: |     | 1)Different |     |          |                |          |      |         |     |
| --------------------------------- | --- | ----------- | --- | -------- | -------------- | -------- | ---- | ------- | --- |
|                                   |     |             |     | training | and evaluation | datasets | used | in this | pa- |
approaches: schedule sampling focuses on RNN per are publicly available and have been widely
modelsinvolvingserialtraining,whereasourstar- adoptedbyresearchers. Thus,webelievethatthis
getsTransformermodelsrequiringparalleltraining. researchwillnotposeethicalissues.
| 2)Differentapplicationscenarios: |     | schedulesam- |     |     |     |     |     |     |     |
| -------------------------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Acknowledgements
plingwasappliedtosmallRNNmodeltraining,but
ourmethodisappliedinthedistillationscenarioof
|     |     |     |     | We are grateful | to the | anonymous | reviewers |     | and |
| --- | --- | --- | --- | --------------- | ------ | --------- | --------- | --- | --- |
LLMs,especiallyforthetext-to-SQL.
|     |     |     |     | the area     | chair for their | insightful | comments  |     | and     |
| --- | --- | --- | --- | ------------ | --------------- | ---------- | --------- | --- | ------- |
|     |     |     |     | suggestions. | This work       | was        | supported | in  | part by |
6 Conclusion
theNationalNaturalScienceFoundationofChina
Inthispaper,werevealandaddressthelimitations underGrant623B2076,U23B2048,62076186and
ofcurrentKDmethodsincompressingtheautore- 62225113, in part by the National Key Research
gressivetext-to-SQLLLMs. Basedonaseriesof andDevelopmentProgramofChinaunderGrant
preliminary analyses, we find that these methods 2023YFC2705700, in part by the Innovative Re-
fall short in balancing performance and training search Group Project of Hubei Province under
efficiency. Tothisend,weproposeanovelefficient Grant 2024AFA017, and in part by the National
KD algorithm (KID), which utilizes a simple-yet- ResearchFoundation,Singapore,andtheCyberSG
effectivestrategytosimulatetheinferencescenar- R&DProgrammeOffice(“CRPO”),undertheNa-
iosduringtraining,withonlyaone-passforward tionalCybersecurityR&DProgramme(“NCRP”),
process. Bydoingso,KIDcanmitigatethetraining- RIE2025NCRPFundingInitiative(AwardCRPO-
inference mismatch in an efficient manner, and GC1-NTU-002). The numerical calculations in
achieveabettertrade-offbetweenperformanceand thispaperhavebeendoneonthesupercomputing
efficiency. Experiments show that our approach system in the Supercomputing Center of Wuhan
| consistentlyandsignificantlyimprovesdistillation |     |     |     | University. |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |

References
|         |          |      |            |       |           | Edward J   | Hu, Phillip                         | Wallis, | Zeyuan  | Allen-Zhu,  |     |
| ------- | -------- | ---- | ---------- | ----- | --------- | ---------- | ----------------------------------- | ------- | ------- | ----------- | --- |
|         |          |      |            |       |           | YuanzhiLi, | SheanWang,                          |         | LuWang, | WeizhuChen, |     |
| Rishabh | Agarwal, | Nino | Vieillard, | Piotr | Stanczyk, |            |                                     |         |         |             |     |
|         |          |      |            |       |           | etal.2021. | Lora: Low-rankadaptationoflargelan- |         |         |             |     |
SabelaRamos,MatthieuGeist,andOlivierBachem.
|                                     |           |              |     |             |         | guagemodels. | InICLR. |     |     |     |     |
| ----------------------------------- | --------- | ------------ | --- | ----------- | ------- | ------------ | ------- | --- | --- | --- | --- |
| 2024.                               | On-policy | distillaiton |     | of language | models: |              |         |     |     |     |     |
| Learningfromself-generatedmistakes. |           |              |     |             | InICLR. |              |         |     |     |     |     |
GeorgeKatsogiannis-MeimarakisandGeorgiaKoutrika.
2023. Asurveyondeeplearningapproachesfortext-
RohanAnil,AndrewMDai,OrhanFirat,MelvinJohn-
to-sql. TheVLDBJournal.
| son, Dmitry |              | Lepikhin, | Alexandre   | Passos,       | Siamak        |                             |               |     |             |           |     |
| ----------- | ------------ | --------- | ----------- | ------------- | ------------- | --------------------------- | ------------- | --- | ----------- | --------- | --- |
| Shakeri,    | Emanuel      | Taropa,   |             | Paige Bailey, | Zhifeng       |                             |               |     |             |           |     |
|             |              |           |             |               |               | Yoon Kim                    | and Alexander | M   | Rush. 2016. | Sequence- |     |
| Chen,       | et al. 2023. | Palm      | 2 technical |               | report. arXiv |                             |               |     |             |           |     |
|             |              |           |             |               |               | levelknowledgedistillation. |               |     | InEMNLP.    |           |     |
preprint.
KushalArora,LaylaElAsri,HareeshBahuleyan,and Yaniv Leviathan, Matan Kalman, and Yossi Matias.
Jackie Chi Kit Cheung. 2022. Why exposure bias 2023. Fast inference from transformers via spec-
|                                   |                                       |     |     |              |     | ulativedecoding. | InICML. |     |     |     |     |
| --------------------------------- | ------------------------------------- | --- | --- | ------------ | --- | ---------------- | ------- | --- | --- | --- | --- |
| matters:                          | Animitationlearningperspectiveoferror |     |     |              |     |                  |         |     |     |     |     |
| accumulationinlanguagegeneration. |                                       |     |     | InFindingsof |     |                  |         |     |     |     |     |
HaoyangLi,JingZhang,CuipingLi,andHongChen.
ACL2022.
|     |     |     |     |     |     | 2023. | Resdsql: Decoupling |     | schema | linking | and |
| --- | --- | --- | --- | --- | --- | ----- | ------------------- | --- | ------ | ------- | --- |
JinzeBai,ShuaiBai,YunfeiChu,ZeyuCui,KaiDang, skeletonparsingfortext-to-sql. InAAAI.
XiaodongDeng,YangFan,WenbinGe,YuHan,Fei
Huang, et al. 2023. Qwen technical report. arXiv Haoyang Li, Jing Zhang, Hanbing Liu, Ju Fan, Xi-
| preprint. |     |     |     |     |     | aokangZhang,JunZhu,RenjieWei,HongyanPan, |     |     |        |     |         |
| --------- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | ------ | --- | ------- |
|           |     |     |     |     |     | CuipingLi,andHongChen.2024a.             |     |     | Codes: |     | Towards |
SamyBengio,OriolVinyals,NavdeepJaitly,andNoam buildingopen-sourcelanguagemodelsfortext-to-sql.
| Shazeer.2015. |     | Scheduledsamplingforsequencepre- |     |     |     |     |     |     |     |     |     |
| ------------- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ProceedingsoftheACMonManagementofData.
| dictionwithrecurrentneuralnetworks. |               |                             |                |     | InNeurIPS.    |                         |             |       |                    |      |         |
| ----------------------------------- | ------------- | --------------------------- | -------------- | --- | ------------- | ----------------------- | ----------- | ----- | ------------------ | ---- | ------- |
|                                     |               |                             |                |     |               | JinyangLi,              | BinyuanHui, | GeQu, | JiaxiYang,         |      | Binhua  |
| Xinyun                              | Chen, Maxwell |                             | Lin, Nathanael |     | Schaerli, and |                         |             |       |                    |      |         |
|                                     |               |                             |                |     |               | Li, Bowen               | Li, Bailin  | Wang, | Bowen              | Qin, | Ruiying |
| DennyZhou.2024.                     |               | Teachinglargelanguagemodels |                |     |               |                         |             |       |                    |      |         |
|                                     |               |                             |                |     |               | Geng,NanHuo,etal.2024b. |             |       | Canllmalreadyserve |      |         |
toself-debug. InICLR. asadatabaseinterface? abigbenchforlarge-scale
XiangDeng,AhmedHassan,ChristopherMeek,Olek- databasegroundedtext-to-sqls. InNeurIPS.
sandrPolozov,HuanSun,andMatthewRichardson.
AlexanderLin,JeremyWohlwend,HowardChen,and
2021. Structure-groundedpretrainingfortext-to-sql.
|     |     |     |     |     |     | TaoLei.2020. | Autoregressiveknowledgedistillation |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | ----------------------------------- | --- | --- | --- | --- |
InNAACL.
|               |     |          |        |        |          | throughimitationlearning. |     |     | InEMNLP. |     |     |
| ------------- | --- | -------- | ------ | ------ | -------- | ------------------------- | --- | --- | -------- | --- | --- |
| Jacob Devlin, |     | Ming-Wei | Chang, | Kenton | Lee, and |                           |     |     |          |     |     |
KristinaToutanova.2019. Bert: Pre-trainingofdeep XiaoxuanLiu, LanxiangHu, PeterBailis, Ion Stoica,
bidirectionaltransformersforlanguageunderstand- ZhijieDeng,AlvinCheung,andHaoZhang.2023.
| ing. InNAACL. |     |     |     |     |     | Onlinespeculativedecoding. |     |     | InICLR. |     |     |
| ------------- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------- | --- | --- |
XuemeiDong, ChaoZhang, YuhangGe, YurenMao, Andrey Malinin and Mark Gales. 2019. Reverse kl-
YunjunGao,JinshuLin,DongfangLou,etal.2023. divergencetrainingofpriornetworks: Improvedun-
NeurIPS.
C3: Zero-shot text-to-sql with chatgpt. arXiv certaintyandadversarialrobustness.
preprint.
ErikNijkamp,BoPang,HiroakiHayashi,LifuTu,Huan
Bent Fuglede and Flemming Topsoe. 2004. Jensen- Wang,YingboZhou,SilvioSavarese,andCaiming
shannondivergenceandhilbertspaceembedding. In Xiong. 2022. Codegen: An open large language
InternationalsymposiumonInformationtheory,2004. model for code with multi-turn program synthesis.
| ISIT2004.Proceedings. |        |             |         |             |           | InICLR.      |                       |     |                |     |     |
| --------------------- | ------ | ----------- | ------- | ----------- | --------- | ------------ | --------------------- | --- | -------------- | --- | --- |
| Yujian Gan,           | Xinyun | Chen,       | Qiuping | Huang,      | Matthew   |              |                       |     |                |     |     |
|                       |        |             |         |             |           | OpenAI.2023. | Gpt-4technicalreport. |     | Preprint,arXiv |     |     |
| Purver,               | John   | R Woodward, |         | Jinxia Xie, | and Peng- |              |                       |     |                |     |     |
preprint:2303.08774.
| shengHuang.2021a.                    |     |     | Towardsrobustnessoftext-to- |     |        |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --------------------------- | --- | ------ | --- | --- | --- | --- | --- | --- |
| sqlmodelsagainstsynonymsubstitution. |     |     |                             |     | InACL. |     |     |     |     |     |     |
LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,
CarrollWainwright,PamelaMishkin,ChongZhang,
YujianGan,XinyunChen,andMatthewPurver.2021b.
Exploringunderexploredlimitationsofcross-domain SandhiniAgarwal,KatarinaSlama,AlexRay,etal.
|                            |        |       |           |            |        | 2022. Training                  | languagemodelsto |     |            | followinstruc- |     |
| -------------------------- | ------ | ----- | --------- | ---------- | ------ | ------------------------------- | ---------------- | --- | ---------- | -------------- | --- |
| text-to-sqlgeneralization. |        |       | InEMNLP.  |            |        |                                 |                  |     |            |                |     |
|                            |        |       |           |            |        | tionswithhumanfeedback.         |                  |     | InNeurIPS. |                |     |
| Yuxian                     | Gu, Li | Dong, | Furu Wei, | and Minlie | Huang. |                                 |                  |     |            |                |     |
|                            |        |       |           |            |        | RichardYuanzhePangandHeHe.2020. |                  |     |            | Textgenera-    |     |
2023. Knowledgedistillationoflargelanguagemod-
|     |     |     |     |     |     | tionbylearningfromdemonstrations. |     |     |     | InICLR. |     |
| --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | ------- | --- |
els. arXivpreprint.
Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. 2015. Mohammadreza Pourreza and Davood Rafiei. 2024.
Distillingtheknowledgeinaneuralnetwork. arXiv Din-sql: Decomposed in-context learning of text-
| preprint. |     |     |     |     |     | to-sqlwithself-correction. |     |     | InNeurIPS. |     |     |
| --------- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ---------- | --- | --- |

ColinRaffel,NoamShazeer,AdamRoberts,Katherine Bin Zhang, Yuxiao Ye, Guoqing Du, Xiaoru Hu,
Lee,SharanNarang,MichaelMatena,YanqiZhou, Zhishuai Li, Sun Yang, Chi Harold Liu, Rui Zhao,
WeiLi,andPeterJLiu.2020. Exploringthelimits ZiyueLi,andHangyuMao.2024a. Benchmarking
oftransferlearningwithaunifiedtext-to-texttrans- thetext-to-sqlcapabilityoflargelanguagemodels:
| former. | JMLR. |     |     |     |     |     | Acomprehensiveevaluation. |     |     | arXivpreprint. |     |     |
| ------- | ----- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | -------------- | --- | --- |
JunRao,XueboLiu,ZepengLin,LiangDing,JingLi, Peiyuan Zhang, Guangtao Zeng, Tianduo Wang, and
andDachengTao.2024. Exploringandenhancing Wei Lu. 2024b. Tinyllama: An open-source small
thetransferofdistributioninknowledgedistillation languagemodel. arXivpreprint.
| forautoregressivelanguagemodels. |     |     |     | arXivpreprint. |     |     |       |           |           |       |     |              |
| -------------------------------- | --- | --- | --- | -------------- | --- | --- | ----- | --------- | --------- | ----- | --- | ------------ |
|                                  |     |     |     |                |     |     | Wayne | Xin Zhao, | Kun Zhou, | Junyi | Li, | Tianyi Tang, |
XiaoleiWang,YupengHou,YingqianMin,Beichen
BaptisteRoziere,JonasGehring,FabianGloeckle,Sten
|         |           |          |       |      |       |      | Zhang, | Junjie Zhang, |     | Zican Dong, | et  | al. 2023. A |
| ------- | --------- | -------- | ----- | ---- | ----- | ---- | ------ | ------------- | --- | ----------- | --- | ----------- |
| Sootla, | Itai Gat, | Xiaoqing | Ellen | Tan, | Yossi | Adi, |        |               |     |             |     |             |
Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023. surveyoflargelanguagemodels. arXivpreprint.
| Codellama:Openfoundationmodelsforcode. |     |     |     |     |     | arXiv |                                      |              |                               |       |      |            |
| -------------------------------------- | --- | --- | --- | --- | --- | ----- | ------------------------------------ | ------------ | ----------------------------- | ----- | ---- | ---------- |
| preprint.                              |     |     |     |     |     |       | Qihuang                              | Zhong, Liang | Ding,                         | Juhua | Liu, | Bo Du, and |
|                                        |     |     |     |     |     |       | DachengTao.2023.                     |              | Self-evolutionlearningfordis- |       |      |            |
|                                        |     |     |     |     |     |       | criminativelanguagemodelpretraining. |              |                               |       |      | InFindings |
RoySchwartz,JesseDodge,NoahASmith,andOren
ofACL.
| Etzioni. | 2020. | Green ai. | Communications |     |     | of the |     |     |     |     |     |     |
| -------- | ----- | --------- | -------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
ACM.
QihuangZhong,LiangDing,LiShen,JuhuaLiu,BoDu,
|            |        |         |        |          |        |     | andDachengTao.2024. |     |     | Revisitingknowledgedistil- |     |     |
| ---------- | ------ | ------- | ------ | -------- | ------ | --- | ------------------- | --- | --- | -------------------------- | --- | --- |
| Ruoxi Sun, | Sercan | O Arik, | Hootan | Nakhost, | Hanjun |     |                     |     |     |                            |     |     |
Dai, Rajarishi Sinha, Pengcheng Yin, and Tomas lationforautoregressivelanguagemodels. InACL.
| Pfister.2023a.                 |     | Sql-palm: | Improvedlargelanguage |                |     |     |                                                  |     |     |     |     |          |
| ------------------------------ | --- | --------- | --------------------- | -------------- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | -------- |
|                                |     |           |                       |                |     |     | RuiqiZhong,TaoYu,andDanKlein.2020.               |     |     |     |     | Semantic |
| modeladaptationfortext-to-sql. |     |           |                       | arXivpreprint. |     |     |                                                  |     |     |     |     |          |
|                                |     |           |                       |                |     |     | evaluationfortext-to-sqlwithdistilledtestsuites. |     |     |     |     | In       |
EMNLP.
ShuoSun,YuzeGao,YuchenZhang,JianSu,BinChen,
| YingzhanLin,andShuqiSun.2023b.         |     |     |     | Anexploratory |         |     |               |          |                                 |        |             |         |
| -------------------------------------- | --- | --- | --- | ------------- | ------- | --- | ------------- | -------- | ------------------------------- | ------ | ----------- | ------- |
|                                        |     |     |     |               |         |     | Victor Zhong, | Caiming  |                                 | Xiong, | and Richard | Socher. |
| studyonmodelcompressionfortext-to-sql. |     |     |     |               | InFind- |     |               |          |                                 |        |             |         |
|                                        |     |     |     |               |         |     | 2017.         | Seq2sql: | Generatingstructuredqueriesfrom |        |             |         |
ingsofACL.
|     |     |     |     |     |     |     | naturallanguageusingreinforcementlearning. |     |     |     |     | arXiv |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | ----- |
preprint.
| Hugo Touvron, | Louis      | Martin, | Kevin   | Stone,  | Peter   | Al- |     |     |     |     |     |     |
| ------------- | ---------- | ------- | ------- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| bert, Amjad   | Almahairi, |         | Yasmine | Babaei, | Nikolay |     |     |     |     |     |     |     |
XunyuZhu,JianLi,YongLiu,CanMa,andWeiping
Bashlykov,SoumyaBatra,PrajjwalBhargava,Shruti
|                                     |     |         |                |                   |             |     | Wang.                         | 2023. A | survey | on model       | compression | for |
| ----------------------------------- | --- | ------- | -------------- | ----------------- | ----------- | --- | ----------------------------- | ------- | ------ | -------------- | ----------- | --- |
| Bhosale,etal.2023.                  |     | Llama2: |                | Openfoundationand |             |     |                               |         |        |                |             |     |
|                                     |     |         |                |                   |             |     | largelanguagemodels.          |         |        | arXivpreprint. |             |     |
| fine-tunedchatmodels.               |     |         | arXivpreprint. |                   |             |     |                               |         |        |                |             |     |
|                                     |     |         |                |                   |             |     | A Appendix                    |         |        |                |             |     |
| TimVanErvenandPeterHarremos.2014.   |     |         |                |                   | Rényidiver- |     |                               |         |        |                |             |     |
| genceandkullback-leiblerdivergence. |     |         |                |                   | IEEETrans-  |     |                               |         |        |                |             |     |
|                                     |     |         |                |                   |             |     | A.1 DetailsofTasksandDatasets |         |        |                |             |     |
actionsonInformationTheory.
|                                 |     |                                  |     |                   |     |     | In this                         | work, we | conduct | extensive |     | experiments |
| ------------------------------- | --- | -------------------------------- | --- | ----------------- | --- | --- | ------------------------------- | -------- | ------- | --------- | --- | ----------- |
| SergioVerdú.2014.               |     | Totalvariationdistanceandthedis- |     |                   |     |     |                                 |          |         |           |     |             |
|                                 |     |                                  |     |                   |     |     | onseveraltext-to-SQLbenchmarks. |          |         |           |     | Here,wein-  |
| tributionofrelativeinformation. |     |                                  |     | In2014Information |     |     |                                 |          |         |           |     |             |
troducethedescriptionsofthesedatasetsindetail.
TheoryandApplicationsWorkshop(ITA).
Firstly,wepresentthestatisticsofalluseddatasets
YuqiaoWen,ZichaoLi,WenyuDu,andLiliMou.2023. inTable8. Then,eachtaskisdescribedas:
f-divergenceminimizationforsequence-levelknowl-
|                   |     |        |     |     |     |     | Spider. | Spider(Yuetal.,2018)isawidely-used |     |     |     |     |
| ----------------- | --- | ------ | --- | --- | --- | --- | ------- | ---------------------------------- | --- | --- | --- | --- |
| edgedistillation. |     | InACL. |     |     |     |     |         |                                    |     |     |     |     |
Englishtext-to-SQLbenchmark,comprising8,659
TaiqiangWu,ChaofanTao,JiahaoWang,ZheZhao,and trainingsamplesand1,034developmentsamples.
NgaiWong.2024. Rethinkingkullback-leiblerdiver- Thetrainingsetencompasses7,000manuallyanno-
| gence in | knowledge | distillation |     | for large | language |     |     |     |     |     |     |     |
| -------- | --------- | ------------ | --- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- |
tatedsamplesand1,659samplessourcedfromsix
| models. | arXivpreprint. |     |     |     |     |     |                                |     |     |     |             |     |
| ------- | -------------- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | ----------- | --- |
|         |                |     |     |     |     |     | previoustext-to-SQLbenchmarks. |     |     |     | Thereare200 |     |
Xiaohan Xu, Ming Li, Chongyang Tao, Tao Shen, databasescovering138diversedomainsinSpider.
ReynoldCheng,JinyangLi,CanXu,DachengTao,
|                     |     |     |                        |     |     |     | Due to | the submission |     | constraints | of  | the Spider |
| ------------------- | --- | --- | ---------------------- | --- | --- | --- | ------ | -------------- | --- | ----------- | --- | ---------- |
| andTianyiZhou.2024. |     |     | Asurveyonknowledgedis- |     |     |     |        |                |     |             |     |            |
leaderboard,wefollowLietal.(2024a)anddonot
| tillationoflargelanguagemodels. |     |     |     | arXivpreprint. |     |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
evaluateourmodelsonitstestset,butalternatively
Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, onthepubliclyavailabledevelopmentset.
DongxuWang,ZifanLi,JamesMa,IreneLi,Qingn-
|          |          |        |     |           |         |     | BIRD. | BIRD | (Li et | al., 2024b) | is  | a more chal- |
| -------- | -------- | ------ | --- | --------- | ------- | --- | ----- | ---- | ------ | ----------- | --- | ------------ |
| ing Yao, | Shanelle | Roman, | et  | al. 2018. | Spider: | A   |       |      |        |             |     |              |
lengingtext-to-SQLbenchmarkthatexaminesthe
large-scalehuman-labeleddatasetforcomplexand
|     |     |     |     |     |     |     | impact | of extensive | database | contents |     | on text-to- |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | -------- | -------- | --- | ----------- |
cross-domainsemanticparsingandtext-to-sqltask.
| InEMNLP. |     |     |     |     |     |     | SQLparsing. | BIRDcontainsover12,751unique |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | ----------- | ---------------------------- | --- | --- | --- | --- |

| Benchmark |     |     | #Training |     | #Development |     | INPUT |     |     |     |     |     |
| --------- | --- | --- | --------- | --- | ------------ | --- | ----- | --- | --- | --- | --- | --- |
Database prompt:
Spider 8,659 1,034 table movie , columns = [ movie.mid ( int | primary key | comment : movie id | values : 101 ,
102 ) , movie.title ( text | values : Gone with the Wind , Star Wars ) , movie.year ( int |
values : 1939 , 1977 ) , movie.director ( text | values : Victor Fleming , George Lucas ) ]
| BIRD |     |     | 9,428 |     |     | 1,534 |     |     |     |     |     |     |
| ---- | --- | --- | ----- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
table reviewer , columns = [ reviewer.rid ( int | primary key | comment : reviewer id | values :
Spider-DK - 535 201 , 202 ) , reviewer.name ( text | values : Sarah Martinez , Daniel Lewis ) ]
table rating , columns = [ rating.rid ( int | comment : reviewer id | values : 201 , 202 ) ,
Spider-Realistic - 508 rating.mid ( int | comment : movie id | values : 101 ,106 ) , rating.stars ( int | comment : rating
stars | values : 2 , 4 ) , rating.ratingdate ( date | values : 2011-01-22 , 2011-01-27 ) ]
| Spider-Syn |     |     | -   |     |     | 1,034 |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
foreign keys :
rating.rid = reviewer.rid
rating.mid = movie.mid
| Table8:Statisticofallusedtext-to-SQLbenchmarks. |     |     |     |     |     |     | matched values : |     |     |     |     |     |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- |
reviewer.name ( Sarah Martinez )
| Notably,“Spider-DK”,“Spider-Realistic”and“Spider- |     |     |     |     |     |     | Question: |     |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
What are the names of all directors whose movies have been reviewed by Sarah Martinez?
Syn”arevariantsofthedevelopmentofSpider.
OUTPUT
SELECT DISTINCT movie.director FROM rating JOIN movie ON rating.mid  =  movie.mid
JOIN reviewer ON rating.rid  =  reviewer.rid WHERE reviewer.name  =  'Sarah Martinez'
| Setting |     |     | QWen1.5 | CodeGen |     | LLaMA2 |     |     |     |     |     |     |
| ------- | --- | --- | ------- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- |
Figure7: Atext-to-SQLsampleinSpider’straining
| LearningRate |     |     | 2e-4 |     | 2e-4 | 2e-4 |     |     |     |     |     |     |
| ------------ | --- | --- | ---- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
set.WefollowLietal.(2024a)toconstructthedatabase
| Epoch |     |     | 8   |     | 8   | 4   |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
prompts. Notethatthisillustrationisfromtheoriginal
| BatchSize       |     |     | 16   |     | 16   | 16   |                       |     |     |     |     |     |
| --------------- | --- | --- | ---- | --- | ---- | ---- | --------------------- | --- | --- | --- | --- | --- |
| MaxInputLength  |     |     | 1024 |     | 1024 | 2048 | paper(Lietal.,2024a). |     |     |     |     |     |
| MaxOutputLength |     |     | 128  |     | 128  | 256  |                       |     |     |     |     |     |
| LoRA_Rank       |     |     | 64   |     | 8    | 64   |                       |     |     |     |     |     |
LoRA_Alpha 32 32 32 allmodelswithapopularparameter-efficientfine-
tuningmethod,i.e.,LoRA.Specifically,thealpha
Table 9: Details of training hyper-parameters for ofLoRAissetas32andtherankofLoRAissetas
| different | LLMs. | For | each | model, | we use | the same |     |     |     |     |     |     |
| --------- | ----- | --- | ---- | ------ | ------ | -------- | --- | --- | --- | --- | --- | --- |
64or8. Wepresentthetraininghyper-parameters
settingsamongallbenchmarks.
|     |     |     |     |     |     |     | in Table | 9. All | experiments | are | conducted | on 8 |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ----------- | --- | --------- | ---- |
NVIDIAH800(80GB)GPUs.
question-SQLpairsand95bigdatabaseswithato-
A.3 DetailsofdivergencefunctionsforKD
talsizeof33.4GB.Eachdatabasecontainsaround
Here,weintroducethecommonly-useddivergence
549Krowsonaverage.
functionsforKD.Lettheprobabilitydistribution
| Spider-DK. |     | Spider-DK |     | (Gan | et al., | 2021b) is |            |     |         |          |                   |     |
| ---------- | --- | --------- | --- | ---- | ------- | --------- | ---------- | --- | ------- | -------- | ----------------- | --- |
|            |     |           |     |      |         |           | of teacher | and | student | be p and | qθ, respectively. |     |
avariantderivedfromtheoriginalSpiderdataset.
ForthetrainingsetG,thedivergencefunctionscan
ItmodifiessomesamplesofSpiderbyaddingdo-
beformulatedas:
mainknowledgethatreflectsreal-worldquestion
paraphrases.
Kullback-Leibler(KL)divergence
| Spider-Realistic. |     |     | Spider-Realistic(Dengetal., |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
p(y|x)
| 2021)isalsoavariantofSpiderdataset. |     |     |     |     |     | Itmodifies |          |     | (cid:88) |           |         |       |
| ----------------------------------- | --- | --- | --- | --- | --- | ---------- | -------- | --- | -------- | --------- | ------- | ----- |
|                                     |     |     |     |     |     |            | F (p∥qθ) |     | =        | p(y|x)log |         | . (3) |
|                                     |     |     |     |     |     |            | KL       |     |          |           | qθ(y|x) |       |
theNLquestionsinthecomplexsubsetofSpiderto
(x,y)∈G
removeorparaphraseexplicitmentionsofcolumn
names,whilekeepingtheSQLqueriesunchanged. Note that the KL divergence is not symmetric,
Spider-Syn. Spider-Syn(Ganetal.,2021a)isa i.e.,F (p∥qθ) ̸= F (qθ∥p). Morespecifically,
|     |     |     |     |     |     |     | KL  |     | KL  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(p∥qθ)
human-curated dataset based on the Spider. NL the F KL refers to the forward KL, while
questions in Spider-Syn are modified from Spi- F (qθ∥p)referstothereverseKL.
KL
der,byreplacingtheirschema-relatedwordswith
Jensen–Shannon(JS)divergence
manuallyselectedsynonymsthatreflectreal-world
questionpara-phrases.
1
|     |     |     |     |     |     |     | F (p∥qθ) | =   | (F  | (p∥M)+F | (qθ∥M)), |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | ------- | -------- | --- |
|     |     |     |     |     |     |     | JS       |     | KL  |         | KL       |     |
2
| A.2 TrainingHyper-parameters. |      |       |      |         |      |           |        |            |     |     |     | (4) |
| ----------------------------- | ---- | ----- | ---- | ------- | ---- | --------- | ------ | ---------- | --- | --- | --- | --- |
|                               |      |       |      |         |      |           | whereM | = 1(p+qθ). |     |     |     |     |
| We train                      | each | model | with | a batch | size | of 16 and |        | 2          |     |     |     |     |
apeaklearningrateof2e-4. Thetrainingepochs Totalvariationdistance(TVD)
| areselectedfrom{4,8}fordifferentmodels. |     |     |     |     |     | We  |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
follow Li et al. (2024a) to construct the database (cid:88) p(y|x)−qθ(y|x)
|     |     |     |     |     |     |     | F   | (p∥qθ) | =   | |   |     | |. (5) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | ------ |
TVD
| prompt(anexampleofaninput-outputpairisillus- |           |               |     |            |         |          |     |     |         |     | 2   |     |
| -------------------------------------------- | --------- | ------------- | --- | ---------- | ------- | -------- | --- | --- | ------- | --- | --- | --- |
| tratedinFigure7)andsetthemaxlengthofinput    |           |               |     |            |         |          |     |     | (x,y)∈G |     |     |     |
| and output                                   | depending |               | on  | different  | models. | Due      |     |     |         |     |     |     |
| to the limited                               |           | computational |     | resources, |         | we train |     |     |         |     |     |     |