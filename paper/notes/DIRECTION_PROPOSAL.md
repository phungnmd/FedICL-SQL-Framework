# Proposal: K-first bootstrap, shortlist KD và private adaptation

Ngày đánh giá: **2026-10-12**. Dự án: **FedLS-SQL**.
Trạng thái: **đề xuất nghiên cứu, chưa chọn làm method, chưa triển khai hay chạy GPU**.
File này tổng hợp **4 nhóm nghiên cứu, 5 phương án thử**, gồm hướng privileged
OPSD của bản trước. Không thay [run queue](PIPELINE_NEXT.md), không chốt method
và không tự cấp phép chạy experiment.

## 1. Quyết định và xác suất thành công

**Thử freeze LoRA factor trước vì ít tốn compute; giữ FedDAT làm ứng viên
framework chính.** TAID là nhánh cải thiện bootstrap; RoLoRA là biến thể nếu
freeze cố định làm thiếu khả năng adaptation. Privileged OPSD vẫn đáng pilot,
nhưng không có bằng chứng nó sẽ tốt hơn các phương án rẻ hơn.

Theo định hướng owner: **paper ứng dụng Q3 có thể adapt cơ chế đã công bố**.
Không bắt buộc phát minh loss mới. Cần lý do phù hợp Text-to-SQL federated,
teacher contribution đo được, controls và evidence đủ rõ; không suy ra chất
lượng paper chỉ từ việc ghép tên các phương pháp hoặc một dev score cao.

Các tỷ lệ dưới đây là **ước lượng chủ quan chưa được calibration**, phục vụ
phân bổ compute theo trao đổi ngày 2026-10-12. Không phải thống kê từ paper,
confidence interval, xác suất journal accept hoặc kết quả pilot đã chạy.

| Nhóm / phương án | Gain hữu ích, tái lập được | Đủ evidence phát triển manuscript Q3 tốt | Lý do và ưu tiên |
|---|---:|---:|---|
| 1. K-first + FedDAT | **35–50%** | **25–40%** | Cơ chế global/local rõ, dùng private gold trực tiếp; ứng viên framework chính, adaptation sang SQL và compute chưa kiểm |
| 2a. K-first + freeze LoRA factor | **30–45%** | **20–35%** | Pilot đầu tiên, không thêm model forward; rủi ro underfit schema private |
| 2b. K-first + RoLoRA | **30–45%** | **20–35%** | Cùng nhóm factor-wise adaptation; thử nếu cần cả hai factor thích nghi, chỉ ba rounds nên evidence chưa rõ |
| 3. K-first + TAID | **30–45%** | **20–35%** | Thay objective ở bootstrap, không sinh thêm data; gain có thể mất sau private AAA |
| 4. K-first + privileged OPSD | **25–40%** | **15–30%** | Hướng trong proposal trước; phụ thuộc chất lượng gold-conditioned tutor 1.5B và rollout cost |

Định nghĩa chung để đọc bảng:

- **Gain hữu ích:** khoảng ít nhất +1 điểm phần trăm Spider EX sau toàn bộ
  AAA so với Hinton K2AAA hiện tại, lợi ích tái lập ở confirmation. Luôn báo
  BIRD và trade-off; +1 điểm không tự bảo đảm significance.
- **Đủ evidence:** ngoài gain, teacher có lợi ích so với matched gold
  bootstrap, ablation hỗ trợ cách giải thích, compute phù hợp và đủ cơ sở
  viết manuscript ứng dụng. Không bắt buộc interaction dương nếu không
  claim synergy giữa bootstrap và private method.
- Ước lượng từ trạng thái hiện nay, giữ student/teacher, data và hai A5000;
  một pilot và tối đa một sửa đổi có lý do trước khi quyết định confirmation.
  Đây là giả định lập ngân sách, không giới hạn exploration của owner.

Các khoảng chồng lấn vì chưa biết hướng nào dễ tăng EX hơn. Thứ tự thử dựa
vào chi phí và câu hỏi cần trả lời, không phải thứ hạng efficacy đã đo.
Các hướng chung baseline và rủi ro teacher-vs-gold: **không cộng/nhân các %
để tính xác suất ít nhất một hướng thành công**. Các khoảng OPSD mới thay
ước lượng ở bản trước theo tiêu chí applied Q3 đã làm rõ, không do có thêm
kết quả GPU. Đổi model/data/CoT hoặc ngân sách phải đánh giá lại.

