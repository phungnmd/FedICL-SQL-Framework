# Proposal: K-first bootstrap và privileged self-distillation tại client

Ngày đánh giá: **2026-10-12**. Dự án: **FedLS-SQL**.
Trạng thái: **đề xuất nghiên cứu, chưa chọn làm method, chưa triển khai hay chạy GPU**.
File này đặc tả một hướng và cách kiểm chứng; không thay [run queue](PIPELINE_NEXT.md).

## 1. Quyết định và xác suất thành công

**Đáng đầu tư một pilot nhỏ; chưa đáng chạy ngay toàn bộ matrix ba seed.**
Teacher 7B dạy student 1.5B trên public BIRD trước FL. Sau đó, tại mỗi client,
một bản sao frozen của student được xem gold SQL private để hướng dẫn bản
student đang train, vốn không được xem gold trong input. Gold vẫn là label
cho CE như bình thường. Không cần bộ rationale private gán nhãn sẵn.

Ưu tiên **SQL-only** để kiểm chứng cơ chế trên checkpoint K2 đã có. CoT là
extension ở mục 8, không được ngầm gộp vào kết quả hoặc chi phí của bản này.

Các tỷ lệ dưới đây là **ước lượng chủ quan phục vụ phân bổ compute**, không
phải xác suất rút ra từ thống kê các paper, confidence interval, hay xác suất
acceptance của một journal. Nếu cần một con số: khoảng **30% cho gain hữu ích**
và **15% cho một manuscript framework Q3 có evidence và contribution đủ rõ**.

| Sự kiện được ước lượng, tính từ trạng thái hiện nay | Khoảng chủ quan |
|---|---:|
| Pilot chạy đúng, ổn định trên hai A5000, không paging | 80–90% |
| Sau đủ ba private rounds, Spider tăng ít nhất 1 điểm phần trăm so với Hinton K2AAA, lợi ích tái lập trên các seed xác nhận | 20–35% |
| H-P hơn G-P trên Spider ở confirmation, effect dương và paired 95% CI loại 0, với cùng private self-KD | 15–30% |
| Đồng thời đạt terminal gain ở hàng 2, teacher effect ở hàng 3, phân tích federation và khác biệt đủ rõ với prior art để viết manuscript framework Q3 đáng tin | 10–20% |

Giả định: giữ model, dữ liệu và hai GPU hiện tại; một pilot, tối đa một sửa đổi
cơ chế có lý do từ diagnostic, rồi mới quyết định đầu tư confirmation. Các
sự kiện có tương quan; **không nhân bốn tỷ lệ**. Đây không phải luật giới hạn
exploration của dự án. Nếu đổi model, chuyển CoT hoặc mở rộng search, phải
đánh giá lại, không giữ nguyên các tỷ lệ này.

Lý do chưa đánh giá cao: gold CE đã cung cấp đáp án; tutor có thể chỉ lặp
lại nhãn hoặc đưa phân phối sai trên một SQL prefix không thể sửa. Bản
SQL-only không hưởng lợi từ các bước reasoning dài như nhiều benchmark
OPSD. Novelty cũng là một nút thắt riêng, không tự được giải quyết bằng EX.

## 2. Evidence hiện có và giới hạn

Snapshot nested repository: **`5cfd646`**, seed 0, Coder-1.5B, k5 alpha 0.1.
K2 là hai public epochs liên tục từ base; A là một local epoch mỗi client
rồi FedAvg. P2.37 hiện chỉ có Hinton K2AAA trong checkout, chưa có gold K2AAA.

| Checkpoint Hinton | Spider EX | BIRD EX |
|---|---:|---:|
| K2 | 62.28 | 43.61 |
| K2 → A1 | 71.57 | 36.77 |
| K2 → A1 → A2 | 71.86 | 38.66 |
| K2 → A1 → A2 → A3 | **72.53** | **38.53** |

Nguồn: [receipt K2](../../fedicl-sql/audits/protocol_v2/p237_phase_e_s0/p237_hinton_k2aaa_k2_s0_receipt.json),
[A1](../../fedicl-sql/audits/protocol_v2/p237_phase_e_s0/p237_hinton_k2aaa_a1_s0_receipt.json),
[A2](../../fedicl-sql/audits/protocol_v2/p237_phase_e_s0/p237_hinton_k2aaa_a2_s0_receipt.json),
[A3](../../fedicl-sql/audits/protocol_v2/p237_phase_e_s0/p237_hinton_k2aaa_a3_s0_receipt.json);
[Spider final](../../fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20261012T002922__d8d21413d6bd__a618e38f16da466ea5c9035fe70cceae/metrics.json),
[BIRD final](../../fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20261012T005429__0e7106cd95ac__dd86990edd4e42f9b04eadb0fff1db14/metrics.json).
Receipts dẫn tới config, metrics và hashes adapter; các thư mục eval giữ
config và predictions. Weights nằm trên GPU server.

