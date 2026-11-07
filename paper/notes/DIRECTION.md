# FedLS-SQL: chọn hướng

Ngày 2026-11-06. Dựa trên `RESEARCH_STATE.md`, `LITERATURE.md`, số đo GPU trong
`fedicl-sql/docs/A5000_RUN_CONFIG.md` và đầu ra teacher có sẵn trong
`fedicl-sql/docs/SERVER_STORAGE.md` mục 5. Bản này đã sửa theo một vòng phản
biện của reviewer độc lập (mục 6). Chưa có kết quả nào kể từ fresh start; mọi
GPU-h dưới đây là ước lượng từ số đo cũ của từng loại job.

## 1. Tóm tắt

- Khuyến nghị: Hướng 1, DPO lặp theo vòng FL, mỗi client tự gán nhãn cặp bằng
  cách chạy SQL trên database của mình. Không cần teacher.
- Nếu owner giữ mục tiêu "teacher phải đóng góp đo được" (đang ghi trong
  `AGENTS.md`), chọn Hướng 2: teacher dạy suy luận ngắn trên BIRD, client DPO
  trên cả suy luận.
- Thí nghiệm đầu tiên phải trả lời một câu trước mọi thứ: DPO có thắng một
  baseline SFT đã hội tụ và thắng "chỉ SFT trên sample đúng" (Fed-RFT) hay
  không. Khoảng 16-26 GPU-h.
- Owner cần quyết định trước khi chạy: chọn hướng; sửa chỗ `AGENTS.md` và
  `RESEARCH_STATE.md` nói khác nhau về teacher; có cho dùng lại adapter SFT cũ
  không (tiết kiệm khoảng 10 GPU-h).

## 2. Bài toán nhìn từ đầu

Năm client giữ dữ liệu Spider riêng, train chung model 1.5B bằng FL, chỉ deploy
model 1.5B. Spider dev và test dùng database khác train, nên số đo chính là khả
năng làm đúng trên database mới cùng kiểu Spider, không phải trên database của
chính các client.

Owner đã quan sát (2026-11-06; số đo thuộc giai đoạn trước fresh start nên
không được dùng trong paper, phải đo lại):

- client drift không đáng kể, FedAvg gần bằng train tập trung. Literature
  cũng thấy vậy với LoRA trên LLM và reward khách quan (FS-LLM, OpenFedLLM,
  Fed-GRPO).
- DPO cho hiệu quả cao.

Hệ quả: method sửa drift (aggregation mới, FedProx, SCAFFOLD) gần như không còn
chỗ để thắng. Muốn thắng baseline federated thì phải đổi cái client học, sao
cho vẫn chạy được trong FL.

Điểm thuận lợi của Text-to-SQL: mỗi client có database và gold SQL, nên chạy
SQL model sinh ra là biết đúng hay sai. Client tự tạo cặp preference (đúng vs
sai), không cần người gán nhãn, không gửi gì ra ngoài.

Điểm phải đối mặt: Liu et al. (ACL 2025) và ExCoT thấy DPO chỉ với SQL (không
CoT) không giúp, có khi hại, ở model 6.7B trở lên; Spider train chỉ cho
0.1-0.3k cặp. Một lý do có thể: model đã SFT trên chính các câu đó nên gần như
luôn ra đúng gold, ít câu có cả đúng lẫn sai. Ở 1.5B điều này chưa ai đo.

## 3. Số đo dùng để ước lượng

GPU-h tính trên một card A5000; hai card chạy hai lane song song.

| Job | Số đo |
|---|---|
| Một vòng FL SFT, 5 client, toàn bộ 8,659 dòng Spider | 1.6-1.7 h |
| Eval SQL-only Spider dev, batch 16 | 0.07-0.3 h |
| Sample K=8 cho DPO | 300 dòng trong 0.3-0.7 h (khoảng 1-2.3 h cho 1,000 câu) |
| Update DPO + NLL | 0.4-0.9 h mỗi vòng, đo trên cặp từ khoảng 300 dòng |
| Sample CoT K=4, T=0.7 (student) | 2.6 s mỗi output |
| SFT trên CoT ngắn, 2,132 dòng | 1.3 h |
| Eval CoT so với SQL-only | khoảng 6.6 lần chậm hơn |
| Teacher sinh CoT ngắn trên BIRD, 4-bit batch 8 | 7.0-7.2 s mỗi output |
| CE trên BIRD gold, 9,428 dòng, 1 epoch | 2.7 h |

