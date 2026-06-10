FedMKT: Federated Mutual Knowledge Transfer for Large and Small
|     |     |     |     |     | Language | Models |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- |
TaoFan1,2,GuoqiangMa2,YanKang2,HanlinGu2,YuanfengSong2,
LixinFan2,KaiChen1,QiangYang1,2
1 TheHongKongUniversityofScienceandTechnology,HongKong,China
2
WeBankCo.,Ltd,Shenzhen,China
Correspondence:tfanac@cse.ust.hk
|        |          | Abstract     |           |                |     | researchers  | and         | practitioners, |        | owing      | to      | their ex- |
| ------ | -------- | ------------ | --------- | -------------- | --- | ------------ | ----------- | -------------- | ------ | ---------- | ------- | --------- |
|        |          |              |           |                |     | ceptional    | performance |                | across | diverse    | text    | gener-    |
| Recent | research | in federated |           | large language |     |              |             |                |        |            |         |           |
|        |          |              |           |                |     | ation tasks. | Despite     |                | their  | widespread | success | in        |
| models | (LLMs)   | has          | primarily | focused        | on  |              |             |                |        |            |         |           |
4202 ceD 61  ]LC.sc[  4v42220.6042:viXra
variousgeneralNLPtasks,LLMsfacechallenges
| enabling | clients | to fine-tune |     | their locally | de- |             |       |          |     |                    |     |     |
| -------- | ------- | ------------ | --- | ------------- | --- | ----------- | ----- | -------- | --- | ------------------ | --- | --- |
|          |         |              |     |               |     | that hinder | their | adoption |     | in domain-specific |     | ap- |
ployedhomogeneousLLMscollaborativelyor
ontransferringknowledgefromserver-based plications (Kang et al., 2023; Fan et al., 2023,
LLMs to small language models (SLMs) at 2024b). The primary challenges include domain-
downstream clients. However, a significant specificknowledgePrivacy,constrainedcomputing
gap remains in the simultaneous mutual resources,andmutualknowledgetransferbetween
| enhancement   | of  | both                      | the server’s | LLM | and |                |     |     |                             |     |     |     |
| ------------- | --- | ------------------------- | ------------ | --- | --- | -------------- | --- | --- | --------------------------- | --- | --- | --- |
|               |     |                           |              |     |     | theLLMandSLMs. |     |     | Asignificantchallengearises |     |     |     |
| clients’SLMs. |     | Tobridgethisgap,wepropose |              |     |     |                |     |     |                             |     |     |     |
fromtheinherentmodelheterogeneitybetweenthe
| FedMKT, | a   | parameter-efficient |     | federated |     |     |     |     |     |     |     |     |
| ------- | --- | ------------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
LLMandSLMs,particularlywhenaligningdistri-
| mutual | knowledge | transfer |     | framework | for |     |     |     |     |     |     |     |
| ------ | --------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
large and small language models. This butions of output logits. The mismatch between
framework is designed to adaptively transfer thetokenizersofdifferentLLMandSLMsposes
knowledge from the server’s LLM to clients’ anotableobstacle. Furthermore,themutualtrans-
SLMswhileconcurrentlyenhancingtheLLM fer of knowledge between the server’s LLM and
| with clients’ | unique |     | domain | insights. | We  |          |      |         |     |                    |     |      |
| ------------- | ------ | --- | ------ | --------- | --- | -------- | ---- | ------- | --- | ------------------ | --- | ---- |
|               |        |     |        |           |     | clients’ | SLMs | remains | a   | largely unexplored |     | area |
facilitatetokenalignmentusingminimumedit
inacademicliterature,warrantingfurtherinvestiga-
| distance | (MinED) | and | then | selective | mutual |     |     |     |     |     |     |     |
| -------- | ------- | --- | ---- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
tion.
knowledgetransferbetweenclient-sideSLMs
Tofillthesegaps,weproposeFedMKT,anovel
andaserver-sideLLM,aimingtocollectively
enhancetheirperformance. Throughextensive federated mutual knowledge transfer framework
experiments across three distinct scenarios, designedtoimprovetheperformanceofbothlarge
we evaluate the effectiveness of FedMKT and small language models. By leveraging the
| by utilizing | diverse | public | LLMs | and | SLMs |     |     |     |     |     |     |     |
| ------------ | ------- | ------ | ---- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
complementarystrengthsoffederatedlearningand
on a variety of NLP text generation tasks. knowledgedistillation,FedMKTfacilitateseffec-
| Empirical      | results | demonstrate |     | that FedMKT |     |             |           |     |          |         |     |          |
| -------------- | ------- | ----------- | --- | ----------- | --- | ----------- | --------- | --- | -------- | ------- | --- | -------- |
|                |         |             |     |             |     | tive mutual | knowledge |     | transfer | between |     | clients’ |
| simultaneously |         | boosts      | the | performance |     |             |           |     |          |         |     |          |
SLMsandtheLLMownedbytheserver.
| of both | LLMs | and SLMs. |     | Our code | has |     |     |     |     |     |     |     |
| ------- | ---- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
been contributed to the FATE open-source AsillustratedinFigure1,FedMKTdeploysan
|         |        |     |          |            |     | LLMontheserverandasetofK |     |     |     |     | heterogeneous |     |
| ------- | ------ | --- | -------- | ---------- | --- | ------------------------ | --- | --- | --- | --- | ------------- | --- |
| project | and is | now | publicly | accessible | at  |                          |     |     |     |     |               |     |
https://github.com/FederatedAI/FATE-LLM/ SLMs across various clients. The cornerstone of
tree/main/python/fate_llm/algo/fedmkt
|     |     |     |     |     |     | FedMKT   | lies     | in its | selective | mutual     | knowledge    |     |
| --- | --- | --- | --- | --- | --- | -------- | -------- | ------ | --------- | ---------- | ------------ | --- |
|     |     |     |     |     |     | transfer | process. | During |           | each round | of federated |     |
1 Introduction
|     |     |     |     |     |     | learning, | the | clients | transmit | the output |     | logits of |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------- | -------- | ---------- | --- | --------- |
TheemergenceofLargeLanguageModels(LLMs) their updated SLMs on the public dataset to the
hasmarkedarevolutionaryshiftinartificialintelli- server. Subsequently,theserverselectivelyaggre-
gence,significantlytransformingourunderstand- gatesandextractstheknowledgeencodedwithin
ingofnaturallanguageprocessingcapabilities. The theseSLMsoutputlogitsintotheserver-sideLLM.
adventofcutting-edgeLLMslikeChatGPT (Ope- This process allows the server LLM to incorpo-
nAI, 2022), Gemma2 (Team et al., 2024), and ratethedomain-specificknowledgelearnedbythe
LLaMa2(Touvronetal.,2023)withtheirbillions clients, thereby enhancing its comprehensive ca-
ofparameters,hassparkedtheimaginationofboth pabilities. Simultaneously, the server-side LLM

2 RelatedWork
alsoselectivelydistillsitsknowledgetotheclients’
SLMs,whichissimilartotheknowledgetransfer
2.1 ModelHeterogeneousFederatedLearning
| fromclientstotheserver. |     |     | Byleveragingtheknowl- |     |     |     |     |     |     |     |     |
| ----------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
edgeoftheserverLLM,theclients’SLMsareable Modelheterogeneousfederatedlearning(MHFL)
toimprovetheirperformanceandgeneralizebetter aimstoaddressthechallengesassociatedwithhet-
tounseendata. Toaddressthemodelheterogeneity erogeneityinfederatedlearning(FL)(Yangetal.,
between the LLM and SLMs, FedMKT incorpo- 2019; McMahan et al., 2017; Liu et al., 2021;
|               |           |     |           |           |       | Cheng et | al., 2021; | Fan | et al., | 2024a). | Initial re- |
| ------------- | --------- | --- | --------- | --------- | ----- | -------- | ---------- | --- | ------- | ------- | ----------- |
| rates a token | alignment |     | technique | utilizing | mini- |          |            |     |         |         |             |
mum edit distance (MinED) prior to knowledge searchinMHFLprimarilyconcentratedonaddress-
transfer. Thisalignmentensuresseamlessintegra- ingheterogeneityinmodelarchitectures. Several
tionandefficientknowledgetransferbetweenLLM methods have been introduced to accommodate
| andSLMs. |     |     |     |     |     | clients with | different | model | architectures |     | partici- |
| -------- | --- | --- | --- | --- | --- | ------------ | --------- | ----- | ------------- | --- | -------- |
Ourcontributionsaresummarizedasfollows: patinginafederatedlearningtask. Thesemethods
typicallyinvolvetechniquessuchasknowledgedis-
| • Federated |     | Mutual | Knowledge |     | Transfer |     |     |     |     |     |     |
| ----------- | --- | ------ | --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
tillation(Hintonetal.,2015),mutuallearningand
| Framework. |     | FedMKT |     | introduces | a novel |     |     |     |     |     |     |
| ---------- | --- | ------ | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- |
splitlearningthatcanhandleheterogeneousmod-
| federated | mutual |     | knowledge | transfer | frame- |                |     |                    |     |      |       |
| --------- | ------ | --- | --------- | -------- | ------ | -------------- | --- | ------------------ | --- | ---- | ----- |
|           |        |     |           |          |        | els. Knowledge |     | distillation-based |     | MHFL | meth- |
workthatenableseffectiveknowledgetrans-
|     |     |     |     |     |     | ods, such | as FedMD | (Li | and | Wang, | 2019) and |
| --- | --- | --- | --- | --- | --- | --------- | -------- | --- | --- | ----- | --------- |
ferbetweenanLLMdeployedontheserver
|     |      |          |             |     |             | FedET (Cho | et al., | 2022), | involve | the | server ag- |
| --- | ---- | -------- | ----------- | --- | ----------- | ---------- | ------- | ------ | ------- | --- | ---------- |
| and | SLMs | residing | on clients. |     | This frame- |            |         |        |         |     |            |
gregatingtheoutputlogitsofdifferentclients’het-
workfillsthegapbysimultaneouslyenhanc-
erogeneousmodelsonapublicdatasettoconstruct
| ing both | the   | server’s | LLM         | and | the clients’ |               |                               |          |       |        |         |
| -------- | ----- | -------- | ----------- | --- | ------------ | ------------- | ----------------------------- | -------- | ----- | ------ | ------- |
|          |       |          |             |     |              | globallogits. | Mutuallearning-basedMHFL,such |          |       |        |         |
| SLMs.    | Our   | work     | is tailored | for | text gener-  |               |                               |          |       |        |         |
|          |       |          |             |     |              | as Deep       | Mutual                        | Learning | (DML) | (Zhang | et al., |
| ation    | tasks | within   | the context |     | of LLMs and  |               |                               |          |       |        |         |
2018),PFML(Yangetal.,2021)andFedLoRA(Yi
| supports | both | Heterogeneous |     |     | and Homoge- |     |     |     |     |     |     |
| -------- | ---- | ------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
etal.,2023),designasmallhomogeneousmodel
| neousscenariosbetweenclientSLMs. |     |     |     |     | Toour |             |               |     |       |     |              |
| -------------------------------- | --- | --- | --- | --- | ----- | ----------- | ------------- | --- | ----- | --- | ------------ |
|                                  |     |     |     |     |       | and a large | heterogeneous |     | model | in  | each client. |
bestknowledge,ourworkisthefirstpublished
|     |     |     |     |     |     | Split learning-based |     | MHFL | approaches, |     | such as |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | ---- | ----------- | --- | ------- |
researchinthisfield.
|     |     |     |     |     |     | FedClassAvg | (Jang | et  | al., 2022) | and | CHFL (Liu |
| --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | ---------- | --- | --------- |
etal.,2022),shareahomogeneousclassifiertoim-
| • Selective | Knowledge |     | Transfer |     | and Token |     |     |     |     |     |     |
| ----------- | --------- | --- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- |
Alignment. FedMKT implements a selec- provemodelclassificationwhilepersonalizingthe
| tive      | knowledge |     | transfer  | mechanism | that se- | localfeatureextractor. |     |     |     |     |     |
| --------- | --------- | --- | --------- | --------- | -------- | ---------------------- | --- | --- | --- | --- | --- |
| lectively | distills  |     | knowledge | from      | the most |                        |     |     |     |     |     |
2.2 FederatedLearningforLLMs
| informative |     | SLMs | to the | server’s | LLM and |     |     |     |     |     |     |
| ----------- | --- | ---- | ------ | -------- | ------- | --- | --- | --- | --- | --- | --- |
viceversa. Furthermore,itincorporatesato- Parameter-EfficientFine-Tuning(PEFT)methods
kenalignmenttechniqueusingminimumedit (Houlsbyetal.,2019;Heetal.,2021;Lesteretal.,
distance (MinED) to address model hetero- 2021; Li and Liang, 2021; Hu et al., 2021) offer
geneity between LLM and SLMs, ensuring a direct solution to the issues of communication
efficientknowledgetransfer. overheadandfine-tuningcostsinfederatedlearn-
|             |     |            |     |                 |     | ing(FL)forLLMs. |     | Anumberofstudieshavebuilt |     |     |     |
| ----------- | --- | ---------- | --- | --------------- | --- | --------------- | --- | ------------------------- | --- | --- | --- |
| • Empirical |     | Evaluation |     | and Performance |     |                 |     |                           |     |     |     |
uponPEFTmethodsinthecontextofFLforLLMs,
| Enhancement. |     |     | Extensive | experiments | con- |     |     |     |     |     |     |
| ------------ | --- | --- | --------- | ----------- | ---- | --- | --- | --- | --- | --- | --- |
includingFedPETuning(Zhangetal.,2022b),Fed-
| ducted | based | on  | various | publicly | available |     |     |     |     |     |     |
| ------ | ----- | --- | ------- | -------- | --------- | --- | --- | --- | --- | --- | --- |
eratedAdapterTuning(Caietal.,2022),Federated
LLMsandSLMs,haveshownthatFedMKT
PromptTuning(Zhaoetal.,2022),andFATE-LLM
| exhibits | competitive |     | performance |     | across a |                        |     |     |                       |     |     |
| -------- | ----------- | --- | ----------- | --- | -------- | ---------------------- | --- | --- | --------------------- | --- | --- |
|          |             |     |             |     |          | (Fanetal.,2023,2024c). |     |     | Thesefindingsindicate |     |     |
broadspectrumofNLPtext-generationtasks.
thatFLclients,especiallythosewithconstrained
| We evaluate |     | FedMKT | with | Heterogeneous, |     |     |     |     |     |     |     |
| ----------- | --- | ------ | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- |
computingandstorageresourcessuchascertainde-
| Homogeneous,andOne-to-Onesettings. |     |     |     |     | The |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
vices,cansignificantlyprofitfromfromPEFTap-
| results | show          | that | the performance |     | of SLMs       |           |                                       |     |     |     |     |
| ------- | ------------- | ---- | --------------- | --- | ------------- | --------- | ------------------------------------- | --- | --- | --- | --- |
|         |               |      |                 |     |               | proaches. | Thesetechniquesfacilitatethesharingof |     |     |     |     |
| can be  | significantly |      | enhanced        |     | with the help |           |                                       |     |     |     |     |
LLMsacrossdiversetasks,whilenecessitatingthe
oftheLLM,whiletheLLMcandelivercom-
storageandupdatingofonlyasmallnumberofpa-
parableresultstofine-tuningwithallclients’
rametersforeachtask,therebyreducingtheoverall
datacentralized.
|     |     |     |     |     |     | computationalandstoragerequirements. |     |     |     |     | Bylever- |
| --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | -------- |

Figure1: OverviewoftheproposedFedMKTworkflow. EachcommunicationroundofFedMKTinvolves11steps
tofine-tunetheserver’LLMandclients’SLMs.
aging PEFT methods, FL clients can efficiently vatedataD . Theobjectiveisformulatedas
k
| adaptLLMstotheirspecificneedswhileminimiz- |     |     |     |     |     |     | follows: |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
ingcommunicationoverheadandfine-tuningcosts.
}K
|     |     |     |     |     |     |     | min          | L   | 1 (ϕ 1 ,ϕ 2 | ,...,ϕ | K ;{D k | ) (1) |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----------- | ------ | ------- | ----- |
|     |     |     |     |     |     |     | ϕ1,ϕ2,...,ϕK |     |             |        |         | k=1   |
3 TheProposedFedMKTMethod
In this section, we introduce FedMKT, an inno- • EachclientcomputestheoutputlogitsonD
p
vative and parameter-efficient federated mutual andsecurelyuploadsthemtotheserver. Upon
knowledge transfer approach for large and small receivingoutputlogitsofallclients,theserver
| language | models. | The | FedMKT | primarily | com- |     |          |     |              |      |              |     |
| -------- | ------- | --- | ------ | --------- | ---- | --- | -------- | --- | ------------ | ---- | ------------ | --- |
|          |         |     |        |           |      |     | computes | the | distillation | loss | by comparing |     |
prisestwokeymodules: BidirectionalTokenAlign- theseclientlogitswiththeoutputlogitspro-
ment and Selective Mutual Knowledge Transfer. ducedbyitsownLLMonD . Theobjective
p
| We will | elaborate | on  | these two | key modules | in  |     |     |     |     |     |     |     |
| ------- | --------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
canbeformulatedasfollows:
Section3.2andSection3.3,respectivelyafterwe
definetheproblemwetrytoaddressinSection3.1. minL 2 (ψ;D p ,ϕ 1 ,ϕ 2 ,...,ϕ K ) (2)
ψ
3.1 ProblemDefinition
|     |     |     |     |     |     |     | The server | aims | to transfer |     | knowledge | from |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---- | ----------- | --- | --------- | ---- |
Weconsiderthefederatedlearningsetting,involv- theclients’SLMsg toitsownedLLMf .
|                            |     |     |     |               |     |     |     |     | ϕ   |     |     | ψ   |
| -------------------------- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| ingoneserverthatownsanLLMf |     |     |     | parameterized |     |     |     |     | k   |     |     |     |
ψ
byψ andK clientsthateachclientk hasanSLM • TheserverdispatchestheLLM’soutputlog-
|                          |     |     |                        |             |        |     | itsonD  | toalltheclients. |                  | Subsequently,the |      |         |
| ------------------------ | --- | --- | ---------------------- | ----------- | ------ | --- | ------- | ---------------- | ---------------- | ---------------- | ---- | ------- |
| g parameterizedbyϕ       |     |     | . Eachclientownsalocal |             |        |     |         | p                |                  |                  |      |         |
| ϕ k                      |     |     | k                      |             |        |     |         |                  |                  |                  |      |         |
|                          |     |     |                        |             |        |     | clients | compute          | the distillation |                  | loss | by com- |
| privatedatasetdenotedasD |     |     | k                      | containingN | train- |     |         |                  |                  |                  |      |         |
ingsamples,andallclientsandserverhaveaccess paringLLMoutputlogitswithSLMs’output
toasharedpublicdatasetD . logitsonD p . Theobjectivecanbeformulated
p
asfollows:
| The server                                   |                 | and clients | aim | to collaboratively |      |     |     |     |         |        |     |         |
| -------------------------------------------- | --------------- | ----------- | --- | ------------------ | ---- | --- | --- | --- | ------- | ------ | --- | ------- |
| enhance                                      | the performance |             | of  | the LLM and        | SLMs |     |     |     |         |        |     |         |
|                                              |                 |             |     |                    |      |     | min |     | L (ϕ ,ϕ | ,...,ϕ | ;D  | ,ψ) (3) |
| throughfederatedlearningwithoutdisclosingany |                 |             |     |                    |      |     |     |     | 3 1     | 2      | K p |         |
ϕ1,ϕ2,...,ϕK
| private data. | We   | assume          | that | the K clients | exe-     |     |             |     |             |     |           |      |
| ------------- | ---- | --------------- | ---- | ------------- | -------- | --- | ----------- | --- | ----------- | --- | --------- | ---- |
|               |      |                 |      |               |          |     | The clients | aim | to transfer |     | knowledge | from |
| cute the      | same | text generation |      | task, but     | they may |     |             |     |             |     |           |      |
holdheterogeneousorhomogeneousSLMmodels. LLMf toenhancetheirSLMs.
ψ
| The collaboration |     | between | clients | and the | server |     |          |     |        |              |     |         |
| ----------------- | --- | ------- | ------- | ------- | ------ | --- | -------- | --- | ------ | ------------ | --- | ------- |
|                   |     |         |         |         |        | We  | consider | the | server | semi-honest, |     | meaning |
involvesthefollowingsub-procedures:
thattheservermaytrytorecovertheprivatedata
• Eachclientk trainsitsSLMg usingitspri- ofclientsfromtheinformationitobserves.
|     |     |     |     | ϕ k |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

FedMKTsolvestheoptimizationproblemsfor- Algorithm2DualMinCE
mulatedinEq.(1),Eq.(2),andEq.(3)inanefficient Input:
and privacy-preservingmanner. We illustrate the 1: D p : thepublicdataset;
workflowofFedMKTinFigure1andAppendixA, 2: h: either the SLM g ϕ +θ of client k or the
k k
elaborate on the associated training algorithm in LLMf oftheserver;
ψ+ω
Algorithm1. 3: S k = {(l k i,pi k )}N i=1 ,k = 0or⌈K⌉: loss-logit
pairspassedfromeithertheserverorclients.
Algorithm1FedMKT Output: S.
4: S˜← {}▷initializeanemptysetofselective
Input:
knowledge.
1: K: numberofclients;
2: T: totalnumberofcommunicationrounds; 5: foreachxi inD p do
6: li ← h(xi)
3: R: localnumberofroundsintheserver; local
(cid:40)
4: E: localnumberofroundsintheclient; 7: k∗ = argm k in(l k i), ifk = ⌈K⌉
5: η ω : thelearningrateofLLMf ψ+ω ; 0, ifk = 0
6: η θ : thelearningrateofSLMg ϕ k +θ k . 8: S˜← S˜+(xi,pi ) if li < li
Output: f ,g ,g ,...,g . k∗ k∗ local
ψ+ω ϕ1+θ1 ϕ2+θ2 ϕK+θK 9: endfor
7: //Serverside:
8: fortincommunicationroundT do
9: {S k }K k=1 ← ClientUpdate1(t). 3.2 BidirectionalTokenAlignment
10: TokenAlignmentfromSLMstoLLM.
A significant challenge in aligning output logits
11: S˜ 0 ← DualMinCE(D p ,f ψ+ω ,{S k }K k=1 ). distributionsliesinthemismatchbetweentokeniz-
12: //knowledgetransferbasedonD p andS˜ 0 . ers of different LLM and SLMs, exemplified by
13: foreachepochr ∈ [R]do
Bloom and LLaMa. Consider the sentence, "we
14: ωt,r+1 ← ωt,r −η ω ▽L 2 . utilizethedynamicprogrammingapproachtoalign
15: endfor
tokens" as an example. Utilizing the Bloom tok-
16: ωt+1 = ωt,R.
enizerwouldsegmentitintothefollowingtokens:
17: ComputeS 0 = {l 0 i,pi 0 }N i=1 basedonD p . [’we’, ’utilize’, ’the,’ ’dynamic,’ ’programming,’
18: ClientUpdate2(t,S 0 ). ’approach,’ ’to,’ ’align,’ ’tokens’]. However, if
19: endfor
theLLaMatokenizerwereused,thesegmentation
20:
wouldbe: [’we’,’util’,’ize’,’the’,’dynamic’,’pro-
21: ClientUpdate1(t):
gramming’,’approach’,’to’,’align’,’tokens’].
22: foreachclientk (inparallel)do
Totacklethisissue,weadoptdynamicprogram-
23: //localfine-tuningbasedonD k . mingtechniquestopromoterobustalignment, as
24: foreachlocalepoche ∈ [E]do
evidenced in studies (Wan et al., 2024; Fu et al.,
25: θ k t,e+1 ← θ k t,e−η θ ▽ℓ TA . 2023). Utilizing LLaMa2 and Bloom as illustra-
26: endfor
tive examples, we establish an optimized vocab-
27: ComputeS k = {l k i,pi k }N i=1 basedonD p . ulary mapping table based on minimum edit dis-
28: endfor
tance(MinED). This mapping table identifies the
29: Upload{S k }K k=1 totheserver closestBloomtokenforeachLLaMa2token(e.g.,
30:
’utilize’for’util’). Wethentokenizeasentenceus-
31: ClientUpdate2(t,S 0 ): ingbothtokenizersandapplyadynamicprogram-
32: foreachclientk (inparallel)do
mingalgorithmtodeterminetheoptimalmatching
33: TokenAlignment fromLLMtoSLMs.
path. WhenmultipleLLaMa2tokensaligntoasin-
34: S˜ k ←DualMinCE(D p ,g ϕ k +θ k ,S 0 ). gleBloomtoken(e.g.,’util’and’ize’aligningto
35: //knowledgetransferbasedonD p andS˜ k . ’utilize’),wehandlethemaccordingtothemapping
36: foreachlocalepoche ∈ [E,2E]do
table. PleaseseeAppendixBforfurtherdetails.
37: θ k t,e+1 ← θ k t,e−η θ ▽L 3 . InFedMKT,abidirectionaltokenalignmentpro-
38: endfor
cess occurs before knowledge transfer between
39: θt+1 = θt,2E .
k k LLMsandSLMs. Onetheonehand,whenclients
40: endfor
transferknowledgefromtheirSLMstotheserver’s
LLM,theserveralignsSLMtokenstoLLMtokens.

Ontheotherhand,whentheservertransfersknowl- strategyonboththeserverandclientsides,termed
edge from its LLM back to clients’ SLMs, each DualMinCE.
clientalignsLLMtokenstoitsSLMtokens. DualMinCE aims to select knowledge that is
positive to the performance of the server’s LLM
3.3 SelectiveMutualKnowledgeTransfer
from clients and vice versa. Specifically, when
BetweenLLMandSLMs
knowledgeneedstobetransferredfromSLMsto
To transfer knowledge between the server and the LLM, each client k computes a knowledge
clientsefficiently,weleverageLoRAtofine-tune setS = {li,pi}N consistingofloss-logitpairs
k k k i=1
the server’s LLM and clients’ SLMs. Specifi- throughitslocalmodelbasedonthepublicdataset
cally,eachclientkinsertsasmalllow-rankadapter D . Then,allK clientssendtheir{S }K tothe
p k k=1
parameterized by θ into its local SLM. We de- server. ByleveragingDualMinCE(seeAlgorithm
k
note client k local SLM with the added θ as 2 for detail), the server picks a logit pi with the
k k∗
g . Likewise, the server inserts a small low- smallest loss from {li,pi}K and adds pi to a
ϕ k +θ k k k k=1 k∗
rankadapterparameterizedbyω intoitsLLMf . selectiveknowledgesetS˜ ifthelossli ofpi is
ψ 0 k∗ k∗
We denote the server’s LLM f with the added smaller than the loss li computed through the
ψ local
ω as f . During the whole federated learning server’slocalLLMbasedonxi foreachxi inD .
ψ+ω p
trainingprocess,θ ,k = 1,...,K andωaretrained, Next,theserverleveragestheknowledgedistil-
k
whileϕ ,k = 1,...,K andψ arefrozen. lationloss,denotedasLf ,tofine-tunef :
k KD ψ+ω
Beforetransferringknowledgetotheserver,each
clientktrainsitsLoRAadapterθ usingitsprivate
k
datasetD k . Consequently,Eq.(1)canbereformu- Lf KD (ω;S˜ 0 ) =E (x,p)∼S˜ 0 ℓ CE (f ψ+ω (x),p) (7)
latedasfollows:
Likewise, each client k leverages DualMinCE
L (θ ,θ ,...,θ ;{D }K ) to form its selective knowledge set S˜ from the
1 1 2 K k k=1 k
knowledgeS sentfromtheserver. Eachclientk
1 (cid:88) K (4) 0
= E ℓ (g (x),y) leveragesthefollowingknowledgedistillationloss
K (x,y)∼D k TA ϕ k +θ k
tofine-tuneitslocalmodelg :
k=1 ϕ k +θ k
w cl h ie e n r t e k ℓ . T T A h i e s o th ri e gi t n a a s l k m lo o s d s el fo p r ar t a ra m in e i t n er g ϕ θ k k o o f f c e li a e c n h t Lg KD (θ k ;S˜ k ) =E (x,p)∼S˜ k ℓ CE (g ϕ k +θ k (x),p) (8)
k’sSLMisfrozenduringtraining. Combining Eq.(5) and Eq.(7), we reformulate
Then,boththeserverandclientsfine-tunetheir the knowledge transfer from SLMs to LLM con-
LoRA adapters based on a shared public dataset ductedontheservertoenhanceLLMasfollows:
D . We formulate the losses of fine-tuning f
p ψ+ω
andg ϕ k +θ k (denotedasLf FT andLg FT )asfollows: L 2 = λLf FT +(1−λ)Lf KD (9)
Lf (ω;D ) = E ℓ (f (x),y) (5) Combining Eq.(6) and Eq.(8), we reformulate
FT p (x,y)∼Dp CE ψ+ω the knowledge transfer from LLM to SLMs con-
Lg (θ ;D ) = E ℓ (g (x),y) ductedontheclientstoenhanceSLMsasfollows:
FT k p (x,y)∼Dp CE ϕ k +θ k
(6) K
where ℓ represents the cross-entropy loss, and L = 1 (cid:88) (λLg +(1−λ)Lg ) (10)
CE 3 K FT KD
themodelparametersψ andϕ k arefrozenduring k=1
fine-tuning.
where λ is the hyperparameter that regulates the
Next, the server and clients conduct selective
significanceofmutualknowledgetransfer.
knowledgetransfertoeachother. Themotivation
for applying selective knowledge transfer is that 4 Experiments
someclients’knowledgemayadverselyaffectthe
4.1 Setup
performanceofLLMontheserverandviceversa
in a heterogeneous environment. Therefore, it is Wesetupafederatedlearningscenarioinvolving
criticaltoguaranteethattheknowledgeexchanged fourclientsandoneservertoevaluatetheFedMKT
between the server and clients is positive to the usingvariouspubliclyavailableLLMsandSLMs.
performanceofLLMandSLMs. Toachievethis Models. We evaluate FedMKT on one LLM
goal, we propose a selective knowledge transfer (LLaMa2-7B(Touvronetal.,2023))intheserver,

| Setting |     | Server |     | Client-1 |     | Client-2 | Client-3 | Client-4 |
| ------- | --- | ------ | --- | -------- | --- | -------- | -------- | -------- |
Heterogeneous LLaMa2-7B GPT-2-xlarge(1.5B) OPT-1.3B Bloom-1.1B LLaMa2-1.3B
Homogeneous LLaMa2-7B LLaMa2-1.3B LLaMa2-1.3B LLaMa2-1.3B LLaMa2-1.3B
| Homogeneous |     | LLaMa2-7B |                                                    | OPT-1.3B |     | OPT-1.3B | OPT-1.3B | OPT-1.3B    |
| ----------- | --- | --------- | -------------------------------------------------- | -------- | --- | -------- | -------- | ----------- |
| One-to-One  |     | LLaMa2-7B |                                                    |          | -   | -        | -        | LLaMa2-1.3B |
| One-to-One  |     | LLaMa2-7B |                                                    |          | -   | OPT-1.3B | -        | -           |
|             |     | Table1:   | ThefivedifferentsettingsweutilizetoevaluateFedMKT. |          |     |          |          |             |
Task Method GPT-2-xlarge OPT-1.3B Bloom-1.1B LLaMa2-1.3B LLaMa2-7B
|     | Centralized |     |      | -   | -    | -    | -    | 85.9 |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | Zero-Shot   |     | 52.4 |     | 52.7 | 52.7 | 49.8 | 63.2 |
RTE
|     | Standalone  |     | 65.7 |     | 62.5 | 58.1 | 55.6 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 70.4 |     | 65.7 | 61.7 | 58.8 | 82.3 |
|     | Centralized |     |      | -   | -    | -    | -    | 70.4 |
|     | Zero-Shot   |     | 49.8 |     | 50.8 | 50   | 50   | 50.3 |
WIC
|     | Standalone  |     | 59.3 |     | 52.2 | 59.1 | 50.6 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 63.2 |     | 62.2 | 61.1 | 51.9 | 61.3 |
|     | Centralized |     |      | -   | -    | -    | -    | 87.6 |
|     | Zero-Shot   |     | 61.3 |     | 58.4 | 59.0 | 61.0 | 70.1 |
BoolQ
|     | Standalone  |     | 71.1 |     | 74.1 | 69.7 | 69.9 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 75.1 |     | 76.8 | 71.4 | 75.1 | 85.0 |
|     | Centralized |     |      | -   | -    | -    | -    | 69.5 |
|     | Zero-Shot   |     | 36.7 |     | 41.9 | 33.8 | 30.1 | 39.5 |
CQA
|     | Standalone  |     | 56.0 |     | 58.6 | 44.7 | 56.7 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 58.3 |     | 60.5 | 50.8 | 57.0 | 71.8 |
|     | Centralized |     |      | -   | -    | -    | -    | 76.9 |
|     | Zero-Shot   |     | 58.3 |     | 57.0 | 51.5 | 53.1 | 69.3 |
ARC-E
|     | Standalone  |     | 59.3 |     | 57.9 | 56.9 | 60.4 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 59.8 |     | 59.6 | 57.5 | 60.8 | 76.1 |
|     | Centralized |     |      | -   | -    | -    | -    | 48.9 |
|     | Zero-Shot   |     | 25.0 |     | 23.4 | 23.6 | 26.7 | 40.0 |
ARC-C
|     | Standalone  |     | 28.2 |     | 28.4 | 24.9 | 28.5 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 30.2 |     | 29.4 | 26.6 | 30.0 | 44.7 |
|     | Centralized |     |      | -   | -    | -    | -    | 49.3 |
|     | Zero-Shot   |     | 5.0  |     | 5.2  | 5.1  | 5.8  | 12.0 |
S-NI
|     | Standalone  |     | 27.9 |     | 26.1 | 10.6 | 33.4 | -    |
| --- | ----------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT      |     | 34.2 |     | 36.0 | 15.1 | 37.3 | 41.4 |
|     | Centralized |     |      | -   | -    | -    | -    | 27.7 |
|     | Zero-Shot   |     | 5.4  |     | 6.4  | 4.9  | 5.7  | 8.5  |
DialogSum
|     | Standalone |     | 22.3 |     | 19.8 | 13.2 | 21.4 | -    |
| --- | ---------- | --- | ---- | --- | ---- | ---- | ---- | ---- |
|     | FedMKT     |     | 23.2 |     | 20.9 | 14.9 | 21.6 | 24.2 |
Table2: MethodPerformanceComparisonintheHeterogeneoussetting. WeevaluateFedMKTwith8different
tasks. Inallthe8tasks,theserverisdeployedwithaLLaMa2-7Bmodel,andthe4clientsaredeployedwitha
GPT-2-xlarge,aOPT-1.3B,aBloom-1.1B,andaLLaMa2-1.3B,respectively. The’-’indicatesamethoddoesnot
applytothecorrespondingparticipant(eithertheserverortheclient).
four SLMs in the clients including GPT-2-xlarge LLaMa2-1.3B (Xia et al., 2023). In our exper-
(1.5B) (Radford et al., 2019), OPT-1.3B (Zhang iments, we evaluate our framework in three dis-
etal.,2022a),Bloom-1.1B(Scaoetal.,2022)and tinct scenarios: Heterogeneous, Homogeneous

andOne-to-One. Table1detailsthesetupforthe ployedwithaGPT-2-xlarge,aOPT-1.3B,aBloom-
LLMandSLMsindifferentsettings. 1.1B, and a LLaMa2-1.3B, respectively. Table 2
Datasets. We evaluate FedMKT on 6 QA reportstheperformancecomparisonsofFedMKT
datasets and 2 instruction-following datasets. againstbaselineson8tasks.
Specifically,forQAtasks,weuseRTE(Wangetal., Tables 2 show that FedMKT performs supe-
2019), WTC (Wang et al., 2019), BoolQ (Clark rioroverZero-ShotandStandaloneonallclients’
et al., 2019), CQA (Talmor et al., 2018), ARC- SLMs. Take the RTE dataset as an example,
E and ARC-C (Clark et al., 2018) to evaluate FedMKToutperformsZero-Shotby34%andStan-
FedMKT. As for instruction-following tasks, we dalone by 7% in relative terms on the GPT-2-
evaluate FedMKT on S-NI (Wang et al., 2022), xlargeSLM;FedMKTsurpassesZero-Shotby25%
DialogSum(Chenetal.,2021). and Standalone by 5% on the OPT-1.3B SLM;
Baselines. Weconductacomparativeanalysis FedMKT-SLMachievesa17%improvementover
ofFedMKTagainstthefollowingbaselines: Zero-Shotanda6%improvementoverStandalone
|     |     |     |     |     | on the | Bloom-1.1B | SLM; | FedMKT-SLM |     | outper- |
| --- | --- | --- | --- | --- | ------ | ---------- | ---- | ---------- | --- | ------- |
• Centralized,inwhichtheserver’sLLMisfine-
formsZero-Shotby18%andStandaloneby6%on
tunedlocallyusingthedatasetscombiningpri-
|     |     |     |     |     | the LLaMa2-1.3B |     | SLM. | These | empirical | results |
| --- | --- | --- | --- | --- | --------------- | --- | ---- | ----- | --------- | ------- |
vatedatasetsofinvolvedclientsandthepublic
|          |                   |          |     |          | demonstrate |     | that, by leveraging |     | FedMKT, | SLMs |
| -------- | ----------------- | -------- | --- | -------- | ----------- | --- | ------------------- | --- | ------- | ---- |
| dataset. | In the One-to-One | setting, |     | the data |             |     |                     |     |         |      |
areabletoeffectivelyleveragetheknowledgetrans-
of one client and the public data are used to ferredfromtheLLM,leadingtoenhancedmodel
fine-tunetheserver’sLLM,whereasinother
capabilities.
| settings, | the data of | all four clients |     | and the |       |        |       |             |     |             |
| --------- | ----------- | ---------------- | --- | ------- | ----- | ------ | ----- | ----------- | --- | ----------- |
|           |             |                  |     |         | Table | 2 also | shows | that FedMKT |     | outperforms |
publicdataareutilizedtofine-tunetheLLM;
|     |     |     |     |     | Zero-Shot | and     | Centralized   |     | on the | LLaMa2-7B |
| --- | --- | --- | --- | --- | --------- | ------- | ------------- | --- | ------ | --------- |
|     |     |     |     |     | of the    | server. | For instance, |     | on the | RTE QA    |
• Zero-Shot,representingthezero-shotcapabil-
dataset,FedMKToutperformsZero-Shotby30%
itiesofLLMorSLMs(withoutfine-tuning);
|     |     |     |     |     | and achieves |     | a performance |     | level that | is nearly |
| --- | --- | --- | --- | --- | ------------ | --- | ------------- | --- | ---------- | --------- |
• Standalone, where each client fine-tunes its on par with Centralized, reaching approximately
own SLM independently using its private 96% of its fine-tuning performance. This signifi-
| dataset; |     |     |     |     | cantachievementsignifiesthatFedMKTeffectively |     |             |     |           |          |
| -------- | --- | --- | --- | --- | --------------------------------------------- | --- | ----------- | --- | --------- | -------- |
|          |     |     |     |     | facilitates                                   | the | acquisition | of  | knowledge | from all |
• FedAvg(McMahanetal.,2017),representing
clientsbytheserver.
| the standard | federated | averaging | algorithm. |     |     |     |     |     |     |     |
| ------------ | --------- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
FedAvgisonlyusedinhomogeneoussettings 4.3 EvaluationonHomogeneousSetting
becauseitrequiresallclients’modelshavethe WeconductexperimentswithtwoHomogeneous
samearchitecture.
|     |     |     |     |     | settings, | as shown | in  | Table | 1. The | first setting |
| --- | --- | --- | --- | --- | --------- | -------- | --- | ----- | ------ | ------------- |
(denotedasS1)involvesoneserver-sideLLaMa2-
• LLM2SLM,representingFedMKTinvolving
7Bandfourclient-sideLLaMa2-1.3B.Thesecond
oneserverwithanLLMandoneclientwith
|     |     |     |     |     | setting | (denoted | as S2) | involves | one | server-side |
| --- | --- | --- | --- | --- | ------- | -------- | ------ | -------- | --- | ----------- |
anSLM.TheLLMisnotupdatedandisused
LLaMa2-7Bandfourclient-sideOPT-1.3B.
totransferknowledgetoSLM.LLM2SLMis
|     |     |     |     |     | Table | 3 reports | the | performance |     | comparisons |
| --- | --- | --- | --- | --- | ----- | --------- | --- | ----------- | --- | ----------- |
onlyusedintheOne-to-Onesetting.
ofFedMKTagainstbaselinesinthetwoHomoge-
Evaluation Metrics. For the QA datasets, we neoussettings. Thetopsub-tableandthebottom
primarily use Accuracy as the metric for evalua- sub-table compare the performance of FedMKT
againstbaselinesontheserver’sLLMandclients’
tion,whereasfortheinstruction-followingdatasets,
| we primarily | rely on Rouge-L. | It’s | worth | noting | SLMs,respectively. |     |     |     |     |     |
| ------------ | ---------------- | ---- | ----- | ------ | ------------------ | --- | --- | --- | --- | --- |
that in our experiments, all methods across the Thetopsub-tableofTable3showsthatFedMKT
threescenariosundergozero-shotevaluation,and significantlyoutperformsZero-Shotontheserver’s
weutilizethelm-evaluation-harnesspackage(Gao LLM(i.e.,LLaMa2-7B)inthetwoHomogeneous
etal.,2023)forevaluationpurposes. settings. ItalsoshowsthatFedMKTachievescom-
|     |     |     |     |     | parable | performance | of  | the | Centralized | scenario, |
| --- | --- | --- | --- | --- | ------- | ----------- | --- | --- | ----------- | --------- |
4.2 EvaluationonHeterogeneousSetting in which the server’ LLM is fine-tuned using all
IntheHeterogeneoussetting,theserverisdeployed clients’dataandthepublicdatacombined.
withaLLaMa2-7Bmodel,andthe4clientsarede- The bottom sub-table of Table 3 shows that

FedMTKperformsbetterthantheZero-Shot,Stan- S1: Server S2: Server
|     |     |     |     |     |     |     | Task | Method |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | --- |
dalone, and FedAvg due to the assistance of the LLaMa2-7B LLaMa2-7B
server’s LLM. For example, in the CQA dataset, Zero-Shot 39.5 39.5
FedMKT outperforms FedAvg by 4% in relative CQA Centralized 69.0 68.3
termsontheLLaMa2-1.3SLMandby5%onthe
|     |     |     |     |     |     |     |     | FedMKT |     | 69.0 |     | 71.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | ---- | --- | ---- |
OPT-1.3BSLM,respectively.
|       |             |        |           |        |           |        |       | Zero-Shot   |     | 40.0        |     | 40.0        |
| ----- | ----------- | ------ | --------- | ------ | --------- | ------ | ----- | ----------- | --- | ----------- | --- | ----------- |
|       |             |        |           |        |           |        | ARC-C | Centralized |     | 45.9        |     | 48.6        |
|       |             |        | S1:       | Server | S2:       | Server |       | FedMKT      |     | 45.9        |     | 45.8        |
| Task  |             | Method |           |        |           |        |       |             |     |             |     |             |
|       |             |        | LLaMa2-7B |        | LLaMa2-7B |        |       |             |     |             |     |             |
|       |             |        |           |        |           |        |       | Zero-Shot   |     | 69.3        |     | 69.3        |
|       | Zero-Shot   |        |           | 39.5   | 39.5      |        |       |             |     |             |     |             |
|       |             |        |           |        |           |        | ARC-E | Centralized |     | 74.4        |     | 73.6        |
| CQA   | Centralized |        |           | 69.5   | 69.5      |        |       | FedMKT      |     | 74.8        |     | 74.8        |
|       | FedMKT      |        |           | 68.8   | 71.3      |        |       |             |     | S1: Clients |     | S2: Clients |
|       | Zero-Shot   |        |           | 40.0   | 40.0      |        | Task  | Method      |     |             |     |             |
|       |             |        |           |        |           |        |       |             |     | LLaMa2-1.3B |     | OPT-1.3B    |
| ARC-C | Centralized |        |           | 49.4   | 49.4      |        |       |             |     |             |     |             |
|       |             |        |           |        |           |        |       | Zero-Shot   |     | 30.1        |     | 41.9        |
|       | FedMKT      |        |           | 46.2   | 46.2      |        |       |             |     |             |     |             |
|       |             |        |           |        |           |        |       | Standalone  |     | 56.7        |     | 58.6        |
CQA
|       | Zero-Shot   |        |             | 69.3    | 69.3     |         |       | LLM2SLM    |     | 56.76 |     | 59.1 |
| ----- | ----------- | ------ | ----------- | ------- | -------- | ------- | ----- | ---------- | --- | ----- | --- | ---- |
| ARC-E | Centralized |        |             | 75.5    | 75.5     |         |       |            |     |       |     |      |
|       |             |        |             |         |          |         |       | FedMKT     |     | 56.84 |     | 60.7 |
|       | FedMKT      |        |             | 74.9    | 74.8     |         |       |            |     |       |     |      |
|       |             |        |             |         |          |         |       | Zero-Shot  |     | 26.7  |     | 23.4 |
|       |             |        | S1:         | Clients | S2:      | Clients |       | Standalone |     | 30.3  |     | 28.8 |
| Task  |             | Method |             |         |          |         |       |            |     |       |     |      |
|       |             |        | LLaMa2-1.3B |         | OPT-1.3B |         | ARC-C |            |     |       |     |      |
|       |             |        |             |         |          |         |       | LLM2SLM    |     | 30.1  |     | 29.6 |
|       | Zero-Shot   |        |             | 30.1    | 41.9     |         |       | FedMKT     |     | 30.8  |     | 30.4 |
|       | Standalone  |        |             | 56.4    | 58.1     |         |       |            |     |       |     |      |
|       |             |        |             |         |          |         |       | Zero-Shot  |     | 53.1  |     | 57.0 |
CQA
|     |     | FedAvg |     | 56.4 | 58.6 |     |     | Standalone |     | 57.0 |     | 57.9 |
| --- | --- | ------ | --- | ---- | ---- | --- | --- | ---------- | --- | ---- | --- | ---- |
ARC-E
|     | FedMKT     |     |     | 58.6 | 61.5 |     |     | LLM2SLM |     | 60.7 |     | 58.4 |
| --- | ---------- | --- | --- | ---- | ---- | --- | --- | ------- | --- | ---- | --- | ---- |
|     | Zero-Shot  |     |     | 26.7 | 23.4 |     |     |         |     |      |     |      |
|     |            |     |     |      |      |     |     | FedMKT  |     | 60.8 |     | 58.5 |
|     | Standalone |     |     | 30.4 | 28.5 |     |     |         |     |      |     |      |
ARC-C
FedAvg 29.7 28.6 Table4: MethodPerformanceComparisoninOne-to-
|     |        |     |     |      |      |     | Onesettings. | WeevaluateFedMKTusingtwoone-to- |     |     |     |     |
| --- | ------ | --- | --- | ---- | ---- | --- | ------------ | ------------------------------- | --- | --- | --- | --- |
|     | FedMKT |     |     | 31.7 | 29.9 |     |              |                                 |     |     |     |     |
Zero-Shot 53.1 57.0 onesettings. Thefirstsetting(denotedasS1)involves
oneserver-sideLLaMa2-7BLLMandoneclient-side
|     | Standalone |     |     | 60.3 | 57.9 |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
ARC-E
LLaMa2-1.3BSLM,whilethesecondsetting(denoted
|     |     | FedAvg |     | 60.6 | 58.8 |     |     |     |     |     |     |     |
| --- | --- | ------ | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
asS2)involvesoneserver-sideLLaMa2-7BLLMand
|     | FedMKT |     |     | 61.7 | 60.1 |     |     |     |     |     |     |     |
| --- | ------ | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
oneclient-sideOPT-1.3BSLM.Thetopandbottomsub-
|     |     |     |     |     |     |     | tables | compare | the performance |     | of FedMKT | against |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------- | --------------- | --- | --------- | ------- |
Table3: MethodPerformanceComparisoninHomo- baselinesontheserver’sLLMandaclient’sSLM,re-
| geneous              | settings. |             | We evaluate                  | FedMKT | using | two      | spectively. |     |     |     |     |     |
| -------------------- | --------- | ----------- | ---------------------------- | ------ | ----- | -------- | ----------- | --- | --- | --- | --- | --- |
| homogeneoussettings. |           |             | Thefirstsetting(denotedasS1) |        |       |          |             |     |     |     |     |     |
| involves             | one       | server-side | LLaMa2-7B                    |        | LLM   | and four |             |     |     |     |     |     |
client-sideLLaMa2-1.3BSLMs,whilethesecondset-
Table4reportstheperformancecomparisonsof
ting(denotedasS2)involvesoneserver-sideLLaMa2-
7B LLM and four client-side OPT-1.3B SLMs. The FedMKTagainstbaselinesinthetwoOne-to-One
| top and | bottom | sub-tables | compare |     | the performance |     |           |                                  |     |     |     |     |
| ------- | ------ | ---------- | ------- | --- | --------------- | --- | --------- | -------------------------------- | --- | --- | --- | --- |
|         |        |            |         |     |                 |     | settings. | Thetopandbottomsub-tablescompare |     |     |     |     |
ofFedMKTagainstbaselinesontheserver’sLLMand
theperformanceofFedMKTagainstbaselineson
| clients’SLMs,respectively. |     |     | Theresultsreportedinthe |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theserver’sLLMandclients’SLMs,respectively.
bottomsub-tablearetheaverageofallclients.
Thetopsub-tableofTable4showsthatFedMKT
|     |     |     |     |     |     |     | notably | surpasses | Zero-Shot | and | rivals | Central- |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --------- | --- | ------ | -------- |
4.4 EvaluationonOne-to-OneSetting
izedontheperformanceoftheserver’sLLM.The
We evaluate FedMKT using two One-to-One set- bottom sub-table of Table 4 shows that FedMTK
tings. Thefirstsetting(denotedasS1)involvesone achieves superior SLM performance over Zero-
server-sideLLaMa2-7BLLMandoneclient-side Shot, Standalone, and LLM2SLM due to the as-
LLaMa2-1.3BSLM,whilethesecondsetting(de- sistanceofLLM.Theseempiricalresultsdemon-
notedasS2)involvesoneserver-sideLLaMa2-7B stratetheeffectivenessofFedMKTintransferring
LLMandoneclient-sideOPT-1.3BSLM. knowledgebetweentheLLMandSLMs.

5 Conclusions
|                     |        |           |           |        |           |     | geneous           | ensemble | knowledge    |           | transfer | for training |     |
| ------------------- | ------ | --------- | --------- | ------ | --------- | --- | ----------------- | -------- | ------------ | --------- | -------- | ------------ | --- |
|                     |        |           |           |        |           |     | large             | models   | in federated | learning. | arXiv    | preprint     |     |
| In this             | study, | we have   | presented |        | FedMKT,   | a   | arXiv:2204.12703. |          |              |           |          |              |     |
| parameter-efficient |        | federated |           | mutual | knowledge |     |                   |          |              |           |          |              |     |
|                     |        |           |           |        |           |     | Christopher       | Clark,   | Kenton       | Lee,      | Ming-Wei | Chang,       |     |
transferframeworktailoredforLLMsandSLMs.
|     |     |     |     |     |     |     | Tom Kwiatkowski, |     | Michael |     | Collins, | and Kristina |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------- | --- | -------- | ------------ | --- |
FedMKTbridgesthegapbetweentheserver-side
|     |     |     |     |     |     |     | Toutanova. | 2019. | Boolq: | Exploring | the | surprising |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | ------ | --------- | --- | ---------- | --- |
LLMs and clients’ SLMs, enabling selective mu- difficultyofnaturalyes/noquestions. arXivpreprint
| tual knowledge |         | transfer  | while |             | preserving | data   | arXiv:1905.10044. |     |     |     |     |     |     |
| -------------- | ------- | --------- | ----- | ----------- | ---------- | ------ | ----------------- | --- | --- | --- | --- | --- | --- |
| privacy.       | Through | extensive |       | experiments |            | across |                   |     |     |     |     |     |     |
PeterClark,IsaacCowhey,OrenEtzioni,TusharKhot,
threedistinctscenarios,wehavedemonstratedthat AshishSabharwal,CarissaSchoenick,andOyvind
FedMKTsimultaneouslybooststheperformance Tafjord.2018. Thinkyouhavesolvedquestionan-
|     |     |     |     |     |     |     | swering? | tryarc,theai2reasoningchallenge. |     |     |     |     | arXiv |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------------------------- | --- | --- | --- | --- | ----- |
ofbothLLMsandSLMs.
preprintarXiv:1803.05457.
Limitations
TaoFan,WeijingChen,GuoqiangMa,YanKang,Lixin
|     |     |     |     |     |     |     | Fan,andQiangYang.2024a. |     |     |     | Secureboost+: |     | Large |
| --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | ------------- | --- | ----- |
Inthisstudy,wetransferknowledgebetweenthe
|     |     |     |     |     |     |     | scale | and high-performance |     |     | vertical federated |     | gra- |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------------------- | --- | --- | ------------------ | --- | ---- |
serverandclientsusinglogitsofapublicdataset, dient boosting decision tree. In Pacific-Asia Con-
motivatedbyefficiencyandprivacyconsiderations. ferenceonKnowledgeDiscoveryandDataMining,
Although empirical evidence suggests that shar- pages237–249.Springer.
| ing logits | of public |     | datasets | between |     | the server |     |     |     |     |     |     |     |
| ---------- | --------- | --- | -------- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
TaoFan,YanKang,WeijingChen,HanlinGu,Yuanfeng
andclientsismoreprivacy-preservingthansharing
Song,LixinFan,KaiChen,andQiangYang.2024b.
modelgradientsorparameters(LiandWang,2019; Pdss: Aprivacy-preservingframeworkforstep-by-
|     |     |     |     |     |     |     | step distillation |     | of large | language | models. |     | arXiv |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------- | -------- | ------- | --- | ----- |
Choetal.,2022),thereisnotheoreticalguarantee
preprintarXiv:2406.12403.
thatthisapproachdoesnotcompromisetheprivacy
ofclients’sensitivedata. Thisissuewarrantsfur- TaoFan,YanKang,GuoqiangMa,WeijingChen,Wen-
|                    |               |                              |          |     |         |      | bin Wei, | Lixin        | Fan, and | Qiang     | Yang.    | 2023.    | Fate-  |
| ------------------ | ------------- | ---------------------------- | -------- | --- | ------- | ---- | -------- | ------------ | -------- | --------- | -------- | -------- | ------ |
| therinvestigation. |               | Additionally,thestudydoesnot |          |     |         |      |          |              |          |           |          |          |        |
|                    |               |                              |          |     |         |      | llm:     | A industrial | grade    | federated | learning |          | frame- |
| address            | the potential |                              | presence | of  | spammer | (Zhu |          |              |          |           |          |          |        |
|                    |               |                              |          |     |         |      | work     | for large    | language | models.   | arXiv    | preprint |        |
etal.,2012)amongclients,whichcouldnegatively
arXiv:2310.10049.
impacttheperformanceofLLMintheserverand
|                        |     |     |                     |     |     |     | Tao Fan, | Yan | Kang, Guoqiang |        | Ma, Lixin | Fan, | Kai |
| ---------------------- | --- | --- | ------------------- | --- | --- | --- | -------- | --- | -------------- | ------ | --------- | ---- | --- |
| theSLMsofotherclients. |     |     | Detectingspammersin |     |     |     |          |     |                |        |           |      |     |
|                        |     |     |                     |     |     |     | Chen,    | and | Qiang Yang.    | 2024c. | Fedcollm: |      | A   |
theFedMKTsettingisidentifiedasanimportantre- parameter-efficient federated co-tuning framework
| searchdirection. |     | Furthermore,ourstudyislimited |     |     |     |     |     |     |     |     | arXivpreprint |     |     |
| ---------------- | --- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- |
forlargeandsmalllanguagemodels.
| by computational |                 | and | storage | constraints, |          | which | arXiv:2411.11707. |           |      |            |            |     |     |
| ---------------- | --------------- | --- | ------- | ------------ | -------- | ----- | ----------------- | --------- | ---- | ---------- | ---------- | --- | --- |
| preclude         | the exploration |     | of      | larger       | language | mod-  |                   |           |      |            |            |     |     |
|                  |                 |     |         |              |          |       | Yao Fu,           | Hao Peng, | Litu | Ou, Ashish | Sabharwal, |     | and |
els. Thishighlightstheinherenttrade-offbetween
|     |     |     |     |     |     |     | Tushar | Khot. | 2023. Specializing |     | smaller | language |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ----- | ------------------ | --- | ------- | -------- | --- |
utilityandefficiency. Ourfutureresearchaimsto models towards multi-step reasoning. In Inter-
|     |     |     |     |     |     |     | national | Conference |     | on Machine | Learning, |     | pages |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | ---------- | --------- | --- | ----- |
investigateandoptimizethistrade-off.
10421–10430.PMLR.
LeoGao,JonathanTow,BaberAbbasi,StellaBiderman,
References
SidBlack,AnthonyDiPofi,CharlesFoster,Laurence
Golding,JeffreyHsu,AlainLeNoac’h,HaonanLi,
| Dongqi | Cai, Yaozong |     | Wu, | Shangguang |     | Wang, Fe- |     |     |     |     |     |     |     |
| ------ | ------------ | --- | --- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
KyleMcDonell,NiklasMuennighoff,ChrisOciepa,
| lix Xiaozhu |     | Lin, and  | Mengwei |            | Xu. 2022. | Aut-  |       |          |                 |           |        |             |     |
| ----------- | --- | --------- | ------- | ---------- | --------- | ----- | ----- | -------- | --------------- | --------- | ------ | ----------- | --- |
|             |     |           |         |            |           |       | Jason | Phang,   | Laria Reynolds, |           | Hailey | Schoelkopf, |     |
| ofednlp:    | An  | efficient | fednlp  | framework. |           | arXiv |       |          |                 |           |        |             |     |
|             |     |           |         |            |           |       | Aviya | Skowron, | Lintang         | Sutawika, | Eric   | Tang,       | An- |
preprintarXiv:2205.10162.
|     |     |     |     |     |     |     | ishThite, | BenWang, |     | KevinWang, | andAndyZou. |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ---------- | ----------- | --- | --- |
Yulong Chen, Yang Liu, Liang Chen, and Yue 2023. A framework for few-shot language model
| Zhang.   | 2021.         | Dialogsum: |          | A   | real-life | scenario | evaluation. |     |     |     |     |     |     |
| -------- | ------------- | ---------- | -------- | --- | --------- | -------- | ----------- | --- | --- | --- | --- | --- | --- |
| dialogue | summarization |            | dataset. |     | arXiv     | preprint |             |     |     |     |     |     |     |
YuxianGu,LiDong,FuruWei,andMinlieHuang.2023.
arXiv:2105.06762.
|     |     |     |     |     |     |     | Minillm: | Knowledgedistillationoflargelanguage |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------------------------ | --- | --- | --- | --- | --- |
Kewei Cheng, Tao Fan, Yilun Jin, Yang Liu, Tian- models. InTheTwelfthInternationalConferenceon
LearningRepresentations.
jianChen,DimitriosPapadopoulos,andQiangYang.
| 2021. | Secureboost: |     | A lossless | federated |     | learning |     |     |     |     |     |     |     |
| ----- | ------------ | --- | ---------- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
JunxianHe,ChuntingZhou,XuezheMa,TaylorBerg-
| framework. | IEEEIntelligentSystems,36(6):87–98. |     |     |     |     |     |                                   |     |     |     |     |          |     |
| ---------- | ----------------------------------- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | -------- | --- |
|            |                                     |     |     |     |     |     | Kirkpatrick,andGrahamNeubig.2021. |     |     |     |     | Towardsa |     |
Yae Jee Cho, Andre Manoel, Gauri Joshi, Robert unifiedviewofparameter-efficienttransferlearning.
Sim, and Dimitrios Dimitriadis. 2022. Hetero- arXivpreprintarXiv:2110.04366.

Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. 2015. SourabMangrulkar,SylvainGugger,LysandreDebut,
Distillingtheknowledgeinaneuralnetwork. arXiv YounesBelkada,SayakPaul,andBenjaminBossan.
preprintarXiv:1503.02531. 2022. Peft: State-of-the-artparameter-efficientfine-
|               |        |          |     |           |              |     | tuning | methods. | https://github.com/huggingface/ |     |     |     |
| ------------- | ------ | -------- | --- | --------- | ------------ | --- | ------ | -------- | ------------------------------- | --- | --- | --- |
| Neil Houlsby, | Andrei | Giurgiu, |     | Stanislaw | Jastrzebski, |     |        |          |                                 |     |     |     |
peft.
| Bruna Morrone, |     | Quentin | De  | Laroussilhe, |     | Andrea |     |     |     |     |     |     |
| -------------- | --- | ------- | --- | ------------ | --- | ------ | --- | --- | --- | --- | --- | --- |
Gesmundo,MonaAttariyan,andSylvainGelly.2019.
|                                            |     |     |     |     |     |       | Brendan       | McMahan, | Eider      | Moore, | Daniel   | Ramage,      |
| ------------------------------------------ | --- | --- | --- | --- | --- | ----- | ------------- | -------- | ---------- | ------ | -------- | ------------ |
| Parameter-efficienttransferlearningfornlp. |     |     |     |     |     | InIn- |               |          |            |        |          |              |
|                                            |     |     |     |     |     |       | Seth Hampson, |          | and Blaise |        | Aguera y | Arcas. 2017. |
ternationalConferenceonMachineLearning,pages
Communication-efficientlearningofdeepnetworks
2790–2799.PMLR.
|     |     |     |     |     |     |     | fromdecentralizeddata. |     |     | InArtificialintelligenceand |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --------------------------- | --- | --- |
statistics,pages1273–1282.PMLR.
| Edward J   | Hu, Yelong |          | Shen,     | Phillip Wallis, |       | Zeyuan   |              |          |     |     |     |     |
| ---------- | ---------- | -------- | --------- | --------------- | ----- | -------- | ------------ | -------- | --- | --- | --- | --- |
| Allen-Zhu, | Yuanzhi    |          | Li, Shean | Wang,           | Lu    | Wang,    |              |          |     |     |     |     |
| and Weizhu | Chen.      | 2021.    |           | Lora: Low-rank  |       | adap-    | OpenAI.2022. | Chatgpt. |     |     |     |     |
| tation of  | large      | language | models.   |                 | arXiv | preprint |              |          |     |     |     |     |
arXiv:2106.09685. AlecRadford,JeffreyWu,RewonChild,DavidLuan,
|     |     |     |     |     |     |     | DarioAmodei,IlyaSutskever,etal.2019. |     |     |     |     | Language |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | -------- |
JaeheeJang,HeoneokHa,DahuinJung,andSungroh
|            |              |     |                           |     |     |     | modelsareunsupervisedmultitasklearners. |     |     |     |     | OpenAI |
| ---------- | ------------ | --- | ------------------------- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | ------ |
| Yoon.2022. | Fedclassavg: |     | Localrepresentationlearn- |     |     |     |                                         |     |     |     |     |        |
blog,1(8):9.
ingforpersonalizedfederatedlearningonheteroge-
neousneuralnetworks. InProceedingsofthe51stIn- Teven Le Scao, Angela Fan, Christopher Akiki, El-
ternationalConferenceonParallelProcessing,pages
|     |     |     |     |     |     |     | lie Pavlick, | Suzana | Ilic´, | Daniel | Hesslow, | Roman |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------ | ------ | ------ | -------- | ----- |
1–10.
Castagné,AlexandraSashaLuccioni,FrançoisYvon,
|     |     |     |     |     |     |     | Matthias | Gallé, | et al. | 2022. | Bloom: | A 176b- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------ | ----- | ------ | ------- |
YanKang,TaoFan,HanlinGu,LixinFan,andQiang
parameteropen-accessmultilinguallanguagemodel.
| Yang.2023. | Groundingfoundationmodelsthrough |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:2211.05100.
| federated | transfer | learning: |     | A general | framework. |     |     |     |     |     |     |     |
| --------- | -------- | --------- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:2311.17431.
|     |     |     |     |     |     |     | Alon Talmor, | Jonathan |     | Herzig, | Nicholas | Lourie, and |
| --- | --- | --- | --- | --- | --- | --- | ------------ | -------- | --- | ------- | -------- | ----------- |
BrianLester,RamiAl-Rfou,andNoahConstant.2021. JonathanBerant.2018. Commonsenseqa:Aquestion
The power of scale for parameter-efficient prompt answeringchallengetargetingcommonsenseknowl-
arXivpreprintarXiv:2104.08691. arXivpreprintarXiv:1811.00937.
| tuning.         |     |        |           |     |        |        | edge. |       |         |          |        |         |
| --------------- | --- | ------ | --------- | --- | ------ | ------ | ----- | ----- | ------- | -------- | ------ | ------- |
| Quentin Lhoest, |     | Albert | Villanova | del | Moral, | Yacine |       |       |         |          |        |         |
|                 |     |        |           |     |        |        | Gemma | Team, | Morgane | Riviere, | Shreya | Pathak, |
Jernite,AbhishekThakur,PatrickvonPlaten,Suraj
PierGiuseppeSessa,CassidyHardin,SuryaBhupati-
Patil,JulienChaumond,MariamaDrame,JulienPlu,
|                 |     |           |          |       |           |      | raju, Léonard                      |     | Hussenot, | Thomas | Mesnard, | Bobak   |
| --------------- | --- | --------- | -------- | ----- | --------- | ---- | ---------------------------------- | --- | --------- | ------ | -------- | ------- |
| Lewis Tunstall, |     | Joe       | Davison, | Mario | Šaško,    | Gun- |                                    |     |           |        |          |         |
|                 |     |           |          |       |           |      | Shahriari,AlexandreRamé,etal.2024. |     |           |        |          | Gemma2: |
| jan Chhablani,  |     | Bhavitvya | Malik,   | Simon | Brandeis, |      |                                    |     |           |        |          |         |
Improvingopenlanguagemodelsatapracticalsize.
| Teven Le | Scao, | Victor | Sanh, | Canwen | Xu, | Nicolas |     |     |     |     |     |     |
| -------- | ----- | ------ | ----- | ------ | --- | ------- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:2408.00118.
| Patry, Angelina |         | McMillan-Major, |           | Philipp |      | Schmid, |     |     |     |     |     |     |
| --------------- | ------- | --------------- | --------- | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- |
| Sylvain         | Gugger, | Clément         | Delangue, |         | Théo | Matus-  |     |     |     |     |     |     |
HugoTouvron,ThibautLavril,GautierIzacard,Xavier
| sière, Lysandre |     | Debut, | Stas | Bekman, | Pierric | Cis- |     |     |     |     |     |     |
| --------------- | --- | ------ | ---- | ------- | ------- | ---- | --- | --- | --- | --- | --- | --- |
Martinet,Marie-AnneLachaux,TimothéeLacroix,
| tac, Thibault |     | Goehringer, | Victor | Mustar, |     | François |          |          |       |     |             |         |
| ------------- | --- | ----------- | ------ | ------- | --- | -------- | -------- | -------- | ----- | --- | ----------- | ------- |
|               |     |             |        |         |     |          | Baptiste | Rozière, | Naman |     | Goyal, Eric | Hambro, |
Lagunas,AlexanderRush,andThomasWolf.2021.
|             |                                     |     |     |     |     |     | Faisal           | Azhar, | et al. 2023. |         | Llama: Open | and effi- |
| ----------- | ----------------------------------- | --- | --- | --- | --- | --- | ---------------- | ------ | ------------ | ------- | ----------- | --------- |
| Datasets:   | Acommunitylibraryfornaturallanguage |     |     |     |     |     |                  |        |              |         |             |           |
|             |                                     |     |     |     |     |     | cient foundation |        | language     | models. | arXiv       | preprint  |
| processing. | InProceedingsofthe2021Conference    |     |     |     |     |     |                  |        |              |         |             |           |
arXiv:2302.13971.
onEmpiricalMethodsinNaturalLanguageProcess-
ing: SystemDemonstrations,pages175–184,Online
FanqiWan,XintingHuang,DengCai,XiaojunQuan,
andPuntaCana,DominicanRepublic.Association
|     |     |     |     |     |     |     | Wei Bi, | and Shuming |     | Shi. | 2024. Knowledge | fu- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------- | --- | ---- | --------------- | --- |
forComputationalLinguistics.
|                                            |     |     |     |        |           |       | sion of           | large | language | models. | arXiv | preprint |
| ------------------------------------------ | --- | --- | --- | ------ | --------- | ----- | ----------------- | ----- | -------- | ------- | ----- | -------- |
| DaliangLiandJunpuWang.2019.                |     |     |     | Fedmd: | Heteroge- |       | arXiv:2401.10491. |       |          |         |       |          |
| nousfederatedlearningviamodeldistillation. |     |     |     |        |           | arXiv |                   |       |          |         |       |          |
preprintarXiv:1910.03581. AlexWang,YadaPruksachatkun,NikitaNangia,Aman-
preetSingh,JulianMichael,FelixHill,OmerLevy,
| Xiang Lisa                                | Li and | Percy | Liang. | 2021. | Prefix-tuning: |       |                         |     |     |     |                   |     |
| ----------------------------------------- | ------ | ----- | ------ | ----- | -------------- | ----- | ----------------------- | --- | --- | --- | ----------------- | --- |
|                                           |        |       |        |       |                |       | andSamuelR.Bowman.2019. |     |     |     | SuperGLUE:Astick- |     |
| Optimizingcontinuouspromptsforgeneration. |        |       |        |       |                | arXiv |                         |     |     |     |                   |     |
ierbenchmarkforgeneral-purposelanguageunder-
preprintarXiv:2101.00190. standingsystems. arXivpreprint1905.00537.
ChangLiu,YuwenYang,XunCai,YueDing,andHong-
taoLu.2022. Completelyheterogeneousfederated Yizhong Wang, Swaroop Mishra, Pegah Alipoor-
|           |                                |     |     |     |     |     | molabashi, | Yeganeh    |     | Kordi, | Amirreza | Mirzaei,    |
| --------- | ------------------------------ | --- | --- | --- | --- | --- | ---------- | ---------- | --- | ------ | -------- | ----------- |
| learning. | arXivpreprintarXiv:2210.15865. |     |     |     |     |     |            |            |     |        |          |             |
|           |                                |     |     |     |     |     | Anjana     | Arunkumar, |     | Arjun  | Ashok,   | Arut Selvan |
YangLiu,TaoFan,TianjianChen,QianXu,andQiang Dhanasekaran,AtharvaNaik,DavidStap,etal.2022.
Yang.2021. Fate: Anindustrialgradeplatformfor Benchmarkinggeneralizationviain-contextinstruc-
collaborativelearningwithdataprotection. J.Mach. tions on 1,600+ language tasks. arXiv preprint
| Learn.Res.,22(226):1–6. |     |     |     |     |     |     | arXiv:2204.07705,2. |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- |

MengzhouXia,TianyuGao,ZhiyuanZeng,andDanqi 4. On the server side, token alignment is per-
Chen.2023. Shearedllama: Acceleratinglanguage formed from the SLMs to the LLM, guaran-
| model pre-training |     | via | structured | pruning. | arXiv |     |        |               |     |         |     |      |     |
| ------------------ | --- | --- | ---------- | -------- | ----- | --- | ------ | ------------- | --- | ------- | --- | ---- | --- |
|                    |     |     |            |          |       |     | teeing | compatibility |     | between | the | SLMs | and |
preprintarXiv:2310.06694.
theLLM.
QiangYang,YangLiu,YongCheng,YanKang,Tian-
5. Ontheserverside,knowledgeisselectedfrom
| jian Chen, | and | Han Yu. | 2019. | Federated | learning. |     |     |     |     |     |     |     |     |
| ---------- | --- | ------- | ----- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
SynthesisLecturesonArtificialIntelligenceandMa- theSLMstotheLLMaccordingtoAlgorithm
chineLearning,13(3):1–207.
2.
| RuihongYang,JunchaoTian,andYuZhang.2021. |     |     |     |     | Reg- |     |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
6. Ontheserverside,knowledgeistransferred
ularizedmutuallearningforpersonalizedfederated
|                                  |                                     |                                 |       |               |      |     | from             | the SLMs | to        | the LLM     | based  | on      | the se- |
| -------------------------------- | ----------------------------------- | ------------------------------- | ----- | ------------- | ---- | --- | ---------------- | -------- | --------- | ----------- | ------ | ------- | ------- |
| learning.                        | InAsianConferenceonMachineLearning, |                                 |       |               |      |     |                  |          |           |             |        |         |         |
| pages1521–1536.PMLR.             |                                     |                                 |       |               |      |     | lectedknowledge. |          |           |             |        |         |         |
| Liping Yi,                       | Han Yu,                             | Gang                            | Wang, | and Xiaoguang | Liu. |     |                  |          |           |             |        |         |         |
|                                  |                                     |                                 |       |               |      |     | 7. Once          | the      | knowledge | transfer    |        | from    | SLMs    |
| 2023. Fedlora:                   |                                     | Model-heterogeneouspersonalized |       |               |      |     |                  |          |           |             |        |         |         |
|                                  |                                     |                                 |       |               |      |     | to LLM           | is       | completed |             | on the | server, | the     |
| federatedlearningwithloratuning. |                                     |                                 |       | arXivpreprint |      |     |                  |          |           |             |        |         |         |
|                                  |                                     |                                 |       |               |      |     | server           | then     | computes  | a knowledge |        | set     | S =     |
| arXiv:2310.13283.                |                                     |                                 |       |               |      |     |                  |          |           |             |        |         | 0       |
{li,pi}N
|     |     |     |     |     |     |     |     |       | consisting | of  | loss-logit |     | pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ---------- | --- | ---------- | --- | ----- |
|     |     |     |     |     |     |     | 0   | 0 i=1 |            |     |            |     |       |
Susan Zhang, Stephen Roller, Naman Goyal, Mikel throughLLMbasedonthepublicdataset.
Artetxe,MoyaChen,ShuohuiChen,ChristopherDe-
| wan, Mona | Diab, | Xian | Li, Xi | Victoria | Lin, et al. |     |                           |     |     |     |                  |     |     |
| --------- | ----- | ---- | ------ | -------- | ----------- | --- | ------------------------- | --- | --- | --- | ---------------- | --- | --- |
|           |       |      |        |          |             |     | 8. TheserverdisseminatesS |     |     |     | toalltheclients. |     |     |
0
| 2022a. Opt: | Openpre-trainedtransformerlanguage |     |     |     |     |     |           |        |       |           |           |              |      |
| ----------- | ---------------------------------- | --- | --- | --- | --- | --- | --------- | ------ | ----- | --------- | --------- | ------------ | ---- |
| models.     | arXivpreprintarXiv:2205.01068.     |     |     |     |     |     |           |        |       |           |           |              |      |
|             |                                    |     |     |     |     |     | 9. On the | client | side, | the token | alignment |              | flow |
|             |                                    |     |     |     |     |     | reverses, | and    | token | alignment |           | is performed |      |
YingZhang,TaoXiang,TimothyMHospedales,and
| HuchuanLu.2018. |     | Deepmutuallearning. |     |     | InPro- |     | fromtheLLMtoSLMs. |     |     |     |     |     |     |
| --------------- | --- | ------------------- | --- | --- | ------ | --- | ----------------- | --- | --- | --- | --- | --- | --- |
ceedingsoftheIEEEconferenceoncomputervision
andpatternrecognition,pages4320–4328. 10. Ontheclientside,knowledgeisselectedfrom
|     |     |     |     |     |     |     | the LLM | to  | each | client | SLM | according | to  |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ---- | ------ | --- | --------- | --- |
ZhuoZhang,YuanhangYang,YongDai,LizhenQu,and
Algorithm2.
| ZenglinXu.2022b. |     | Whenfederatedlearningmeets |     |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
pre-trainedlanguagemodels’parameter-efficienttun-
ingmethods. arXivpreprintarXiv:2212.10025. 11. On the client side, knowledge is transferred
|     |     |     |     |     |     |     | from | the LLM | to each | client | SLM | based | on  |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------- | ------- | ------ | --- | ----- | --- |
Haodong Zhao, Wei Du, Fangqi Li, Peixuan Li, and theselectedknowledge.
| GongshenLiu.2022.   |     | Reducecommunicationcosts |     |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| andpreserveprivacy: |     | Prompttuningmethodinfed- |     |     |     |     |     |     |     |     |     |     |     |
B ImplementationDetailsofToken
| eratedlearning. |     | arXivpreprintarXiv:2208.12268. |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Alignment
YinZhu,XiaoWang,ErhengZhong,NathanLiu,HeLi,
|                    |     |     |                          |     |     | In  | our work, | we  | engage | in a | bidirectional |     | token |
| ------------------ | --- | --- | ------------------------ | --- | --- | --- | --------- | --- | ------ | ---- | ------------- | --- | ----- |
| andQiangYang.2012. |     |     | Discoveringspammersinso- |     |     |     |           |     |        |      |               |     |       |
cialnetworks. InproceedingsoftheAAAIconference alignmentprocedure,encompassingthealignment
onartificialintelligence,volume26,pages171–177.
ofSLMtokenswiththeircorrespondingLLMto-
|     |     |     |     |     |     | kens,andviceversa. |     |     | Bothalignmentsadheretoa |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ----------------------- | --- | --- | --- | --- |
A FedMKTWorkflow
|     |     |     |     |     |     | similarmethodology. |     |     | Presently,weshallelaborate |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | -------------------------- | --- | --- | --- | --- |
TheworkflowofFedMKTisoutlinedasfollows: ontheprocessofaligningLLMtokenswiththeir
|     |     |     |     |     |     | matchingSLMtokens. |     |     | Tomapthepredictedtoken |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ---------------------- | --- | --- | --- | --- |
1. In the t-th communication round, the K logits from the LLaMa2-7B (LLM) model to the
clients train their respective LoRA adapters Bloom-1.1B(SLM)model,severalstepsmustbe
usingtheirprivatedata. Thisstepallowsthe undertaken. Thedetailedprocessisasfollows:
clientstoadapttheirmodelstotheirspecific
| datadistributions. |     |     |     |     |     |     | 1. BuildinganOptimalVocabularyMappingTa- |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- |
ble:
| 2. Afterlocaltraining,eachclientk |     |     |          | computesa    |     |     |     |               |         |        |           |     |         |
| --------------------------------- | --- | --- | -------- | ------------ | --- | --- | --- | ------------- | ------- | ------ | --------- | --- | ------- |
|                                   |     |     | {li,pi}N |              |     |     | (a) | For each      | token   | in the | LLaMa2    |     | vocabu- |
| knowledgesetS                     |     | k = |          | consistingof |     |     |     |               |         |        |           |     |         |
|                                   |     |     | k        | k i=1        |     |     |     | lary, iterate | through |        | the Bloom |     | vocabu- |
loss-logitpairsthroughitslocalmodelbased
lary.
onthepublicdataset.
|     |     |     |     |     |     |     | (b) | Use minimum |     | edit distance(MinED) |     |     | as  |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------------------- | --- | --- | --- |
3. Eachclientk uploadS totheserver. a similarity measure to find the closest
k

tokenintheBloomvocabularytotheto- Bloomvocabularythatcorrespondstot p
kenintheLLaMa2vocabulary. There- usingtheoptimalvocabularymappingta-
cursionfunctionforMinEDindynamic ble. Ifposhasnotbeenassignedavalue
programmingiselaboratedin(Fuetal., before,copylogit tothecorresponding
p
| 2023).                                 |     |     |     |     |     | positionintheBloomlogitsdistribution |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- |
|                                        |     |     |     |     |     | matrixlogit                          | .   |     |     |
| (c) Iftherearemultipletokenwiththesame |     |     |     |     |     |                                      | t   |     |     |
minimumeditdistance, choosetheone (d) Ift doesnothaveauniquematch,gen-
t
withthelexicographicallysmallestorder. erateone-hotlogitsfort .
t
(d) Savethismappingrelationshipintheop-
|     |     |     |     |     | 4. ProcessingtheResults: |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- |
timalvocabularymappingtable.
|                              |     |     |     |     |     | (a) Ultimately,eachtokent |     | inBloomwill |     |
| ---------------------------- | --- | --- | --- | --- | --- | ------------------------- | --- | ----------- | --- |
| 2. TokenizationandAlignment: |     |     |     |     |     |                           |     | t           |     |
haveacorrespondinglogitsdistribution
| (a) Tokenizethesentence"weutilizethedy- |     |     |     |     |     | matrixlogit | .   |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
t
namicprogrammingapproachtoalignto-
(b) Theselogitscanbedirectlyusedforsub-
kens"usingboththeLLaMa2andBloom sequenttrainingintheBloommodel.
tokenizers.
(b) Toalignthetwotokenizationresultsand
| determine |                              | the optimal | matching    |     | path, |     |     |     |     |
| --------- | ---------------------------- | ----------- | ----------- | --- | ----- | --- | --- | --- | --- |
| we        | utilize                      | a dynamic   | programming |     | al-   |     |     |     |     |
| gorithm.  | Asanillustration,considerthe |             |             |     |       |     |     |     |     |
tokenizationoutputsfromLLaMa2and
| Bloom. | LLaMa2’s |     | tokenization |     | yields: |     |     |     |     |
| ------ | -------- | --- | ------------ | --- | ------- | --- | --- | --- | --- |
[’we’,’util’,’ize’,’the’,’dynamic’,’pro-
gramming’,’approach’,’to’,’align’,’to-
| kens’].       | In  | contrast,                  | Bloom’s | tokeniza- |     |     |     |     |     |
| ------------- | --- | -------------------------- | ------- | --------- | --- | --- | --- | --- | --- |
| tionproduces: |     | [’we’,’utilize’,’the’,’dy- |         |           |     |     |     |     |     |
namic’,’programming’,’approach’,’to’,
| ’align’,’tokens’]. |     | Inthisinstance,seven |     |     |     |     |     |     |     |
| ------------------ | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
termsfromLLaMa2alignperfectlywith
thosefromBloom,suchas"we"and"dy-
| namic". | Notably, |     | the LLaMa2 |     | tokens |     |     |     |     |
| ------- | -------- | --- | ---------- | --- | ------ | --- | --- | --- | --- |
’util’and’ize’collectivelymaptothesin-
| gle | Bloom | token ’utilize’. |     | In scenarios |     |     |     |     |     |
| --- | ----- | ---------------- | --- | ------------ | --- | --- | --- | --- | --- |
wheremultipletokensaligntoone,like
the 2-to-1 case of ’util’ and ’ize’ map- Figure2: AnexamplefortokenalignmentviaMinED.
pingto’utilize’,weconsider’utilize’as
| a match | for | ’util’ | based on | an optimal |     |     |     |     |     |
| ------- | --- | ------ | -------- | ---------- | --- | --- | --- | --- | --- |
vocabularymapping. Figure2illustrates C ComputationandCommunication
Complexity
anexampleoftokenalignmentbetween
LLaMa2andBloom.
OneofthekeyadvantagesofFedMKTisitscompu-
3. LogitsMapping: tationalefficiency. ByleveragingPEFT,theframe-
worksignificantlyreducesthenumberofparame-
| (a) Iterate | through | each | token | t   | in the                                    |     |     |     |     |
| ----------- | ------- | ---- | ----- | --- | ----------------------------------------- | --- | --- | --- | --- |
|             |         |      |       | t   | tersthatneedtobeupdatedduringfine-tuning. |     |     |     | For |
Bloomtokenizationresult.
|              |                           |     |     |     | instance,                                     | it consumesjust0.12% |     | ofthecomputa- |     |
| ------------ | ------------------------- | --- | --- | --- | --------------------------------------------- | -------------------- | --- | ------------- | --- |
| (b) Foreacht | ,checkifituniquelymatches |     |     |     |                                               |                      |     |               |     |
|              | t                         |     |     |     | tionalcostassociatedwithfine-tuningallparame- |                      |     |               |     |
a token t in the LLaMa2 tokenization tersinOPT-1.3BwhenusingFedMKT.Thisleads
s
| result. |     |     |     |     | tofastertrainingtimesandreducedcomputational |     |     |     |     |
| ------- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- |
(c) Ift t uniquelymatchest s ,thenforeach requirements,makingitmorefeasibletofine-tune
tokent intheTop-K predictedtokenof LLMandSLMsinafederatedlearningsetting.
p
t from LLaMa2 and its corresponding In terms of communication complexity,
s
logitlogit : Findthepositionposinthe FedMKTminimizestheamountofdataexchanged
p

betweenclientsandtheserver. Insteadoftransmit- outputlengthgreaterthanorequalto11. Fromthis
tingentiremodels(Forexample,OPT-1.3Bisabout processeddata,werandomlyselected300samples
1.3B floating-point numbers), clients only share astheevaluationdataset. Theremainingdatawas
theoutputlogitsandcorrespondingcross-entropy thensplitintofiveequalparts,withonepartserv-
losses of the public dataset with the server. Sup- ingasthepublicdatasetandtheotherfourpartsas
posethereareN = 1000publictextsampleswith privatedataforthefourclients.
| atextsequencelengthofS |     |     |     | = 512andatoptoken |     |
| ---------------------- | --- | --- | --- | ----------------- | --- |
D.3 MachineConfiguration
| sizeofK | = 16. | Thecommunicationcost,denoted |     |     |     |
| ------- | ----- | ---------------------------- | --- | --- | --- |
as Cost , would be calculated as follows: The experiments were conducted on machines
com
Cost = N ∗S ∗K = 1000∗512∗16 = 8M equipped with either 4 Nvidia V100 32G or 8
com
floating-point numbers. This approach reduces NvidiaV10032GGPUs.
| communicationoverhead, |     |     | allowingformoreeffi- |     |     |
| ---------------------- | --- | --- | -------------------- | --- | --- |
cientdatatransmissionandenhancingscalability
infederatedlearningscenarios.
D MoreonExperimentalDetails
D.1 HyperparameterSettings
| LoRA                        | Parameters. |     |         | We utilized        | the  |
| --------------------------- | ----------- | --- | ------- | ------------------ | ---- |
| PEFT(Mangrulkar             |             |     | et al., | 2022) library      | with |
| thefollowingconfigurations: |             |     |         | r=8,lora_alpha=16, |      |
lora_dropout=0.05.
| Common | Parameters |     | for | LLM | and SLMs. |
| ------ | ---------- | --- | --- | --- | --------- |
Wesetbatch_size=4,usedtheAdamWoptimizer
| withadam_beta1=0.9andadam_beta2=0.95. |     |     |     |     | The |
| ------------------------------------- | --- | --- | --- | --- | --- |
warmup_ratiowassetto0.008,theweight_decay
| was0.1,max_grad_normwas1.0. |     |     |     | Theλwas0.9. |     |
| --------------------------- | --- | --- | --- | ----------- | --- |
Thenumberoftrainingroundsforalldataiswithin
10andthenumberoftrainingroundsfordifferent
datasetsmaybedifferent.
| LLM         | Parameters. |     | During  | distillation,   | the      |
| ----------- | ----------- | --- | ------- | --------------- | -------- |
| local epoch | R           | was | set to  | 1. The learning | rates    |
| η were      | specified   |     | as 3e-5 | for the         | datasets |
ω
RTE/WIC/BoolQ/CQA/ARC-C/DialogSum/S-NI,
and2e-5forARC-E.
| SLMParameters.                   |     |     | Duringtrainingforthefour |                   |          |
| -------------------------------- | --- | --- | ------------------------ | ----------------- | -------- |
| clients,thelocalepochEwassetto1. |     |     |                          | Thelearning       |          |
| ratesη θ wereasfollows:          |     |     | for"OPT-1.3B",η          |                   | θ =3e-5; |
| for "GPT-2-xlarge",              |     |     | η =3e-4;                 | for "Bloom-1.1B", |          |
θ
η =3e-5;andfor"LLaMa-2-1.3B",thesamelearn-
θ
ingratesasfortheLLMwereused.
D.2 DataSplitting
| For the | datasets | RTE/WIC/BoolQ/CQA/ARC- |     |     |     |
| ------- | -------- | ---------------------- | --- | --- | --- |
E/ARC-C/DialogSum,werandomlysplitthetrain-
ingdataintofiveequalparts,withonepartserving
asthepublicdatasetandtheremainingfourparts
| as private | dataset | for | the four | clients. | All these |
| ---------- | ------- | --- | -------- | -------- | --------- |
datasets(includingtrain,validate,test)weredown-
| loadedfromHuggingFace(Lhoestetal.,2021). |     |     |     |     | For |
| ---------------------------------------- | --- | --- | --- | --- | --- |
theS-NIdataset,wefirstprocessedthedatausing
minillm(Guetal.,2023)toretainsampleswithan