K2AAA hơn [h_plain](../../fedicl-sql/audits/protocol_v2/p229_h_plain_s0/summary.md)
0.77 Spider nhưng thấp hơn 1.43 BIRD. Đây là so recipe, chưa tách riêng vị trí K.
Kết quả đủ để ưu tiên K-first, chưa chứng minh teacher hơn public gold
pretraining, chưa kiểm local self-KD và hoàn toàn chưa kiểm CoT.

## 3. Literature thay đổi đánh giá như thế nào?

Tìm kiếm có mục tiêu, không phải systematic review. Đã đối chiếu full text
và metadata primary tới ngày trên; không tuyên bố bao phủ toàn bộ literature.

| Prior gần | Điều đã có | Hệ quả cho đề xuất |
|---|---|---|
| [OPSD, ICML 2026, bản v3][opsd] | Self-teacher xem privileged solution, chấm student rollouts; dùng clipped forward KL. Qwen3-1.7B có kết quả dương. | Cơ chế local được kế thừa. Training có CoT solutions, evaluation math có thinking và nhiều samples; không phải bằng chứng SQL-only 1.5B. |
| [SDFT, ICML 2026][sdft] | Demonstration-conditioned self-teacher cho continual learning. | Qwen2.5-3B thua SFT trong thí nghiệm Science Q&A của paper. Paper báo khoảng 4 lần wall-time SFT; cả hai kết quả chưa phải dự báo cho SQL. |
| [FedSDR, ICML 2026][fedsdr] | Client rewrite đáp án bằng local model; dual LoRA học distilled/raw data, chỉ aggregate một nhánh. | Private-label self-distillation và adapter-only FL đã có; khác đề xuất ở offline sequence targets và thiết kế hai nhánh. |
| [SPEAR, preprint, v2 2026-09-27][spear] | Có federated OPSD baseline trên Qwen2.5-1.5B, LoRA r16. | Không thể claim lần đầu đưa OPSD vào FL. Collapse trong feedback setting không trực tiếp bác bỏ gold-SQL conditioning của ta. |
| [SERL-SQL, preprint, v4 2026-10-08][serl] | Self-teacher dùng execution hindsight để reweight GRPO trên SQL trajectories. | SQL self-distillation có privileged feedback cũng đã có. Khác direct KL với gold SQL; không có bằng chứng cho setup 1.5B/hai A5000 của ta. |
| [Rethinking Privileged Information, preprint 2026][rethinking] | Reference đúng không luôn tốt hơn no-reference hoặc reference khác bài. | Gain không tự chứng minh model học thông tin từ gold; cần no-hint control và counterfactual diagnostic. |

**Đính chính so với trao đổi trước:** nhận định OPSD yếu ở 1.7B dựa trên v2
không còn đại diện cho v3. Bản mới chuyển trọng tâm sang clipped forward KL.
Tuy vậy, không được chuyển gain math của Qwen3 sang kỳ vọng gain SQL của
Qwen2.5-Coder bằng phép cộng điểm.

Khoảng trống còn đáng kiểm: **LLM public bootstrap có làm local self-KD
trên schema private hữu ích hơn so với public gold bootstrap hay không?**
Chưa tìm thấy đúng toàn bộ cấu hình này trong phạm vi search. Điều đó chưa
đủ để claim novelty. Công thức local vẫn chạy được trong centralized training.

## 4. Cơ chế được đề xuất

### 4.1 Server bootstrap

Giữ nguyên Hinton K2: frozen Qwen2.5-Coder-7B-Instruct, public BIRD có nhãn
9,428 rows, hai epochs, gold CE + forward KL hiện tại. Đối chứng G dùng cùng
public rows và hai epochs gold CE, không dùng output teacher.

Pilot H dùng adapter đã có:
`artifacts/protocol_v2/p237_phase_e_s0/hinton_k2aaa_k2/m_g`.
Confirmation phải chạy lại toàn pipeline theo seed và protocol đã chốt.

