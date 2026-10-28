# FedLS-SQL: hướng paper

Cập nhật: **2026-10-28**. Owner chọn hướng này sau review của một cố vấn
ngoài (LAB_LOG 2026-10-28). Method, comparator, phép kiểm và wording của
từng claim nằm trong LAB_LOG: FREEZE 2026-10-26 và hai addendum 2026-10-28.
File này nói paper kể gì, có bảng nào, so với baseline nào, nộp ở đâu.
Bản proposal trước (2026-10-12) ở
[archive](../archive/directions_2026-10/direction_proposal_2026-10-12.md).

## 1. Câu chuyện

1. Client giữ Spider (private), server có teacher Qwen2.5-Coder-7B frozen
   và BIRD (public). Client chỉ gửi LoRA adapter; chỉ deploy SLM 1.5B.
2. Teacher distill vào SLM ở server trước FL (K2, Hinton). Kiến thức này
   bị quên trong các round FedAvg: BIRD 43.61 ở K2 còn 36.77 sau A1.
3. Client replay: mỗi client trộn một ít câu BIRD có target nén của teacher
   (top-50 token + tail) vào round private. Kết quả: BIRD giữ được (hơn
   `hinton_k2aaa` +6.25, hơn `k2plus_aaa` +6.98 trên dev), Spider không
   giảm.
4. Teacher đóng góp đo được ở BIRD (C2: hơn pipeline cùng dữ liệu nhưng
   không teacher +3.52; hơn replay gold +4.04). Trên Spider test seed 0,
   phần của teacher chỉ khoảng 0.5 điểm (C1 +0.56, C6 +0.47): teacher chỉ
   thấy BIRD, nên kiến thức riêng cho Spider đến student rất ít.
5. Framework hơn FedAvg trên Spider test (C7, seed 0 +1.68, p=.029), phần
   lớn nhờ public data ở server (`gold_k2aaa` - FedAvg +1.53).

## 2. Title và contribution

Working title (không dùng chữ "Novel"): *Keeping the Teacher's Knowledge:
Server-Side LLM Distillation with Client-Side Logit Replay for Federated
Text-to-SQL*.

1. Framework: teacher 7B frozen chỉ ở server, client 1.5B LoRA, chỉ deploy
   SLM; bảng communication.
2. Phát hiện forgetting: lợi ích public domain của server KD mất qua các
   round FedAvg (hình theo round, 3 seed).
3. Client-side teacher-logit replay, dựa trên DER (Buzzega et al., 2020)
   và distillation trên public data ở client (FedMD, Li và Wang, 2019);
   adaptation: target nén của LLM frozen chỉ chạy ở server, tính một lần,
   cho task sinh SQL.
4. Đánh giá chốt trước trên Spider test, 3 seed, question-clustered test,
   so với FedCoLLM-style và các control tách teacher, replay, vị trí.

## 3. Claim và khả năng giữ

Ước lượng của cố vấn trước seed 1-2, chủ quan. Wording từng trường hợp:
LAB_LOG.

| Claim | So sánh | Metric | Seed 0 | Khả năng giữ |
|---|---|---|---|---:|
| C1 | method > `gmixgold_k2aaa` | Spider test | +0.56 (p=.43) | khoảng 25% |
| C2 | method > `gmixgold_k2aaa` | BIRD dev, Spider không kém quá 2.0 | BIRD +3.52 | 75-80% |
| C3 | method > `hinton_k2aaa` | như C2 | BIRD +6.25, Spider test -0.33 | khoảng 95% |
| C4 | method > `k2plus_aaa` | như C2 | BIRD +6.98, Spider test -0.70 | khoảng 80% |
| C5 | method so với FedCoLLM-style | Spider test, BIRD dev | chưa chạy | |
| C6 | `hinton_k2aaa` > `gold_k2aaa` | Spider test | dev +2.12; test +0.47 | thấp sau seed 0 |
| C7 | method > FedAvg | Spider test | dev +6.48; test +1.68 (p=.029) | cao sau seed 0 |

- C6 và C1 báo đúng như đã chốt; nếu cả hai không significant, paper không
  claim teacher trên Spider, và teacher được trình bày qua BIRD (C2). Paper ghi C6, C7 được thêm sau khi đã thấy Spider test seed 0
  của 4 arm.
