# Independent review, 2026-10-08

Provenance: one Opus subagent acting as an outside PhD data-science reviewer.
It was told to ignore project instruction files, memory and style directives,
and to read only [FACTS.md](FACTS.md) (numbers only, no project interpretation)
plus the raw paired summaries of P2.14-P2.18 (nested
`audits/protocol_v2/p21{4,5,6,7,8}_*/summary.md`). Full isolation was not
possible: `claude --bare` needs an API key, and this machine uses OAuth.
`hinton_k2aaa` (63.9) was unpublished when reviewed. The text below is the
reviewer's report, unedited apart from HTML entities.

---

# Đánh giá độc lập kết quả FedLS-SQL (federated text-to-SQL với KD từ LLM ở server)

Chỉ dựa trên `FACTS.md` và `raw/`. Kiểm tra prior work bằng web search (nguồn cuối bài).

## 1. Kết quả nào đủ vững để claim

| Finding | Bằng chứng | Đánh giá |
|---|---|---|
| **F1. Có stage public BIRD (gold hoặc Hinton) tốt hơn FL ở cùng số private pass** | 1.5B: gold − FL = +3.29/+3.68/+3.29 (2/3/4 pass, p ≤ .004); Hinton +4.06/+3.38/+3.00. 0.5B: +2.61 đến +5.61 (p .03 đến 3e-6). Cả 4 arm KD ở 0.5B đều dương | **Vững nhất.** Cùng dấu ở 2 student, 2 schedule, 2 objective; p rất nhỏ, sống sót Holm. Điều kiện: confound ở mục 5 |
| **F2. Robustness ngoài Spider dev tăng** | 0.5B: Syn +4.7 đến +7.1, Realistic +5.1 đến +6.3 so với centralized (p ≤ .014) | Vững, nhất quán 1.5B (Hinton AKAKA Syn 57.93 vs central 54.06) |
| **F3. Hinton > gold khi có HAI stage K tách rời (AKAKA)** | 1.5B: +2.03 (p=.033); 0.5B: +2.42 (p=.0199). Fisher gộp p ≈ .0055 | **Gợi ý, chưa chứng minh.** Seed 0, McNemar chỉ đo variance theo câu hỏi, không đo variance training seed. Holm trên 13 contrast Spider của P2.18: p=.0199×9=.18, không qua. Điểm cứu: lặp lại trên student khác |
| Hinton > gold với 1 K | 1.5B A>K>A: +0.09; A>K>A>A: −0.29; A>K>A>A>A: −0.29 (đều ns) | **Null.** Hai objective không phân biệt sau recover ở 1.5B |
| Schedule AKKAA vs AKAKA | Hinton +0.58 (p=.58), gold +1.64 (p=.10) | Noise |
| K2-first (`hinton_k2aaa` 63.9) | Chưa qua evidence check, log server, run bị interrupt/resume | **Không được dùng.** Hơn AKKAA 0.75 điểm, trong noise |
| "FL+KD vượt centralized" | 0.5B: Hinton AKAKA − central_e3 +3.19 (p=.025) | **Gây hiểu nhầm** (mục 5): centralized không có BIRD, và E2 (60.35) > E3 |
| seq, KID, plan, DSS, retention, merging | Tất cả ns hoặc âm ở endpoint cuối; plan +1.84 trên pool 1,000 dòng biến mất ở full pool | Null/âm. Báo cáo được như negative result |

## 2. Có đủ cho một METHOD paper?

**Hiện tại không.** Arm tốt nhất (Hinton AKAKA) là vòng "FL round → server KD (CE + KL) từ LLM xuống SLM aggregate trên auxiliary data". Đây chính là nửa SLM của FedCoLLM, bỏ phần mutual. Chỗ mới chỉ là domain (text-to-SQL) và public pool cross-benchmark.

Method claim chỉ đứng được nếu chứng minh tất cả:
- **Method:** "repeated server-side Hinton KD stages trên public cross-domain pool, mỗi stage có một private round theo sau".
- **Phải thắng:** (a) FL compute-matched (thêm round, FedProx); (b) gold CE cùng schedule (hiện +2.0/+2.4, seed 0); (c) một control regularization: label smoothing hoặc KL tới teacher yếu, vì Hinton = 0.5 CE + 0.5 KL nên cải thiện có thể do smoothing chứ không phải dark knowledge (Yuan et al., CVPR 2020); (d) K2-first, vì nếu K2AAA ≈ AKAKA thì interleaving thừa và "method" chỉ là public pre-training trước FL.
- **Còn thiếu:** ≥3 seed, control (c), central + BIRD baseline.

Kết luận thực tế: hướng tới **empirical/analysis paper**.

## 3. Pattern đang bị dùng chưa hết