### 4.2 Một round tại client

```text
Server: teacher 7B + BIRD gold → student K2 → gửi adapter

Client i: nhận global adapter θt
    frozen tutor φt := θt, giữ nguyên trong cả local round
    student θ := θt, được cập nhật
    x = private question + private schema
    y* = private gold SQL

    student hiện tại sinh một SQL rollout ŷ cho mỗi row trong microbatch
    tutor(x, reference=y*) chấm đúng các prefix của ŷ
    student học gold CE và distillation trên ŷ

Gửi adapter θi → sample-weighted FedAvg → θ(t+1)
```

Tutor là **bản sao SLM 1.5B**, không phải teacher 7B. Nó không tự sinh một
bộ rationale để SFT trong phiên bản này. Đầu mỗi round, tutor được thay bằng
snapshot global mới; việc refresh theo round là lựa chọn của đề xuất.
Rollout được sinh mới từ student hiện tại ngay trước update của minibatch;
không sinh một lần cho cả round rồi gọi đó là on-policy. Token cache chỉ
phục vụ scoring và update tương ứng, không thay việc refresh rollout.

Với response prefix giống nhau:

\[
q_n=p_{\phi_t}(\cdot\mid x,y^*,\hat y_{<n}),\qquad
p_n=p_\theta(\cdot\mid x,\hat y_{<n}).
\]

Loss dự kiến:

\[
L=L_{\mathrm{CE}}(y^*\mid x)
 +\lambda\frac{1}{|\hat y|}\sum_{n,v}
 \min\{q_n(v)[\log q_n(v)-\log p_n(v)],\tau\}.
\]

Pointwise clipping kế thừa [OPSD §3.2][opsd]; đây là clipped objective,
không gọi nó là KL chuẩn sau clipping. Stop-gradient qua tutor và sampled
token IDs; chỉ student logits nhận gradient. Align theo response token,
không theo absolute position vì hai prompt dài khác nhau.

Cấu hình screen **đề xuất**, không phải default của paper: `λ=0.1`,
`τ=1.0` cho mỗi vocabulary contribution, KD temperature 1, một sampled
SQL/row với sampling temperature 1 và top-p 1, cap 256 new tokens.
Giữ LoRA r16, optimizer/LR/batch/accumulation như A baseline; một optimizer
update sau khi cộng gradient CE và KD. `τ` không phải ratio clipping.
Trong probe, đo `||λg_KD|| / ||g_CE||` và gradient cosine giữa hai objectives
trên cùng minibatch để phân biệt tín hiệu yếu với xung đột CE. Báo fraction
vocabulary contributions bị clip, fraction response positions có clipping
và độ dài thực tế. Các giá trị này chưa được tune hoặc đo.
Prompt tutor nêu đây là SQL tham chiếu của câu đang
train; student và evaluation không nhận phần tham chiếu đó.

CE và KD là hai forward/backward microsteps với hai sequences khác nhau.
Giữ **mọi private gold row**, kể cả rollout sai; không chọn pool bằng EX.
Overflow không được silently truncate hoặc bỏ row. Nếu cần sửa context cap,
phải sửa có ghi nhận và chạy comparator tương ứng. Output lỗi format hoặc
đụng cap vẫn được ghi nhận, không tính là thành công.

### 4.3 Vì sao có thể có ích, và vì sao có thể không?

Đây là giả thuyết: gold context giúp tutor tạo soft targets phù hợp hơn với
sample private, còn CE giữ supervision đúng. Khác student-prefix KD với
cùng input, teacher context ở đây đã khác ngay tại token đầu tiên.

Nhưng gold SQL có thể biến tutor thành máy chép đáp án. Khi prefix đã chọn
sai bảng, tutor cũng không thể sửa token đã sinh. Model có thể học aliases,
style hoặc độ tự tin thay vì semantic SQL. Vì vậy, đây là nghiên cứu
**private adaptation**, chưa được gọi là internalized reasoning.

Private question/schema/gold/rollout/logits ở lại client; chỉ adapters và
aggregate metrics di chuyển. Deployment chỉ có student, SQL-only, greedy
như baseline. Giữ định nghĩa privacy là structural data isolation, không DP.

## 5. Những comparator tối thiểu

H = Hinton K2; G = gold-CE K2; C = private gold CE; P = CE + privileged KD.