Setup chung: teacher 7B chỉ ở server trên public BIRD có gold; private
question/schema/gold ở client; không cần SynSQL hay pool không nhãn. Deploy
một global SLM, SQL-only, greedy. CoT là extension của OPSD ở mục 9, không
tính thành phương án thứ sáu.

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

## 3. Cơ chế, rủi ro và pilot của từng hướng

### 3.1 K-first + FedDAT: local tutor thích nghi cùng shared model

Nguồn: [FedDAT, AAAI 2024][feddat] và [official trainer][feddat-code].
Paper gốc là vision-language; chuyển sang LoRA causal LM là adaptation của
ta, chưa có kết quả SQL. Có ba adapter states dùng chung frozen backbone:

- `S`: shared adapter trainable, nhận từ server mỗi round, được aggregate
  và deploy độc lập.
- `F`: frozen snapshot của `S` đầu round, refresh ở round tiếp theo.
- `C`: local adapter trainable, giữ riêng từng client qua các round.

Tutor DAT kết hợp residual `0.5 B_F A_F + 0.5 B_C A_C` ở mỗi LoRA layer
(cùng scaling LoRA), không average A/B riêng và không ensemble logits.
`S` và DAT học gold CE cùng mutual KD. Theo code gốc, KD là
`KL(target || student)` với temperature 3, dùng detached targets. Adaptation
SQL tính CE/KD trên response tokens, normalize theo số token, cùng gold
prefix; không rollout, không gold hint trong input, không rationale.

Đề xuất initialize `S/F/C` từ K2 ở lần đầu, rồi giữ `C` local. Warm-start
`C` là lựa chọn của ta: nhánh zero cộng với nhánh K2 theo tỷ lệ 1/2 sẽ làm
thay đổi ngay hàm bootstrap. Chỉ `S` rời client; tutor 1.5B không phải LLM
7B. Code gốc dùng 3 forward và 2 backward mỗi minibatch; target shared cho
DAT dùng logits trước update. Chưa coi recipe đó là code đã có trong repo.

**Giả thuyết:** local specialist giúp shared student tiếp thu private gold
mà vẫn khai thác kiến thức global. **Rủi ro:** frozen snapshot cản adaptation,
local overfit, hoặc thêm compute không giúp EX. Snapshot refresh mỗi round
không bảo đảm giữ nguyên kiến thức K2. Evidence gốc xa autoregressive SQL
hơn evidence LLM nhỏ của OPSD; không xếp FedDAT cao vì đã chứng minh dễ thắng.

**Pilot:** cùng Hinton K2, một private round FedDAT so với CE hiện có;
eval shared `S` sau FedAvg, giữ local checkpoints để diagnostic. Nếu có
tín hiệu, hoàn tất AAA và gold-bootstrap control. Comparator bổ sung đầu
tiên là frozen-global full-KL tại cùng K2 parent; sau đó mới ablate mutual
KD thành một chiều và kiểm compute-budget CE. Nếu claim gain đến từ mutual
KD, thêm ablation giữ các nhánh và lịch CE updates nhưng bỏ KD, báo compute
để tách tác dụng KD khỏi architecture/extra optimization. Không cần chạy
control này ngay ở pilot. Không lấy FedNTD all-A từ
parent khác để kết luận đã tách riêng tác dụng FedDAT. Hạ ưu tiên nếu chỉ
giữ BIRD bằng cách hại Spider hoặc không hơn regularization đơn giản hơn.

### 3.2 K-first + freeze factor: học trước rồi giới hạn private update

Nguồn: [FFA-LoRA, ICLR 2024][ffa], với precedent học trước rồi freeze trong
[RoLoRA §5.3][rolora]. Theo notation PEFT, `ΔW = (α/r) B A`; A là down
projection, B là up projection. Sau K2 học cả hai factor, **freeze A_K,
train B từ B_K** bằng private gold CE, aggregate B theo sample weights:

\[
\sum_i w_i B_i A_K = (\sum_i w_i B_i) A_K.
\]

FFA gốc freeze random A từ đầu; dùng A đã học qua public KD là adaptation
cần kiểm. Không zero B sau K2, vì sẽ xóa bootstrap. Không merge K2 vào
backbone rồi thêm adapter mới nếu đang kiểm learned factor hiện có.

**Giả thuyết:** factor chung giới hạn local update và làm average LoRA
weight updates chính xác. **Rủi ro:** BIRD basis không đủ cho Spider; B thay
đổi vẫn có thể làm mất kiến thức teacher. Exact weight averaging không
đồng nghĩa function ensemble, EX tốt hơn hoặc giải quyết client drift.
Chưa có bằng chứng aggregation là bottleneck chính của K2AAA hiện tại.

