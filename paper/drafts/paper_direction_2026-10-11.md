# Hướng paper FedLS-SQL từ 11/10/2026

Hướng đã chọn (owner, 11/10/2026): **hướng A**, tức paper empirical-method trên method v1,
cộng một screen ExST có giới hạn và vài screen nhỏ cho các hướng có thể làm paper mạnh hơn.
Proposal v2 ([method_v2_proposal_2026-10-11.md](method_v2_proposal_2026-10-11.md)) không còn là
hướng chính; ExST chỉ được nâng lên method chính khi qua đủ ba cổng ở mục 5.

Luật đọc kết quả ở file này là bản tóm tắt. Bản gốc, cố định trước khi có kết quả, nằm trong
[LAB_LOG](../notes/LAB_LOG.md) mục 2026-10-11. Lệnh chạy nằm trong
[PIPELINE_NEXT](../notes/PIPELINE_NEXT.md).

## 1. Paper nói gì

Một SLM 1.5B train federated trên dữ liệu Text-to-SQL private của các client, cộng với teacher
LLM frozen ở server trên public data, phục vụ được cả miền private (Spider) lẫn miền public
(BIRD). Chỉ LoRA adapter rời client; chỉ SLM được deploy.

Novelty nằm ở task và setting, không ở từng thành phần. Search 10/2026 không thấy công trình
federated Text-to-SQL nào có teacher LLM ở server. Tiền lệ gần nhất là Federated Semantic Parsing
(ACL 2023), không có teacher và không có public pool. Các thành phần (FedAvg LoRA, server KD,
execution filter) đều đã có; xem
[RELATED_WORK_NOVELTY_MATRIX](../notes/RELATED_WORK_NOVELTY_MATRIX.md).

| | Đóng góp | Bằng chứng đến 11/10 (seed 0) | Còn thiếu |
|---|---|---|---|
| C1 | Một SLM phục vụ cả hai miền | Hinton v1 − FedNTD: BIRD +18.97 (p<.001), Spider +1.45 [−0.89, 3.79]; pass luật `server_kd` | Seed 1, 2 |
| C2 | Teacher hơn public gold, nhất là robustness | Spider: +2.03 (P2.17), +2.42 (P2.18), +3.77 (P2.25), +1.35 (P2.27, ns). P2.27 DK +4.67 (p<.001) | Kiểm định gộp 3 seed |
| C3 | Cơ chế: Hinton KD làm miền private bị quên ít hơn gold CE trong stage public | P2.27 sau stage K: Spider +3.48 (K1, p=.002), +3.00 (K2, p=.013) | Seed; đo cùng cách ở 0.5B |
| C4 | Phân tích: heterogeneity, scale, headroom, lỗi theo loại SQL, chi phí | α=0.1 (P2.27), 0.5B và 1.5B, P2.28 headroom | α=0.5 ở 1.5B, `central`, `central_mix` 1.5B |

Bốn số C2 dùng chung test set nên không gộp được như bằng chứng độc lập; chỉ nói được là
hướng hiệu ứng nhất quán.

Câu chuyện C3 là cách đọc lại các số mà proposal v2 gọi là "round private làm mòn teacher":
khoảng cách Hinton − gold lớn ngay sau K vì gold CE làm Spider rơi nhiều hơn (K2: 60.54 so với
63.54), rồi round private đưa cả hai về trần khoảng 68-69.

Phân tích churn A1 (đã chạy 11/10, luật R2) ủng hộ cách đọc này:
- Trên BIRD, Hinton mất 26.1% số câu chỉ mình nó đúng ở K2; gold mất 31.9% số câu chỉ gold đúng.
  Không có xóa riêng phần của teacher (p=.38).
- Trên Spider, Hinton giữ tốt hơn (mất 15.7% so với 27.6%). Khoảng cách thu hẹp chủ yếu vì gold
  bắt kịp: gold A3 đúng 60.7% số câu Spider mà trước đó chỉ Hinton đúng.

## 2. Method

FedLS-SQL = các round private FedAvg LoRA ở client, xen kẽ stage K ở server: Hinton KD
(0.5 CE + 0.5 forward KL, T=2) từ teacher Coder-7B frozen trên 9,428 câu BIRD train. Schedule
AKAKA. Student Qwen2.5-Coder-1.5B-Instruct, 5 client theo split domain-cluster α=0.1.

