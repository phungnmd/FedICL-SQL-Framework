# Fed-ICKD v2 — Proposal (2026-07-11)

> **Trạng thái: MERGED + LOCKED (2026-07-12) — user quyết, không cần advisor.**
> Cả 3 mục đã chuyển vào `system_architecture.md`: **V2-1** → §8.3, **V2-2** →
> §8.4 (cả hai PROPOSED, chưa build, arm ở §10 "Federated v2 extension"),
> **V2-3** → §3.2 (đã chốt trước). File này giờ chỉ còn giá trị lịch sử/nguồn
> gốc lý luận — đọc `system_architecture.md` cho trạng thái sống.

## Mục tiêu không đổi (Q3)

Framework Fed + ICL + KD hiệu quả cho SLM: student nhỏ (1.5B) đạt hiệu năng
cao gần teacher (7B) trong setting federated, chi phí serving thấp. Khung
hiện tại (client CE → FedAvg LoRA → server-side RKL distill trên pool công
khai P → gated-ICL inference) **giữ nguyên xương sống**. Proposal này nâng
cấp 3 slot bên trong khung, dựa trên 3 trend hội tụ của lit gần đây, và tất
cả đều tái dùng code đã có.

## Vì sao cần v2 — tình trạng sau PoC (data nội bộ)

- KD signal đã validate: `rkd − ft` = +6.09 EX, McNemar p=3.1e-07. Backbone đứng.
- KID (semi-imperfect-data) **thua** RKD ở chỗ ta (−1.45, p=0.072, 1 seed) —
  ngược headline của [10]. Nghi phạm số 1: mask-token `pad` chèn giữa câu là
  artifact không tồn tại trong pretrain distribution (LAB_LOG 2026-07-11 (2)).
- Retrieval sophistication không còn là contribution (question ≈ DAIL ≈ CodeS
  post-KD); claim #3 đã reframe sang usage-policy (gate). Gate = analysis
  contribution, không phải method headline.
- Pool `P`: TBD từ khi bỏ BIRD (2026-07-07) → **đã quyết 2026-07-12: BIRD train** (V2-3).
- Chưa có một số federated nào — trong khi title là *Federated*.

## Ba nâng cấp đề xuất

### V2-1. KD direction: thêm nấc **on-policy distillation** (thay thế tự nhiên của KID)

Lit: GKD (arXiv:2306.13649), survey on-policy distillation (2604.00626),
recipe thực dụng của Thinking Machines. Cơ chế: student tự sample trọn câu
SQL ŷ → teacher chạy **một forward duy nhất** lấy logprobs trên tokens của
student → reverse-KL per-token làm signal. Không cần reward model. Chi phí
9–30× rẻ hơn off-policy KD, 50–100× rẻ hơn RL (số của Thinking Machines).

Vì sao khớp ta:

- `train_online_kd` đã co-load teacher 4-bit + RKL + skew-RKL (§8.2). KID
  hiện tại (mask ρ=0.2 → student fill → splice) chính là "semi on-policy".
  **Full on-policy = thay `mask_rewrite` bằng student sampling trọn target**
  — sửa trainer nhỏ, cùng VRAM profile A5000, cùng loss code.
