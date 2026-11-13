# Đề xuất paper FedLS-SQL: tên, outline và thực nghiệm

Ngày 2026-11-13, theo các kết quả đã committed đến 15:25 cùng ngày. Số liệu
lấy từ `paper/notes/RESEARCH_STATE.md` (mục 4) và `LAB_LOG.md`; nguồn tham
khảo lấy từ `paper/notes/LITERATURE.md`.

Stage DPO ở client cho phần lớn gain, stage distillation ở server cho phần
nhỏ hơn; title giữ cả hai. Nửa server của title phụ thuộc kết quả seed 2
(mục 9).

## 1. Tóm tắt

| Mục | Đề xuất |
|---|---|
| Title | **Distill at the Server, Verify at the Client: Federated Text-to-SQL for Small Language Models** |
| Tên method | FedLS-SQL (Federated LLM-to-SLM for Text-to-SQL) |
| Loại paper | Empirical method paper, cấu trúc IMRaD mở rộng cho ML |
| Venue | Data & Knowledge Engineering, Int. J. Data Science and Analytics, Neural Processing Letters, Distributed and Parallel Databases; stretch: J. Intelligent Information Systems |
| Kết quả chính (Spider test EX) | Method 76.71 / 77.04 (seed 0 / 1), FedAvg 71.26 / 71.87, SFT tập trung Spider + BIRD 73.96, teacher 7B zero-shot 77.22 |
| Đang queue | khoảng 16 GPU-h (mục 7.2) |
| Phải chạy thêm | khoảng 49 GPU-h trên một A5000 (mục 7.3), tức khoảng 2 ngày chạy liên tục |
| Phải chạy thêm nếu nhắm Q2 | khoảng 36 đến 41 GPU-h nữa (mục 7.4) |

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
loại này ở mọi dòng, từ base model đến DPO round 4.

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
   mình, ghép cặp đúng / sai (gold SQL làm chosen khi không sample nào
   đúng), train DPO + NLL; server làm FedAvg trên LoRA. Ở 1.5B stage này cho
   +2.5 đến +3.9 điểm từ ba điểm xuất phát, trong khi SFT và NLL cùng
   compute thì không. Work gần nhất: FedDPO trong OpenFedLLM và FedBiscuit
   (preference của người), Liu et al. 2025 và ExCoT (DPO tập trung, 7B trở
   lên, DPO chỉ trên SQL không có gain), Iterative RPO (gold làm chosen).
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
5. Phân tích: verifier sửa loại lỗi nào và không sửa loại nào, verify lúc
   train so với verify lúc inference, stage DPO trong setting federated so
   với tập trung và local, thành phần các cặp co lại thế nào qua các round,
   và trần khoảng 20% câu chạy được nhưng sai kết quả.

Không dùng "first".

## 6. Outline

Ký hiệu: [có] số đã có và committed; [queue] đã queue (mục 7.2); [N1], [M1]
đến [M5], [S1] đến [S4] là các thực nghiệm ở mục 7.

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
  inference. [M3, M4, N1]
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
- 7.3 Verify lúc train so với verify lúc inference (Bảng 5): FedAvg và
  method, mỗi dòng với greedy và với chọn câu theo execution trên 8 sample;
  số lần gọi model và database cho mỗi câu hỏi. [N1]
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
- 7.7 Ablation của stage DPO (Bảng 7, nửa dưới): chỉ NLL, không có NLL,
  thêm round SFT, ghép cặp ngẫu nhiên, Focused-DPO, không có gold fallback,
  các round dùng lại sample của round 1, số round. [có; queue]