Có giữ FedNTD ở round private hay không do P2.29 quyết (luật R1). Ở 1.5B, FedNTD so với FL
không giúp Spider (+0.19) và làm BIRD giảm (−1.37, p=.044). Nếu Hinton không NTD không thua
Hinton v1, bỏ NTD: method đơn giản hơn và FedNTD chỉ còn là baseline.

## 3. Bằng chứng nền (đã kiểm lại từ predictions đã publish)

P2.27, model cuối (A3), seed 0:

| Arm | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| base | 59.19 | 46.26 | 45.94 | 47.66 | 21.32 |
| FL A>A>A | 67.60 | 59.65 | 53.68 | 53.27 | 25.68 |
| FedNTD | 67.79 | 57.09 | 53.38 | 51.96 | 24.32 |
| gold v1 | 67.89 | 59.06 | 55.61 | 52.90 | 41.40 |
| Hinton v1 | 69.25 | 60.83 | 56.38 | 57.57 | 43.29 |
| teacher Coder-7B zero-shot | 76.69 | | | | 47.07 |

Luật P2.27 (cố định 10/10, trước kết quả): `server_kd` pass; `teacher` fail (Spider +1.35,
p=.23); `server_kd_spider_gain` fail (p=.26). Ghi đúng như vậy. Từ seed 1, claim teacher đánh
giá bằng kiểm định gộp 3 seed (luật R7), không đánh giá trên một seed.

P2.28 (G3, cố định trước): pass. pass@8 − greedy 13.0 / 17.8 / 13.7 điểm cho FL A2 / gold K2 /
Hinton K2; variant 65-77%. Số này đo trên câu train mà adapter đã thấy, nên là trần, không phải
dự báo cho dev.

## 4. Kế hoạch thí nghiệm

### Bắt buộc cho paper

| ID | Việc | Chi phí ước tính | Phụ thuộc |
|---|---|---|---|
| P2.28 publish | summary + 3 JSONL | không GPU | ngay |
| A1 | Churn trên predictions P2.27 (luật R2) | CPU | **xong**: R2 không được ủng hộ |
| P2.29 | `h_plain`: từ Hinton v1 K2, một round A3 plain, eval 5 bộ (luật R1) | khoảng 2-3 h, 1 GPU | runner mới, nhỏ |
| P2.31 | Seed 1, 2 cho FL, FedNTD, gold, Hinton (theo kết quả R1), central | khoảng 2 × 25 h wall clock trên 2 GPU | P2.29 |
| P2.32 | α=0.5 ở 1.5B: FL, gold, Hinton, central, seed 0 | khoảng 20 h | P2.29 |
| P2.33 | `central_mix` (Spider+BIRD) ở 1.5B làm ceiling | khoảng 7-10 h | không |
| A2 | Test-suite EX cho Spider (Zhong et al., EMNLP 2020) trên predictions đã có | CPU | tải test-suite DB |
| A3 | Lỗi theo loại SQL (JOIN, nested) và độ khó BIRD; chi phí truyền thông và teacher | CPU | không |

### Screen nhỏ, có điều kiện dừng cố định trước

| ID | Câu hỏi | Thiết kế | Chi phí | Pass thì | Fail thì |
|---|---|---|---|---|---|
| S1 = P2.30 | ExST có hơn train thêm bước trên gold không | Từ FL A2: A3[ExST] (k=8, T=0.7, m=4) so với A3 gold lặp cho bằng số bước (`fl_dup`); FL A3 đã có. Một cấu hình, không tune trên dev | sample khoảng 9-13 h (chưa đo) + 2 round train | Mở P2.35: `h_exst`, `h_dup` từ Hinton K2 | Đóng ExST; P2.28 vào paper như phân tích headroom |
| S2 = P2.34 | Gate KD theo execution ở server có giúp không | Như Hinton v1 đến A2, nhưng K1 chỉ distill logit teacher trên 5,319 câu teacher đúng, gold CE trên phần còn lại | khoảng 6 h | Đưa vào seed 1, 2 như biến thể | Đóng; ghi negative |

