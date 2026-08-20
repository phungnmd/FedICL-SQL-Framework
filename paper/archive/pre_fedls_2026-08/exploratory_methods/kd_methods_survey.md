# KD Methods Survey — 7B teacher → 1.5B student, Text-to-SQL

> Research note 2026-07-17. Câu hỏi: ngoài RKD/KID (từ [10]), còn phương pháp KD
> nào đáng áp dụng cho setup của mình — teacher Qwen2.5-Coder-7B-Instruct (frozen),
> student Qwen2.5-1.5B-Instruct (LoRA), distill server-side trên public pool P
> (BIRD train), 16 GB VRAM, teacher co-loaded 4-bit?
>
> Bối cảnh hiện tại: PoC đã chạy — RKD (RKL trên gold) provisional winner
> (LAB_LOG 2026-07-11 (2)). Note này khảo sát các họ phương pháp KD gần đây và
> đề xuất nâng cấp, xếp theo độ khả thi. Quyết định cuối vẫn ghi ở
> `system_architecture.md`.

---

## Ràng buộc của mình (đọc trước khi so phương pháp)

1. **Cùng tokenizer** — teacher và student đều Qwen2.5 family → white-box
   token-level KD dùng được trực tiếp, KHÔNG cần các phương pháp cross-vocab
   (DSKD dual-projector, universal-logit v.v.). Loại cả nhóm đó khỏi bàn.
2. **KD chạy server-side mỗi round** trên pool P cố định — nghĩa là mọi phương
   pháp "on-policy" có thể amortize theo round (generate 1 lần/round) thay vì
   per-step. Đây là lợi thế cấu trúc ít setup nào có.
3. **VRAM 16 GB**: teacher 4-bit (~5–6 GB) + student fp16 (~3 GB) đã co-load.
   Phương pháp nào cần thêm model thứ ba (discriminator, reward model) là gánh nặng.
4. **CoT direction đã drop** (2026-07-07, latency + scope) — rationale/CoT
   distillation chỉ vào Related Work, không vào method.
5. Ladder hiện tại: `central_ft` → `central_rkd` → `central_kid`. Mọi đề xuất mới
   phải là **một rung mới trên ladder**, không thay ladder.

---

## Họ 1 — Off-policy token-level KD (mình đang ở đây)

Distill trên sequence cố định (gold hoặc gold-corrupted), teacher chấm từng token.

| Phương pháp | Divergence | Data | Ghi chú |
|---|---|---|---|
| FKD (classic) | Forward KL | gold | Mode-covering → tệ cho SQL ([10] Table 2: ~57.3 vs RKD 60.1–62.7). Đã loại. |
| **RKD = arm `central_rkd`** | Reverse KL | gold | [10]. Provisional winner của PoC. |
| **KID = arm `central_kid`** | Reverse KL | ŷ (mask-fill 1 pass) | [10]. ŷ = xấp xỉ rẻ tiền của student-generated data — xem Họ 2. |
| DistiLLM (Ko 2024, arXiv:2402.03898) | Skew KL — mix α·student + (1−α)·teacher rồi mới lấy KL | gold hoặc student output | Gradient ổn định hơn RKL thuần khi hai distribution lệch xa. Drop-in thay `rkl_div_loss`. |
| TAID (2025, arXiv:2501.16937) | KL với target nội suy teacher↔student, tăng dần theo training | gold | Curriculum trong không gian distribution. Ý tưởng đẹp, gain nhỏ ở gap 7B→1.5B (gap không quá lớn). |
| ToDi / Entropy-aware (2026) | Chọn FKL/RKL **per token** theo entropy của teacher | gold | Insight: token "pivot" (keyword SQL, tên cột) cần RKL chặt; token filler chịu được FKL. Hợp SQL về mặt trực giác, chưa có số trên Text-to-SQL. |

**Đánh giá:** mình đã ở điểm tốt của họ này (RKL đúng hướng theo cả [10] lẫn
literature — mode-seeking hợp SQL vì đáp án gần như deterministic). Skew-KL là
ablation rẻ nhất nếu training bất ổn; không phải hướng mới.

## Họ 2 — On-policy KD: distill trên output do student tự sinh

Vấn đề mà họ này giải: **exposure bias / train-inference mismatch** — student học
trên sequence hoàn hảo (teacher-forced) nhưng lúc inference tự decode, lỗi compound.
Với SQL điều này đau đúng chỗ: một token sai (tên bảng, phép JOIN) phá cả query.

