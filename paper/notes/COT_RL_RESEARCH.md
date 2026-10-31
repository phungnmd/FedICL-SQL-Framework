# CoT và RL cho FedLS-SQL: tổng hợp nghiên cứu

Cập nhật 2026-11-01. File này tổng hợp literature và kết quả của dự án về một
câu hỏi: server teacher có thể dạy student Coder-1.5B qua reasoning (CoT) không,
và RL giúp gì. Số của dự án là seed 0, EX (%), đã commit trừ P2.57 (ghi rõ bên
dưới). Quyết định và lệnh chạy không nằm ở đây: quyết định ở
[LAB_LOG](LAB_LOG.md), lệnh ở [PIPELINE_NEXT](PIPELINE_NEXT.md).

## 1. Kết luận

1. **Ưu tiên CoT theo clause, có kiểm SQL/schema, rồi Iterative DPO + NLL.**
   Lấy cách xây target từ VCoT-SQL, cleaning từ SLM-SQL, execution preferences
   từ ExCoT và NLL từ Iterative RPO. Đây là adaptation cho setup hiện tại;
   mục 10 ghi phương pháp và pilot được khuyến nghị, chưa phải lịch chạy.
2. **7B có cơ sở để làm teacher CoT.** VCoT-SQL tạo dữ liệu bằng các model 7B.
   RetrySQL và SLM-SQL cho thấy student 1.5B học được reasoning. Chưa có bài
   trong nhóm đã đọc xác nhận toàn bộ chuỗi 7B → 1.5B LoRA → private FL này.
3. **P2.58 chưa tách được nguyên nhân CoT thua.** Target, learning rate và
   coverage cần được xem cùng nhau. Trên SynSQL, median target CoT/SQL là
   566/123 token; trên Spider là 384/29. Số 23 là output SQL lúc eval, không
   phải target train cùng tập. CoT private còn bỏ 2,037/8,659 câu.
4. **Ngắn là lựa chọn cần thử, không phải kết luận nguyên nhân.** Bằng chứng
   length chủ yếu từ toán; chính các bài đó cũng phân biệt độ chi tiết hữu ích
   với số token. Ưu tiên các quyết định đúng, bỏ phần lặp và phần sau SQL.
5. **DPO trước vì có tín hiệu tại chỗ; GRPO có bằng chứng gần student hơn.**
   DPO + NLL đã tăng CoT 2.61 điểm trong P2.58. SLM-SQL có GRPO trên đúng
   Coder-1.5B, nhưng dùng nhiều samples khi eval và tài nguyên lớn hơn.
   Chưa có so sánh trực tiếp xác lập thuật toán nào tốt hơn ở setup này.
6. **Đóng góp teacher phải đo ở endpoint private/FL.** So với writer không dùng
   teacher trong cùng recipe. Template là control hữu ích nếu rationale chủ
   yếu diễn lại SQL; kết quả gần nhau chưa chứng minh effect bằng zero.

## 2. Bài toán và ràng buộc

- Student Qwen2.5-Coder-1.5B-Instruct, LoRA r16, greedy. Teacher Coder-7B, 4-bit,
  chỉ ở server và chỉ trên public data.
- **Điểm khó nhất:** teacher không được viết rationale cho dữ liệu private. Client
  muốn train CoT trên Spider thì phải tự viết (STaR) hoặc dùng template. Mọi kết
  quả literature dùng LLM viết rationale ngay trên tập train đều không chuyển thẳng
  được sang round private.
- Budget: hai RTX A5000 24 GB. Teacher rationalize 18.35 s/row (p50 538 token), base
  student 2.40 s/row, sampling CoT của student 2.62 s/output (P2.57,
  `fedicl-sql/docs/A5000_RUN_CONFIG.md`).

## 3. Dữ liệu của dự án

P2.58, tập trung, Spider dev, không có teacher 7B trong screen:

| Stage | SQL-only | CoT | Khoảng cách |
|---|---:|---:|---:|
| SFT trên SynSQL 3,336 dòng (`g1`, `t1`) | 66.34 | 58.22 | -8.12 |
| Thêm SFT trên Spider (`g2`, `t2`) | 72.53 | 62.48 | -10.06 |
| Thêm DPO + NLL (`g3d`, `t3d`) | 74.47 | 65.09 | -9.38 |

Các chi tiết quan trọng:

- Base student SQL-only 59.19. `t1` 58.22 nên CoT SFT chưa vượt được base.
- `g2` học đủ 8,659 câu Spider; `t2` chỉ học 6,622 câu có rationalization được
  nhận. Chênh lệch -10.06 không phải contrast chỉ đổi CoT trên cùng dữ liệu.
