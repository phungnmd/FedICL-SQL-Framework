# FedLS-SQL: hướng nghiên cứu

Cập nhật 2026-11-07. Chưa có kết quả nào kể từ fresh start; mọi GPU-h dưới
đây là ước lượng từ số đo của các job cùng loại (mục 7). Bản trước:
`archive/paper/directions_2026-11/DIRECTION_2026-11-07.md` (local) và Git
history.

## 1. Bài toán trong một đoạn

Năm client giữ dữ liệu Spider riêng, cùng train model Qwen2.5-Coder-1.5B bằng
FL, chỉ deploy model 1.5B. Server có thể dùng teacher Qwen2.5-Coder-7B (frozen)
và dữ liệu public. Mục tiêu: một method thắng rõ các baseline federated.

Hai quan sát định hướng:

- FedAvg SFT đã gần bằng SFT tập trung (Spider test 71.50 so với 71.08), nên
  method sửa drift (FedProx, SCAFFOLD, aggregation mới) gần như không có chỗ
  để thắng. Phải đổi cái model học.
- Text-to-SQL có verifier sẵn: client chạy SQL trên database của mình là biết
  đúng hay sai, không cần gửi dữ liệu đi đâu.

## 2. Method gồm ba lựa chọn

Một method của paper = **cách client train** + **việc server làm thêm** +
**thời điểm server làm**. Mỗi phần có vài lựa chọn (mục 3, 4, 5); mục 6 chọn
thứ tự thử.

![Method tổng thể](figures/01_overview.svg)

Hình trên là tổ hợp đang đề xuất: client DPO + NLL, server KD on-policy có
cổng (S2), chạy sau mỗi vòng.

## 3. Cách client train

| | Lựa chọn | Làm gì | Vai trò |
|---|---|---|---|
| C1 | DPO + NLL bằng execution | Model sinh 8 SQL mỗi câu, chạy trên database riêng, học ưu tiên câu đúng hơn câu sai | Ứng viên method |
| C2 | RFT | Như C1 nhưng chỉ SFT trên các sample đúng, bỏ câu sai | Đối chứng: câu sai có giúp không |
| C3 | SFT thêm vòng | FedAvg SFT bình thường, thêm vòng | Baseline chính |

Chưa chốt. Round 1 trong `PIPELINE_NEXT.md` chạy cả ba từ cùng điểm xuất phát
(FedAvg R3) và quyết định:

- C1 hơn C2 và C3: giữ C1.
- C2 bằng C1: client dùng C2 vì đơn giản hơn.
- Cả hai không hơn C3: phía client không có method; phần server phải gánh cả
  paper.

![Vòng client](figures/02_client_round.svg)

Chi tiết C1:

1. Mỗi vòng, client lấy một phần câu hỏi của mình (400 câu), sample K=8 SQL ở
   T=0.7 từ model global.
2. Chạy từng SQL so với gold trên database riêng. SQL chỉ tính là đúng khi
   cũng khớp gold trên vài bản database đổi giá trị (cách sinh database của
   test-suite, Zhong et al. 2020), để giảm "đúng giả".
3. Chọn cặp: chosen là SQL đúng (dùng gold nếu không sample nào đúng);
   rejected ưu tiên SQL chạy được nhưng ra kết quả sai, rồi mới tới SQL lỗi.
4. Train DPO + NLL 2 epoch, reference là model global của vòng đó, gửi LoRA.
5. Server FedAvg theo số cặp. Vòng sau sample lại từ model mới.

Paper gần nhất: Iterative RPO (tập trung, toán), ExCoT (tập trung, SQL,
32-70B, có CoT), FedDPO trong OpenFedLLM, FedBiscuit, Fed-GRPO. Điểm phải đối
mặt: Liu et al. (ACL 2025) và ExCoT thấy DPO SQL-only không giúp ở 6.7B trở
lên; ở 1.5B chưa ai đo.

## 4. Việc server làm thêm

### 4.1 Vì sao cần bước server

C1 chỉ biến cái model đã biết (pass@8) thành câu trả lời greedy. Muốn nâng
trần đó phải thêm kiến thức mà dữ liệu client không có: dữ liệu public và
teacher ở server. Nếu server chỉ train giống client trên dữ liệu public, nó
chỉ là "client thứ 6"; bước server nên dùng thứ chỉ server có: teacher, gold
public, adapter của mọi client, compute tập trung.

Teacher không dùng để sửa câu student viết sai: teacher chỉ khớp gold trên
5,319 / 9,428 câu BIRD train (56%), và server đã có gold.

### 4.2 Dữ liệu ở server

