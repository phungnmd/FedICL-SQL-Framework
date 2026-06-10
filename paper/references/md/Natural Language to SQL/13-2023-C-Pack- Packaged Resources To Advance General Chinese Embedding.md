C-Pack: Packaged Resources To Advance General Chinese Embedding
ShitaoXiao♠ ZhengLiu♠† PeitianZhang♠ NiklasMuennighoff♣
♠ BeijingAcademyofArtificialIntelligence ♣ HuggingFace
stxiao@baai.ac.cn {zhengliu1026,namespace.pt,n.muennighoff}@gmail.com
Abstract
WeintroduceC-Pack,apackageofresources
thatsignificantlyadvancethefieldofgeneral
Chineseembeddings. C-Packincludesthree
criticalresources. 1)C-MTEBisacomprehen-
sivebenchmarkforChinesetextembeddings General-Purpose
Text Embedding
covering6tasksand35datasets. 2)C-MTP
C-Pack
is a massive text embedding dataset curated
from labeled and unlabeled Chinese corpora
fortrainingembeddingmodels. 3)C-TEMis
afamilyofembeddingmodelscoveringmul- C-MTEB C-MTP C-TEM Recipe
tiple sizes. Our models outperform all prior
ChinesetextembeddingsonC-MTEBbyup Figure1: TheC-Packresourcestosupportgeneral
to +10% upon the time of the release. We Chineseembedding.
alsointegrateandoptimizetheentiresuiteof
trainingmethodsforC-TEM. Alongwithour Thewidevarietyofapplicationscenarioscalls
resourcesongeneralChineseembedding,we for a single unified embedding model that can
release our data and models for English text
handleallkindsofusages(likeretrieval,ranking,
embeddings. TheEnglishmodelsachievestate-
classification) in any application scenarios (e.g.,
of-the-art performance on the MTEB bench-
question answering, language modeling, conver-
mark; meanwhile, our released English data
is 2 times larger than the Chinese data. All sation). However, learning general-purpose text
theseresourcesaremadepubliclyavailableat embeddings is much more challenging than task-
https://github.com/FlagOpen/FlagEmbedding. specificones. Thefollowingfactorsarecritical:
• Data. The development of general-purpose
1 Introduction
text embeddings puts forward much higher de-
mands on the training data in terms of scale, di-
Text embedding is a long-standing topic in natu-
versity,andquality. Toachievehighdiscriminative
rallanguageprocessingandinformationretrieval.
powerfortheembeddings,itmaytakemorethan
Byrepresentingtextswithlatentsemanticvectors,
hundreds of millions of training instances (Izac-
text embedding can support various applications,
ard et al., 2021; Ni et al., 2021b; Wang et al.,
e.g.,websearch,questionanswering,andretrieval-
2022b),whichisordersofmagnitudegreaterthan
augmented language modeling (Karpukhin et al.,
typical task-specific datasets, like MS MARCO
2020; Lewis et al., 2020; Guu et al., 2020). The
(Nguyen et al., 2016) and NLI (Bowman et al.,
recentpopularityoflargelanguagemodels(LLMs)
2015; Williams et al., 2017). Besides scale, the
has made text embeddings even more important.
training data needs to be collected from a wide
DuetotheinherentlimitationsofLLMs, suchas
range of sources so as to improve the generality
world knowledge and action space, external sup-
across different tasks (Izacard et al., 2021; Wang
portviaknowledgebasesortooluseisnecessary.
et al., 2022b). Finally, the augmentation of scale
TextembeddingsarecriticaltoconnectLLMswith
anddiversitywillprobablyintroducenoise. Thus,
theseexternalmodules(Borgeaudetal.,2022;Qin
thecollecteddatamustbeproperlycleanedbefore
etal.,2023).
beingutilizedforthetrainingofembeddings(Wang
†. Correspondenceauthor etal.,2022b).
3202
ceD
51
]LC.sc[
2v79570.9032:viXra

ChineseextensionofMTEB.1
| •Training. |     | Thetrainingofgeneral-purposetext |     |     |     |     |     |     | C-MTEBcollects |     |
| ---------- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | -------------- | --- |
embeddings depends on two critical elements: a 35 public-available datasets belonging to 6 types
well-suitedbackboneencoderandanappropriate of tasks. Thanks to the scale and diversity of C-
trainingrecipe. Whileonecanresorttogenericpre- MTEB, all major capabilities of Chinese embed-
trainedmodelslikeBERT(Devlinetal.,2018)and dingscanbereliablymeasured,makingitthemost
T5(Raffeletal.,2020),thequalityoftextembed- suitable benchmark to evaluate the generality of
dingcanbesubstantiallyimprovedbypre-training Chinesetextembedding.
withlarge-scaleunlabeleddata(Izacardetal.,2021; •C-MTP(ChineseMassiveTextPairs). Wecre-
| Wangetal.,2022b). |     |     | Further,insteadofrelyingon |     |     |                      |     |           |     |                |
| ----------------- | --- | --- | -------------------------- | --- | --- | -------------------- | --- | --------- | --- | -------------- |
|                   |     |     |                            |     |     | atea massivetraining |     | datasetof |     | 100Mtextpairs, |
asinglealgorithm, ittakesacompoundrecipeto which integrates both labeled data and unlabeled
traingeneral-purposetextembedding. Particularly, datacuratedfromWudao(Yuanetal.,2021),one
| it needs | embedding-oriented |     |     | pre-training | to  | pre- |     |     |     |     |
| -------- | ------------------ | --- | --- | ------------ | --- | ---- | --- | --- | --- | --- |
ofthelargestcorporaforpre-trainingChineselan-
parethetextencoder(GaoandCallan,2021),con-
|     |     |     |     |     |     | guage models. | C-MTP | is  | not only | large and di- |
| --- | --- | --- | --- | --- | --- | ------------- | ----- | --- | -------- | ------------- |
trastivelearningwithsophisticatednegativesam- versebutalsocleanedtoensurethedataquality.
plingtoimprovetheembedding’sdiscriminability • C-TEM (Chinese Text Embedding Models).
(Quetal.,2020),andinstruction-basedfine-tuning
|     |     |     |     |     |     | We provide | a family | of well-trained |     | models for |
| --- | --- | --- | --- | --- | --- | ---------- | -------- | --------------- | --- | ---------- |
(Suetal.,2022;Asaietal.,2022)tointegratediffer-
|     |     |     |     |     |     | Chinesegeneraltextembeddings. |     |     |     | Therearethree |
| --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | ------------- |
entrepresentationcapabilitiesoftextembedding.
|     |     |     |     |     |     | optionalmodelsizes: |     | small(24M),base(102M), |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | ---------------------- | --- | --- |
• Benchmark. Another pre-requisite condi- and large (326M), which present users with the
tion is the establishment of proper benchmarks, flexibilitytotradeoffefficiencyandeffectiveness.
| where all | needed | capabilities |     | of text | embeddings |     |     |     |     |     |
| --------- | ------ | ------------ | --- | ------- | ---------- | --- | --- | --- | --- | --- |
Ourmodelsmakeabigleapforwardingenerality:
canbecomprehensivelyevaluated. BEIR(Thakur C-TEM outperforms all previously Chinese text
et al., 2021) provides a collection of 18 to eval- embeddingmodelsonallaspectsofC-MTEBby
uate the embedding’s general performances on large margins. Besides being directly applicable,
| different | retrieval | tasks, | e.g., | question | answering |     |     |     |     |     |
| --------- | --------- | ------ | ----- | -------- | --------- | --- | --- | --- | --- | --- |
C-TEMcanalsobefine-tunedwithadditionaldata
and fact-checking. Later, MTEB (Muennighoff forbettertask-specificperformances.
etal.,2022a)proposesamoreholisticevaluation • Training Recipe. Accompanying our re-
ofembeddingsandextendsBEIR.Itintegrates56
sources,weintegrateandoptimizetrainingmeth-
| datasets, | where | all important |     | capabilities | of  | text |     |     |     |     |
| --------- | ----- | ------------- | --- | ------------ | --- | ---- | --- | --- | --- | --- |
odstobuildgeneral-purposetextembeddings,in-
embeddings,likeretrieval,ranking,clustering,etc.,
cludingthepre-trainingofanembedding-oriented
canbejointlyevaluated. textencoder,general-purposecontrastivelearning,
Altogether,thedevelopmentofgeneral-purpose and task-specific fine-tuning. The release of the
textembeddingneedstobemadeontopofamix- training recipe will help the community to repro-
tureofdrivingforces,fromdata,andencodermod- ducethestate-of-the-artmethodsandmakecontin-
els, to training methods and benchmarking. In uousprogressontopofthem.
recentyears,continualprogresshasbeenachieved Insummary,C-Packprovidesago-tooptionfor
inthisfield,suchasworkfromContriever(Izacard
people’sapplicationofgeneral-purposeChinese
| et al., 2021), |     | E5 (Wang | et  | al., 2022b), | and | Ope-           |                                  |     |     |     |
| -------------- | --- | -------- | --- | ------------ | --- | -------------- | -------------------------------- | --- | --- | --- |
|                |     |          |     |              |     | textembedding. | Itsubstantiallyadvancesthetrain- |     |     |     |
nAI Text Embedding (Neelakantan et al., 2022). ingandevaluation,layingasolidfoundationfor
However,mostoftheseworksareorientedtothe thefuturedevelopmentofthisfield.
| Englishworld. |     | Incontrast,thereisasevereshort- |     |     |     |     |     |     |     |     |
| ------------- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
ageofcompetitivemodelsforgeneralChineseem-
2 C-Pack
| bedding | due           | to a series | of       | limitations: | there | are   |     |     |     |     |
| ------- | ------------- | ----------- | -------- | ------------ | ----- | ----- | --- | --- | --- | --- |
| neither | well-prepared |             | training | resources    | nor   | suit- |     |     |     |     |
Inthissection,wefirstintroducetheresourcesin
ablebenchmarkstoevaluatethegenerality.
|            |              |           |             |         |            | C-Pack:                          | the benchmark | C-MTEB, |     | the training |
| ---------- | ------------ | --------- | ----------- | ------- | ---------- | -------------------------------- | ------------- | ------- | --- | ------------ |
| To address |              | the above | challenges, |         | we present | a                                |               |         |     |              |
|            |              |           |             |         |            | dataC-MTP,andthemodelclassC-TEM. |               |         |     | Then,        |
| package    | of resources |           | called      | C-Pack, | which      | con-                             |               |         |     |              |
wediscussthetrainingrecipe,whichenablesusto
tributestothedevelopmentofgeneralChineseem- trainthestate-of-the-artmodelsforgeneralChinese
beddingfromthefollowingperspectives.
embeddingbasedontheofferedresources.
•C-MTEB(ChineseMassiveTextEmbedding
| Benchmark). |     | The benchmark |     | is established |     | as a |     |     |     |     |
| ----------- | --- | ------------- | --- | -------------- | --- | ---- | --- | --- | --- | --- |
1. https://huggingface.co/spaces/mteb/leaderboard

C-MTEB (6 tasks, 35 datasets)
C-MTP (16 datasets, 100M pairs)
Classisication(9 datasets) Clustering(4 datasets) Wudao Corpora
|     |                  |     |     |         |     | CLSClusteringP2P |     | CLSClusteringS2S |     |     |     |
| --- | ---------------- | --- | --- | ------- | --- | ---------------- | --- | ---------------- | --- | --- | --- |
|     | AmazonReviews-ZH |     |     | IFlyTek |     |                  |     |                  |     |     |     |
Science Literature
|     |                  |     |     |          |     | ThuNewsClusteringP2P |     | ThuNewsClusteringS2S |     |     |     |
| --- | ---------------- | --- | --- | -------- | --- | -------------------- | --- | -------------------- | --- | --- | --- |
|     | MassiveIntent-ZH |     |     | JDReview |     |                      |     |                      |     |     |     |
XLSUM-Zh
|     | MassiveScenario-ZH |     |     | TNews |     |     |     |     |     |     |     |
| --- | ------------------ | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Reranking(4 datasets)
Wiki-Atomic-Edit
|     | MultilingualSentiment |     |     | Waimai |     |          |     |                 |     |     |     |
| --- | --------------------- | --- | --- | ------ | --- | -------- | --- | --------------- | --- | --- | --- |
|     |                       |     |     |        |     | CMedQAv1 |     | MMarcoReranking |     |     |     |
AmazonReviews-Zh
|     | OnlineShopping |     |     |     |     | CMedQAv2 |     | T2Reranking |     |     |     |
| --- | -------------- | --- | --- | --- | --- | -------- | --- | ----------- | --- | --- | --- |
and 11 others
|     |     | Retrieval(8 datasets) |     |     |     | STS(8 datasets) |     |     |     |     |     |
| --- | --- | --------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
Pair CLF
CmedqaRetrieval MedicalRetrieval AFQMC PAWSX (2 datasets) C-TEM(3 models)
C-TEM (large)
|     | CovidRetrieval |     |     | MMarcoRetrieval |     | ATEC | QBQTC | Cmnli |     |     |              |
| --- | -------------- | --- | --- | --------------- | --- | ---- | ----- | ----- | --- | --- | ------------ |
|     | DuRetrieval    |     |     | T2Retrieval     |     | BQ   | STS22 |       |     |     | C-TEM (base) |
Ocnli
|     | EcomRetrieval |     |     | VideoRetrieval |     | LCQMC | STSB |     |     |     |     |
| --- | ------------- | --- | --- | -------------- | --- | ----- | ---- | --- | --- | --- | --- |
C-TEM (small)
|     | Pre-Training  |     |                   | General-PurposeFine-tuning  |     |                   |                    | Task-SpecificFine-tuning  |                 |     |             |
| --- | ------------- | --- | ----------------- | --------------------------- | --- | ----------------- | ------------------ | ------------------------- | --------------- | --- | ----------- |
|     |               |     | Pre-Trained Model |                             |     |                   | Intermediate Model |                           |                 |     | Final Model |
|     | Wudao Corpora |     |                   |                             |     | C-MTP (unlabeled) |                    |                           | C-MTP (labeled) |     |             |
Figure2: OverviewofC-Pack. C-MTEBisabenchmarkforChinesetextembeddings. C-MTPisalarge-scale
Chineseembeddingtrainingdataset. C-TEMarestate-of-the-artChineseembeddingmodels. Thetrainingrecipeis
shownatthebottom.
2.1 Benchmark: C-MTEB ensuring the corresponding capability to be fully
evaluated.
| C-MTEB |     | is established |     | for the | comprehensive |     |     |     |     |     |     |
| ------ | --- | -------------- | --- | ------- | ------------- | --- | --- | --- | --- | --- | --- |
Thenatureofeachtaskanditsevaluationmetric
evaluationofthegeneralityofChineseembeddings
arebrieflyintroducedasfollows.
| (Figure | 2).         | In the | past      | few years, | the | community  |     |             |                                 |     |     |
| ------- | ----------- | ------ | --------- | ---------- | --- | ---------- | --- | ----------- | ------------------------------- | --- | --- |
|         |             |        |           |            |     |            |     | •Retrieval. | Theretrievaltaskispresentedwith |     |     |
| has     | put forward |        | essential | datasets   | to  | study Chi- |     |             |                                 |     |     |
nesetextembeddings,suchasCMNLI(Xuetal., thetestqueriesandalargecorpus. Foreachquery,
|         |          |     |     |                |     |           | it  | finds the Top-k | similar | documents | within the |
| ------- | -------- | --- | --- | -------------- | --- | --------- | --- | --------------- | ------- | --------- | ---------- |
| 2020a), | DuReader |     | (He | et al., 2017), |     | T2Ranking |     |                 |         |           |            |
corpus. Theretrievalqualitycanbemeasuredby
| (Xieetal.,2023). |     |     | However,thesedatasetsareinde- |     |     |     |     |     |     |     |     |
| ---------------- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
rankingandrecallmetricsatdifferentcut-offs. In
pendentlycuratedandonlyfocusononespecific
capability of the text embeddings. Thus, we cre- thiswork,weusethesettingfromBEIR(Thakur
etal.,2021),usingNDCG@10asthemainmetric.
ateC-MTEBto1)comprehensivecollectrelated
datasets,2)categorizethedatasetsand3)standard- •Re-ranking. There-rankingtaskispresented
izeandintegratetheevaluationpipleines. with test queries and their lists of candidate doc-
uments(onepositiveplusNnegativedocuments).
| In  | particular, |     | we collect | a total | of  | 35 public |     |     |     |     |     |
| --- | ----------- | --- | ---------- | ------- | --- | --------- | --- | --- | --- | --- | --- |
datasets,allofwhichcanbeusedtoevaluateChi- Foreachquery,itre-ranksthecandidatedocuments
|                     |     |     |     |                         |     |     | basedontheembeddingsimilarity. |     |     |     | TheMAPscore |
| ------------------- | --- | --- | --- | ----------------------- | --- | --- | ------------------------------ | --- | --- | --- | ----------- |
| nesetextembeddings. |     |     |     | Thecollecteddatasetsare |     |     |                                |     |     |     |             |
isusedasthemainmetric.
| categorized |     | based | on  | the embedding’s |     | capability |     |     |     |     |     |
| ----------- | --- | ----- | --- | --------------- | --- | ---------- | --- | --- | --- | --- | --- |
•
theymayevaluate. Thereare6groupsofevaluation STS (Semantic Textual Similarity). The
tasks: retrieval,re-ranking,STS(semantictextual STS(Agirreetal.,2012,2013,2014,2015,2016)
similarity), classification, pair classification, and taskistomeasurethecorrelationoftwosentences
clustering,whichcoverthemaininterestingaspects based on their embedding similarity. Following
of Chinese text embeddings. Note that there are the original setting in Sentence-BERT (Reimers
multipledatasetsforeachcategory. Thedatasetsof andGurevych,2019),theSpearman’scorrelation
thesamecategoryarecollectedfromdifferentdo- is computed with the given label, whose result is
mainsandcomplementarytoeachother,therefore usedasthemainmetric.

