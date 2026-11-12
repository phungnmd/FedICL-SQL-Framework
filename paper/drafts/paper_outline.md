# FedLS-SQL: tên và outline paper

Bản nháp 2026-11-13. Số liệu lấy từ `paper/notes/RESEARCH_STATE.md` (mục 4)
và `LAB_LOG.md`; nguồn tham khảo lấy từ `paper/notes/LITERATURE.md`.

## 1. Cấu hình paper

| Mục | Giá trị |
|---|---|
| Loại paper | Empirical method paper, cấu trúc IMRaD mở rộng cho ML (Setting, Method, Experiments, Analysis) |
| Lĩnh vực | Federated learning, Text-to-SQL, LLM-to-SLM |
| Venue | Data & Knowledge Engineering, Int. J. Data Science and Analytics, Neural Processing Letters, Distributed and Parallel Databases; stretch: J. Intelligent Information Systems |
| Ngôn ngữ | Tiếng Anh |
| Độ dài | khoảng 9,000 từ phần chính (không tính references, appendix), 6 bảng, 4-5 hình |
| Citation | dạng số theo template của venue (Elsevier / Springer), chốt khi chọn venue |
| Output | LaTeX theo template venue, khi bắt đầu viết |

## 2. Câu chuyện của paper trong một đoạn

Năm client giữ dữ liệu Text-to-SQL riêng và cùng train một model 1.5B; chỉ
model 1.5B được deploy. Mỗi client có sẵn một verifier: chạy SQL trên
database của chính nó là biết đúng hay sai. Paper dùng verifier đó để mỗi
client tự tạo cặp preference (SQL đúng / SQL sai do chính model sinh ra) và
train DPO + NLL, server chỉ average update. Trên Spider test, method cao hơn
FedAvg 5.3 điểm (hai seed gộp), cao hơn cả SFT tập trung trên Spider + BIRD
(không có privacy). Gain đến từ việc model hết viết SQL không chạy được
(execution errors 211 xuống 58); khoảng 20% câu trả lời chạy được nhưng sai
kết quả thì không stage nào sửa được, và đó là trần của method. Stage server
với teacher 7B (Hinton KD trên BIRD) giữ thêm khoảng 1.4 điểm sau DPO; vai
trò của nó đang chờ hai control (mục 6).

## 3. Đề xuất tên

### 3.1 Title

| # | Title | Số từ | Dùng khi |
|---|---|---:|---|
| A | **Private Databases as Verifiers: Federated Preference Optimization for Small Text-to-SQL Models** | 12 | Đề xuất chính. Nói đúng cơ chế cốt lõi (database của client gán nhãn cặp, không dữ liệu nào rời client), không phụ thuộc vào quyết định về teacher |
| B | Execution-Verified Federated Preference Optimization for Small Text-to-SQL Models | 9 | Bản mô tả an toàn, dễ tìm kiếm nhất, nhưng nhạt hơn A |
| C | Distill at the Server, Verify at the Client: Federated Text-to-SQL for Small Language Models | 15 | Chỉ khi teacher ở lại trong method (control ở mục 6 cho thấy lead sau DPO cần teacher 7B) |
| D | Federated Text-to-SQL with Execution-Labelled Preference Pairs for a Deployed Small Model | 12 | Nếu venue thích title nói rõ setting deploy model nhỏ |

Lý do đề xuất A: phần chắc nhất của kết quả là DPO stage (+3.2 đến +3.9 từ
mọi điểm xuất phát, cả hai seed), còn phần teacher chưa chốt. Title nên đặt
khái niệm chính lên đầu và không hứa điều chưa có số. Nếu teacher ở lại,
chuyển sang C (hai nửa title khớp với hai stage của method).

### 3.2 Tên method

Working title `FedLS-SQL` gợi ý hướng LLM-to-SLM (teacher sang student),
trong khi theo số hiện tại DPO ở client mới là phần chính. Hai lựa chọn:

- Giữ `FedLS-SQL` nếu teacher ở lại, và giải nghĩa rõ trong paper.
- Đổi sang tên theo cơ chế verifier nếu teacher bị bỏ, ví dụ `FedVeri-SQL`
  hoặc `ExecFed-DPO`. Chưa kiểm tra trùng tên; cần search trước khi chốt
  (`EXPO-SQL` đã tồn tại, Lee et al. 2026, nên tránh các tên gần nó).

### 3.3 Keywords

Federated learning; Text-to-SQL; direct preference optimization; execution
feedback; small language models; knowledge distillation (chỉ khi teacher ở
lại).

## 4. Contributions (dự kiến, ở cuối Introduction)