**Quan sát:**
- **K kéo Spider về một mức gần như cố định:** sau K, Spider EX 0.5B là 46-48 (gold) và 50-53 (Hinton) bất kể điểm xuất phát (53.38 hay ~60). Do đó K thứ hai rơi sâu hơn (gold −11.41, Hinton −7.65) so với K đầu (−6.96 / −2.80).
- **Recovery cực mạnh:** một A sau K tăng +10 đến +13 điểm, trong khi một A của FL chỉ ~+2. Endpoint luôn cao hơn chuỗi chỉ A.
- **Hinton forget ít hơn trong K:** 0.5B −2.80 vs −6.96; 1.5B A>K 58.32 vs 55.03; 1.5B A>K>A>K 62.67 vs 58.03 (p=7e-5). Gold recover mạnh hơn sau đó, nên với một K khoảng cách bị xóa.
- **K liên tục 2 epoch forget ít hơn K 1 epoch** (0.5B gold 48.07 vs 46.42; Hinton 52.42 vs 50.58).
- **K thứ hai bằng gold vô ích ở 1.5B** (67.50 vs 67.89 của A>K>A>A), K thứ hai bằng Hinton có ích (+1.93, p=.035).
- **BIRD cũng bị forget đối xứng sau A cuối** (Hinton 35.53 → 28.88).
- **Chiều ngược** (BIRD private, Spider public): gold 20.73 < FL 22.88 < seq 24.45. Public gold gây hại, teacher target giúp.

**Giả thuyết (cần test):**
- Thiệt hại của K chủ yếu là format/distribution (prompt BIRD có evidence, style SQL), không phải capability, nên recovery nhanh.
- Lợi thế Hinton đến từ giảm drift trong K và chỉ tích lũy khi có ≥ 2 K.
- Teacher có ích hơn khi distribution public gold xa target (chiều ngược).

Bộ "forget-recover trajectory" này là phần phân tích giá trị nhất nhưng chưa được đặt ở trung tâm.

## 4. Rủi ro novelty

| Prior work | Trùng |
|---|---|
| FedCoLLM (arXiv 2411.11707; venue chưa xác minh) | LoRA SLM ở client, server làm mutual KD (SFT + KL) trên auxiliary data sau mỗi round. **Trùng gần hoàn toàn với AKAKA-Hinton.** Đánh giá trên QA, không có text-to-SQL |
| FedMKT (COLING 2025) | Mutual KD LLM-SLM trên public data |
| FedCoT (Findings EMNLP 2025) | CoT distillation LLM sang SLM trong FL; làm yếu hướng "CoT/plan KD" |
| FedDF (NeurIPS 2020); FSL "Federated Learning with Server Learning" (Mai et al.) | Server train hoặc distill trên proxy/server data giữa các round |
| Nguyen et al. ICLR 2023 "Where to Begin?"; STILTs / Pruksachatkun et al. ACL 2020 | Pre-training / intermediate-task trước fine-tune. Nếu K2-first thắng, đây là prior trực tiếp |
| Federated semantic parsing (ACL 2023, Lorar) | Đã có FL cho text-to-SQL (không LLM teacher). Không claim "first FL text-to-SQL" |

Phần còn lại có thể mới: setting text-to-SQL với public pool cross-benchmark, phân tích placement và forget-recover, negative results về seq/plan/CoT KD.

## 5. Confound và validity threat

1. **Exposure/compute:** arm KD có thêm 2 epoch BIRD (~4.6-5 GPU-h ≈ 3.7 round A) mà FL không có. FL bão hòa ở 1.5B 4 pass (64.80) giảm nhẹ lo ngại, nhưng 0.5B chưa có FL nhiều round. FedProx một mu, đang chạy.
2. **Centralized không công bằng:** không có BIRD, chọn E3 trong khi E2 tốt hơn. "Vượt centralized" thực chất là "có thêm data public vượt không có". Thiếu central + BIRD.
3. **Optimizer restart:** mỗi K/A reset optimizer và LR; AKAKA vs AKKAA lẫn số lần restart với placement (tương tự warm restart).
4. **K2AAA bị interrupt và resume:** không bảo đảm tương đương run liền mạch.
5. **Loss mode:** Hinton trước P2.17 dùng bf16, gold rerun fp32; riêng loss mode đã lệch −0.68. So sánh A>K>A trộn mode. Bằng ~1/3 hiệu ứng Hinton.
6. **Đổi student:** 1.5B-Instruct sang Coder-0.5B đổi cả size lẫn pretraining family (Coder cùng họ teacher). Không quy được hiệu ứng cho size.
7. **Một chiều public pool:** chiều ngược đảo kết quả của gold.
8. **Contamination:** Qwen2.5-Coder-7B có thể đã thấy Spider/BIRD khi pretraining (76.69 zero-shot). "Teacher knowledge" có thể là memorization benchmark.
9. **Federated yếu:** một dataset chia Dirichlet, FedAvg plaintext, không DP. Stage K không tương tác với thuật toán FL.
10. **Multiplicity:** hơn 200 contrast qua các screen, không có primary contrast pre-register, không correction.

## 6. Framing đề xuất và thí nghiệm tối thiểu

**Thesis:** *"Public-pool teacher distillation in federated text-to-SQL: what survives private fine-tuning, and where to place it."*

