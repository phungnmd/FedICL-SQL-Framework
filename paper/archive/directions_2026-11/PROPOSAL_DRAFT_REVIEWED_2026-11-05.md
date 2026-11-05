# FedLS-SQL: đề xuất cuối (bản nháp 2026-11-05, chờ phản biện)

Mục tiêu (owner): thắng baseline trên miền private (Spider EX, báo dev và
test). BIRD dev là kết quả phụ. Vai trò teacher và RL phải đo được trên Spider.
Ràng buộc: teacher Coder-7B 4-bit chỉ ở server trên BIRD; student Coder-1.5B
LoRA r16; 5 client Spider alpha 0.1; hai A5000; deploy SLM SQL-only greedy.

Đã bỏ (owner 2026-11-05): teacher tổng hợp dữ liệu mới (BIRD đã đủ); CoT
làm trục chính khi chưa qua cổng ở mục 3.

## 1. Hướng chính P (không CoT)

```text
Server, BIRD:  Hinton KD (0.5 CE + 0.5 T^2 KL, T=2), 2 epoch -> K2      [teacher]
Client:        a round FedAvg SFT trên gold Spider (a = 0..2)             [FL]
Client:        r round: sinh K=8 SQL, execution check, DPO + NLL trên
               pair đúng/sai, retry câu toàn sai, rồi FedAvg               [RL]
Deploy:        SLM, SQL-only, greedy
```

Căn cứ (seed 0, centralized trừ khi ghi FL):
- RL: `s1` 58.80 lên 74.18 dev; sau Spider SFT thêm +1.93 (`g3d`-`g2`, p=.012);
  preference term +2.22 (`g3d`-`g3n`, p=.004).
- SFT trước RL có lợi: `sql_rl9` 75.53 so với `s1_rl9` 74.18 (+1.35, p=.33);
  P2.59 `tp3`-`tp_r3` +3.00 (p=.023).
- Teacher: `hinton_k2aaa`-`gold_k2aaa` +2.13 dev (p=.020), +0.47 test (FL).
- Mốc FL Spider test: FedAvg 71.50, `hinton_k2aaa` 73.50, FedProx 70.42,
  FedCoLLM-style 66.88 (seed 1), teacher 7B zero-shot 77.22.
- Literature: chưa thấy federated + RL/DPO + Text-to-SQL; từng mảnh đã có
  (Hinton 2015, FedAvg, Iterative RPO, ExCoT, OpenFedLLM FedDPO).

## 2. Biến thể của P có thể chạy (mỗi biến thể một phép so)

| # | Biến thể | So với | Căn cứ | Ưu tiên |
|---|---|---|---|---|
| V1 | Điểm xuất phát Hinton K2 | gold K2, cùng lịch | Đo vai trò teacher trên Spider; RL nén chênh lệch điểm xuất phát (14.80 còn 1.35) | Bắt buộc, quyết định |
| V2 | Lịch: a = 1-2 round SFT trước RL | a = 0 | `sql_rl9` > `s1_rl9`; `tp3` > `tp_r3` | Bắt buộc |
| V3 | Q: một round DPO + NLL trên BIRD ở server, teacher SQL đúng làm chosen, SQL sai của student làm rejected, trên câu student sai hết | cùng câu, gold làm chosen | ExCoT round off-policy; có sẵn 1,266 lời giải teacher đã kiểm và cache SeqKD 5,319 dòng | Chạy nếu V1 < +1 Spider |
| V4 | Teacher xen kẽ: sau mỗi round FL, server chạy lại KD (hoặc Q) trên BIRD | P không xen kẽ | FedCoLLM, FedMKT, FedDF; nhưng của ta: server step làm Spider giảm ngay (71.57 xuống 65.57), kết thúc bằng K mất khoảng 8 Spider | Chỉ làm baseline FedCoLLM-style, không làm method |
| V5 | Task ẩn: ở K2 thêm target phụ (CoT hoặc plan của teacher) bên cạnh SQL, inference SQL-only | K2 thường | Distilling step-by-step (Hsieh et al. 2023); P2.14 +1.84 trên 1,000 dòng, P2.15 -0.97 trên toàn bộ (student cũ) | Thấp |
| V6 | D: CoT mode làm explorer cho câu private SQL sai hết, SQL đúng tìm được làm chosen cho prompt SQL; deploy SQL | (a) SQL explorer cùng compute (K=64 SQL so với K=8 CoT), (b) gold làm chosen, (c) retry thường | C7: `c1` cứu 42.3% câu `s1` sai hết, `s1` retry 23.83%; nhưng hai model khác nhau và không cùng compute | Pilot rẻ, centralized |

