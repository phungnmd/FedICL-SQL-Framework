# FedLS-SQL: trạng thái nghiên cứu

File này trả lời bốn câu: ta đang hỏi gì, đã biết gì (kèm mức chắc chắn), còn
chưa biết gì, và đang ở giai đoạn nào. Method và claim đã chốt nằm trong
LAB_LOG (FREEZE 2026-10-26 và hai addendum 2026-10-28); câu chuyện paper:
[DIRECTION_PROPOSAL](DIRECTION_PROPOSAL.md). Số liệu và bằng
chứng: [LAB_LOG](LAB_LOG.md) (từ 2026-10-10) và
[log cũ](../archive/lab_log_2026-10/LAB_LOG_2026-09-24_to_2026-10-09.md).
Setup và protocol: [system_architecture](system_architecture.md). Lệnh chạy:
[PIPELINE_NEXT](PIPELINE_NEXT.md). Các hướng đã cân nhắc trước 2026-10-11:
[archive/directions_2026-10](../archive/directions_2026-10/README.md).

Cập nhật: 2026-10-28.

## 1. Câu hỏi nghiên cứu

Nhiều client giữ dữ liệu Text-to-SQL riêng (Spider, chia theo domain) và cùng
train một model nhỏ (SLM) bằng federated learning. Server có một LLM lớn
frozen (teacher) và một public dataset khác miền (BIRD). Chỉ deploy SLM.

> Dùng teacher và public data khác miền thế nào để SLM federated tốt hơn, và
> phần lợi ích nào thực sự đến từ teacher, từ public data, hay từ cách sắp
> xếp các stage?

**Metric (owner, 2026-10-16, nới 2026-10-29):** mặc định Spider EX (miền
private của client) là metric chính, BIRD EX (miền public) là metric phụ;
luôn báo cả hai. Metric nào gánh câu chuyện thì chọn theo cái làm paper
mạnh nhất (owner quyết định).

## 2. Setup cố định

- Student Qwen2.5-Coder-1.5B-Instruct, LoRA r16. Teacher Qwen2.5-Coder-7B,
  4-bit, frozen, chỉ ở server.
- 5 client, split domain-cluster Dirichlet alpha 0.1 (`k5`). FedAvg theo số
  mẫu. Client chỉ gửi adapter; server gửi adapter đã gộp và, với method,
  một lần public row kèm target nén của teacher để replay. Không ICL, client
  và inference chỉ sinh SQL.
- Stage: `A` = một round private (1 epoch mỗi client rồi FedAvg); `K` = một
  epoch server trên 9,428 câu BIRD train; `K2` = hai epoch liên tục.
  `K[ce]` = gold CE, `K[fkl]` = Hinton (0.5 CE + 0.5 KL, T=2). `A[ntd]` =
  FedNTD ở client (beta 1, tau 3).