- Giải thích được luôn giả thuyết vì sao KID thua RKD ở ta: on-policy không
  có mask-token artifact (nghi phạm #1 biến mất theo thiết kế).
- Ladder mở rộng tự nhiên, mỗi nấc một ingredient:
  `rkd (off-policy, gold y)` → `kid (semi, masked-splice ŷ)` →
  `onpolicy (full, sampled ŷ)`.

### V2-2. Server distill: **execution-anchored** (filter/weight bằng SQL execution trên P)

Lit consensus 2025–26 cho SLM text-to-SQL = execution feedback:
SLM-SQL (2507.22478 — 1.5B đạt 67.08 EX BIRD dev bằng SFT+GRPO), FINER-SQL
(2605.03465 — dense execution reward, 1.5B thắng CodeS-7B), Arctic-Text2SQL-R1
(GRPO execution reward, SOTA BIRD), ExeSQL (execution-driven rejection
sampling).

Phiên bản khả thi cho ta (KHÔNG phải full RL):

- Trong bước server-distill: student sample ŷ trên câu hỏi của P → execute ŷ
  trên DB của P → chỉ distill (hoặc weight cao hơn) các sample chạy được.
- Hạ tầng có sẵn: SQLite exec + 60s progress-handler timeout trong
  `fedicl_sql/eval/metrics.py`. P phải có DB executable → xem V2-3.
- Đây là differentiator thật so với FedCoLLM [8]: họ distill mù trên public
  data; ta có verifier rẻ gắn vào từng sample. Tên gọi đề xuất:
  **execution-anchored server distillation**.
- Full GRPO: KHÔNG adopt — compute (N samples/query + reward pipeline trên
  A5000) và scope đều không cho phép. Ghi Tier-3 nếu cần trả lời reviewer.

### V2-3. Pool P = **BIRD train** (QUYẾT ĐỊNH user 2026-07-12)

> Bản gốc của proposal này đề xuất subset một mega-corpus synthetic. User
> quyết: **BIRD train** — số câu hỏi (~9.4k) tương đương Spider train (8.7k),
> gọn hơn mega-corpus synthetic; human-curated, reviewer quen mặt. Đảo quyết
> định drop BIRD 2026-07-07 *cho riêng vai trò pool P* (vẫn không dùng BIRD
> làm eval benchmark). Đã ghi vào `system_architecture.md` §3.2.

- Đáp ứng điều kiện V2-2: BIRD DBs là SQLite thật, executable.
- Khác distribution client data (Spider) → update-alignment rationale đứng.
- Caveat mang theo từ lần drop cũ (mitigated vì vai trò hẹp hơn):
  download đo được ~49 GB extracted (train/ 39 GB, gồm zip gốc 8.3 GB + zip
  nested dư 8.7 GB — xóa được sau extract; dev_20240627 1.7 GB không cần cho
  P). Tải 1 lần trên compute host, xóa zip sau khi verify extraction; field
  `evidence` — đã chốt+implement: drop khỏi mọi prompt trên P, giữ format
  khớp Spider (chi tiết + risk/escalation: `system_architecture.md` §3.2);
  không trộn trong một comparison; dialect gap — chấp nhận được vì P là
  distill corpus, không phải eval.
- **Kill-switch bắt buộc trước khi build distill loop:** probe E0.1 —
  1k BIRD-gold SFT từ base → eval Spider dev; nếu làm tụt floor Spider →
  escalate (fallback: Spider held-out 15%).

## Khuyến nghị kèm (ngoài 3 slot)

- **Student swap: Qwen2.5-1.5B-Instruct → Qwen2.5-Coder-1.5B-Instruct.**
  Toàn bộ SOTA SLM (SLM-SQL, CodeS, OmniSQL) dùng coder base. Model pair
  trong docs vẫn "not finalized" — swap trước khi build federation để khỏi
  rerun. Chi phí: rerun PoC arms (~vài giờ A5000). Kỳ vọng: vài EX miễn phí.
- **Gate giữ nguyên** (k=0 draft → exec → k=3 question-sim fallback) — đã
  verify 6/6 arms. CSC-SQL (2505.13271) = họ hàng đắt (N samples + voting +
  merge-revision model); cite làm related work, định vị gate là "cheap end
  of test-time scaling". Attribution control (A5 random) đã chạy 2026-07-11: repair = perturbation + exec-verify, gate đổi tên verifier-gated retry.
- **FedAvg giữ weighted nᵢ/n**; cite dòng FLoRA/LoRA-FAIR cho caveat
  A/B-averaging đã ghi 2026-07-06; stacking chỉ là fallback nếu A4 lộ drift.
  Không build trước.
- **Novelty slot còn trống:** không tìm thấy paper nào train federated
  text-to-SQL end-to-end (lit 2025–26 chỉ có privacy-masking inference kiểu
  MaskSQL). Giữ tốc độ.
- **Định vị honest:** không thi số tuyệt đối với centralized SOTA (SLM-SQL
  dùng RL + 310k synthetic). Claim = framework federated + analysis; cite họ
  làm centralized ceiling reference.

## Pipeline v2 đầy đủ (một vòng)

```
Round t:
  1. K=8 clients: QLoRA CE, train k=0 (không cần DAIL ở client)   [code có]
  2. Server: weighted FedAvg LoRA                                  [build nhỏ]
  3. Server distill trên P ⊂ BIRD train, ~300 steps:
       M_G sample ŷ trên câu hỏi P            (on-policy, V2-1)   [sửa trainer nhỏ]
       execute ŷ trên DB của P → filter/weight (V2-2)              [exec infra có]
       teacher Coder-7B 4-bit forward 1 lần → RKL / skew-RKL       [code có, §8.2]
Inference (client): k=0 draft → exec gate → k=3 question-sim       [code có, verified]
```

Ablation ladder federated (mỗi nấc một ingredient):

| nấc | thêm gì |
|---|---|
| `fedavg` | chỉ FedAvg, không teacher |
| `fedavg_pub` | + CE trên P gold (control: public data, không teacher) |
| `fedkd_rkd` | + teacher RKL off-policy trên gold của P |
| `fedkd_onpolicy` | + student-sampled ŷ thay gold |
| `fedkd_onpolicy_exec` | + execution filter/weight |

3 nấc đầu tái dùng logic PoC đã trả tiền. 2 nấc cuối = method contribution
chính của v2.

## Thứ tự build

1. **Probe P** (E0.1-style: 1k BIRD gold SFT → eval Spider dev) + **student
   coder-base PoC rerun** — 2 việc nhỏ, quyết định trước khi federate.
2. **FedAvg + server-distill RKD** (đường validate rồi, +6.09) → cặp số
   `fedavg` vs `fedkd` — sống còn của paper.
3. Nấc `onpolicy` + `exec-filter` như arm bổ sung sau khi ladder đứng.
4. Song song, GPU rảnh: seed 2 rkd/kid; Tier-3 rẻ (multi-retry gate, static-demos gate).
5. **Advisor bundle:** server-side pivot + claim-3 reframe + RKD pick + toàn
   bộ proposal này (V2-1/2/3 đổi §5.6/§9 → cần sign-off trước khi ghi vào
   `system_architecture.md`).

## Rủi ro chính

| rủi ro | đỡ bằng |
|---|---|
| BIRD↔Spider distribution/dialect gap làm distill lệch | probe E0.1-style trước, kill-switch rẻ; fallback Spider held-out |
| on-policy sampling chậm trên A5000 (student generate mỗi step) | sample trước theo batch/round (semi-online); teacher vẫn 1 forward |
| coder-base swap làm mất so-sánh-được với các run cũ | rerun trọn PoC ladder trên base mới, không trộn stack (hygiene rule cũ) |
| exec-filter bias về câu dễ (câu khó ít khi chạy được) | report thêm weight-mode (soft) bên cạnh filter-mode (hard); đo hardness mix của sample được giữ |
| 2 nấc mới ăn hết quỹ GPU trước khi có số federated cơ bản | thứ tự build ở trên: fedavg/fedkd trước, on-policy sau |

## Nguồn

- GKD — Agarwal et al., arXiv:2306.13649
- Survey on-policy distillation — arXiv:2604.00626
- Thinking Machines, "On-Policy Distillation" — thinkingmachines.ai/blog/on-policy-distillation
- SLM-SQL — arXiv:2507.22478 (IJCNLP-AACL 2025 Findings)
- FINER-SQL — arXiv:2605.03465
- Arctic-Text2SQL-R1 — Snowflake engineering blog + arXiv:2505.20315
- ExeSQL — EMNLP 2025 Findings
- CSC-SQL — arXiv:2505.13271
- BIRD (pool `P` mặc định, quyết định 2026-07-12) — Li et al., NeurIPS 2023, bird-bench.github.io
- FLoRA-style stacking aggregation — arXiv:2509.26399; LoRA-FAIR — arXiv:2411.14961
- MaskSQL (privacy-masking inference, không phải federated training) — arXiv:2509.23459
- Nội bộ: LAB_LOG 2026-07-11 (2)/(3); `system_architecture.md` §5.4/§8.2/§10