|     |     | C-MTP |     | C-MTP |     | tativeoneistheWudaocorpus(Yuanetal.,2021), |     |     |     |     |     |     |
| --- | --- | ----- | --- | ----- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- |
dataset
(unlabeled) (labeled) whichisthelargestwell-formatteddatasetforpre-
Wudao,CSL, T2-Ranking, trainingChineselanguagemodels. Foreachofits
|        |                | XLSUM-Zh, |     | mMARCO-Zh,       |     |                 |            |          |          |     |         |         |
| ------ | -------------- | --------- | --- | ---------------- | --- | --------------- | ---------- | -------- | -------- | --- | ------- | ------- |
| source |                |           |     |                  |     | articles,       | we extract | (title,  | passage) |     | to form | a text  |
|        | Amazon-Review- |           |     | DuReader,NLI-Zh, |     |                 |            |          |          |     |         |         |
|        |                |           |     |                  |     | pair. Following |            | the same | recipe,  |     | we also | collect |
|        | Zh,CMRC,etc.   |           |     | etc.             |     |                 |            |          |          |     |         |         |
suchtextpairsfromothersimilarwebcontentlike
| size |     | 100M |     | 838K |     |                               |     |     |     |     |              |     |
| ---- | --- | ---- | --- | ---- | --- | ----------------------------- | --- | --- | --- | --- | ------------ | --- |
|      |     |      |     |      |     | Zhihu,Baike,newswebsites,etc. |     |     |     |     | Asidefromthe |     |
Table1: CompositionofC-MTP openwebcontent,wealsoexploreotherpublicChi-
nesedatasetstoextracttextpairs,suchasCSL(sci-
|     |     |     |     |     |     | entific literature), |     | Amazon-Review-Zh |     |     |     | (reviews), |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | ---------------- | --- | --- | --- | ---------- |
• Classification.
|     |     | The | classification |     | task re- |     |     |     |     |     |     |     |
| --- | --- | --- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
WikiAtomicEdits(paraphrases),CMRC(machine
usesthelogisticregressionclassifierfromMTEB
readingcomprehension),XLSUM-Zh(summariza-
| (Muennighoff |           | et al., 2022a), | where  | the   | provided   |             |     |        |            |     |     |            |
| ------------ | --------- | --------------- | ------ | ----- | ---------- | ----------- | --- | ------ | ---------- | --- | --- | ---------- |
|              |           |                 |        |       |            | tion), etc. | The | paired | structures |     | are | obvious in |
| label is     | predicted | based           | on the | input | embedding. |             |     |        |            |     |     |            |
thesedatasets,whicharedirectlyextractedforthe
Theaverageprecisionisusedasthemainmetric.
augmentationofC-MTP(unlabeled).
| •Pair-classification. |     | Thistaskdealswithapair |     |     |     |          |       |         |      |     |     |           |
| --------------------- | --- | ---------------------- | --- | --- | --- | -------- | ----- | ------- | ---- | --- | --- | --------- |
|                       |     |                        |     |     |     | The text | pairs | curated | from | the | web | and other |
ofinputsentences,whoserelationshipispresented
|                    |     |                            |     |     |     | public | sources | are not | guaranteed |     | to  | be closely |
| ------------------ | --- | -------------------------- | --- | --- | --- | ------ | ------- | ------- | ---------- | --- | --- | ---------- |
| byabinarizedlabel. |     | Therelationshipispredicted |     |     |     |        |         |         |            |     |     |            |
related. Therefore,dataqualitycanbeamajorcon-
byembeddingsimilarity,wheretheaveragepreci-
cern. Inourwork,weuseasimplestrategytofilter
sionisusedasthemainmetric.
|                               |     |                                |     |                   |     | the data                             | before                              | adding | it to | C-MTP | (unlabeled). |           |
| ----------------------------- | --- | ------------------------------ | --- | ----------------- | --- | ------------------------------------ | ----------------------------------- | ------ | ----- | ----- | ------------ | --------- |
| •Clustering.                  |     | Theclusteringtaskistogroupsen- |     |                   |     |                                      |                                     |        |       |       |              |           |
|                               |     |                                |     |                   |     | Particularly,weuseathird-partymodel: |                                     |        |       |       |              | Text2Vec- |
| tencesintomeaningfulclusters. |     |                                |     | Followingtheorig- |     |                                      |                                     |        |       |       |              |           |
|                               |     |                                |     |                   |     | Chinese2                             | toscorethestrengthofrelationforeach |        |       |       |              |           |
inalsettinginMTEB(Muennighoffetal.,2022a),
|     |     |     |     |     |     | text pair. | We  | empirically |     | choose | a threshold | of  |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | ------ | ----------- | --- |
itusesthemini-batchk-meansmethodfortheeval-
|     |     |     |     |     |     | 0.43, and | drop | the samples |     | whose | scores | are be- |
| --- | --- | --- | --- | --- | --- | --------- | ---- | ----------- | --- | ----- | ------ | ------- |
uation,withbatchsizeequalto32andkequalto
|            |     |               |     |             |     | low the | threshold. | With | such  | an       | operation, | there     |
| ---------- | --- | ------------- | --- | ----------- | --- | ------- | ---------- | ---- | ----- | -------- | ---------- | --------- |
| the number | of  | labels within | the | mini-batch. | The |         |            |      |       |          |            |           |
|            |     |               |     |             |     | are 100 | million    | text | pairs | filtered | from       | the unla- |
V-measurescoreisusedasthemainmetric.
|     |     |     |     |     |     | beledcorpora. |     | Despitethesimplicity,wefindthat |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ------------------------------- | --- | --- | --- | --- |
Finally,theembedding’scapabilityoneachtask
iteffectivelyremovestheirrelevanttextpairswhen
| is measured | by       | the average | performance |     | of all  |          |           |     |         |     |       |           |
| ----------- | -------- | ----------- | ----------- | --- | ------- | -------- | --------- | --- | ------- | --- | ----- | --------- |
|             |          |             |             |     |         | manually | reviewing |     | samples | and | leads | to strong |
| datasets    | for that | task. The   | embedding’s |     | overall |          |           |     |         |     |       |           |
empiricalperformancesforthemodelstrainedon
generalityismeasuredbytheaverageperformance
C-MTP(unlabeled).
ofalldatasetsinC-MTEB.
|                   |     |       |     |     |     | • C-MTP  |               | (labeled). | The       | following |           | labeled |
| ----------------- | --- | ----- | --- | --- | --- | -------- | ------------- | ---------- | --------- | --------- | --------- | ------- |
|                   |     |       |     |     |     | datasets | are collected |            | for C-MTP |           | (labeled) | due     |
| 2.2 TrainingData: |     | C-MTP |     |     |     |          |               |            |           |           |           |         |
T2-Ranking
|     |     |     |     |     |     | to their | quality | and | diversity: |     |     | (Xie |
| --- | --- | --- | --- | --- | --- | -------- | ------- | --- | ---------- | --- | --- | ---- |
WecuratethelargestdatasetC-MTPforthetrain-
|                |     |         |            |     |            | et al.,        | 2023), | DuReader | (He        | et  | al., | 2017; Qiu   |
| -------------- | --- | ------- | ---------- | --- | ---------- | -------------- | ------ | -------- | ---------- | --- | ---- | ----------- |
| ing of general |     | Chinese | embedding. |     | The paired |                |        |          |            |     |      |             |
|                |     |         |            |     |            | et al., 2022), | mMARCO |          | (Bonifacio |     | et   | al., 2021), |
textsconstitutethedatafoundationforthetraining
CMedQA-v2(Zhangetal.,2018a),multi-cpr(Long
oftextembedding,e.g.,aquestionanditsanswer,
etal.,2022),NLI-Zh3,cmnli(Xuetal.,2020a)and
| two paraphrase  |        | sentences, | or    | two documents | on         |                       |                               |     |                       |     |     |     |
| --------------- | ------ | ---------- | ----- | ------------- | ---------- | --------------------- | ----------------------------- | --- | --------------------- | --- | --- | --- |
|                 |        |            |       |               |            | ocnli(Xuetal.,2020a). |                               |     | Thereare838,465paired |     |     |     |
| the same        | topic. | To ensure  | the   | generality    | of the     |                       |                               |     |                       |     |     |     |
|                 |        |            |       |               |            | textsintotal.         | AlthoughitismuchsmallerthanC- |     |                       |     |     |     |
| text embedding, |        | the paired | texts | need          | to be both |                       |                               |     |                       |     |     |     |
MTP(unlabeled),mostofthedataiscuratedfrom
| large-scaleanddiversified. |     |     | Therefore,C-MTPis |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
humanannotation,thusensuringahighcredibility
| collectedfromtwosources: |       |              | thecurationofmassive |              |     |              |                                 |     |     |     |     |     |
| ------------------------ | ----- | ------------ | -------------------- | ------------ | --- | ------------ | ------------------------------- | --- | --- | --- | --- | --- |
|                          |       |              |                      |              |     | ofrelevance. | Besides,C-MTP(labeled)alsofully |     |     |     |     |     |
| unlabeled                | data, | a.k.a. C-MTP |                      | (unlabeled); | and |              |                                 |     |     |     |     |     |
coversdifferentcapabilitiesofthetextembedding,
thecomprehensivecollectionoflabeleddata,a.k.a.
likeretrieval,ranking,similaritycomparison,etc.,
| C-MTP(labeled). |     | Thedatacollectionprocessis |     |     |     |             |     |         |     |           |     |         |
| --------------- | --- | -------------------------- | --- | --- | --- | ----------- | --- | ------- | --- | --------- | --- | ------- |
|                 |     |                            |     |     |     | which helps | to  | improve | the | embedding |     | model’s |
brieflyintroducedasfollows.
generalityafterfine-tuning.
| •C-MTP(unlabeled). |     |     | Welookforawidevari- |     |     |       |                 |     |     |       |     |             |
| ------------------ | --- | --- | ------------------- | --- | --- | ----- | --------------- | --- | --- | ----- | --- | ----------- |
|                    |     |     |                     |     |     | Given | the differences |     | in  | scale | and | quality, C- |
etyofcorpora,wherewecanextractrich-semantic
|                   |             |          |         |        |             | MTP (unlabeled) |     | and | C-MTP |     | (labeled) | are ap- |
| ----------------- | ----------- | -------- | ------- | ------ | ----------- | --------------- | --- | --- | ----- | --- | --------- | ------- |
| paired structures |             | from the | plain   | text,  | e.g., para- |                 |     |     |       |     |           |         |
| phrases,          | title-body. | Our      | primary | source | of data     |                 |     |     |       |     |           |         |
2. https://huggingface.co/GanymedeNil
| comesfromopenwebcorpora. |     |     |     | Themostrepresen- |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
3. https://huggingface.co/datasets/shibing624/nli_zh

