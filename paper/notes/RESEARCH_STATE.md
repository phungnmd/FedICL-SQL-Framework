# FedLS-SQL: trạng thái nghiên cứu

File này trả lời bốn câu: ta đang hỏi gì, đã biết gì (kèm mức chắc chắn), còn
chưa biết gì, và đang ở giai đoạn nào. Không chứa method hay câu chuyện paper
đã chốt: câu chuyện sẽ được chọn từ kết quả của giai đoạn E. Số liệu và bằng
chứng: [LAB_LOG](LAB_LOG.md) (từ 2026-10-10) và
[log cũ](../archive/lab_log_2026-10/LAB_LOG_2026-09-24_to_2026-10-09.md).
Setup và protocol: [system_architecture](system_architecture.md). Lệnh chạy:
[PIPELINE_NEXT](PIPELINE_NEXT.md). Các hướng đã cân nhắc trước 2026-10-11:
[archive/directions_2026-10](../archive/directions_2026-10/README.md).

Cập nhật: 2026-10-17.

## 1. Câu hỏi nghiên cứu

Nhiều client giữ dữ liệu Text-to-SQL riêng (Spider, chia theo domain) và cùng
train một model nhỏ (SLM) bằng federated learning. Server có một LLM lớn
frozen (teacher) và một public dataset khác miền (BIRD). Chỉ deploy SLM.

> Dùng teacher và public data khác miền thế nào để SLM federated tốt hơn, và
> phần lợi ích nào thực sự đến từ teacher, từ public data, hay từ cách sắp
> xếp các stage?

**Metric chính (owner, 2026-10-16), cố định cho mọi giai đoạn: Spider EX**,
miền private của client (Spider dev khi thăm dò, Spider test khi xác nhận).
BIRD EX (miền public) là metric phụ: xếp hạng theo Spider trước; gain BIRD
chỉ tính là lợi khi Spider không thấp hơn, và giữa các phương án có Spider
không khác nhau thì BIRD cao hơn là tốt hơn. Không đổi Spider lấy BIRD. Vẫn
luôn báo cả hai miền.

## 2. Setup cố định

- Student Qwen2.5-Coder-1.5B-Instruct, LoRA r16. Teacher Qwen2.5-Coder-7B,
  4-bit, frozen, chỉ ở server.
- 5 client, split domain-cluster Dirichlet alpha 0.1 (`k5`). FedAvg theo số
  mẫu. Chỉ adapter di chuyển. Không ICL, client và inference chỉ sinh SQL.
- Stage: `A` = một round private (1 epoch mỗi client rồi FedAvg); `K` = một
  epoch server trên 9,428 câu BIRD train; `K2` = hai epoch liên tục.
  `K[ce]` = gold CE, `K[fkl]` = Hinton (0.5 CE + 0.5 KL, T=2). `A[ntd]` =
  FedNTD ở client (beta 1, tau 3).
- Eval: Spider dev (1,034) và các bản Realistic, SYN, DK; BIRD dev (1,534).
  Spider test (2,147) chỉ dùng để xác nhận (R10), chưa eval lần nào.

## 3. Những gì đã biết

Mức: **vững** = lặp lại qua nhiều model hoặc seed; **1 seed** = một lần chạy,
đáng tin về chiều, chưa về độ lớn; **thăm dò** = tìm ra sau khi xem dữ liệu,
chỉ là giả thuyết.