Owner cho phép dùng BIRD hoặc SynSQL (2026-11-07), chọn theo cái hợp với lựa
chọn server hơn.

| | BIRD train (có evidence) | SynSQL-2.5M (OmniSQL, Apache-2.0) |
|---|---|---|
| Quy mô | 9,428 câu, 69 database | 2.5M câu, 16,583 database (có sẵn trên máy); pool đã lọc 3,336 câu trên 3,027 database, lấy thêm được |
| Giống Spider ở đâu | Database thật, giá trị thật | Nhiều database và nhiều domain như Spider; không có evidence |
| Khác Spider ở đâu | Có evidence, prompt dài, SQL khó hơn | Câu hỏi sinh tự động, nhiều kiểu văn phong; database chỉ khoảng 2 dòng mỗi bảng |
| Có sẵn từ teacher | SQL teacher (5,319 câu khớp gold), logit cache trên gold, 1,266 CoT đã kiểm | Chưa có; dataset kèm sẵn CoT |
| Nhãn bằng execution | Tin được | Yếu: database quá ít dòng nên SQL sai vẫn dễ ra cùng kết quả |
| Paper dùng | OmniSQL, SQLoom, ExCoT, Think2SQL, Reasoning-SQL | OmniSQL, SLM-SQL, SQL-R1, CAPER, EXPO-SQL |

### 4.3 Các lựa chọn

| | Server làm gì | Teacher | Chỉ server có |
|---|---|---|---|
| S0 | Không làm gì, chỉ FedAvg | Không | |
| S1 | KD offline: student bắt chước xác suất từng token của teacher trên SQL có sẵn | Có | Teacher |
| S2 | KD on-policy có cổng: student tự viết SQL, teacher chấm từng token, chỉ dùng câu mà SQL teacher khớp gold | Có | Teacher |
| S3 | DPO bằng execution trên dữ liệu public, giống C1 | Không | Gold public |
| S4 | Cho 5 adapter client cùng viết SQL trên dữ liệu public, giữ câu đúng, model global học từ đó | Không | Adapter mọi client |
| S5 | Teacher viết CoT ngắn, student học suy luận rồi mới viết SQL | Có | Teacher |

**S1. KD offline.** Loss là KL giữa phân phối token của student và teacher
trên chuỗi SQL cố định (gold hoặc SQL teacher). Trên BIRD, logit cache đã có;
một epoch 9,428 dòng mất 3.3-3.6 h. Paper: KID (SQL, 1B: reverse-KL KD hơn SFT
khoảng 2 điểm), MiniLLM, FedCoLLM.

![S1](figures/03_s1_offline_kd.svg)

**S2. KD on-policy có cổng execution.** Model global sinh SQL; teacher chấm
log-prob từng token trên SQL của student và trên SQL đúng; loss kiểu
DistiLLM-2 (kéo lên ở SQL đúng, đẩy xuống ở token student mà teacher cho là
khó xảy ra). Cổng: chỉ dùng câu mà SQL teacher khớp gold. Client có tín hiệu
thưa (cả câu đúng hay sai), server có tín hiệu dày (sai ở token nào). Student
train trên BIRD đã chiếm khoảng 20 GiB nên teacher chấm ở card còn lại, theo
từng vòng. Paper: DistiLLM-2 (đúng cặp Coder 7B → 1.5B, code: HumanEval 30.7
→ 42.2), GKD, KID, SERL-SQL, FedCoLLM.

![S2](figures/04_s2_gated_kd.svg)

**S3. DPO bằng execution trên dữ liệu public.** Như C1 nhưng ở server. Bản
GRPO online quá đắt; bản DPO trên tập con khoảng 2,000 câu BIRD tốn khoảng
5-8 h phần sample. Bằng chứng chuyển BIRD → Spider mạnh nhất trong các lựa
chọn (Think2SQL 3B: 72.5 → 77.0).

![S3](figures/05_s3_exec_rl.svg)

**S4. Chưng cất từ ensemble adapter client.** Kiểu FedDF với chọn output bằng
execution. Không cần teacher. Các adapter đều train trên Spider nên có thể ít
khác nhau.

![S4](figures/06_s4_ensemble.svg)

**S5. CoT ngắn từ teacher.** Teacher viết lời giải từng bước trên dữ liệu
public, student SFT rồi client DPO trên cả chuỗi. Inference chậm khoảng 6.6
lần; đổi setup SQL-only ở client. Paper: Liu et al. ACL 2025, ExCoT,
Struct-SQL, OmniSQL.

![S5](figures/07_s5_cot.svg)

## 5. Thời điểm server làm