| Phương pháp | Cơ chế | Chi phí thêm |
|---|---|---|
| **GKD** (Agarwal, ICLR 2024, arXiv:2306.13649) | Student sample output của chính nó; teacher chấm token-level (JSD hoặc RKL); mix λ giữa gold data và student samples | 1 lần student decode / batch. Có sẵn `GKDTrainer` trong TRL. |
| MiniLLM (Gu, arXiv:2306.08543) | RKL qua policy gradient (REINFORCE) | Variance cao, cần nhiều trick (reward hacking, mix 0.2 teacher). Nặng, không đáng ở scale này. |
| DistiLLM-2 (Ko 2025, arXiv:2503.07067) | Contrastive: Skew-KL trên teacher output + Skew-RKL trên student output | Cần teacher decode nữa → đắt hơn GKD. |
| SKD — Speculative KD (ICLR 2025, arXiv:2410.11325) | Student propose token, teacher thay token bị rank thấp (kiểu speculative decoding) → data tự thích nghi giữa supervised và on-policy | Teacher decode xen kẽ mỗi bước sinh — đắt, cài phức tạp. |

**Insight quan trọng cho paper:** KID của [10] chính là **xấp xỉ một-pass của
on-policy data** — thay vì để student decode tự do (đắt), nó mask gold rồi cho
student điền 1 forward. Nghĩa là ladder của mình đã có sẵn trục "data càng gần
student policy càng tốt?": gold (`rkd`) → pseudo-on-policy (`kid`) → true
on-policy (GKD). Thêm rung GKD là câu chuyện tự nhiên, không phải bolt-on.

**Chi phí trong kiến trúc của mình:** on-policy per-step đắt (survey
arXiv:2604.00626 ước 2–47× off-policy), NHƯNG server-side round loop cho phép
**amortize**: đầu mỗi round, student aggregated sinh SQL trên P một lần (batch
generation, 1.5B sinh nhanh), rồi cả round distill trên batch đó. Teacher vẫn chỉ
1 forward/step như hiện tại. Không tốn VRAM thêm.

## Họ 3 — Execution-aware KD (đặc thù Text-to-SQL)

SQL có thứ mà BBH/math không có: **executor rẻ và khách quan**. Literature 2025
mới dùng execution cho RL/self-training, chưa ai gắn vào logit-level KD:

- ExeSQL (EMNLP 2025 Findings, arXiv:2505.17231) — execution-driven rejection
  sampling + DPO, self-taught, không dùng teacher logits.
- Reward-SQL (arXiv:2505.04671), EXPO-SQL, CAPER — process reward / RL theo
  clause, hướng RL không phải KD.
- Struct-SQL mới (arXiv:2512.17053, CanAI 2026) — distill CoT có cấu trúc theo
  execution plan, +8.1% so với CoT thường. Là CoT direction → mình đã drop,
  chỉ cite ở Related Work.

**Khoảng trống:** execution signal × white-box KD. Chưa thấy paper nào làm
"teacher logits chỉ đổ vào chỗ student thực sự sai khi execute". Đây là chỗ
mình có thể claim novelty nhỏ mà chi phí thấp (xem Đề xuất B).

## Họ 4 — Black-box / data-level distillation

Synthetic data từ teacher đóng (GPT-4 v.v.), knowledge-base injection
(arXiv:2605.22843), discriminator-based GAD. **Không hợp:** mình có teacher
white-box cùng vocab — bỏ logits đi dùng data-level là tự vứt tín hiệu mạnh nhất.
Chỉ liên quan nếu sau này đổi teacher đóng. Skip.

---

## Đề xuất — xếp theo (giá trị kỳ vọng / chi phí build)

### A. Rung `gkd`: on-policy hóa rung KID *(khuyến nghị chính)*

Thêm arm mới cạnh `central_kid`: student sinh ŷ bằng **autoregressive decode thật**
(thay vì mask-fill 1 pass), teacher chấm RKL trên ŷ đó, giữ nguyên `CE(gold) + RKL`.
Đúng công thức GKD với λ mixing (λ=0.5 gold/student mặc định của GKD).

- Build: nhỏ — thay hàm sinh ŷ trong `imperfect.py` bằng generate-per-round
  (cache ŷ theo round, không sinh per-step); loss giữ nguyên `rkl_div_loss`.
  TRL `GKDTrainer` làm reference, không cần dùng trực tiếp (trainer mình đã có).
- Đo được: `gkd − kid` = giá trị của true on-policy so với xấp xỉ 1-pass của [10].
  Chưa paper nào báo số này trên Text-to-SQL → bảng ablation có giá trị tự thân.
- Rủi ro: student 1.5B đầu training sinh SQL rác → RKL trên rác dạy điều vô nghĩa.
  GKD xử bằng λ-mix với gold; mình còn có executor để lọc (xem B).