- CoT mất nhiều nhất ở câu JOIN (-13.5) và GROUP BY (-13.7); câu không JOIN -6.7.
- Trong 157 câu chỉ `g3d` đúng, `t3d` chạy được nhưng sai kết quả 98 câu và sai tên
  cột hoặc bảng 55 câu.
- Theo độ dài output của `t3d`, từ ngắn đến dài, khoảng cách là -8.5, -4.2, -11.2,
  -13.5. Câu dài cũng là câu khó (`g3d` giảm từ 89.5 xuống 62.9), nên đây là tương
  quan.
- Target SynSQL có đoạn "Reasoning Trace" lặp lại sau SQL, và 259/3,336 dòng nhắc đến
  reference solution. Phần sau SQL chiếm 13.6% output của `t3d` (p50).
- Sampling trên train (K=8): `t2` pass@8 88.58, câu có cả đúng lẫn sai 54.67%; `g2`
  pass@8 97.17, mixed 25.08%. CoT đa dạng hơn, nên voting có thể giúp CoT nhiều hơn.
  Voting chưa được đo trên dev.

P2.57 (chưa publish; số từ bảng trên server), không train:

| Đo | Teacher 7B | Base student 1.5B |
|---|---:|---:|
| SynSQL, thấy gold (rationalize) | 91.33 | 75.33 |
| SynSQL, không thấy gold (solve) | 52.33 | 19.00 |
| Spider dev, CoT so với SQL-only | 75.73 so với 76.89 | chưa đo |

Lịch sử: các CoT trước đều dùng student cũ Qwen2.5-1.5B-Instruct. P2.10 (QP-CoT
template ở client, CoT lúc inference) Spider 56.38 so với 62.57 SQL-only. Plan phụ
trợ (plan chỉ lúc train, inference SQL-only): P2.14 +1.84 sau round private trên
1,000 dòng, P2.15 `dss` -0.97 và `goldplan` -0.97 trên toàn bộ dữ liệu.

## 4. CoT có hơn SQL-only không?

Chỉ các bài có cả hai dòng trên cùng model mới trả lời được câu này:

| Bài | Model, cách train | Điều kiện đo | SQL-only | CoT |
|---|---|---|---:|---:|
| RetrySQL | OpenCoder 1.5B, chuỗi step | BIRD, gold schema links, beam sampling | 37.48 | 54.71 |
| Think2SQL | Qwen-Coder 3B, SFT | BIRD, weighted EX, localized relevant schema | 42.7 | 46.0 |
| OmniSQL | Coder 7B, Spider + BIRD | Spider dev / test, greedy | 76.9 / 80.7 | 80.3 / 86.6 |
| ExCoT | LLaMA 70B, SFT | Spider test | 83.00 | 81.42 |
| ExCoT | LLaMA 70B, SFT | BIRD dev | 62.03 | 58.14 |
| Struct-SQL | Qwen3 4B, LoRA r64 | BIRD mini-dev | 34.30 | 36.90 tự do, 45.00 có cấu trúc |
| P2.58 | Coder 1.5B, LoRA r16 | Spider dev, greedy, full schema | 72.53 | 62.48 |

Lưu ý khi đọc bảng:

- Struct-SQL: dòng SQL-only (FN-Gold) train trên 9,000+ dòng và eval với prompt
  QP-CoT; hai dòng CoT chỉ có 1,000 dòng.
- Kết quả dương lớn nhất nằm ở BIRD và dùng gold schema links, tức đã loại phần chọn
  cột mà P2.58 sai 55/157 câu.
- Không có dòng SQL-only cho Qwen trong RetrySQL. Với Coder 1.5B chỉ có 36.78
  zero-shot và 55.96 reasoning trên BIRD. Trên Spider chỉ có 73.25 reasoning sạch và
  77.18 khi thêm retry; trên BIRD retry gần như không đổi (55.96 so với 55.65 và
  56.36).
- Các kết quả 1.5B được trích từ ba bài sau dùng sampling hoặc voting: SLM-SQL 16-64 samples,
  FINER-SQL 30 candidates, RetrySQL beam. Ở 0.5B, FINER báo greedy khoảng 35 và
  voting khoảng 49. SLM-SQL 1.5B Spider dev: SFT với 16 samples 74.53, gần `g3d`
  SQL-only greedy 74.47 (khác data, không paired). SLM-SQL không có dòng SQL-only.