1. Setting: federated Text-to-SQL với một decoder SLM được deploy một mình,
   đo bằng execution accuracy, dữ liệu client không rời client và teacher
   (nếu có) chỉ chạy ở server trên dữ liệu public khác domain.
2. Method: mỗi round, client sample 8 SQL cho mỗi câu hỏi từ model hiện tại,
   gán nhãn bằng execution trên database của mình, ghép cặp đúng / sai (gold
   SQL làm chosen khi không sample nào đúng), train DPO + NLL; server làm
   FedAvg trên LoRA.
3. Kết quả: Spider test 76.71 / 77.04 (seed 0 / 1) so với FedAvg 71.26 /
   71.87; gain giữ trên Spider dev, DK, SYN, Realistic (các set không dùng để
   chọn gì).
4. Phân tích: gain đến từ execution errors, tập cặp có rejected là execution
   error co lại qua các round, method bão hòa ở round 3-4, và trần khoảng 20%
   wrong results. Ở 1.5B, DPO chỉ trên SQL có gain rõ, khác với báo cáo ở
   6.7B trở lên (Liu et al. 2025; ExCoT); paper giải thích bằng số cặp.
5. (Nếu teacher ở lại) Stage server: Hinton KD từ teacher 7B trên BIRD trước
   các round federated, với control cùng câu hỏi BIRD nhưng dùng gold SQL và
   control soft target không cần teacher.

Không dùng "first". Mỗi contribution có câu nêu work gần nhất và điểm khác.

## 5. Outline chi tiết

Ký hiệu: [có] số đã có và committed; [chờ] đang chạy hoặc đã queue; [thiếu]
chưa chạy, chưa queue.

### 1. Introduction (khoảng 1,100 từ)

Mục đích: đưa người đọc từ bài toán thực tế đến contribution, theo ba bước
CARS (bối cảnh, khoảng trống, đóng góp).

- 1.1 Bối cảnh: nhiều tổ chức có database và câu hỏi riêng, không gửi được
  ra ngoài; model nhỏ rẻ để deploy; FL là cách train chung.
- 1.2 Vấn đề: FedAvg SFT đã gần bằng SFT tập trung, nên các method sửa
  client drift (FedProx, SCAFFOLD, aggregation mới) có ít chỗ để thắng. Phải
  đổi cái model học, không phải cách gộp.
- 1.3 Ý chính: Text-to-SQL có verifier tại chỗ. Mỗi client dùng database của
  mình để gán nhãn SQL do model sinh ra, không cần nhãn người, không gửi dữ
  liệu.
- 1.4 Tóm tắt kết quả chính (2-3 con số) và danh sách contribution (mục 4).

Nguồn: FL4SP (Zhang et al. ACL 2023), OpenFedLLM, FedLLM-Bench, Liu et al.
ACL 2025, ExCoT.
Chuyển sang mục 2: mỗi ý trong 1.3 có một nhóm work gần, mục 2 nói rõ khác
ở đâu.

### 2. Related Work (khoảng 1,300 từ)

- 2.1 Federated learning cho LLM và Text-to-SQL: FL4SP (T5-base, exact
  match, là federated Text-to-SQL duy nhất trước đây), FederatedScope-LLM,
  OpenFedLLM, FedLLM-Bench, các biến thể LoRA (FLoRA, FedSA-LoRA, FFA-LoRA).
- 2.2 Server LLM giúp client SLM: FedMKT, FedCoLLM, CrossLM, FedBiOT,
  FedAuto, GPT-FL. Điểm khác: teacher của họ được train, dữ liệu public cùng
  phân phối, task QA / phân loại, và không có control "cùng dữ liệu server,
  gold label".
- 2.3 Federated preference optimization và federated RL với reward kiểm
  chứng được: FedDPO trong OpenFedLLM, FedBiscuit (preference của người),
  PubSwap, Fed-GRPO, FedMOA (toán, code). Điểm khác: cặp được tạo và gán
  nhãn bằng execution ngay tại client, cho Text-to-SQL.
- 2.4 Train model nhỏ cho Text-to-SQL: SFT (CodeS, OmniSQL), DPO trên cặp
  gán nhãn bằng execution (Liu et al., ExCoT, SENSE), RL (Arctic-Text2SQL-R1,
  Reasoning-SQL, Think2SQL, SLM-SQL, SQL-R1), và DPO có định vị lỗi
  (Focused-DPO, CAPER, EXPO-SQL, SQLoom).