| | Khi nào | Ai làm vậy | Ưu | Nhược |
|---|---|---|---|---|
| Trước FL | Một lần, trước các vòng client | GPT-FL | Rẻ, ablation sạch | Đóng góp một lần, dễ bị quên; nếu thắng, đóng góp chỉ là "khởi tạo tốt hơn", không còn gì federated |
| Sau mỗi vòng | Sau FedAvg, trước khi gửi model xuống | FedCoLLM, FedBiOT, FedBiscuit | On-policy đúng model vừa aggregate; phần server thành một phần của FL | Thêm thời gian mỗi vòng |
| Song song | Server là participant thứ 6 trong FedAvg | FedAuto | Không thêm thời gian tuần tự | Trọng số server là hyperparameter; dữ liệu public nhiều nên dễ lấn át |

Một lần sau FL bị loại: model deploy cho client sẽ bị dữ liệu public định hình
sau cùng.

![Thời điểm](figures/08_placement.svg)

## 6. Thứ tự thử

Đang research (2026-11-07); mục này được viết lại khi có kết quả.

## 7. Số đo chi phí

GPU-h trên một card A5000; hai card chạy hai lane song song. Nguồn:
`fedicl-sql/docs/A5000_RUN_CONFIG.md`.

| Job | Số đo |
|---|---|
| Một vòng FL SFT, 5 client, 8,659 dòng Spider | 1.6-1.7 h |
| Eval SQL-only Spider dev, batch 16 | 0.07-0.3 h |
| Sample K=8 cho DPO (Spider) | 300 dòng trong 0.3-0.7 h |
| Update DPO + NLL | 0.4-0.9 h mỗi vòng (cặp từ khoảng 300 dòng) |
| CE trên BIRD gold, 9,428 dòng, 1 epoch | 2.7 h, khoảng 20 GiB |
| KD từ logit cache BIRD, 9,428 / 5,193 dòng | 3.3-3.6 h / 2.17 h |
| SFT trên CoT ngắn, 2,132 dòng | 1.3 h |
| Teacher sinh CoT ngắn trên BIRD, 4-bit batch 8 | 7.0-7.2 s mỗi output |
| Teacher sinh CoT trên SynSQL, 1,024 token | 13-18 s mỗi output |
| Eval CoT so với SQL-only | khoảng 6.6 lần chậm hơn |

Chưa đo: tốc độ và bộ nhớ khi teacher chấm từng token trên prompt BIRD; sample
K=8 trên BIRD (prompt dài hơn Spider, ước lượng 1.5-3 lần); thời gian CPU để
chạy 50-100k SQL gán nhãn mỗi vòng.

## 8. Baseline và metric

Baseline: zero-shot student; teacher zero-shot (tham khảo); mỗi client train
riêng; FedAvg SFT (cùng vòng và cùng GPU-h); FedProx; FedOPT + Lorar (FL4SP);
SFT tập trung; RFT (C2); DPO offline (không sample lại); method chạy tập
trung; SFT thêm dữ liệu public (đối chứng cho mọi lựa chọn server).

Metric: EX greedy trên Spider test (batch 16) là số chính; Spider dev (EX và
test-suite) để chọn cấu hình; Spider-Realistic, SYN, DK cho độ bền; BIRD dev
khi server dùng BIRD. Kèm số cặp mỗi client, GPU-h và dung lượng truyền mỗi
vòng, kết quả theo độ khó. Ba seed cho arm chính, gộp seed bằng kiểm định theo
cụm câu hỏi.

Ngân sách cả paper với C1 (ước lượng): 200-450 GPU-h, khoảng 4-10 ngày trên
hai card.

## 9. Quyết định của owner

- 2026-11-06: chạy C1 trước, không teacher. Teacher là tuỳ chọn. Dùng lại
  adapter FedAvg SFT `p227_fl_aaa_s0` (R3) làm baseline và điểm xuất phát.
- 2026-11-07: thêm phần server vào hướng nghiên cứu; dữ liệu server có thể là
  BIRD hoặc SynSQL.

Tên cũ trong bản trước: Hướng 1 = C1; Hướng 2 ≈ S5; Hướng 3 ≈ S3 (có thêm
chosen từ teacher); Hướng 4 ≈ S2 (chưa có cổng); cách đặt A, B, C = song song,
sau mỗi vòng, trước FL.

## 10. Diagram

Nguồn Mermaid (`.mmd`) và SVG trong `figures/`. Ô màu cam là bước chính của
mỗi hình. Sửa file `.mmd` rồi render lại từ thư mục `figures/`:

```bash
for f in *.mmd; do npx -y -p @mermaid-js/mermaid-cli@11.4.2 mmdc -q -i "$f" -o "${f%.mmd}.svg" -c mermaid.config.json -b white; done
```