Mức chênh của mình (-10.06) lớn hơn nhiều so với mức âm của ExCoT (-1.58 đến -3.89).
Phần chênh này là thứ cần giải thích.

## 5. Vì sao CoT của mình thua?

| Giả thuyết | Bằng chứng | Đánh giá |
|---|---|---|
| Target quá dài với 1.5B | Li et al.: dài 27.0, ngắn 34.2 ở Qwen 1.5B (toán). Chen et al. phân biệt granularity với length; Skip-Thinking đề xuất học theo chunk | Đáng kiểm trước; chưa xác định là nguyên nhân chính trên SQL |
| Target nhiễu | SLM-SQL bỏ phần sau SQL, bỏ dòng lặp SQL. Target của mình còn cả hai | Có thật; tỷ lệ 13.6% token không đo được tác động lên EX |
| Writer/prompt không phù hợp | Khoảng cách -8.12 đã có ở stage 1 với CoT SynSQL. LLM đã viết target không đồng nghĩa target phù hợp student | Chưa tách writer khỏi format và filtering |
| Thiếu epoch | Thí nghiệm toán của Li et al. không cải thiện đủ khi tăng 2 lên 5 epoch; P2.58 không lưu checkpoint từng epoch | Chưa loại trừ trên SQL; cần đường EX theo epoch, không chỉ CE |
| Learning rate | Li et al. (full fine-tune): 1e-4 .133, 1e-5 .276. Literature dùng 2e-5 đến 5e-5 full, Struct-SQL LoRA 1e-4. Mình LoRA 2e-4 | Chưa kiểm, một arm là đủ |
| Ít dữ liệu | SLM-SQL 916K, FINER 37.6K, SCoTD 30 CoT mỗi câu (+5 đến +11). Nhưng RetrySQL 8.6K-9K và OmniSQL Spider + BIRD vẫn dương | Một phần; không đủ budget để nhân |
| Mất coverage private | `t2` bỏ 23.52% câu Spider còn `g2` giữ đủ | Confound trực tiếp; giữ gold supervision cho các câu chưa có CoT hợp lệ |
| Greedy | Mục 4 và độ đa dạng ở mục 3 | Chưa đo. Voting làm tăng chi phí inference của SLM |

## 6. Teacher có đóng góp gì riêng?

**Bằng chứng ngược chiều:**

- Li et al.: Qwen 1.5B teacher lớn 32.2, teacher nhỏ 33.0; 3B 39.7 và 39.4.
- Chen et al.: teacher mạnh hơn không phải lúc nào cũng cho student tốt hơn.
- RetrySQL: input duy nhất của prompt tạo step là gold SQL (Figure S3), không có
  question hay schema. Các step là thao tác theo thứ tự thực thi, gần với thứ template
  làm được.
- ExCoT (Table 2): một round GPT-4o rồi hai round tự sinh đạt BIRD 68.51, Spider 86.59;
  ba round tự sinh đạt 67.08 và 86.21. Đây là so sánh gần nhất trong Text-to-SQL: teacher
  thêm rõ hơn trên BIRD, rất ít trên Spider, và ở DPO trên model 70B.
- FINER-SQL không có ablation teacher. SLM-SQL không tách. Struct-SQL không so với
  self. Trong đợt search này không thấy bài Text-to-SQL nào chỉ đổi writer của rationale
  khi SFT model nhỏ.

**Bằng chứng hỗn hợp, sát cấu trúc FL của mình nhất:** SERT (GPT-2, QA) so reasoning
tự sinh đã lọc với reasoning của GPT-3.5. Trên StrategyQA, GPT-2-large: fine-tune 53.57,
teacher 50.22, tự sinh 55.75, cả hai 57.21. Trên CommonsenseQA: 20.88, 22.93, 22.63,
26.03. Kết hợp cao nhất ở cả sáu ô; riêng teacher có thể thua cả fine-tune. Bài này khác
task và model rất nhỏ, nhưng gợi ý cặp "teacher ở server, tự sinh ở client" đáng thử.

**Bằng chứng cùng chiều:**

- FedCoT: rationale từ server nâng model client trên bài trắc nghiệm, ví dụ Qwen1.5
  0.5B CQA 55.7 lên 58.6 (có privacy) và 59.3 (không privacy). Standalone là baseline
  gần nhất; bài không có control self hoặc template, và chỉ có một client.
- P2.57: trên SynSQL, teacher solve 52.33, base student 19.00.
- Dự án: soft label của teacher có edge trên Spider không do softening (F13, F15, F20).