Ba chỗ chưa có số đo: sample K=8 không ghi là Spider hay BIRD (BIRD prompt dài
hơn nhiều, nhân thêm 1.5-3 lần); update DPO trên cặp từ 2,000 câu có thể tốn
0.4-6 h (tới khoảng 7 lần số đo cũ); chạy 50-100k câu SQL để gán nhãn mỗi vòng
là việc của CPU và có thể thêm vài giờ, nên dùng timeout gán nhãn ngắn (ví dụ
10 s, bỏ sample quá giờ và báo tỉ lệ bỏ). Timeout eval 60 s giữ nguyên.

## 4. Các hướng, xếp theo khả năng được nhận

Mỗi hướng tách method (cái paper đề xuất) và thí nghiệm kiểm chứng.

### Hướng 1: DPO lặp theo vòng FL, client tự gán nhãn bằng execution

Method:

1. Khởi động bằng FedAvg SFT trên Spider của các client.
2. Mỗi vòng, server gửi LoRA global. Mỗi client lấy một phần câu hỏi (ví dụ
   400 câu), sample K=8 SQL từ model global.
3. Client chạy từng SQL trên database của mình, so kết quả với gold. Hai điểm
   riêng cho SQL:
   - giảm "đúng giả": SQL chỉ tính là đúng khi cũng khớp gold trên vài bản
     database đổi giá trị, theo cách sinh database của test-suite (Zhong et
     al., EMNLP 2020), áp vào nhãn train thay vì vào eval;
   - chọn cặp: chosen là SQL đúng (dùng gold nếu không có sample nào đúng);
     rejected ưu tiên SQL chạy được nhưng ra kết quả sai, rồi mới tới SQL lỗi.
4. Client train DPO + NLL vài bước, reference là model global của vòng đó, rồi
   gửi LoRA.
5. Server FedAvg, trọng số theo số cặp. Vòng sau sample lại từ model mới, nên
   cặp luôn là lỗi của model hiện tại.

Phần "federated" có ích ở đâu: mỗi client có ít câu hỏi nên ít cặp. Nếu client
tự làm DPO một mình không đủ cặp mà federated thì đủ, FL là cần thiết, không
chỉ là đường truyền. Đây là phép so phải có.

Teacher đóng góp: không dùng.

Phép so chính, trên Spider test (greedy EX) và Spider dev (EX và test-suite):

- method vs FedAvg SFT cùng số vòng, và vs FedAvg SFT được thêm epoch cho bằng
  GPU-h (một vòng DPO tốn hơn một vòng SFT nên không thể vừa bằng vòng vừa bằng
  GPU-h);
- method vs Fed-RFT (SFT trên chính các sample đúng, không có rejected): cho
  biết cặp sai có thật sự giúp không;
- method vs FedDPO offline (cặp sample một lần, không sample lại): tách phần
  "lặp on-policy";
- method vs mỗi client tự DPO một mình, và vs method chạy tập trung: cho biết
  FL cứu được bao nhiêu phần của bản tập trung;
- trọng số theo số cặp vs theo số dòng; báo cả client kém nhất.

Paper gần nhất: Iterative RPO (NeurIPS 2024, tập trung, toán), ExCoT (tập
trung, SQL, 32-70B, có CoT), FedDPO trong OpenFedLLM và FedBiscuit (human
preference), federated GRPO (Fed-GRPO, PubSwap; toán và code). Khác: federated
với verifier tại client, 1.5B, SQL-only, có lọc "đúng giả" cho Spider.