**Pilot:** Hinton K2 + freeze-A một round so với Hinton K2 + full-LoRA CE;
nếu đáng theo thì hoàn tất AAA và lặp với gold K2. Không thêm forward,
generation hay private logits cache. Chưa hứa giảm một nửa VRAM/wall-time;
chỉ có communication savings nếu thực sự truyền B-only. Matrix H/G ×
full/frozen kiểm recipe và teacher contribution, chưa cô lập chất lượng A;
claim “teacher học basis tốt hơn” cần thiết kế giữ cùng starting function.

### 3.3 K-first + RoLoRA: luân phiên factor qua các round

[RoLoRA, NeurIPS 2025][rolora] train một factor mỗi round, giữ factor còn
lại chung và frozen. Variant dự kiến sau K2: round 1 train B, round 2 train
A, round 3 train B; giữ exact weight averaging ở từng round nhưng cho basis
thích nghi. Đây là phương án 2b của nhóm factor-wise adaptation.

**Pilot:** ưu tiên khi freeze-A cho dấu hiệu underfit; so với full-LoRA và
freeze-A cùng parent. Lợi ích của đổi factor phải đọc sau round 2 và AAA,
không thể phân biệt bằng round 1. B được train hai round, A một round;
báo rõ exposure này, không gọi contrast là cùng lịch train factor. Paper
gốc chạy nhiều rounds và code-generation gain nhỏ; không suy ra gain SQL.
Chi phí forward như CE; không mặc định thêm rounds để làm đẹp lịch luân phiên.

### 3.4 K-first + TAID: cải thiện objective của public bootstrap

[TAID, ICLR 2025][taid] dùng target trung gian từ logits student detached
và teacher, tăng dần ảnh hưởng teacher theo tiến độ thích nghi. Thử thay
Hinton term ở K2 bằng TAID, giữ gold CE, cùng public rows/hai epochs, rồi
private AAA plain. Dùng implementation/schedule của paper làm điểm xuất
phát; hằng số cụ thể phải chốt khi đặc tả pilot, chưa có default mới ở đây.

**Giả thuyết:** student học teacher tốt hơn trước khi vào FL. Không thêm
student rollout hay model forward so với cached Hinton; cache chỉ tái dùng
nếu đủ logits, đúng tokenizer/prefix/temperature representation và identity.
**Rủi ro:** gap ở K2 có thể bị private adaptation xóa; chưa có diagnostic
cho thấy capacity gap là nguyên nhân hạn chế Hinton hiện tại.

**Pilot:** TAID K2AAA so với Hinton K2AAA và gold K2AAA, giữ gold-CE weight
và exposure; đọc cả K2 lẫn endpoint AAA. Không ghép ngay với FedDAT/freeze,
để biết gain đến từ đâu. SQL đã có [reverse KL + dynamic α scheduler, 2025][sql-dynamic];
cần cite và so objective, không claim adaptive mixing mới cho SQL. Điều
này không loại một framework ứng dụng có evidence tốt.

### 3.5 K-first + privileged OPSD: self-teacher xem private gold SQL

Giữ hướng của proposal trước: local frozen student được xem gold SQL làm
reference, chấm rollout của student không thấy reference. Student học gold
CE + clipped forward KL. Chi tiết, controls và probe riêng ở mục 5–7.

**Giả thuyết:** gold context tạo soft targets hữu ích hơn tutor không hint.
**Rủi ro:** gold CE đã cung cấp đáp án; tutor chỉ copy nhãn hoặc chấm một SQL
prefix không thể sửa; thêm on-policy generation. OPSD v3 có evidence dương
ở 1.7B, nên không hạ điểm dựa trên v2 cũ. Chưa có evidence SQL-only 1.5B.
Ưu tiên SQL-only trước, CoT chỉ là extension riêng có controls.

FedSDR đã được screen nhưng **ngoài shortlist ưu tiên**: cần rewrite rồi
train hai LoRA streams; phải kiểm R-only khi deployment bỏ S vì lúc train
R có S cùng hoạt động. Không lấy local R+S score làm global-model evidence.
Chưa thấy nó đáng ưu tiên hơn FedDAT dưới budget hiện tại [FedSDR][fedsdr].

## 4. Literature gần privileged OPSD và giới hạn search

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