- Eval: Spider dev (1,034) và các bản Realistic, SYN, DK; BIRD dev (1,534).
  Spider test (2,147) là tập test cuối; seed 0 đã eval cho method và các
  comparator (LAB_LOG 2026-10-28).

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
| F20 | Edge Spider của teacher ở K2AAA không phải do kéo về base model (anchoring), ở mức kéo của self-teacher | P2.44 `self_k2aaa` (base 1.5B làm teacher): Hinton - self Spider K2 +4.26 (p=.0015), A3 +2.32 (p=.021), DK A3 +5.61; self - gold A3 Spider -0.19; self làm sập BIRD (K2 28.94). Một anchor yếu hơn (cùng gold mass 0.728) chưa được kiểm tra | 1 seed, chưa commit |
| F21 | Client replay với target của teacher giữ BIRD qua các round FedAvg, không làm giảm Spider | `mixkd50_k2aaa` - `hinton_k2aaa` A3: BIRD dev +6.25, Spider dev +1.55, Spider test -0.33 (p=.62) | 1 seed |
| F22 | Replay chỉ giữ BIRD khi có target của teacher | `mixkd50` - `mixgold` (replay gold) BIRD +4.04 (p<.001); `gmixgold` - `gold_k2aaa` BIRD +1.24 (p=.23) | 1 seed |
| F23 | Cùng các row đó train thêm ở server thì BIRD mất ngay ở round đầu | `k2plus_aaa` BIRD 42.96 sau stage server, 37.87 sau A1; method - `k2plus_aaa` BIRD +6.98 (p<1e-10), Spider test -0.70 (p=.27) | 1 seed |
| F24 | So với pipeline cùng dữ liệu không teacher, method hơn rõ trên BIRD, trên Spider test không | method - `gmixgold_k2aaa`: dev Spider +2.51 (p=.009), BIRD +3.52 (p<.001); Spider test +0.56 (103/91, p=.43) | 1 seed |
| F25 | Lợi thế dev của method phần lớn do chọn lọc | method là cấu hình tốt nhất trong 17 trên dev; dev sang test: method -0.91, 3 comparator +0.66 đến +1.04 | 1 seed |
| F26 | Đổi public pool sang SynSQL: method vẫn hơn FedAvg trên 5/5 tập dev và trên Spider test; teacher cùng chiều nhưng nhỏ | P2.54 A3 (nested `76496b4`), paired: method - FedAvg Spider +3.09 (67/35, p=.002), BIRD +4.11 (124/61, p<.001), Realistic +1.57, SYN +1.16, DK +1.68 (p=.27-.35); Spider test 72.99 so với 71.50 (+1.49, 116/84, p=.028). Method - `gmixgold` +0.77, +0.98, +0.20, +1.74, +0.37, không cặp nào significant. Dưới BIRD pool trên dev (Spider -3.38, p=.001; BIRD -14.99), ngang trên Spider test (72.99 so với 73.17) | 1 seed, robustness theo pool |
| F27 | Đảo vai: replay giữ public domain (Spider) nhưng không giúp private (BIRD) | P2.52: Spider +6.29 (p<.001), BIRD -1.69 (p=.061) | 1 seed, appendix |
| F28 | Trên Spider test, mọi arm K2 nằm trong 72.6-73.9, FedAvg 71.50; phần teacher trên Spider khoảng 0.5 | seed 0: method - FedAvg +1.68 (p=.029), `gold_k2aaa` - FedAvg +1.53, method - `gold_k2aaa` +0.14, `hinton_k2aaa` - `gold_k2aaa` +0.47; dev sang test FedAvg +3.90, nhóm K2 +0.66 đến +2.62 | 1 seed, Spider test |
| F29 | Trên Spider test, method ngang train tập trung Spider + BIRD (không privacy) và hơn train tập trung chỉ Spider; FL penalty của dev không còn trên test | seed 0: method - `central_mix` -0.61 (p=.46), - `central` +2.10 (p=.009), - FedNTD +3.49, - local tốt nhất +2.89 (local trung bình 67.27); `central` - FedAvg -0.42 (p=.66; dev +3.77) | 1 seed, Spider test; `central`, `central_mix` chỉ có seed 0 |

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
| Q1 | Vì sao FL thuần thua central 3.8 điểm trên dev và gần như không hơn client tốt nhất (F19)? Trên Spider test seed 0 khoảng cách này không còn (F29) | audit client drift (Q7) |
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
| Q12 | Đảo vai (BIRD private, Spider public): teacher có đóng góp rõ hơn không? | hướng ưu tiên (owner 2026-10-17); P2.43 đã có code, đang chạy early signal (K2 và A1), metric chính là BIRD EX, LAB_LOG 2026-10-17 |
| Q13 | Teacher ở K2 có nâng Spider test không (`hinton_k2aaa` - `gold_k2aaa`, dev +2.12)? | C6, 3 seed (addendum 2 ngày 2026-10-28) |
| Q14 | Forgetting và retention (F14, F21-F23) có lặp lại qua 3 seed không? | eval dev ở A1, A2 seed 1-2; C2-C4 |

Danh sách arm P2.37 giữ làm baseline. Từ 2026-10-12 được thêm arm sau khi
xem kết quả (luật 1, mục 5).

## 5. Giai đoạn và luật đang áp dụng

Giai đoạn hiện tại: **xác nhận** (P2.53, 3 seed, Spider test). Hướng paper
(owner, 2026-10-28): [DIRECTION_PROPOSAL](DIRECTION_PROPOSAL.md).

Luật (owner, 2026-10-29): mục tiêu là paper Q3 hay và mạnh nhất mà kết quả
cho phép. Chỉ giữ cố định ba điều, đều về trung thực:

- Mọi số trong paper có evidence trail (checkpoint, config, dataset, seed,
  file prediction, Git SHA).
- Paper không nói sai cách có số: mỗi số ghi rõ tập (dev hay test); số
  Spider test đã dùng để chọn gì thì không gọi là held-out.
- Thống kê tính đúng: gộp seed bằng question-clustered test, không cộng
  discordant pair qua các seed (R13).

Còn lại là thực hành, nhường chỗ khi cách khác làm paper hay hơn. Không chặn
lựa chọn nào hay gọi kết quả là "mất giá trị" vì bỏ qua một thực hành; nếu
reviewer có thể bắt bẻ thì nói một dòng rồi đề xuất cách làm paper mạnh
nhất. Owner quyết định.

- Thăm dò tự do; mọi run và mọi lựa chọn ghi vào LAB_LOG.
- Chỉ chạy control khi kết quả của nó có thể đổi method hoặc reviewer chắc
  chắn sẽ hỏi.
- Claim giữ khi đa số kết quả kiểm nó ủng hộ (owner 2026-10-28). Claim và
  tập eval được thêm bất cứ lúc nào (ví dụ Spider-DK, 2026-10-29).
- Chọn trên dev làm số phồng lên: mỗi so sánh trên Spider dev có khoảng 140
  câu lệch nhau, nên cái tốt nhất trong 10 biến thể không có tác dụng thật
  vẫn thấy khoảng +1.7 điểm. Kết quả gánh câu chuyện nên giữ được ở seed
  khác hoặc trên test.
- Chỉ claim điều có comparator tách riêng. R9: so central và FL ở cùng số
  pass, không chỉ checkpoint cuối.

Đã bỏ: luật pass/fail viết trước cho từng thí nghiệm (R1-R6, R11, R12) và
danh sách arm cố định của giai đoạn E (2026-10-12); R8, R10 và phần số seed
của R13 (2026-10-29: luật ràng buộc hướng bài thì bỏ). Kết quả đã ghi theo
các luật đó giữ nguyên làm lịch sử.

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