| Arm | Public stage | Ba private rounds | Contrast nó phục vụ |
|---|---|---|---|
| H-C | Hinton K2 | CE | Baseline K2AAA hiện có |
| H-P | Hinton K2 | CE + privileged KD | Self-KD có thêm ích sau H không? |
| G-C | Gold K2 | CE | Public data control |
| G-P | Gold K2 | CE + privileged KD | Server teacher còn cần không? |
| H-N | Hinton K2 | CE + self-KD, tutor không thấy gold | Gold context có hơn regularization thông thường không? |

Cùng private rows, số epochs, optimizer updates, LoRA và evaluation.
H-N giữ pipeline rollout/scoring như H-P; prompt giữ cùng hướng dẫn và bỏ
reference. Không gọi CE và self-KD là compute-matched: self-KD có thêm
generation và forward. Nếu có gain, cần thêm CE control được cấp cùng
compute budget; báo số passes mới của control đó, không giả vờ vừa matched
compute vừa matched exposure.

Ba phép so cần tách riêng:

- `H-P − H-C`: lợi ích thêm local self-KD.
- `H-P − G-P`: đóng góp teacher cho toàn pipeline.
- `I = (H-P − H-C) − (G-P − G-C)`: interaction cần để nói teacher
  bootstrap làm local self-KD hữu ích hơn. Hai gain dương riêng lẻ không đủ.

Nếu H-P chỉ hơn H-C nhưng không hơn H-N, chưa quy gain cho gold context.
Nếu H-P và G-P tương đương về effect/uncertainty, không claim teacher thiết yếu.
Non-significant không đồng nghĩa equivalent.

## 6. Chạy theo từng bước, dừng sớm khi không có tín hiệu

Các mốc sau là **decision guidance cho exploration**, không phục hồi những
pass/fail rules đã retired. Chưa có lệnh chạy mới trong proposal.

1. **Probe tutor và memory:** cố định 64 training rows/client, phân tầng độ
   dài và SQL constructs, thêm longest-example probe. Từ cùng checkpoint và
   cùng rollout, chấm bằng tutor có gold, không gold và gold của câu khác.
   Giữ instruction giống nhau; mismatch chọn trong cùng client, ưu tiên
   cùng DB và độ dài tương tự, không tráo gold giữa các client.
   Đo loss/entropy/clipping, lỗi parse, throughput và peak reserved/shared
   memory qua cả backward + optimizer. Kiểm tay một số quyết định table,
   JOIN, aggregation; không lấy gold likelihood tăng làm bằng chứng thành công.
2. **Một private round:** chạy H-P và H-N, so với H-C A1. Lưu từng client
   adapter và model sau aggregation. Eval Spider và BIRD dev; báo paired
   wins/losses, exact McNemar và CI. Có tín hiệu hữu ích sau aggregation
   mới đáng cấp compute cho phần tiếp; một round không chứng minh terminal gain.
3. **Hoàn tất AAA và gold controls:** chạy tiếp H-P/H-N; bổ sung G-P và G-C
   theo cùng recipe. Đọc interaction và trajectory sau từng round, tránh
   chọn riêng checkpoint cao nhất làm headline. Thêm compute-budget CE
   control nếu gain vẫn còn.
4. **Chẩn đoán federation rồi mới confirmation:** so local checkpoints,
   FedAvg và matched centralized H/G × C/P; thêm alpha 0.5 nếu claim liên
   quan heterogeneity. Không gọi aggregation loss hay client drift chỉ từ
   việc FL thấp hơn central. Trước claim framework mới, cần một comparator
   federated self-distillation gần như FedSDR trên cùng student/budget,
   ghi rõ mọi adaptation; matrix trên chỉ tách cơ chế, chưa thay thế được
   related-method baseline. Xác nhận cuối tuân theo mục 9.

**Lý do dừng hoặc thu hẹp:** không chạy được dưới memory cap; gold-context
không tạo lợi ích downstream hơn H-N; gain chỉ có sau A1 rồi mất ở AAA;
extra CE compute giải thích hết gain; hoặc G-P làm tốt như H-P khiến mục
tiêu server teacher không còn evidence. Một thất bại của cấu hình này chỉ
bác cấu hình này, không chứng minh mọi self-distillation đều vô ích.

Probe dùng training rows là diagnostic đã nhìn nhãn, không phải validation
hay generalization evidence. Nếu tạo private holdout mới để đánh giá từng
client, phải giữ holdout local và rerun matched baselines trên cùng split;
không retrofit vào checkpoints cũ.