Khoảng trống còn đáng kiểm: **public teacher đóng góp thế nào cho private
adaptation của một SLM federated, khi teacher không được thấy schema private?**
Targeted search chưa tìm thấy ứng dụng trực tiếp FedDAT/FFA/RoLoRA đúng setup
Text-to-SQL này; không đủ để claim “first”. Federated Text-to-SQL đã có
[ACL 2023][fed-semparse]. Công thức local của OPSD cũng chạy được centrally;
điều này giới hạn claim cơ chế federation mới, không tự loại paper ứng dụng.

## 5. Đặc tả riêng privileged OPSD

### 5.1 Server bootstrap

Giữ nguyên Hinton K2: frozen Qwen2.5-Coder-7B-Instruct, public BIRD có nhãn
9,428 rows, hai epochs, gold CE + forward KL hiện tại. Đối chứng G dùng cùng
public rows và hai epochs gold CE, không dùng output teacher.

Pilot H dùng adapter đã có:
`artifacts/protocol_v2/p237_phase_e_s0/hinton_k2aaa_k2/m_g`.
Confirmation phải chạy lại toàn pipeline theo seed và protocol đã chốt.

### 5.2 Một round tại client

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

### 5.3 Vì sao có thể có ích, và vì sao có thể không?

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

## 6. Comparator chung và controls riêng OPSD

Với local method được chọn M (FedDAT, freeze factor, RoLoRA hoặc OPSD),
matrix gọn là **H-C, H-M, G-C, G-M**: H/G là Hinton/gold K2, C là private
full-LoRA CE. `H-M − H-C` kiểm local method, `H-M − G-M` kiểm teacher trong
pipeline cuối. Interaction chỉ bắt buộc cho claim synergy, không là điều
kiện mặc định của manuscript ứng dụng. TAID thay stage K nên dùng ba arm
TAID K2AAA, Hinton K2AAA, gold K2AAA trước khi ghép local method.

Không chạy toàn bộ matrix cho cả năm phương án từ đầu. Bảng dưới là
controls **riêng OPSD**, giữ lại để có thể triển khai nếu chọn hướng này.

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

## 7. Thứ tự pilot và khi nào thu hẹp

Các mốc sau là **decision guidance cho exploration**, không phục hồi những
pass/fail rules đã retired. Chưa có lệnh chạy mới trong proposal.

### 7.1 Lộ trình chung cho shortlist

1. Reuse Hinton K2 đã có; smoke và chạy freeze-A một private round. Mỗi
   GPU path mới phải đo longest example qua backward + optimizer.
2. Screen FedDAT từ cùng Hinton K2; giữ local adapters và eval shared model
   sau FedAvg. Đọc Spider và BIRD, không chỉ local training loss.
3. Phương án có tín hiệu hữu ích mới hoàn tất AAA và gold-bootstrap pair;
   paired seed-0 dev contrasts chỉ phục vụ exploration. Nếu freeze underfit,
   cân nhắc RoLoRA; TAID là nhánh bootstrap riêng; OPSD dùng probe ở dưới.
4. Sau khi chọn candidate, thêm ablation/related-method comparator sát với
   claim. Nếu phương pháp tốn hơn CE, kiểm compute-budget CE khi đã có gain;
   không gọi vừa compute-matched vừa exposure-matched nếu số passes khác.
5. So local checkpoints và FedAvg để phân biệt local forgetting với loss
   sau aggregation. Centralized control và alpha 0.5 chỉ cần theo claim về
   FL penalty hoặc heterogeneity, không mở cả matrix mặc định cho mọi pilot.
   Freeze recipe/claims trước confirmation theo mục 10.

Hạ ưu tiên nếu gain chỉ có giữa chuỗi, chỉ giữ BIRD bằng cách làm hại Spider,
hoặc thêm compute mà không hơn comparator đơn giản. Nếu teacher-vs-gold
chưa rõ, kết luận chưa có evidence, không gọi hai phương án equivalent.

### 7.2 Probe và các bước riêng nếu chọn OPSD

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
4. **Controls theo claim rồi confirmation:** so local checkpoints và FedAvg;
   thêm matched centralized H/G × C/P nếu claim lợi ích riêng federation,
   alpha 0.5 nếu claim tác dụng heterogeneity. Không gọi client drift chỉ từ
   FL thấp hơn central. Chọn related-method comparator phù hợp, FedSDR là
   ứng viên cần đánh giá adaptation/cost, không là điều kiện bắt buộc cho
   mọi pilot. Matrix trên tách cơ chế, không thay toàn bộ baseline cho paper.
   Xác nhận cuối tuân theo mục 10.