Vì sao DPO mà không GRPO: GRPO phải sample K output ở mỗi bước train. Với số đo
sample hiện có (1-2.3 h cho 1,000 câu K=8), một lượt GRPO qua 8,659 câu tốn
khoảng 9-20 GPU-h chỉ riêng phần sample, trong khi một vòng DPO chỉ sample một
phần câu. Paper nên nêu con số này; một bản GRPO ngắn chỉ chạy nếu còn ngân
sách.

Thí nghiệm đầu tiên (xem mục 5): khoảng 16-26 GPU-h.

Baseline cần có: zero-shot student; teacher zero-shot (chỉ tham khảo, không
deploy); mỗi client train riêng; FedAvg SFT (cùng vòng và cùng GPU-h); FedProx
(một đại diện sửa drift); FedOPT + Lorar của FL4SP (method FL Text-to-SQL duy
nhất đã công bố); SFT tập trung; Fed-RFT; FedDPO offline; method tập trung;
DPO từng client riêng.

Ngân sách cả paper: mỗi vòng DPO khoảng 3-11 GPU-h; 5 vòng x 3 seed cho arm
chính là 45-165 GPU-h; cộng các baseline và đối chứng ở 3 seed, tổng khoảng
200-450 GPU-h, tức khoảng 4-10 ngày trên hai card.

Rủi ro chính:

- Kết quả DPO của owner không lặp lại được khi so với SFT đã hội tụ và Fed-RFT.
  Khi đó hướng này mất trụ; thí nghiệm đầu tiên được thiết kế để biết điều này
  sớm.
- Ít cặp vì model đã thấy câu hỏi lúc SFT. Cách xử lý: tách dữ liệu mỗi client
  thành phần SFT và phần preference (ví dụ 60/40).
- Novelty mỏng nếu bản federated bằng bản tập trung và không có phép so
  "client riêng vs federated". Reviewer đánh giá khả năng "major revision rồi
  accept" ở DKE, IJDSA, NPL nếu có đủ các phép so trên với 3 seed; thiếu thì
  nhiều khả năng bị reject.
- Lợi ích bão hoà sau 2-3 vòng (Iterative RPO, ExCoT đều thấy vậy).

### Hướng 2: teacher dạy suy luận ngắn trên BIRD, client DPO trên cả suy luận

Method:

1. Server: teacher viết CoT ngắn, có cấu trúc cho câu BIRD (đã có 1,266 dòng đã
   kiểm; sinh thêm khoảng 7 s mỗi dòng, 5,000 dòng khoảng 10 GPU-h), giữ dòng
   có SQL khớp gold.
2. Server SFT student trên CoT này để student có format "suy luận ngắn rồi SQL".
3. Các vòng FL: client sample K output CoT + SQL trên câu Spider của mình, gán
   nhãn bằng execution, DPO + NLL trên cả chuỗi, FedAvg (như Hướng 1).

Teacher đóng góp: cách suy luận mà Spider không có và gold không cung cấp được.
Đây là đóng góp của teacher khó thay bằng gold nhất trong bốn hướng.

Phép so đo teacher: cùng pipeline, thay CoT teacher bằng CoT student tự viết
trên BIRD (cũng lọc bằng execution). So thêm với Hướng 1 (SQL-only) và với SFT
trên CoT teacher không DPO.

Paper gần nhất: Liu et al. ACL 2025 (CoT làm DPO có tác dụng trên SQL ở 7B+),
ExCoT, Struct-SQL (CoT có cấu trúc từ BIRD, 4B), OmniSQL; FedCoT (nhưng FedCoT
cho teacher thấy dữ liệu client). Khác: federated, teacher chỉ thấy BIRD,
student 1.5B.

Thí nghiệm đầu tiên rẻ nhất (cổng vào): SFT student trên 1,266 dòng CoT teacher
và SFT trên SQL gold của cùng 1,266 dòng, eval cả hai trên Spider dev. Khoảng
2-3 GPU-h (eval CoT chậm hơn). Nếu CoT không hơn SQL-only, dừng hướng này.

Sau cổng: sample CoT K=4 trên 2,000 câu client để đếm cặp (khoảng 5.8 h), một
vòng DPO (0.9 h trở lên), eval (1-2 h). Cả paper: riêng phần sample CoT 5 vòng x
3 seed khoảng 87 GPU-h, cộng eval CoT trên bốn tập; khoảng 2-3 tuần.

