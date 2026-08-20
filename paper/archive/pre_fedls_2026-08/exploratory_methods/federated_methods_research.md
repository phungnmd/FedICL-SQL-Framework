# Research note — phương pháp Federated LoRA phù hợp cho Fed-ICKD

**Ngày rà soát:** 2026-07-19
**Phạm vi:** aggregation và optimization của LoRA trong kiến trúc Fed-ICKD; không thay thế note về KD/ICL.
**Kết luận ngắn:** không nên giữ weighted FedAvg trên hai factor LoRA làm phương pháp chính. Nó là baseline cần thiết, nhưng sai lệch đại số tồn tại ngay cả khi dữ liệu IID. Với cấu hình hiện tại `K=8`, rank đồng nhất `r=16`, lựa chọn có bằng chứng xuất bản mạnh nhất là **FedEx-LoRA**; lựa chọn giữ downlink thật sự nhỏ và có tiềm năng tốt nhất là **Fed-SB**, nhưng nó thay đổi parameterization và cần kiểm tra xem subspace cố định có làm yếu server KD hay không. **FLoRA** chỉ đáng dùng nếu paper thật sự nghiên cứu rank/resource heterogeneity. **FLoRA-NA** rất phù hợp về engineering nhưng hiện mới là preprint/submission, nên phù hợp làm ablation mới hơn là nền tảng duy nhất của paper.

---

## 1. Chẩn đoán kiến trúc hiện tại

Mỗi LoRA layer biểu diễn cập nhật

\[
\Delta W_i = s B_i A_i, \qquad
B_i\in\mathbb{R}^{d_{out}\times r},\quad
A_i\in\mathbb{R}^{r\times d_{in}},
\]

với `s = lora_alpha / r`. Cập nhật đúng trong weight space sau một round là

\[
\Delta W_* = \sum_i p_i B_iA_i,\qquad p_i=n_i/\sum_jn_j.
\]