**Điểm phân biệt có thể có:** template chỉ diễn lại SQL. Teacher có thể nói vì sao
chọn cột, JOIN qua khóa nào, khi nào cần DISTINCT hoặc GROUP BY. Đó đúng là các nhóm
CoT thua nhiều nhất ở mục 3. Target ngắn nên chứa các quyết định này, vì nếu chỉ là
step diễn lại SQL thì teacher không có lý do tồn tại.

**Giới hạn:** phần lợi ích này phải đi qua được bước private. P2.15 cho thấy edge ở K
có thể mất sau A (`dss` +1.35 xuống -0.97), và F14 cho thấy round private bào mòn phần
đã học ở server.

## 7. RL

| Bài | Cấu hình | Kết quả |
|---|---|---|
| SLM-SQL | GRPO, 6 rollouts, lr 3e-6, 1 epoch, reward EX + 0.1 format, RL trên BIRD | Spider 1.5B, 16 samples: dev 74.53 lên 75.15, test 77.35 lên 78.42. BIRD: bỏ RL 62.91, đủ 67.08 |
| FINER-SQL | GRPO, 32 rollouts, lr 8e-6, khoảng 2000 step, reward thêm memory và atomic | BIRD 1.5B 59.4 lên 63.1. Bỏ cả hai reward phụ -2.16 |
| Arctic-Text2SQL-R1 | GRPO từ checkpoint OmniSQL, 16 rollouts, reward 1 / 0.1 / 0, cụm 64 H100 | 7B BIRD dev 68.9, Spider test 88.8, greedy. Nhỏ nhất là 7B |
| Think2SQL | GRPO reward QATCH | 3B BIRD: SFT 46.0, RL 50.0, SFT + RL 48.2. Spider 3B: 77.0, 77.0, 77.2. 1.5B RL từ zero-shot 27.5 lên 44.2 |
| ExCoT | DPO, 1 round off-policy (GPT-4o) rồi 2 on-policy, 32 candidates | Spider 70B CoT: SFT 81.42, off-policy 82.49, on-policy 86.59 |
| Schema-R1 | 200 CoT cold-start rồi GRPO | Schema linking 1.5B: baseline 75.0 / 42.43, cold-start 70.41 / 35.05, thêm RL 89.94 / 68.82 (Filtered Acc bảng / cột). Không có EX |
| Xiong et al. | So thuật toán trên toán, Qwen 7B | RAFT 52.3, RAFT++ 56.1, GRPO 56.3, PPO 52.5, Iterative DPO 48.8 |
| P2.58 | DPO + NLL 1 round, K=8, 1,200 câu, lr 1e-5 | SQL-only +1.93, CoT +2.61 trên Spider dev |

Rút ra:

- **DPO hay GRPO chưa ngã ngũ.** ExCoT ủng hộ DPO, còn Xiong et al. xếp Iterative DPO
  thấp nhất trên toán. Mình có tín hiệu thực nghiệm với DPO, và có thể chạy theo từng
  stage riêng.
- **Rollout là chi phí lớn cần đo.** 6 rollouts x 8,659 câu x 2.62 s/output là
  khoảng 38 h nếu sinh tuần tự theo throughput cũ, chưa phải wall-clock của
  GRPO mới. Pilot có thể dùng subset; mức giảm nhờ target gọn phải đo lại.
- **Không chọn RFT hay PPO lúc này.** RFT âm của P2.58 bị lẫn với lr (2e-4 so với
  1e-5), nên chưa kết luận về RFT. Xiong et al. cho thấy lợi thế chính của GRPO là bỏ
  câu toàn sai, không phải normalize.
- **Schema-R1 gợi ý một vai trò nhỏ cho teacher:** CoT ít chỉ khởi động format, RL mới
  đem lại phần lớn gain. Vai trò đó có thật nhưng teacher khó được ghi công.
- **Reward:** bắt đầu từ execution correctness. Phần thưởng phụ của FINER đáng 2.16
  điểm ở 1.5B nhưng cần thêm memory bank.

SLM-SQL và FINER-SQL hỗ trợ GRPO ở đúng cỡ student; ExCoT và Iterative RPO
hỗ trợ cơ chế DPO ở model lớn hơn. Training gốc tương ứng cần 4 GPU 80 GB
(SLM-SQL), 2 A6000 48 GB (FINER-SQL), hoặc cụm H100 (ExCoT). Bảng inference
24 GB không phải bằng chứng GRPO training fit A5000. Ngược lại, P2.58 đã đo
DPO CoT peak reserved 14.43 GiB; số này áp dụng cho đường chạy cũ.