pliedtodifferenttrainingstages,whichjointlyre- larly, we make use of the Wudao corpora (Yuan
sult in a strong performance for the embedding et al., 2021), which is a huge and high-quality
model. Detailedanalysiswillbemadeinourtrain- dataset for Chinese language model pre-training.
| ingrecipe. |     |     |     |     | WeleveragetheMAE-styleapproachpresentedin |     |     |     |
| ---------- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- |
RetroMAE(LiuandShao,2022;Xiaoetal.,2023),
| 2.3 ModelClass: |     | C-TEM |     |     |                                  |     |             |     |
| --------------- | --- | ----- | --- | --- | -------------------------------- | --- | ----------- | --- |
|                 |     |       |     |     | whichissimplebuthighlyeffective. |     | Thepolluted |     |
Weprovideacomprehensiveclassofwell-trained text is encoded into its embedding, from which
| embeddingmodelsforthecommunity. |     |     | Ourmodels |     |     |     |     |     |
| ------------------------------- | --- | --- | --------- | --- | --- | --- | --- | --- |
thecleantextisrecoveredontopofalight-weight
| takeaBERT-likearchitecture,wherethelastlayer’s |     |     |     |     | decoder: |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- |
hiddenstateofthespecialtoken[CLS]istrainedto
|     |     |     |     |     | (cid:88) |     | Enc(X˜). |     |
| --- | --- | --- | --- | --- | -------- | --- | -------- | --- |
workastheembedding. Therearethreedifferent min. −logDec(x|e ), e ←
|            |             |             |              |     |     | X˜  | X˜  |     |
| ---------- | ----------- | ----------- | ------------ | --- | --- | --- | --- | --- |
| scales for | the models: | large (with | 326M parame- |     |     |     |     |     |
x∈X
ters),base(with102Mparameters),andsmall(with
(Enc,Decaretheencoderanddecoder,X,X˜
| 24Mparameters). |         | Thelarge-scalemodelachieves |               |     |     |     |     | indi- |
| --------------- | ------- | --------------------------- | ------------- | --- | --- | --- | --- | ----- |
| the highest     | general | representation              | performances, |     |     |     |     |       |
catethecleanandpollutedtext.)
| leading | the current | public-available | models | by a |                             |     |                |     |
| ------- | ----------- | ---------------- | ------ | ---- | --------------------------- | --- | -------------- | --- |
|         |             |                  |        |      | •Generalpurposefine-tuning. |     | Thepre-trained |     |
considerable margin. The small-scale model is model is fine-tuned on C-MTP (unlabeled) via
also empirically competitive compared with the contrastivelearning,whereitislearnedtodiscrim-
public-availablemodelsandothermodeloptionsin
inatethepairedtextsfromtheirnegativesamples:
C-TEM;besides,itiswayfasterandlighter,mak-
| ingitsuitabletohandlemassiveknowledgebases |     |     |     |     |     | e⟨ep,eq⟩/τ |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | ---------- | --- | --- |
(cid:88)
| and high-throughput |     | applications. | Thanks to | the | min. −log |     |     | .   |
| ------------------- | --- | ------------- | --------- | --- | --------- | --- | --- | --- |
(cid:80) e⟨ep,e q′⟩/τ
|                                             |     |     |     |     |       | e⟨ep,eq⟩/τ + |     |     |
| ------------------------------------------- | --- | --- | --- | --- | ----- | ------------ | --- | --- |
| comprehensivecoverageofdifferentmodelsizes, |     |     |     |     | (p,q) |              | Q′  |     |
peoplearepresentedwiththeflexibilitytotradeoff
|     |     |     |     |     | (pandq arethepairedtexts,q′ |     | ∈ Q′ isanegative |     |
| --- | --- | --- | --- | --- | --------------------------- | --- | ---------------- | --- |
runningefficiencyandrepresentationqualitybased
ontheirownneeds. sample, τ is the temperature). One critical fac-
Asintroduced,themodelswithinC-TEMhave torofcontrastivelearningisthenegativesamples.
|     |     |     |     |     | Instead of mining | hard negative | samples | on pur- |
| --- | --- | --- | --- | --- | ----------------- | ------------- | ------- | ------- |
beenwell-trainedandachieveastronggenerality
for a wide variety of tasks. Meanwhile, they can pose,wepurelyrelyonin-batchnegativesamples
alsobefurtherfine-tunedif1)theembeddingsare (Karpukhinetal.,2020)andresorttoabigbatch
size(aslargeas19,200)toimprovethediscrimina-
appliedforaspecificscenario,2)thetrainingdata
ispresentedfortheapplicationscenario. Itisempir- tivenessoftheembedding.
icallyverifiedthatthefine-tunedmodelmaybring • Task-specific fine-tuning. The embedding
forth a much better performance for its applica- modelisfurtherfine-tunedwithC-MTP(labeled).
Thelabeleddatasetsaresmallerbutofhigherqual-
tion,comparedwithitsoriginalmodelinC-TEM,
andthefine-tunedmodelsfromothergeneralpre- ity. However, thecontainedtasksareofdifferent
trained encoders, like BERT. In other words, C- types,whoseimpactscanbemutuallycontradicted.
TEM not only presents people with direct usage In this place, we apply two strategies to mitigate
embeddingsbutalsoworksasafoundationwhere thisproblem. Ononehand,weleverageinstruction-
peoplemaydevelopmorepowerfulembeddings. basedfine-tuning(Suetal.,2022;Asaietal.,2022),
wheretheinputisdifferentiatedtohelpthemodel
2.4 TrainingRecipe accommodatedifferenttasks. Foreachtextpair(p,
The training recipe of C-TEM is completely re- q), ataskspecificinstructionI isattachedtothe
t
q′
leasedtothepublicalongwithC-Pack(Figure2). queryside: ← q+I . Theinstructionisaverbal
t
Ourtrainingrecipehasthreemaincomponents: 1) prompt,whichspecifiesthenatureofthetask,e.g.,
pre-trainingwithplaintexts,2)contrastivelearning “search relevant passages for the query”. On the
withC-MTP(unlabeled),and3)multi-tasklearn- other hand, the negative sampling is updated: in
ingwithC-MTP(labeled),whosespecifications additiontothein-batchnegativesamples,onehard
aremadeasfollows. negativesampleq′isminedforeachtextpair(p,q).
• Pre-Training. Our model is pre-trained on Thehardnegativesampleisminedfromthetask’s
massiveplaintextsthroughatailoredalgorithmin originalcorpus,followingtheANN-stylesampling
ordertobettersupporttheembeddingtask. Particu- strategyin(Xiongetal.,2020).

| model          |     |     | Dim | Retrieval |       | STS | PairCLF | CLF   | Re-rank |     | Cluster | Average |       |
| -------------- | --- | --- | --- | --------- | ----- | --- | ------- | ----- | ------- | --- | ------- | ------- | ----- |
| Text2Vec(base) |     |     | 768 | 38.79     | 43.41 |     | 67.41   | 62.19 | 49.45   |     | 37.66   |         | 48.59 |
Text2Vec(large) 1024 41.94 44.97 70.86 60.66 49.16 30.02 48.56
| Luotuo(large)  |     |     | 1024 | 44.40 | 42.79 |     | 66.62 | 61.0  | 49.25 |     | 44.39 |     | 50.12 |
| -------------- | --- | --- | ---- | ----- | ----- | --- | ----- | ----- | ----- | --- | ----- | --- | ----- |
| M3E(base)      |     |     | 768  | 56.91 | 50.47 |     | 63.99 | 67.52 | 59.34 |     | 47.68 |     | 57.79 |
| M3E(large)     |     |     | 1024 | 54.75 | 50.42 |     | 64.30 | 68.20 | 59.66 |     | 48.88 |     | 57.66 |
| Multi.E5(base) |     |     | 768  | 61.63 | 46.49 |     | 67.07 | 65.35 | 54.35 |     | 40.68 |     | 56.21 |
Multi.E5(large) 1024 63.66 48.44 69.89 67.34 56.00 48.23 58.84
OpenAI-Ada-002 1536 52.00 43.35 69.56 64.31 54.28 45.68 53.02
| BGE(small)    |     |     | 512     | 63.07                               | 49.45 |     | 70.35                  | 63.64 | 61.48 |                       | 45.09 |     | 58.28 |
| ------------- | --- | --- | ------- | ----------------------------------- | ----- | --- | ---------------------- | ----- | ----- | --------------------- | ----- | --- | ----- |
| BGE(base)     |     |     | 768     | 69.53                               | 54.12 |     | 77.50                  | 67.07 | 64.91 |                       | 47.63 |     | 62.80 |
| BGE(large)    |     |     | 1024    | 71.53                               | 54.98 |     | 78.94                  | 68.32 | 65.11 |                       | 48.39 |     | 63.96 |
|               |     |     | Table2: | PerformanceofvariousmodelsonC-MTEB. |       |     |                        |       |       |                       |       |     |       |
| 3 Experiments |     |     |         |                                     |       |     | oflargelanguagemodels. |       |       | Althoughtheadvantages |       |     |       |
forclassificationandclusteringtasksarenotasob-
Weconductexperimentalstudiesforthefollowing
vious,ourperformancesarestillonparorslightly
| purposes. | P1.  | Theextensiveevaluationofdifferent |     |         |     |     |                                          |     |     |     |     |     |     |
| --------- | ---- | --------------------------------- | --- | ------- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- |
|           |      |                                   |     |         |     |     | betterthantheothermostcompetitivemodels. |     |     |     |     |     | The |
| Chinese   | text | embeddings                        | on  | C-MTEB. | P2. | The |                                          |     |     |     |     |     |     |
aboveobservationsverifythestronggeneralityof
| empirical | verification |                                   | of the | text embeddings |     | by  |        |     |        |     |             |          |     |
| --------- | ------------ | --------------------------------- | ------ | --------------- | --- | --- | ------ | --- | ------ | --- | ----------- | -------- | --- |
|           |              |                                   |        |                 |     |     | C-TEM. | Our | models | can | be directly | utilized | to  |
| C-TEM.    | P3.          | Theexplorationofthepracticalvalue |        |                 |     |     |        |     |        |     |             |          |     |
supportdifferenttypesofapplicationscenarios.
| brought | by C-MTP. |     | P4. The | exploration |     | of the |     |     |     |     |     |     |     |
| ------- | --------- | --- | ------- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Second,weobserveperformancegrowthresult-
impactsintroducedbythetrainingrecipe.
ingfromthescalingupmodelsizeandembedding
WeconsiderthefollowingpopularChinesetext
|     |     |     |     |     |     |     | dimension. |     | Particularly,theaverageperformance |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ---------------------------------- | --- | --- | --- | --- |
embeddingmodelsasthebaselinesforourexper-
improvesfrom58.28to63.96,whentheembedding
| iments: | Text2Vec-Chinese4 |     |     | base and | large; | Luo- |       |             |      |       |     |        |         |
| ------- | ----------------- | --- | --- | -------- | ------ | ---- | ----- | ----------- | ---- | ----- | --- | ------ | ------- |
|         |                   |     |     |          |        |      | model | is expanded | from | small | to  | large. | Besides |
tuo5;M3E6
baseandlarge;multilingualE5(Wang
thegrowthinaverageperformance,therearealso
etal.,2022b)andOpenAItextembeddingada0027.
|          |        |           |     |            |     |        | improvementsacrossalltheevaluationtasks. |     |     |     |     |     | Com- |
| -------- | ------ | --------- | --- | ---------- | --- | ------ | ---------------------------------------- | --- | --- | --- | --- | --- | ---- |
| The main | metric | presented |     | in Section | 2.1 | is re- |                                          |     |     |     |     |     |      |
paredtotheothertwobaselines(Text2Vec,M3E),
portedforeachtaskinC-MTEB.
|     |     |     |     |     |     |     | the impact               |     | of scaling | up is | more                | consistent | and |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | ---------- | ----- | ------------------- | ---------- | --- |
|     |     |     |     |     |     |     | significantforourmodels. |     |            |       | Itisworthnotingthat |            |     |
3.1 GeneralEvaluation
|                |     |          |       |         |         |     | our small | model      | is still | empirically |     | competitive |     |
| -------------- | --- | -------- | ----- | ------- | ------- | --- | --------- | ---------- | -------- | ----------- | --- | ----------- | --- |
| We extensively |     | evaluate | C-TEM | against | popular |     |           |            |          |             |     |             |     |
|                |     |          |       |         |         |     | despite   | its highly | reduced  | model       |     | size, where | the |
ChinesetextembeddingsonC-MTEBasshownin
averageperformanceisevenhigherthanthelarge-
Table2.8
Wemakethefollowingobservations. scaleoptionofmanyexistingmodels. Asaresult,
First, our models outperform existing Chinese it provides people with the flexibility to trade-off
| text embeddings |              | by  | large margins. |     | There | is not |                                       |     |     |     |     |     |        |
| --------------- | ------------ | --- | -------------- | --- | ----- | ------ | ------------------------------------- | --- | --- | --- | --- | --- | ------ |
|                 |              |     |                |     |       |        | embeddingqualityandrunningefficiency: |     |     |     |     |     | people |
| only an         | overwhelming |     | advantage      | in  | terms | of the |                                       |     |     |     |     |     |        |
mayresorttoourlarge-scaleembeddingmodelto
average performance, but also notable improve- deal with high-precision usages, or switch to the
| mentsforthemajorityoftasksinC-MTEB. |     |     |     |     |     | The |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
small-scaleoneforhigh-throughputscenarios.
biggestimprovementsareontheretrievaltaskfol-
lowedbySTS,pairclassification,andre-ranking. 3.2 DetailedAnalysis
Suchaspectsarethemostcommonfunctionalities WeinvestigatethedetailedimpactofC-MTPand
oftextembeddings,whichareintensivelyutilized
|                 |     |      |                 |             |     |     | our training |     | recipe. | The | corresponding |     | experi- |
| --------------- | --- | ---- | --------------- | ----------- | --- | --- | ------------ | --- | ------- | --- | ------------- | --- | ------- |
| in applications |     | like | search engines, | open-domain |     |     |              |     |         |     |               |     |         |
mentresultsarepresentedinTable3andTable4.
questionanswering,andtheretrievalaugmentation
Firstofall,weanalyzetheimpactofourtrain-
|     |     |     |     |     |     |     | ingdata,C-MTP. |     | Asmentioned,C-MTPconsists |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------------------------- | --- | --- | --- | --- |
4. https://huggingface.co/shibing624
5. https://huggingface.co/silk-road/luotuo-bert-medium of two parts. 1) C-MTP (unlabeled), which is
6. https://huggingface.co/moka-ai
|     |     |     |     |     |     |     | used | for general-purpose |     | fine-tuning; |     | the | model |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------------------- | --- | ------------ | --- | --- | ----- |
7. https://platform.openai.com/docs/guides/embeddings
|     |     |     |     |     |     |     | produced | from | this stage | is  | called | the intermedi- |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ---------- | --- | ------ | -------------- | --- |
8. OurC-TEMmodelsarenamedBGEinthetables.