Baseline: như Hướng 1, thêm SFT trên CoT teacher không DPO, và CoT tự viết.

Rủi ro chính: model 1.5B học CoT kém (Li et al. 2025: 1.5B chỉ hợp CoT ngắn);
deploy chậm khoảng 6.6 lần; nếu DPO SQL-only đã mạnh thì CoT có thể không thêm
gì; mỗi vòng sample tốn gấp nhiều lần Hướng 1.

### Hướng 3: như Hướng 1, thêm bước server dùng cặp từ teacher trên BIRD

Method:

1. Client làm như Hướng 1.
2. Sau mỗi FedAvg, server sample K SQL từ model global trên một phần BIRD
   train, chạy so với gold BIRD.
3. Câu nào student không có sample đúng thì chosen là SQL teacher đã khớp gold
   (có sẵn 5,319 dòng); câu khác thì chosen là sample đúng của student.
   Rejected là sample sai của student.
4. Server chạy một bước DPO + NLL ngắn trên các cặp BIRD rồi gửi model xuống.

Teacher đóng góp: SQL đúng cho câu BIRD student không tự giải được, viết theo
phong cách Qwen. Nhưng SQL teacher chỉ được giữ khi khớp gold, nên teacher chỉ
viết lại cái server đã có theo kiểu khác.

Phép so đo teacher: cùng bước server, cùng câu, thay chosen từ SQL teacher sang
gold BIRD. Hai bản chỉ khác nhau trên tập câu "student không có sample đúng và
teacher khớp gold".

Paper gần nhất: ExCoT (vòng off-policy với cặp GPT-4o), FedBiscuit (DPO tại
server), PubSwap (public prompt), FedCoLLM (KD tại server).

Thí nghiệm đầu tiên rẻ nhất: đo trên đúng tập câu khác nhau đó (báo số câu)
NLL của student trên SQL teacher và trên gold. Khoảng 0.5-1 GPU-h. Nếu tập chỉ
vài trăm câu hoặc NLL không khác rõ, dừng.

Rủi ro chính: chênh lệch teacher vs gold dự kiến dưới mức phát hiện được (khoảng
1-1.5 điểm EX với 3 seed trên 2,147 câu), nên teacher thành ablation; cặp SQL
từ BIRD có thể không chuyển sang Spider (Reasoning-SQL thấy SFT trên BIRD làm
Spider kém đi); DPO độ dài BIRD vượt 21.5 GiB nếu không tính chosen và rejected
lần lượt.

### Hướng 4: on-policy distillation tại server giữa các vòng

Method: sau mỗi FedAvg, server sample SQL student trên câu BIRD; teacher tính
log-prob từng token trên SQL của nó và của student; server train một bước theo
loss kiểu DistiLLM-2 (kéo lên ở SQL teacher, đẩy xuống ở token student mà
teacher cho là khó xảy ra), rồi gửi model xuống.

Teacher đóng góp: tín hiệu từng token (sai ở chỗ nào), thứ execution không cho.

Phép so đo teacher: cùng bước server, cùng câu, thay bằng SFT trên gold BIRD.

Paper gần nhất: DistiLLM-2 (đúng cặp Qwen2.5-Coder 7B -> 1.5B, trên code),
GKD, KID (SQL, 1.1B), FedCoLLM.

Thí nghiệm đầu tiên: thử tập trung tại server trước. Khoảng 3-5 GPU-h nếu
teacher chấm token nhanh, nhưng tốc độ chấm chưa đo, cần code mới (teacher và
student cùng lúc trên hai card) và probe bộ nhớ.

Rủi ro chính: FL không đóng vai gì trong bước server; KID thấy on-policy KD cho
SQL chỉ thêm khoảng 2 điểm với chi phí gấp 8 lần; không tận dụng DPO.

## 5. Khuyến nghị và thí nghiệm đầu tiên

