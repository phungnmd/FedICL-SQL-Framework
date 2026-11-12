# Đề xuất paper FedLS-SQL: tên, outline và thực nghiệm

Ngày 2026-11-13. Số liệu lấy từ `paper/notes/RESEARCH_STATE.md` (mục 4) và
`LAB_LOG.md`; nguồn tham khảo lấy từ `paper/notes/LITERATURE.md`.

Giả định của bản này: dòng gold của seed 1 xác nhận vai trò teacher, tức là
sau DPO dòng Hinton vẫn cao hơn dòng gold khi gộp hai seed và khoảng tin cậy
không chứa 0. Mục 9 nói phần nào đổi nếu giả định không đúng.

## 1. Tóm tắt

| Mục | Đề xuất |
|---|---|
| Title | **Distill at the Server, Verify at the Client: Federated Text-to-SQL for Small Language Models** |
| Tên method | FedLS-SQL (Federated LLM-to-SLM for Text-to-SQL) |
| Loại paper | Empirical method paper, cấu trúc IMRaD mở rộng cho ML |
| Venue | Data & Knowledge Engineering, Int. J. Data Science and Analytics, Neural Processing Letters, Distributed and Parallel Databases; stretch: J. Intelligent Information Systems |
| Kết quả chính (Spider test EX) | Method 76.71 / 77.04 (seed 0 / 1), FedAvg 71.26 / 71.87, SFT tập trung Spider + BIRD 73.96, teacher 7B zero-shot 77.22 |
| Thực nghiệm phải chạy thêm | khoảng 60 GPU-h trên một A5000 (mục 7.3), tức khoảng 2.5 ngày chạy liên tục |
| Thực nghiệm nên chạy để hướng tới Q2 | khoảng 55 GPU-h nữa (mục 7.4) |

## 2. Câu chuyện của paper

Năm tổ chức giữ dữ liệu Text-to-SQL riêng và cùng train một model 1.5B; chỉ
model 1.5B được deploy. Trong federation này mỗi bên có một nguồn giám sát mà
bên kia không có. Server có GPU, dữ liệu public (BIRD) và một teacher 7B: nó
distill teacher vào student trước khi các round federated bắt đầu. Client có
database riêng: chạy một câu SQL trên database đó là biết đúng hay sai, nên
mỗi client tự tạo cặp preference (SQL đúng / SQL sai do chính model sinh ra)
và train DPO + NLL; server chỉ average update. Không có dữ liệu client nào
rời client, và teacher không bao giờ thấy dữ liệu client.

Hai nguồn này sửa hai loại lỗi khác nhau. Verifier ở client loại bỏ SQL không
chạy được (execution errors 211 xuống 58, phần lớn là `no such column`).
Teacher ở server để lại phần lead nằm ở các câu chạy được nhưng sai kết quả,
trên nhóm extra-hard, là loại lỗi mà DPO không chạm tới. Kết quả là model
1.5B cao hơn FedAvg 5.3 điểm trên Spider test (hai seed gộp), cao hơn cả SFT
tập trung trên Spider + BIRD (không có privacy), và ngang teacher 7B
zero-shot trên domain của client dù nhỏ hơn gần 5 lần.

## 3. Tên

### 3.1 Title

**Distill at the Server, Verify at the Client: Federated Text-to-SQL for
Small Language Models** (14 từ).

Hai vế trước dấu hai chấm là hai stage của method và cũng là hai nửa của
Hình 1; vế sau mang các từ khóa tìm kiếm (federated, Text-to-SQL, small
language models). Abstract nói rõ tỉ trọng: stage ở client cho phần lớn gain
(+3.2 đến +3.9), stage ở server cho thêm khoảng 1.4.

Bản dự phòng cho venue thích title mô tả, có tên method:

- FedLS-SQL: Server-Side Distillation and Client-Side Execution-Verified
  Preference Optimization for Federated Text-to-SQL (11 từ).