| model      |     | Dim  | Retrieval | STS   | PairCLF | CLF   | Re-rank | Cluster | Average |
| ---------- | --- | ---- | --------- | ----- | ------- | ----- | ------- | ------- | ------- |
| M3E(large) |     | 1024 | 54.75     | 50.42 | 64.30   | 68.20 | 59.66   | 48.88   | 57.66   |
OpenAI-Ada-002 1536 52.00 43.35 69.56 64.31 54.28 45.68 53.02
| w.o.Instruct |     | 1024 | 70.55 | 53.00 | 76.77 | 68.58 | 64.91 | 50.01 | 63.40 |
| ------------ | --- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| BGE-i        |     | 1024 | 63.90 | 47.71 | 61.67 | 68.59 | 60.12 | 47.73 | 59.00 |
BGE-iw.o.pre-train 1024 62.56 48.06 61.66 67.89 61.25 46.82 58.62
| BGE-f |         | 1024                                                  | 71.53 | 54.98 | 78.94 | 68.32 | 65.11 | 48.39 | 63.96 |
| ----- | ------- | ----------------------------------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
|       | Table3: | Ablationofthetrainingdata,C-MTP,andthetrainingrecipe. |       |       |       |       |       |       |       |
ate checkpoint, denoted as BGE-i. 2) C-MTP pre-trainedembeddingmodel.
| (labeled), | where | the task-specific | fine-tuning | is  |     |                 |     |            |               |
| ---------- | ----- | ----------------- | ----------- | --- | --- | --------------- | --- | ---------- | ------------- |
|            |       |                   |             |     | We  | further explore |     | the impact | of our train- |
furtherconductedontopofBGE-i;themodelpro- ingrecipe,particularlycontrastivelearning,task-
ducedfromthisstageiscalledthefinalcheckpoint,
specificfine-tuning,andpre-training.
| notedasBGE-f. | Basedonourobservationsfrom |     |     |     |     |     |     |     |     |
| ------------- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Onenotablefeatureofourtrainingrecipeisthat
theexperimentalresult,bothC-MTP(unlabeled)
weadoptalargebatchsizeforcontrastivelearning.
andC-MTP(labeled)substantiallycontributeto
Accordingtopreviousstudies,thelearningofthe
theembedding’squality.
embeddingmodelmaybenefitfromtheincreasing
RegardingC-MTP(unlabeled),despitemostly ofnegativesamples(Izacardetal.,2021;Quetal.,
beingcuratedfromunlabeledcorpora,thisdataset 2020;Muennighoff,2022). Givenourdependency
alone brings forth strong empirical performance onin-batchnegativesamples,thebatchsizeneeds
for the embedding models trained on it. Com- tobeexpandedasmuchaspossible. Inourimple-
paredwithotherbaselineslikeText2Vec,M3E,and mentation,weuseacompoundstrategyofgradient
OpenAItextembedding,BGE-ialreadyachieves checkpointingandcross-deviceembeddingsharing
ahigheraverageperformance. Afurtherlookinto (Gao et al., 2021b), which results in a maximum
the performances reveals more details. On one batchsizeof19,200. Bymakingaparallelcompar-
hand,C-MTP(unlabeled)makesamajorimpact ison between bz: 256, 2028, 19,200, we observe
ontheembedding’sretrievalquality,whereBGE-i consistentimprovementinembeddingqualitywith
notablyoutperformsthebaselinesinthisattribute. theexpansionofbatchsize(notedasbz). Themost
On the other hand, the general capability of em- notableimprovementisachievedinretrievalperfor-
beddingisprimarilyestablishedwithC-MTP(un- mance. Thisislikelyduetothefactthatretrieval
labeled), as BGE-i’s performance is close to the isusuallyperformedoveralargedatabase,where
baselines onthe rest ofthe aspects, like STS and embeddingsneedtobehighlydiscriminative.
| Clustering. | Thisputsourembeddingmodelsina |     |     |     |     |     |     |     |     |
| ----------- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Anotherfeatureistheutilizationofinstructions
veryfavorablepositionforfurtherimprovements. duringtask-specificfine-tuning. Thetask-specific
|              |     |            |             |         | instructionservesasahardprompt. |     |     | Itdifferentiates |     |
| ------------ | --- | ---------- | ----------- | ------- | ------------------------------- | --- | --- | ---------------- | --- |
| As for C-MTP |     | (labeled), | the dataset | is much |                                 |     |     |                  |     |
smaller but of better quality. With another round theembeddingmodel’sactivation,whichletsthe
|                |     |                  |     |             | model | better accommodate |     | a variety | of different |
| -------------- | --- | ---------------- | --- | ----------- | ----- | ------------------ | --- | --------- | ------------ |
| of fine-tuning | on  | C-MTP (labeled), |     | the empiri- |       |                    |     |           |              |
tasks. Weperformtheablationstudybyremoving
caladvantageissignificantlyexpandedforthefi-
nal checkpoint BGE-f, where it gives rise to a thisoperation,notedas“w.o. Instruct”. Compared
withthisvariation,theoriginalmethodBGE-fgives
jumpinaverageperformancefrom59.0(BGE-i)to
|               |                             |     |     |     | risetobetteraverageperformance. |             |           |            | Besides,there |
| ------------- | --------------------------- | --- | --- | --- | ------------------------------- | ----------- | --------- | ---------- | ------------- |
| 63.96(BGE-f). | KnowingthatthetextpairsinC- |     |     |     |                                 |             |           |            |               |
|               |                             |     |     |     | are more                        | significant | empirical | advantages | on re-        |
MTP(labeled)aremainlygatheredfromretrieval
andNLItasks,themostnotableimprovementsare trieval, STS, pair classification, and re-rank. All
theseperspectivesarecloselyrelatedtothetrain-
achievedoncloselyrelatedtasks,namelyretrieval,
|                                       |     |     |     |         | ing data | at the final | stage, | i.e. C-MTP | (labeled), |
| ------------------------------------- | --- | --- | --- | ------- | -------- | ------------ | ------ | ---------- | ---------- |
| re-ranking,STS,andpairclassification. |     |     |     | Onother |          |              |        |            |            |
tasks, itpreservesormarginallyimprovesperfor- wherethemodelisfine-tunedonasmallgroupof
|     |     |     |     |     | tasks. | This indicates | that | using instructions | may |
| --- | --- | --- | --- | --- | ------ | -------------- | ---- | ------------------ | --- |
mance. Thisindicatesthatamixtureofhigh-quality
substantiallycontributetotask-specificfine-tuning.
anddiversifiedlabeleddataisabletobringforth
substantialandcomprehensiveimprovementsfora Onemorecharacteristicisthatweuseaspecif-