- 7.8 Độ nhạy (ngắn, hình ở appendix): mức non-IID, kích thước student, số
  sample K, beta. [S1, S3, S2]

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
| Ablation stage DPO | chỉ NLL, thêm 1 và 2 round SFT, Focused-DPO round 1, ghép cặp ngẫu nhiên round 1, không có NLL round 1, 5 adapter client của DPO round 1 trước khi aggregate | 0 |
| Các set khác | Spider dev, DK, SYN, Realistic, BIRD dev: điểm xuất phát và round 3 của mỗi dòng | 0, 1 |
| Teacher 7B zero-shot | Spider test (engine HF, 4-bit) | 0 |
| Phân tích từ prediction | loại lỗi, chuyển trạng thái giữa các dòng, theo độ khó, teacher so với student | 0, 1 |

### 7.2 Đã queue

Trạng thái và giờ: `paper/notes/PIPELINE_NEXT.md`. Các task dưới đây là seed
0, từ điểm xuất phát Hinton. N1, M1, M3 và M4 của mục 7.3 cũng đã queue
(2026-11-13).

| Task | Trả lời câu hỏi | Vào đâu trong paper |
|---|---|---|
| DPO round 1 không có gold fallback | Gold fallback có vai trò không | Bảng 7 |
| Round 2-3 của dòng không có NLL | NLL có vai trò qua các round không | Bảng 7 |
| Round 1-3 đều train trên sample của round 1 | Sample lại mỗi round có cần không | Bảng 7 |
| DPO tập trung trên dữ liệu client gộp, 3 round | Setting federated mất gì ở stage chính | Bảng 7 |

Dòng local chỉ có round 1; ba round không aggregate cần code mới (khoảng
6 h), xem mục 7.5.

### 7.3 Phải chạy thêm

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| N1 | Chọn câu theo execution lúc inference, không train thêm: sample 8 SQL cho mỗi câu hỏi test, (a) giữ câu greedy nếu chạy được, nếu không lấy sample chạy được xuất hiện nhiều nhất, (b) bỏ phiếu theo kết quả execution. Trên bốn dòng: FedAvg R3, điểm xuất phát Hinton, DPO round 3 từ FedAvg, method | DPO cho được gì mà một bước kiểm tra ở inference không cho; hai cách có cộng được không | Bảng 5, mục 7.3 | 1 |
| M1 | Seed 2 cho ba dòng (FedAvg, Hinton, gold): hai stage server, 3 round FedAvg và 3 round DPO mỗi dòng, các set khác | Mọi dòng chính có trung bình và độ lệch chuẩn trên 3 seed; cỡ phần teacher trên 3 seed | Bảng 2, 3, 4, 6, Hình 2 | 45 |
| M3 | FedProx, FedNTD và các model local của từng client trên engine vLLM, sáu set, seed 0 | Bảng chính có đủ baseline FL chuẩn trên cùng engine | Bảng 2, 3 | 2 |
| M4 | Teacher 7B zero-shot trên vLLM, sáu set | Dòng teacher cùng engine với student; phân tích 7.5 so từng câu hợp lệ | Bảng 2, 3, Hình 5 | 1 |
| M5 | Tổng hợp không cần GPU: số cặp theo client và round; bảng chi phí (GPU-h, số request sampling, dung lượng update); ước lượng tỉ lệ chosen dương tính giả trên 200 cặp có chosen không phải gold | Ba câu hỏi reviewer chắc chắn đặt ra về một method DPO dùng nhãn execution | Hình 4, Appendix B, mục 8.3 | 0 |

Tổng: khoảng 49 GPU-h.

Ghi chú thực hiện:

- N1: chạy trước khi viết mục 6 và 7, vì kết quả quyết định cách mô tả stage
  DPO (mục 9). Cần một chế độ evaluation mới; thời gian là ước lượng từ tốc
  độ sampling vLLM đã đo (400 câu hỏi, 8 sample, 3:40).
- M1: logit cache của teacher trên BIRD dùng lại được vì không phụ thuộc
  seed. Trong 45 h có khoảng 7 h cho stage Hinton, 5.5 h cho stage gold,
  15 h cho 9 round FedAvg, 16.5 h cho ba dòng DPO. Thứ tự: dòng Hinton
  (khoảng 17.5 h), rồi dòng gold (khoảng 16 h): hai dòng này trả lời câu hỏi
  ở mục 9 về nửa server của title; dòng FedAvg (khoảng 10.5 h) chạy sau.
  Các round DPO của seed 2 chạy sau round 2-3 của dòng không có NLL (mục
  7.2), vì kết quả đó có thể đổi recipe DPO.
