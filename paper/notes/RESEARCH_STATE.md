# FedLS-SQL: trạng thái nghiên cứu

File này trả lời bốn câu: ta đang hỏi gì, đã biết gì (kèm mức chắc chắn), còn
chưa biết gì, và đang ở giai đoạn nào. Không chứa method hay câu chuyện paper
đã chốt: câu chuyện sẽ được chọn từ kết quả của giai đoạn E. Số liệu và bằng
chứng: [LAB_LOG](LAB_LOG.md) (từ 2026-10-10) và
[log cũ](../archive/lab_log_2026-10/LAB_LOG_2026-09-24_to_2026-10-09.md).
Setup và protocol: [system_architecture](system_architecture.md). Lệnh chạy:
[PIPELINE_NEXT](PIPELINE_NEXT.md). Các hướng đã cân nhắc trước 2026-10-11:
[archive/directions_2026-10](../archive/directions_2026-10/README.md).

Cập nhật: 2026-10-12.

## 1. Câu hỏi nghiên cứu

Nhiều client giữ dữ liệu Text-to-SQL riêng (Spider, chia theo domain) và cùng
train một model nhỏ (SLM) bằng federated learning. Server có một LLM lớn
frozen (teacher) và một public dataset khác miền (BIRD). Chỉ deploy SLM.

> Dùng teacher và public data khác miền thế nào để SLM federated tốt hơn, và
> phần lợi ích nào thực sự đến từ teacher, từ public data, hay từ cách sắp
> xếp các stage?

Luôn báo cả hai miền: Spider (miền private của client) và BIRD (miền public).
Miền nào là endpoint chính được chọn cùng câu chuyện, sau giai đoạn E.

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
| F3 | Soft label của teacher hơn gold cùng chuỗi trên Spider, nhưng ở Coder-1.5B edge này mất khi round cuối là plain | +2.42 (0.5B, p=.020), +2.03 (1.5B-Instruct, p=.033), +2.03 (0.5B K2AAA, p=.048); Coder-1.5B: v1 +1.35 (p=.23), plain +0.39 (p=.76). Biến thể Spider dương ở cả 6 ô (2 chuỗi), nhưng set có p<.05 đổi (DK với NTD, SYN plain) | yếu ở Coder-1.5B; phần robustness là thăm dò (R8) |
| F4 | Trong stage K, Hinton làm quên Spider ít hơn gold | Coder-1.5B: Spider +3.48 sau K1, +3.00 sau K2; 0.5B K2AAA: +3.29 sau K2 | 1 seed mỗi model |
| F5 | Round private cuối quyết định điểm cân bằng Spider-BIRD | Coder-1.5B plain so với NTD: Hinton Spider +2.51, BIRD -3.32; gold Spider +3.48 (p<.001), BIRD -1.04 (p=.21); 0.5B: NTD không tốn Spider, BIRD +1.89 (2 seed, p=.004) | 1-2 seed |
| F6 | NTD ở round giữa (A2) không có tác dụng, vì K2 sau đó đưa BIRD về cùng mức | 0.5B P2.25: hai model cuối gần như trùng (Spider 20/20 discordant) | 1 seed, chưa thử ở 1.5B |
| F7 | FedNTD và FedProx không phải FL baseline mạnh hơn FedAvg ở setting này | Coder-1.5B FedNTD - FL BIRD -1.37; 0.5B FedProx (P2.20) | 1 seed |
| F8 | Vị trí K: K càng sớm Spider càng cao, K càng muộn BIRD càng cao; edge BIRD của teacher chỉ rõ khi K muộn | 0.5B alpha 0.5, cùng budget: Spider K2AAA 63.93 / AK2AA 63.15 / AKAKA 62.57 (Hinton), cùng thứ tự với gold; không cặp nào p<.1; teacher - gold BIRD chỉ có ý nghĩa ở AKAKA (+3.13) | thăm dò, chưa thử ở 1.5B |
| F9 | FL thua central khi so cùng số lần đi qua dữ liệu; ở Coder-1.5B khoảng cách tăng theo số pass | Coder-1.5B alpha 0.1: +1.93 / +2.90 / +3.77 (E1-E3, p=.13/.028/.003), FL đạt đỉnh ở A2 rồi giảm; khoảng cách JOIN xuất hiện trước. 0.5B alpha 0.5: +4.6 / +4.8 / +1.8 (central overfit ở E3). BIRD không có khoảng cách | 1 seed mỗi model |
| F10 | EX phóng đại khoảng 5-7 điểm đều ở mọi arm; mọi contrast giữ dấu dưới test-suite EX | Coder-1.5B seed 0, Spider dev | 1 seed |
| F11 | Gain của `h_plain` so với FL nằm ở câu JOIN; round NTD cuối giữ lỗi over-join | JOIN +9.07 (p<.001), no-JOIN +0.96; over-join 87 (FL), 84 (v1), 57 (`h_plain`) | thăm dò (R8 kiểm trên seed mới) |
| F12 | Sample nhiều lần có headroom lớn trên câu train | pass@8 - greedy 13-18 điểm, cần oracle gold | 1 seed, chỉ là trần |