### 3.2 Tên method

`FedLS-SQL`, giải nghĩa một lần ở Introduction: federated training đưa kiến
thức từ một LLM ở server sang một SLM được deploy. Search ngày 2026-11-13
không thấy method nào tên FedLS-SQL; tên gần nhất là Multi-FedLS (framework
chạy FL trên multi-cloud, khác chủ đề).

Hai stage có tên riêng để dùng trong bảng và hình: *server distillation*
(Hinton KD trên BIRD) và *execution-verified federated DPO*.

### 3.3 Keywords

Federated learning; Text-to-SQL; small language models; knowledge
distillation; direct preference optimization; execution feedback.

## 4. Cấu hình paper

| Mục | Giá trị |
|---|---|
| Ngôn ngữ | Tiếng Anh |
| Độ dài | khoảng 9,200 từ phần chính (không tính references, appendix) |
| Bảng, hình | 6 bảng và 5 hình ở phần chính; bảng chi phí và hyperparameter ở appendix |
| Citation | dạng số theo template của venue (Elsevier / Springer), chốt khi chọn venue |
| Output | LaTeX theo template venue |
| Thống kê | mỗi dòng chính: trung bình và độ lệch chuẩn trên 3 seed; so sánh cặp: bootstrap theo database trong một seed, cluster theo câu hỏi khi gộp seed |

## 5. Contributions (cuối Introduction)

1. Setting: federated Text-to-SQL với một decoder SLM được deploy một mình,
   đo bằng execution accuracy; dữ liệu client không rời client, teacher chỉ
   chạy ở server trên dữ liệu public khác domain.
2. Execution-verified federated DPO: mỗi round, client sample 8 SQL cho mỗi
   câu hỏi từ model hiện tại, gán nhãn bằng execution trên database của
   mình, ghép cặp đúng / sai (gold SQL làm chosen khi không sample nào
   đúng), train DPO + NLL; server làm FedAvg trên LoRA. Work gần nhất:
   FedDPO trong OpenFedLLM và FedBiscuit (preference của người), Liu et al.
   2025 và ExCoT (DPO tập trung, 7B trở lên).
3. Server distillation có control: Hinton KD từ teacher 7B trên BIRD trước
   các round federated, so với cùng câu hỏi BIRD nhưng dùng gold SQL, và so
   với soft target không cần teacher. Work gần nhất: FedMKT, FedCoLLM,
   CrossLM (không có control "cùng dữ liệu server, gold label").
4. Kết quả: cao hơn FedAvg 5.3 điểm trên Spider test, gain giữ trên Spider
   dev, DK, SYN, Realistic (các set không dùng để chọn gì), cao hơn SFT tập
   trung không privacy, ngang teacher 7B zero-shot.
5. Phân tích: mỗi stage sửa loại lỗi nào, thành phần các cặp co lại thế nào
   qua các round, vì sao DPO chỉ trên SQL có gain ở 1.5B trong khi các báo
   cáo ở 7B trở lên thì không, và trần khoảng 20% câu chạy được nhưng sai
   kết quả.

Không dùng "first".

## 6. Outline

Ký hiệu: [có] số đã có và committed; [chờ] đang chạy hoặc đã queue; [M1]
đến [M5] và [S1] đến [S4] là các thực nghiệm ở mục 7.

### 1. Introduction (khoảng 1,000 từ)

- 1.1 Bối cảnh: nhiều tổ chức có database và câu hỏi riêng, không gửi được
  ra ngoài; model nhỏ rẻ để deploy; FL là cách train chung.
- 1.2 Vấn đề: FedAvg SFT đã gần bằng SFT tập trung, nên các method sửa
  client drift (FedProx, FedNTD, aggregation mới) có ít chỗ để thắng. Phải
  đổi cái model học, không phải cách gộp.