- 2.5 LLM-to-SLM distillation (chỉ giữ nếu teacher ở lại; nếu không, gộp
  thành một đoạn trong 2.2): KID, DistiLLM-2 (đúng cặp model 7B / 1.5B),
  GKD, MiniLLM.

Lưu ý khi viết: SQLoom là preprint chưa peer-review; nêu số 89.2 của nó và
nói rõ nó train tập trung trên Spider + BIRD với GPT-4 trong vòng lặp.

### 3. Problem Setting (khoảng 600 từ)

- 3.1 Client, server, dữ liệu: 5 client trên Spider train, split non-IID
  theo domain (`alpha_0.1/k5`); server có thể có teacher frozen và BIRD train
  (public, khác domain).
- 3.2 Ràng buộc: dữ liệu client không rời client; client chỉ gửi LoRA
  update; teacher chỉ chạy ở server trên dữ liệu public; test không bao giờ
  thành dữ liệu train, retrieval hay teacher. Privacy ở đây là cô lập dữ liệu
  về cấu trúc, không phải differential privacy (nói rõ một câu).
- 3.3 Mục tiêu: execution accuracy của model 1.5B được deploy, greedy
  decoding, output chỉ có SQL.

### 4. Method (khoảng 1,500 từ)

Hình 1: pipeline ba stage, chỉ rõ cái gì ở server, cái gì ở client, cái gì
đi qua mạng.

- 4.1 Tổng quan và thứ tự các stage.
- 4.2 Federated SFT (FedAvg trên LoRA, 3 round).
- 4.3 Federated DPO với cặp gán nhãn bằng execution (phần chính):
  - sample 8 SQL mỗi câu từ model hiện tại;
  - gán nhãn: so kết quả chạy với kết quả của gold SQL trên database của
    client;
  - ghép cặp: một sample đúng với một sample sai; gold làm chosen khi không
    sample nào đúng;
  - loss DPO + NLL trên chosen; server làm FedAvg; 3 round.
- 4.4 Stage server (tùy kết quả mục 6): Hinton KD từ teacher 7B trên BIRD
  train, 2 epoch, trước các round federated. Nếu teacher bị bỏ, mục này
  chuyển thành một ablation trong mục 7.
- 4.5 Chi phí: số lần forward cho sampling, kích thước update gửi đi mỗi
  round, GPU-h mỗi round [thiếu: bảng chi phí tổng hợp, lấy từ log].

### 5. Experimental Setup (khoảng 900 từ)

- 5.1 Dữ liệu và split (Bảng 1: số câu, số database mỗi client).
- 5.2 Evaluation: Spider test EX (2,147 câu) là metric chính; Spider test
  được dùng để chọn cấu hình, nên paper không gọi nó là held-out. Spider dev,
  DK, SYN, Realistic (không dùng để chọn gì) và BIRD dev là các set kiểm tra
  thêm. Engine vLLM, batch 16, timeout 60 s (Spider), 30 s (BIRD). Khoảng tin
  cậy bằng bootstrap theo database; gộp hai seed thì cluster theo câu hỏi.
- 5.3 Baselines: base model, FedAvg, FedProx [thiếu số vLLM], FedNTD
  [thiếu số vLLM], local-only client models [thiếu số vLLM], SFT tập trung
  Spider, SFT tập trung Spider + BIRD (không privacy, mốc trên), teacher 7B
  zero-shot (mốc tham chiếu).
- 5.4 Chi tiết train (bảng hyperparameter đưa vào Appendix A).

### 6. Results (khoảng 1,400 từ)

- 6.1 Kết quả chính (Bảng 2): các dòng như bảng mục 4 của
  `RESEARCH_STATE.md`, hai seed, EX và execution errors. [có seed 0 đủ;
  seed 1 thiếu dòng gold: chờ]
- 6.2 Đóng góp từng phần (Bảng 3): whole method, DPO stage, DPO không có
  server stage, preference term so với SFT control tốt nhất, so với tập
  trung không privacy; khoảng tin cậy 95%. [có]
- 6.3 Các set khác (Bảng 4): Spider dev, DK, SYN, Realistic, BIRD dev. [có
  seed 0; seed 1 một phần]
- 6.4 Theo round (Hình 2): EX theo round DPO cho ba điểm xuất phát (FedAvg,
  gold, Hinton), cho thấy bão hòa ở round 3-4. [có seed 0; seed 1 chờ]

### 7. Analysis (khoảng 1,400 từ)

- 7.1 Gain đến từ đâu (Hình 3): right / execution error / wrong result theo
  từng dòng; `no such column` là loại lỗi chính bị loại bỏ. [có]