## 7. Compute trên hai RTX A5000

P2.37 đã đo, không phải dự báo:

| Stage | Training time | Peak reserved VRAM |
|---|---:|---:|
| Hinton K2 | 7.28 GPU-h | 19.89 GiB |
| Private A1 / A2 / A3 | 2.36 / 2.57 / 1.63 GPU-h | khoảng 14.19 GiB |
| Tổng K2AAA training | **13.84 GPU-h** | Không cộng peak giữa stages |

Nguồn: [metrics K2](../../fedicl-sql/experiments/federated/results/federated_stage__K2fkl__s0__132e798a5be2__8393f0f9/metrics.json)
và result directories trong receipts A1–A3 ở mục 2. Chưa cộng evaluation;
đây là một run dưới tải thực tế, không phải tốc độ ổn định của phần cứng.
K2 dùng teacher-logit cache đã có. Các số này loại trừ chi phí tạo cache
7B ban đầu; paper resource table phải báo riêng chi phí một lần và cách
phân bổ qua các runs dùng chung cache.

Kịch bản lập ngân sách, **chưa đo**: nếu local self-KD tốn 2–4 lần A hiện
tại, ba private rounds tốn khoảng 13–26 GPU-h. Từ base, cộng K2 thành
khoảng **20–34 GPU-h/arm**, dùng lại public cache, chưa eval và debug. Hai arm local mới ở bước 2
khoảng 9–19 GPU-h theo A1 hiện tại; smoke sẽ thay thế dự báo này.
Không chia GPU-hours cho hai để hứa wall-time, vì các round phụ thuộc nhau
và hai card cùng bận đã từng chậm hơn.

Đường triển khai cần response-window logits, `target_fp32` cho CE,
gradient checkpointing, tutor no-grad, generation/scoring/CE/KD tách pha.
Có thể share frozen base với hai LoRA adapters; đây là phương án kỹ thuật
chưa smoke, không phải bảo đảm VRAM. Không cache full-vocabulary logits cho
toàn private pool; stream theo microbatch, chỉ giữ token IDs/receipt local.
Nếu dùng top-k approximation thì đó là variant phải khai báo, không tự thay
vào objective đã mô tả.

Gate bắt buộc: peak reserved dưới khoảng 21.5 GiB, shared GPU memory gần 0,
probe cả prompt teacher có thêm gold SQL và backward + optimizer. Giữ
execution timeout BIRD 30 s, Spider 60 s; không giảm timeout để cứu runtime.
Không đưa teacher 7B vào client, không cần teacher 14B/32B.

## 8. CoT nằm ở đâu trong hướng này?

CoT **không phải điều kiện để bản SQL-only chạy**. Chỉ mở một extension
riêng nếu tutor diagnostic hoặc outcome cho lý do cụ thể để thêm reasoning.

Extension: public teacher tạo short rationales, student học cả solve và
gold-conditioned rationalization; client tutor sau đó chấm student rollouts
`rationale → SQL`. [Rationalization Models for Text-to-SQL][rationalization]
là nguồn cho answer-conditioned rationalization, không phải bằng chứng
1.5B hoặc FL sẽ hiệu quả. Phải có public SQL-only và matched-budget controls.

Extension đổi output contract và cần đặc tả loss mới trước implementation.
Không vừa yêu cầu student sinh rationale vừa dùng SQL-only CE với cùng
prompt mà bỏ qua conflict. Không train trên rationale sai rồi gọi gold SQL
sau nó là faithful reasoning. Execution đúng chỉ kiểm outcome, không kiểm
lập luận. Không bỏ private rows vì rationale không qua lọc.

Nếu thay online logit KD bằng generate/filter/cache rationale rồi CE, đó là
sequence self-distillation gần STaR/FedSDR, phải ghi là method khác. Các xác
suất và budget ở mục 1, 7 không tự áp dụng cho extension này.

## 9. Claim, confirmation và quyết định cuối

**Novelty hiện tại: thấp đến trung bình, chưa đủ để chốt paper story.**
Các thành phần đều đã có nguồn. Đóng góp tiềm năng là evidence cho việc
public LLM bootstrap mở khả năng private adaptation của một SLM nhỏ dưới
giới hạn schema isolation và compute, kèm điều kiện nó có hoặc không có ích.
Chỉ chuyển OPSD sang SQL hoặc ghép thêm FedAvg chưa đủ novel framework.