- 1.3 Ý chính: giao mỗi nguồn giám sát cho bên sở hữu nó. Server có teacher
  và dữ liệu public; client có verifier tại chỗ là database của mình.
- 1.4 Hai, ba con số chính và danh sách contribution (mục 5).

Nguồn: FL4SP (Zhang et al., ACL 2023), OpenFedLLM, FedLLM-Bench, Liu et al.
(ACL 2025), ExCoT, FedMKT.

### 2. Related Work (khoảng 1,300 từ)

- 2.1 Federated learning cho LLM và Text-to-SQL: FL4SP (T5-base, exact
  match), FederatedScope-LLM, OpenFedLLM, FedLLM-Bench, các biến thể LoRA
  (FLoRA, FedSA-LoRA, FFA-LoRA).
- 2.2 Server LLM giúp client SLM: FedMKT, FedCoLLM, CrossLM, FedBiOT,
  FedAuto, GPT-FL. Điểm khác: teacher của họ được train, dữ liệu public
  cùng phân phối, task QA / phân loại.
- 2.3 LLM-to-SLM distillation: KID, DistiLLM-2 (đúng cặp model 7B / 1.5B),
  GKD, MiniLLM; distillation cho Text-to-SQL (Zhong et al. 2024,
  Struct-SQL).
- 2.4 Federated preference optimization và federated RL với reward kiểm
  chứng được: FedDPO, FedBiscuit, PubSwap, Fed-GRPO, FedMOA.
- 2.5 Train model nhỏ cho Text-to-SQL: SFT (CodeS, OmniSQL), DPO trên cặp
  gán nhãn bằng execution (Liu et al., ExCoT, SENSE), RL
  (Arctic-Text2SQL-R1, Reasoning-SQL, SLM-SQL, SQL-R1), DPO có định vị lỗi
  (Focused-DPO, CAPER, EXPO-SQL, SQLoom).

Khi viết: SQLoom là preprint; nêu số 89.2 của nó và nói rõ nó train tập
trung trên Spider + BIRD với GPT-4 trong vòng lặp.

### 3. Problem Setting (khoảng 500 từ)

- 3.1 Client, server, dữ liệu: 5 client trên Spider train, split non-IID
  theo domain; server có teacher frozen và BIRD train (public, khác domain).
- 3.2 Ràng buộc: client chỉ gửi LoRA update; teacher chỉ chạy ở server trên
  dữ liệu public; test không bao giờ thành dữ liệu train, retrieval hay
  teacher. Privacy là cô lập dữ liệu về cấu trúc, không phải differential
  privacy.
- 3.3 Mục tiêu: execution accuracy của model 1.5B được deploy, greedy
  decoding, output chỉ có SQL.

### 4. Method (khoảng 1,600 từ)

Hình 1: pipeline ba stage; cái gì ở server, cái gì ở client, cái gì đi qua
mạng.

- 4.1 Tổng quan và thứ tự các stage.
- 4.2 Server distillation: Hinton KD từ teacher 7B trên BIRD train, 2 epoch,
  trước các round federated.
- 4.3 Federated SFT: FedAvg trên LoRA, 3 round.
- 4.4 Execution-verified federated DPO: sampling, gán nhãn bằng execution,
  ghép cặp, loss DPO + NLL, aggregation; 3 round. Algorithm 1.
- 4.5 Chi phí: số request sampling, kích thước update mỗi round, GPU-h mỗi
  stage (bảng đầy đủ ở Appendix B). [M5]

### 5. Experimental Setup (khoảng 900 từ)

- 5.1 Dữ liệu và split (Bảng 1: số câu và số database mỗi client, BIRD ở
  server, các set đánh giá). [có]
- 5.2 Evaluation: Spider test EX (2,147 câu) là metric chính. Spider test
  được dùng để chọn cấu hình nên paper không gọi nó là held-out; Spider dev,
  DK, SYN, Realistic không dùng để chọn gì và là phép kiểm tra độc lập với
  lựa chọn; BIRD dev đo domain của dữ liệu server. Greedy decoding, vLLM,
  batch 16, timeout 60 s (Spider) và 30 s (BIRD).