- 7.2 Thành phần các cặp qua các round (Hình 4): cặp có rejected là
  execution error 2,806 xuống 858; cặp có rejected là wrong result 2,587
  xuống 2,012; số câu có cả 8 sample đúng. [có; thiếu: số cặp theo từng
  client, reviewer sẽ hỏi]
- 7.3 Ablation (Bảng 5): không có NLL [chờ: `pilot_no_nll`], chỉ NLL, thêm
  một round SFT, Focused-DPO (`fdpo`), số round. [có trừ no-NLL]
- 7.4 Vai trò của stage server và teacher (Bảng 6): Hinton so với gold so
  với soft target không teacher (`virtual`), trước và sau DPO. [chờ: dòng
  gold seed 1, DPO từ `virtual_k2aaa_a3`]
- 7.5 So với teacher 7B: EX gần bằng (76.7 và 77.0 so với 77.2) nhưng đúng trên các
  câu khác nhau; ít nhất một trong hai đúng trên 84%. Ghi chú: dòng teacher
  là HF 4-bit, các dòng method là vLLM.
- 7.6 Federated so với tập trung trong DPO stage: DPO cùng recipe trên dữ
  liệu gộp, và DPO ở từng client không aggregate. [thiếu, chưa queue; khoảng
  5.5-6 GPU-h mỗi dòng, ước lượng]
- 7.7 (Ngắn hoặc đưa vào Appendix) CoT ở 1.5B không giúp.

### 8. Discussion (khoảng 700 từ)

Viết dưới dạng các điểm cần cân nhắc.

- 8.1 Vì sao DPO chỉ trên SQL có tác dụng ở 1.5B mà không ở 7B trở lên:
  model nhỏ sai nhiều hơn, nên có nhiều cặp hơn; dẫn bằng số cặp.
- 8.2 Trần wrong results: 442 câu sai kết quả, 193 câu trong đó có dòng khác
  làm đúng; verifier chỉ thấy "sai" chứ không thấy sai ở đâu. Hướng tiếp:
  định vị lỗi theo clause.
- 8.3 Nhãn dương tính giả: Spider train không có test-suite database, nên
  một SQL khớp kết quả vẫn có thể sai [thiếu: ước lượng tỉ lệ trên một mẫu
  cặp].
- 8.4 Giới hạn: một backbone, một split, hai seed, một benchmark client;
  privacy là cô lập dữ liệu, không có đảm bảo DP.

### 9. Conclusion (khoảng 300 từ)

Một đoạn: câu hỏi, cơ chế, con số chính, giới hạn chính, hướng tiếp.

### Phần cuối bắt buộc

Data availability (code, split, prediction files), Ethics declaration
(không có dữ liệu người), Author contributions (CRediT), Conflict of
interest, Funding, khai báo dùng công cụ AI theo chính sách của venue.

### Appendix

- A. Hyperparameter và prompt.
- B. Chi phí tính toán và bộ nhớ (A5000, LoRA, vLLM).
- C. Kết quả từng seed đầy đủ, từng client.
- D. Phân tích CoT (nếu không để trong mục 7).
- E. Ví dụ cặp preference (đúng / sai) và các loại lỗi.

## 6. Phần outline phụ thuộc vào kết quả đang chạy

| Kết quả đang chờ | Nếu ra thế này | Thay đổi trong paper |
|---|---|---|
| Dòng gold seed 1 + DPO từ `virtual_k2aaa_a3` | Lead sau DPO cần teacher 7B (virtual gần gold) | Teacher ở lại: title C, mục 4.4 là một stage của method, mục 2.5 giữ riêng |
| | Soft target nào cũng đủ (virtual gần Hinton) | Method nói "soft target ở server", teacher là một lựa chọn; title A |
| | Không còn lead tách được sau hai seed | Bỏ stage server khỏi method; mục 4.4 thành ablation trong 7.4; title A hoặc B |
| `pilot_no_nll` | NLL cần thiết hoặc không | Một dòng trong Bảng 5 và một câu ở 4.3 |

## 7. Bằng chứng còn thiếu mà reviewer sẽ hỏi

Theo `LITERATURE.md` mục 4, sắp theo mức chắc chắn bị hỏi:

1. Số cặp theo từng client và từng round (có trong log train, chỉ cần tổng
   hợp).
2. DPO cùng recipe trên dữ liệu gộp (tập trung) và DPO local không aggregate
   (mục 7.6).
3. FedProx, FedNTD, local models trên engine vLLM (mục 5.3).
4. Ước lượng tỉ lệ chosen dương tính giả (mục 8.3).
5. Bảng chi phí: GPU-h và dung lượng gửi đi mỗi round (mục 4.5).
