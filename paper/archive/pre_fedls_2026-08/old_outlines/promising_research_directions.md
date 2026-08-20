# Research directions for FedICL-SQL after the BIRD-KD probe

**Ngày rà soát:** 2026-07-20  
**Mục tiêu:** chọn hướng phương pháp có xác suất tạo contribution tốt nhất,
không chỉ chọn paper FedLoRA mới nhất.  
**Bối cảnh thực nghiệm:** FLoRA-NA đã được chọn làm main aggregation; factor
FedAvg là baseline. BIRD teacher EX-match stage dùng toàn bộ pool 3.873 mẫu và
`CE + reverse-KL`, sau đó Spider recovery FT. Trên matched control, greedy EX
gần như không đổi (`+0.29 pp`, `p=0.83`), còn SC execution voting tăng
`+1.84 pp` (`p=0.070`) và gain tập trung ở hard queries.

## 1. Kết luận điều hành

Không nên thay FLoRA-NA ngay lúc này. Hướng triển vọng nhất là thay **static
teacher-target RKD** bằng **execution-anchored on-policy distillation**:

1. student sinh SQL trên public BIRD pool;
2. chạy SQL và nhóm candidate theo execution result;
3. teacher chấm chính các trajectory student vừa sinh;
4. tối ưu CE anchor cộng skew-RKL/RKL trên trajectory có thông tin;
5. giữ toàn bộ 3.873 câu làm population mặc định, nhưng weight/mask loss theo
   độ khó, disagreement hoặc mức executable của candidate set.

Tên làm việc phù hợp là **Exec-GKD**. Đây là thay đổi có cơ sở nhất vì nó tác
động đúng failure mode đã đo: static KD không đổi top-1 greedy nhưng dường như
đã thay hình dạng phân phối candidate mà SC có thể khai thác.

Nếu chỉ đủ tài nguyên cho một nhánh mới, thứ tự nên là:

```text
static BIRD CE+RKL
        ↓ thay bằng
Exec-GKD trên cùng full pool 3.873
        ↓ nếu centralized gate pass
FLoRA-NA + server Exec-GKD trong federated rounds
```

Không nên nhảy thẳng sang GRPO, FedDF hay đổi FLoRA-NA thành FLoRG trước khi
gate này pass.

## 2. Vì sao static RKD hiện tại chưa phải thiết kế tối ưu?

Pipeline hiện tại chấm token distribution của teacher trên một chuỗi SQL
teacher-generated cố định. Nó có ba giới hạn:

- **Train–inference mismatch:** lúc inference, lỗi cần sửa là lỗi trên chuỗi
  student tự sinh; nhưng lúc KD, model chủ yếu nhìn prefix của teacher output.
- **Selection bias:** pool chỉ chứa teacher generations đã EX-match. Đây là
  tập clean và hữu ích, nhưng bỏ qua chính các student mistakes mà ta muốn
  điều chỉnh.
- **Objective–decoder mismatch:** deployment SC quyết định theo execution
  cluster của nhiều sequence, trong khi loss chỉ tối ưu token-level trên một
  target. Kết quả thực nghiệm phù hợp với mismatch này: greedy không gain,
  còn SC có tín hiệu gain.