- 5.3 Baselines: base model, local-only, FedAvg, FedProx, FedNTD, SFT tập
  trung Spider, SFT tập trung Spider + BIRD (không privacy), teacher 7B
  zero-shot (mốc tham chiếu). [M3, M4]
- 5.4 Chi tiết train (hyperparameter ở Appendix A).

### 6. Results (khoảng 1,300 từ)

- 6.1 Kết quả chính (Bảng 2): Spider test EX và execution errors, trung
  bình và độ lệch chuẩn trên 3 seed, mọi baseline ở 5.3 và method. [có seed
  0; seed 1 chờ dòng gold; M1, M3, M4]
- 6.2 Các set khác (Bảng 3): Spider dev, DK, SYN, Realistic, BIRD dev. [có
  seed 0, seed 1 một phần; M1]
- 6.3 Đóng góp từng stage (Bảng 4): FedAvg; + DPO; + server distillation; cả
  hai; chênh lệch cặp và khoảng tin cậy 95% gộp seed. [có 2 seed; M1]
- 6.4 Theo round (Hình 2): EX theo round DPO từ ba điểm xuất phát (FedAvg,
  gold, Hinton), dải theo seed; bão hòa ở round 3-4. [có seed 0; chờ; M1]

### 7. Analysis (khoảng 1,700 từ)

- 7.1 Mỗi stage sửa loại lỗi nào (Hình 3): right / execution error / wrong
  result theo từng dòng; `no such column` là loại lỗi chính bị loại bỏ. [có]
- 7.2 Thành phần các cặp qua các round (Hình 4): cặp có rejected là
  execution error 2,806 xuống 858; cặp có rejected là wrong result 2,587
  xuống 2,012; số cặp theo từng client. [có; M5 cho số theo client]
- 7.3 Teacher đóng góp gì (Bảng 5): gold SQL, virtual teacher, logit của
  chính student, teacher 7B ở stage server, trước và sau DPO; phần lead của
  teacher sau DPO nằm ở wrong results trên nhóm extra-hard. [có trước DPO;
  chờ: gold seed 1, DPO từ virtual teacher; M1]
- 7.4 Student so với teacher (Hình 5): EX ngang nhau nhưng đúng trên các
  câu khác nhau, ít nhất một trong hai đúng trên 84%; theo độ khó, teacher
  dẫn ở medium và hard, student dẫn ở extra-hard. [có với dòng teacher HF;
  M4]
- 7.5 Federated, tập trung và local trong stage DPO (Bảng 6, nửa trên):
  cùng recipe trên dữ liệu gộp, và ở từng client không aggregate. [M2]
- 7.6 Ablation của stage DPO (Bảng 6, nửa dưới): không có NLL, chỉ NLL,
  thêm một round SFT, Focused-DPO, số round. [có; chờ `pilot_no_nll`]
- 7.7 Độ nhạy (ngắn, hình ở appendix): mức non-IID, số sample K, beta. [S1,
  S2]

### 8. Discussion (khoảng 600 từ)

Viết dưới dạng các điểm cần cân nhắc.

- 8.1 Vì sao DPO chỉ trên SQL có tác dụng ở 1.5B: model nhỏ sai nhiều hơn
  nên có nhiều cặp hơn; dẫn bằng số cặp.
- 8.2 Trần wrong results: 442 câu sai kết quả, 193 câu trong đó có dòng khác
  làm đúng, và teacher đúng trên 129 câu. Verifier chỉ thấy "sai" chứ không
  thấy sai ở đâu; hướng tiếp là định vị lỗi theo clause và đưa phần teacher
  đúng sang student.