Hướng đã đóng vì kết quả âm hoặc quá tốn: plan task và CoT ở client hoặc
server (P2.10-P2.15), retention loss (P2.9), weight merge (A1), KID, GKD,
ICL, self-consistency, public pool cùng miền, public pool không có
gold SQL (owner quyết định 2026-10-11 sau P2.36: không mở hướng teacher thay
nhãn). P2.16 centralized E1-E4 chưa
từng được publish, không trích dẫn.

## 4. Chưa biết (câu hỏi cho giai đoạn E, Coder-1.5B, seed 0)

| # | Câu hỏi | Cần arm |
|---|---|---|
| Q1 | Federation có cần không (local-only so với FL), và vì sao FL thua central 3.8 điểm ở Coder-1.5B? | local-only (P2.37), FL và central (có) |
| Q2 | Teacher có hơn gold ở Coder-1.5B không, và có phụ thuộc lịch không? Chuỗi plain: không trên Spider (P2.36) | cặp Hinton/gold K2AAA và AKAKA plain (P2.37) |
| Q3 | Đặt K ở đâu: đầu (K2AAA), xen kẽ (AKAKA), hay chuỗi hiện có? | Hinton và gold K2AAA; Hinton và gold AKAKA plain (không NTD); `h_plain` và `g_plain` (có) |
| Q4 | Trần khi có đủ dữ liệu ở một chỗ là bao nhiêu? | `central_mix` (Spider + BIRD gold) |
| Q5 | Teacher SQL (SeqKD) có khác soft label không? | không trong giai đoạn E (P2.6: edge mất sau round private cuối) |
| Q6 | Kết quả có giữ khi heterogeneity khác không? | alpha 0.5, để sau |

Danh sách arm của giai đoạn E đã chốt (P2.37, LAB_LOG 2026-10-11) trước khi
chạy; không thêm arm sau khi thấy kết quả.

## 5. Giai đoạn và luật đang áp dụng

1. **E, thăm dò** (hiện tại): hoàn thiện bảng baseline Coder-1.5B ở seed 0,
   chỉ trên Spider dev và BIRD dev.
2. **Chốt câu chuyện:** một entry có ngày trong LAB_LOG nêu claim, arm, phép
   kiểm và câu chữ cho từng kết quả, trước khi chạy seed 1-2 hay eval Spider
   test.
3. **C, xác nhận:** seed 0-2, Spider test cho claim Spider.

Luật còn hiệu lực (chi tiết trong LAB_LOG 2026-10-11):

- R10: Spider test chỉ dùng để xác nhận; không dùng để chọn cấu hình.
- R13: gộp seed bằng question-clustered test; mặc định 3 seed (power đã
  tính); không thêm seed sau khi đọc kết quả.
- R8: phân tích JOIN chỉ thành claim khi giữ trên seed không sinh ra nó.
- R9: so central và FL ở cùng số pass, không chỉ checkpoint cuối.
- Chỉ claim điều có comparator tách riêng; thành phần giữ lại mà không có
  bằng chứng ở setting hiện tại thì ghi là thừa kế, không claim.
- Paper công khai quá trình chọn (ngày các rule, dữ liệu đã xem, số
  checkpoint đã eval trên dev).

Tạm treo: R12 (method `h_plain` và claim P/T/D) và R11, cho tới khi câu
chuyện được chốt lại. Kết quả đã ghi theo các rule cũ giữ nguyên.