- M3: dùng lại adapter seed 0 của ba baseline (owner cho phép ngày
  2026-11-13); một task kiểm tra chúng còn trên server trước khi evaluate.
  Model local của từng client chỉ chạy trên Spider test.
- M4: teacher 7B chưa từng chạy qua vLLM trên card này, kiểm tra bộ nhớ ở
  batch đầu.
- M5: phần ước lượng dương tính giả cần khoảng 2 giờ đọc tay các chosen
  khác cấu trúc với gold.

### 7.4 Phải chạy thêm nếu nhắm Q2

| # | Thực nghiệm | Trả lời câu hỏi | Vào đâu | GPU-h |
|---|---|---|---|---:|
| S1 | Split `alpha_0.5/k5` (non-IID nhẹ hơn), seed 0: dòng FedAvg và dòng method; dùng lại stage server | Gain có phụ thuộc vào một mức non-IID không | 7.8, Appendix D | 21 |
| S3 | Student thứ hai (Qwen2.5-Coder-0.5B), seed 0: dòng FedAvg và dòng method | Method có giữ được ở một kích thước model khác không; title nói "small models" | Một bảng ở mục 6 | 15-20 |

Tổng: khoảng 36 đến 41 GPU-h.

- S3 thay đổi phần setup cố định (một student); thời gian chưa đo trên
  0.5B với chuỗi này, và logit cache của teacher cần audit lại cho student
  mới.

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

Thứ tự trong queue (owner đồng ý ngày 2026-11-13):

1. Gold fallback và round 2-3 của dòng không có NLL (mục 7.2).
2. M1, dòng Hinton rồi dòng gold của seed 2 (khoảng 33.5 h); chạy nền trong
   lúc viết Introduction, Related Work, Setting, Method. M5 làm song song vì
   không cần GPU.
3. N1, M4 và M3 (khoảng 4 h): hoàn thiện Bảng 2 và Bảng 5 cho seed 0, đủ để
   bắt đầu viết mục 5, 6 và 7.
4. Các round dùng lại sample của round 1 và DPO tập trung (khoảng
   10.75 h), rồi M1 dòng FedAvg (khoảng 10.5 h).
5. S1, rồi S3 (36 đến 41 h), chưa queue.
6. Mục 7.5 theo thứ tự trong bảng, nếu còn thời gian trước khi nộp.

## 8. Đối chiếu với chuẩn Q2-Q3

Các điểm mà reviewer ở nhóm venue mục tiêu thường xét với một paper method
về federated learning cho LLM, và trạng thái của paper theo kế hoạch này.

