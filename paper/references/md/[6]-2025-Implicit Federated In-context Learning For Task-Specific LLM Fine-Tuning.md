Implicit Federated In-context Learning For Task-Specific LLM Fine-Tuning
DongchengLi1,JunhanChen1,AoxiangZhou1,ChunpeiLi1,YouquanXian2,PengLiu1,Xianxian
LI1
1KeyLabofEducationBlockchainandIntelligentTechnology,MinistryofEducation,GuangxiNormalUniversity,Guilin,
Guangxi541004,China
2SchoolofCyberspaceSecurity,BeijingUniversityofPostsandTelecommunications,Beijing100876,China
5202 voN 01  ]GL.sc[  1v75760.1152:viXra Abstract widespread adoption of LLMs has permeated various do-
mains,includingintelligentdialoguesystems,creativewrit-
As large language models continue to develop and expand, ingassistance,medicaldiagnosissupport,scientificresearch
the extensive public data they rely on faces the risk of de- acceleration,andpersonalizededucation.Theseapplications
| pletion. | Consequently, | leveraging |     | private | data within | orga- |     |     |     |     |     |     |     |
| -------- | ------------- | ---------- | --- | ------- | ----------- | ----- | --- | --- | --- | --- | --- | --- | --- |
notonlyenhanceefficiencyandinnovationbutalsoprovide
| nizations | to enhance | the performance |     | of  | large models | has |     |     |     |     |     |     |     |
| --------- | ---------- | --------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
emergedasakeychallenge.Thefederatedlearningparadigm, new tools for addressing the complex challenges faced by
| combinedwithmodelfine-tuningtechniques,effectivelyre- |     |     |     |     |     |     | humanity. |     |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
duces the number of trainable parameters. However,the ne- As the parameters and functionalities of LLMs continue
cessitytoprocesshigh-dimensionalfeaturespacesresultsin to grow,their rate of data consumption is also increasing
| substantial | overall | computational |     | overhead. | To address | this |                  |      |       |               |     |           |       |
| ----------- | ------- | ------------- | --- | --------- | ---------- | ---- | ---------------- | ---- | ----- | ------------- | --- | --------- | ----- |
|             |         |               |     |           |            |      | rapidly. Studies | have | shown | that publicly |     | available | high- |
issue,weproposetheImplicitFederatedIn-ContextLearning
|     |     |     |     |     |     |     | quality textual | data | is expected | to  | be exhausted | between |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ---- | ----------- | --- | ------------ | ------- | --- |
(IFed-ICL)framework.IFed-ICLdrawsinspirationfromfed-
|     |     |     |     |     |     |     | 2026 and | 2032 (Ye | et al. | 2024). Reusing |     | existing | datasets |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | ------ | -------------- | --- | -------- | -------- |
eratedlearningtoestablishanoveldistributedcollaborative
|           |               |        |       |         |          |      | not only | limits the | upper | bound of | model | performance | but |
| --------- | ------------- | ------ | ----- | ------- | -------- | ---- | -------- | ---------- | ----- | -------- | ----- | ----------- | --- |
| paradigm, | by converting | client | local | context | examples | into |          |            |       |          |       |             |     |
alsorisksoverfittingandreducesthemodel’sgeneralization
implicitvectorrepresentations,itenablesdistributedcollab-
orative computation during the inference phase and injects ability. According to a survey conducted by Epoch AI, the
model residual streams to enhance model performance. Ex- totalglobalvolumeoftextualdataisapproximately31tril-
periments demonstrate that our proposed method achieves lion tokens, with publicly available data comprising only a
outstanding performance across multiple text classification small fraction. In contrast, private data, which is often of
tasks.Comparedtotraditionalmethods,IFed-ICLavoidsthe higherqualityandmoredomain-specific,hasemergedasthe
| extensive | parameter | updates | required | by  | conventional | fine- |     |     |     |     |     |     |     |
| --------- | --------- | ------- | -------- | --- | ------------ | ----- | --- | --- | --- | --- | --- | --- | --- |
newfrontierforbreakthroughsinmodelperformance(Jones
| tuning methods |     | while reducing | data | transmission |     | and local |     |     |     |     |     |     |     |
| -------------- | --- | -------------- | ---- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
2024).Asaresult,FederatedLearning(FL)hasemergedasa
computationattheclientlevelinfederatedlearning.Thisen-
highlyattractivesolution,enablinguserstosupplementlarge
ablesefficientdistributedcontextlearningusinglocalprivate-
|     |     |     |     |     |     |     | models with | knowledge |     | derived from | privately | held | data |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --------- | --- | ------------ | --------- | ---- | ---- |
domaindata,significantlyimprovingmodelperformanceon
throughcollaborativemulti-partytraining.Thisapproachef-
specifictasks.
|     |     |     |     |     |     |     | fectively | enhances | the reasoning | capabilities |     | of LLMs | for |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ------------- | ------------ | --- | ------- | --- |
specifictasks.
|           |        | Introduction          |     |     |       |          | Toimprovetheperformanceoffoundationmodelsonspe- |          |           |              |          |             |       |
| --------- | ------ | --------------------- | --- | --- | ----- | -------- | ----------------------------------------------- | -------- | --------- | ------------ | -------- | ----------- | ----- |
|           |        |                       |     |     |       |          | cific tasks,                                    | two main | paradigms | have         | emerged: | fine-tuning |       |
| In recent | years, | the rapid development |     | of  | Large | Language |                                                 |          |           |              |          |             |       |
|           |        |                       |     |     |       |          | and In-Context                                  | Learning |           | (ICL) (Brown | et       | al. 2020).  | Fine- |
Models(LLMs)hasbroughtaboutarevolutionarytransfor-
|           |           |               |               |     |       |        | tuning approaches |     | include | full fine-tuning |     | and parameter- |     |
| --------- | --------- | ------------- | ------------- | --- | ----- | ------ | ----------------- | --- | ------- | ---------------- | --- | -------------- | --- |
| mation in | the field | of artificial | intelligence. |     | These | models |                   |     |         |                  |     |                |     |
efficientfine-tuningmethodssuchasLoRA(Huetal.2022)
havenotonlypushedtheboundariesoftechnologybutalso
|     |     |     |     |     |     |     | and P-Tuning-v2(Liu |     | et  | al. 2021). | In contrast, | In-Context |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ---------- | ------------ | ---------- | --- |
reshapedthefundamentalparadigmofhuman-computerin-
|     |     |     |     |     |     |     | Learning | is a training-free |     | approach | that | guides the | model |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------ | --- | -------- | ---- | ---------- | ----- |
teraction.Trainedonmassivetextualdatasetsandbuiltupon
toperformspecifictasksbyprovidingafewexamplesdur-
deepneuralnetworkarchitectures,modelssuchastheGPT
inginference,significantlyloweringthebarriertoentryfor
| series, LLaMA, |     | and PaLM | have | demonstrated |     | unprece- |     |     |     |     |     |     |     |
| -------------- | --- | -------- | ---- | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
taskadaptation.
| dented capabilities |     | in language     | understanding |                |         | and gener- |                |     |          |              |         |      |        |
| ------------------- | --- | --------------- | ------------- | -------------- | ------- | ---------- | -------------- | --- | -------- | ------------ | ------- | ---- | ------ |
|                     |     |                 |               |                |         |            | To effectively |     | leverage | high-quality | private | data | within |
| ation, surpassing   |     | the limitations |               | of traditional | natural | lan-       |                |     |          |              |         |      |        |
guageprocessingapproaches.Asthenumberofparameters organizations, recent studies (Peng et al. 2024; Wu et al.
2024a)haveproposedcombiningFLwithfine-tuningtech-
hasscaledfrombillionstohundredsofbillions,LLMshave
niques.Whilefederatedfine-tuningcanadaptLLMtodown-
| exhibited      | remarkable | emergent | abilities,  |                | such | as reason- |               |             |          |       |            |     |        |
| -------------- | ---------- | -------- | ----------- | -------------- | ---- | ---------- | ------------- | ----------- | -------- | ----- | ---------- | --- | ------ |
|                |            |          |             |                |      |            | stream tasks, | it requires | updating | model | parameters |     | within |
| ing, planning, | coding,    | and      | cross-modal | understanding. |      | The        |               |             |          |       |            |     |        |
high-dimensionalfeaturespaces,leadingtosignificantcom-
Copyright©2026,AssociationfortheAdvancementofArtificial putationaloverhead.Consequently,thedeploymentofFed-
Intelligence(www.aaai.org).Allrightsreserved. eratedLargeLanguageModels(FedLLMs)facessubstantial

challengesinpractice.Onesignificantbarrieristhecommu- constraineddevices.
| nication | cost. For | instance, | transmitting |     | the parameters | of  |     |     |     |     |     |     |
| -------- | --------- | --------- | ------------ | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
• Extensiveexperimentsacrossmultipletextclassification
LLaMA3.1-405B over a 100 Mbps network would require tasks demonstrate that, compared to federated parame-
morethan36hours,whichfarexceedsthecapacityofcon- ter fine-tuning, IFed-ICL reduces clients computational
| temporary                                        | communication |     | systems. | On  | the other hand, | ap- |          |                  |      |                |               |     |
| ------------------------------------------------ | ------------- | --- | -------- | --- | --------------- | --- | -------- | ---------------- | ---- | -------------- | ------------- | --- |
|                                                  |               |     |          |     |                 |     | overhead | by more          | than | 20 times and   | communication |     |
| proachesbasedonICL(Wuetal.2024b;Zhangetal.2024b) |               |     |          |     |                 |     |          |                  | 104  |                |               |     |
|                                                  |               |     |          |     |                 |     | costs    | by approximately |      | times, thereby | ensuring      | the |
involvecollectingexamplesfrommultipleclientsandincor-
feasibilityoflarge-scalefederateddeployment.
poratingthemintotheinferenceprompt.However,thisfun-
damentally violates the principle of data locality in feder- RelatedWork
| ated learning | and | poses | a serious | risk of | sensitive | informa- |                      |     |     |     |     |     |
| ------------- | --- | ----- | --------- | ------- | --------- | -------- | -------------------- | --- | --- | --- | --- | --- |
| tionleakage.  |     |       |           |         |           |          | FederatedFine-Tuning |     |     |     |     |     |
To address the limitations of ICL, (Li et al. 2024) offers FL is a distributed machine learning paradigm that enables
anovelperspectivebyconvertingcontextualexamplesinto multiple clients to collaboratively train a global model by
vectorrepresentationsandinjectingthemintoLLMstoper- exchangingmodelparameterswithoutexposingtheirrawlo-
form inference tasks. This work provides valuable inspira- cal data(McMahan et al. 2017; Konecˇny` et al. 2016; Yang
| tion for   | our research. | Building | upon     | it,       | we propose | a col- |               |                |                |                |      |          |
| ---------- | ------------- | -------- | -------- | --------- | ---------- | ------ | ------------- | -------------- | -------------- | -------------- | ---- | -------- |
|            |               |          |          |           |            |        | et al. 2019). | Its primary    | goal           | is to mitigate | the  | systemic |
| laborative | framework     | named    | Implicit | Federated | In-Context |        |               |                |                |                |      |          |
|            |               |          |          |           |            |        | privacy       | risks inherent | in traditional | centralized    | data | col-     |
Learning,whichaimstotacklethedualchallengesofcom- lection (Kairouz et al. 2021). In recent years, LLMs have
putational inefficiency in traditional federated fine-tuning achieved remarkable breakthroughs in performance. How-
and the limited collaborative capacity of conventional ICL. ever,thescaleofpubliclyavailabledatasetshasapproached
Unlike traditional FL paradigms that require extensive lo- itslimit,andfurtherdevelopmentofthesemodelsisincreas-
caltrainingonclientdevices,ourapproachinnovativelyde-
inglyconstrainedbythechallengeof”datasilos”(Villalobos
composes the federated process into two parts: the extrac- etal.2022).FederatedLargeLanguageModels(FedLLMs)
tionofcontextvectorsandthecollaborativecomputationof (Chenetal.2023)havebeenproposedinthiscontext,aim-
injectioncoefficients.Thissignificantlyreducesthecompu- ing to combine the powerful generalization capabilities of
tationalburdenonlocalclients. LLMswiththeprivacy-preservingadvantagesofFL.
We implement efficient collaboration through a three- Nevertheless,theimplementationofFedLLMscontinues
stageprocess.Inthefirststage,eachparticipatingclientde- to face formidable challenges. When the number of model
signstask-specificcontexttemplates,convertslocaldatainto parametersreachesthescaleofbillions,full-parameterfine-
context vectors, and sends them to the server for aggrega- tuning of LLMs results in massive communication over-
tion. In the second stage, the server returns the aggregated head,whichseverelylimitstheirscalabilityinpracticalde-
global context vectors to each client, where clients com- ployments (Shu et al. 2024). To address this, Parameter-
pute the perplexity loss using their local data to calibrate Efficient Fine-tuning (PEFT) has become the mainstream
the injection coefficients. These coefficients are then sent optimization pattern (Hu et al. 2024). The core idea is to
back to the server for aggregation. After several rounds of freeze the majority of the LLM’s parameters and fine-tune
iterative optimization, the injection coefficients are refined only a small set of newly added or selectively chosen pa-
toensureoptimalintegrationofcontextualinformationinto
|     |     |     |     |     |     |     | rameters, | thereby reducing |     | the computational, | storage, | and |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------------- | --- | ------------------ | -------- | --- |
theLLM.Finally,inthethirdstage,theserverdistributesthe communicationburdenonclientdevices.TheFedPETuning
calibratedcoefficientstoclients,whichcanthenconvertthe framework (Zhang et al. 2023) was among the earliest to
rawLLMintoatask-specificLLMwithasinglelinearinjec- systematicallyincorporatemultiplePEFTmethods(includ-
tion operation. This design not only reduces computational ingLoRA)intoFLsettings,demonstratingthefeasibilityof
andcommunicationoverheadbutalsoachievesaneffective
|     |     |     |     |     |     |     | significantly | lowering | communication | costs | by aggregating |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | -------- | ------------- | ----- | -------------- | --- |
decouplingofdatautilizationandmodeltraining,offeringa onlyasmallportionoftrainableparameters.
new paradigm for distributed AI collaboration in resource- Beyond LoRA and its variants, other PEFT strategies
constrainedenvironments.Themaincontributionsofthispa- havealsoprovideddiverseandefficientfine-tuningpathsfor
perareasfollows: FedLLMs.Inadapter-basedmethods,FedAdapter(Caietal.
2022)enhancestrainingefficiencybydynamicallyconfigur-
| • we propose | a          | novel | federated | ICL paradigm. | Instead   | of  |              |                |     |                     |       |      |
| ------------ | ---------- | ----- | --------- | ------------- | --------- | --- | ------------ | -------------- | --- | ------------------- | ----- | ---- |
|              |            |       |           |               |           |     | ing adapters | and leveraging |     | activation caching, | while | FeD- |
| synthesizing | contextual |       | data,     | our method    | transmits | and |              |                |     |                     |       |      |
eRA(Yanetal.2024)initializeslow-rankadaptersviasin-
| aggregates | context | vectors, | which | are | then injected | dur- |             |               |       |            |             |     |
| ---------- | ------- | -------- | ----- | --- | ------------- | ---- | ----------- | ------------- | ----- | ---------- | ----------- | --- |
|            |         |          |       |     |               |      | gular value | decomposition | (SVD) | to improve | performance |     |
ingthemodelinferencephasetoenhanceperformance.
|     |     |     |     |     |     |     | under Non-IID | data | distributions. | Prompt-based |     | methods |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ---- | -------------- | ------------ | --- | ------- |
• In contrast to traditional FL, our approach decomposes havegainedsignificantattentionduetotheirextremelylow
thefederatedprocessintotwocomponents:contextvec- communication overhead. For example, FedPepTAO (Che
toraggregationandinjectioncoefficienttraining.Clients et al. 2023) achieves efficient fine-tuning through partial
are responsible for converting local data into context prompt tuning and dual-end adaptive optimization. Addi-
vectors and performing lightweight training of injec- tionally, some selective PEFT methods, such as BitFit (Za-
tioncoefficients.Thisdesignsignificantlyreducescom- ken, Ravfogel, and Goldberg 2021), which only fine-tunes
munication bandwidth requirements and computational bias parameters, and FedAMoLE (Zhang et al. 2024a),
overhead,enablingeffectiveparticipationfromresource- whichbuildsmixturesofLoRAexpertsforhighlyheteroge-

neous scenarios, demonstrate strong potential in improving personalization while avoiding the direct sharing of sensi-
bothpersonalizationandefficiency. tive data. Methods such as (Wu et al. 2024b; Zhang et al.
Furthermore, Federated Knowledge Distillation (FKD) 2024b) combine the context learning capabilities of LLMs
offers an alternative approach to reducing communication withFLbyhavingserversandclientsshareLLM-generated
overhead by allowing clients to transmit compact repre- synthetic data, allowing clients to fine-tune using locally
sentations of knowledge instead of full model parameters. private datasets. (Wang et al. 2025) achieves efficient and
For instance, AdaFedSelecKD (Feng et al. 2024) adopts low-overhead learning for question-answering tasks in dis-
adapter-based selective knowledge distillation to improve tributed environments by applying ICL using high-quality
communicationefficiency.Thesecommunicationoptimiza- local data at each client, and employing a parameter-free
tiontechniquesarenotmutuallyexclusivewithPEFTmeth- communication strategy. However, these approaches com-
ods.Despiteaseriesofadvancementsinefficientparameter monlyassumeaninfinitecontextwindow,overlookingtrun-
tuning, the process fundamentally relies on executing gra- cation bias and exemplar overflow effects caused by token
dientupdatesandbackpropagationwithinhigh-dimensional limits,whichresultsinsignificantperformancedegradation
parameter spaces. Consequently, the reduction in computa- inlong-sequencescenarios.
tionaloverheadisinherentlyconstrainedbytheupperlimit
ofthetrainablerank.
ProposedFramework
In-ContextLearning
|     |     |     |     |     |     |     |     | In this section, | we  | present | the workflow | of  | IFed-ICL. | As  |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------- | ------------ | --- | --------- | --- |
Compared to parameter fine-tuning,which requires explic- illustrated in Figure 1, the overall collaborative framework
itly updating model weights via backpropagation,ICL en- ofIFed-ICLisdividedintothreekeystages.
| ables LLMs   | to            | adapt to | new tasks | during | inference |           | simply |             |     |     |     |     |     |     |
| ------------ | ------------- | -------- | --------- | ------ | --------- | --------- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
| by providing | demonstration |          | examples, |        | without   | modifying |        | SystemSetup |     |     |     |     |     |     |
anymodelparameters.Thisopensupanewlightweightde-
|          |         |           |     |           |     |             |     | In IFed-ICL, | the system |     | consists of | K clients | and | a cen- |
| -------- | ------- | --------- | --- | --------- | --- | ----------- | --- | ------------ | ---------- | --- | ----------- | --------- | --- | ------ |
| ployment | pathway | for LLMs. |     | The study | by  | (Von Oswald |     |              |            |     |             |           |     |        |
et al. 2023) reveals that the Transformer architecture can tral server. The server maintains both a conventional stor-
implicitlysimulategradientdescentdynamicsduringinfer- age database and a vector database to store task-related in-
|     |     |     |     |     |     |     |     | formation | and aggregated |     | context vectors. | Each | client | pos- |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | ---------------- | ---- | ------ | ---- |
ence,offeringkeyinsightsintotheunderlyingmechanismof
|                       |     |        |     |         |     |         |       | sessesitsownprivatedatasetD |     |     | andapre-trainedLLMM. |     |     |     |
| --------------------- | --- | ------ | --- | ------- | --- | ------- | ----- | --------------------------- | --- | --- | -------------------- | --- | --- | --- |
| ICL. Complementarily, |     | (Wies, |     | Levine, | and | Shashua | 2023) |                             |     |     | k                    |     |     |     |
Basedontherequirementsofaspecifictask,theserverde-
providesarigoroustheoreticalperspectivebasedonProba-
blyApproximatelyCorrectlearningtheory,emphasizingthe finesacontextexampletemplateT anddistributesittothe
decisive impact of context example quality on ICL perfor- clients. Each client then uses the template to label relevant
|                                                   |     |     |     |     |     |     |     | data from | its local | private  | dataset D | as context      | examples |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --------- | --------- | -------- | --------- | --------------- | -------- | --- |
| manceandlayingafoundationalframeworkforsubsequent |     |     |     |     |     |     |     |           |           |          |           | k               |          |     |
|                                                   |     |     |     |     |     |     |     | E = {(s   | ,o )}N    | ,where(s | ,o        | )denotesthej-th |          |     |
| methodologicalinnovations.                        |     |     |     |     |     |     |     | k         | k,j k,j   | j= k 1   | k,j       | k,j             |          |     |
In the domain of ICL optimization, the empirical study input-output pair and N k is the number of examples gen-
by (Agarwal et al. 2024) demonstrates that increasing the erated by client k. The ultimate goal is to leverage these
numberofin-contextexamplesinitiallyimprovesmodelper- private context examples from multiple clients to collabo-
rativelyenhancethelargemodel’srepresentationalcapacity
formanceonopen-endedtasks.(Bertschetal.2024)further
andgeneralizationability.
| investigates | the | model’s    | capacity | to        | utilize | extended | con-    |     |     |     |     |     |     |     |
| ------------ | --- | ---------- | -------- | --------- | ------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| text windows |     | containing | numerous | examples. |         | To       | address |     |     |     |     |     |     |     |
the limitation of context window length, (Ye et al. 2023) Phase1:ContextVectorExtractionandUpload
| proposes              | a retrieval-augmented |            |      | approach      | that | dynamically  |     |                                                  |         |             |          |               |                |       |
| --------------------- | --------------------- | ---------- | ---- | ------------- | ---- | ------------ | --- | ------------------------------------------------ | ------- | ----------- | -------- | ------------- | -------------- | ----- |
|                       |                       |            |      |               |      |              |     | At the beginning                                 | of      | each        | round of | collaboration | in             | IFed- |
| selects task-relevant |                       | exemplars, |      | significantly |      | enhancing    | in- |                                                  |         |             |          |               |                |       |
|                       |                       |            |      |               |      |              |     | ICL,theserverandtheselectedparticipatingclientsk |         |             |          |               |                | ∈ K   |
| ference               | accuracy.             | However,   | such | strategies    |      | rely heavily | on  |                                                  |         |             |          |               |                |       |
|                       |                       |            |      |               |      |              |     | first perform                                    | forward | propagation | using    | the           | large language |       |
theprecisionoftheretrievalsystemandinevitablyintroduce
|     |     |     |     |     |     |     |     | modelMoneachdemonstrationexample(s |     |     |     |     | ,o  | ).Dur- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | --- | ------ |
additionalarchitecturalcomplexity.(Huangetal.2024)ex- k,j k,j
plores techniques for compressing multiple examples into ingthisprocess,thecontextexamplesareusedatthetoken
positionsrequiredforpredictionineachlayerofthemodel
| compact             | latent    | representations, |            | thereby | reducing   | inference   |      |            |              |            |          |            |            |     |
| ------------------- | --------- | ---------------- | ---------- | ------- | ---------- | ----------- | ---- | ---------- | ------------ | ---------- | -------- | ---------- | ---------- | --- |
|                     |           |                  |            |         |            |             |      | to extract | intermediate | activation | vectors. | These      | activation |     |
| costs and           | improving | performance      |            | in      | multimodal | ICL         | set- |            |              |            |          |            |            |     |
|                     |           |                  |            |         |            |             |      | vectors    | include the  | outputs    | from the | Multi-Head | Attention  |     |
| tings. Nonetheless, |           | practical        | deployment |         | is         | constrained | by   |            |              |            |          |            |            |     |
(MHA)andMulti-LayerPerceptron(MLP)modulesacross
| the requirement |     | to access | internal | model | states. | (Hendel, |     |     |     |     |     |     |     |     |
| --------------- | --- | --------- | -------- | ----- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Geva, and Globerson 2023) conceptualizes the transforma- allLTransformerlayers.LettheMHAandMLPactivations
tionofmultiplein-contextexamplesintoasingletaskvec- extractedfromthel-thlayerofexamples bedenotedas
k,j
|                                                        |     |     |     |     |     |     |     | ae and   | me , respectively. |     | These         | layer-wise | activations |         |
| ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | -------- | ------------------ | --- | ------------- | ---------- | ----------- | ------- |
| tortoguidemodelinference,therebysimplifyingtraditional |     |     |     |     |     |     |     | k,j,l    | k,j,l              |     |               |            |             |         |
|                                                        |     |     |     |     |     |     |     | are then | fused to form      | the | demonstration | vector     | for         | the ex- |
explicitexampleenumeration.Expandingonthislineofre-
| search,(Lietal.2024)injectstask-relevantcontextdirectly |     |     |     |     |     |     |     | ample: |     |     |     |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
into intermediate activation layers of the model. This strat- d′ ={ae ,me }L
(1)
egy significantly reduces reliance on long contexts and im- k,j k,j,l k,j,l l=1
provescomputationalefficiency. Finally, the server and client k compute the arith-
InFLscenarios,ICLcanbeleveragedtoenhancemodel metic mean of all locally generated demonstration vectors

Server
1 egatS
Clinet 1CClileienntt
Client
3
egatS
Client 0
{Task,Index}
#4. Text: {text1} Category: {category1} Input
Server Private Template #1 # . 2 T # . e 3 T x . e t T : x { e t: t x e { t x : t e t { 1 x t } e t 1 x C } t 1 a C t } e a C g te o a g r t y e o g : r y o { : c r y a { : c t e a { g c te o a g r te o y g r 1 o y } r 1 y } 1}
Database Retrieval dataset
LLM
Cached Task model Insuffcient Local Data Vector Extract Task
Request +
Extract
Demonstration MLP Layer’s
Vectors Context
+ Vector
Vector Database {Task,Global Vector} Arithmetic ATTN
Mean
Cached Global Aggregation Context Calibration opitimize
vector Context Vector Vector ※ +
Suffcient Data Transport Inject C La o y n e te r x ’s t MLP
※ Perplexity Vector ※ +
Calibration Coefficients n-Epochs Itretation Loss ATTN
Global
Optimize Context Vector Inject ※ Inject ※
Raw Task-Specific
Raw Task-Specific Calibration Coefficients LLM LLM
LLM LLM
2 egatS
：Trainable ※：Linear Combination
Figure 1: Overall of IFed-ICL framework.First stage: Each client extracts vector representations from its private dataset D
k
andtransmitsthemtotheserverforaggregation.Secondstage:ClientscollaborativelycalibratetheinjectioncoefficientsΛby
minimizingtheperplexitylossontheirlocaldataincoordinationwiththeserver.Thirdstage:Thetrainedinjectioncoefficients
andtheaggregatedglobalcontextvectorareutilizedtoenablein-contextlearningforthelargelanguagemodel.
{d′ }Nk toobtainthelocalcontextvectorv : The client first initializes the hyperparameters Λ and uses
k,j j=1 k k
the local dataset E to optimize and calibrate the injection
1 (cid:88)
Nk
coefficientsofthec
k
ontextvector.Foreachcalibrationsam-
v = d′ (2)
k N k,j ple(xk,yk)∈Dk,theclientfeedsitintothemodelMand
k i i
j=1 performs layer-wise forward propagation. Assume that for
wheretheaveragingisperformedelement-wiseacrosseach thequeryxk,theMHAandMLPactivationsatlayerl and
i
dimensionofthevectors.Aftergeneratingv k ,theclientup- token position τ are denoted as ak and mk respectively.
l,τ l,τ
loads it to the central server. Since v is a compact vector
k Then,theupdatedresidualstreamafterinjectionrk is:
representation,itssizeissignificantlyreducedcomparedto l,τ
theoriginaldataorlarge-scalemodelparameters. rk ←rk +(λa(ae)t +βaak )+(λm(me)t +βmmk ) (5)
l,τ l−1,τ l l g l l,τ l l g l l,τ
Subsequently,allclientsperformnroundsofjointtrain-
Stage2:GlobalContextVectorAggregationand
ingwiththeserver,optimizingtheinjectioncoefficientsΛ
k
CoefficientCalibration
byminimizingtheperplexitylossonthecalibrationdataset
Afterreceivingthelocalcontextvectorsvt fromallpartic- D .
k k
ipating clients k ∈ K , the central server first aggregates
t
thesevectorstoformaglobalcontextvectorvt.Theaggre-  
gationmethodadoptsFederatedAveraging: g Λ(n) =argmin  − (cid:88) logP(yk|xk,v ,Λ )  (6)
k i i g k
Λ  
vt = 1 (cid:88) vt (3) (xk i ,y i k)∈Dk
g |K | k Uponreceivingthelocalinjectioncoefficientsfromallpar-
t
k∈Kt ticipatingclients,theserveraggregatesthemtocomputethe
Letthecorrespondingcomponentsofthel-thlayerMHA
globalinjectioncoefficients.Λ(n):
andMLPoftheglobalcontextvectorvt bedenotedas(ae)t g
g l g
and(me l )t g . Λ(n+1) = 1 (cid:88) K Λ(n) (7)
By configuring a set of hyperparameters Λ, the model’s g K k
residual stream during inference can be injected with con- k=1
textual information to achieve the goal of in-context learn- After receiving the global injection coefficients returned
ing. bytheserver,eachclientusesEquation6toiterativelycom-
Λ={λa,βa,λm,βm}L (4) puteΛ(n).Afterniterations,thetrainingiscompleted.This
l l l l l=1 k

optimization process only targets the injection coefficients News(Chatterjeeetal.2019).Exceptforthezero-shotbase-
Λ, whose number is significantly smaller than that of the line,whichisevaluatedusingonly500testsamplestoassess
LLM parameters. For the global context vector, only a sin- the model’s inherent capabilities, all other experiments uti-
gle round of aggregation is required. Furthermore, this ap- lize5,000trainingsamplesand500testsamplesfromeach
proachcanadapttoincrementaldatascenarios,whereonly dataset.
the incremental context vectors need to be aggregated over Tosimulatethecommonlyobservednon-independentand
multiple rounds, and this can be computed in parallel with identically distributed (Non-IID) nature of federated learn-
thecalibrationofinjectioncoefficients. ing, we partition the training data across 10 clients using
a Dirichlet distribution with a concentration parameter of
Stage3:GlobalCalibrationCoefficientsInjection α = 0.5. We compare IFed-ICL against several represen-
tativebaselines:
Aftercalibrationiscompleted,thecentralserverdistributes
Zero-Shot:servingasareferenceforthemodel’srawper-
the optimized injection coefficients Λ∗ obtained in the cur-
g formance;
rent round to all participating clients. Upon receiving Λ∗,
g Local ICL (Brown et al. 2020): which simulates a non-
eachclientappliesittotheirlocalLLMM.Whennewin-
collaborativescenariowhereeachclientperformsinference
ferencequeriesarrive,theclient’sLLMperformscontextin-
independentlyusinglocaldata;
jection according to Equation 5 using v and Λ∗. Through
g g FedAvg-LoRA(Huetal.2022):arepresentativemethod
thissinglelinearinjectionoperation,therawLLMistrans-
of parameter-efficient fine-tuning (PEFT) in federated set-
formedintoatask-specificLLMtailoredforspecificscenar-
tings,whereclientsfine-tuneLoRAweightsthatareaggre-
ios,withoutrequiringanylocalparameterfine-tuningorgra-
gatedviafederatedaveragingontheserver.
dient computations. This design effectively decouples data
Zero-shot performance serves as a baseline for evaluat-
utilizationfrommodeltraining,significantlyreducingcom-
ingtheinherenttaskcapabilitiesofLLMswithoutanytask-
putational and communication overhead on the client side,
specificadaptation.TohighlightthevalueofFederatedICL,
while also addressing the issue of token length limitations
wedesigncomparativeexperimentsbuiltuponthisbaseline.
in long context inputs. It thus provides a novel paradigm
In contrast to the traditional paradigm of federated learn-
fordistributedAIcollaborationinresource-constraineden-
inginPEFT,whichreliesonexchangingmodelparameters,
vironments.
weintroducethreecomparativebaselinestodemonstratethe
Application Optimization: We designed two types of superiorityofourproposedframework.Allserver-sidecom-
databasestoenhancetaskprocessingefficiencyandresource putationsareexecutedonasingleNVIDIAA100GPU.
utilization.Thefirsttypeisaserverdatabase,suchasMon-
goDB, which is utilized to store task-related information ExperimentalDesign
alongwiththeircorrespondingcalibrationcoefficients.The
IFed-ICLisdesignedtoaddresskeychallengesinfederated
secondtypeisavectordatabase,suchasElasticsearch,de-
large language models related to performance, efficiency,
signedtostoreglobalcontextvectors.Byestablishingatask
and collaborative adaptation. We evaluate its effectiveness
vectorindex,thesimilaritysearchprocessissignificantlyre-
throughthefollowingaspects:
ducedcomparedtotraditionalRetrieval-AugmentedGener-
Performance Comparison: We compare the task accu-
ation(RAG)systems.Specifically,uponreceivinganewtask
racyofIFed-ICLagainstseveralbaselines,includingZero-
request,theserverfirstqueriesthetaskindextoretrievethe
Shot, Local ICL, and a representative parameter-efficient
associated task information and calibration coefficients. If
federatedfine-tuningmethod,FedAvg-LoRA.Thecoreob-
the task has been previously cached, the server directly re-
jective is to assess whether our training-free federated
trievesthecalibratedcoefficientsandthecorrespondingcon-
paradigm can achieve competitive or superior performance
textvectorfromthedatabases.Otherwise,theservercollects
relativetocomputationallyintensivefine-tuningapproaches.
sufficient data and performs an n-epoch iterative training
System Efficiency Evaluation: This aspect focuses on
processtoobtainatask-specificLLM.Duringthisprocess,
the practical deployability of the framework. We quanti-
the server also updates the calibration coefficients and the
tatively compare the communication overhead (in KB per
globalcontextvector,storingthenewlygenerateddatainto
round) and the total client-side computation time (in sec-
the respective databases for efficient future retrieval. This
onds) per federated round, demonstrating IFed-ICL’s suit-
cachingmechanismeffectivelyreducesredundantcomputa-
ability for deployment in resource-constrained environ-
tion and significantly accelerates task response time, form-
ments.
ingaclosed-loopoptimizationsystem.
Impact of Federated Aggregation on Injection Coef-
ficient Performance: This analysis evaluates the effective-
Experiments ness of federated aggregation in producing a global injec-
tioncoefficientfromclients’locallycalibratedcoefficients.
ExperimentalSetup
Specifically,wecomparetheperformanceoftheglobalco-
To comprehensively evaluate the effectiveness of our pro- efficient obtained via aggregation with that of locally opti-
posed IFed-ICL framework, we conduct rigorous experi- mized coefficients used independently by each client. The
mentsusingtwoLLMs,LLaMA-3-8BandQwen2.5-7Bon goal is to quantitatively demonstrate that federated aggre-
three widely used text classification datasets: SUBJ (Pang gationcaneffectivelyintegratediverselocalknowledge,re-
and Lee 2004), Emotion (Chatterjee et al. 2019), and AG sultinginasuperiorinjectioncoefficientthatenhancesboth

Table1:CommunicationoverheadofFedAvg-LoRAandIFed-ICLontheSUBJdataset.
|     | Method |     |     | Direction     |     | FedAvg-LoRA |     | IFed-ICL             |     |     |     |     |     |
| --- | ------ | --- | --- | ------------- | --- | ----------- | --- | -------------------- | --- | --- | --- | --- | --- |
|     |        |     |     | Client→Server |     | 0KB         |     | 514KB(contextvector) |     |     |     |     |     |
Initialization
Server→Client 13357.78KB 515.8KB(contextvector+calibrationcoefficients)
Training(perround) Client↔Server 13357.78KB 1.8KB(calibrationcoefficients)
modelperformanceandgeneralization. Table 3: Running time (seconds) of Llama-3-8B and
Qwen2.5-7BonSUBJ,Emotion,andAGNews.
| Table | 2: Performance |     | comparison |     | of Llama-3-8B |     | and |     |     |     |     |     |     |
| ----- | -------------- | --- | ---------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Qwen2.5-7BontheSUBJ,Emotion,andAGNewsdatasets. Runningtime(s)
|     |     |     |     |     |     |     |     | Dataset | Method |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------ | --- | --- | --- | --- |
Accuracy(acc)andF1-scorearereportedinpercentage(%)
|         |        |     |     |            |     |            |     |     |           |     | Llama-3-8B |       | Qwen2.5-7B |
| ------- | ------ | --- | --- | ---------- | --- | ---------- | --- | --- | --------- | --- | ---------- | ----- | ---------- |
|         |        |     |     |            |     |            |     |     | Zero-Shot |     |            | 30.14 | 29.44      |
|         |        |     |     | Llama-3-8B |     | Qwen2.5-7B |     |     |           |     |            |       |            |
| Dataset | Method |     |     |            |     |            |     |     | LocalICL  |     |            | 45.74 | 45.31      |
SUBJ
|     |           |     | acc(%) | f1(%) |     | acc(%) | f1(%) |     | FedAvg-LoRA |     | 27637.48 |        | 14945.92 |
| --- | --------- | --- | ------ | ----- | --- | ------ | ----- | --- | ----------- | --- | -------- | ------ | -------- |
|     | Zero-Shot |     | 62.60  | 62.48 |     | 62.60  | 62.48 |     | IFed-ICL    |     |          | 670.25 | 530.99   |
|     | LocalICL  |     | 70.00  | 66.90 |     | 70.80  | 67.90 |     |             |     |          |        |          |
SUBJ
|     | FedAvg-LoRA |     | 66.00 | 64.58 |     | 66.00 | 64.58 |     | Zero-Shot |     |     | 28.92 | 57.74 |
| --- | ----------- | --- | ----- | ----- | --- | ----- | ----- | --- | --------- | --- | --- | ----- | ----- |
|     | IFed-ICL    |     | 91.20 | 90.67 |     | 81.20 | 80.66 |     | LocalICL  |     |     | 40.82 | 84.19 |
Emotion
|     |           |     |       |       |     |       |       |     | FedAvg-LoRA |     | 28168.84 |        | 14043.47 |
| --- | --------- | --- | ----- | ----- | --- | ----- | ----- | --- | ----------- | --- | -------- | ------ | -------- |
|     | Zero-Shot |     | 52.20 | 53.51 |     | 52.20 | 53.52 |     |             |     |          |        |          |
|     |           |     |       |       |     |       |       |     | IFed-ICL    |     |          | 809.73 | 1298.17  |
|     | LocalICL  |     | 49.82 | 50.42 |     | 49.70 | 50.30 |     |             |     |          |        |          |
Emotion
|     | FedAvg-LoRA |     | 54.60 | 54.89 |     | 54.60 | 54.89 |     | Zero-Shot |     |     | 27.90 | 56.45  |
| --- | ----------- | --- | ----- | ----- | --- | ----- | ----- | --- | --------- | --- | --- | ----- | ------ |
|     | IFed-ICL    |     | 67.40 | 65.85 |     | 60.80 | 59.32 |     |           |     |     |       |        |
|     |             |     |       |       |     |       |       |     | LocalICL  |     |     | 54.02 | 112.20 |
AGNews
Zero-Shot 82.40 80.06 82.40 82.04 FedAvg-LoRA 30046.70 13719.66
|     | LocalICL |     | 75.00 | 74.70 |     | 74.90 | 74.70 |     | IFed-ICL |     |     | 973.62 | 867.55 |
| --- | -------- | --- | ----- | ----- | --- | ----- | ----- | --- | -------- | --- | --- | ------ | ------ |
AGNews
|     | FedAvg-LoRA |     | 79.00 | 78.58 |     | 80.00 | 79.60 |                  |     |              |     |     |                 |
| --- | ----------- | --- | ----- | ----- | --- | ----- | ----- | ---------------- | --- | ------------ | --- | --- | --------------- |
|     | IFed-ICL    |     | 91.60 | 89.57 |     | 90.60 | 90.53 |                  |     |              |     |     |                 |
|     |             |     |       |       |     |       |       | of communication | and | computation. |     | In  | terms of commu- |
PerformanceComparison nication, IFed-ICL exhibits a decisive advantage. As de-
|     |     |     |     |     |     |     |     | tailed in | Table 1, during |     | the core | training | phase, IFed- |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --------------- | --- | -------- | -------- | ------------ |
As shown in Table 2, our proposed IFed-ICL significantly ICL requires only 1.8 KB of communication per round to
outperformsallbaselinemethodsacrossallevaluatedtasks. transmit a lightweight injection coefficient, while FedAvg-
| Notably, | on AG | News, | FedAvg-LoRA |     | underperforms |     | even |     |     |     |     |     |     |
| -------- | ----- | ----- | ----------- | --- | ------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
LoRAneedstoexchangeapproximately13.08MBofLoRA
| compared | to Local | ICL | and | Zero-Shot. | This | can | be at- |     |     |     |     |     |     |
| -------- | -------- | --- | --- | ---------- | ---- | --- | ------ | --- | --- | --- | --- | --- | --- |
weightmatrices.Evenaccountingfortheone-timetransmis-
| tributed | to its reliance |     | on client-specific |     | fine-tuning |     | using |                 |         |        |                |     |                |
| -------- | --------------- | --- | ------------------ | --- | ----------- | --- | ----- | --------------- | ------- | ------ | -------------- | --- | -------------- |
|          |                 |     |                    |     |             |     |       | sion of context | vectors | during | initialization |     | (approximately |
localdata.Duetodataheterogeneity,suchlocaladaptation 514KB),ourmethodremainshighlyefficient.
| may lead | to overfitting |     | on certain | clients, |     | thus degrading |     |      |                 |     |              |     |                  |
| -------- | -------------- | --- | ---------- | -------- | --- | -------------- | --- | ---- | --------------- | --- | ------------ | --- | ---------------- |
|          |                |     |            |          |     |                |     | From | the perspective | of  | computation, |     | IFed-ICL further |
theoverallperformance.Incontrast,ICLandZero-Shotap-
improvesefficiencybyrestrictingbackpropagationtoamin-
| proaches | primarily | leverage |     | global knowledge |     | and | exhibit |     |     |     |     |     |     |
| -------- | --------- | -------- | --- | ---------------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
imalsetofinjectioncoefficients,therebysignificantlyreduc-
strongergeneralizationtothetargettask,makingthemmore
|        |         |                |     |                |     |     |           | ing client-side | complexity. |     | As shown | in Table | 3, IFed-ICL |
| ------ | ------- | -------------- | --- | -------------- | --- | --- | --------- | --------------- | ----------- | --- | -------- | -------- | ----------- |
| robust | to data | heterogeneity. |     | By aggregating |     | and | injecting |                 |             |     |          |          |             |
achieves20–30timesfastercomputationspeedsonaverage,
| context | vectors, | our proposed |     | method | effectively |     | mitigates |     |     |     |     |     |     |
| ------- | -------- | ------------ | --- | ------ | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- |
andupto41.22timesinthebestcasecomparedtoFedAvg-
theadverseeffectsofnon-IIDdata,therebyachievingsupe-
LoRA.WhileIFed-ICLtakesslightlylongerthanZero-Shot
riorperformance.
andLocalICL.Moreover,IFed-ICLprovidesthedualben-
|     |     |     |     |     |     |     |     | efits of privacy | preservation |     | and performance |     | enhancement |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | ------------ | --- | --------------- | --- | ----------- |
EfficiencyandCommunicationEvaluation
underafederatedlearningsetting,unlikeZero-ShotandLo-
In terms of system efficiency, we compare the communi- cal ICL, which are more suitable for standalone or trusted
cation and clients computation overhead of IFed-ICL with environments and are difficult to deploy in real-world fed-
|                |     |      |          |              |     |          |     | erated scenarios. | Thus, | thecomputational |     |     | costof IFed-ICL |
| -------------- | --- | ---- | -------- | ------------ | --- | -------- | --- | ----------------- | ----- | ---------------- | --- | --- | --------------- |
| the mainstream |     | PEFT | baseline | FedAvg-LoRA. |     | Communi- |     |                   |       |                  |     |     |                 |
canbeconsideredanecessaryandacceptabletrade-offinthe
| cation | overhead | is defined | as  | the total | amount | of  | data (in |     |     |     |     |     |     |
| ------ | -------- | ---------- | --- | --------- | ------ | --- | -------- | --- | --- | --- | --- | --- | --- |
kilobytes, KB) each client uploads to the server per round. privacy–performancebalance.
Clientscomputationoverheadreferstothetotaltime(insec- ThecoreinnovationofIFed-ICLliesinexchangingonlya
onds)requiredtocompleteonelocaltaskperround. smallnumberoflow-dimensionalscalarcoefficients,rather
Tables 1 and 3 present the efficiency comparison be- thanfull-scalemodelweights.Thisdrasticallyreducesboth
tween IFed-ICL and FedAvg-LoRA from the perspectives communication and computation burdens. Such a property

      * O R E D O  $ F F X U D F \              * O R E D O  $ F F X U D F \              * O R E D O  $ F F X U D F \       
 & O L H Q W  $ F F X U D F \       & O L H Q W  $ F F X U D F \       & O L H Q W  $ F F X U D F \
|      |            |     |          |     |     |     |     |      |     |     |     |
| -------- | ---------- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
|          |       |     |      |     |     |     |     |          |     |     |     |
 \ F D U X F F $  O H G R 0                        \ F D U X F F $  O H G R 0        \ F D U X F F $  O H G R 0     
|     |            |            |          |       |     |                 |     |      |     |     |            |
| --- | ---------- | ---------- | -------- | ---------- | --- | ------------------------------ | --- | -------- | --- | --- | ---------- |
|     |       |       |      |            |     |                                |     |          |     |     |       |
                                 
                                   
|      |     |            |          |     |       |            |     |             |                      |            |            |
| -------- | --- | ---------- | -------- | --- | ---------- | ---------- | --- | ----------- | -------------------- | -------------------- | ---------- |
|          |     |            |      |     |       |            |     |         |                      |                      |            |
|          |     |            |          |     |            |            |     |         |            |                      |            |
|      |     |       |      |     |            |            |     |             |                      |                 |       |
|          |     |            |          |     |            |       |     |         |                      |                      |            |
|      |     |            |      |     |            |            |     |         |                      |                      |            |
 & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W     & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W     & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   & O L H Q W   
|     |  & O L H Q W  , ' |     |     |            |  & O L H Q W  , ' |     |     |     |         |  & O L H Q W  , ' |     |
| --- | ------------------ | --- | --- | ---------- | ------------------ | --- | --- | --- | ------- | ------------------ | --- |
|     | (a)AGNews          |     |     | (b)Emotion |                    |     |     |     | (c)SUBJ |                    |     |
Figure2:Performancecomparisonbetweenlocalandglobalinjectioncoefficients.Thefigureshowstheaccuracyofeachclient
whenusingitslocallyoptimizedcoefficientversusthegloballyaggregatedcoefficientobtainedthroughfederatedaveraging.
|       |  3 H D N        |     |      |     |     |                        |     |      |     |     |                        |
| ---------- | ---------------------- | --- | -------- | --- | --- | ---------------------- | --- | -------- | --- | --- | ---------------------- |
|            |                        |     |      |     |     |  3 H D N        |     |          |     |     |  3 H D N        |
|       |                        |     |          |     |     |                        |     |      |     |     |                        |
    
 \ F D U X F F $  O H G R 0  \ F D U X F F $  O H G R 0  \ F D U X F F $  O H G R 0     
|       |     |     |      |     |     |     |     |          |     |     |     |
| ---------- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
|            |     |     |      |     |     |     |     |      |     |     |     |
     
|     |     |     |      |     |     |     |     |      |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
    
|       |     |     |     |     |     |     |     |      |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
    
       * O R E D O  0 R G H O  $ F F X U D F \  * O R E D O  0 R G H O  $ F F X U D F \       * O R E D O  0 R G H O  $ F F X U D F \
 3 H D N  $ F F X U D F \       3 H D N  $ F F X U D F \  3 H D N  $ F F X U D F \
|     |     |     |      |     |     |     |     |      |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
                                                        
 ) H G H U D W H G  / H D U Q L Q J  5 R X Q G  ) H G H U D W H G  / H D U Q L Q J  5 R X Q G  ) H G H U D W H G  / H D U Q L Q J  5 R X Q G
|     | (a)AGNews |     |     | (b)Emotion |     |     |     |     | (c)SUBJ |     |     |
| --- | --------- | --- | --- | ---------- | --- | --- | --- | --- | ------- | --- | --- |
Figure3:Analysisoftheimpactofinjectioncoefficientoptimizationonperformance.Thefigureillustrateshowmodelperfor-
manceevolvesastheinjectioncoefficientisoptimizedoversuccessivecommunicationrounds.
not only alleviates deployment bottlenecks in bandwidth- significantly enhances model performance and generaliza-
constrainedorhigh-latencyenvironments,butalsoprovides tion. This effect is particularly pronounced on the SUBJ
practical communication feasibility for large-scale applica- dataset, which features highly non-uniform data distribu-
tionsonmobile,edge,andIoTdevicesinreal-worldfeder- tions, thereby demonstrating the efficiency and robustness
atedsettings. oftheproposedframeworkinreal-worldfederatedlearning
scenarios.
ImpactofFederatedAggregationonInjection As illustrated in Figure 3, we analyze the performance
CoefficientPerformance trajectoryandstabilityoftheglobalinjectioncoefficientas
thenumberoffederatedroundsincreases.Theexperimental
| To evaluate          | the effectiveness | of forming   | a global injection |        |         |          |              |             |            |          |               |
| -------------------- | ----------------- | ------------ | ------------------ | ------ | ------- | -------- | ------------ | ----------- | ---------- | -------- | ------------- |
|                      |                   |              |                    |        | results | indicate | a consistent | improvement |            | in model | perfor-       |
| coefficient          | through federated | aggregation  | of locally         | cali-  |         |          |              |             |            |          |               |
|                      |                   |              |                    |        | mance   | over     | successive   | rounds,     | suggesting | that     | the iterative |
| brated coefficients, | we compare        | the accuracy | of the             | global |         |          |              |             |            |          |               |
refinementoftheglobalinjectioncoefficientplaysapivotal
| coefficient | on each client | with that of | locally optimized | in- |     |     |     |     |     |     |     |
| ----------- | -------------- | ------------ | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
roleinenhancingtheeffectivenessofIFed-ICLthroughcol-
| jection coefficients | derived | independently | using only | local |     |     |     |     |     |     |     |
| -------------------- | ------- | ------------- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
laborativeoptimization.
data.Foreachround,werecordtheaccuracyofall10client-
specificmodels,theiraverageaccuracy,andtheaccuracyof
Conclusion
theglobalmodel.Byquantifyingthedifferencebetweenthe
globalmodelaccuracyandthemeanlocalmodelaccuracy, ThispaperproposesaImplicitFederatedIn-contextLearn-
andanalyzingthedistributionofindividuallocalmodelper-
|     |     |     |     |     | ing | framework, | which | decomposes | the | federated | process |
| --- | --- | --- | --- | --- | --- | ---------- | ----- | ---------- | --- | --------- | ------- |
formance,weassesstheimpactoffederatedaggregationon intotwocomponents:contextvectoraggregationandinjec-
overallmodelperformanceandgeneralization. tion coefficient optimization. This enables lightweight task
AsillustratedinFigure2,thefederatedaggregationmech- adaptation for LLMs. Specifically, each client is respon-
anism in IFed-ICL substantially improves the performance sible for transforming the context into vector representa-
of the global injection coefficient. Compared to the aver- tionsandcalibratingtheinjectioncoefficientsthroughmulti-
age accuracy of local models, the global model achieves round federated optimization based on local data. A one-
notable improvements of approximately 10.71%, 26.05%, time linear injection is then performed to achieve model
and12.81%ontheAGNews,SUBJ,andEmotiondatasets, adaptation. Unlike traditional approaches such as context
respectively. Moreover, in most rounds, the global model concatenationorfullmodelfine-tuninginfederatedsettings,
outperforms the majority of individual local models. By IFed-ICLdecouplesdatafrommodeltraining,significantly
integrating knowledge from heterogeneous clients, the ag- reducing both communication and computation costs. Ex-
gregation process yields a superior global coefficient that periments across multiple text classification tasks demon-

stratetheeffectivenessoftheproposedframework,offering Konecˇny`, J.; McMahan, H. B.; Yu, F. X.; Richta´rik, P.;
a new paradigm for distributed intelligent collaboration on Suresh, A. T.; and Bacon, D. 2016. Federated learning:
resource-constraineddevices. Strategies for improving communication efficiency. arXiv
preprintarXiv:1610.05492.
References
|     |     |     |     |     |     |     | Li, Z.; Xu, | Z.; Han, | L.; | Gao, | Y.; Wen, | S.; Liu, | D.; Wang, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ---- | -------- | -------- | --------- |
Agarwal, R.; Singh, A.; Zhang, L.; Bohnet, B.; Rosias, L.; H.;andMetaxas,D.N.2024. ImplicitIn-contextLearning.
Chan,S.;Zhang,B.;Anand,A.;Abbas,Z.;Nova,A.;etal. arXiv:2405.14660.
| 2024. Many-shot |     | in-context | learning. | Advances |     | in Neural |          |             |     |         |         |           |         |
| --------------- | --- | ---------- | --------- | -------- | --- | --------- | -------- | ----------- | --- | ------- | ------- | --------- | ------- |
|                 |     |            |           |          |     |           | Liu, X.; | Ji, K.; Fu, | Y.; | Tam, W. | L.; Du, | Z.; Yang, | Z.; and |
InformationProcessingSystems,37:76930–76966.
|     |     |     |     |     |     |     | Tang,J.2021. | P-tuningv2:Prompttuningcanbecompara- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------------------------------------ | --- | --- | --- | --- | --- |
Bertsch, A.; Ivgi, M.; Alon, U.; Berant, J.; Gormley, bletofine-tuninguniversallyacrossscalesandtasks. arXiv
| M. R.; | and Neubig, |     | G. 2024. | In-Context |     | Learning |     |     |     |     |     |     |     |
| ------ | ----------- | --- | -------- | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
preprintarXiv:2110.07602.
| with Long-Context |     | Models: |     | An In-Depth | Exploration. |     |          |            |     |             |     |          |         |
| ----------------- | --- | ------- | --- | ----------- | ------------ | --- | -------- | ---------- | --- | ----------- | --- | -------- | ------- |
|                   |     |         |     |             |              |     | McMahan, | B.; Moore, |     | E.; Ramage, | D.; | Hampson, | S.; and |
arXiv:2405.00200.
|     |     |     |     |     |     |     | y Arcas, | B. A. 2017. | Communication-efficient |     |     |     | learning of |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | ----------------------- | --- | --- | --- | ----------- |
Brown,T.;Mann,B.;Ryder,N.;Subbiah,M.;Kaplan,J.D.;
|     |     |     |     |     |     |     | deepnetworksfromdecentralizeddata. |     |     |     |     | InArtificialintelli- |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | -------------------- | --- |
Dhariwal,P.;Neelakantan,A.;Shyam,P.;Sastry,G.;Askell,
genceandstatistics,1273–1282.PMLR.
| A.;etal.2020. | Languagemodelsarefew-shotlearners. |     |     |     |     | Ad- |     |     |     |     |     |     |     |
| ------------- | ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
vancesinneuralinformationprocessingsystems,33:1877– Pang,B.;andLee,L.2004.ASentimentalEducation:Senti-
mentAnalysisUsingSubjectivitySummarizationBasedon
1901.
|          |         |       |          |        |         |          | MinimumCuts. |     | InProceedingsofthe42ndAnnualMeeting |     |     |     |     |
| -------- | ------- | ----- | -------- | ------ | ------- | -------- | ------------ | --- | ----------------------------------- | --- | --- | --- | --- |
| Cai, D.; | Wu, Y.; | Wang, | S.; Lin, | F. X.; | and Xu, | M. 2022. |              |     |                                     |     |     |     |     |
oftheAssociationforComputationalLinguistics(ACL-04),
| Fedadapter: | Efficient | federated |     | learning | for modern | nlp. |     |     |     |     |     |     |     |
| ----------- | --------- | --------- | --- | -------- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- |
271–278.
arXivpreprintarXiv:2205.10162.
Chatterjee, A.; Narahari, K. N.; Joshi, M.; and Agrawal, P. Peng, Z.; Fan, X.; Chen, Y.; Wang, Z.; Pan, S.; Wen,
2019. SemEval-2019 task 3: EmoContext contextual emo- C.; Zhang, R.; and Wang, C. 2024. Fedpft: Federated
tion detection in text. In Proceedings of the 13th interna- proxy fine-tuning of foundation models. arXiv preprint
arXiv:2404.11536.
tionalworkshoponsemanticevaluation,39–48.
Che,T.;Liu,J.;Zhou,Y.;Ren,J.;Zhou,J.;Sheng,V.S.;Dai, Shu, Y.; Hu, W.; Ng, S.-K.; Low, B. K. H.; and Yu, F. R.
H.;andDou,D.2023. Federatedlearningoflargelanguage 2024. Ferret: Federated full-parameter tuning at scale for
|     |     |     |     |     |     |     | largelanguagemodels. |     |     | arXivpreprintarXiv:2409.06277. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ------------------------------ | --- | --- | --- |
modelswithparameter-efficientprompttuningandadaptive
optimization. arXivpreprintarXiv:2310.15080. Villalobos, P.; Sevilla, J.; Heim, L.; Besiroglu, T.; Hobb-
| Chen, C.;            | Feng,          | X.; Zhou, | J.;      | Yin, J.; and | Zheng,   | X. 2023. |                                       |            |            |         |           |                 |             |
| -------------------- | -------------- | --------- | -------- | ------------ | -------- | -------- | ------------------------------------- | ---------- | ---------- | ------- | --------- | --------------- | ----------- |
|                      |                |           |          |              |          |          | hahn, M.;                             | and Ho,    | A. 2022.   | Will    | we        | run out         | of data? an |
| Federated            | large language |           | model:   | A position   | paper.   | arXiv    |                                       |            |            |         |           |                 |             |
|                      |                |           |          |              |          |          | analysis of                           | the limits | of         | scaling | datasets  | in machine      | learn-      |
| e-prints,arXiv–2307. |                |           |          |              |          |          | ing. arXivpreprintarXiv:2211.04325,1. |            |            |         |           |                 |             |
| Feng, X.;            | Feng, X.;      | Du,       | X.; Kan, | M.-Y.;       | and Qin, | B. 2024. |                                       |            |            |         |           |                 |             |
|                      |                |           |          |              |          |          | Von Oswald,                           | J.;        | Niklasson, | E.;     | Randazzo, | E.; Sacramento, |             |
Adapter-basedselectiveknowledgedistillationforfederated
|     |     |     |     |     |     |     | J.; Mordvintsev, |     | A.; Zhmoginov, |     | A.; and | Vladymyrov, | M.  |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | -------------- | --- | ------- | ----------- | --- |
multi-domainmeetingsummarization. IEEE/ACMTransac- 2023. Transformers learn in-context by gradient descent.
tionsonAudio,Speech,andLanguageProcessing. In International Conference on Machine Learning, 35151–
| Hendel, | R.; Geva, | M.; | and | Globerson, | A. 2023. | In- |     |     |     |     |     |     |     |
| ------- | --------- | --- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
35174.PMLR.
|         |          |         |      |          | arXiv | preprint |     |     |     |     |     |     |     |
| ------- | -------- | ------- | ---- | -------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
| context | learning | creates | task | vectors. |       |          |     |     |     |     |     |     |     |
Wang,R.;Wang,Z.;Huang,C.;Wang,R.;Yu,T.;Yao,L.;
arXiv:2310.15916.
|     |     |     |     |     |     |     | Lui,J.;andZhou,D.2025. |     |     | FederatedIn-ContextLearning: |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | ---------------------------- | --- | --- | --- |
Hu,E.J.;Shen,Y.;Wallis,P.;Allen-Zhu,Z.;Li,Y.;Wang,
|                               |     |     |     |                      |     |     | Iterative | Refinement | for | Improved | Answer | Quality. | arXiv |
| ----------------------------- | --- | --- | --- | -------------------- | --- | --- | --------- | ---------- | --- | -------- | ------ | -------- | ----- |
| S.;Wang,L.;Chen,W.;etal.2022. |     |     |     | Lora:Low-rankadapta- |     |     |           |            |     |          |        |          |       |
preprintarXiv:2506.07440.
| tionoflargelanguagemodels. |                                        |               |     | ICLR,1(2):3. |         |     |                                      |     |     |          |          |               |             |
| -------------------------- | -------------------------------------- | ------------- | --- | ------------ | ------- | --- | ------------------------------------ | --- | --- | -------- | -------- | ------------- | ----------- |
|                            |                                        |               |     |              |         |     | Wies,N.;Levine,Y.;andShashua,A.2023. |     |     |          |          | Thelearnabil- |             |
| Hu,J.; Wang,D.;            |                                        | Wang,Z.;Pang, |     | X.;Xu,H.;    | Ren,J.; | and |                                      |     |     |          |          |               |             |
|                            |                                        |               |     |              |         |     | ityof in-contextlearning.            |     |     | Advances | inNeural |               | Information |
| Ren,K.2024.                | FederatedLargeLanguageModel:Solutions, |               |     |              |         |     |                                      |     |     |          |          |               |             |
ProcessingSystems,36:36637–36651.
|            |            |     |             | IEEE | Wireless | Commu- |             |         |           |     |          |           |      |
| ---------- | ---------- | --- | ----------- | ---- | -------- | ------ | ----------- | ------- | --------- | --- | -------- | --------- | ---- |
| Challenges | and Future |     | Directions. |      |          |        |             |         |           |     |          |           |      |
|            |            |     |             |      |          |        | Wu, F.; Li, | Z.; Li, | Y.; Ding, | B.; | and Gao, | J. 2024a. | Fed- |
nications.
biot:Llmlocalfine-tuninginfederatedlearningwithoutfull
Huang,B.;Mitra,C.;Karlinsky,L.;Arbelle,A.;Darrell,T.;
andHerzig,R.2024. Multimodaltaskvectorsenablemany- model. In Proceedings of the 30th ACM SIGKDD Con-
|                 |     |            |           |          |     |           | ference on | Knowledge | Discovery |     | and | Data Mining, | 3345– |
| --------------- | --- | ---------- | --------- | -------- | --- | --------- | ---------- | --------- | --------- | --- | --- | ------------ | ----- |
| shot multimodal |     | in-context | learning. | Advances |     | in Neural |            |           |           |     |     |              |       |
3355.
InformationProcessingSystems,37:22124–22153.
Jones, N. 2024. The AI revolution is running out of data. Wu, P.; Li, K.; Nan, J.; and Wang, F. 2024b. Fed-
Nature,636(8042):290–292. erated in-context llm agent learning. arXiv preprint
Whatcanresearchersdo?
arXiv:2412.08054.
Kairouz,P.;McMahan,H.B.;Avent,B.;Bellet,A.;Bennis,
M.;Bhagoji,A.N.;Bonawitz,K.;Charles,Z.;Cormode,G.; Yan, Y.; Yang, Q.; Tang, S.; and Shi, Z. 2024. Fed-
Cummings, R.; et al. 2021. Advances and open problems era: Efficient fine-tuning of language models in federated
infederatedlearning. Foundationsandtrends®inmachine learning leveraging weight decomposition. arXiv preprint
| learning,14(1–2):1–210. |     |     |     |     |     |     | arXiv:2404.18848. |     |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |

| Yang, Q.;                               | Liu,        | Y.; Chen, | T.; and        | Tong, Y. | 2019.       | Federated |
| --------------------------------------- | ----------- | --------- | -------------- | -------- | ----------- | --------- |
| machinelearning:Conceptandapplications. |             |           |                |          | ACMTransac- |           |
| tions on                                | Intelligent | Systems   | and Technology |          | (TIST),     | 10(2):    |
1–19.
| Ye,J.;Wu,Z.;Feng,J.;Yu,T.;andKong,L.2023. |     |                |     |           |                  | Compo- |
| ----------------------------------------- | --- | -------------- | --- | --------- | ---------------- | ------ |
| sitional exemplars                        |     | for in-context |     | learning. | In International |        |
ConferenceonMachineLearning,39818–39833.PMLR.
| Ye, R.; Wang, |     | W.; Chai, | J.; Li, D.; | Li, Z.; | Xu, | Y.; Du, Y.; |
| ------------- | --- | --------- | ----------- | ------- | --- | ----------- |
Wang,Y.;andChen,S.2024.OpenFedLLM:TrainingLarge
LanguageModelsonDecentralizedPrivateDataviaFeder-
| atedLearning. |                     | arXiv:2402.06954. |                   |     |                  |          |
| ------------- | ------------------- | ----------------- | ----------------- | --- | ---------------- | -------- |
| Zaken, E.     | B.; Ravfogel,       |                   | S.; and Goldberg, |     | Y. 2021.         | Bitfit:  |
| Simple        | parameter-efficient |                   | fine-tuning       |     | for transformer- |          |
| based masked  |                     | language-models.  |                   |     | arXiv            | preprint |
arXiv:2106.10199.
| Zhang, Y.;                             | Qin,      | Z.; Wu, | Z.; Hou,    | J.; and | Deng,         | S. 2024a. |
| -------------------------------------- | --------- | ------- | ----------- | ------- | ------------- | --------- |
| Personalized                           | Federated |         | Fine-Tuning | for     | LLMs          | via Data- |
| DrivenHeterogeneousModelArchitectures. |           |         |             |         | arXivpreprint |           |
arXiv:2411.19128.
| Zhang, Z.; | Yang,    | Y.; Dai,     | Y.; Wang, | Q.;            | Yu, Y.; | Qu, L.;  |
| ---------- | -------- | ------------ | --------- | -------------- | ------- | -------- |
| and Xu,    | Z. 2023. | FedPETuning: |           | When federated |         | learning |
meetstheparameter-efficienttuningmethodsofpre-trained
| language | models. | In Annual | Meeting | of  | the Association |     |
| -------- | ------- | --------- | ------- | --- | --------------- | --- |
ofComputationalLinguistics2023,9963–9977.Association
forComputationalLinguistics(ACL).
Zhang,Z.;Zhang,J.;Huang,J.;Qu,L.;Zhang,H.;andXu,
| Z. 2024b.                       | FedPIT: | Towards | Privacy-preserving |                      |     | and Few- |
| ------------------------------- | ------- | ------- | ------------------ | -------------------- | --- | -------- |
| shotFederatedInstructionTuning. |         |         |                    | CoRR,abs/2403.06131. |     |          |