| # | Phát hiện | Bằng chứng chính | Mức |
|---|---|---|---|
| F1 | Thêm stage K trên BIRD làm SLM federated tốt hơn trên cả hai miền | Coder-1.5B `h_plain` - FL: Spider +4.16 (p=.0002), BIRD +14.28; tương tự ở 0.5B (+5.0) và 1.5B-Instruct (khoảng +4.5) | vững (3 model, mỗi model 1 seed) |
| F2 | Gain BIRD đến từ chính public data; với round private cuối plain, gold đủ để đưa Spider lên mức central | Coder-1.5B `g_plain` - FL: Spider +3.77 (p=.001), BIRD +14.67; `g_plain` = central E3 trên Spider (71.37), DK thấp hơn 4.1 (p=.02). Gold v1 (NTD cuối) - FL: Spider +0.29. 0.5B gold AKAKA - FL: Spider +2.6 | 1 seed |
| F3 | Soft label của teacher hơn gold cùng chuỗi trên Spider, nhưng ở Coder-1.5B với chuỗi AKAKA edge này mất khi round cuối là plain (lịch K-first: F13) | +2.42 (0.5B, p=.020), +2.03 (1.5B-Instruct, p=.033), +2.03 (0.5B K2AAA, p=.048); Coder-1.5B: v1 +1.35 (p=.23), plain +0.39 (p=.76). Biến thể Spider dương ở cả 6 ô (2 chuỗi), nhưng set có p<.05 đổi (DK với NTD, SYN plain) | yếu ở Coder-1.5B; phần robustness là thăm dò (R8) |
| F4 | Trong stage K, Hinton làm quên Spider ít hơn gold | Coder-1.5B: Spider +3.48 sau K1, +3.00 sau K2; 0.5B K2AAA: +3.29 sau K2 | 1 seed mỗi model |
| F5 | Round private cuối quyết định điểm cân bằng Spider-BIRD | Coder-1.5B plain so với NTD: Hinton Spider +2.51, BIRD -3.32; gold Spider +3.48 (p<.001), BIRD -1.04 (p=.21); 0.5B: NTD không tốn Spider, BIRD +1.89 (2 seed, p=.004) | 1-2 seed |
| F6 | NTD ở round giữa (A2) không có tác dụng, vì K2 sau đó đưa BIRD về cùng mức | 0.5B P2.25: hai model cuối gần như trùng (Spider 20/20 discordant) | 1 seed, chưa thử ở 1.5B |
| F7 | FedNTD và FedProx không phải FL baseline mạnh hơn FedAvg ở setting này | Coder-1.5B FedNTD - FL BIRD -1.37; 0.5B FedProx (P2.20) | 1 seed |
| F8 | Vị trí K: K càng sớm Spider càng cao, K càng muộn BIRD càng cao; edge BIRD của teacher chỉ rõ khi K muộn | 0.5B alpha 0.5, cùng budget: Spider K2AAA 63.93 / AK2AA 63.15 / AKAKA 62.57 (Hinton), cùng thứ tự với gold; không cặp nào p<.1; teacher - gold BIRD chỉ có ý nghĩa ở AKAKA (+3.13) | thăm dò, chưa thử ở 1.5B |
| F9 | FL thua central khi so cùng số lần đi qua dữ liệu; ở Coder-1.5B khoảng cách tăng theo số pass | Coder-1.5B alpha 0.1: +1.93 / +2.90 / +3.77 (E1-E3, p=.13/.028/.003), FL đạt đỉnh ở A2 rồi giảm; khoảng cách JOIN xuất hiện trước. 0.5B alpha 0.5: +4.6 / +4.8 / +1.8 (central overfit ở E3). BIRD không có khoảng cách | 1 seed mỗi model |
| F10 | EX phóng đại khoảng 5-7 điểm đều ở mọi arm; mọi contrast giữ dấu dưới test-suite EX | Coder-1.5B seed 0, Spider dev | 1 seed |
| F11 | Gain của `h_plain` so với FL nằm ở câu JOIN; round NTD cuối giữ lỗi over-join | JOIN +9.07 (p<.001), no-JOIN +0.96; over-join 87 (FL), 84 (v1), 57 (`h_plain`) | thăm dò (R8 kiểm trên seed mới) |
| F12 | Sample nhiều lần có headroom lớn trên câu train | pass@8 - greedy 13-18 điểm, cần oracle gold | 1 seed, chỉ là trần |
| F13 | Với lịch K-first (K2AAA, round plain), teacher hơn gold trên Spider ở model cuối; edge tạo ra ở K2 và còn khoảng 2/3 (net) ở A3 | Coder-1.5B `hinton_k2aaa` - `gold_k2aaa`: Spider K2 +3.19 (p=.010), A3 +2.13 (p=.020); DK A3 +5.98 (p<.001); BIRD A1 -3.98, A3 -1.50. Các câu tạo edge đổi nhiều giữa K2 và A3 | 1 seed; DK là thăm dò (R8) |
| F14 | Rounds private bào mòn BIRD đã học ở K2, chủ yếu qua LoRA B | Hinton BIRD 43.61 (K2) xuống 36.77 (A1); với A đóng băng vẫn xuống 37.61, tức khoảng 88% đi qua B (P2.39 pilot) | 1 seed |
| F15 | Edge Spider của teacher trong K2AAA không phải do softening; ở DK một phần là softening | P2.38 virtual teacher (`a`=0.728): Hinton - virtual Spider K2 +6.09 (p<.001), A3 +2.03 (p=.031); virtual - gold Spider A3 +0.10, K2 -2.90; DK A3: virtual - gold +3.36, Hinton - virtual +2.62 (p=.049). Phần BIRD mất thêm sau Hinton K2 cũng do teacher (Hinton - virtual A1 -2.28) | 1 seed |
| F16 | Có teacher, K2AAA ngang train tập trung Spider+BIRD trên Spider và DK | `central_mix` E3 - `hinton_k2aaa` A3: Spider +0.68 (p=.60), DK +0.37; so với `gold_k2aaa`: Spider +2.80 (p=.016), DK +6.36 (p<.001); BIRD +5.15 so với Hinton | 1 seed |
| F17 | Sau Hinton K2, FL chỉ thua central Spider khoảng 2 điểm; BIRD mất sau K2 là do train Spider, không do FL | P2.42 `central_k2` - `hinton_k2aaa`: Spider pass 3 +2.13 (p=.061), DK +0.19; từ base (P2.27) +3.77 (p=.003). BIRD: central mất nhiều hơn FL (-4.50, p<.001) | 1 seed |
| F18 | TAID ở K2 không hơn Hinton T=2 ở model cuối | P2.40 TAID - Hinton A3: Spider -1.84 (p=.050), DK -4.11 (p=.001), BIRD +1.04 (n.s.); ở A1 BIRD +3.19 (p<.001) rồi mất. TAID - gold A3 Spider +0.29 | 1 seed |
| F19 | FL thuần gần như không hơn client tốt nhất train một mình trên Spider | P2.37 `local`: Spider 64.60-67.02 (trung bình 65.49); FL A3 - client tốt nhất +0.58 (p=.69); `hinton_k2aaa` A3 - client tốt nhất +5.51 (p<.001) | 1 seed |