**Contributions:**
1. Protocol federated text-to-SQL (private Spider, public BIRD, frozen 7B teacher, 5 eval set, paired stats + multi-seed).
2. Một stage public bất kỳ cho +2.6 đến +5.6 Spider EX và +5 đến +9 Syn/Realistic so với FL ở cùng số private pass, ở 2 student; FL thêm round thì bão hòa.
3. Phân tích forget-recover: K kéo Spider về mức cố định, một private round recover và vượt; khác biệt objective sau một K bị xóa.
4. Soft-label KD chỉ vượt gold khi stage public được lặp lại (tùy E1, E4).
5. Negative results có hệ thống (seq, KID, plan/DSS, retention, merging, ICL).

**Thí nghiệm theo ưu tiên** (0.5B; tổng ≈ 120 GPU-h ≈ 2.5-3 ngày trên 2 GPU):

| # | Thí nghiệm | Cost | Kết quả đổi framing |
|---|---|---|---|
| E1 | Seed 1, 2 cho `fl_aaa`, `gold_akaka`, `hinton_akaka`, `gold_k2aaa`, `hinton_k2aaa`. Test có tính seed (mixed-effects logistic, hoặc bootstrap seed × câu hỏi) | ~78 GPU-h | Hinton − gold AKAKA đổi dấu ở bất kỳ seed nào hoặc mean < +1: bỏ contribution 4 |
| E2 | Hoàn tất `gold_k2aaa`, chạy lại `hinton_k2aaa` liền mạch (nằm trong E1) | trong E1 | K2AAA ≥ AKAKA: thesis thành "public KD một lần trước FL là đủ; per-round server KD kiểu FedCoLLM thừa", một claim phản biện có giá trị |
| E3 | Centralized + BIRD: K2 rồi 3 epoch Spider, gold và Hinton | ~18 GPU-h | FL+K ≈ central+K: claim "khi có public stage, federation gần như không mất gì". Dù sao cũng phải bỏ câu "vượt centralized" |
| E4 | Control regularization: AKAKA với gold + label smoothing (hoặc KL tới teacher yếu, cùng 0.5/0.5) | ~9 GPU-h | Nếu bằng Hinton: lợi thế là regularization, không phải teacher |
| E5 | FL compute-matched: `fl_aaaaaa` (6 round ≈ cùng GPU-h) + kết quả FedProx | ~8 GPU-h | Nếu FL đuổi kịp: F1 chỉ là exposure, paper mất finding chính |
| E6 (tùy chọn) | Chiều ngược ở 0.5B với schedule tốt nhất | ~10-15 GPU-h | Gold vẫn hại, Hinton/seq giúp: finding "teacher quan trọng khi public gold lệch distribution". Không chạy thì ghi limitation |

## 7. Kết luận

Ở dạng hiện tại, bộ kết quả **chưa publishable**, kể cả Q3, nếu đóng gói như method paper: mọi thứ đều seed 0, contrast duy nhất ủng hộ teacher (+2.03/+2.42) không sống sót multiplicity, arm tốt nhất về bản chất là phía SLM của FedCoLLM, và baseline centralized thiếu BIRD.

Phần thực sự vững (một public stage ở server cải thiện rõ FL text-to-SQL ở hai student, cùng trajectory forget-recover nhất quán) là chất liệu tốt cho một **empirical study**. Với E1-E5 (~3 ngày GPU), framing ở mục 6 đủ cho Q3 journal ứng dụng, dù E1/E2 nghiêng về hướng nào: Hinton thắng ổn định cho một contribution KD; K2-first thắng cho một phản biện cụ thể với các framework per-round KD. Không nên viết claim "method mới vượt SOTA" hay "vượt centralized".

**Nguồn:**
- [FedCoLLM, arXiv 2411.11707](https://arxiv.org/html/2411.11707v2)
- [FedMKT, COLING 2025](https://aclanthology.org/2025.coling-main.17)
- [FedCoT, Findings EMNLP 2025](https://arxiv.org/html/2406.12403v2)
- [Federated Learning with Server Learning, Mai et al.](https://arxiv.org/abs/2210.02614)
- [Where to Begin?, ICLR 2023](https://mlanthology.org/iclr/2023/nguyen2023iclr-begin)
- [Intermediate-Task Transfer Learning, ACL 2020](https://aclanthology.org/2020.acl-main.467/)
- [Federated Learning for Semantic Parsing, ACL 2023](https://ar5iv.labs.arxiv.org/html/2305.17221)
- [Flashback, arXiv 2402.05558](https://arxiv.org/pdf/2402.05558)
- [Struct-SQL, PMLR v318](https://proceedings.mlr.press/v318/thaker26a.html)
- FedDF (NeurIPS 2020) và Yuan et al. (CVPR 2020, "Revisiting KD via Label Smoothing Regularization"): từ hiểu biết sẵn có, chưa kiểm tra lại trong lần review này.

---

## Project notes on this review (added by the project, not the reviewer)

- The Fisher-combined p ≈ .0055 is not valid: both McNemar tests use the same
  Spider questions, so they are not independent.
- Holm over 13 Spider contrasts is strict; Hinton − gold at AKAKA was the
  planned replication target of P2.17 and can be argued as the primary contrast.
- The owner deferred seed replication (E1); without it, the teacher claim stays
  at "consistent direction on two students".