S2 chưa có nguồn trực tiếp cho việc gate logit KD theo execution; nếu dùng phải ghi là lựa chọn
của chúng tôi. Struct-SQL lọc target teacher theo execution, nhưng là SeqKD, không phải logit KD.

### Thứ tự GPU

1. GPU0: `central` P2.27 đang chạy; xong thì chạy bước publish P2.27.
2. GPU1 (đang rảnh): P2.29 khi runner xong.
3. Sau P2.29: GPU0 và GPU1 chạy P2.31, rồi P2.32 và P2.33. S2 chen vào khi một GPU rảnh. S1
   chạy cuối nếu còn GPU.

Tổng khoảng 130 GPU-h không tính S1, khoảng 1-1.5 tuần trên 2 GPU.

## 5. Khi nào ExST thành method chính

**Kết quả 11/10: cổng 1 không qua** (A1, mục 1), nên theo R5 ExST không thể thành method chính.
S1 vẫn có thể chạy như phân tích, nhưng xếp sau P2.31-P2.33; bỏ S1 cũng hợp lý nếu thiếu GPU.

Ba cổng (luật R5):

1. **Churn (R2) ủng hộ "round private xóa phần riêng của teacher".**
2. **`central` cho thấy FL thua central ít nhất 3.0 điểm Spider ở α=0.1 (R3)**, tức còn chỗ cho
   giảm drift.
3. **S1 pass (R4).**

Thiếu một cổng thì giữ hướng A; ExST chỉ xuất hiện trong paper như phân tích.

Lý do không làm ExST là hướng chính ngay:
- Execution chỉ xác nhận SQL tương đương gold, mà gold đã có trong tập train, nên ExST không
  thêm supervision; lợi ích chỉ có thể đến từ hiệu ứng on-policy.
- Output chỉ có SQL, nên biến thể chủ yếu là bề mặt (alias, thứ tự, `count(*)`). RFT có lợi
  trong literature nhờ nhiều đường suy luận CoT.
- Novelty yếu hơn proposal nói: PubSwap (arXiv 2604.12160) đã làm federated RLVR với LoRA và
  dùng response đúng để giảm client drift; FedMOA (arXiv 2602.00453) làm federated GRPO.
- Chi phí sample lớn: khoảng 9-13 h mỗi round mỗi arm, so với 1.6 h cho một round A.

## 6. Cách đọc khác và điều có thể làm hướng A sai

- **FL gần như không thua central ở α=0.1:** câu chuyện non-IID yếu đi; paper đặt trọng tâm vào
  C1 và C2, FedNTD/FedProx chỉ là baseline chuẩn.
- **Gộp 3 seed, teacher − gold Spider về 0 ở 1.5B:** C2 thu hẹp còn robustness (DK) và C3;
  thêm câu chuyện "teacher giúp nhiều hơn khi student nhỏ" (0.5B so với 1.5B).
- **Reviewer nói train trên BIRD thì BIRD tăng:** đúng, gold public cũng cho +15.7. Vì vậy C1
  luôn đi cùng gold control và `central_mix`; phần riêng của teacher là C2/C3.
- **Chỉ có họ Qwen:** ghi là limitation; chỉ thêm student khác họ nếu còn compute.

## 7. Việc cần làm

1. Publish P2.28.
2. Viết runner P2.29 (`h_plain`) và đưa lệnh vào PIPELINE_NEXT.
3. Viết runner seed cho P2.31 theo kết quả R1.
4. Sau khi `central` xong: publish P2.27, đọc R3.
5. A2, A3 (CPU) bất cứ lúc nào.
6. Chỉ khi còn GPU: trainer ExST cho S1; đo thời gian sample thật từ log P2.28 trước khi lên lịch.

Nguồn mới cho mục 1 và 5:
[PubSwap](https://arxiv.org/abs/2604.12160),
[FedMOA](https://arxiv.org/abs/2602.00453),
[AdaFD](https://arxiv.org/abs/2508.20557),
[Federated Semantic Parsing](https://aclanthology.org/2023.acl-long.678/),
[test-suite accuracy](https://aclanthology.org/2020.emnlp-main.29/).