[MiniLLM](https://openreview.net/pdf?id=5h0qf7IBZZ) cho thấy reverse-KL phù hợp
với generative KD hơn forward-KL trong nhiều setting, nhưng điểm quan trọng
không chỉ là đổi chiều KL. [GKD](https://arxiv.org/abs/2306.13649) giải quyết
training–inference mismatch bằng cách cho student học từ chính generations
của nó với teacher feedback. [DistiLLM](https://arxiv.org/abs/2402.03898)
kết hợp skew-KL với adaptive off-policy reuse để giảm chi phí của
student-generated trajectories. Vì vậy code đã có RKL/skew-lambda là nền tốt;
phần nên thay là **nguồn sequence và cách chọn sequence**, không phải vứt bỏ
RKL để quay lại CE thuần.

## 3. Phương án đề xuất chính: Execution-anchored On-Policy GKD

### 3.1 Một server step

Với mỗi public example `x=(question, schema)` trong pool 3.873:

1. Sinh `m` candidate `y_1...y_m` từ aggregated student adapter. Gate đầu có
   thể dùng `m=2`; main experiment dùng `m=4` nếu compute cho phép.
2. Parse/execute từng candidate trong sandbox DB và ghi:
   `executable`, execution result hash, execution error type.
3. Nhóm các candidate executable theo execution result, giống SC evaluator.
4. Teacher tạo logits trên **prefix student-generated**. Không cần teacher
   generate lại target.
5. Tối ưu

   \[
   L = \lambda_{CE}L_{CE}(y_{pub})
       + \lambda_{KD}\sum_j w_j
         D_{skew/RKL}(p_T(\cdot|x,y_{j,<t})\|p_S(\cdot|x,y_{j,<t})).
   \]

`y_pub` vẫn là teacher EX-match SQL để giữ CE anchor. `w_j` có thể ưu tiên:

- candidate executable nhưng khác winning execution group;
- query có 4–7 executable candidates, đúng bucket đã cho gain lớn;
- low-consensus/high-entropy query;
- hard query hoặc teacher–student disagreement cao.

Không nên chỉ giữ candidate đã EX-match gold: làm vậy lại loại các mistakes
cần học. Execution status và teacher score nên quyết định weight; gold EX có
thể là một feature/label để phân tích và curriculum, không phải privacy leak
vì đây là public pool.

### 3.2 Vì sao khả thi với code hiện tại?

Hướng này tái sử dụng ba thành phần đã có:

- teacher logit scorer/RKL loss;
- online-KD path;
- SQL execution và SC grouping.

Khác biệt chính là cache không còn chỉ keyed theo `example_id`: logits phụ
thuộc student trajectory và adapter snapshot. Cache hợp lệ phải có key tối
thiểu `(round_or_adapter_hash, example_id, candidate_sql, teacher_id,
tokenizer_id)`. Có thể tái sử dụng candidate/logits trong vài optimizer step,
nhưng không được dùng một cache cố định qua mọi round rồi gọi là on-policy.

### 3.3 Cách giữ chi phí trong giới hạn

- Full pool 3.873 vẫn là default population; adaptive weighting không thay
  policy đã chốt.
- Gate với `m=2`; chỉ tăng `m=4` cho query low-consensus hoặc partial-exec.
- Teacher chỉ forward-score candidate, không autoregressive-generate.
- Lưu top-k logits hoặc log-prob tại student support nếu approximation error
  được đo; full-vocabulary cache vẫn là reference implementation.
- Refresh trajectories mỗi server round hoặc mỗi `R_refresh` rounds; báo cáo
  rõ stale-policy interval.

## 4. Phương án nhẹ hơn: SC-consensus distillation

Nếu online teacher scoring quá đắt, có thể distill trực tiếp execution voting:

1. student sinh `N` SQL;
2. execution-cluster như SC;
3. chọn representative của winning cluster;
4. train CE trên representative, có thể thêm teacher RKL trên chính sequence
   đó.

Mục tiêu là nén lợi ích của test-time SC vào một greedy adapter. Hướng này là
một **đề xuất kết hợp**, không nên viết như một method đã có nguyên xi trong
literature. Cơ sở của nó là on-policy sequence distillation từ GKD và bằng
chứng rằng execution feedback/majority voting hữu ích cho Text-to-SQL. Các
preprint gần đây như
[Arctic-Text2SQL-R1](https://arxiv.org/abs/2505.20315),
[ReEx-SQL](https://arxiv.org/abs/2505.12768), và
[execution-based GRPO for Text-to-SQL](https://arxiv.org/abs/2506.06093)
đều khai thác execution signal, nhưng chúng không phải federated KD và mức độ
peer review cần được mô tả đúng.

Ưu điểm là rất aligned với kết quả hiện tại. Nhược điểm là pseudo-label do
student vote có thể self-reinforce một execution-equivalent nhưng sai về ngữ
nghĩa; CE anchor và teacher scoring vẫn cần để kiểm soát drift.

## 5. Phương án mạnh nhưng rủi ro cao: execution-reward GRPO

Có thể fine-tune aggregated adapter bằng reward:

- `+1` nếu EX-match;
- reward mềm cho executable/no error;
- penalty cho invalid SQL, timeout hoặc unsafe statement;
- optionally reward agreement với teacher hoặc winning execution cluster.

Execution reward tối ưu trực tiếp metric paper quan tâm và các Text-to-SQL
works gần đây cho tín hiệu tốt. Tuy nhiên đây chưa phải lựa chọn đầu tiên:

- rollout cost cao hơn KD;
- variance và reward hacking lớn;
- cần nhiều hyperparameter/control hơn;
- contribution dễ chuyển thành một paper execution-RL khác, làm mờ câu hỏi
  federated aggregation + public distillation.

Chỉ mở nhánh này nếu Exec-GKD pass centralized gate nhưng plateau, hoặc nếu
paper quyết định chuyển claim trung tâm sang execution-aligned post-training.

## 6. Có nên thay FLoRA-NA?

### 6.1 FLoRG là replacement triển vọng nhất về aggregation

[FLoRG](https://openreview.net/forum?id=kntrZOm2AQ), ICLR 2026 Poster, dùng
một low-rank matrix, aggregate Gram matrix và Procrustes alignment. Nó xử lý
aggregation error cùng ambiguity do rotation của factorization và có bằng
chứng xuất bản mạnh hơn FLoRA-NA tại thời điểm rà soát.

Nhưng FLoRG không phải drop-in replacement: nó đổi parameterization và local
training. Chỉ nên implement nếu diagnostic cho thấy:

- FLoRA-NA projection error `e_agg` còn lớn;
- FLoRA-NA không hơn factor FedAvg ổn định;
- aggregation, chứ không phải server KD/decoder mismatch, là bottleneck.

Nếu các điều kiện này chưa xuất hiện, giữ FLoRA-NA giúp paper có một global
rank-`r` adapter, communication cố định và pipeline KD đơn giản. FLoRG nên
được cập nhật vào Related Work và có thể làm aggregation-only baseline nếu
ngân sách cho phép.

### 6.2 FedDF/FedMKT: function-space fusion thay parameter fusion

[FedDF](https://proceedings.neurips.cc/paper/2020/hash/18df51b97ccd68128e994804f3eccc87-Abstract.html)
distill ensemble predictions của client trên unlabeled/public data thay vì
average parameters. [FedMKT](https://aclanthology.org/2025.coling-main.17/)
trao đổi và selectively aggregate logits trên public dataset giữa server LLM
và client SLM. Đây là hướng rất hợp về mặt khái niệm: SQL clients chuyên biệt
theo domain có thể fusion trong function space, tránh lỗi `mean(A)mean(B)`.

Với setting này, nó chưa thực dụng làm main method:

- `8 clients × 3.873 rows × target tokens × 152k vocabulary` tạo communication
  rất lớn nếu gửi full logits;
- client phải infer trên public BIRD schemas mỗi round;
- prediction/logit sharing thêm một privacy surface;
- kiến trúc không còn đơn giản là client gửi một LoRA adapter.

Biến thể đáng nghiên cứu dài hạn là **FedExecDistill**: client chỉ gửi vài SQL
candidates + execution metadata trên public questions, server execution-cluster
rồi distill global adapter. Nó giảm communication so với logits và có novelty
Text-to-SQL rõ, nhưng là high-risk method cần privacy/threat analysis riêng.

### 6.3 Personalized LoRA chỉ đáng làm nếu worst-client là vấn đề chính

[FedPissa](https://openreview.net/forum?id=ZEWN40uNEh), ICML 2026 Spotlight,
dùng LoRA subspace mapping cho federated personalized adaptation. Đây là hướng
phù hợp nếu một global adapter hy sinh mạnh các domain/schema clients. Nhưng
paper hiện cần một adapter dùng chung và server KD chung. Chuyển sang
personalization sẽ thay evaluation, serving và research question; chỉ nên mở
khi per-client/worst-client results chứng minh global model thất bại dù mean
EX ổn.

## 7. Xếp hạng theo expected research value

| Hướng | Fit với bằng chứng hiện tại | Implementation | Compute | Novelty | Quyết định |
|---|---:|---:|---:|---:|---|
| Exec-GKD + FLoRA-NA | **rất cao** | vừa | vừa–cao | cao cho Fed Text-to-SQL | **main candidate** |
| adaptive static RKL trên full pool | cao | thấp | thấp–vừa | vừa | cheap ablation/gate |
| SC-consensus distillation | rất cao | vừa | vừa | cao | phương án 2 |
| FLoRG thay FLoRA-NA | vừa | cao | vừa | thấp hơn vì method có sẵn | chỉ khi `e_agg` xấu |
| execution-GRPO | cao | cao | rất cao | cao | tier 2 |
| FedDF/FedMKT logits | vừa | rất cao | rất cao | vừa | không nên làm main hiện tại |
| FedExecDistill candidates | cao về ý tưởng | rất cao | cao | **rất cao** | future/high-risk |
| FedPissa personalization | thấp nếu cần 1 adapter | cao | cao | vừa | chỉ khi worst-client gap lớn |

## 8. Experimental ladder đề xuất

### Gate 0 — hoàn thành attribution hiện tại

Trước khi claim RKL có hiệu quả:

```text
A  Spider-FT → Spider-FT
B  Spider-FT → BIRD teacher EX-match CE-only → Spider-FT
C  Spider-FT → BIRD teacher EX-match CE+RKL → Spider-FT
```

Chạy greedy và SC seeds `0,1,2`. `B vs C` mới định danh phần logits/RKL;
`A vs C` chỉ định danh cả BIRD stage.

### Gate 1 — centralized method screen

Thêm:

```text
D  Spider-FT → BIRD Exec-GKD → Spider-FT
E  Spider-FT → BIRD SC-consensus distill → Spider-FT   (optional)
```

Cùng full pool 3.873, cùng effective optimizer steps/token budget nếu có thể.
Báo cáo greedy EX/EM, SC EX/EM, exec errors, EX theo hardness và số executable
candidates. Method pass nếu qua ít nhất một điều kiện pre-registered:

- greedy EX hơn static RKL ít nhất `1.0 pp`; hoặc
- SC EX hơn ít nhất `1.5 pp` ở trung bình nhiều sampling seeds;
- không tăng đáng kể execution errors và không chỉ đổi EM formatting.

Ngưỡng này là engineering gate, không thay confidence interval/significance.

### Gate 2 — federated factorial tối thiểu

Nếu D pass:

| Aggregation | Server update |
|---|---|
| factor FedAvg | none |
| factor FedAvg | static RKL |
| FLoRA-NA | none |
| FLoRA-NA | CE-only |
| FLoRA-NA | static RKL |
| FLoRA-NA | Exec-GKD |

Nếu budget căng, ưu tiên bốn arm: factor/no-KD, FLoRA-NA/no-KD,
FLoRA-NA/static-RKL, FLoRA-NA/Exec-GKD. CE-only vẫn cần xuất hiện ở
centralized attribution hoặc một federated seed để tránh claim quá mức.

### Gate 3 — chỉ mở aggregation replacement khi cần

Log mỗi round:

- FLoRA-NA projection error so với ideal weighted `sum_i p_i B_iA_i`;
- client update pairwise cosine/Frobenius distance;
- global mean EX và worst-client/domain EX;
- bytes/round và server KD FLOPs/time.

Nếu projection error lớn và correlate với accuracy loss, thêm FLoRG. Nếu
worst-client gap lớn nhưng aggregation error nhỏ, xem personalization. Nếu cả
hai đều nhỏ, không mở thêm nhánh federated method.

## 9. Claim paper có thể hướng tới

Claim khả thi và mạch lạc nhất là:

> Nearly-accurate adapter aggregation và execution-anchored on-policy public
> distillation giải quyết hai lỗi trực giao trong federated Text-to-SQL:
> weight-space aggregation error và train–inference/decoder mismatch dưới
> schema-domain heterogeneity.

Để claim này đứng vững, paper phải chứng minh ba điểm riêng:

1. FLoRA-NA giảm aggregation error/giữ communication so với factor FedAvg;
2. Exec-GKD hơn CE-only và static RKL trên matched token/step budget;
3. gain còn tồn tại qua federated seeds và SC sampling seeds, không chỉ một
   centralized checkpoint.

## 10. Quyết định cuối

**Giữ FLoRA-NA làm main aggregation. Thay đổi có triển vọng nhất là nâng
server KD thành Exec-GKD; SC-consensus distillation là phương án kế tiếp.**
FLoRG là replacement aggregation đáng tin cậy nhất để theo dõi/ablate, nhưng
chưa phải bottleneck có bằng chứng. FedDF/FedMKT và execution-GRPO có upside
lớn hơn về lý thuyết nhưng chi phí và scope risk quá cao cho vòng paper hiện
tại.