Hướng đã đóng vì kết quả âm hoặc quá tốn: plan task và CoT ở client hoặc
server (P2.10-P2.15), retention loss (P2.9), weight merge (A1), KID, GKD,
ICL, self-consistency, public pool cùng miền, public pool không có
gold SQL (owner quyết định 2026-10-11 sau P2.36: không mở hướng teacher thay
nhãn), shared teacher replay và teacher ở client (owner 2026-10-12), freeze
LoRA A ở client (P2.39 pilot: Spider -1.55, BIRD không giữ được; owner
2026-10-13). Ở protocol v1 đã đóng: FedDF và aggregation chính xác (FLoRA,
không có headroom). P2.16 centralized E1-E4 chưa
từng được publish, không trích dẫn.

## 4. Chưa biết (Coder-1.5B, seed 0)

| # | Câu hỏi | Cần arm |
|---|---|---|
| Q1 | Vì sao FL thuần thua central 3.8 điểm và gần như không hơn client tốt nhất (F19)? | audit client drift (Q7) |
| Q2 | Teacher có hơn gold ở Coder-1.5B không, và có phụ thuộc lịch không? K2AAA: có (F13); AKA plain: không trên Spider (P2.36) | cặp AKAKA plain (P2.37, hoãn) |
| Q3 | Đặt K ở đâu: đầu (K2AAA), xen kẽ (AKAKA), hay chuỗi hiện có? | AKAKA plain (hoãn; chỉ cần nếu paper claim lịch K-first) |
| Q4 | Trần khi có đủ dữ liệu ở một chỗ là bao nhiêu? | đã có: `central_mix` (F16); không có teacher nên chỉ là mốc pooled data, không phải trần cho method có teacher |
| Q5 | Teacher SQL (SeqKD) có khác soft label không? | không trong giai đoạn E (P2.6: edge mất sau round private cuối) |
| Q6 | Kết quả có giữ khi heterogeneity khác không? | alpha 0.5, để sau |
| Q7 | Setup hiện tại có client drift thật không, hay FL thua central vì lý do khác? | audit trên adapter client của P2.27 FL (chưa lên lịch) |
| Q8 | Nếu teacher dạy CoT ở server và client tự sinh CoT có kiểm chứng trên dữ liệu private, lợi thế teacher có sống tới model cuối không? | pilot P0-P2 rồi `cot_fed`, `cot_template`, `cot_noteacher` trong [DIRECTION_PROPOSAL](DIRECTION_PROPOSAL.md); cần owner mở lại hướng CoT |
| Q9 | Edge của teacher có phải chỉ do softening (label smoothing) không? | đã có: không trên Spider, một phần trên DK (F15). Còn mở: LS epsilon 0.1 và self-distillation (teacher-specific chưa chắc là 7B-specific) |
| Q10 | KD target khác có làm teacher đóng góp nhiều hơn Hinton T=2 không? | TAID: không (F18). P2.41 Hinton T=1 không chạy (điều kiện không đạt) |
| Q11 | Sau K2, FL còn thua train tập trung bao nhiêu? | đã có: khoảng 2 điểm Spider (F17), sát độ phân giải 1 seed |
| Q12 | Đảo vai (BIRD private, Spider public): teacher có đóng góp rõ hơn không? | hướng ưu tiên (owner 2026-10-17); pilot P2.43 chưa có code, LAB_LOG 2026-10-17 |
| Q13 | Edge Spider +2.13 của `hinton_k2aaa` có giữ ở seed 1-2 không? Đây là recipe tốt nhất trong 4 recipe teacher đã thử | xác nhận sau khi chốt (luật 2) |