### B. `exec-gated KD`: execution feedback điều phối on-policy KD *(novelty chính cho paper)*

Chồng lên A, tận dụng round loop server-side:

1. Đầu round: student aggregated sinh SQL cho mẫu trong P, **execute trên DB BIRD**.
2. So kết quả execute với gold execution:
   - Sinh **đúng** → mẫu này student đã ổn, CE nhẹ hoặc bỏ qua (tiết kiệm compute).
   - Sinh **sai** → đây là failure mode thật của policy hiện tại → teacher RKL
     đổ vào chính sequence sai đó (học từ lỗi của mình, như GKD) + CE trên gold.
3. Tỉ lệ đúng/sai per round còn là **curriculum tự nhiên**: đầu training gần như
   toàn sai (≈KID/GKD thuần), cuối training chỉ distill chỗ còn yếu (hard-example
   mining tự động, giảm cost theo round).

- Vì sao khả thi: BIRD train có sẵn DB + gold SQL; executor là sqlite, rẻ; sinh
  1 lần/round nên execution cost amortized. Không thêm model nào → VRAM giữ nguyên.
- Vì sao mới: ExeSQL dùng execution cho rejection-sampling + DPO (không logits);
  [10] dùng imperfect data nhưng mù execution; GKD on-policy nhưng mù execution.
  Giao điểm ba cái này trống. Với venue KBS/NCA/IEEE Access, đây là điểm
  differentiation cộng thêm bên cạnh federated framing (FedCoLLM không có gì
  tương tự).
- Rủi ro: signal sparse nếu student đúng quá nhiều/quá ít; cần probe nhỏ đo
  tỉ lệ execution-match của student 1.5B trên P trước khi build (kiểu E0.1).

### C. Skew-KL ablation *(rẻ, chỉ khi cần)*

Thay `rkl_div_loss` bằng skewed-RKL của DistiLLM (mix α=0.1 teacher vào student
trước khi KL). 1 dòng đổi loss. Chỉ làm nếu (a) reviewer hỏi, hoặc (b) RKL
training loss bất ổn khi chuyển sang on-policy data. Không phải contribution.

### Loại — có lý do

| Phương pháp | Lý do loại |
|---|---|
| MiniLLM policy-gradient | REINFORCE variance, engineering nặng, gain không hơn GKD ở scale 7B→1.5B |
| SKD token-interleave | teacher decode xen kẽ mỗi token — đắt, phức tạp, gain chính (data adaptivity) đã có ở B qua execution gate |
| CoT/rationale distill (Struct-SQL mới, CoT-SFT) | direction đã drop 2026-07-07 (latency); chỉ cite Related Work |
| Cross-tokenizer KD (DSKD…) | không cần — cùng Qwen vocab |
| Forward KL | [10] Table 2 đã bác; mode-covering sai bản chất với SQL |
| DPO/RL từ execution (ExeSQL, Reward-SQL) | đổi hẳn training paradigm sang preference/RL — ngoài scope KD framework; cite Related Work |

---

## Thứ tự làm (nếu advisor duyệt)

1. Probe: đo execution-match rate của student hiện tại (adapter tốt nhất từ PoC)
   trên sample của P — quyết định B có signal không. Rẻ (chỉ generate + execute).
2. Rung A (`gkd`) trên setup centralized PoC trước — so `gkd` vs `rkd` vs `kid`
   cùng data, cùng seed protocol. Nếu `gkd ≤ kid` thì dừng, giữ [10] recipe.
3. Nếu A thắng → B (exec-gate) cũng ở centralized, rồi mới mang direction thắng
   cuộc vào federated build.

## Bổ sung 2026-07-18 — KD trên pool nhiễu (BIRD gold): target-teacher consistency

> Bối cảnh: §3.2 gold-ban vừa hạ xuống provisional (LAB_LOG 2026-07-18 (2));
> arm quyết định `central_ft_then_kd_bird_gold` chưa chạy. Câu hỏi: RKD trên
> gold nhiễu hỏng vì đâu, literature có cách nào cứu không?

**Cơ chế — vì sao RKD-trên-gold cần teacher đồng ý với target.** Loss
`CE(target) + RKL(q‖p)` chỉ nhất quán khi `p` (teacher teacher-forced trên
target) đặt mass cao lên chính token của target:

- Target = teacher-text (`y_pub`): nhất quán **by construction** — text là mode
  của teacher. CE và RKL kéo cùng hướng.