Khuyến nghị Hướng 1, vì nó bám đúng hai quan sát của owner, rẻ nhất, dùng lại
code DPO + NLL và round loop có sẵn, và lấp một khoảng trống rõ (chưa có
federated DPO với verifier, chưa có DPO Text-to-SQL dưới 6.7B, chưa có FL
Text-to-SQL với model decoder hiện đại). Nếu teacher bắt buộc, chọn Hướng 2
thay cho Hướng 3: SQL teacher trong Hướng 3 chỉ là gold viết kiểu khác.

Thí nghiệm đầu tiên cho Hướng 1, theo thứ tự:

1. FedAvg SFT trên toàn bộ dữ liệu client, eval Spider dev mỗi vòng, dừng khi
   dev hết tăng (tối đa 5 vòng). Khoảng 10 GPU-h, chạy tuần tự. Đây cũng là
   baseline chính. Bỏ được nếu owner cho dùng lại adapter SFT cũ đã eval cùng
   protocol.
2. Từ checkpoint tốt nhất, sample K=8 trên 2,000 câu client (400 mỗi client),
   chia đều hai card: 2-4.6 GPU-h. Gán nhãn trên CPU với timeout 10 s và lọc
   "đúng giả" bằng database đổi giá trị.
3. Đếm: số cặp mỗi client, tỉ lệ câu toàn đúng, toàn sai, có cả hai; tỉ lệ
   "đúng giả" bị lọc. Nếu câu có cả đúng lẫn sai quá ít, chuyển sang thiết kế
   tách dữ liệu 60/40 trước khi đi tiếp.
4. Ba arm từ cùng checkpoint, cùng sample: một vòng DPO + NLL (0.4-6 h); một
   vòng Fed-RFT (khoảng 0.5-2 h); một vòng SFT thêm (1.7 h).
5. Eval cả ba trên Spider dev, EX greedy batch 16 và test-suite (khoảng 1-1.5
   h). Đo độ chính xác của bộ lọc "đúng giả" trên Spider dev so với test-suite
   (chỉ eval, không train).

Tổng khoảng 16-26 GPU-h, khoảng 12-18 h wall trên hai card (phần SFT chạy tuần
tự). Kết quả cho biết DPO có thắng SFT và Fed-RFT không, và có đủ cặp không;
cả hai quyết định có đi tiếp Hướng 1 hay không.

Metric của paper: EX trên Spider test (greedy, batch 16) là số chính; Spider
dev (EX và test-suite) để chọn cấu hình; Spider-Realistic, SYN, DK cho độ bền;
BIRD dev chỉ khi có bước server trên BIRD. Kèm số cặp mỗi client, GPU-h mỗi
vòng, dung lượng truyền mỗi vòng, kết quả chia theo độ khó và loại lỗi. Ba
seed cho arm chính; seed gộp dùng kiểm định theo cụm câu hỏi.

## 6. Phản biện của reviewer và chỗ còn bất đồng

Reviewer đóng vai người phản biện ở DKE, IJDSA, NPL, DAPD. Xếp hạng của
reviewer: Hướng 1, rồi Hướng 2, Hướng 3, Hướng 4. Bản này đã sửa theo các ý
sau:

- Kết quả DPO của owner chưa phải bằng chứng cho paper và ngược với Liu et al.;
  thí nghiệm đầu tiên giờ so với SFT đã hội tụ và Fed-RFT.
- Sample trên câu đã SFT cho ít cặp; thêm bước đếm cặp và phương án tách
  60/40.
- Phần federated dễ bị coi là phụ; thêm phép so client riêng vs federated, trọng
  số theo cặp vs theo dòng, client kém nhất.
- Bộ lọc database đổi giá trị là cách của test-suite (Zhong et al. 2020), phải
  trích dẫn như vậy và đo độ chính xác trên Spider dev.
- Thêm baseline Fed-RFT, SFT cùng GPU-h, lý do không dùng GRPO bằng con số,
  test-suite trên Spider dev.
- Sửa ước lượng: DPO có thể tốn tới khoảng 7 lần số đo cũ; thời gian gán nhãn
  CPU; wall time 12-18 h thay vì 6-7 h; thêm ngân sách cả paper 200-450 GPU-h.