| Điểm reviewer xét | Hiện tại | Sau mục 7.2 và 7.3 | Sau mục 7.4 |
|---|---|---|---|
| Số seed, độ lệch chuẩn, kiểm định cặp | 2 seed, có khoảng tin cậy | 3 seed cho mọi dòng chính | như trước |
| Baseline FL chuẩn trên cùng engine | chỉ FedAvg | FedAvg, FedProx, FedNTD, local | như trước |
| Baseline dùng execution lúc inference | chưa có | có, trên bốn dòng | như trước |
| Mốc tập trung của chính method | chỉ có SFT tập trung | có DPO tập trung; local ở round 1 | như trước |
| Mỗi phần của stage DPO có vai trò được đo | preference term rõ; NLL và cách ghép cặp không có vai trò ở round 1 | thêm gold fallback, NLL qua 3 round, sample lại mỗi round | như trước |
| Control tách "thêm dữ liệu ở server" khỏi "tín hiệu teacher" | gold 2 seed, virtual teacher seed 0 | gold và Hinton trên 3 seed | như trước |
| Hai nửa của title đều có số đỡ | client: +2.5 đến +3.9, rõ; server: +1.40 gộp 2 seed, trong đó teacher +0.98 sát ngưỡng | teacher so với gold trên 3 seed (mục 9) | như trước |
| Kết quả ngoài set dùng để chọn | 4 set trên database dev, không chọn gì trên đó, 2 seed | như trước, 3 seed | như trước |
| Hơn một mức non-IID | một split | một split (ghi ở giới hạn) | hai split |
| Hơn một backbone | một student | một student (ghi ở giới hạn) | hai student |
| Hơn một benchmark ở client | chỉ Spider | chỉ Spider (ghi ở giới hạn) | chỉ Spider |
| Chi phí và communication | chưa tổng hợp | có bảng, cả phía client | như trước |
| So với số đã công bố ở cùng cỡ model | chưa có bảng | bảng ngữ cảnh ghi rõ greedy hay self-consistency, tập trung hay federated | như trước |
| Privacy | cô lập dữ liệu, không DP | nói rõ một câu ở 3.2 và 8.4 | như trước |

Điểm cần cân nhắc:

- Phần chắc nhất của paper là stage DPO (+2.5 đến +3.9 từ mọi điểm xuất
  phát). Stage server nhỏ hơn (+1.40 gộp hai seed); phần teacher trong đó
  (+0.98) sát ngưỡng và lệch giữa hai seed (+1.49, +0.47), nên cần seed 2
  cùng Bảng 6 để đứng vững như một contribution.
- Sau mục 7.2 và 7.3 paper đủ cho nhóm venue Q3. Với Q2, một split và một
  backbone là điểm reviewer sẽ yêu cầu bổ sung, nên S1 và S3 thuộc phần phải
  chạy cho mục tiêu đó.
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

## 9. Quyết định còn mở và kết quả sẽ đổi gì

| Kết quả hoặc quyết định | Thay đổi trong paper |
|---|---|
| Seed 2: teacher so với gold sau DPO, khoảng tin cậy gộp 3 seed không chứa 0 | Title và contribution 3 giữ nguyên; 7.4 nói teacher cho một phần nhỏ, tách được |
| Seed 2: khoảng tin cậy gộp 3 seed chứa 0 | Title đổi sang bản thứ ba ở mục 3.1; stage server được mô tả là một stage trên dữ liệu public, Hinton KD là một lựa chọn; contribution 3 thành "control cho thấy teacher không thêm gì tách được sau DPO"; mục 7.5 và Hình 5 thành một đoạn ngắn. Dòng method có giữ teacher hay không là quyết định của owner |
| N1: FedAvg với chọn câu theo execution đạt gần EX của method | Stage DPO được mô tả là đưa bước kiểm tra vào trọng số của model: một lần greedy, không cần database lúc inference, so với 8 sample và database cho mỗi câu hỏi. Con số +5.3 vẫn là so greedy với greedy |
| N1: method với chọn câu theo execution cao hơn method greedy | Thêm một dòng "method + chọn theo execution" ở Bảng 5: hai cách cộng được |
| Round 2-3 không có NLL ngang DPO + NLL | Một dòng ở Bảng 7 và một câu ở 4.2; method giữ nguyên. Nếu cao hơn rõ ở round 3, bỏ NLL là quyết định của owner (phải chạy lại các dòng DPO) |
| Không có gold fallback ngang có fallback | Gold fallback là một chi tiết ở 4.2, không nằm trong danh sách điểm khác biệt |
| Các round dùng lại sample của round 1 ngang các round sample lại | Sample một lần là đủ: nêu như một cách giảm chi phí ở 4.5; nếu thấp hơn, sample lại mỗi round có vai trò được đo |
| DPO tập trung cao hơn rõ dòng federated | Khoảng cách được báo cáo là chi phí của setting federated ở Bảng 7; nếu ngang, một câu: federation không làm mất gain của stage DPO |