- Target = BIRD gold: tại token teacher không đồng ý (gold là oracle không
  đáng tin — 52.8% Mini-Dev bị flag annotation issue, phạm trù rộng gồm cả
  mơ hồ, xem scope note §3.2 — cộng style lạ), CE kéo `q` về token gold, RKL kéo `q` về mode của
  teacher — **gradient conflict trong cùng một loss**. Gold càng nhiễu, vùng
  conflict càng rộng. Đây là giải thích mechanistic thống nhất cả E0.1 (CE
  thuần nuốt độc) lẫn dự đoán cho arm `bird_gold`.

**Literature — họ "selective/token-gated KD" xử đúng vấn đề này (2025–26):**

| Phương pháp | Cơ chế | Áp cho mình |
|---|---|---|
| SelecTKD (arXiv:2510.24021) | verify token rồi đánh trọng số — ưu tiên tín hiệu teacher confidence cao | template trực tiếp cho token-gating |
| ATKD / Self-Evolution KD | đo độ khó per-token (KL gap / teacher uncertainty), nới constraint ở token dễ, tăng guidance ở token khó | biến thể trọng số mềm |
| SpecKD (ICLR 2025, arXiv:2410.11325) | chỉ tính loss ở token được teacher verify — chặn học từ prediction nhiễu | cùng ý tưởng, cơ chế đắt hơn |
| "Teachable tokens" (on-policy line) | chỉ distill token mà corrective mass của teacher nằm trong support của student | tinh vi hơn, chưa cần |
| Reliability-gated multi-teacher (arXiv:2604.03192) | gate theo confidence + consistency | 1 teacher nên chỉ mượn framing |

Điểm chung: **gate/weight theo teacher-confidence**. Chưa thấy paper nào gate
theo đúng **CE↔RKL conflict** (teacher-vs-gold disagreement) — vì setting
"distill trên gold nhiễu của dataset khác" ít người gặp. Khe hở nhỏ có thể
claim nếu cần.

**Đề xuất, xếp theo chi phí:**

1. **Teacher-agreement pre-probe (không train, chạy trước R1.2):**
   teacher-forced trên 3 corpus — BIRD gold / `y_pub` / Spider gold — đo
   per-token top-1 agreement + ppl. Ra ngay: vùng conflict của BIRD gold lớn
   cỡ nào so với hai baseline. Dự đoán được kết quả arm `bird_gold` trước khi
   tốn một run train, và là figure pool-quality cho A3.
2. **Nếu muốn cứu gold — agreement-gated RKD:** tại token teacher đồng ý
   (top-1 == gold hoặc `p(gold) > τ`): giữ cả CE + RKL; tại token bất đồng:
   một trong ba policy — (a) bỏ cả hai, (b) CE-only (tin gold), (c) RKL-only
   (tin teacher — ở hàng gold sai thì teacher mới đúng). Cài rẻ: thêm mask
   per-token vào `rkl_div_loss`/`weighted_lm_loss`, không model mới, không
   VRAM mới. Đây là biến thể thứ ba cho R1.2 nếu hai arm đầu ra mù mờ.
3. **Row-level rẻ hơn:** lọc hàng theo teacher-ppl trên gold (superfiltering
   style) — thô hơn token-gating, chồng một phần lên exmatch filter đã có.
4. **Giữ nguyên default:** teacher-text `y_pub` = lựa chọn consistency-by-
   construction, khớp literature; gold chỉ đáng quay lại nếu probe 1 cho
   thấy vùng conflict nhỏ hơn dự đoán.

## Sources

- Survey on-policy distillation: https://arxiv.org/abs/2604.00626
- GKD: https://arxiv.org/abs/2306.13649 · MiniLLM: https://arxiv.org/abs/2306.08543
- DistiLLM: https://arxiv.org/abs/2402.03898 · DistiLLM-2: https://arxiv.org/abs/2503.07067
- SKD (speculative KD): https://arxiv.org/abs/2410.11325 · TAID: https://arxiv.org/abs/2501.16937
- KID [10]: https://arxiv.org/abs/2410.11371
- ExeSQL: https://arxiv.org/abs/2505.17231 · Reward-SQL: https://arxiv.org/abs/2505.04671
- Struct-SQL structured-CoT KD (2026): https://arxiv.org/abs/2512.17053
- KD low-resource Text-to-SQL (KB injection): https://arxiv.org/abs/2605.22843
- FKL vs RKL blogpost (ICLR 2025): https://d2jud02ci9yv69.cloudfront.net/2025-04-28-llm-knowledge-distil-157/blog/llm-knowledge-distil/
- Text2SQL pure FT vs pure KD (NAACL 2025 industry): https://aclanthology.org/2025.naacl-industry.5.pdf