## 8. Federated

- Trong đợt search này không thấy bài federated Text-to-SQL nào với CoT hoặc RL. Trang
  awesomepapers gắn tag federated cho FINER-SQL, nhưng phần tóm tắt của bài không nói
  về federated.
- Federated Text-to-SQL không có CoT hay RL thì đã có: Zhang et al., ACL 2023 (Lorar,
  mỗi client là một dataset một domain).
- FedCoT là bài gần nhất về server LLM và client SLM qua rationale. Bài này một client,
  không gộp model, không có execution check.
- FedAvg + DPO giảm khi tăng client trong FedPDPO: IMDB 3 client 82.73, 10 client 76.45;
  Code-Vulnerability 3 client 93.49, 11 client 84.09 (DistilGPT2, không phải Text-to-SQL).
  Bài không có 5 client và không tách nguyên nhân cho từng con số. FedMOA và FedDPO
  trong OpenFedLLM cần được cite và đọc kỹ khi viết related work.
- Chi phí trong round private: rationalize toàn bộ 8,659 câu khoảng 5.8 h mỗi round với
  CoT hiện tại (P2.57), chưa tính train.

## 9. Chỉnh các claim đã nhận

| Claim | Thực tế |
|---|---|
| RetrySQL là bằng chứng trực tiếp teacher reasoning giúp 1.5B | Số đúng (37.48, 54.71). Đây là OpenCoder, gold links, beam sampling, full model 5 epochs. Bằng chứng cho recipe reasoning, không tách riêng format và kiến thức của GPT-4o |
| Teacher-CoT ở 1.5B đã qua mức ý tưởng | Đúng với "CoT giúp 1.5B" trong các điều kiện trên. Chưa có với "teacher tốt hơn writer yếu" |
| P2.58 chưa thử CoT của teacher 7B | Đúng. `t1` dùng CoT do LLM viết, có kiểm SQL cuối; chưa tách writer, prompt, format và chất lượng rationale |
| Bộ ba Gold, Self, Teacher trên public | Cần đi tiếp private/FL. Template bổ sung khi cần tách lợi ích khỏi việc diễn lại SQL; không bắt buộc mở bốn writer ngay từ pilot |
| Schema-R1 | Số đúng; student là Qwen2.5 (không phải Coder), metric là schema linking, không có EX |
| SLM-SQL: SFT 54.26 | Có trong Figure 1 của PDF đã xuất bản, cùng 61.95 sau RL và 67.08 sau CSC. Table 6 có số khác; không dùng nó để phủ nhận Figure 1. Các số này không phải bằng chứng greedy |
| ExCoT: SQL-only DPO tăng +2.2, gần `g3d` +1.93 (LAB_LOG trước) | Sai cách so. +2.2 là so với base 78.81, không so với SFT 83.00; dòng DPO no-CoT là 81.00, điểm khởi đầu không được nêu. ExCoT kết luận DPO không CoT chỉ có lợi nhỏ, còn `g3d` tăng so với SFT của chính nó |

## 10. Phương pháp nên thử (khuyến nghị 2026-11-01)

**Chọn CoT theo clause, kiểm SQL/schema, rồi execution-based Iterative DPO +
NLL.** Đây là lựa chọn ưu tiên về khả năng triển khai và bằng chứng hiện có,
không phải dự báo xác suất thành công. Nếu cần RL policy-gradient, chọn GRPO
làm nhánh tiếp theo từ cùng checkpoint CoT. Giữ Coder-1.5B và teacher 7B để
trả lời trực tiếp câu hỏi về teacher trong setup hiện tại.

### 10.1. Cơ sở chọn phương pháp