FedAvg-LoRA đang lấy `B_bar = sum p_i B_i`, `A_bar = sum p_i A_i`, rồi dùng
`B_bar A_bar`. Hai biểu thức không bằng nhau: tích của trung bình sinh ra các
cross-client terms `B_i A_j` với `i != j` và thay đổi hệ số của các term đúng.
[FLoRA](https://papers.neurips.cc/paper_files/paper/2024/file/28312c9491d60ed0c77f7fff4ad86dd1-Paper-Conference.pdf)
và [FedEx-LoRA](https://aclanthology.org/2025.acl-long.67/) đều xác lập vấn đề
này. Vì vậy câu trong draft “re-initializing every client from the same
aggregated adapter mitigates the issue” không đúng: cùng initialization giúp
alignment, nhưng không làm phép nhân trở thành phép toán tuyến tính.

Ba loại heterogeneity cũng cần tách riêng:

1. **Data/statistical heterogeneity:** mỗi client có schema/domain khác nhau;
   gây client drift. Đây là vấn đề chắc chắn có trong Fed-ICKD.
2. **System/rank heterogeneity:** client dùng rank khác nhau vì tài nguyên khác
   nhau. Draft chưa mô phỏng điều này; K=8 hiện dùng cùng model và cùng rank.
3. **Factorization/aggregation error:** trung bình `A`, `B` sai so với trung
   bình `BA`. Vấn đề này tồn tại với cả rank đồng nhất và dữ liệu IID.

Server reverse-KL distillation chỉ có thể sửa hành vi trên public pool sau khi
aggregation; nó không làm aggregation trở nên exact. Đây là hai cơ chế trực
giao và tạo factorial ablation tự nhiên:

| Trục | Baseline | Phương pháp |
|---|---|---|
| LoRA aggregation | factor-wise FedAvg | exact/nearly-exact aggregation |
| Server update | none hoặc CE trên `P` | CE + RKL trên `P` |

Thiết kế này cho phép trả lời liệu KD chỉ đang chữa aggregation error hay còn
đóng vai trò consensus regularizer dưới non-IID sau khi aggregation đã đúng.

---

## 2. Các phương pháp chính

### 2.1 FedAvg/FedIT-style LoRA — baseline bắt buộc, không nên là default cuối

**Cơ chế.** Trung bình riêng `A_i` và `B_i`, thường theo số mẫu. Ưu điểm là
code đơn giản, uplink/downlink đúng bằng một adapter rank `r`, tương thích
PEFT/Hugging Face và server KD hiện tại.

**Điểm yếu.** Inexact trong weight space; sai lệch tăng khi local models tách
xa nhau, tức đúng vào regime domain-non-IID và nhiều local epochs của paper.
Không nên chỉ “acknowledge in one sentence”; phải đo nó.

**Vai trò đề xuất.** Giữ nguyên arm `fedavg` và `fedkd_factoravg` làm baseline.
Log mỗi layer:

\[
e_{agg}=\frac{\|\sum_i p_iB_iA_i-\bar B\bar A\|_F}
{\|\sum_i p_iB_iA_i\|_F+\epsilon}.
\]

Đây là diagnostic trực tiếp hơn việc dùng Dirichlet-alpha sweep làm trigger.

### 2.2 FLoRA — exact bằng stacking

**Nguồn:** Wang et al., NeurIPS 2024,
[FLoRA: Federated Fine-Tuning Large Language Models with Heterogeneous Low-Rank Adaptations](https://papers.neurips.cc/paper_files/paper/2024/file/28312c9491d60ed0c77f7fff4ad86dd1-Paper-Conference.pdf).

**Cơ chế.** Server xếp chồng các factor:

\[
B_*=[B_1,\ldots,B_K],\qquad
A_*=[p_1A_1;\ldots;p_KA_K],
\]

nên `B_* A_* = sum_i p_i B_i A_i` chính xác. Rank global bằng
`R=sum_i r_i`, nên tự nhiên hỗ trợ client có rank khác nhau.

**Ưu điểm.** Exact, dễ hiểu, không cần SVD để tạo global update, và là paper
peer-reviewed mạnh. Hữu ích nhất khi rank heterogeneity là một RQ thật.

**Hạn chế quan trọng cho Fed-ICKD.** Với `K=8,r=16`, global rank thành 128.
Nếu broadcast adapter rank 128 mỗi round thì downlink xấp xỉ 8 lần vanilla;
rank còn tăng/đổi theo participation nếu không có reset/compression protocol.
FLoRA còn có rủi ro lộ block của từng client khi gửi stacked adapter; paper đề
nghị tách rank-1 và shuffle, nhưng đó không phải bảo đảm DP. Vì rank clients
hiện đồng nhất và paper không đặt resource heterogeneity làm RQ, FLoRA giải
quyết nhiều hơn yêu cầu và làm câu chuyện deployment nặng hơn.

**Verdict:** baseline exact hữu ích, không phải lựa chọn chính cho kiến trúc
hiện tại. Chỉ nâng thành main method nếu thêm rank-heterogeneous experiment.

### 2.3 FedEx-LoRA — exact bằng residual correction

**Nguồn:** Singhal et al., ACL 2025,
[FedEx-LoRA: Exact Aggregation for Federated and Efficient Fine-Tuning of Large Language Models](https://aclanthology.org/2025.acl-long.67/).

**Cơ chế.** Vẫn tạo `A_bar`, `B_bar`, nhưng tính residual

\[
E_t=\sum_i p_iB_iA_i-\bar B\bar A,
\]

rồi fold `E_t` vào frozen weight `W_0^t`. Do đó
`W_0^{t+1} + B_bar A_bar` đúng bằng model-space average. Local LoRA ở round
sau vẫn train được cả `A` và `B`, giữ expressivity của LoRA chuẩn.

**Phù hợp với Fed-ICKD.** Rank đồng nhất, K nhỏ, server mạnh và LoRA chuẩn là
đúng regime mà FedEx-LoRA hấp dẫn nhất. Nó ít thay đổi local objective, nên
so sánh `FedEx` với `FedEx+RKL` sạch hơn so với đổi sang một PEFT family khác.
Paper đã đánh giá model autoregressive tới 9B và nhiều task NLP/reasoning.

**Sửa một nhận định trong draft.** FedEx-LoRA không hoàn toàn giữ giao thức
“chỉ aggregated rank-r adapter được broadcast”. Residual có rank tối đa
`K*r`; paper factor hóa residual để gửi xuống client và thừa nhận exact
communication tăng tuyến tính theo K, sau đó đề xuất truncated SVD nếu cần
giới hạn bandwidth. Với `K=8,r=16`, residual rank tối đa 128, nên vẫn khả thi
trong simulation nhưng phải báo cáo số byte thật. Không được tiếp tục mô tả
mọi upload/download là “a few MB” nếu dùng exact residual.

**Tương tác với server KD.** Server KD phải cập nhật adapter trên cùng
`W_0^{t+1}` đã nhận residual. Checkpoint toàn cục vì thế là cặp
`(frozen_base_state_or_residual_history, adapter)`, không còn chỉ là adapter.
Trước khi client round kế tiếp bắt đầu, residual sau KD/aggregation phải được
materialize hoặc phân phối nhất quán. Điều này chạm trực tiếp vào invariant
hiện tại “base 1.5B bất biến và chỉ adapter đi qua wire”.

**Verdict:** lựa chọn chính có độ tin cậy học thuật cao nhất nếu paper chấp
nhận downlink `O(Kr)` và sửa checkpoint/communication claim.

### 2.4 Fed-SB — exact, communication cực nhỏ, nhưng đổi parameterization

**Nguồn:** Singhal et al., arXiv 2025 v2,
[Fed-SB: A Silver Bullet for Extreme Communication Efficiency and Performance in (Private) Federated LoRA Fine-Tuning](https://arxiv.org/abs/2502.15436).

**Cơ chế.** Dùng LoRA-SB: chọn/fix hai basis `B` và `A`, chỉ học ma trận vuông
`R_i in R^{r x r}` trong `B R_i A`. Vì `B,A` chung và cố định,

\[
\sum_i p_i B R_i A = B\left(\sum_i p_iR_i\right)A,
\]

nên averaging `R` là exact. Communication mỗi layer là `r^2`, độc lập với
số client; trainable parameters và DP noise requirement cũng giảm. Paper báo
cáo lợi ích tới 230x về communication và có thí nghiệm highly non-IID, nhưng
hiện nguồn là preprint chứ chưa có vị thế venue như FLoRA/FedEx-LoRA.

**Phù hợp với Fed-ICKD.** Đây là lựa chọn duy nhất trong nhóm khởi đầu vừa
exact vừa bảo toàn câu chuyện adapter-only nhỏ qua nhiều round. Client 1.5B
cũng nhẹ hơn. Tuy nhiên server RKL chỉ có thể dịch chuyển model trong subspace
`span(B,A)` cố định. Text-to-SQL có domain shift Spider -> BIRD public pool;
subspace quá hẹp có thể làm KD không đủ khả năng hấp thụ teacher signal.
Fed-SB thường dùng rank lớn hơn LoRA thông thường; không nên so `r=16` với
`r=16` rồi kết luận.

**Verdict:** ứng viên main method tốt nhất nếu communication/privacy-efficiency
là claim trung tâm, nhưng cần một feasibility gate trước: centralized
`LoRA-SB + CE/RKL` phải không thua LoRA `r=16 + CE/RKL` quá ngưỡng đã định,
và so sánh nên match trainable-parameter hoặc communication budget.

### 2.5 FLoRA-NA — gần exact với communication bằng vanilla

**Nguồn:** Nguyen et al., 2025,
[FLoRA-NA: Communication-Efficient and Accurate Approach for Aggregation in Federated Low-Rank Adaptation](https://arxiv.org/abs/2509.26399)
(đồng thời là submission ICLR 2026; chưa nên mô tả như accepted paper).

**Cơ chế.** Server tìm surrogate rank-r `A_hat,B_hat` để giảm khoảng cách
giữa `B_hat A_hat` và ideal update `sum_i p_iB_iA_i`, rồi chỉ broadcast một
adapter rank r. Đây là nearly-exact low-rank projection/estimation, không phải
exact equality.

**Ưu điểm.** Giữ nguyên API LoRA, checkpoint adapter-only và communication
`O(r)`, không tăng theo K; rất hợp constraints engineering hiện tại.

**Hạn chế.** Projection bỏ phần singular spectrum ngoài rank r; chất lượng phụ
thuộc mức độ các client update dùng chung subspace. Domain-partitioned SQL có
thể là trường hợp khó vì mỗi schema family tạo direction riêng. Độ trưởng
thành bằng chứng thấp hơn FLoRA/FedEx-LoRA.

**Verdict:** ablation “best fixed-rank practical aggregation” rất đáng chạy;
không nên là citation duy nhất bảo vệ phương pháp chính.

---

## 3. Các hướng mới hơn cần biết

### 3.1 FLoRG (ICLR 2026)

[FLoRG: Federated Fine-tuning with Low-rank Gram Matrices and Procrustes Alignment](https://openreview.net/forum?id=kntrZOm2AQ)
dùng một low-rank matrix, aggregate Gram matrix và Procrustes alignment để xử
lý cả aggregation error lẫn non-uniqueness/rotation của factorization. Đây là
paper mới có venue mạnh và báo cáo giảm communication lớn. Nó đáng đưa vào
Related Work và có thể là follow-up nếu factor alignment diagnostic cao.
Nhưng parameterization khác LoRA chuẩn và implementation risk lớn hơn FedEx;
chưa nên chặn round-loop hiện tại để chuyển sang nó.

### 3.2 ILoRA (2025 preprint)

[ILoRA](https://arxiv.org/abs/2511.16069) kết hợp QR-orthonormal initialization,
concatenated-QR aggregation cho heterogeneous rank, và rank-aware control
variates để giảm client drift. Điểm đáng học là nó xử lý đồng thời ba lỗi mà
draft đang trộn lẫn: initialization, aggregation và non-IID drift. Tuy nhiên
đây là một bundle nhiều thành phần, khó attribution và chưa cần thiết khi mọi
client Fed-ICKD dùng cùng rank.

### 3.3 FSLoRA và Fed-PLoRA — chỉ khi thêm resource heterogeneity

[Federated Sketching LoRA](https://arxiv.org/abs/2501.19389) cho client chỉ
cập nhật các row/column con của global LoRA theo sketch ratio, phù hợp partial
participation và thiết bị có budget khác nhau.
[Fed-PLoRA](https://arxiv.org/abs/2602.16936) tách LoRA thành nhiều rank-1
branch và dùng Select-N-Fold để client chọn số branch theo tài nguyên. Cả hai
đều trả lời system heterogeneity tốt hơn cấu hình hiện tại, nhưng không trực
tiếp tăng novelty Text-to-SQL nếu paper chưa đo compute/bandwidth heterogeneity.

### 3.4 FedProx/SCAFFOLD — orthogonal, không thay exact aggregation

FedProx thêm proximal penalty để local model không đi quá xa global model;
SCAFFOLD dùng control variates để hiệu chỉnh client drift. Chúng có thể ghép
với FedEx/Fed-SB nhưng không sửa `mean(B)mean(A) != mean(BA)`. Với tất cả 8
client tham gia mỗi round và local epoch nhỏ, chưa cần đưa vào main grid.
Chỉ kích hoạt nếu post-FedAvg metric oscillate/diverge hoặc client-update
cosine/Frobenius diagnostics cho thấy drift, sau khi aggregation error đã
được tách ra.

---

## 4. Ma trận quyết định cho paper này

| Phương pháp | Model-space aggregation | Downlink/round | Heterogeneous rank | Đổi LoRA training | Độ trưởng thành | Fit hiện tại |
|---|---:|---:|---:|---:|---|---|
| factor-wise FedAvg | sai | `O(r)` | không | không | chuẩn baseline | baseline bắt buộc |
| FLoRA | exact | `O(Kr)` | có | reset/stack rank | NeurIPS 2024 | trung bình |
| FedEx-LoRA | exact | `O(Kr)` residual + `O(r)` adapter | không phải mục tiêu chính | rất ít | ACL 2025 | **cao** nếu sửa comm claim |
| Fed-SB | exact | `O(r^2)` | rank chung | **có**, chỉ train `R` | arXiv v2 | **cao** nếu KD feasibility pass |
| FLoRA-NA | gần exact | `O(r)` | chủ yếu rank cố định | ít | preprint/ICLR submission | cao cho ablation |
| FLoRG | alignment-aware | rất thấp theo paper | có khía cạnh alignment | có | ICLR 2026 | promising, implementation risk |
| FSLoRA/Fed-PLoRA | xấp xỉ/structured | budget-dependent | có | có | preprint 2025/2026 | thấp nếu không có system heterogeneity |

Không có một phương pháp thắng trên mọi trục. Quyết định phụ thuộc claim:

- Nếu claim chính là **server KD trên public data cải thiện federated
  Text-to-SQL**, chọn **FedEx-LoRA** làm aggregation mặc định vì nó giữ local
  LoRA training gần kiến trúc hiện tại nhất và loại confound aggregation.
- Nếu claim chính thêm **cực kỳ communication-efficient**, chọn **Fed-SB**,
  nhưng phải chứng minh fixed subspace không bóp nghẹt KD.
- Nếu claim thêm **clients có resource/rank khác nhau**, dùng **FLoRA** hoặc
  FSLoRA; khi đó phải thêm rank allocation và per-client resource setting vào
  problem formulation, không chỉ đổi aggregator.

---

## 5. Đề xuất kiến trúc Fed-ICKD đã chỉnh

### Phương án A — khuyến nghị cho paper hiện tại: FedEx-ICKD

Mỗi round:

1. Client nhận cùng effective global model `(W_0^t, A^t, B^t)`, train LoRA
   bằng private CE và upload `A_i,B_i`.
2. Server tính weighted ideal update `Delta W_* = sum_i p_i B_iA_i`.
3. Server tạo `A_bar,B_bar` và residual
   `E_t = Delta W_* - B_bar A_bar`; cập nhật frozen base.
4. Trên effective global model exact này, server chạy CE+RKL trên `P`, cập
   nhật global adapter.
5. Broadcast adapter và factorized residual cần thiết cho round sau.

Tên method trong paper có thể là **FedEx-ICKD** cho implementation arm, nhưng
novelty phải mô tả là “FedEx-LoRA aggregation + proposed public reverse-KL
server regularization”; không được ngụ ý exact aggregation là đóng góp mới.

### Phương án B — communication-first: FedSB-ICKD

Khởi tạo common `A,B` một lần, client và server KD chỉ cập nhật `R`. Server
aggregate `R_bar=sum_i p_iR_i`, rồi distill `R_bar` trên public pool. Mọi
round chỉ truyền `R`. Đây là system story sạch nhất, nhưng cần làm lại
centralized baselines trên cùng LoRA-SB parameterization.

### Không khuyến nghị

Không dùng pipeline “factor-wise FedAvg rồi server KD” làm phương pháp chính
và gọi KD là consensus regularizer mà không có exact-aggregation control.
Nếu KD thắng, reviewer có thể hợp lý hỏi liệu nó chỉ bù lỗi LoRA averaging.

---

## 6. Experiment ladder tối thiểu nhưng đủ thuyết phục

### Gate 0 — không cần train

Trên checkpoint client của pilot T=1, tính `e_agg` theo layer và toàn model;
so sánh prediction/EX của:

- `bar_B bar_A` (factor FedAvg),
- exact stacked/product average,
- truncated rank-16 SVD của exact average.

Điều này cho biết phần lỗi do factor averaging và phần mất mát bắt buộc do
ép global update về rank 16.

### Gate 1 — chọn parameterization

- LoRA r=16 centralized CE+RKL.
- LoRA-SB ở ít nhất hai rank, match communication budget và gần match
  trainable-parameter budget.

Nếu Fed-SB giữ được EX và execution-error, chọn phương án B. Nếu không, dùng
FedEx phương án A.

### Tier-1 factorial federation

Tối thiểu bốn arms, cùng split/seed/client checkpoints khi có thể:

1. `FactorAvg` — private CE only.
2. `FactorAvg + public CE+RKL` — kiến trúc hiện tại.
3. `ExactAgg` — FedEx hoặc Fed-SB, private CE only.
4. `ExactAgg + public CE+RKL` — proposed full method.

Arm public CE-only có thể thêm làm control drift đã có trong draft. Báo cáo
EX, EM, execution-error, worst-client EX, macro-client EX, communication
bytes, peak VRAM, wall time và `e_agg`. Với domain-non-IID, chỉ global micro-EX
không đủ; macro/worst-client cho biết consensus có đánh đổi client nhỏ không.

### Tier-2 có điều kiện

- `FLoRA-NA + RKL`: fixed-rank practical alternative.
- `FLoRA + RKL` với ranks `{4,8,16,32}`: chỉ nếu thêm system heterogeneity.
- `FedProx` hoặc control variate: chỉ khi exact aggregation vẫn oscillate dưới
  Dirichlet-alpha thấp.
- Partial participation: cần nếu muốn claim realistic cross-silo robustness;
  full participation K=8 không kiểm tra churn.

### Thống kê

Chạy ít nhất 3 partition/training seeds cho main comparison. McNemar trên
Spider-dev rows hữu ích cho cặp model, nhưng không thay seed variance của FL.
Báo cáo mean ± std/CI, và paired seed differences. Các method 2025–2026 mới
không nên được chọn chỉ từ một seed.

---

## 7. Những thay đổi nên đưa ngược vào `system_architecture.md`

1. Đổi weighted factor FedAvg từ “default” thành **baseline**.
2. Bỏ câu common initialization là mitigation đủ cho aggregation error.
3. Nâng exact aggregation thành Tier-1 control, không đợi alpha sweep.
4. Nếu chọn FedEx, sửa invariant communication/checkpoint: effective frozen
   base thay đổi; downlink có residual rank tối đa `K*r`.
5. Nếu chọn Fed-SB, sửa toàn bộ notation từ `BA` trainable sang `BRA` với
   common fixed bases; server KD cũng chỉ optimize `R`.
6. Tách diagnostic `aggregation error` khỏi `client drift`; alpha sweep chủ
   yếu kiểm tra drift/data heterogeneity, không quyết định lỗi đại số có tồn
   tại hay không.
7. Thêm macro-client/worst-client metrics và actual bytes/round vào bảng kết
   quả; “few MB” phải là measurement theo model/rank/dtype, không là giả định.

---

## 8. Kết luận lựa chọn

Thứ tự khuyến nghị thực dụng:

1. **Ngay bây giờ:** tính `e_agg` và rank-16 SVD oracle trên pilot T=1.
2. **Main architecture an toàn:** FedEx-LoRA + server CE/RKL, vì exact và đã
   peer-reviewed ở ACL 2025, đồng thời giữ local LoRA/KD gần code hiện tại.
3. **Candidate có upside lớn:** Fed-SB + server CE/RKL, sau centralized
   feasibility gate; nếu pass, đây là câu chuyện communication đẹp hơn.
4. **Ablation mới:** FLoRA-NA + RKL.
5. **Cite/để future work:** FLoRG, ILoRA, FSLoRA, Fed-PLoRA; không mở rộng
   scope sang rank heterogeneity khi federated number cơ bản còn chưa có.

Điểm nghiên cứu mạnh nhất của Fed-ICKD không nên là “một aggregator LoRA mới”.
Nó nên là bằng chứng rằng **public reverse-KL distillation còn đem lại lợi ích
sau khi đã loại bỏ lỗi aggregation**, trên Text-to-SQL non-IID theo schema,
đồng thời teacher không thấy private schema/query. Factorial design ở trên là
cách sạch nhất để bảo vệ claim đó.