- Hướng teacher dự phòng đổi từ cặp BIRD sang CoT, và hướng cặp BIRD xuống thứ
  ba.
- Câu hỏi nghiên cứu: Spider dev và test đo khả năng trên database mới, không
  phải "domain của client".

Còn bất đồng hoặc còn mở:

- Tách dữ liệu 60/40 ngay từ đầu (reviewer) hay đo số cặp trước rồi mới quyết
  (bản này). Bản này chọn đo trước vì tách sẵn làm baseline SFT ít dữ liệu hơn
  và tốn thêm một lần SFT; nếu số cặp thấp thì làm theo reviewer.
- Reviewer cho rằng lý do chính khiến Liu et al. có ít cặp là model đã thấy câu
  hỏi lúc SFT. Đây là suy luận, chưa có số; bước 3 ở mục 5 đo nó.
- Reviewer coi một bản GRPO ngắn là nên có; bản này chỉ nêu chi phí bằng số và
  chạy GRPO nếu còn ngân sách sau các phép so chính.

## 7. Quyết định của owner (2026-11-06)

1. Chạy Hướng 1 trước: DPO + NLL federated, không dùng teacher.
2. Teacher là tuỳ chọn (`AGENTS.md`, `RESEARCH_STATE.md`).
3. Dùng lại adapter FedAvg SFT cũ (`p227_fl_aaa_s0`, R3) làm baseline và điểm
   xuất phát; số tham chiếu ghi trong `LAB_LOG.md`.

## 8. Hướng tiếp theo: bước server trên public data (đề xuất 2026-11-07)

Nối tiếp Hướng 1, chưa chạy. Diagram cho từng phương án: `paper/notes/figures/`
(mục 8.6).

### 8.1 Vì sao cần bước server

- FedAvg SFT đã gần bằng SFT tập trung (Spider test 71.50 so với 71.08), nên
  server không có gì nhiều để "sửa" sau aggregate. Vai trò của server là thêm
  kiến thức mà dữ liệu client không có.
- DPO ở client chỉ kéo được cái model đã biết (khoảng cách pass@8 và greedy).
  Public data ở server là chỗ để nâng trần đó.
- Nhiều paper train chung Spider và BIRD (OmniSQL, SQLoom, ExCoT), nên dùng
  BIRD làm public data là hợp lệ. Điều kiện: SFT gold BIRD chuyển sang Spider
  kém (Reasoning-SQL, OmniSQL), còn tín hiệu execution hoặc tương phản trên
  BIRD chuyển tốt (Think2SQL, Reasoning-SQL, SQLoom B→S 76.3 → 82.1).
- Nếu server chỉ chạy DPO trên BIRD giống client, nó chỉ là "client thứ 6 giữ
  BIRD". Bước server phải dùng thứ chỉ server có: teacher, toàn quyền trên
  public data, thấy mọi adapter client, compute tập trung.
- Teacher không dùng để sửa câu student viết sai: teacher chỉ khớp gold trên
  5,319 / 9,428 câu BIRD train (56%), và server đã có gold BIRD.

### 8.2 Các phương án train ở server

| | Phương án | Thứ chỉ server có | Bằng chứng | Chi phí | Đánh giá |
|---|---|---|---|---|---|
| S1 | KD offline trên logit teacher của chuỗi BIRD (cache có sẵn) | Teacher | KID: reverse-KL KD hơn SFT khoảng 2 điểm; MiniLLM: KD token xấp xỉ SFT ở 1.3B | Rẻ | Yếu; hợp làm bước khởi động |
| S2 | KD on-policy có cổng execution: student sinh SQL trên BIRD, teacher chấm từng token, chỉ trên câu teacher khớp gold | Teacher | DistiLLM-2 (đúng cặp 7B → 1.5B, code): HumanEval 30.7 → 42.2. KID (SQL, 1B): GKD +2, tốn 8.3 lần. Speculative KD: on-policy KD hỏng khi sample student kém | Trung bình; tốc độ teacher chấm chưa đo | **Đề xuất chính** |
| S3 | RL hoặc DPO bằng execution trên BIRD, dạng nặng hơn client (GRPO online) | Compute, toàn quyền dữ liệu | Chuyển BIRD → Spider mạnh nhất: Think2SQL 3B 72.5 → 77.0 | Cao | Dự phòng; cơ chế giống client |
| S4 | Chưng cất từ ensemble các adapter client trên BIRD, chọn output bằng execution (kiểu FedDF) | Thấy mọi adapter client | FedMKT, FedCoLLM: client +1-3; FedDF trên vision (chưa đọc) | Trung bình | Ít chỗ tăng vì drift nhỏ |
| S5 | Teacher viết CoT ngắn trên BIRD, student học suy luận | Teacher | Liu et al. ACL 2025; Struct-SQL | Cao; inference chậm khoảng 6.6 lần | Để dành |