Ghi chú V6 "format prompt khác": explorer có thể là CoT tự do, CoT có cấu trúc,
hay SQL với prompt khác/temperature cao. Câu cần trả lời là đổi format có cứu
nhiều câu hơn lấy thêm sample cùng format ở cùng compute không, và pair cứu
được có hơn gold làm chosen không (client có gold). Chưa có bằng chứng chắc.

## 3. Hướng CoT (phụ, có cổng)

```text
Server, BIRD:  teacher viết CoT theo clause kiểu VCoT-SQL (thấy gold, prompt
               trung tính, 3 few-shot), lọc 4 tầng; SFT -> cotV
Client:        RL CoT (DPO + NLL trên CoT tự sinh), FedAvg; deploy CoT
```

Bằng chứng ngược chiều trên Spider: C1 -3.29 dev; AutoThinkSQL (train BIRD, eval
Spider, greedy) CoT DPO 69.14 so với SQL 84.23; Liu et al. CoT DPO +0.6-1.1
Spider dev ở 7B; không bài nào cho CoT > SQL ở 1.5B greedy Spider cùng data.
Gain Spider của VCoT đến từ CoT viết trên Spider train, ta không có. Teacher
thấy gold: Lee et al. (toán) cảnh báo prompt "rationalize toward" làm giảm
16.2, prompt trung tính khoảng 1; P2.59 `tc` (thấy gold, không kiểm SQL của
writer) thua template 4.45.

Cổng: (1) BIRD dev `c1_rl8` so với `s1_rl9`; (2) pilot cotV SFT so với SQL-only
trên cùng tập đã lọc và `sql1`, khoảng 30 GPU-h. Chỉ chạy RL CoT nếu (2) hơn rõ
cả hai trên Spider dev.

## 4. Baseline và control của bảng chính

FedAvg SFT (cùng round và cùng compute), FedProx, FedCoLLM-style (cần seed 0,
2), `hinton_k2aaa`, local tốt nhất, centralized P (cận trên), teacher 7B
zero-shot, base 1.5B; federated rejection-sampling SFT (NLL trên SQL đúng tự
sinh) để tách preference term; 3 seed, question-clustered test; Spider dev +
test, BIRD dev, Spider-DK/Realistic/SYN cho arm chốt; communication và GPU-h.

## 5. Thứ tự

| Bước | Nội dung | GPU-h | Quyết định |
|---|---|---:|---|
| 0 | Spider test `s1_rl9`, `sql_rl9`, `sql2_e1`; BIRD dev `c1_rl8`, `s1_rl9` | < 8 | Mốc test của route SQL RL |
| 1 | V1 centralized: route `s1` từ Hinton K2 và gold K2 | ~25 | ≥ +1 Spider dev và test: giữ teacher như hiện tại; dưới: thêm V3 |
| 1b | V6 pilot: một round DPO + NLL từ `s1_rl9` với pair cứu bởi CoT / SQL K=64 / gold-chosen / retry | ~10 | V6 vào FL chỉ nếu hơn cả gold-chosen và SQL K=64 |
| 2 | Pilot FL một round | ~8 | Chi phí, pair theo client |
| 3 | FL seed 0: P-Hinton (V2 lịch tốt nhất), P-gold, rejection-SFT, FedCoLLM-style seed 0 | ~60 | Bảng chính seed 0 |
| 4 | Seed 1-2 cho các arm chính | ~130 | Claim chính |
| 5 | Eval đầy đủ | ~20 | |
| opt | Cổng CoT (mục 3), V5, alpha 0.5 | ~30 mỗi mục | |