BatchSize 256 2,048 19,200 2021b,a) in line with observations for the impor-
tanceofscalingLLMs(Hoffmannetal.,2022;Rae
| Retrieval |     | 57.25 |     | 60.96 | 63.90 |     |     |     |     |     |     |     |
| --------- | --- | ----- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
etal.,2021;Brownetal.,2020;Chowdheryetal.,
| STS |     | 46.16 |     | 46.60 | 47.71 |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
2022;Srivastavaetal.,2022;Gaoetal.,2021a;Li
| PairCLF |     | 62.02 |     | 61.91 | 61.67 |     |     |     |     |     |     |     |
| ------- | --- | ----- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
etal.,2023a;Allaletal.,2023;Muennighoffetal.,
| CLF     |     | 65.71 |     | 67.42 | 68.59 |     |               |                                      |              |          |           |          |
| ------- | --- | ----- | --- | ----- | ----- | --- | ------------- | ------------------------------------ | ------------ | -------- | --------- | -------- |
|         |     |       |     |       |       |     | 2023b).       | Thirdly,thetrainingrecipemustbeopti- |              |          |           |          |
| Re-rank |     | 58.59 |     | 59.98 | 60.12 |     |               |                                      |              |          |           |          |
|         |     |       |     |       |       |     | mized through |                                      | pre-training | (Liu     | and Shao, | 2022;    |
| Cluster |     | 49.52 |     | 49.04 | 47.73 |     |               |                                      |              |          |           |          |
|         |     |       |     |       |       |     | Wang et       | al., 2022a),                         | negative     | sampling |           | (Izacard |
Average 56.43 57.92 59.00 et al., 2021; Wang et al., 2022a), and multi-task
fine-tuning(Suetal.,2022;Asaietal.,2022;Sanh
Impactofbatchsize.
Table4:
|     |     |     |     |     |     |     | et al., 2021;                 | Wei | et al., | 2021; Muennighoff |              | et al., |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | ------- | ----------------- | ------------ | ------- |
|     |     |     |     |     |     |     | 2022b,2023a;Chungetal.,2022). |     |         |                   | Asidefromthe |         |
ically pre-trained text encoder to train C-TEM, above,itisalsocriticaltoestablishproperbench-
ratherthanusingcommonchoices,likeBERTand markstoevaluatethegeneralityoftextembeddings.
RoBERTa(Liuetal.,2019). Toexploreitsimpact, Unlikeprevioustask-specificevaluations,likeMS-
we replace the pre-trained text encoder with the MARCO (Nguyen et al., 2016), SentEval (Con-
widelyusedChinese-RoBERTa9,notedas“BGE- neauandKiela,2018),itisneededtosubstantially
i w.o. pre-train”. According to the comparison augmentthebenchmarkssoastoevaluatetheem-
bedding’sperformanceforawidevarietyoftasks.
withBGE-i,thepre-trainedtextencodernotably
improvestheretrievalcapability,whilepreserving OnerepresentativeworkismadebyBEIR(Thakur
similarperformancesonotheraspects. etal.,2021;Kamallooetal.,2023),wheretheem-
beddingscanbeevaluatedacrossdifferentretrieval
| 4 RelatedWork |     |     |     |     |     |     | tasks. ItislaterextendedbyMTEB(Muennighoff |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
etal.,2022a),whereallmajoraspectsoftextem-
| The importance |     | of general |     | text embedding |     | is  |     |     |     |     |     |     |
| -------------- | --- | ---------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
beddingscanbecomprehensivelyevaluated.
| widely recognized,     |     | not                   | only | for its | wide | usage |       |           |           |        |              |     |
| ---------------------- | --- | --------------------- | ---- | ------- | ---- | ----- | ----- | --------- | --------- | ------ | ------------ | --- |
|                        |     |                       |      |         |      |       | Given | the above | analysis, | it can | be concluded |     |
| intypicalapplications, |     | likewebsearchandques- |      |         |      |       |       |           |           |        |              |     |
thatthegeneraltextembeddingishighlyresource-
| tion answering         | (Karpukhin |     | et      | al., 2020) | but | also  |            |       |       |            |       |         |
| ---------------------- | ---------- | --- | ------- | ---------- | --- | ----- | ---------- | ----- | ----- | ---------- | ----- | ------- |
|                        |            |     |         |            |     |       | dependent, | which | calls | for a wide | range | of ele- |
| due to its fundamental |            |     | role in | augmenting |     | large |            |       |       |            |       |         |
ments,suchasdatasets,models,andbenchmarks.
| language models |     | (Lewis | et al., | 2020; | Guu | et al., |     |     |     |     |     |     |
| --------------- | --- | ------ | ------- | ----- | --- | ------- | --- | --- | --- | --- | --- | --- |
Thus,thecreationandpublicreleaseofthecorre-
| 2020; Borgeaud | et  | al., 2022; | Izacard |     | et al., | 2022; |     |     |     |     |     |     |
| -------------- | --- | ---------- | ------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
spondingresourcesiscruciallyimportant.
| Shietal.,2023). | Comparedwiththeconventional |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
task-specificmethods,thegeneraltextembedding
|     |     |     |     |     |     |     | 5 Conclusion |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
needstobeextensivelyapplicableindifferentsce-
narios. Inrecentyears,therehasbeenacontinual We present C-Pack to advance progress towards
effort in this field, where a series of well-known general Chinese embedding. C-Pack consists of
threecoreresources1)ThebenchmarkC-MTEB,
worksareproposed,likeContriever(Izacardetal.,
2021), GTR (Ni et al., 2021b), sentence-T5 (Ni covering 6 major tasks of embeddings and 35
etal.,2021a),Sentence-Transformer(Reimersand datasets,makingitthemostcomprehensivebench-
marktoevaluatethegeneralityofChineseembed-
| Gurevych, 2019),   |     | E5 (Wang     | et  | al., | 2022a), | Ope-   |                                           |     |     |     |     |     |
| ------------------ | --- | ------------ | --- | ---- | ------- | ------ | ----------------------------------------- | --- | --- | --- | --- | --- |
|                    |     |              |     |      |         |        | dings. 2)ThetrainingdataC-MTP,curatedfrom |     |     |     |     |     |
| nAI text embedding |     | (Neelakantan |     |      | et al., | 2022), |                                           |     |     |     |     |     |
etc. Althoughitremainsanopenproblem,recent massiveunlabeledcorporaandhigh-qualitylabeled
studies highlight the following important factors. datasets. Its unprecedented scale, diversity, and
qualitycontributetothesuperiorgeneralityofour
Firstly,thetrainingdataisdesiredtobelarge-scale
anddiversified,fromwhichtheembeddingmodel embeddingmodels. 3)ThemodelsC-TEM,which
can learn to recognize different kinds of seman- areempiricallycompetitive. Theirdifferentsizes
providepeoplewiththeflexibilitytotradeoffeffi-
ticrelationships(Izacardetal.,2021;Wangetal.,
|                    |     |     |             |           |     |     | ciencyandembeddingquality. |     |     | Theentiretraining |     |     |
| ------------------ | --- | --- | ----------- | --------- | --- | --- | -------------------------- | --- | --- | ----------------- | --- | --- |
| 2022b; Neelakantan |     | et  | al., 2022). | Secondly, |     | the |                            |     |     |                   |     |     |
embeddingmodelmustbescaledup,aslargetext recipeisalsoprovidedalongwiththeseresources.
encoders are more generalizable across different ThepublicreleaseofC-Packfacilitatestheusage
ofgeneralChineseembeddingandalsopavesthe
applicationscenarios(Muennighoff,2022;Nietal.,
wayforitsfutureadvancement.
9. huggingface.co/hfl/chinese-roberta-wwm-ext-large

References
|     |     |     |     |     |     | Lespiau, | BogdanDamoc, |     | AidanClark, | etal.2022. |     |
| --- | --- | --- | --- | --- | --- | -------- | ------------ | --- | ----------- | ---------- | --- |
Improvinglanguagemodelsbyretrievingfromtril-
EnekoAgirre,CarmenBanea,ClaireCardie,DanielCer,
|      |             |                  |     |        |      | lionsoftokens. | InInternationalconferenceonma- |     |     |     |     |
| ---- | ----------- | ---------------- | --- | ------ | ---- | -------------- | ------------------------------ | --- | --- | --- | --- |
| Mona | Diab, Aitor | Gonzalez-Agirre, |     | Weiwei | Guo, |                |                                |     |     |     |     |
chinelearning,pages2206–2240.PMLR.
| InigoLopez-Gazpio, |     | MontseMaritxalar, |     | RadaMi- |     |     |     |     |     |     |     |
| ------------------ | --- | ----------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
halcea,etal.2015. Semeval-2015task2: Semantic SamuelRBowman,GaborAngeli,ChristopherPotts,
textualsimilarity,english,spanishandpilotoninter- andChristopherDManning.2015. Alargeannotated
| pretability. | InProceedingsofthe9thinternational |     |     |     |     |                                            |     |     |     |     |       |
| ------------ | ---------------------------------- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | ----- |
|              |                                    |     |     |     |     | corpusforlearningnaturallanguageinference. |     |     |     |     | arXiv |
workshoponsemanticevaluation(SemEval2015),
preprintarXiv:1508.05326.
pages252–263.
|     |     |     |     |     |     | Tom Brown, | Benjamin | Mann, | Nick | Ryder, | Melanie |
| --- | --- | --- | --- | --- | --- | ---------- | -------- | ----- | ---- | ------ | ------- |
EnekoAgirre,CarmenBanea,ClaireCardie,DanielM Subbiah,JaredDKaplan,PrafullaDhariwal,Arvind
Cer,MonaTDiab,AitorGonzalez-Agirre,Weiwei Neelakantan,PranavShyam,GirishSastry,Amanda
Guo, Rada Mihalcea, German Rigau, and Janyce Askell,etal.2020. Languagemodelsarefew-shot
| Wiebe.2014.                |     | Semeval-2014task10: |                   | Multilingual |     |           |                                       |     |     |     |     |
| -------------------------- | --- | ------------------- | ----------------- | ------------ | --- | --------- | ------------------------------------- | --- | --- | --- | --- |
|                            |     |                     |                   |              |     | learners. | Advancesinneuralinformationprocessing |     |     |     |     |
| semantictextualsimilarity. |     |                     | InSemEval@COLING, |              |     |           |                                       |     |     |     |     |
systems,33:1877–1901.
pages81–91.
|     |     |     |     |     |     | Daniel Cer, | Mona Diab, | Eneko | Agirre, | Inigo | Lopez- |
| --- | --- | --- | --- | --- | --- | ----------- | ---------- | ----- | ------- | ----- | ------ |
EnekoAgirre,CarmenBanea,DanielCer,MonaDiab,
|     |     |     |     |     |     | Gazpio, | and Lucia | Specia. | 2017. | Semeval-2017 |     |
| --- | --- | --- | --- | --- | --- | ------- | --------- | ------- | ----- | ------------ | --- |
Aitor Gonzalez Agirre, Rada Mihalcea, German task1: Semantictextualsimilarity-multilingualand
RigauClaramunt,andJanyceWiebe.2016. Semeval- cross-lingual focused evaluation. arXiv preprint
| 2016 task                       | 1:  | Semantic textual | similarity, | monolin-        |     | arXiv:1708.00055. |     |     |     |     |     |
| ------------------------------- | --- | ---------------- | ----------- | --------------- | --- | ----------------- | --- | --- | --- | --- | --- |
| gualandcross-lingualevaluation. |     |                  |             | InSemEval-2016. |     |                   |     |     |     |     |     |
10th International Workshop on Semantic Evalua- JingChen,QingcaiChen,XinLiu,HaijunYang,Daohe
tion;2016Jun16-17;SanDiego,CA.Stroudsburg Lu,andBuzhouTang.2018. Thebqcorpus: Alarge-
(PA):ACL;2016.p.497-511.ACL(Associationfor scale domain-specific chinese corpus for sentence
ComputationalLinguistics). semanticequivalenceidentification. InProceedings
ofthe2018conferenceonempiricalmethodsinnatu-
Eneko Agirre, Daniel Cer, Mona Diab, and Aitor rallanguageprocessing,pages4946–4951.
| Gonzalez-Agirre. |     | 2012. | Semeval-2012 | task | 6: A |     |     |     |     |     |     |
| ---------------- | --- | ----- | ------------ | ---- | ---- | --- | --- | --- | --- | --- | --- |
pilotonsemantictextualsimilarity. In*SEM2012: AakankshaChowdhery,SharanNarang,JacobDevlin,
TheFirstJointConferenceonLexicalandCompu- Maarten Bosma, Gaurav Mishra, Adam Roberts,
tational Semantics–Volume 1: Proceedings of the Paul Barham, Hyung Won Chung, Charles Sutton,
main conference and the shared task, and Volume Sebastian Gehrmann, et al. 2022. Palm: Scaling
2: ProceedingsoftheSixthInternationalWorkshop language modeling with pathways. arXiv preprint
| onSemanticEvaluation(SemEval2012),pages385– |     |     |     |     |     | arXiv:2204.02311. |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- |
393.
|     |     |     |     |     |     | Hyung | Won Chung, | Le Hou, | Shayne | Longpre, | Bar- |
| --- | --- | --- | --- | --- | --- | ----- | ---------- | ------- | ------ | -------- | ---- |
EnekoAgirre,DanielCer,MonaDiab,AitorGonzalez- ret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi
Agirre,andWeiweiGuo.2013. *sem2013shared Wang,MostafaDehghani,SiddharthaBrahma,etal.
task: Semantic textual similarity. In Second joint 2022. Scalinginstruction-finetunedlanguagemodels.
conferenceonlexicalandcomputationalsemantics arXivpreprintarXiv:2210.11416.
| (*SEM),volume1: |     | proceedingsoftheMainconfer- |     |     |     |     |     |     |     |     |     |
| --------------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
enceandthesharedtask: semantictextualsimilarity, AlexisConneauandDouweKiela.2018. Senteval: An
| pages32–43. |        |              |        |                 |     | evaluationtoolkitforuniversalsentencerepresenta- |                                |     |                          |      |     |
| ----------- | ------ | ------------ | ------ | --------------- | --- | ------------------------------------------------ | ------------------------------ | --- | ------------------------ | ---- | --- |
|             |        |              |        |                 |     | tions.                                           | arXivpreprintarXiv:1803.05449. |     |                          |      |     |
| Loubna Ben  | Allal, | Raymond      | Li,    | Denis Kocetkov, |     |                                                  |                                |     |                          |      |     |
|             |        |              |        |                 |     | Jacob Devlin,                                    | Ming-Wei                       |     | Chang, Kenton            | Lee, | and |
| Chenghao    | Mou,   | Christopher  | Akiki, | Carlos Munoz    |     |                                                  |                                |     |                          |      |     |
|             |        |              |        |                 |     | KristinaToutanova.2018.                          |                                |     | Bert: Pre-trainingofdeep |      |     |
| Ferrandis,  | Niklas | Muennighoff, |        | Mayank Mishra,  |     |                                                  |                                |     |                          |      |     |
bidirectionaltransformersforlanguageunderstand-
| AlexGu,MananDey,etal.2023. |     |     |     | Santacoder: | don’t |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ----------- | ----- | --- | --- | --- | --- | --- | --- |
reachforthestars! arXivpreprintarXiv:2301.03988. ing. arXivpreprintarXiv:1810.04805.
AkariAsai,TimoSchick,PatrickLewis,XilunChen, Jack FitzGerald, Christopher Hench, Charith Peris,
Gautier Izacard, Sebastian Riedel, Hannaneh Ha- ScottMackie,KayRottmann,AnaSanchez,Aaron
jishirzi,andWen-tauYih.2022. Task-awareretrieval Nash,LiamUrbach,VisheshKakarala,RichaSingh,
|                   |     |                                |     |     |     | et al. | 2022. Massive:   |               | A 1m-example |         | multilin- |
| ----------------- | --- | ------------------------------ | --- | --- | --- | ------ | ---------------- | ------------- | ------------ | ------- | --------- |
| withinstructions. |     | arXivpreprintarXiv:2211.09260. |     |     |     |        |                  |               |              |         |           |
|                   |     |                                |     |     |     | gual   | natural language | understanding |              | dataset | with      |
Luiz Bonifacio, Vitor Jeronymo, Hugo Queiroz 51typologically-diverselanguages. arXivpreprint
| Abonizio,IsraelCampiotti,MarziehFadaee,Roberto |             |           |       |         |     | arXiv:2204.08582. |     |     |     |     |     |
| ---------------------------------------------- | ----------- | --------- | ----- | ------- | --- | ----------------- | --- | --- | --- | --- | --- |
| Lotufo,                                        | and Rodrigo | Nogueira. | 2021. | mmarco: | A   |                   |     |     |     |     |     |
multilingualversionofthemsmarcopassageranking Leo Gao, Jonathan Tow, Stella Biderman, Sid Black,
dataset. arXivpreprintarXiv:2108.13897. AnthonyDiPofi,CharlesFoster,LaurenceGolding,
|     |     |     |     |     |     | Jeffrey | Hsu, Kyle | McDonell, | Niklas | Muennighoff, |     |
| --- | --- | --- | --- | --- | --- | ------- | --------- | --------- | ------ | ------------ | --- |
Sebastian Borgeaud, Arthur Mensch, Jordan Hoff- JasonPhang,LariaReynolds,EricTang,AnishThite,
mann, Trevor Cai, Eliza Rutherford, Katie Milli- BenWang,KevinWang,andAndyZou.2021a. A
can,GeorgeBmVanDenDriessche,Jean-Baptiste frameworkforfew-shotlanguagemodelevaluation.

Luyu Gao and Jamie Callan. 2021. Condenser: a Association for Computational Linguistics, 7:453–
| pre-training | architecture |     | for | dense | retrieval. | arXiv | 466. |     |     |     |     |     |
| ------------ | ------------ | --- | --- | ----- | ---------- | ----- | ---- | --- | --- | --- | --- | --- |
preprintarXiv:2104.08253.
PatrickLewis,EthanPerez,AleksandraPiktus,Fabio
LuyuGao,YunyiZhang,JiaweiHan,andJamieCallan.
Petroni,VladimirKarpukhin,NamanGoyal,Hein-
| 2021b. | Scaling | deep | contrastive |     | learning | batch    |              |            |     |             |     |          |
| ------ | ------- | ---- | ----------- | --- | -------- | -------- | ------------ | ---------- | --- | ----------- | --- | -------- |
|        |         |      |             |     |          |          | richKüttler, | MikeLewis, |     | Wen-tauYih, |     | TimRock- |
|        |         |      |             |     | arXiv    | preprint |              |            |     |             |     |          |
size under memory limited setup. täschel,etal.2020. Retrieval-augmentedgeneration
arXiv:2101.06983. forknowledge-intensivenlptasks. AdvancesinNeu-
ralInformationProcessingSystems,33:9459–9474.
TianyuGao,XingchengYao,andDanqiChen.2021c.
| Simcse:   | Simplecontrastivelearningofsentenceem- |     |     |     |     |     |                                 |        |            |      |                 |               |
| --------- | -------------------------------------- | --- | --- | --- | --- | --- | ------------------------------- | ------ | ---------- | ---- | --------------- | ------------- |
|           |                                        |     |     |     |     |     | Jingyang                        | Li and | Maosong    | Sun. | 2007.           | Scalable term |
| beddings. | arXivpreprintarXiv:2104.08821.         |     |     |     |     |     |                                 |        |            |      |                 |               |
|           |                                        |     |     |     |     |     | selectionfortextcategorization. |        |            |      | InProceedingsof |               |
|           |                                        |     |     |     |     |     | the 2007                        | Joint  | Conference |      | on Empirical    | Methods       |
KelvinGuu,KentonLee,ZoraTung,PanupongPasu-
inNaturalLanguageProcessingandComputational
| pat,andMingweiChang.2020. |     |     |     | Retrievalaugmented |     |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
NaturalLanguageLearning(EMNLP-CoNLL),pages
| languagemodelpre-training. |     |     |     | InInternationalconfer- |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
774–782.
enceonmachinelearning,pages3929–3938.PMLR.
|         |          |      |             |     |            |       | JingyangLi,MaosongSun,andXianZhang.2006. |     |     |     |     | A   |
| ------- | -------- | ---- | ----------- | --- | ---------- | ----- | ---------------------------------------- | --- | --- | --- | --- | --- |
| Wei He, | Kai Liu, | Jing | Liu, Yajuan |     | Lyu, Shiqi | Zhao, |                                          |     |     |     |     |     |
comparisonandsemi-quantitativeanalysisofwords
| Xinyan | Xiao, | Yuan | Liu, Yizhong |     | Wang, | Hua Wu, |     |     |     |     |     |     |
| ------ | ----- | ---- | ------------ | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
andcharacter-bigramsasfeaturesinchinesetextcat-
| QiaoqiaoShe,etal.2017. |     |     |     | Dureader: | achinesema- |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
chinereadingcomprehensiondatasetfromreal-world egorization. InProceedingsofthe21stInternational
applications. arXivpreprintarXiv:1711.05073. ConferenceonComputationalLinguisticsand44th
AnnualMeetingoftheAssociationforComputational
Jordan Hoffmann, Sebastian Borgeaud, Arthur Men- Linguistics,pages545–552.
| sch, Elena | Buchatskaya, |     | Trevor | Cai, | Eliza | Ruther- |     |     |     |     |     |     |
| ---------- | ------------ | --- | ------ | ---- | ----- | ------- | --- | --- | --- | --- | --- | --- |
ford, Diego de Las Casas, Lisa Anne Hendricks, Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas
Johannes Welbl, Aidan Clark, et al. 2022. Train- Muennighoff,DenisKocetkov,ChenghaoMou,Marc
ingcompute-optimallargelanguagemodels. arXiv Marone,ChristopherAkiki,JiaLi,JennyChim,etal.
preprintarXiv:2203.15556. 2023a. Starcoder: may the source be with you!
arXivpreprintarXiv:2305.06161.
| Hai Hu,                       | Kyle Richardson, |     | Liang | Xu, | Lu Li,         | Sandra |     |     |     |     |     |     |
| ----------------------------- | ---------------- | --- | ----- | --- | -------------- | ------ | --- | --- | --- | --- | --- | --- |
| Kübler,andLawrenceSMoss.2020. |                  |     |       |     | Ocnli:Original |        |     |     |     |     |     |     |
YudongLi,YuqingZhang,ZheZhao,LinlinShen,Wei-
chinesenaturallanguageinference. arXivpreprint jieLiu,WeiquanMao,andHuiZhang.2022. Csl: A
arXiv:2010.05444. large-scalechinesescientificliteraturedataset. arXiv
preprintarXiv:2209.05034.
GautierIzacard,MathildeCaron,LucasHosseini,Se-
| bastian | Riedel, | Piotr | Bojanowski, |     | Armand | Joulin, |     |     |     |     |     |     |
| ------- | ------- | ----- | ----------- | --- | ------ | ------- | --- | --- | --- | --- | --- | --- |
ZehanLi,XinZhang,YanzhaoZhang,DingkunLong,
| andEdouardGrave.2021.                      |     |     |     | Unsuperviseddensein- |     |       |                                   |     |     |     |     |         |
| ------------------------------------------ | --- | --- | --- | -------------------- | --- | ----- | --------------------------------- | --- | --- | --- | --- | ------- |
|                                            |     |     |     |                      |     |       | PengjunXie,andMeishanZhang.2023b. |     |     |     |     | Towards |
| formationretrievalwithcontrastivelearning. |     |     |     |                      |     | arXiv |                                   |     |     |     |     |         |
generaltextembeddingswithmulti-stagecontrastive
preprintarXiv:2112.09118.
|                  |     |         |        |       |         |     | learning. | arXivpreprintarXiv:2308.03281. |     |     |     |     |
| ---------------- | --- | ------- | ------ | ----- | ------- | --- | --------- | ------------------------------ | --- | --- | --- | --- |
| Gautier Izacard, |     | Patrick | Lewis, | Maria | Lomeli, | Lu- |           |                                |     |     |     |     |
XinLiu,QingcaiChen,ChongDeng,HuajunZeng,Jing
| cas Hosseini, |     | Fabio | Petroni, | Timo | Schick, | Jane |                                     |     |     |     |     |        |
| ------------- | --- | ----- | -------- | ---- | ------- | ---- | ----------------------------------- | --- | --- | --- | --- | ------ |
|               |     |       |          |      |         |      | Chen,DongfangLi,andBuzhouTang.2018. |     |     |     |     | Lcqmc: |
Dwivedi-Yu,ArmandJoulin,SebastianRiedel,and
|         |        |       |          |     |          |          | Alarge-scalechinesequestionmatchingcorpus. |     |     |     |     | In  |
| ------- | ------ | ----- | -------- | --- | -------- | -------- | ------------------------------------------ | --- | --- | --- | --- | --- |
| Edouard | Grave. | 2022. | Few-shot |     | learning | with re- |                                            |     |     |     |     |     |
Proceedingsofthe27thinternationalconferenceon
| trievalaugmentedlanguagemodels. |     |     |     |     | arXivpreprint |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
computationallinguistics,pages1952–1962.
arXiv:2208.03299.
Ehsan Kamalloo, Nandan Thakur, Carlos Lassance, YinhanLiu,MyleOtt,NamanGoyal,JingfeiDu,Man-
|                                          |           |            |         |       |              |       | dar Joshi, | Danqi                          | Chen, | Omer        | Levy,     | Mike Lewis,     |
| ---------------------------------------- | --------- | ---------- | ------- | ----- | ------------ | ----- | ---------- | ------------------------------ | ----- | ----------- | --------- | --------------- |
| Xueguang                                 | Ma,       | Jheng-Hong |         | Yang, | and Jimmy    | Lin.  |            |                                |       |             |           |                 |
|                                          |           |            |         |       |              |       | Luke       | Zettlemoyer,                   |       | and Veselin | Stoyanov. | 2019.           |
| 2023.                                    | Resources | for        | brewing | beir: | Reproducible |       |            |                                |       |             |           |                 |
|                                          |           |            |         |       |              |       | Roberta:   | A robustly                     |       | optimized   | bert      | pretraining ap- |
| referencemodelsandanofficialleaderboard. |           |            |         |       |              | arXiv |            |                                |       |             |           |                 |
|                                          |           |            |         |       |              |       | proach.    | arXivpreprintarXiv:1907.11692. |       |             |           |                 |
preprintarXiv:2306.07471.
VladimirKarpukhin,BarlasOg˘uz,SewonMin,Patrick Zheng Liu and Yingxia Shao. 2022. Retromae: Pre-
Lewis,LedellWu,SergeyEdunov,DanqiChen,and trainingretrieval-orientedtransformersviamasked
|             |      |          |            |         |           |          | auto-encoder. |     | arXivpreprintarXiv:2205.12035. |     |     |     |
| ----------- | ---- | -------- | ---------- | ------- | --------- | -------- | ------------- | --- | ------------------------------ | --- | --- | --- |
| Wen-tau     | Yih. | 2020.    | Dense      | passage | retrieval | for      |               |     |                                |     |     |     |
| open-domain |      | question | answering. |         | arXiv     | preprint |               |     |                                |     |     |     |
DingkunLong,QiongGao,KuanZou,GuangweiXu,
arXiv:2004.04906.
|     |     |     |     |     |     |     | Pengjun | Xie, | Ruijie | Guo, Jian | Xu, | Guanjun Jiang, |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---- | ------ | --------- | --- | -------------- |
TomKwiatkowski, JennimariaPalomaki, OliviaRed- LuxiXing,andPingYang.2022. Multi-cpr: Amulti
field,MichaelCollins,AnkurParikh,ChrisAlberti, domainchinesedatasetforpassageretrieval. InPro-
DanielleEpstein,IlliaPolosukhin,JacobDevlin,Ken- ceedingsofthe45thInternationalACMSIGIRCon-
tonLee,etal.2019. Naturalquestions: abenchmark ferenceonResearchandDevelopmentinInformation
forquestionansweringresearch. Transactionsofthe Retrieval,pages3046–3056.

JulianMcAuleyandJureLeskovec.2013. Hiddenfac- YingqiQu,YuchenDing,JingLiu,KaiLiu,Ruiyang
torsandhiddentopics: Understandingratingdimen- Ren, Wayne Xin Zhao, Daxiang Dong, Hua Wu,
sionswithreviewtext. RecSys’13,NewYork,NY, and Haifeng Wang. 2020. Rocketqa: An opti-
USA.AssociationforComputingMachinery. mizedtrainingapproachtodensepassageretrieval
|                     |     |       |     |       |              |     | foropen-domainquestionanswering. |     |     |     |     | arXivpreprint |     |
| ------------------- | --- | ----- | --- | ----- | ------------ | --- | -------------------------------- | --- | --- | --- | --- | ------------- | --- |
| Niklas Muennighoff. |     | 2022. |     | Sgpt: | Gpt sentence |     |                                  |     |     |     |     |               |     |
arXiv:2010.08191.
| embeddings |     | for semantic | search. |     | arXiv | preprint |     |     |     |     |     |     |     |
| ---------- | --- | ------------ | ------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:2202.08904.
|     |     |     |     |     |     |     | Jack W    | Rae, Sebastian |           | Borgeaud, | Trevor  |       | Cai, Katie |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --------- | --------- | ------- | ----- | ---------- |
|     |     |     |     |     |     |     | Millican, | Jordan         | Hoffmann, |           | Francis | Song, | John       |
NiklasMuennighoff,QianLiu,ArmelZebaze,Qinkai
|        |         |       |         |           |        |     | Aslanides, | Sarah | Henderson,   |     | Roman            | Ring, | Susan-  |
| ------ | ------- | ----- | ------- | --------- | ------ | --- | ---------- | ----- | ------------ | --- | ---------------- | ----- | ------- |
| Zheng, | Binyuan | Hui,  | Terry   | Yue Zhuo, | Swayam |     |            |       |              |     |                  |       |         |
|        |         |       |         |           |        |     | nah Young, |       | et al. 2021. |     | Scaling language |       | models: |
| Singh, | Xiangru | Tang, | Leandro | von       | Werra, | and |            |       |              |     |                  |       |         |
Methods,analysis&insightsfromtraininggopher.
| ShayneLongpre.2023a. |     |     | Octopack: |     | Instructiontun- |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:2112.11446.
| ing code | large | language | models. |     | arXiv | preprint |     |     |     |     |     |     |     |
| -------- | ----- | -------- | ------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:2308.07124.
ColinRaffel,NoamShazeer,AdamRoberts,Katherine
Lee,SharanNarang,MichaelMatena,YanqiZhou,
NiklasMuennighoff,AlexanderMRush,BoazBarak,
|     |     |     |     |     |     |     | WeiLi,andPeterJLiu.2020. |     |     |     | Exploringthelimits |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | ------------------ | --- | --- |
TevenLeScao,AleksandraPiktus,NouamaneTazi,
Sampo Pyysalo, Thomas Wolf, and Colin Raffel. oftransferlearningwithaunifiedtext-to-texttrans-
2023b. Scaling data-constrained language models. former. TheJournalofMachineLearningResearch,
21(1):5485–5551.
arXivpreprintarXiv:2305.16264.
NiklasMuennighoff,NouamaneTazi,LoïcMagne,and NilsReimersandIrynaGurevych.2019. Sentence-bert:
Sentenceembeddingsusingsiamesebert-networks.
| NilsReimers.2022a. |     | Mteb: | Massivetextembedding |     |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | ----- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:1908.10084.
| benchmark. |     | arXivpreprintarXiv:2210.07316. |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
NiklasMuennighoff,ThomasWang,LintangSutawika,
VictorSanh,AlbertWebson,ColinRaffel,StephenH
Adam Roberts, Stella Biderman, Teven Le Scao, Bach, Lintang Sutawika, Zaid Alyafeai, Antoine
MSaifulBari,ShengShen,Zheng-XinYong,Hailey Chaffin, Arnaud Stiegler, Teven Le Scao, Arun
Schoelkopf, et al. 2022b. Crosslingual generaliza- Raja, et al. 2021. Multitask prompted training en-
tion through multitask finetuning. arXiv preprint ableszero-shottaskgeneralization. arXivpreprint
| arXiv:2211.01786. |              |     |     |            |      |      | arXiv:2110.08207. |       |        |      |             |     |            |
| ----------------- | ------------ | --- | --- | ---------- | ---- | ---- | ----------------- | ----- | ------ | ---- | ----------- | --- | ---------- |
| Arvind            | Neelakantan, | Tao | Xu, | Raul Puri, | Alec | Rad- |                   |       |        |      |             |     |            |
|                   |              |     |     |            |      |      | Teven Le          | Scao, | Angela | Fan, | Christopher |     | Akiki, El- |
ford,JesseMichaelHan,JerryTworek,QimingYuan,
|     |     |     |     |     |     |     | lie Pavlick, |     | Suzana | Ilic´, | Daniel Hesslow, |     | Roman |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------ | ------ | --------------- | --- | ----- |
NikolasTezak,JongWookKim,ChrisHallacy,etal. Castagné,AlexandraSashaLuccioni,FrançoisYvon,
2022. Textandcodeembeddingsbycontrastivepre- Matthias Gallé, et al. 2022a. Bloom: A 176b-
training. arXivpreprintarXiv:2201.10005. parameteropen-accessmultilinguallanguagemodel.
arXivpreprintarXiv:2211.05100.
TriNguyen,MirRosenberg,XiaSong,JianfengGao,
| Saurabh | Tiwary,  | Rangan                       | Majumder, |     | and Li | Deng. |                |       |        |         |          |          |        |
| ------- | -------- | ---------------------------- | --------- | --- | ------ | ----- | -------------- | ----- | ------ | ------- | -------- | -------- | ------ |
|         |          |                              |           |     |        |       | Teven Le       | Scao, | Thomas | Wang,   | Daniel   | Hesslow, | Lu-    |
| 2016.   | Msmarco: | Ahuman-generatedmachineread- |           |     |        |       |                |       |        |         |          |          |        |
|         |          |                              |           |     |        |       | cile Saulnier, |       | Stas   | Bekman, | M Saiful | Bari,    | Stella |
ingcomprehensiondataset.
Bideman,HadyElsahar,NiklasMuennighoff,Jason
|     |     |     |     |     |     |     | Phang,etal.2022b. |     |     | Whatlanguagemodeltotrain |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | ------------------------ | --- | --- | --- |
JianmoNi,GustavoHernándezÁbrego,NoahConstant,
|        |       |                |     |          |        |       | ifyouhaveonemilliongpuhours? |     |     |     |     | arXivpreprint |     |
| ------ | ----- | -------------- | --- | -------- | ------ | ----- | ---------------------------- | --- | --- | --- | --- | ------------- | --- |
| Ji Ma, | Keith | B Hall, Daniel |     | Cer, and | Yinfei | Yang. |                              |     |     |     |     |               |     |
arXiv:2210.15424.
| 2021a.                             | Sentence-t5: |     | Scalable | sentence | encoders      |     |             |       |      |           |     |           |      |
| ---------------------------------- | ------------ | --- | -------- | -------- | ------------- | --- | ----------- | ----- | ---- | --------- | --- | --------- | ---- |
| frompre-trainedtext-to-textmodels. |              |     |          |          | arXivpreprint |     |             |       |      |           |     |           |      |
|                                    |              |     |          |          |               |     | Weijia Shi, | Sewon | Min, | Michihiro |     | Yasunaga, | Min- |
arXiv:2108.08877.
|                |          |          |        |         |      |         | joon                      | Seo, Rich | James,    | Mike     | Lewis,  | Luke    | Zettle-    |
| -------------- | -------- | -------- | ------ | ------- | ---- | ------- | ------------------------- | --------- | --------- | -------- | ------- | ------- | ---------- |
|                |          |          |        |         |      |         | moyer,andWen-tauYih.2023. |           |           |          | Replug: |         | Retrieval- |
| Jianmo         | Ni, Chen | Qu, Jing | Lu,    | Zhuyun  | Dai, | Gus-    |                           |           |           |          |         |         |            |
|                |          |          |        |         |      |         | augmented                 |           | black-box | language |         | models. | arXiv      |
| tavo Hernández |          | Ábrego,  | Ji Ma, | Vincent |      | Y Zhao, |                           |           |           |          |         |         |            |
preprintarXiv:2301.12652.
| Yi Luan,  | Keith                          | B Hall,       | Ming-Wei |                   | Chang, | et al. |        |             |         |     |          |          |      |
| --------- | ------------------------------ | ------------- | -------- | ----------------- | ------ | ------ | ------ | ----------- | ------- | --- | -------- | -------- | ---- |
| 2021b.    | Large                          | dual encoders |          | are generalizable |        | re-    |        |             |         |     |          |          |      |
|           |                                |               |          |                   |        |        | Aarohi | Srivastava, | Abhinav |     | Rastogi, | Abhishek | Rao, |
| trievers. | arXivpreprintarXiv:2112.07899. |               |          |                   |        |        |        |             |         |     |          |          |      |
AbuAwalMdShoeb,AbubakarAbid,AdamFisch,
YujiaQin,ShihaoLiang,YiningYe,KunlunZhu,Lan Adam R Brown, Adam Santoro, Aditya Gupta,
|     |     |     |     |     |     |     | Adrià | Garriga-Alonso, |     | et  | al. 2022. | Beyond | the |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------------- | --- | --- | --------- | ------ | --- |
Yan,YaxiLu,YankaiLin,XinCong,XiangruTang,
|            |     |           |          |              |     |       | imitation | game: | Quantifying |     | and extrapolating |     | the |
| ---------- | --- | --------- | -------- | ------------ | --- | ----- | --------- | ----- | ----------- | --- | ----------------- | --- | --- |
| Bill Qian, | et  | al. 2023. | Toolllm: | Facilitating |     | large |           |       |             |     |                   |     |     |
languagemodelstomaster16000+real-worldapis. capabilities of language models. arXiv preprint
| arXivpreprintarXiv:2307.16789. |     |     |     |     |     |     | arXiv:2206.04615. |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
YifuQiu,HongyuLi,YingqiQu,YingChen,Qiaoqiao Hongjin Su, Jungo Kasai, Yizhong Wang, Yushi Hu,
She, Jing Liu, Hua Wu, and Haifeng Wang. 2022. MariOstendorf,Wen-tauYih,NoahASmith,Luke
Dureader_retrieval:Alarge-scalechinesebenchmark Zettlemoyer,TaoYu,etal.2022. Oneembedder,any
forpassageretrievalfromwebsearchengine. arXiv task: Instruction-finetunedtextembeddings. arXiv
| preprintarXiv:2203.10232. |     |     |     |     |     |     | preprintarXiv:2212.09741. |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |

Nandan Thakur, Nils Reimers, Andreas Rücklé, Ab- Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Ben-
hishekSrivastava,andIrynaGurevych.2021. Beir: gio,WilliamWCohen,RuslanSalakhutdinov,and
A heterogenous benchmark for zero-shot evalua- ChristopherDManning.2018. Hotpotqa: Adataset
tionofinformationretrievalmodels. arXivpreprint fordiverse,explainablemulti-hopquestionanswer-
arXiv:2104.08663. ing. arXivpreprintarXiv:1809.09600.
James Thorne, Andreas Vlachos, Christos Sha Yuan, Hanyu Zhao, Zhengxiao Du, Ming Ding,
Christodoulopoulos, and Arpit Mittal. 2018. Xiao Liu, Yukuo Cen, Xu Zou, Zhilin Yang, and
Fever: a large-scale dataset for fact extraction and JieTang.2021. Wudaocorpora: Asuperlarge-scale
verification. arXivpreprintarXiv:1803.05355. chinesecorporaforpre-traininglanguagemodels. AI
Open,2:65–68.
LiangWang,NanYang,XiaolongHuang,BinxingJiao,
LinjunYang, DaxinJiang, RanganMajumder, and S. Zhang, X. Zhang, H. Wang, L. Guo, and S. Liu.
FuruWei.2022a. Simlm: Pre-trainingwithrepresen- 2018a. Multi-scaleattentiveinteractionnetworksfor
tationbottleneckfordensepassageretrieval. arXiv chinese medical question answer selection. IEEE
preprintarXiv:2207.02578. Access,6:74061–74071.
Liang Wang, Nan Yang, Xiaolong Huang, Binxing Sheng Zhang, Xin Zhang, Hui Wang, Jiajun Cheng,
Jiao,LinjunYang,DaxinJiang,RanganMajumder, PeiLi,andZhaoyunDing.2017. Chinesemedical
andFuruWei.2022b. Textembeddingsbyweakly- questionanswermatchingusingend-to-endcharacter-
supervisedcontrastivepre-training. arXivpreprint levelmulti-scalecnns. AppliedSciences,7(8):767.
arXiv:2212.03533.
ShengZhang,XinZhang,HuiWang,LixiangGuo,and
Jason Wei, Maarten Bosma, Vincent Y Zhao, Kelvin ShanshanLiu.2018b. Multi-scaleattentiveinterac-
Guu, Adams Wei Yu, Brian Lester, Nan Du, An- tionnetworksforchinesemedicalquestionanswer
drewMDai,andQuocVLe.2021. Finetunedlan- selection. IEEEAccess,6:74061–74071.
guagemodelsarezero-shotlearners. arXivpreprint
arXiv:2109.01652.
Adina Williams, Nikita Nangia, and Samuel R Bow-
man.2017. Abroad-coveragechallengecorpusfor
sentence understanding through inference. arXiv
preprintarXiv:1704.05426.
ShitaoXiao,ZhengLiu,YingxiaShao,andZhaoCao.
2023. Retromae-2: Duplex masked auto-encoder
forpre-trainingretrieval-orientedlanguagemodels.
arXivpreprintarXiv:2305.02564.
XiaohuiXie,QianDong,BingningWang,FeiyangLv,
TingYao,WeinanGan,ZhijingWu,XiangshengLi,
Haitao Li, Yiqun Liu, et al. 2023. T2ranking: A
large-scalechinesebenchmarkforpassageranking.
arXivpreprintarXiv:2304.03679.
LeeXiong,ChenyanXiong,YeLi,Kwok-FungTang,
JialinLiu,PaulBennett,JunaidAhmed,andArnold
Overwijk.2020. Approximatenearestneighborneg-
ative contrastive learning for dense text retrieval.
arXivpreprintarXiv:2007.00808.
Liang Xu, Hai Hu, Xuanwei Zhang, Lu Li, Chenjie
Cao, Yudong Li, Yechen Xu, Kai Sun, Dian Yu,
Cong Yu, et al. 2020a. Clue: A chinese language
understandingevaluationbenchmark. arXivpreprint
arXiv:2004.05986.
Liang Xu, Xuanwei Zhang, and Qianqian Dong.
2020b. Cluecorpus2020: Alarge-scalechinesecor-
pusforpre-traininglanguagemodel. arXivpreprint
arXiv:2003.01355.
Yinfei Yang, Yuan Zhang, Chris Tar, and Jason
Baldridge.2019. Paws-x:Across-lingualadversarial
datasetforparaphraseidentification. arXivpreprint
arXiv:1908.11828.

A C-MTEBDatasets
| Name |     | URL | Description | Categ. | Test |
| ---- | --- | --- | ----------- | ------ | ---- |
Samples
Classification
AmazonReviewsClassification https://hf.co/datasets/mteb/ Sentiment of Ama- s2s 5,000
| (Muennighoff | et al., 2022a; | amazon_reviews_multi | zonreviews |     |     |
| ------------ | -------------- | -------------------- | ---------- | --- | --- |
| McAuley      | and Leskovec,  |                      |            |     |     |
2013)
| IFlyTek(Xuetal.,2020a) |     |     | Long text | classifi- s2s | 2,600 |
| ---------------------- | --- | --- | --------- | ------------- | ----- |
https://hf.co/
|     |     | datasets/C-MTEB/       | cation for | App de- |     |
| --- | --- | ---------------------- | ---------- | ------- | --- |
|     |     | IFlyTek-classification | scriptions |         |     |
JDReview (https://hf.co/ https://hf.co/ iPhonereviews s2s 533
| datasets/kuroneko5943/jd21) |     | datasets/C-MTEB/ |     |     |     |
| --------------------------- | --- | ---------------- | --- | --- | --- |
JDReview-classification
MassiveIntentClassification https://hf.co/datasets/mteb/ Amazon Alexa s2s 16,500
(Muennighoff et al., 2022a; amazon_massive_intent virtual assistant ut-
| FitzGeraldetal.,2022) |     |     | terances | annotated |     |
| --------------------- | --- | --- | -------- | --------- | --- |
with the associated
intent
MassiveScenarioClassification https://hf.co/datasets/mteb/ Amazon Alexa s2s 16,500
(Muennighoff et al., 2022a; amazon_massive_scenario virtual assistant ut-
| FitzGeraldetal.,2022) |     |     | terances | annotated |     |
| --------------------- | --- | --- | -------- | --------- | --- |
with the associated
scenario
MultilingualSentiment https://hf.co/ Sentiment of Ama- s2s 3,000
| (McAuley | and Leskovec, | datasets/C-MTEB/                     | zonreviews |     |     |
| -------- | ------------- | ------------------------------------ | ---------- | --- | --- |
| 2013)    |               | MultilingualSentiment-classification |            |     |     |
OnlineShopping (https: https://hf.co/ SentimentAnalysis s2s 1,000
| //github.com/SophonPlus/ |     | datasets/C-MTEB/ | of User | Reviews |     |
| ------------------------ | --- | ---------------- | ------- | ------- | --- |
ChineseNlpCorpus/blob/ OnlineShopping-classification onOnlineShopping
| master/datasets/online_ |     |     | Websites |     |     |
| ----------------------- | --- | --- | -------- | --- | --- |
shopping_10_cats/intro.
ipynb)
TNews(Xuetal.,2020a) https://hf.co/datasets/ Short Text Classifi- s2s 10,000
|     |     | C-MTEB/TNews-classification | cationforNews |     |     |
| --- | --- | --------------------------- | ------------- | --- | --- |
Waimai (https://github.com/ https://hf.co/ SentimentAnalysis s2s 1,000
SophonPlus/ChineseNlpCorpus/ datasets/C-MTEB/ of user reviews on
takeawayplatforms
| blob/master/datasets/waimai_ |     | waimai-classification |     |     |     |
| ---------------------------- | --- | --------------------- | --- | --- | --- |
10k/intro.ipynb)
Clustering

| CLSClusteringP2P(Lietal., |     |     | Clustering | of titles p2p | 10,000 |
| ------------------------- | --- | --- | ---------- | ------------- | ------ |
https://hf.co/datasets/
| 2022) |     | C-MTEB/CLSClusteringP2P | +abstractfromCLS |            |     |
| ----- | --- | ----------------------- | ---------------- | ---------- | --- |
|       |     |                         | dataset.         | Clustering |     |
of13sets,basedon
themaincategory.
CLSClusteringS2S(Lietal., https://hf.co/datasets/ Clustering of titles s2s 10,000
| 2022) |     | C-MTEB/C-MTEB/   | from CLS    | dataset. |     |
| ----- | --- | ---------------- | ----------- | -------- | --- |
|       |     | CLSClusteringS2S | Clustering  | of 13    |     |
|       |     |                  | sets, based | on the   |     |
maincategory.
ThuNewsClusteringP2P (Li https://hf.co/datasets/ Clustering of titles p2p 10,000
etal.,2006;LiandSun,2007) C-MTEB/ThuNewsClusteringP2P + abstract from the
THUCNewsdataset
ThuNewsClusteringS2S (Li https://hf.co/datasets/ Clustering of titles s2s 10,000
| etal.,2006;LiandSun,2007) |     |     | from | the THUC- |     |
| ------------------------- | --- | --- | ---- | --------- | --- |
C-MTEB/ThuNewsClusteringS2S
Newsdataset
PairClassification
| Cmnli (Xu | et al., 2020a,b; |     | Chinese | Multi- s2s | 139,000 |
| --------- | ---------------- | --- | ------- | ---------- | ------- |
https://hf.co/datasets/
| Conneau | and Kiela, | 2018; C-MTEB/CMNLI | GenreNLI |     |     |
| ------- | ---------- | ------------------ | -------- | --- | --- |
Williamsetal.,2017)
Ocnli(Huetal.,2020) https://hf.co/datasets/ Original Chinese s2s 3,000
|     |     | C-MTEB/OCNLI | Natural | Language |     |
| --- | --- | ------------ | ------- | -------- | --- |
Inferencedataset
Reranking
T2Reranking (Xie et al., https://hf.co/datasets/ T2Ranking: A s2p 24,382
| 2023) |     |     | large-scaleChinese |     |     |
| ----- | --- | --- | ------------------ | --- | --- |
C-MTEB/T2Reranking
|     |     |     | Benchmark | for |     |
| --- | --- | --- | --------- | --- | --- |
PassageRanking
MMarcoRetrieval(Bonifacio https://hf.co/datasets/ mMARCOisamul- s2p 7,437
| etal.,2021) |     | C-MTEB/Mmarco-reranking | tilingual | version of |     |
| ----------- | --- | ----------------------- | --------- | ---------- | --- |
|             |     |                         | the MS    | MARCO      |     |
|             |     |                         | passage   | ranking    |     |
dataset
CMedQAv1 (Zhang et al., https://hf.co/datasets/ Chinesecommunity s2p 2,000
| 2017) |     | C-MTEB/CMedQAv1-reranking | medical | question |     |
| ----- | --- | ------------------------- | ------- | -------- | --- |
answering
| CMedQAv2 | (Zhang | et al., | Chinesecommunity | s2p | 4,000 |
| -------- | ------ | ------- | ---------------- | --- | ----- |
https://hf.co/datasets/
| 2018b) |     | C-MTEB/C-MTEB/     | medical   | question |     |
| ------ | --- | ------------------ | --------- | -------- | --- |
|        |     | CMedQAv2-reranking | answering |          |     |
Retrieval

| T2Retrieval(Xieetal.,2023) |     |     | T2Ranking: | A s2p | 24,832 |
| -------------------------- | --- | --- | ---------- | ----- | ------ |
https://hf.co/datasets/
|     |     | C-MTEB/T2Retrieval | large-scaleChinese |     |     |
| --- | --- | ------------------ | ------------------ | --- | --- |
|     |     |                    | Benchmark          | for |     |
PassageRanking
MMarcoRetrieval(Bonifacio https://hf.co/datasets/ mMARCOisamul- s2p 7,437
| etal.,2021) |     | C-MTEB/MMarcoRetrieval | tilingual version | of      |     |
| ----------- | --- | ---------------------- | ----------------- | ------- | --- |
|             |     |                        | the MS MARCO      |         |     |
|             |     |                        | passage           | ranking |     |
dataset
| DuRetrieval(Qiuetal.,2022) |     |     | A Large-scale | Chi- s2p | 4,000 |
| -------------------------- | --- | --- | ------------- | -------- | ----- |
https://hf.co/datasets/
|     |     | C-MTEB/DuRetrieval | neseBenchmarkfor  |        |     |
| --- | --- | ------------------ | ----------------- | ------ | --- |
|     |     |                    | Passage Retrieval |        |     |
|     |     |                    | from Web          | Search |     |
Engine
| CovidRetrieval | (Qiu et al., |     | COVID-19newsar- | s2p | 949 |
| -------------- | ------------ | --- | --------------- | --- | --- |
https://hf.co/datasets/
| 2022) |     | C-MTEB/CovidRetrieval | ticles |     |     |
| ----- | --- | --------------------- | ------ | --- | --- |
CmedqaRetrieval (Qiu et al., https://hf.co/datasets/ Onlinemedicalcon- s2p 3,999
| 2022) |     | C-MTEB/CmedqaRetrieval | sultationtext |     |     |
| ----- | --- | ---------------------- | ------------- | --- | --- |
EcomRetrieval (Long et al., https://hf.co/datasets/ Passage retrieval s2p 1,000
| 2022) |     | C-MTEB/EcomRetrieval | dataset collected |         |     |
| ----- | --- | -------------------- | ----------------- | ------- | --- |
|       |     |                      | from              | Alibaba |     |
|       |     |                      | search            | engine  |     |
|       |     |                      | systems           | in e-   |     |
commercedomain
| MedicalRetrieval(Longetal., |     |     | Passage | retrieval s2p | 1,000 |
| --------------------------- | --- | --- | ------- | ------------- | ----- |
https://hf.co/datasets/
| 2022) |     | C-MTEB/MedicalRetrieval | dataset collected |         |     |
| ----- | --- | ----------------------- | ----------------- | ------- | --- |
|       |     |                         | from              | Alibaba |     |
|       |     |                         | search            | engine  |     |
systemsinmedical
domain
VideoRetrieval (Long et al., https://hf.co/datasets/ Passage retrieval s2p 1,000
| 2022) |     | C-MTEB/VideoRetrieval | dataset collected |         |     |
| ----- | --- | --------------------- | ----------------- | ------- | --- |
|       |     |                       | from              | Alibaba |     |
|       |     |                       | search            | engine  |     |
|       |     |                       | systems in        | video   |     |
domain
STS
AFQMC(Xuetal.,2020a) https://hf.co/datasets/ AntFinancialQues- s2s 3,861
|     |     | C-MTEB/AFQMC | tion Matching | Cor- |     |
| --- | --- | ------------ | ------------- | ---- | --- |
pus
ATEC (https://github.com/ https://hf.co/datasets/ ATEC NLP sen- s2s 20,000
| IceFlameWorm/NLP_Datasets/ |     | C-MTEB/ATEC | tencepairsimilarity |     |     |
| -------------------------- | --- | ----------- | ------------------- | --- | --- |
| tree/master/ATEC)          |     |             | competition         |     |     |
BQ(Chenetal.,2018) https://hf.co/datasets/ Bank Question Se- s2s 10,000
|     |     | C-MTEB/BQ | manticSimilarity |     |     |
| --- | --- | --------- | ---------------- | --- | --- |

| LCQMC(Liuetal.,2018) |     |     |     | A   | large-scale | s2s 12,500 |
| -------------------- | --- | --- | --- | --- | ----------- | ---------- |
https://hf.co/datasets/
|     |     | C-MTEB/LCQMC |     | Chinese | question |     |
| --- | --- | ------------ | --- | ------- | -------- | --- |
matchingcorpus.
PAWSX(Yangetal.,2019) https://hf.co/datasets/ Translated PAWS s2s 2,000
|     |     | C-MTEB/PAWSX |     | evaluationpairs |     |     |
| --- | --- | ------------ | --- | --------------- | --- | --- |
QBQTC(Xuetal.,2020a) https://hf.co/datasets/ QQBrowserQuery s2s 5,000
|                     |     | C-MTEB/QBQTC |     | TitleCorpus |       |           |
| ------------------- | --- | ------------ | --- | ----------- | ----- | --------- |
| STSB(Ceretal.,2017) |     |              |     | Translate   | STS-B | s2s 1,360 |
https://hf.co/datasets/
|     |     | C-MTEB/STSB |     | intoChinese |     |     |
| --- | --- | ----------- | --- | ----------- | --- | --- |
STS-22 (Muennighoff et al., https://hf.co/datasets/mteb/ Chinesenews p2p 656
| 2022a) |         | sts22-crosslingual-sts      |     |     |     |     |
| ------ | ------- | --------------------------- | --- | --- | --- | --- |
|        | Table5: | OverviewofdatasetsinC-MTEB. |     |     |     |     |
B C-MTPComposition
Weminelarge-scalepairsofdatafromvariousdomains. Table6showsthedetailsforeachdata.
| datasource | typeoftextpairs |     | #ofpairs |     | URL |     |
| ---------- | --------------- | --- | -------- | --- | --- | --- |
https:
| cmrc2018 | (query,context) |     | 9,669 |     |     |     |
| -------- | --------------- | --- | ----- | --- | --- | --- |
//huggingface.co/datasets/cmrc2018
dureader (query,context) 96,486 https://github.com/baidu/DuReader
https:
| simclue | (sentence | a ,sentence ) | 388,779 |                                    |     |     |
| ------- | --------- | ------------- | ------- | ---------------------------------- | --- | --- |
|         |           | b             |         | //github.com/CLUEbenchmark/SimCLUE |     |     |
csl (title,abstract) 394,846 https://arxiv.org/abs/2209.05034
https://huggingface.co/datasets/
| amazon_reviews_multi |     | (title,body) | 157,762 |     |     |     |
| -------------------- | --- | ------------ | ------- | --- | --- | --- |
amazon_reviews_multi
https://huggingface.co/datasets/wiki_
| wiki_atomic_edits | (sentence,editedsentence) |     | 1,213,688 |     |     |     |
| ----------------- | ------------------------- | --- | --------- | --- | --- | --- |
atomic_edits
mlqa (question,context) 70,594 https://huggingface.co/datasets/mlqa
https://huggingface.co/datasets/
| xlsum | (title,summary)(title,text) |     | 89,505 |     |     |     |
| ----- | --------------------------- | --- | ------ | --- | --- | --- |
csebuetnlp/xlsum
https://data.baai.ac.cn/details/
| wudao | (title,passage) |     | 37,318,330 |     |     |     |
| ----- | --------------- | --- | ---------- | --- | --- | --- |
WuDaoCorporaText
| Misc |     | –   | 60,260,341 |     | –   |     |
| ---- | --- | --- | ---------- | --- | --- | --- |
Table6: Detailsforeachdataset. TheMiscdatacomesfromtheInternet,includingQA,paper,andnewsdata.
C EnglishModels
Usingourrecipe,wealsotrainasetofEnglishtextembeddingmodelspresentedinTable7. Atthetime
ofwriting,ourEnglishBGEmodelsarestate-of-the-artontheEnglishMTEBbenchmark(Muennighoff
etal.,2022a)acrossits56datasets. Ourmodelsoutperformsignificantlylargermodels,suchasSGPT
Bloomwhichhas7.1billionparameters(Muennighoff,2022;Scaoetal.,2022a,b). Weadvancetheprior
state-of-the-artbyanabsolute1.1(Lietal.,2023b). OurtrainingrecipeisthesameasforourChinese
models,exceptfortheusageofEnglishdata. Wefirstfinetuneonunsuperviseddatasetsincludingdatasets
likeWikipedia,CC-net,StackExchange,Reddit,S2orc,anddatasetsfromsentence-transformers.10 We
thenfurtherfine-tuneonsuperviseddatasetsincludingNLI(Gaoetal.,2021c),FEVER(Thorneetal.,
2018),NQ(Kwiatkowskietal.,2019),HotpotQA(Yangetal.,2018),Quora,StackExchangeDuplicates
andMEDI(Suetal.,2022).
10. https://huggingface.co/datasets/sentence-transformers/embedding-training-data

ModelName Dim. Average Retrieval Cluster PairCLF Re-rank STS Summarize CLF
BGE(large) 1024 64.23 54.29 46.08 87.12 60.03 83.11 31.61 75.97
| BGE(base) | 768 63.55 | 53.25 45.77 | 86.55 58.86 | 82.4 31.07 | 75.53 |
| --------- | --------- | ----------- | ----------- | ---------- | ----- |
BGE(small) 384 62.17 51.68 43.82 84.92 58.36 81.59 30.12 74.14
GTE(large) 1024 63.13 52.22 46.84 85.00 59.13 83.35 31.66 73.33
| GTE(base) | 768 62.39 | 51.14 46.2 | 84.57 58.61 | 82.3 31.17 | 73.01 |
| --------- | --------- | ---------- | ----------- | ---------- | ----- |
E5(large) 1024 62.25 50.56 44.49 86.03 56.61 82.05 30.19 75.24
Instructor-XL 768 61.79 49.26 44.74 86.62 57.29 83.06 32.32 61.79
| E5(base) | 768 61.5 | 50.29 43.80 | 85.73 55.91 | 81.05 30.28 | 73.84 |
| -------- | -------- | ----------- | ----------- | ----------- | ----- |
GTE(small) 384 61.36 49.46 44.89 83.54 57.7 82.07 30.42 72.31
OpenAIAda002 1536 60.99 49.25 45.9 84.89 56.32 80.97 30.8 70.93
E5(small) 384 59.93 49.04 39.92 84.67 54.32 80.39 31.16 72.94
| ST5(XXL) | 768 59.51 | 42.24 43.72 | 85.06 56.42 | 82.63 30.08 | 73.42 |
| -------- | --------- | ----------- | ----------- | ----------- | ----- |
MPNet(base) 768 57.78 43.81 43.69 83.04 59.36 80.28 27.49 65.07
SGPTBloom(7.1B) 4096 57.59 48.22 38.93 81.9 55.65 77.74 33.60 66.19
|     | Table7: PerformanceofEnglishModelsonMTEB. |     |     |     |     |
| --- | ----------------------------------------- | --- | --- | --- | --- |