- 8.3 Nhãn dương tính giả: Spider train không có test-suite database nên
  một SQL khớp kết quả vẫn có thể sai; ước lượng tỉ lệ trên một mẫu cặp.
  [M5]
- 8.4 Giới hạn: một benchmark ở client, privacy là cô lập dữ liệu không có
  đảm bảo DP, và (nếu không chạy S1, S3) một split, một backbone.

### 9. Conclusion (khoảng 300 từ)

Câu hỏi, cơ chế, con số chính, giới hạn chính, hướng tiếp.

### Phần cuối bắt buộc

Data availability (code, split, prediction files), Ethics declaration
(không có dữ liệu người), Author contributions (CRediT), Conflict of
interest, Funding, khai báo dùng công cụ AI theo chính sách của venue.

### Appendix

- A. Hyperparameter và prompt.
- B. Chi phí tính toán, bộ nhớ và dung lượng gửi đi mỗi round.
- C. Kết quả từng seed đầy đủ.
- D. Độ nhạy theo K, beta và mức non-IID.
- E. CoT ở 1.5B không giúp (plan + SQL).
- F. Ví dụ cặp preference và các loại lỗi.

## 7. Thực nghiệm

Tất cả thời gian là ước lượng trên một RTX A5000 (GPU 0), tính từ các lần
chạy đã đo: một round FedAvg khoảng 1.65 h, ba round DPO kèm evaluation
khoảng 5.5 h, một epoch Hinton KD trên BIRD khoảng 3.5 h, một epoch gold
khoảng 2.7 h.

### 7.1 Đã có

| Nhóm | Nội dung | Seed |
|---|---|---|
| Mốc tham chiếu | base model, SFT tập trung Spider, SFT tập trung Spider + BIRD | 0 |
| Dòng FedAvg | FedAvg R3, DPO round 1-3 | 0, 1 |
| Dòng Hinton (method) | server distillation, FedAvg R3, DPO round 1-4 | 0, 1 (DPO round 1-3) |
| Dòng gold | server stage gold, FedAvg R3, DPO round 1-3 | 0 |
| Ablation stage DPO | chỉ NLL, thêm một round SFT, Focused-DPO round 1 | 0 |
| Các set khác | Spider dev, DK, SYN, Realistic, BIRD dev cho các dòng trên | 0, 1 (một phần) |
| Control soft target trước DPO | virtual teacher, logit của chính student (engine HF) | 0 |
| Teacher 7B zero-shot | Spider test (engine HF, 4-bit) | 0 |
| Phân tích từ prediction | loại lỗi, chuyển trạng thái giữa các dòng, theo độ khó, teacher so với student | 0, 1 |

### 7.2 Đang chạy và đã queue (xong khoảng 15:50 ngày 11-13)

| Task | Trả lời câu hỏi | Vào đâu trong paper |
|---|---|---|
| Dòng gold seed 1: FedAvg round 2-3, DPO round 1-3, các set khác | Lead của Hinton sau DPO là của teacher hay của dữ liệu BIRD, trên seed thứ hai | Bảng 4, Bảng 5 |
| `pilot_no_nll` (DPO round 1 không có NLL, seed 0) | NLL có cần không | Bảng 6 |
| DPO round 1-3 từ `virtual_k2aaa_a3` (seed 0), kèm các set khác | Lead sau DPO cần teacher 7B hay soft target nào cũng đủ | Bảng 5 |
| Đánh giá lại `self_k2aaa_a3` trên vLLM | Dòng control cùng engine với các dòng khác | Bảng 5 |