- Nếu C4 không đạt non-inferiority mà BIRD vẫn +7: viết thành trade-off
  ("train các row đó ở server cho Spider test cao hơn X nhưng mất Y
  BIRD"), bỏ câu "chỉ có ích khi trộn vào client round". C3 vẫn đủ để biện
  minh replay.

## 4. Bảng và hình

**Bảng chính** (mean ± std qua 3 seed, CI và p của paired test):

- Không privacy: base 1.5B, teacher 7B zero-shot, centralized Spider
  (`central`), centralized pooled (`central_mix`).
- Federated: `local` (trung bình, tốt nhất), FedAvg, FedCoLLM-style,
  public data sharing (`gmixgold_k2aaa`), server KD + FedAvg
  (`hinton_k2aaa`), method.
- Cột: Spider test EX, Spider-DK, BIRD dev EX, có dùng teacher không,
  communication mỗi client.

**Ablation:** `k2plus_aaa` (vị trí: cùng row train ở server); lưới
objective K2 × objective replay: `gold_k2aaa`, `gmixgold_k2aaa`,
`hinton_k2aaa`, `mixgold_k2aaa` (chỉ seed 0), method.

**Hình:** Spider và BIRD theo round (K2, A1, A2, A3) cho method,
`hinton_k2aaa`, `k2plus_aaa`, `gmixgold_k2aaa`, 3 seed; Pareto Spider-BIRD.

**Communication:** LoRA r16 trên 7 projection = 18,464,768 params, 73.9 MB
fp32 (36.9 MB bf16) mỗi client mỗi chiều mỗi round; replay target khoảng
16.6 KB mỗi row, khoảng 33 MB mỗi client cho subset 2,000 row, gửi một lần.

**Appendix:** Realistic, SYN, test-suite EX; số từng seed và sensitivity
seed 1-2; selection record (17 cấu hình, số dev); virtual teacher và
self-teacher; top-50 so với full target; replay lọc theo execution (âm);
reverse roles (giới hạn); loại lỗi; GPU-h.

**Ngoài paper:** SynSQL (P2.54) giữ số seed 0 làm tham khảo; không có EX
trên SynSQL nên không kiểm được claim retention.

## 5. Baseline

| Mức | Arm | Lý do |
|---|---|---|
| Bắt buộc | base, teacher zero-shot, `local`, FedAvg, `central_mix` | bài cùng loại đều có (FedCoLLM, FedMKT, ACL 2023) |
| Bắt buộc | FedCoLLM-style | prior gần nhất |
| Bắt buộc | `gmixgold_k2aaa`, `hinton_k2aaa` | tách teacher và replay |
| Nên có | `k2plus_aaa`, `gold_k2aaa`, FedNTD (appendix, seed 0) | vị trí; teacher ở K2; baseline chống forgetting trong FL |
| Không chạy | FedProx, SCAFFOLD, FedOPT | method không phụ thuộc aggregator; FedProx đã âm |
| Không chạy | FedMKT reimplement | cho model khác nhau và mutual KD |
| Không chạy | TAID, SeqKD làm dòng riêng; teacher lớn hơn | đã thử hoặc vượt compute |

## 6. Rủi ro khi review và cách trả lời

1. Winner's curse: ghi 17 cấu hình đã thử trên dev; claim chỉ từ test 3
   seed chốt trước; sensitivity seed 1-2.
2. "Teacher không giúp task private": C6; vai trò retention; hình Pareto.
3. "Train thêm BIRD thì BIRD tăng": `k2plus_aaa` và `gmixgold_k2aaa` dùng
   cùng row, cùng số bước.
4. "Client giữ Spider, sao quan tâm BIRD": giữ năng lực ngoài federation là
   mục tiêu đã có trong FL và fine-tuning (participation gap, Yuan et al.,
   ICLR 2022; Lin et al., 2023; SDFT, ACL 2024; FedNTD; FedBE). Ghi rõ:
   BIRD dev cùng kiểu với pool của server, nên đây là giữ public domain mà
   server đã trả công học; Spider-DK, Realistic, SYN gần như không đổi.
5. Novelty: bảng related work
   ([novelty matrix](RELATED_WORK_NOVELTY_MATRIX.md)); không dùng "first".
6. Chỉ 3 round, 5 client: hình theo round; FedAvg đã chững (A2 68.28, A3
   67.60); framing cross-silo.
7. Một cặp benchmark: reverse roles trong appendix; một đoạn limitation.
8. BIRD dev vừa chọn vừa claim (BIRD test không công khai): sensitivity
   seed 1-2.
9. Privacy: "structural isolation", không claim DP; client nhận public row
   và target của teacher, không dữ liệu private nào rời client.
10. FedCoLLM-style không đúng bản gốc: gọi là "-style", nêu teacher frozen,
    một chiều, và lý do compute.

## 7. Chạy gì tiếp

Theo thứ tự; lệnh trong [PIPELINE_NEXT](PIPELINE_NEXT.md):

1. Phần còn lại của reference rows seed 0 (P2.53 step 1c: `central_mix`,
   `central`, base, FedNTD, `local`), cho bảng chính. FedAvg và
   `gold_k2aaa` đã xong; evaluator giống nhau ở mọi dòng.
2. Seed 1-2 cho các arm đã chốt và FedCoLLM-style (khoảng 80 GPU-h).
3. FedAvg và `gold_k2aaa` seed 1-2 (khoảng 8 GPU-h mỗi arm), cần thêm code.
4. Eval dev ở A1, A2 cho 4 arm ở seed 1-2 (khoảng 5 GPU-h); teacher
   zero-shot trên Spider test (khoảng 1 GPU-h, smoke VRAM trước).
5. Analyze 3 seed (C1-C7, sensitivity).

Không chạy: E2 (student 0.5B, bỏ); E1 (alpha 0.5) và replay ratio để dành
cho revision; seed của SynSQL và reverse roles; mọi thăm dò mới trên dev.

## 8. Venue

Kiểm lại quartile trên SJR và JCR lúc nộp:

- Data & Knowledge Engineering (SJR Q2, JCR Q3).
- International Journal of Data Science and Analytics (JCR Q3).
- Neural Processing Letters (SJR Q2, JCR Q3).
- Distributed and Parallel Databases (SJR Q2-Q3 theo ngành).
- Stretch: Journal of Intelligent Information Systems (Q2).
