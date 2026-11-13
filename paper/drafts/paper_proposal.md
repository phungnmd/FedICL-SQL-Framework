# Đề xuất paper FedLS-SQL: tên, outline và thực nghiệm

Ngày 2026-11-14, theo các kết quả đã committed đến 01:19 cùng ngày. Số liệu
lấy từ `paper/notes/RESEARCH_STATE.md` (mục 4) và `LAB_LOG.md`; nguồn tham
khảo lấy từ `paper/notes/LITERATURE.md`.

Stage DPO ở client cho phần lớn gain, stage distillation ở server cho phần
nhỏ hơn; title giữ cả hai. Nửa server của title phụ thuộc kết quả seed 2
(mục 9). Các thực nghiệm đề xuất thêm ở mục 7.3 và 7.4 chờ owner quyết.

## 1. Tóm tắt

| Mục | Đề xuất |
|---|---|
| Title | **Distill at the Server, Verify at the Client: Federated Text-to-SQL for Small Language Models** |
| Tên method | FedLS-SQL (Federated LLM-to-SLM for Text-to-SQL) |
| Loại paper | Empirical method paper, cấu trúc IMRaD mở rộng cho ML |
| Venue | Data & Knowledge Engineering, Int. J. Data Science and Analytics, Neural Processing Letters, Distributed and Parallel Databases; stretch: J. Intelligent Information Systems. Quartile và độ hợp: mục 8.1 |
| Kết quả chính (Spider test EX) | Method 76.71 / 77.04 (seed 0 / 1), FedAvg 71.26 / 71.87, SFT tập trung Spider + BIRD 73.96, teacher 7B zero-shot 77.22. Với vote theo execution trên 8 sample (seed 0): method 78.39, FedAvg 75.55 |
| Đang queue | khoảng 58 GPU-h trên một A5000 (mục 7.2), tức khoảng 2.5 ngày chạy liên tục |
| Đề xuất chạy thêm | khoảng 4.5 GPU-h (mục 7.3) |
| Đề xuất chạy thêm nếu nhắm Q2 | khoảng 57 đến 62 GPU-h nữa (mục 7.4) |

## 2. Câu chuyện của paper

Năm tổ chức giữ dữ liệu Text-to-SQL riêng và cùng train một model 1.5B; chỉ
model này được deploy. Trên setup này FedAvg SFT đã ngang SFT tập trung
(71.26 so với 70.75 trên Spider test), nên cách gộp update không còn chỗ để
cải thiện. Thứ còn thiếu là tín hiệu train: sau SFT, khoảng 10% câu SQL model
viết ra không chạy được (211 trên 2,147), phần lớn vì gọi cột không có trong
schema (`no such column`, 177 câu).

Mỗi client có sẵn một verifier không tốn nhãn: database của chính mình. Mỗi
round, client sample 8 câu SQL cho mỗi câu hỏi từ model hiện tại, chạy chúng
trên database của mình, ghép một câu đúng với một câu sai và train DPO + NLL;
server chỉ average LoRA update. Không dữ liệu nào rời client.

Ba round như vậy cho +2.5 đến +3.9 điểm từ cả ba điểm xuất phát đã thử, trên
hai seed. Thêm round SFT hoặc chỉ dùng NLL với cùng compute không cho gain
này (+0.84 và +0.19). Execution errors giảm từ 211 xuống 58. Các báo cáo ở
7B trở lên thấy DPO chỉ trên SQL không có gain vì quá ít cặp (Liu et al.:
0.1 đến 0.3 nghìn cặp trên Spider train); model 1.5B sai nhiều hơn nên có
5,393 cặp từ 8,659 câu hỏi ở round 1.

Database cũng dùng được lúc inference, không cần train: sample 8 câu SQL,
chạy chúng và lấy kết quả xuất hiện nhiều nhất. Bước vote này đưa FedAvg từ
71.26 lên 75.55 (seed 0). Stage DPO không thay được bằng bước đó: với cùng 8
sample và cùng cách vote, method vẫn cao hơn FedAvg 2.84 điểm, và stage DPO
thêm 1.2 đến 1.9 điểm. Hai cách sửa các câu khác nhau (chỉ 55% số câu DPO
sửa được là câu vote đã đúng từ trước) nên cộng được: method với vote đạt
78.39, cao hơn greedy của chính nó 1.68. Số câu có ít nhất một sample đúng
trong 8 gần như không đổi qua DPO (83.5% đến 85.0%): DPO đưa câu đúng lên
đầu chứ không tạo thêm câu đúng.