Danh sách arm P2.37 giữ làm baseline. Từ 2026-10-12 được thêm arm sau khi
xem kết quả (luật 1, mục 5).

## 5. Giai đoạn và luật đang áp dụng

Giai đoạn hiện tại: **thăm dò**, seed 0, chỉ trên dev (Spider dev, các biến
thể, BIRD dev). Hướng đề xuất tiếp theo, chưa chốt:
[DIRECTION_PROPOSAL](DIRECTION_PROPOSAL.md).

Ba luật (owner, LAB_LOG 2026-10-12):

1. **Thăm dò tự do.** Được đọc mọi kết quả dev ở seed 0 và dùng nó để chọn
   arm, setting, schedule hay hướng tiếp theo; được thêm arm sau khi xem kết
   quả; không cần viết luật pass/fail trước một run thăm dò. Mọi run và mọi
   lựa chọn ghi vào LAB_LOG.
2. **Chốt rồi mới xác nhận.** Trước khi chạy seed 1-2 hay eval Spider test,
   một entry có ngày trong LAB_LOG chốt method, cấu hình, comparator, phép
   kiểm và claim. Claim trong paper chỉ lấy từ các run xác nhận này, không
   lấy từ số dev đã dùng để chọn. Không sửa entry đó sau khi đọc kết quả xác
   nhận. Đi kèm luật này:
   - R10: Spider test chỉ dùng để xác nhận.
   - R13: gộp seed bằng question-clustered test, 3 seed, không thêm seed sau
     khi đọc kết quả.
   - R8: subgroup tìm ra sau (ví dụ JOIN) chỉ là giả thuyết, kiểm trên seed
     không sinh ra nó.
3. **Công khai.** Paper ghi đã thử gì trên dev (arm, setting, số checkpoint
   đã eval) và nói rõ số dev là thăm dò.

Vì sao giữ luật 2: mỗi so sánh trên Spider dev có khoảng 140 câu lệch nhau,
nên chọn cái tốt nhất trong 10 biến thể không có tác dụng thật vẫn thấy
khoảng +1.7 điểm, và khoảng 40% lần tìm như vậy cho ra một p<.05.

Thực hành báo cáo (không phải luật chọn):

- R9: so central và FL ở cùng số pass, không chỉ checkpoint cuối.
- Chỉ claim điều có comparator tách riêng; thành phần giữ lại mà không có
  bằng chứng ở setting hiện tại thì ghi là thừa kế, không claim.

Đã bỏ (2026-10-12): luật pass/fail viết trước cho từng thí nghiệm (R1-R6,
R11, R12) và danh sách arm cố định của giai đoạn E. Kết quả đã ghi theo các
luật đó giữ nguyên làm lịch sử.

Mức paper (owner, 2026-10-14): **floor** là paper ứng dụng Q3 chuẩn:
framework chạy trọn; mỗi thành phần là cơ chế đã công bố có adaptation cho
federated Text-to-SQL; đóng góp của teacher đo so với gold bootstrap cùng
lịch ở endpoint cuối và xác nhận qua 3 seed; các thành phần chỉ cần cộng
thêm lợi ích, không bắt buộc synergy; báo đủ control và quá trình thăm dò.
**Aim** trên Q3 khi có bằng chứng, ví dụ method phía client làm khoảng
teacher-gold lớn hơn. Không bỏ, hạ hay hoãn một hướng đạt floor chỉ vì nó
chưa đạt aim; fallback được đánh giá theo floor. Câu chuyện dưới floor
(teacher chỉ là ablation) vẫn bị loại. K2AAA đơn thuần là baseline mạnh
nhất mà method phải vượt (owner 2026-10-13).