| Kết quả sau controls và confirmation | Cách diễn giải được phép |
|---|---|
| Gain cuối, H-P hơn G-P, interaction dương, lợi ích qua aggregation và phân tích heterogeneity | Có cơ sở phát triển claim public-teacher bootstrap hỗ trợ private self-KD; còn phải đối chiếu prior và scope journal |
| H-P hơn H-C nhưng G-P cũng có cùng gain | Local self-KD hữu ích; chưa chứng minh bootstrap teacher tạo ra lợi ích đó |
| H-P hơn G-P, interaction chưa rõ | Teacher có giá trị trong pipeline; chưa claim synergy giữa hai stages |
| Chỉ seed 0 dương hoặc chỉ checkpoint giữa dương | Kết quả exploratory; chưa đủ claim terminal improvement |
| Teacher không có lợi ích đo được | Không đáp ứng mục tiêu teacher-contributing framework hiện tại |

Trước seed 1–2 hoặc Spider test: ghi entry có ngày trong LAB_LOG chốt
recipe, comparator, endpoint, số seed theo power check, statistical test và
claim cho từng outcome. Seed-0 dev dùng chọn phương pháp là exploratory;
không dùng chính gain đã chọn làm confirmation độc lập. Gộp seed bằng
question-clustered test theo R13, không cộng discordant pairs như các quan
sát độc lập. Báo Spider/BIRD, robustness, compute và tất cả biến thể đã thử;
không thêm seed vì p-value chưa đẹp. Đích +1 điểm ở mục 1 định nghĩa sự kiện
được ước lượng, không phải ngưỡng bảo đảm significance hay journal acceptance.

Đánh giá này đã có phản biện từ một agent riêng trên cùng bối cảnh, không
phải external peer review. Phản biện chính đã được giữ lại: small-model
capacity chưa biết, gold-context có thể dư thừa, và framework novelty yếu.
**Khuyến nghị: làm bước 1, sau đó quyết định bước 2; chưa cam kết full matrix.**

## 10. Nguồn primary và phạm vi đọc

- **OPSD:** Zhao et al., *Self-Distilled Reasoner*, [ICML 2026 proceedings](https://proceedings.mlr.press/v306/zhao26be.html).
  Nội dung phương pháp đối chiếu [arXiv v3, 2026-03-20][opsd], §3.2,
  §4.1–4.3, Appendix B. Không lấy recipe JSD của v2 làm default hiện tại.
- **SDFT:** Shenfeld et al., *Self-Distillation Enables Continual Learning*,
  [ICML 2026 proceedings](https://proceedings.mlr.press/v306/shenfeld26a.html);
  [v2][sdft], §4.4 và §5 cho scaling/cost.
- **FedSDR:** Ren et al., [ICML 2026 proceedings](https://proceedings.mlr.press/v306/ren26n.html);
  [full text][fedsdr], §4.2–4.4 và §5.
- **SPEAR:** *Self-Play Enhancement via Advantage-Weighted Refinement in Online
  Federated LLM Fine-Tuning*, [v2][spear], §5, Table 1, Appendix C.2/Table 22.
  Chỉ xác minh preprint, không gán venue.
- **SERL-SQL:** *Selective Hindsight Distillation for Text-to-SQL Reinforcement
  Agentic Learning*, [v4][serl], phần execution-hindsight teacher và setup.
  Chỉ xác minh preprint.
- **Rethinking Privileged Information in On-Policy Self-Distillation:**
  [v1, 2026-08-18][rethinking], abstract và §4; counterevidence về reference.
- **Rationalization Models for Text-to-SQL:** [full text][rationalization],
  phương pháp và thí nghiệm; nguồn cho extension, không cho core SQL-only.

Các truy vấn định hướng gồm `on-policy self-distillation text-to-SQL`,
`federated self-distillation privileged`, cùng tên paper và các bản mới của
OPSD/SDFT. Primary sources được dùng để kiểm claim; search không đầy đủ nên
không suy ra “chưa ai làm” từ việc chưa tìm thấy.

[opsd]: https://arxiv.org/html/2601.18734v3
[sdft]: https://arxiv.org/html/2601.19897v2
[fedsdr]: https://arxiv.org/html/2605.18028v1
[spear]: https://arxiv.org/html/2605.07977v2
[serl]: https://arxiv.org/html/2608.00485v4
[rethinking]: https://arxiv.org/html/2608.18271v1
[rationalization]: https://arxiv.org/html/2502.06759v1