Server có một nguồn mà client không có: dữ liệu public khác domain (BIRD) và
một teacher 7B. Trước các round federated, server distill teacher vào
student trên BIRD. Stage này cho thêm 1.4 điểm sau DPO trên Spider test, 3.5
trên Spider dev, 4.1 trên DK, và giữ 11.4 điểm trên BIRD dev. Control "cùng
câu hỏi BIRD, gold SQL thay teacher" tách hai phần của nó. Trên Spider test,
stage với gold SQL không còn lead sau DPO (+0.42, không tách được); teacher
cho thêm +0.98 (gộp hai seed, sát ngưỡng; +1.49 ở seed 0, +0.47 ở seed 1).
Phần giữ trên BIRD dev đến từ dữ liệu, có hay không có teacher. Các paper
server LLM cho FL (FedMKT, FedCoLLM) không có control này.

Cả pipeline cao hơn FedAvg 5.3 điểm trên Spider test (hai seed gộp), cao hơn
SFT tập trung trên Spider + BIRD (không có privacy) 2.75 điểm, và ngang
teacher 7B zero-shot dù nhỏ hơn gần 5 lần.

Giới hạn được nói thẳng: verifier sửa câu không chạy được, không sửa câu
chạy được nhưng sai kết quả. Khoảng 20% Spider test (khoảng 440 câu) thuộc
loại này ở mọi dòng, từ base model đến DPO round 4. Trong 442 câu loại này
của method, 288 câu không có sample đúng nào trong 8, nên chọn giữa các
sample cũng không với tới.

## 3. Tên

### 3.1 Title

**Distill at the Server, Verify at the Client: Federated Text-to-SQL for
Small Language Models** (14 từ).

Hai vế trước dấu hai chấm là hai stage của method và cũng là hai nửa của
Hình 1; vế sau mang các từ khóa tìm kiếm (federated, Text-to-SQL, small
language models). Abstract nói rõ tỉ trọng: stage ở client cho phần lớn gain
(+2.5 đến +3.9), stage ở server cho thêm khoảng 1.4.

Bản dự phòng cho venue thích title mô tả, có tên method:

- FedLS-SQL: Server-Side Distillation and Client-Side Execution-Verified
  Preference Optimization for Federated Text-to-SQL.

Bản dùng khi sau seed 2 phần teacher không tách được khỏi gold SQL (mục 9):

- FedLS-SQL: Execution-Guided Federated Preference Optimization for Small
  Text-to-SQL Models.

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
   mình, ghép cặp đúng / sai và train bằng preference; server làm FedAvg
   trên LoRA. Ở 1.5B stage này cho +2.5 đến +3.9 điểm từ ba điểm xuất phát,
   trong khi SFT và NLL cùng compute thì không. Phần cần là preference term
   trên nhãn execution: NLL term, gold fallback và cách ghép cặp không có
   vai trò đo được (mục 7.7 của outline). Work gần nhất: FedDPO trong
   OpenFedLLM và FedBiscuit (preference của người), Liu et al. 2025 và
   ExCoT (DPO tập trung, 7B trở lên, DPO chỉ trên SQL không có gain),
   Iterative RPO (DPO + NLL, gold làm chosen).