| Phương pháp | Phần nên lấy | Giới hạn quyết định thứ tự thử |
|---|---|---|
| [VCoT-SQL, EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2686.pdf), §3.1 | Teacher 7B tạo CoT theo clause; lọc SQL/schema và reference leakage | Student gốc 7B, không RL; chỉ lấy phần tạo target, không sao chép generator + validator + retriever |
| [RetrySQL, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/40556) | Reasoning và retry có bằng chứng trực tiếp ở 1.5B | Gold schema links và beam sampling; thử retry sau khi clean CoT đã học được |
| [SLM-SQL](https://aclanthology.org/2025.findings-ijcnlp.92.pdf) | Bỏ phần sau SQL và SQL lặp; recipe CoT SFT → GRPO ở đúng backbone | Dữ liệu 916K, training 4 × 80 GB; không lấy headline voting làm mục tiêu greedy |
| [ExCoT](https://arxiv.org/html/2503.19988v1) + [Iterative RPO](https://arxiv.org/html/2404.19733v3) | Sinh mới, execute, lập preference pairs, DPO + NLL | Bằng chứng gốc ở model lớn; ưu tiên ở đây vì P2.58 đã chạy được và có gain |

VCoT-SQL Table 3: Coder-7B gold SFT đạt 60.04 BIRD dev / 83.1 Spider test;
logic-order CoT chưa lọc 61.60 / 84.9; đã lọc 64.86 / 86.7. Các thiết lập
có schema filtering, và lọc CoT còn thay đổi dữ liệu được giữ. Đây là bằng
chứng cho recipe tạo target, chưa cô lập giá trị teacher hoặc dự báo gain
cho 1.5B. §3.1 kiểm final SQL EX và heuristic schema matching, không execute
từng bước reasoning dù abstract dùng cách diễn đạt mạnh hơn.

### 10.2. CoT sẽ trông như thế nào?

Teacher nhận **question + schema + evidence nếu có + gold SQL**, chỉ trên
public. Rationale giải thích các quyết định cần thiết: cột nào biểu diễn yêu
cầu, lọc ở đâu, đơn vị cần đếm, có cần DISTINCT/GROUP BY/subquery không, nối
qua khóa nào. Sau đó là một SQL cuối cùng, không có phần nhắc lại sau SQL.

Ví dụ nội dung mong muốn cho câu đếm sinh viên đã đăng ký từng môn:

```text
Count students per course, using course_id as the grouping key.
Join enrollment to course through enrollment.course_id = course.course_id.
Use COUNT(DISTINCT enrollment.student_id) to avoid counting repeat enrollments.
Return the course name and the count.
<final SQL>
```

Đây là ví dụ cho schema có các tên trên, không phải prompt dùng nguyên xi.
Mục tiêu ban đầu là khoảng **150–300 token rationale**, tùy độ phức tạp; đây
là lựa chọn của pilot, không phải optimum từ literature. Không cắt SQL hoặc
ép câu đơn giản mang đủ mọi clause. VCoT-SQL dùng few-shot; adaptation này
giữ teacher zero-shot để theo protocol hiện tại.

Kiểm target trước SFT: SQL parse được và khớp gold khi execute; tên bảng/cột
bám schema; không nhắc reference/gold; không có SQL hoặc giải thích lặp. Đọc
một mẫu phân tầng để kiểm liên hệ question → quyết định SQL. Khi chốt target
train với gold SQL chung giữa các arm, EX của SQL đó không còn là phép kiểm
độc lập cho rationale; không gọi rationale là đã được xác minh từng bước.

### 10.3. Đường đi qua public và private

1. **Public bootstrap:** pilot giữ 3,336 câu SynSQL của P2.58 để không đồng thời
   đổi pool. Tạo target theo format mới bằng teacher 7B. Kiểm khoảng 200 câu
   có đủ JOIN, aggregation, nested trước khi sinh cả pool; ghi throughput và
   coverage. SynSQL có database nhỏ nên EX cần đi cùng kiểm schema/nội dung.
2. **Private SFT:** mỗi client dùng student sau bootstrap để tự rationalize
   với gold tại chỗ, theo cùng format. Cách dùng đáp án để sinh rationale có
   nguồn từ [STaR](https://arxiv.org/abs/2203.14465); đây là adaptation, không
   phải chạy lại nguyên bản STaR. Câu không có rationale hợp lệ vẫn học gold
   SQL với prompt SQL-only riêng. Giữ đủ 8,659 câu, tránh lặp lại mất coverage
   của P2.58. Ghi tỷ lệ CoT hợp lệ và mức độ khó của phần còn lại.
3. **FedAvg sau private SFT:** đánh giá global adapter, rồi dùng nó làm điểm
   bắt đầu chung và frozen reference cho round DPO của các client trong arm.
4. **Private preference training rồi FedAvg:** student sinh CoT + SQL với
   prompt không chứa gold; execution tại client tạo chosen/rejected. DPO +
   NLL học trên completion. Client không có pairs giữ adapter đầu round;
   giữ cách tính trọng số FedAvg theo số private examples nhất quán giữa
   các arm. Teacher không nhận question, SQL, schema hoặc rollout private.
   Đánh giá adapter gộp. Sinh pairs mới từ checkpoint mới nếu thử iteration
   tiếp; lặp epoch trên pairs cũ không phải một iteration tự sinh mới.

Không cần tự rationalize lại toàn bộ private ở mọi round. Với pilot, cache
target SFT một lần cho mỗi arm; chỉ rollout preference được làm mới khi cần.
Giữ full schema và greedy khi đánh giá để so đúng mục tiêu triển khai.

### 10.4. Pilot nhỏ nhưng trả lời được câu hỏi

Ba nhánh, cùng base, public rows, gold SQL, private coverage, lịch optimizer
và downstream procedure:

| Nhánh | Target public | Điều cần biết |
|---|---|---|
| Gold | SQL-only | CoT recipe có đem lại giá trị so với học SQL trực tiếp? |
| Self-CoT | Base student tự viết cùng format compact | Có cần teacher 7B để tạo target tốt hơn? |
| Teacher-CoT | Teacher 7B viết cùng format compact | Đóng góp teacher còn sau private và FedAvg không? |

Hai nhánh CoT dùng cùng quy tắc giữ gold supervision khi rationale bị loại.
Gold giữ SQL-only xuyên suốt. Ở SFT, ghép cặp số lượt question/updates; target
CoT dài hơn nên vẫn phải báo token và thời gian, không gọi là compute-matched.
Ở DPO, dùng cùng question pool và rollout budget; số mixed questions, pairs
và updates có thể khác, phải báo riêng, không gọi là update-matched.
Template không cần thành arm thứ tư ngay. Thêm nó khi kết quả dương chủ yếu
đến từ target gần như chuyển SQL thành văn bản.

- **SFT:** bắt đầu 2 epoch public, lưu checkpoint mỗi epoch; LR đề xuất 5e-5
  cho LoRA, thấp hơn 2e-4 cũ. Đây là lựa chọn chưa đo, không suy LR full fine-tune
  của paper sang LoRA. Giữ LoRA r16 và `target_fp32`. Dùng cùng LR cho ba nhánh;
  nếu cần giải thích nguyên nhân cải thiện, thêm một contrast LR trên cùng
  target, không mở grid trước. Nếu train/dev EX còn tăng ở epoch cuối thì
  cân nhắc kéo dài từ optimizer checkpoint; CE thấp không đủ để quyết định.
- **Private:** chạy một round SFT cùng lịch local giữa các nhánh, rồi một round
  DPO + NLL. Không lấy `g2/g3d` centralized làm matched comparator cho endpoint
  FL; chúng là mốc tham khảo. Không yêu cầu CoT-SFT phải thắng SQL-only mới
  được thử DPO: ExCoT cho thấy thứ tự có thể đảo sau preference training.
- **DPO:** giữ điểm khởi đầu P2.58: K=8, tổng 1,200 câu private phân bổ theo
  client, LR 1e-5, beta 0.1, NLL weight 1. Với nhánh CoT có tín hiệu, thêm
  NLL-only trên đúng chosen của các pairs, cùng LR/updates, để biết preference
  loss có giúp hơn chỉ học câu đúng không. RFT cũ không trả lời được contrast này.
- **Đọc kết quả:** greedy Spider dev theo checkpoint, Spider test cho endpoint
  được đưa ra đánh giá; test đã dùng để chọn không gọi held-out. Theo dõi cả
  train EX trên subset cố định, SQL/schema errors, coverage và inference tokens.
  Main claim cần xác nhận nhiều seed sau screen.

Contrast chính là Teacher-CoT − Self-CoT sau FL; Teacher-CoT − Gold cho biết
toàn recipe có đáng dùng. Teacher − Self gồm cả tác động lên coverage CoT và
preference pairs, chưa cô lập chất lượng rationale trên cùng accepted rows.
Một gain public hoặc DPO gain trên chính CoT chưa
trả lời đủ hai câu này. Nếu self và teacher gần nhau, kết luận là chưa thấy
lợi ích tăng thêm của teacher trong phép so đó, không phải teacher có effect
bằng zero.

### 10.5. Khi nào thử GRPO hoặc một CoT khác?

**GRPO là lựa chọn policy-gradient đầu tiên.** Dùng cùng checkpoint CoT,
reward EX + format nhỏ theo SLM-SQL; thử 4–6 rollouts, subset trước, rollout
và update tuần tự. Chưa thêm memory reward, atomic reward hoặc critic. Đường
chạy mới phải smoke long examples dưới khoảng 21.5 GiB và đo throughput;
chưa có số đo để cam kết training GRPO fit hai A5000. Nhóm toàn đúng hoặc
toàn sai không tạo advantage phân biệt nên cần ghi tỷ lệ này.

Nếu CoT sạch học được nhưng còn lỗi quyết định cục bộ, **RetrySQL là lựa chọn
CoT thứ hai**: thêm bước sai, dấu backtrack và bước sửa vào training targets.
Nếu chưa học được clean CoT thì thêm retry làm target khó hơn, chưa giải quyết
được vấn đề nền. [ReSQL](https://aclanthology.org/2026.findings-acl.1677.pdf)
cũng có reasoning sửa lỗi ở 1.5B LoRA, nhưng kết quả dùng hai lần sửa nên
không phải comparator single-pass của pilot này.

[VET](https://aclanthology.org/2026.findings-acl.1544.pdf) thực thi reasoning
bằng Python từng bước lúc inference, không phải CoT training cho 1.5B.
FINER-SQL thêm memory/reward và voting; Skip-Thinking thay cách train theo
chunk. Các hướng này có giá trị riêng nhưng chưa phải bước đầu tốt nhất khi
target quality và private coverage còn chưa được xử lý.

So với khuyến nghị 2026-10-31 trong LAB_LOG, thay đổi là đưa **teacher-CoT lên
làm thử nghiệm chính**, không ưu tiên chuỗi SQL-only iterative DPO rồi mới
thử CoT phụ. Lý do là mục tiêu paper cần đóng góp teacher, và có thêm nguồn
VCoT-SQL phù hợp teacher size. Không có bằng chứng đủ để gán phần trăm xác
suất thành công cho các hướng này.

## 11. Nguồn

Đợt 2026-11-01 đối chiếu các nguồn quyết định lựa chọn ở mục 10 bằng bản
published PDF khi có; các nguồn nền từ đợt trước vẫn được giữ bên dưới.
Đây là research brief phục vụ chọn thí nghiệm, không phải systematic review.

- Li et al. 2025, [Small Models Struggle to Learn from Strong Reasoners](https://arxiv.org/html/2502.12143v3), Findings ACL 2025
- Chen et al. 2025, [Unveiling the Key Factors for Distilling Chain-of-Thought Reasoning](https://arxiv.org/abs/2502.18001)
- Chen et al. 2025, [Skip-Thinking](https://arxiv.org/abs/2505.18642), EMNLP 2025
- Li et al. 2023, [SCoTD](https://arxiv.org/html/2306.14050v1), ACL 2023
- Li et al. 2022, [Explanations from LLMs Make Small Reasoners Better](https://arxiv.org/abs/2210.06726)
- [RetrySQL](https://ojs.aaai.org/index.php/AAAI/article/view/40556), AAAI 2026; [full text](https://arxiv.org/html/2507.02529v2)
- [SLM-SQL](https://aclanthology.org/2025.findings-ijcnlp.92.pdf), Findings IJCNLP-AACL 2025
- [VCoT-SQL](https://aclanthology.org/2026.emnlp-main.2686.pdf), EMNLP 2026
- [ReSQL](https://aclanthology.org/2026.findings-acl.1677.pdf), Findings ACL 2026
- [VET](https://aclanthology.org/2026.findings-acl.1544.pdf), Findings ACL 2026
- [Rationalization Models for Text-to-SQL](https://arxiv.org/html/2502.06759v1)
- [STaR](https://arxiv.org/abs/2203.14465), NeurIPS 2022
- [Iterative RPO](https://arxiv.org/html/2404.19733v3), NeurIPS 2024
- [FINER-SQL](https://arxiv.org/html/2605.03465v1)
- [Struct-SQL](https://arxiv.org/html/2512.17053)
- [Schema-R1](https://arxiv.org/html/2506.11986)
- [OmniSQL](https://arxiv.org/html/2503.02240v2)
- [ExCoT](https://arxiv.org/html/2503.19988v1), Findings ACL 2025
- [Arctic-Text2SQL-R1](https://arxiv.org/html/2505.20315), Findings ACL 2026
- [Think2SQL](https://arxiv.org/html/2504.15077)
- Xiong et al. 2025, [RAFT và GRPO](https://arxiv.org/html/2504.11343)
- [FedCoT](https://arxiv.org/html/2406.12403v2), Findings EMNLP 2025
- Zhang et al. 2025, [SERT](https://arxiv.org/html/2502.12744v1)
- Agarwal et al., [GKD](https://arxiv.org/html/2306.13649v3)
- Zhang et al. 2023, [Federated Learning for Semantic Parsing](https://arxiv.org/abs/2305.17221), ACL 2023
- [FedPDPO](https://arxiv.org/html/2603.19741), [FedMOA](https://arxiv.org/html/2602.00453v1), [OpenFedLLM](https://arxiv.org/pdf/2402.06954)
