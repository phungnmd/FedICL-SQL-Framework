# Critical reading of KID and related KD methods for FedICL-SQL

**Ngày rà soát:** 2026-07-20  
**Paper trung tâm:** Zhong et al., *Learning from Imperfect Data: Towards
Efficient Knowledge Distillation of Autoregressive Language Models for
Text-to-SQL* ([arXiv:2410.11371](https://arxiv.org/abs/2410.11371)).  
**Câu hỏi:** pipeline BIRD teacher EX-match hiện tại thực sự kế thừa gì từ KID,
và phương pháp KD nào gần bài toán hơn hoặc triển vọng hơn?

## 1. Kết luận trước

Ba kết luận quan trọng sau khi đọc paper đầy đủ:

1. **KD hiện tại không phải KID.** Nó là `CE + RKL` trên một sequence cố định do
   teacher sinh và đã EX-match. Có thể gọi chính xác là **teacher-sequence RKD**
   hoặc **SeqKD + logit RKD hybrid**. KID thật phải để student tạo imperfect
   sequence bằng masking–predicting–rewriting.
2. **True KID là baseline kế tiếp rẻ và bắt buộc nên có**, vì đây là paper gần
   setup nhất: Text-to-SQL, autoregressive Qwen-family, LoRA, RKL, Spider và
   BIRD. Nó giúp kiểm tra liệu exposure-bias correction một-pass có hơn static
   RKD trong cross-domain pipeline của ta hay không.
3. **Phương pháp có upside cao hơn KID là execution-gated SKD/GKD**, không phải
   một KL variant thuần. KID chỉ mô phỏng lỗi bằng corrupt 20% token; GKD/SKD
   học trên state student thật sự đi qua; executor của SQL cho phép chọn đúng
   failure trajectory. Đây là khoảng trống hợp với contribution của paper.

Thứ tự khuyến nghị:

```text
Static teacher-sequence RKD (đã có)
        ↓ baseline trực tiếp, chi phí thấp
True KID trên cùng y_pub 3.873
        ↓ nếu cần method mới có khả năng vượt KID
Execution-gated SKD/GKD
        ↓ chỉ khi rollout budget rất lớn
Execution-RL / GRPO
```

## 2. KID thực sự làm gì?

### 2.1 Motivation

Paper so sánh năm họ KD trên Text-to-SQL:

| Method | Sequence dùng để tính KD | Divergence |
|---|---|---|
| FKD | ground-truth | forward KL |
| RKD | ground-truth | reverse KL |
| f-distill | teacher + student generated | TVD/f-divergence |
| ImitKD | ground-truth + student generated | forward KL |
| GKD | student on-policy generation | FKL/RKL/JSD |
| KID | imperfect rewrite của ground-truth | reverse KL |

Hai empirical findings dẫn đến KID:

- RKL tốt hơn FKL cho SQL vì table/column/value tokens chính xác và ít mode;
- student-generated/on-policy sequences giảm train–inference mismatch nhưng
  autoregressive generation làm GKD rất đắt.

Trên Qwen1.5-0.5B student và 7B teacher, Spider EX trong preliminary table là:

| SFT | FKD | RKD | GKD-FKL | GKD-RKL | GKD-JSD |
|---:|---:|---:|---:|---:|---:|
| 57.8 | 57.3 | 61.5 | 60.7 | **64.3** | **64.3** |

Điểm quan trọng: kết quả này ủng hộ cả **RKL** lẫn **on-policy data**. Nó không
chứng minh RKL trên teacher-generated sequence là KID.

### 2.2 Masking–predicting–rewriting

Với gold output `y`:

1. Chọn tỷ lệ `alpha` token và thay bằng special token, mặc định random
   `alpha=0.2`.
2. Student điền các vị trí mask bằng **một teacher-forced forward pass**, không
   autoregressive generation.
3. Splice predictions vào `y` để tạo imperfect sequence `y_hat`.
4. Teacher và student đều forward trên `y_hat`; tối ưu RKL trên các prefix của
   `y_hat`.
5. Đồng thời giữ auxiliary MLE/CE trên original `y` để tránh student samples
   xấu ở đầu training.

Loss khái quát:

\[
L_{KID}=L_{CE}(y)+\lambda D_{RKL}
\left(q_S(\cdot\mid x,\hat y_{<t})\,\|\,
p_T(\cdot\mid x,\hat y_{<t})\right).
\]

Ý tưởng của KID không phải “distill teacher SQL sai”. `y_hat` là các prefix bị
student làm imperfect để model học cách phục hồi sau lỗi trước đó.

### 2.3 Ablations đáng tin nhất từ paper

- Random masking ổn định hơn Easy/Hard entropy masking.
- `alpha=0.1–0.3` đều tốt; `0.2` tốt nhất trong thí nghiệm; `0.5` làm hỏng ngữ
  nghĩa sequence và giảm chất lượng.
- Rewriting là thành phần chính. So với “vanilla KID”, masking-only chỉ thêm
  khoảng `+0.5–0.7 EX`, còn full rewriting thêm `+2.1 EX` trên TinyLLaMA và
  `+3.3 EX` trên CodeGen.
- Trên Qwen0.5B←Qwen7B, average score: SFT `43.85`, RKD `45.74`, GKD `48.20`,
  KID `47.88`; latency tương ứng `1.0x`, `2.3x`, `13.9x`, `2.3x`.
- Riêng BIRD with external knowledge: SFT `30.51`, RKD `31.81`, GKD `34.62`,
  KID `34.35`. KID gần GKD nhưng không luôn thắng GKD tuyệt đối.
- KID giảm exposure mismatch metric `ExAccErr` từ RKD `16.2` xuống `5.3`;
  GKD thấp hơn nữa ở `0.8`.

Kết luận đúng từ số liệu là: **KID xấp xỉ phần lớn gain của GKD với chi phí gần
RKD**, không phải KID luôn tốt hơn true on-policy KD.

## 3. Những giới hạn khi chuyển kết quả KID sang paper ta

| Trục | KID paper | FedICL-SQL hiện tại |
|---|---|---|
| Mục tiêu | model compression cùng task | federated learning + cross-domain public KD |
| Teacher data | teacher FT trên chính train task | frozen coder teacher; BIRD teacher EX-match pool |
| KD target | original gold SQL bị rewrite | teacher-generated EX-matched SQL cố định |
| Student | Qwen1.5-0.5B trong main Qwen table | Qwen2.5-1.5B |
| Teacher | Qwen1.5 1.8B/4B/7B | Qwen2.5-Coder-7B |
| Training | Qwen LoRA, 8 epochs, batch 16 | ngắn hơn; adapter nối qua nhiều stages/rounds |
| Domain | train/eval cùng Spider hoặc cùng BIRD | BIRD public KD rồi Spider recovery/eval |
| Decoder | greedy | greedy và SC execution voting |
| Federation | không | 8 non-IID clients + server update |

Do đó gain `+4.03 average` của KID không phải prior hợp lệ cho pipeline ta.
Khác biệt lớn nhất không phải model version mà là **same-domain compression vs
cross-domain post-aggregation adaptation**.

KID paper hiện là arXiv preprint; nên cite đúng trạng thái, không mô tả như một
ACL/EMNLP accepted paper nếu chưa có nguồn venue chính thức.

## 4. Pipeline hiện tại nên được gọi là gì?

Với `y_pub` là teacher SQL đã EX-match:

\[
L_{current}=L_{CE}(y_{pub})+lambda D_{RKL}
(q_S(\cdot|x,y_{pub,<t})\|p_T(\cdot|x,y_{pub,<t})).
\]

Đây là giao của:

- **sequence-level/hard distillation:** target do teacher sinh;
- **token-distribution distillation:** teacher logits trên target prefixes;
- **RKD baseline:** reverse KL;
- **execution-filtered data selection:** chỉ giữ teacher output EX-match.

Nó không có imperfect student rewrite và cũng không có student rollout. Trong
paper nên viết:

> We use execution-filtered teacher-sequence reverse-KL distillation, adapted
> from the RKD baseline studied by KID.

Không nên viết “we use KID” trừ khi masking–predicting–rewriting được bật.

## 5. Các paper KD gần bài toán nhất

### 5.1 GKD — true on-policy soft distillation

[GKD](https://arxiv.org/abs/2306.13649), ICLR 2024, để student sinh sequence
theo policy hiện tại rồi teacher cung cấp token distribution trên chính prefix
đó. Đây là comparator quan trọng nhất của KID và là lời giải trực tiếp cho
exposure bias.

**Fit:** rất cao. SQL student đang lỗi ở schema/join prefix nào thì teacher chấm
đúng state đó. Student 1.5B của ta mạnh hơn Qwen0.5B trong KID paper nên nguy cơ
rollout toàn rác có thể thấp hơn.

**Hạn chế:** KID đo GKD tới `13.9x` latency SFT khi generate online per step.
Trong federated pipeline, generate một lần mỗi server round và replay vài step
có thể amortize, nhưng khi đó phải gọi chính xác là periodically refreshed
off-policy GKD, không phải fully on-policy.

### 5.2 SKD — teacher–student interleaved sampling

[Speculative Knowledge Distillation](https://proceedings.iclr.cc/paper_files/paper/2025/file/a2747a3844ca1e4667fbff3f558eb39b-Paper-Conference.pdf),
ICLR 2025, nằm giữa supervised KD và GKD:

- student đề xuất token;
- teacher kiểm tra token có trong top-K teacher distribution không;
- token bị reject được teacher resample;
- tiếp tục student generation từ prefix đã sửa;
- distill teacher–student distribution trên sequence xen kẽ đó.

SKD giải đúng một nhược điểm của raw GKD: early student rollouts có thể OOD đối
với teacher, khiến teacher feedback trên prefix vô nghĩa. Trong main experiments
paper dùng `K=25` và speculative block `gamma=5`.

**Fit:** rất cao về cơ chế. Với SQL, có thể thêm execution gate sau khi hoàn
thành sequence. Đây có khả năng tốt hơn “GKD rồi chỉ lọc executable” vì SKD sửa
sớm table/column tokens trước khi cả suffix bị phá.

**Chi phí:** teacher phải tham gia trong generation loop; phức tạp và đắt hơn
KID. Đây là main-method candidate sau khi true KID baseline chạy xong.

### 5.3 DistiLLM và DistiLLM-2 — ổn định divergence và reuse rollouts

[DistiLLM](https://arxiv.org/abs/2402.03898), ICML 2024, đưa ra skew-KL/skew-RKL
để giới hạn gradient xấu và một replay scheduler để reuse student-generated
outputs; paper báo tới `4.3x` speedup so với các KD methods gần đó.

[DistiLLM-2](https://arxiv.org/abs/2503.07067), ICML 2025, dùng asymmetric
contrastive treatment: tăng likelihood của teacher response và giảm/điều chỉnh
student response thay vì dùng một loss giống nhau trên hai loại data.

**Fit:**

- skew-RKL là drop-in ablation tốt nếu on-policy RKL bất ổn;
- adaptive replay rất hợp server rounds;
- contrastive teacher-correct/student-wrong pairs có thể lấy từ execution
  groups của SC.

**Không nên làm:** chỉ đổi RKL thành skew-RKL rồi claim contribution chính. Nó
không giải decoder mismatch và novelty thấp.

### 5.4 ATKD và TAID — xử lý capacity gap

[ATKD](https://aclanthology.org/2024.acl-long.587/), ACL 2024, cho rằng các
token có teaching mode khác nhau và teacher lớn hơn không luôn tạo student tốt
hơn; adaptive teaching của họ cải thiện nhiều baseline KD tới `+3.04` average
trên các generative/understanding tasks.

[TAID](https://proceedings.iclr.cc/paper_files/paper/2025/hash/e664650506f1cf2b4696df892147c06e-Abstract-Conference.html),
ICLR 2025, tạo intermediate distribution dịch dần từ student sang teacher theo
thời gian để tránh capacity gap, mode averaging và mode collapse.

**Fit:** trung bình. Teacher 7B→student 1.5B là gap vừa phải và cùng Qwen
tokenizer. Hai phương pháp này đáng làm nếu log cho thấy teacher–student KL rất
lớn hoặc RKL unstable, nhưng chúng không xử lý student-prefix mismatch trực
tiếp như KID/GKD/SKD.

### 5.5 Selective KD 2026 — hướng mới rất hợp cache budget

[Rethinking Selective Knowledge Distillation](https://arxiv.org/abs/2602.01395)
phân tách selection theo position, vocabulary class và sample; SE-KD dùng
student entropy để chọn position và báo cáo giảm wall time/storage đáng kể.

[TIP: Token Importance in On-Policy Distillation](https://arxiv.org/abs/2604.14084)
chỉ ra hai vùng token hữu ích:

1. student entropy cao;
2. student entropy thấp nhưng teacher–student divergence cao—student tự tin
   nhưng sai.

TIP báo cáo giữ 50% entropy-selected tokens có thể match/vượt all-token
training, và một số low-entropy/high-divergence subsets rất nhỏ vẫn giữ phần
lớn hiệu quả. Đây đều là preprint rất mới, nên coi là hypothesis generator chứ
không phải established Text-to-SQL evidence.

**Fit:** rất cao cho engineering và ablation. SQL có nhiều token filler
(`SELECT`, punctuation) và một ít pivot token quyết định execution
(table/column/join/value). Có thể cache/distill full 3.873 rows nhưng chỉ giữ
top positions theo entropy + divergence, không trái policy full-data.

### 5.6 Pure-KD — distill privileged prompt

[Pure Fine-Tuning and Pure Knowledge Distillation](https://aclanthology.org/2025.naacl-industry.5/),
NAACL 2025 Industry, cho teacher 3B prompt tinh gọn/relevant hơn và student 1B
prompt đầy đủ hơn; distilled student tăng `1.9 TS` trên Spider. Điểm hữu ích
không phải mức gain mà là **asymmetric context**: teacher có privileged, clean
context rồi truyền distribution cho student có context khó hơn.

**Fit:** cao với ICL/schema selection. Có thể cho teacher thấy retrieved values,
oracle-relevant schema hoặc canonical SQL trong server KD, còn student chỉ thấy
deployment prompt. Tuy nhiên phải tránh dùng oracle information không tồn tại ở
deployment nếu mục tiêu là benchmark-comparable inference.

### 5.7 Struct-SQL — structured reasoning distillation

[Struct-SQL](https://arxiv.org/abs/2512.17053) dùng GPT-4o sinh query-execution-plan
CoT rồi SFT Qwen3-4B trên plan + SQL. Trên BIRD mini-dev, structured CoT tăng
EX từ `36.9` lên `45.0` so với unstructured CoT; paper báo `60.42 EX` trên
BIRD test cho single 4B greedy model.

**Fit về task:** rất cao. **Fit với scope hiện tại:** thấp, vì:

- đây là hard sequence/rationale distillation, không logit KD;
- output dài hơn và inference phải generate plan;
- teacher đóng GPT-4o;
- paper hiện là preprint;
- project đã chủ động bỏ CoT direction vì latency/scope.

Nên cite Related Work, không nên mở lại trừ khi paper đổi research question
sang structured reasoning compression.

### 5.8 Execution-feedback code generation — supporting evidence, không phải KD

[ConCoder](https://aclanthology.org/2025.coling-main.704/) dùng contrastive
execution feedback để code model học phân biệt correct/incorrect code.
[StepCoder](https://aclanthology.org/2024.acl-long.251/) dùng compiler feedback
và fine-grained masking trong RL. Chúng hỗ trợ luận điểm rằng execution signal
nên quyết định sequence/token nào cần học, nhưng không thể được trình bày như
Text-to-SQL logit-KD predecessors.

## 6. Hướng phương pháp tốt nhất sau khi đọc KID

### 6.1 Baseline ngay lập tức: true KID on teacher EX-match targets

Áp nguyên KID lên `y_pub`:

```text
y_pub (teacher-generated, EX-match)
  → random mask 20%
  → student one-pass fill
  → y_hat
  → CE(y_pub) + RKL teacher/student on y_hat
```

Lợi ích:

- gần code hiện tại;
- không cần autoregressive rollout;
- giữ full pool 3.873;
- tạo comparator trực tiếp với paper gần nhất;
- test được liệu gain của KID còn tồn tại khi target là teacher SQL và domain
  sau cùng là Spider.

Arm này nên gọi `bird_kid`, không đổi tên `bird_rkd` hiện tại.

### 6.2 Main candidate: Execution-gated SKD

Phương pháp đề xuất:

1. aggregated student đề xuất token blocks;
2. teacher giữ token nếu nằm trong `top-K_T`, thay token quá lệch;
3. hoàn thành 2–4 SQL candidates;
4. execute, group theo result như SC;
5. tính RKL/skew-RKL trên interleaved sequences;
6. tăng weight cho wrong-executable, low-consensus, 4–7 executable bucket và
   hard queries; vẫn giữ CE trên `y_pub`.

Execution signal nên dùng để **weight/select** chứ không chỉ binary drop:

- drop toàn bộ invalid rollouts sẽ làm model không học cách sửa syntax;
- chỉ giữ EX-correct sẽ biến method thành rejection-SFT;
- giữ wrong but executable trajectories với teacher correction mới cung cấp
  failure-state supervision có giá trị.

Tên paper-safe: **Execution-Gated Speculative Distillation (Exec-SKD)**. Cần
viết rõ đây là phương pháp đề xuất lấy nền từ SKD + execution-aware training,
không phải một published method đã có.

### 6.3 Low-cost enhancement: SQL-selective RKL

Trên static/KID/Exec-SKD đều có thể dùng token weight:

\[
w_t=f(H(q_t),D(q_t\|p_t),\text{SQL token type},\text{execution state}).
\]

Gate đầu nên dùng rule đơn giản, pre-registered:

- giữ top 50% token theo normalized student entropy;
- cộng lại low-entropy/high teacher–student divergence tokens;
- luôn giữ identifiers, literals và join/operator tokens;
- punctuation/filler dùng weight thấp, không nhất thiết zero.

Đây là cách thực tế nhất để giảm cache/full-vocab compute và có một ablation
mechanistic rõ: gain đến từ schema pivots hay từ phân phối toàn vocabulary?

## 7. Experimental design tối thiểu

### Phase A — xác nhận paper KID trong setting của ta

Từ cùng incoming adapter:

| Arm | BIRD stage | Mục đích |
|---|---|---|
| A | CE-only trên `y_pub` | data/extra-steps control |
| B | static RKL hiện tại | logit contribution |
| C | true KID, random `alpha=0.2` | imperfect-data contribution |
| D | true KID, `alpha=0.0` | implementation identity check với RKD |

Sau đó cùng một Spider recovery epoch. D phải numerically gần B; nếu không,
loss masking, target shift hoặc step accounting chưa matched.

### Phase B — method screen

| Arm | Sequence policy | Teacher correction | Execution gate |
|---|---|---|---|
| C | one-pass imperfect | logits only | no |
| E | GKD rollout | logits only | no |
| F | GKD rollout | logits only | weighted |
| G | SKD interleaved | token replacement + logits | weighted |

Để công bằng, báo cả:

- effective optimizer steps;
- student/teacher forward tokens;
- generated tokens;
- wall time và peak VRAM;
- cache size;
- greedy + SC EX/EM qua nhiều sampling seeds.

Không match “epoch” đơn thuần vì KID, GKD và SKD có generation cost khác hẳn.

### Phase C — federated

Chỉ mang C hoặc G vào FLoRA-NA loop nếu centralized screen pass. Grid gọn:

```text
factoravg / no server KD
FLoRA-NA / no server KD
FLoRA-NA / static RKL
FLoRA-NA / true KID
FLoRA-NA / Exec-SKD winner
```

## 8. Decision rules

- Nếu true KID không hơn static RKL: không claim imperfect-data mechanism
  transfer sang cross-domain/federated setting; giữ nó làm negative result.
- Nếu true KID hơn nhưng GKD/SKD không hơn: chọn KID vì performance/compute
  frontier tốt nhất và novelty đặt ở federated integration.
- Nếu Exec-SKD hơn KID ít nhất `1.0 pp` greedy EX hoặc `1.5 pp` SC EX ổn định
  qua seeds: chọn Exec-SKD làm method chính.
- Nếu selective KD giữ accuracy trong khi giảm ít nhất 50% cache/teacher-token
  compute: đưa thành efficiency contribution dù EX không tăng.
- Không mở Struct-SQL/CoT nếu inference-token budget vẫn là constraint.

## 9. Final recommendation

**Việc cần làm tiếp theo về KD không phải thay RKL bằng một loss ngẫu nhiên.**

1. Implement/evaluate **true KID** để có baseline đúng với paper gần nhất.
2. Dùng **SKD thay raw GKD** làm nền cho on-policy method vì nó bảo vệ teacher
   khỏi student prefixes quá OOD.
3. Thêm **execution gating + selective token weighting** để tạo contribution
   riêng cho federated Text-to-SQL.
4. Giữ DistiLLM skew-RKL làm stabilization ablation và Pure-KD/Struct-SQL trong
   related work.

Nếu chỉ chọn một replacement triển vọng hơn static RKD, lựa chọn là
**Exec-SKD**. Nếu chỉ chọn một experiment rẻ tiếp theo, lựa chọn là
**true KID trên đúng pool 3.873**.

## 10. Hardware-constrained decision: one RTX A5000 24 GB

> **Revision after applying the real project budget.** The recommendation
> above ranks methodological upside. It is not the production decision for a
> full `K=8`, multi-round, multi-seed FLoRA-NA grid on one A5000. Under that
> constraint, the main method should remain **cache-backed execution-filtered
> RKD**; **cached skew-RKL** is the only higher-priority KD variant to gate.

### 10.1 Local evidence dominates generic paper averages

The project already ran matched centralized RKD and KID:

| Method | measured time/step | measured peak VRAM | accuracy result |
|---|---:|---:|---|
| RKD | 1.95 s | 38.2 GB in that full-precision run | reference |
| KID | 8.65 s | 51.5 GB in that full-precision run | greedy `−1.45 pp` vs RKD, `p=0.072` |

The measurements came from a configuration larger than the 24 GB deployment
profile, so their absolute VRAM values are not an A5000 fit claim. They show
the relevant **relative** cost: KID was `4.4x` slower and used `35%` more peak
memory. On the adopted SC decoder, KID and RKD were statistically identical:
`72.24` vs `72.34 EX`, with paired McNemar `p=1.0`.

Quantizing the teacher to 4-bit makes KID fit a 24 GB card at batch 1, but does
not solve its total-compute problem and can reduce throughput. More importantly:

- RKD's fixed `y_pub` permits one offline teacher-logit cache reused by every
  FLoRA-NA round and seed;
- KID's `y_hat` changes with the current student, so the 7B teacher must score
  new prefixes online;
- GKD/SKD add autoregressive generation and are also non-cacheable across
  changing adapters.

### 10.2 Full-grid cost implication

At the measured rates, one pass over 3,873 examples is approximately:

- RKD online reference: `3,873 × 1.95 s ≈ 2.1 GPU-hours`;
- KID online reference: `3,873 × 8.65 s ≈ 9.3 GPU-hours`.

Across 15 server rounds, that is about `31.5` vs `139.6` GPU-hours for only
the server KD stage of one arm, before eight-client local training, evaluation,
retries and additional seeds. Cache-backed RKD removes the 7B teacher from the
round loop and should be cheaper than the online RKD reference; KID cannot gain
the same amortization. GKD/SKD would be more expensive again because decoding
dominates.

Thus a method may fit 24 GB VRAM but still be scientifically infeasible: if it
prevents matched controls and seeds, its nominally higher upside is not useful
for this paper.

### 10.3 Recommended FLoRA-NA configuration

**Main arm:**

```text
weighted FLoRA-NA
→ full 3,873-row BIRD teacher EX-match pool
→ cached CE + RKL(q || p)
→ rank-16 global adapter
```

Operational profile:

- build full teacher cache once with Qwen2.5-Coder-7B 4-bit;
- all federated KD runs load only Qwen2.5-1.5B + LoRA during server training;
- batch 1, gradient accumulation 16, fp16, gradient checkpointing;
- cache is shared across rounds only when pool/prompt/teacher/tokenizer hashes
  match exactly;
- keep CE-only `florana_pub` as the causal control.

This is the best expected **performance × reproducibility × GPU-hour** choice,
not a claim that RKD is universally superior to KID.

### 10.4 Only practical stronger candidate: cached skew-RKL

[DistiLLM](https://arxiv.org/abs/2402.03898)'s skew-RKL changes the divergence,
not the target sequence. Therefore it can reuse the exact same offline teacher
cache and has almost the same memory/forward profile as RKD. The code already
supports `rkl_skew_lambda=0.1`.

Use one cheap centralized or `T=1` FLoRA-NA gate:

```text
florana_pub       = CE-only
florana_kd        = CE + cached RKL
florana_srkd      = CE + cached skew-RKL, alpha=0.1
```

Promote skew-RKL only if it beats RKL by at least `1 pp` EX or materially
reduces instability/execution errors under matched steps. Otherwise do not add
it to the three-seed headline grid.

### 10.5 Methods to defer on one A5000

| Method | VRAM fit with 4-bit teacher | Reusable teacher cache | Multi-round verdict |
|---|---:|---:|---|
| cached RKD | easily | **yes** | **main** |
| cached skew-RKL | easily | **yes** | one gate, promising |
| true KID | likely at batch 1 | no | single-round ablation only |
| GKD | likely with careful sequential phases | no | defer |
| Exec-GKD | likely but generation-heavy | no | defer |
| SKD / Exec-SKD | risky throughput and complex KV lifecycle | no | future/high-resource |
| TAID | likely | potentially yes on fixed targets | lower priority than implemented skew-RKL |
| Struct-SQL/CoT | training may fit | hard targets cacheable | rejected because inference latency/scope |

Selective token KD remains an interesting efficiency extension, but it only
reduces real runtime after implementing a sparse/top-k cache and sparse loss.
Merely masking token positions after materializing full `T × V` student logits
does not remove the dominant vocabulary projection cost, so it should not be
sold as an immediate A5000 speedup.

### 10.6 Final hardware-aware decision

For the actual paper and one A5000 24 GB:

1. **Use FLoRA-NA + cache-backed RKD as the proposed full method.**
2. Run CE-only as the mandatory control because the current BIRD experiment
   identifies the whole `CE+RKL` stage, not RKL alone.
3. Give cached skew-RKL exactly one gate because it is nearly free and already
   implemented.
4. Keep true KID as a one-round/centralized literature baseline only; do not
   run it every federated round.
5. Put Exec-SKD/GKD in future work unless more GPUs or a much smaller public
   schedule becomes available.
