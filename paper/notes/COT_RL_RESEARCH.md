# CoT và RL cho FedLS-SQL: tổng hợp nghiên cứu

Cập nhật 2026-10-31. File này tổng hợp literature và kết quả của dự án về một
câu hỏi: server teacher có thể dạy student Coder-1.5B qua reasoning (CoT) không,
và RL giúp gì. Số của dự án là seed 0, EX (%), đã commit trừ P2.57 (ghi rõ bên
dưới). Quyết định và lệnh chạy không nằm ở đây: quyết định ở
[LAB_LOG](LAB_LOG.md), lệnh ở [PIPELINE_NEXT](PIPELINE_NEXT.md).

## 1. Kết luận

1. **Hình dạng của target có bằng chứng mạnh nhất.** Model nhỏ học tốt hơn với
   reasoning ngắn, bám thao tác SQL. Target hiện tại dài khoảng 566 token (p50)
   so với 23 token của SQL.
2. **Chưa có bằng chứng là teacher lớn hơn thì dạy reasoning tốt hơn ở cỡ 1.5B.**
   Nghiên cứu trực tiếp nhất (Li et al.) cho kết quả 32.2 (teacher lớn) so với
   33.0 (teacher nhỏ). RetrySQL, bài tích cực nhất, tạo step từ gold SQL, nên nó
   chứng minh giá trị của format nhiều hơn giá trị kiến thức của teacher.
3. **So sánh còn thiếu là teacher so với template.** Bộ ba Gold, Self-CoT,
   Teacher-CoT chưa đủ. Nếu một template không có LLM đạt mức của teacher, phần
   đóng góp của teacher bằng 0, và reviewer sẽ hỏi đúng điều này.
4. **Trên Spider, RL có ít dư địa khi model đã qua SFT.** Mức tăng lớn của RL nằm
   ở BIRD. `g3d` +1.93 của mình đã ở mức cao so với literature trên Spider.
5. **Teacher mạnh hơn student đã train không nhiều trên Spider.** Teacher zero-shot
   76.89 so với `g3d` 74.47 trên Spider dev. Trên SynSQL, teacher hơn base student
   33 điểm, nên lợi thế kiến thức có thật ở miền public khó hơn, nhưng còn phải
   chuyển được sang Spider.
6. **Chưa thấy bài nào khớp đồng thời** teacher frozen ở server, student LoRA,
   public data khác miền, client tự sinh và kiểm reasoning, và đo lợi ích sau FL.
   Đây vừa là khoảng trống novelty, vừa là phần không có recipe để sao chép.

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
| Think2SQL | Qwen-Coder 3B, SFT | BIRD, weighted EX | 42.7 | 46.0 |
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
- Các bài dùng CoT ở 1.5B đều dùng sampling hoặc voting: SLM-SQL 16-64 samples,
  FINER-SQL 30 candidates, RetrySQL beam. Ở 0.5B, FINER báo greedy khoảng 35 và
  voting khoảng 49. SLM-SQL 1.5B Spider dev: SFT với 16 samples 74.53, gần `g3d`
  SQL-only greedy 74.47 (khác data, không paired). SLM-SQL không có dòng SQL-only.

Mức chênh của mình (-10.06) lớn hơn nhiều so với mức âm của ExCoT (-1.58 đến -3.89).
Phần chênh này là thứ cần giải thích.

## 5. Vì sao CoT của mình thua?

| Giả thuyết | Bằng chứng | Đánh giá |
|---|---|---|
| Target quá dài với 1.5B | Li et al.: dài 27.0, ngắn 34.2 ở Qwen 1.5B (toán). Chen et al.: model yếu đạt đỉnh ở độ chi tiết vừa phải. Skip-Thinking: rationale dài làm gradient của token cốt lõi bị loãng | Mạnh nhất, kiểm rẻ |
| Target nhiễu | SLM-SQL bỏ phần sau SQL, bỏ dòng lặp SQL. Target của mình còn cả hai | Có thật, nhưng phần sau SQL chỉ 13.6% nên không đủ |
| Writer yếu | Khoảng cách -8.12 đã có ở stage 1 với CoT SynSQL, chưa có student viết. Teacher zero-shot CoT cũng không hơn SQL-only của chính nó (-1.16) | Khó là nguyên nhân chính |
| Thiếu epoch | Li et al.: CoT dài từ 2 đến 5 epoch vẫn .270 đến .286, ngắn .341 | Yếu |
| Learning rate | Li et al. (full fine-tune): 1e-4 .133, 1e-5 .276. Literature dùng 2e-5 đến 5e-5 full, Struct-SQL LoRA 1e-4. Mình LoRA 2e-4 | Chưa kiểm, một arm là đủ |
| Ít dữ liệu | SLM-SQL 916K, FINER 37.6K, SCoTD 30 CoT mỗi câu (+5 đến +11). Nhưng RetrySQL 8.6K-9K và OmniSQL Spider + BIRD vẫn dương | Một phần; không đủ budget để nhân |
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
- **GRPO với CoT dài quá tốn.** 6 rollouts x 8,659 câu x 2.62 s/output là khoảng 38 h
  sinh dữ liệu mỗi epoch. CoT ngắn sẽ giảm đáng kể con số này.