### 8.3 Đề xuất: S2, KD on-policy có cổng execution

Mỗi lần ở server:

1. Model global sinh SQL cho câu BIRD train.
2. Chỉ giữ câu mà SQL teacher khớp gold (5,319 câu có sẵn): học từ teacher ở
   chỗ teacher đáng tin.
3. Teacher chấm từng token trên SQL của student và trên SQL đúng. Loss kiểu
   DistiLLM-2: kéo lên trên SQL đúng, đẩy xuống ở token student mà teacher cho
   là khó xảy ra.

Phân vai: client có tín hiệu thưa (cả câu đúng hay sai, từ execution trên dữ
liệu riêng); server có tín hiệu dày (sai ở token nào, từ teacher trên public
data). Paper gần nhất cần đọc kỹ: SERL-SQL (teacher chấm lại action của
student để chỉnh GRPO), DistiLLM-2 (loss), GKD, FedDF.

Rủi ro: tốc độ và bộ nhớ khi teacher chấm prompt BIRD dài chưa đo; chưa có
bằng chứng trên SQL rằng KD trên BIRD chuyển sang Spider; student yếu trên BIRD
(BIRD dev 25.68) nên sample nhiễu.

### 8.4 Đặt bước server ở đâu

| | Cách | Ai làm | Ưu | Nhược |
|---|---|---|---|---|
| A | Server là một participant trong FedAvg, song song với client | FedAuto | Không thêm thời gian tuần tự; đối xứng | Trọng số server là hyperparameter; BIRD có nhiều cặp nên dễ lấn át; update hai hướng có thể triệt tiêu |
| B | Server train sau mỗi lần aggregate, rồi gửi xuống | FedCoLLM, FedBiOT, FedBiscuit | Bước server tác động đủ; on-policy đúng model global vừa aggregate; reviewer quen | Bước cuối trước khi gửi luôn là BIRD; thêm thời gian mỗi vòng |
| C | Server train một lần trước các vòng client | GPT-FL, FedAuto stage 1 | Đơn giản, rẻ, ablation sạch | Chỉ đóng góp một lần, có thể bị quên |
| D | Server train một lần sau FL | | | Model deploy bị BIRD định hình sau cùng; loại |

Thứ tự: thử C trước (E1). Nếu Spider dev tăng, dùng B cho method, A làm
ablation.

### 8.5 Thí nghiệm E1 (chỉ phía server, từ FedAvg R3)

Bốn arm trên cùng câu BIRD, eval Spider dev và BIRD dev:

1. SFT gold BIRD (đối chứng "chỉ thêm dữ liệu").
2. DPO bằng execution trên BIRD (S3, bản rẻ).
3. KD offline từ cache (S1).
4. KD on-policy có cổng (S2).

Trước E1: probe tốc độ và bộ nhớ cho teacher chấm trên BIRD; đọc kỹ SERL-SQL,
DistiLLM-2, GKD, FedDF và thêm vào `LITERATURE.md`. Nếu không arm nào tăng
Spider dev so với R3, dừng hướng server.

### 8.6 Diagram

Một trang cho mỗi phương án, trong `paper/notes/figures/`: method tổng thể,
vòng client, S1-S5, cách đặt A/B/C.