3. Server distillation có control: Hinton KD từ teacher 7B trên BIRD trước
   các round federated, so với ba loại target khác trên cùng câu hỏi (gold
   SQL, soft target không teacher, logit của chính student), đo trước và
   sau DPO. Kết quả: stage cho thêm 1.4 điểm sau DPO trên Spider test; với
   gold SQL thay teacher phần này không tách được (+0.42), teacher thêm
   +0.98. Work gần nhất: FedMKT, FedCoLLM, CrossLM (không có control "cùng
   dữ liệu server, gold label").
4. Kết quả: cao hơn FedAvg 5.3 điểm trên Spider test, gain giữ trên Spider
   dev, DK, SYN, Realistic (các set không dùng để chọn gì), cao hơn SFT tập
   trung không privacy, ngang teacher 7B zero-shot.
5. Phân tích: verifier sửa loại lỗi nào và không sửa loại nào; verify lúc
   train và verify lúc inference sửa các câu khác nhau và cộng được (method
   với vote 78.39, cao hơn FedAvg với vote 2.84 điểm); stage DPO trong
   setting federated so với tập trung và local; thành phần các cặp co lại
   thế nào qua các round; và trần khoảng 20% câu chạy được nhưng sai kết
   quả.

Không dùng "first".

## 6. Outline

Ký hiệu: [có] số đã có và committed; [queue] đã queue (mục 7.2); [M1] đến
[M5], [N2], [N3], [S1] đến [S4], [F1], [P1] là các thực nghiệm ở mục 7.

### 1. Introduction (khoảng 1,000 từ)

- 1.1 Bối cảnh: nhiều tổ chức có database và câu hỏi riêng, không gửi được
  ra ngoài; model nhỏ rẻ để deploy; FL là cách train chung.
- 1.2 Vấn đề: FedAvg SFT đã ngang SFT tập trung, nên các method sửa client
  drift (FedProx, FedNTD, aggregation mới) có ít chỗ để thắng. Thứ giới hạn
  model là tín hiệu train: 10% output không chạy được sau SFT.
- 1.3 Ý chính: database của client là một verifier có sẵn. Client tự gán
  nhãn sample của model bằng execution và train bằng preference; server góp
  thứ chỉ nó có, dữ liệu public và teacher, trong một stage distillation
  trước các round federated.
- 1.4 Hai, ba con số chính và danh sách contribution (mục 5).

Nguồn: FL4SP (Zhang et al., ACL 2023), OpenFedLLM, FedLLM-Bench, Liu et al.
(ACL 2025), ExCoT, FedMKT.

### 2. Related Work (khoảng 1,300 từ)

- 2.1 Federated learning cho LLM và Text-to-SQL: FL4SP (T5-base, exact
  match), FederatedScope-LLM, OpenFedLLM, FedLLM-Bench, các biến thể LoRA
  (FLoRA, FedSA-LoRA, FFA-LoRA).
- 2.2 Federated preference optimization và federated RL với reward kiểm
  chứng được: FedDPO, FedBiscuit, PubSwap, Fed-GRPO, FedMOA.
- 2.3 Train model nhỏ cho Text-to-SQL: SFT (CodeS, OmniSQL), DPO trên cặp
  gán nhãn bằng execution (Liu et al., ExCoT, SENSE), RL
  (Arctic-Text2SQL-R1, Reasoning-SQL, SLM-SQL, SQL-R1), DPO có định vị lỗi
  (Focused-DPO, CAPER, EXPO-SQL, SQLoom).
- 2.4 Server LLM giúp client SLM: FedMKT, FedCoLLM, CrossLM, FedBiOT,
  FedAuto, GPT-FL. Điểm khác: teacher của họ được train, dữ liệu public
  cùng phân phối, task QA / phân loại, không có control gold label.
- 2.5 LLM-to-SLM distillation: KID, DistiLLM-2 (đúng cặp model 7B / 1.5B),
  GKD, MiniLLM; distillation cho Text-to-SQL (Zhong et al. 2024,
  Struct-SQL).

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
mạng. Vòng lặp sample, execute, ghép cặp, train ở client là phần trung tâm
của hình.

- 4.1 Tổng quan và thứ tự các stage.
- 4.2 Server distillation: Hinton KD từ teacher 7B trên BIRD train, 2 epoch,
  trước các round federated.
- 4.3 Federated SFT: FedAvg trên LoRA, 3 round.
- 4.4 Execution-verified federated DPO: sampling, gán nhãn bằng execution,
  ghép cặp, loss DPO + NLL, aggregation; 3 round. Algorithm 1.
- 4.5 Chi phí: số request sampling, kích thước update mỗi round, GPU-h và
  bộ nhớ mỗi stage ở client và ở server (bảng đầy đủ ở Appendix B). [M5]

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
  zero-shot (mốc tham chiếu), FedAvg với chọn câu theo execution lúc
  inference. [có: chọn theo execution, seed 0; M3, M4]
- 5.4 Chi tiết train (hyperparameter ở Appendix A).

### 6. Results (khoảng 1,300 từ)

- 6.1 Kết quả chính (Bảng 2): Spider test EX và execution errors, trung
  bình và độ lệch chuẩn trên 3 seed, mọi baseline ở 5.3 và method. [có seed
  0 và 1; M1, M3, M4]
- 6.2 Các set khác (Bảng 3): Spider dev, DK, SYN, Realistic, BIRD dev. [có
  seed 0 và 1; M1]
- 6.3 Đóng góp từng stage (Bảng 4): FedAvg, thêm DPO, thêm stage server với
  gold SQL, thêm stage server với teacher; chênh lệch cặp và khoảng tin cậy
  95% gộp seed. [có 2 seed; M1]
- 6.4 Theo round (Hình 2): EX theo round DPO từ ba điểm xuất phát (FedAvg,
  gold, Hinton), dải theo seed; bão hòa ở round 3-4. [có 2 seed; M1]

### 7. Analysis (khoảng 1,700 từ)

- 7.1 Verifier sửa loại lỗi nào (Hình 3): right / execution error / wrong
  result theo từng dòng; `no such column` là loại lỗi chính bị loại bỏ;
  wrong results đứng yên ở 406 đến 464 trong mọi dòng. [có]
- 7.2 Thành phần các cặp qua các round (Hình 4): cặp có rejected là
  execution error 2,806 xuống 858; cặp có rejected là wrong result 2,587
  xuống 2,012; số cặp theo từng client. [có; M5 cho số theo client]
- 7.3 Verify lúc train so với verify lúc inference (Bảng 5): FedAvg R3,
  điểm xuất phát Hinton, DPO round 3 từ mỗi dòng; mỗi dòng với greedy, với
  fallback (giữ câu greedy nếu chạy được), với vote trên 8 sample, pass@8 và
  số lần gọi model cho mỗi câu hỏi. Vote trên điểm xuất phát ngang greedy
  sau DPO về tổng (76.53 so với 76.71) nhưng khác câu (lệch 150 câu). Với
  cùng vote, stage DPO thêm 1.86 (Hinton) và 1.21 (FedAvg), method hơn
  FedAvg 2.84; vote thêm 1.68 trên method. pass@8 gần như đứng yên. [có,
  seed 0; N3 cho seed 1]
- 7.4 Stage server cho gì: dữ liệu hay teacher (Bảng 6): gold SQL, virtual
  teacher, logit của chính student, teacher 7B, trước và sau DPO, trên sáu
  set. Trước DPO bốn target ngang nhau trên Spider test. Sau DPO dòng gold
  và dòng virtual teacher ngang nhau và không tách được khỏi dòng không có
  stage server; dòng teacher cao hơn khoảng 1 điểm trên Spider test, rõ hơn
  trên Spider dev và DK ở seed 0, gần 0 ở seed 1. Phần giữ trên BIRD dev
  (khoảng 11.7 điểm) đến từ dữ liệu. [có: gold 2 seed, virtual và self seed
  0; M1]
- 7.5 Student so với teacher (Hình 5): EX ngang nhau nhưng đúng trên các
  câu khác nhau, ít nhất một trong hai đúng trên 84%; teacher dẫn ở medium
  và hard, student dẫn ở extra-hard. [có với dòng teacher HF; M4]
- 7.6 Federated, tập trung và local trong stage DPO (Bảng 7, nửa trên):
  cùng recipe trên dữ liệu gộp, và các adapter client trước khi aggregate.
  [queue]
- 7.7 Ablation của stage DPO (Bảng 7, nửa dưới): chỉ NLL (+0.19), thêm
  round SFT (+0.84), không có NLL qua 3 round (76.76 so với 76.71), ghép
  cặp ngẫu nhiên (75.73 so với 75.69), Focused-DPO, không có gold fallback
  (75.50 so với 75.69), số round [có]; các round dùng lại sample của round
  1 [queue]; nhãn bằng vote thay nhãn gold, và chỉ cặp chạy được / không
  chạy được [N2].
- 7.8 Độ nhạy (ngắn, hình ở appendix): mức non-IID, số client và tỉ lệ tham
  gia, kích thước student, schema có value và foreign key trong prompt, số
  sample K, beta. [S1, F1, S3, P1, S2]

### 8. Discussion (khoảng 600 từ)

Viết dưới dạng các điểm cần cân nhắc.

- 8.1 Vì sao DPO chỉ trên SQL có tác dụng ở 1.5B: model nhỏ sai nhiều hơn
  nên có nhiều cặp hơn; dẫn bằng số cặp.
- 8.2 Trần wrong results: 442 câu sai kết quả, 193 câu trong đó có dòng khác
  làm đúng, và teacher đúng trên 129 câu. 154 câu có sample đúng trong 8
  (vote lấy lại 43), 288 câu không có. Một phần của trần này có thể nằm ở
  nhãn: audit tay 100 câu tách gold SQL lỗi và câu hỏi mơ hồ khỏi lỗi của
  model. [M5]
- 8.3 Nhãn dương tính giả: Spider train không có test-suite database nên
  một SQL khớp kết quả vẫn có thể sai; ước lượng tỉ lệ trên một mẫu cặp.
  [M5]
- 8.4 Giới hạn: một benchmark ở client, 5 client tham gia đủ mọi round,
  privacy là cô lập dữ liệu không có đảm bảo DP, client cần GPU để sample và
  train.

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
- D. Độ nhạy theo K, beta, mức non-IID và kích thước student.
- E. CoT ở 1.5B không giúp (plan + SQL).
- F. Ví dụ cặp preference và các loại lỗi.

## 7. Thực nghiệm

Tất cả thời gian là ước lượng trên một RTX A5000 (GPU 0), tính từ các lần
chạy đã đo: một round FedAvg khoảng 1.65 h, ba round DPO kèm evaluation
khoảng 5.5 h, một epoch Hinton KD trên BIRD khoảng 3.5 h, một epoch gold
khoảng 2.7 h, một lần evaluation Spider test khoảng 6 phút.

### 7.1 Đã có

| Nhóm | Nội dung | Seed |
|---|---|---|
| Mốc tham chiếu | base model, SFT tập trung Spider, SFT tập trung Spider + BIRD | 0 |
| Dòng FedAvg | FedAvg R3, DPO round 1-3 | 0, 1 |
| Dòng Hinton (method) | server distillation, FedAvg R3, DPO round 1-3 (seed 0 có thêm round 4) | 0, 1 |
| Dòng gold | server stage gold, FedAvg R3, DPO round 1-3 | 0, 1 |
| Dòng virtual teacher | điểm xuất phát, DPO round 1-3 | 0 |
| Self teacher | điểm xuất phát (không có DPO) | 0 |
| Ablation stage DPO | chỉ NLL, thêm 1 và 2 round SFT, Focused-DPO round 1, ghép cặp ngẫu nhiên round 1, không có NLL round 1-3 (round 3 trên cả sáu set), không có gold fallback round 1, 5 adapter client của DPO round 1 trước khi aggregate | 0 |
| Chọn câu theo execution lúc inference | 8 sample mỗi câu hỏi Spider test, fallback và vote, trên FedAvg R3, điểm xuất phát Hinton và DPO round 3 từ mỗi dòng | 0 |
| Các set khác | Spider dev, DK, SYN, Realistic, BIRD dev: điểm xuất phát và round 3 của mỗi dòng | 0, 1 |
| Teacher 7B zero-shot | Spider test (engine HF, 4-bit) | 0 |
| Phân tích từ prediction | loại lỗi, chuyển trạng thái giữa các dòng, theo độ khó, teacher so với student | 0, 1 |

### 7.2 Đã queue

Trạng thái và giờ: `paper/notes/PIPELINE_NEXT.md`. Theo thứ tự trong queue:

| # | Task | Trả lời câu hỏi | Vào đâu trong paper | GPU-h |
|---|---|---|---|---:|
| | Round 1-3 đều train trên sample của round 1 (seed 0, từ điểm xuất phát Hinton) | Sample lại mỗi round có cần không | Bảng 7 | 5 |
| M1 | Seed 2 của dòng Hinton, rồi dòng gold: stage server, 3 round FedAvg và 3 round DPO mỗi dòng, các set khác | Dòng method có 3 seed; cỡ phần teacher trên 3 seed | Bảng 2, 3, 4, 6, Hình 2 | 33.5 |
| M4 | Teacher 7B zero-shot trên vLLM, sáu set | Dòng teacher cùng engine với student; phân tích 7.5 so từng câu hợp lệ | Bảng 2, 3, Hình 5 | 1 |
| M3 | FedProx, FedNTD trên sáu set và các model local của từng client trên Spider test, engine vLLM, seed 0 | Bảng chính có đủ baseline FL chuẩn trên cùng engine | Bảng 2, 3 | 2 |
| | DPO tập trung trên dữ liệu client gộp, 3 round (seed 0) | Setting federated mất gì ở stage chính | Bảng 7 | 5.75 |
| M1 | Seed 2 của dòng FedAvg | Stage DPO không có stage server trên 3 seed | Bảng 2, 4, Hình 2 | 10.5 |

Tổng: khoảng 58 GPU-h.

- M1: logit cache của teacher trên BIRD dùng lại được vì không phụ thuộc
  seed.
- M3: dùng lại adapter seed 0 của ba baseline (owner cho phép ngày
  2026-11-13); một task kiểm tra chúng còn trên server trước khi evaluate.
- M4: teacher 7B chưa từng chạy qua vLLM trên card này, kiểm tra bộ nhớ ở
  batch đầu.
- Dòng local chỉ có round 1; ba round không aggregate cần code mới (khoảng
  6 h), xem mục 7.5.

### 7.3 Đề xuất chạy thêm

Chưa queue; chờ owner quyết.

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| N2 | Hai biến thể của DPO round 1 trên sample round 1 của dòng Hinton (seed 0, code mới cho cách gán nhãn): (V) nhãn bằng vote theo kết quả execution, không đọc gold SQL; (X) chỉ cặp "chạy được / không chạy được" | Nhãn gold có vai trò gì trong stage DPO; gain có phải chỉ là học viết SQL chạy được không | Bảng 7 | 3.5 |
| N3 | Chọn câu theo execution trên seed 1, bốn dòng | Các số ở Bảng 5 có 2 seed | Bảng 5 | 1 |
| M5 | Tổng hợp không cần GPU: số cặp theo client và round; bảng chi phí và communication (GPU-h, số request sampling, dung lượng update mỗi round, so với FedProx và FedNTD); ước lượng tỉ lệ chosen dương tính giả trên 200 cặp có chosen không phải gold; audit tay 100 câu wrong-result của method (gold lỗi, kết quả tie, câu hỏi mơ hồ, lỗi của model); một đoạn threat model | Các câu hỏi reviewer chắc chắn đặt ra về một method DPO dùng nhãn execution trong FL | Hình 4, Appendix B, mục 8.2, 8.3, 3.2 | 0 |

Tổng: khoảng 4.5 GPU-h.

- N2: hơn nửa gain ròng của DPO trên Spider test nằm ở các câu mà vote của
  điểm xuất phát sai (mục 7.3 của outline), nên kỳ vọng V thấp hơn DPO với
  nhãn gold. Nếu V ngang, xem mục 9.
- M5: hai phần đọc tay cần khoảng 2 giờ mỗi phần.
- Teacher 7B zero-shot ở đây đạt 77.22 trên Spider test (HF, 4-bit), thấp
  hơn số 82.2 OmniSQL báo cho cùng model với prompt của họ. Sau M4 (bf16,
  vLLM), mục 5.3 của outline nêu rõ khác biệt về prompt (schema DDL, không
  có sample value) và về metric.

### 7.4 Đề xuất chạy thêm nếu nhắm Q2

Chưa queue; chờ owner quyết.

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| F1 | 20 client trên Spider train, tỉ lệ tham gia 100% và 25% mỗi round, chỉ stage DPO từ model SFT đã có, seed 0 | Method có giữ được khi nhiều client hơn và không phải client nào cũng tham gia mỗi round | 7.8, Appendix D | 10 |
| S3 | Student thứ hai (Qwen2.5-Coder-0.5B), seed 0: dòng FedAvg và dòng method | Method có giữ được ở một kích thước model khác không; title nói "small models" | Một bảng ở mục 6 | 15-20 |
| S1 | Split `alpha_0.5/k5` (non-IID nhẹ hơn), seed 0: dòng FedAvg và dòng method; dùng lại stage server | Gain có phụ thuộc vào một mức non-IID không | 7.8, Appendix D | 21 |
| P1 | FedAvg 3 round rồi DPO 3 round với schema có sample value và foreign key trong prompt (`--schema-style codes`), seed 0, không có stage server | Gain của stage DPO có còn khi baseline SFT nhận input giàu hơn, vì lỗi `no such column` có thể tự giảm | 7.8, Appendix D | 10.5 |

Tổng: khoảng 57 đến 62 GPU-h.

- F1 thay đổi phần setup cố định (5 client) và cần một split mới; chạy
  stage SFT lại trên split đó thêm khoảng 5 h.
- S3 thay đổi phần setup cố định (một student); thời gian chưa đo trên
  0.5B với chuỗi này, và logit cache của teacher cần audit lại cho student
  mới.
- P1 thay đổi prompt cố định; kết quả là một phép kiểm tra độ bền của gain,
  không thay các dòng chính.

### 7.5 Nên chạy nếu còn thời gian

| # | Thực nghiệm | Trả lời câu hỏi | GPU-h |
|---|---|---|---:|
| S2 | Độ nhạy của stage DPO: K = 4 và 16, beta = 0.05 và 0.5, chỉ round 1, seed 0 | Method có nhạy với hai hyperparameter chính không | 7 |
| S4 | FedProx seed 1 và 2 | Baseline FL mạnh nhất cũng có 3 seed | 10 |
| L1 | Ba round DPO ở từng client, không aggregate (cần code mới) | Dòng local đủ 3 round cho Bảng 7 | 6 |
| B1 | Benchmark client thứ hai (ví dụ BIRD train chia theo database làm dữ liệu client) | Kết quả có giữ trên một domain client khác không | chưa đo |

- S2 chỉ chạy round 1 thay vì 3 round (đủ 3 round sẽ là 22 h); kết quả là
  xu hướng theo hyperparameter, không phải số cuối của method.
- B1 thay đổi setup cố định (5 client Spider) và cần một nguồn public khác
  cho server; là quyết định của owner.

### 7.6 Thứ tự

Thứ tự trong queue (owner, 2026-11-13 và 2026-11-14):

1. Các round dùng lại sample của round 1 (khoảng 5 h).
2. M1, dòng Hinton rồi dòng gold của seed 2 (khoảng 33.5 h); chạy nền trong
   lúc viết Introduction, Related Work, Setting, Method. M5 làm song song vì
   không cần GPU.
3. M4 và M3 (khoảng 3 h): hoàn thiện Bảng 2 cho seed 0, đủ để bắt đầu viết
   mục 5, 6 và 7.
4. DPO tập trung (khoảng 5.75 h), rồi M1 dòng FedAvg (khoảng 10.5 h).

Chưa queue, theo thứ tự đề xuất:

1. N2 và N3 (khoảng 4.5 h). N2 nên chạy trước các round DPO của seed 2, vì
   kết quả của nó có thể đổi cách mô tả stage DPO.
2. F1, S3, S1, P1 (57 đến 62 h).
3. Mục 7.5 theo thứ tự trong bảng, nếu còn thời gian trước khi nộp.

## 8. Đối chiếu với chuẩn Q2-Q3

Các điểm mà reviewer ở nhóm venue mục tiêu thường xét với một paper method
về federated learning cho LLM, và trạng thái của paper theo kế hoạch này.

| Điểm reviewer xét | Hiện tại | Sau mục 7.2 và 7.3 | Sau mục 7.4 |
|---|---|---|---|
| Số seed, độ lệch chuẩn, kiểm định cặp | 2 seed, có khoảng tin cậy | 3 seed cho mọi dòng chính | như trước |
| Baseline FL chuẩn trên cùng engine | chỉ FedAvg | FedAvg, FedProx, FedNTD, local | như trước |
| Baseline dùng execution lúc inference | có trên bốn dòng, seed 0: với cùng vote, method hơn FedAvg 2.84 | 2 seed | như trước |
| Mốc tập trung của chính method | chỉ có SFT tập trung | có DPO tập trung; local ở round 1 | như trước |
| Mỗi phần của stage DPO có vai trò được đo | preference term rõ; NLL (3 round), gold fallback và cách ghép cặp (round 1) không có vai trò | thêm sample lại mỗi round, nhãn gold so với nhãn vote | như trước |
| Control tách "thêm dữ liệu ở server" khỏi "tín hiệu teacher" | gold 2 seed, virtual teacher seed 0 | gold và Hinton trên 3 seed | như trước |
| Hai nửa của title đều có số đỡ | client: +2.5 đến +3.9, rõ; server: +1.40 gộp 2 seed, trong đó teacher +0.98 sát ngưỡng | teacher so với gold trên 3 seed (mục 9) | như trước |
| Kết quả ngoài set dùng để chọn | 4 set trên database dev, không chọn gì trên đó, 2 seed | như trước, 3 seed | như trước |
| Hơn một mức non-IID | một split | một split (ghi ở giới hạn) | hai split |
| Số client và tỉ lệ tham gia | 5 client, tham gia đủ mọi round | như trước (ghi ở giới hạn) | thêm 20 client, 100% và 25% |
| Hơn một backbone | một student | một student (ghi ở giới hạn) | hai student |
| Hơn một benchmark ở client | chỉ Spider | chỉ Spider (ghi ở giới hạn) | chỉ Spider |
| Gain có giữ với input giàu hơn | chưa đo; prompt là schema DDL | chưa đo (ghi ở giới hạn) | có, một dòng với sample value và foreign key |
| Chi phí và communication | chưa tổng hợp | có bảng, cả phía client | như trước |
| So với số đã công bố ở cùng cỡ model | chưa có bảng | bảng ngữ cảnh ghi rõ greedy hay self-consistency, tập trung hay federated | như trước |
| Privacy | cô lập dữ liệu, không DP | nói rõ một câu ở 3.2 và 8.4 | như trước |

Điểm cần cân nhắc:

- Phần chắc nhất của paper là stage DPO (+2.5 đến +3.9 từ mọi điểm xuất
  phát). Stage server nhỏ hơn (+1.40 gộp hai seed); phần teacher trong đó
  (+0.98) sát ngưỡng và lệch giữa hai seed (+1.49, +0.47), nên cần seed 2
  cùng Bảng 6 để đứng vững như một contribution.
- Sau mục 7.2 và 7.3 paper đủ cho nhóm venue Q3. Với Q2, năm client tham
  gia đủ mọi round, một split và một backbone là các điểm reviewer sẽ yêu
  cầu bổ sung, nên F1, S3 và S1 thuộc phần nên chạy cho mục tiêu đó.
- Gain của method nằm ở các câu SQL không chạy được, và một bước vote lúc
  inference cũng sửa loại lỗi này. Bảng 5 trả lời bằng so sánh cùng ngân
  sách inference: với cùng 8 sample và cùng vote, method hơn FedAvg 2.84
  điểm và stage DPO thêm 1.2 đến 1.9 (seed 0).
- Teacher 7B zero-shot ở đây (77.22) thấp hơn số đã công bố cho cùng model
  (OmniSQL: 82.2 với prompt của họ). Paper nêu rõ khác biệt về prompt; P1 đo
  gain của stage DPO khi prompt có sample value và foreign key.
- Phần mới về kỹ thuật là sự kết hợp và kết quả đo, không phải một loss hay
  một cách aggregate mới: FedDPO, nhãn execution và gold fallback đều đã có
  ở các paper khác. Paper nói rõ điều này và dựa vào các control để cho thấy
  phần nào của stage DPO thật sự cần.
- EX tuyệt đối 77 thấp hơn các số Spider test cao nhất đã công bố; paper so
  trong setting của mình (1.5B, greedy, federated, không model ngoài thấy dữ
  liệu client) và nêu rõ khác biệt setting với SQLoom.
- Một benchmark ở client là giới hạn còn lại sau mục 7.4; DK, SYN,
  Realistic cho thấy độ bền với cách hỏi khác, không thay được một domain
  client khác (B1).

### 8.1 Venue

Quartile theo SJR 2025, lấy từ một trang đăng lại bảng SCImago (chỉ Data &
Knowledge Engineering được đối chiếu với trang SCImago); cần kiểm tra lại
trên SCImago và JCR trước khi chọn.

| Venue | Quartile SJR 2025 | Độ hợp |
|---|---|---|
| J. Intelligent Information Systems | Q2 | hợp nhất: nhiều paper LLM Text-to-SQL trong 2025-2026, có paper về model nhỏ |
| Int. J. Data Science and Analytics | Q1 | hợp; thời gian đến accept dài |
| Neural Processing Letters | Q2 (một category Q3) | chủ đề còn mới với venue |
| Data & Knowledge Engineering | Q1 (Q2 năm 2024) | thiên về conceptual modelling |
| Distributed and Parallel Databases | Q2 ở một trên bốn category | scope lệch, ít bài mỗi năm |

Trong các paper Text-to-SQL đã đăng ở nhóm venue này, phần lớn dùng một
dataset và một backbone, không báo seed. Các paper federated LoRA ở các
venue lân cận dùng từ 10 client, có partial participation và báo
communication cost. Chọn venue chính là quyết định của owner.

## 9. Quyết định còn mở và kết quả sẽ đổi gì

Đã có kết quả:

| Kết quả | Thay đổi trong paper |
|---|---|
| Chọn câu theo execution (seed 0): vote trên điểm xuất phát ngang greedy sau DPO về tổng, nhưng hai cách đúng trên các câu khác nhau; method với vote cao hơn method greedy 1.68 | Bảng 5 có bốn dòng với greedy, fallback, vote và pass@8. Stage DPO không được mô tả là "bước vote đưa vào trọng số". Paper báo cả hai protocol: greedy (method hơn FedAvg 5.45 ở seed 0) và cùng vote (2.84). "Method + vote" là một dòng decoding, không phải dòng method |
| Round 1-3 không có NLL ngang DPO + NLL (76.76 so với 76.71 ở round 3) | Một dòng ở Bảng 7 và một câu ở 4.4. Bỏ NLL khỏi method là quyết định của owner (phải chạy lại các dòng DPO); method hiện giữ nguyên |
| Không có gold fallback ngang có fallback (75.50 so với 75.69, round 1) | Gold fallback là một chi tiết ở 4.4, không nằm trong danh sách điểm khác biệt |

Còn mở:

| Kết quả hoặc quyết định | Thay đổi trong paper |
|---|---|
| Seed 2: teacher so với gold sau DPO, khoảng tin cậy gộp 3 seed không chứa 0 | Title và contribution 3 giữ nguyên; 7.4 nói teacher cho một phần nhỏ, tách được |
| Seed 2: khoảng tin cậy gộp 3 seed chứa 0 | Title đổi sang bản thứ ba ở mục 3.1; stage server được mô tả là một stage trên dữ liệu public, Hinton KD là một lựa chọn; contribution 3 thành "control cho thấy teacher không thêm gì tách được sau DPO"; mục 7.5 và Hình 5 thành một đoạn ngắn. Dòng method có giữ teacher hay không là quyết định của owner |
| N2: nhãn vote (V) thấp hơn rõ nhãn gold | Nhãn gold qua execution là phần của stage DPO có vai trò được đo; một dòng ở Bảng 7 |
| N2: V ngang nhãn gold | Stage DPO không cần gold SQL. Mở ra một setting có client chỉ có câu hỏi và database; có chạy setting đó hay không (khoảng 27 GPU-h, giấu SQL của một phần client) là quyết định của owner |
| N2: chỉ cặp "chạy được / không chạy được" (X) ngang nhãn gold | Stage DPO được mô tả hẹp hơn: học viết SQL chạy được trên schema; mục 7.1 và 8.2 nói rõ |
| Các round dùng lại sample của round 1 ngang các round sample lại | Sample một lần là đủ: nêu như một cách giảm chi phí ở 4.5; nếu thấp hơn, sample lại mỗi round có vai trò được đo |
| DPO tập trung cao hơn rõ dòng federated | Khoảng cách được báo cáo là chi phí của setting federated ở Bảng 7; nếu ngang, một câu: federation không làm mất gain của stage DPO |
| P1: gain của stage DPO giảm rõ khi prompt có sample value và foreign key | Paper báo cả hai prompt và nói gain phụ thuộc mức lỗi execution của điểm xuất phát; nếu gain giữ, một dòng ở Appendix D |
| F1: EX giảm rõ ở 25% tham gia | Báo cáo như chi phí của partial participation ở 7.8; nếu giữ, một câu ở 7.8 và 8.4 bỏ giới hạn "5 client tham gia đủ" |