**Lý do dừng hoặc thu hẹp:** không chạy được dưới memory cap; gold-context
không tạo lợi ích downstream hơn H-N; gain chỉ có sau A1 rồi mất ở AAA;
extra CE compute giải thích hết gain; hoặc G-P làm tốt như H-P khiến mục
tiêu server teacher không còn evidence. Một thất bại của cấu hình này chỉ
bác cấu hình này, không chứng minh mọi self-distillation đều vô ích.

Probe dùng training rows là diagnostic đã nhìn nhãn, không phải validation
hay generalization evidence. Nếu tạo private holdout mới để đánh giá từng
client, phải giữ holdout local và rerun matched baselines trên cùng split;
không retrofit vào checkpoints cũ.

## 8. Compute trên hai RTX A5000

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

| Phương án | Công việc thêm so với Hinton K2AAA | Điều chưa được đo |
|---|---|---|
| Freeze factor / RoLoRA | Không thêm model forward hay generation; đổi factor trainable | Wall-time, VRAM, bytes truyền thực tế; không hứa giảm một nửa |
| FedDAT | Code gốc 3 forward + 2 backward/minibatch thay vì CE 1 + 1; ba adapter states | SQL-vocabulary logits/activations, throughput và memory của shared-backbone implementation |
| TAID | Thay loss/schedule K2, không thêm model forward so với cached Hinton | Cache compatibility, loss overhead, tổng thời gian train lại K2 |
| Privileged OPSD | Rollout online, tutor scoring, gold CE và rollout KD | Độ dài SQL thật, generation/scoring cost, peak VRAM với gold hint |

Mọi hàng là phân tích cơ chế, **chưa phải benchmark trên hai A5000**. Ba
adapter states của FedDAT không có nghĩa ba bản backbone; vẫn cần smoke
sequential forward/backward. Không suy ra thời gian từ số forward đơn thuần.

Kịch bản lập ngân sách **riêng OPSD, chưa đo**: nếu local self-KD tốn 2–4 lần A hiện
tại, ba private rounds tốn khoảng 13–26 GPU-h. Từ base, cộng K2 thành
khoảng **20–34 GPU-h/arm**, dùng lại public cache, chưa eval và debug. Hai arm local mới ở mục 7.2 bước 2
khoảng 9–19 GPU-h theo A1 hiện tại; smoke sẽ thay thế dự báo này.
Không chia GPU-hours cho hai để hứa wall-time, vì các round phụ thuộc nhau
và hai card cùng bận đã từng chậm hơn.

Đường triển khai OPSD cần response-window logits, `target_fp32` cho CE,
gradient checkpointing, tutor no-grad, generation/scoring/CE/KD tách pha.
Có thể share frozen base với hai LoRA adapters; đây là phương án kỹ thuật
chưa smoke, không phải bảo đảm VRAM. Không cache full-vocabulary logits cho
toàn private pool; stream theo microbatch, chỉ giữ token IDs/receipt local.
Nếu dùng top-k approximation thì đó là variant phải khai báo, không tự thay
vào objective đã mô tả.

Gate mọi GPU path mới: peak reserved dưới khoảng 21.5 GiB, shared GPU memory
gần 0, đủ backward + optimizer; OPSD probe cả tutor prompt có gold SQL. Giữ
execution timeout BIRD 30 s, Spider 60 s; không giảm timeout để cứu runtime.
Không đưa teacher 7B vào client, không cần teacher 14B/32B.

## 9. CoT là extension riêng của OPSD

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
suất và budget ở mục 1, 8 không tự áp dụng cho extension này.

## 10. Claim, confirmation và quyết định cuối

**Mục tiêu là framework ứng dụng có evidence, không bắt buộc loss mới.**
Các cơ chế đều có nguồn; adaptation sang federated Text-to-SQL có thể là
hướng Q3 hợp lý nếu giải quyết bài toán rõ và chứng minh được lợi ích.
Đóng góp tiềm năng là public teacher bootstrap kết hợp private adaptation
của SLM dưới schema isolation và compute budget. Không mặc định phải có
synergy, lý thuyết mới hay claim “first”; cũng không bảo đảm acceptance chỉ
vì chưa tìm thấy cùng tổ hợp trong search. Chưa chọn paper story trước pilot.