### 7.3 Phải chạy thêm

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| M1 | Seed 2 cho ba dòng (FedAvg, gold, Hinton): hai stage server, 3 round FedAvg và 3 round DPO mỗi dòng, các set khác | Mọi dòng chính có trung bình và độ lệch chuẩn trên 3 seed; kết luận về teacher không dựa trên hai lần chạy | Bảng 2, 3, 4, 5, Hình 2 | 45 |
| M2 | Stage DPO cùng recipe trên dữ liệu client gộp (tập trung), và ở từng client không aggregate (local), từ điểm xuất phát Hinton, seed 0 | Setting federated mất hay được gì ở stage chính so với hai cực | Bảng 6 | 11.5 |
| M3 | FedProx, FedNTD và các model local của từng client trên engine vLLM, sáu set, seed 0 | Bảng chính có đủ baseline FL chuẩn trên cùng engine | Bảng 2, 3 | 2 |
| M4 | Teacher 7B zero-shot trên vLLM, sáu set | Dòng teacher cùng engine với student; phân tích 7.4 so từng câu hợp lệ | Bảng 2, 3, Hình 5 | 1 |
| M5 | Tổng hợp không cần GPU: số cặp theo client và round; bảng chi phí (GPU-h, số request sampling, dung lượng update); ước lượng tỉ lệ chosen dương tính giả trên 200 cặp có chosen không phải gold | Ba câu hỏi reviewer chắc chắn đặt ra về một method DPO dùng nhãn execution | Hình 4, Appendix B, mục 8.3 | 0 |

Tổng: khoảng 60 GPU-h.

Ghi chú thực hiện:

- M1: logit cache của teacher trên BIRD dùng lại được vì không phụ thuộc
  seed. Trong 45 h có khoảng 7 h cho stage Hinton, 5.5 h cho stage gold,
  15 h cho 9 round FedAvg, 16.5 h cho ba dòng DPO.
- M2: runner DPO hiện chưa có chế độ tập trung và chế độ không aggregate,
  cần thêm trước khi queue. Dòng local báo cáo trung bình EX của năm model
  client.
- M3: adapter seed 0 của ba baseline là kết quả trước ngày 2026-11-05, cần
  owner cho phép dùng và cần kiểm tra còn trên server. Nếu thiếu, train lại
  mỗi baseline khoảng 5 h.
- M4: teacher 7B chưa từng chạy qua vLLM trên card này, kiểm tra bộ nhớ ở
  batch đầu.
- M5: phần ước lượng dương tính giả cần khoảng 2 giờ đọc tay các chosen
  khác cấu trúc với gold.

### 7.4 Nên chạy để hướng tới Q2

Xếp theo mức tăng độ tin cậy của paper trên mỗi GPU-h.

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| S1 | Split `alpha_0.5/k5` (non-IID nhẹ hơn), seed 0: dòng FedAvg và dòng method; dùng lại stage server | Gain có phụ thuộc vào một mức non-IID không | 7.7, Appendix D | 21 |
| S2 | Độ nhạy của stage DPO: K = 4 và 16, beta = 0.05 và 0.5, chỉ round 1, seed 0 | Method có nhạy với hai hyperparameter chính không | 7.7, Appendix D | 7 |
| S3 | Student thứ hai (Qwen2.5-Coder-0.5B), seed 0: dòng FedAvg và dòng method | Method có giữ được ở một kích thước model khác không; title nói "small language models" | Một bảng ở mục 6 | 15-20 |
| S4 | FedProx seed 1 và 2 | Baseline FL mạnh nhất cũng có 3 seed | Bảng 2 | 10 |

Tổng: khoảng 55 GPU-h.

- S2 chỉ chạy round 1 thay vì 3 round (đủ 3 round sẽ là 22 h); kết quả là
  xu hướng theo hyperparameter, không phải số cuối của method.
- S3 thay đổi phần setup cố định (một student); thời gian chưa đo trên
  0.5B với chuỗi này, và logit cache của teacher cần audit lại cho student
  mới.

### 7.5 Thứ tự

1. Chờ các task ở 7.2 xong (khoảng 15:50 ngày 11-13), đọc dòng gold seed 1
   và dòng virtual teacher.
2. M3 và M4 (3 h): hoàn thiện Bảng 2 cho seed 0, đủ để bắt đầu viết mục 5
   và 6.