- **Không chọn RFT hay PPO lúc này.** RFT âm của P2.58 bị lẫn với lr (2e-4 so với
  1e-5), nên chưa kết luận về RFT. Xiong et al. cho thấy lợi thế chính của GRPO là bỏ
  câu toàn sai, không phải normalize.
- **Schema-R1 gợi ý một vai trò nhỏ cho teacher:** CoT ít chỉ khởi động format, RL mới
  đem lại phần lớn gain. Vai trò đó có thật nhưng teacher khó được ghi công.
- **Reward:** bắt đầu từ execution correctness. Phần thưởng phụ của FINER đáng 2.16
  điểm ở 1.5B nhưng cần thêm memory bank.

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
| RetrySQL là bằng chứng trực tiếp teacher reasoning giúp 1.5B | Số đúng (37.48, 54.71). Đây là OpenCoder, gold links, beam sampling, full model 5 epochs. Bằng chứng cho format, không tách được kiến thức của GPT-4o |
| Teacher-CoT ở 1.5B đã qua mức ý tưởng | Đúng với "CoT giúp 1.5B" trong các điều kiện trên. Chưa có với "teacher tốt hơn writer yếu" |
| P2.58 chưa thử CoT của teacher 7B | Đúng. Nhưng `t1` dùng CoT do LLM viết và gold-verified, nên là proxy gần: writer không phải lý do duy nhất |
| Bộ ba Gold, Self, Teacher trên public | Thiếu template, và thiếu bước Spider. Screen chỉ trên public từng không dự báo được sau round private (P2.14, P2.15) |
| Schema-R1 | Số đúng; student là Qwen2.5 (không phải Coder), metric là schema linking, không có EX |
| SLM-SQL: SFT 54.26 (đề xuất trước) | Không có trong bài. Table 6 có 54.17, nhưng bảng này tự mâu thuẫn (SFT + RL 50.59) |
| ExCoT: SQL-only DPO tăng +2.2, gần `g3d` +1.93 (LAB_LOG trước) | Sai cách so. +2.2 là so với base 78.81, không so với SFT 83.00; dòng DPO no-CoT là 81.00, điểm khởi đầu không được nêu. ExCoT kết luận DPO không CoT chỉ có lợi nhỏ, còn `g3d` tăng so với SFT của chính nó |

## 10. Hàm ý cho thiết kế

- Target teacher nên ngắn, theo từng quyết định SQL, kết thúc bằng gold SQL, không có
  gì sau SQL.
- Cùng câu, cùng gold SQL, cùng format, chỉ đổi writer: teacher, base student, template.
- Phải đi hết stage Spider với writer hợp lệ (student tự viết hoặc template), và so với
  `g2` chứ không dừng ở stage public.
- Nên có một arm kiểm lr.
- Khi có CoT cạnh tranh, đo voting cho cả CoT lẫn SQL-only, kèm chi phí inference.
- Nếu trao đổi format làm khoảng cách gần 0 nhưng template bằng teacher, đường CoT
  không mang được đóng góp của teacher. Khi đó vai trò teacher phải tìm ở chỗ khác, ví
  dụ SQL sai của teacher làm negative cho DPO (4,109 dòng BIRD có sẵn).

## 11. Nguồn

Đọc qua trích xuất HTML của arXiv (Chen et al. từ PDF), chưa đọc hết toàn văn từng bài.

- Li et al. 2025, [Small Models Struggle to Learn from Strong Reasoners](https://arxiv.org/html/2502.12143v3), Findings ACL 2025
- Chen et al. 2025, [Unveiling the Key Factors for Distilling Chain-of-Thought Reasoning](https://arxiv.org/abs/2502.18001)
- Chen et al. 2025, [Skip-Thinking](https://arxiv.org/abs/2505.18642), EMNLP 2025
- Li et al. 2023, [SCoTD](https://arxiv.org/html/2306.14050v1), ACL 2023
- Li et al. 2022, [Explanations from LLMs Make Small Reasoners Better](https://arxiv.org/abs/2210.06726)
- [RetrySQL](https://arxiv.org/html/2507.02529v2), AAAI 2026 theo đề xuất ngoài, chưa kiểm venue
- [SLM-SQL](https://arxiv.org/html/2507.22478v1)
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