Bảng outcome dưới dùng OPSD làm ví dụ; với local method khác thay P bằng M.
TAID cần contrast riêng với Hinton và gold như mục 6.

| Kết quả sau controls và confirmation | Cách diễn giải được phép |
|---|---|
| Gain cuối so với H-C và H-P hơn G-P, controls hỗ trợ cơ chế, chi phí phù hợp | Có cơ sở phát triển manuscript framework ứng dụng; chưa cần interaction dương nếu không claim synergy |
| Interaction dương qua confirmation | Có thêm cơ sở nói teacher bootstrap làm local method hữu ích hơn; claim heterogeneity cần contrast tương ứng |
| H-P hơn H-C nhưng G-P cũng có cùng gain thêm | Private adaptation mới hữu ích; teacher contribution vẫn phải đọc H-P so với G-P, không suy từ hai gain thêm bằng nhau |
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

Shortlist đã có phản biện độc lập từ một agent trên cùng bối cảnh, không
phải external peer review. Các điểm đã tích hợp: FedDAT không có evidence
SQL trực tiếp và tốn thêm optimization; freeze không bảo đảm giữ kiến thức
teacher; OPSD v3 có evidence model nhỏ; TAID không bị loại vì dùng cơ chế cũ;
controls mở theo claim thay vì bắt buộc full matrix. **Khuyến nghị: freeze
factor pilot đầu, FedDAT là candidate framework, chưa cam kết full matrix.**

## 11. Nguồn primary và phạm vi đọc

- **FedDAT:** [AAAI 2024 paper][feddat], Eq. 4–7/Algorithm 1;
  [official trainer][feddat-code] cho KL direction và 3 forward/2 backward,
  [adapter lifecycle][feddat-lifecycle] cho shared/frozen/persistent local states.
- **FFA-LoRA:** [ICLR 2024 paper][ffa], frozen random factor và aggregation.
- **RoLoRA:** [NeurIPS 2025 paper][rolora], alternating factors và §5.3
  học trước rồi freeze; notation A/B cần đối chiếu PEFT trước implementation.
- **TAID:** [full text v4][taid], §3 và Algorithm 1; ICLR 2025.
- **SQL dynamic mixing:** Le et al., *Distilling Large Language Models for
  Structured Query Language generation with reverse Kullback–Leibler and
  dynamic α scheduler*, [publisher, 2025][sql-dynamic] và
  [author repository][sql-dynamic-code]. Đã đối chiếu metadata/abstract,
  chưa reproduce hoặc kết luận objective tương đương TAID.
- **Federated semantic parsing:** Zhang et al., [ACL 2023][fed-semparse],
  prior cho Text-to-SQL heterogeneous clients và một global model.
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
`federated self-distillation privileged`, tên FedDAT/FFA-LoRA/RoLoRA/TAID
kèm SQL/Spider/BIRD, cùng các bản mới của OPSD/SDFT. Primary sources dùng
để kiểm claim; search không đầy đủ nên
không suy ra “chưa ai làm” từ việc chưa tìm thấy.

[feddat]: https://ojs.aaai.org/index.php/AAAI/article/download/29007/29911
[feddat-code]: https://raw.githubusercontent.com/HaokunChen245/FedDAT/main/src/train/visionlanguage_tasks/task_trainer.py
[feddat-lifecycle]: https://raw.githubusercontent.com/HaokunChen245/FedDAT/main/src/train/main.py
[ffa]: https://proceedings.iclr.cc/paper_files/paper/2024/file/4e243e95c913b367775d71d7182b99d9-Paper-Conference.pdf
[rolora]: https://papers.nips.cc/paper_files/paper/2025/file/adf17e7346b6be4c2f2bb40de572e5bc-Paper-Conference.pdf
[taid]: https://arxiv.org/html/2501.16937v4
[sql-dynamic]: https://www.sciencedirect.com/science/article/pii/S0045790625005506
[sql-dynamic-code]: https://github.com/nthng-quan/distill_t2sql
[fed-semparse]: https://aclanthology.org/2023.acl-long.678/
[opsd]: https://arxiv.org/html/2601.18734v3
[sdft]: https://arxiv.org/html/2601.19897v2
[fedsdr]: https://arxiv.org/html/2605.18028v1
[spear]: https://arxiv.org/html/2605.07977v2
[serl]: https://arxiv.org/html/2608.00485v4
[rethinking]: https://arxiv.org/html/2608.18271v1
[rationalization]: https://arxiv.org/html/2502.06759v1