3. M1 (45 h): chạy nền trong lúc viết Introduction, Related Work, Setting,
   Method; M5 làm song song vì không cần GPU.
4. M2 (11.5 h).
5. S1, S2, S3, S4 theo thứ tự, nếu còn thời gian trước khi nộp.

## 8. Đối chiếu với chuẩn Q2-Q3

Các điểm mà reviewer ở nhóm venue mục tiêu thường xét với một paper method
về federated learning cho LLM, và trạng thái của paper theo kế hoạch này.

| Điểm reviewer xét | Hiện tại | Sau mục 7.3 | Sau mục 7.4 |
|---|---|---|---|
| Số seed, độ lệch chuẩn, kiểm định cặp | 2 seed, có khoảng tin cậy | 3 seed cho mọi dòng chính | như trước, thêm FedProx 3 seed |
| Baseline FL chuẩn trên cùng engine | chỉ FedAvg | FedAvg, FedProx, FedNTD, local | như trước |
| Mốc tập trung của chính method | chỉ có SFT tập trung | có DPO tập trung và local | như trước |
| Control tách "thêm dữ liệu ở server" khỏi "tín hiệu teacher" | seed 0, sát ngưỡng | gold và Hinton trên 3 seed, virtual teacher seed 0 | như trước |
| Mỗi thành phần có vai trò được chỉ ra | DPO rõ; teacher +1.4 gộp 2 seed | cả hai trên 3 seed, kèm loại lỗi mỗi stage sửa | như trước |
| Kết quả ngoài set dùng để chọn | 4 set trên database dev, không chọn gì trên đó | như trước, 3 seed | như trước |
| Hơn một mức non-IID | một split | một split (ghi ở giới hạn) | hai split |
| Hơn một backbone | một student | một student (ghi ở giới hạn) | hai student |
| Hơn một benchmark ở client | chỉ Spider | chỉ Spider (ghi ở giới hạn) | chỉ Spider |
| Chi phí và communication | chưa tổng hợp | có bảng | như trước |
| So với số đã công bố ở cùng cỡ model | chưa có bảng | bảng ngữ cảnh ghi rõ greedy hay self-consistency, tập trung hay federated | như trước |
| Privacy | cô lập dữ liệu, không DP | nói rõ một câu ở 3.2 và 8.4 | như trước |

Điểm cần cân nhắc:

- Phần chắc nhất của paper là stage DPO (+3.2 đến +3.9 từ mọi điểm xuất
  phát); phần teacher nhỏ hơn (+1.4) và cần 3 seed cùng Bảng 5 để đứng vững
  như một contribution.
- EX tuyệt đối 77 thấp hơn các số Spider test cao nhất đã công bố; paper so
  trong setting của mình (1.5B, greedy, federated, không model ngoài thấy dữ
  liệu client) và nêu rõ khác biệt setting với SQLoom.
- Một benchmark ở client là giới hạn không gỡ được trong kế hoạch này;
  DK, SYN, Realistic cho thấy độ bền với cách hỏi khác, không thay được một
  domain client khác.

## 9. Nếu giả định không đúng

| Kết quả | Thay đổi |
|---|---|
| Dòng gold seed 1 ngang dòng Hinton sau DPO | M1 thành điều kiện để giữ teacher; nếu sau 3 seed vẫn không tách được thì stage server rời method và thành một ablation, title đổi sang "Private Databases as Verifiers: Federated Preference Optimization for Small Text-to-SQL Models" |
| Dòng virtual teacher ngang dòng Hinton sau DPO | Method nói "soft target ở server", teacher 7B là một lựa chọn; contribution 3 viết lại theo hướng đó, title như dòng trên |
| `pilot_no_nll` cho thấy NLL không cần | Một dòng ở Bảng 6 và một câu ở 4.4; method giữ nguyên |
