# Báo cáo tiến độ FedICL-SQL — 07/07/2026

Chào thầy Hùng,

Tuần này em bị ốm nên chưa update được nhiều, chủ yếu tập trung vào phần thực nghiệm KD (knowledge distillation) — đang chốt lại cơ chế và code, chưa có số EX để báo cáo.

---

## Cập nhật hướng KD

Sau khi đọc kỹ lại KID [arXiv:2410.11371, EMNLP Findings 2024], em quyết định bỏ hướng Struct-SQL (CoT distillation) — quá phức tạp so với lợi ích. Thu hẹp lại còn **2 hướng, cả hai đều từ KID paper**, chạy online (teacher + student cùng load, 1 forward của teacher mỗi step):

- **RKD** — `L = CE(gold SQL) + RKL(q‖p)`, teacher chấm điểm trực tiếp trên gold SQL
- **KID** — cùng loss, nhưng trước khi chấm, student tự che (mask) một phần token gold SQL (tỷ lệ ρ=0.2, ngẫu nhiên) rồi tự đoán lại (1 forward, không cần backprop) tạo ra bản SQL "không hoàn hảo" `ŷ` — mô phỏng lỗi mà student hay mắc lúc inference (train/inference mismatch). Teacher chấm điểm trên `ŷ` này thay vì gold.

Ý tưởng: RKD là baseline đơn giản (KL trên dữ liệu sạch), KID thêm bước "làm bẩn" dữ liệu để dạy student cách tự sửa lỗi giống lúc suy luận thật — theo paper KID cho kết quả tốt hơn hẳn so với các phương pháp KD cũ (+3–6% EX so với SFT thường).

**Public dataset cho KD (BIRD hay dataset khác) vẫn để đó, chưa quyết định.** Trước khi chốt, em đang chạy 2 phương pháp trên ngay chính **Spider** để so sánh với FT thường: 3 arm từ base model — `central_ft` (fine-tune CE thường, baseline) vs `central_rkd` vs `central_kid`, cùng trên 1 tập data. Nếu `central_rkd`/`central_kid` vượt `central_ft` rõ ràng → tín hiệu KD thật sự có ích, mới đáng đầu tư tiếp cho pipeline đầy đủ (multi-client federation + public corpus).

**Đã xong tuần này:** code cho cả 2 hướng (loss RKL, bước mask+rewrite, teacher forward, training loop, CLI) — unit test pass hết. **Đang chạy** 2 phương pháp này trên Spider để lấy số so sánh với FT (cần GPU + load teacher 7B, máy em đang set up).

**Tuần tới:** chạy PoC trên compute host, lấy số EX cho 3 arm. Nếu KD cho kết quả khả quan (vượt `central_ft`), em sẽ thử kết hợp **ICL + KD** (liệu KD có cộng hưởng với ICL demo lúc inference không) và chạy các thực nghiệm compare giữa các kết hợp, hoặc bắt đầu xây pipeline đầy đủ (federation + public corpus) để thực nghiệm quy mô lớn hơn.

---

# Báo cáo tiến độ FedICL-SQL — 29/06/2026

Chào thầy Hùng,

Em cập nhật tiến độ tuần này. Tuần này có hai nội dung chính: (1) hoàn thành thực nghiệm tối ưu ICL bằng DAIL-SQL selection và (2) chốt lại kiến trúc distillation theo hướng KID (EMNLP 2024).

---

## 1. Kết quả ICL với DAIL-SQL Selection

Tuần trước ICL theo question-similarity retrieval không có contribution (+0.2pp trên base, −5.6pp trên model fine-tuned). Tuần này em thử DAIL-SQL selection [9] — vẫn retrieve bằng **question embedding similarity**, nhưng thêm bước **SQL skeleton quality gate** (chỉ giữ demo có SQL structure tương đồng với câu test), demo style `never_schema` (question + SQL verbatim, không có DDL). Kết quả toàn bộ đo trên **full test set Spider (n=1034, 1 seed, cross-schema, train-pool demos)**:

### Base model (Qwen2.5-1.5B-Instruct, chưa fine-tune)

| Config | EX | EM | ghi chú |
|--------|----|----|---------|
| **k=0** (baseline) | 49.0% | 13.2% | — |
| question-similarity, k=3 | 47.9% | 13.3% | neutral/âm (tuần trước) |
| **DAIL k=1**, never_schema | **53.0%** | 17.2% | gate=77.1% ✅ |
| **DAIL k=3**, never_schema | **52.5%** | 19.3% | gate=74.9% ✅ |
| DAIL k=3, with_schema | 48.7% | 14.4% | schema bên ngoài làm hại |

**Nhận xét:** DAIL selection **đảo ngược** kết quả ICL trên base model — từ neutral/âm sang **+4.0pp (k=1)** và **+3.5pp (k=3)**. Quality gate (lọc demo kém similarity) là yếu tố then chốt: giữ lại ~75% demo, loại bỏ nhiễu. Demo style `with_schema` vẫn bị âm vì DDL từ schema khác làm model nhầm cột/bảng.

### Central model (Qwen2.5-1.5B + LoRA fine-tuned trên toàn bộ train, k=0: 63.1%)

| Config | EX | EM |
|--------|----|----|
| **k=0** (ceiling) | **63.1%** | 41.7% |
| DAIL k=1 | 59.8% | 41.9% |
| DAIL k=3 | 60.2% | 41.6% |

**Nhận xét:** DAIL vẫn âm trên model fine-tuned (−2.9 đến −3.3pp), dù ít hại hơn question-similarity (tuần trước −5.6pp). Điều này nhất quán với DAIL-SQL [9] gốc và Open-SQL [arXiv:2405.06674] — model đã fine-tune "quên" cách đọc demo do lệch phân phối train/test. DAIL giảm được mức độ hại chứ chưa đảo ngược được.

### Gemma-2-2B (khảo sát cho slm_swap ablation)

| Config | EX | EM |
|--------|----|----|
| k=0 | 50.8% | 13.9% |
| DAIL k=3, never_schema | 49.8% | 23.3% |
| DAIL k=3, skeleton | 48.2% | 16.7% |

Gemma-2B có floor cao hơn Qwen-1.5B (+1.8pp) nhưng ICL cũng âm. Demo style `skeleton` (SQL identifier được mask) làm giảm thêm. Gemma-2B sẽ là candidate cho `slm_swap` ablation trong giai đoạn sau.

### Lưu ý: regression ngày 29/06

Run DAIL k=3 mới nhất (ngày 29/06, git_sha=`5dd4d62`) trả về EX=49.0% — ngang k=0, thấp hơn đáng kể so với run cùng config ngày 24/06 (52.5%). Có thể liên quan đến thay đổi code giữa hai commit. Em cần kiểm tra trước khi dùng số này làm reference chính thức.

---

## 2. Chốt kiến trúc: KID (Learning from Imperfect Data)

Sau khi review lại KID [arXiv:2410.11371, EMNLP Findings 2024], em quyết định thay thế cơ chế distillation cũ (offline annotation + exec-filter) bằng KID. Lý do chính: teacher offline cần ~13 giờ mỗi client chỉ để sinh targets — quá tốn kém để sweep. KID online chỉ cần 1 forward pass của teacher mỗi training step.

### Cơ chế mới (KID-based):

- **Teacher frozen** — Qwen2.5-7B, load cùng lúc với student (co-loaded), online per step
- **Public data** — teacher chạy trên **BIRD train** (không bao giờ thấy Spider `Qᵢ` → privacy tuyệt đối)
- **Per step:** student nhận BIRD gold SQL → mask một phần (`ρ`) → rewrite thành `ŷ` → teacher forward (với ICL k=3 từ BIRD) → soft labels `p` → `L_KD = RKL(q‖p)`
- **Loss combined:** `L = λ₁·L_FT + λ₂(t)·L_KD` với alpha-decay (`λ₂`: 1.0 → 0)
- **Reverse KL** (mode-seeking) thay vì Forward KL — KID [2024] chứng minh RKL hợp hơn cho SQL generation

### Thay đổi so với kiến trúc cũ:

| Cũ | Mới (KID) |
|----|-----------|
| Teacher offline inference trên `Qᵢ` (~13h/client) | Teacher online per step trên BIRD public (~100× nhanh hơn) |
| Exec-filter lọc target | Không cần (ŷ từ student mask, teacher chỉ score) |
| CoT generation | Không cần CoT riêng |
| L_struct (skeleton-structure loss) | Không còn |
| Forward KL | Reverse KL (per KID) |

### BIRD dataset — vai trò kép (locked 2026-06-29):

1. **Public KD dataset:** teacher distill trên BIRD train — tách hoàn toàn khỏi private Spider `Qᵢ`
2. **Second eval benchmark:** báo cáo EX trên BIRD test → chứng minh cross-dataset generalization

### VRAM:

- Teacher 7B (4-bit) ~8 GB + student 1.5B ~3 GB = **~11 GB** → T4 chạy được (PoC)
- Teacher full precision ~14 GB + student ~3 GB = **~17 GB** → cần A100 40 GB

---

## 3. Scoreboard hiện tại (clean, citable)

| Arm | Config | EX | EM | n_eval | run_date |
|-----|--------|----|----|--------|---------|
| `base` | Qwen-1.5B, k=0 | 49.0% | 13.2% | 1034 | 24/06 |
| `base@dail_k1` | Qwen-1.5B, DAIL k=1 | **53.0%** | 17.2% | 1034 | 24/06 |
| `base@dail_k3` | Qwen-1.5B, DAIL k=3 | 52.5% | 19.3% | 1034 | 24/06 |
| `central` | Qwen-1.5B LoRA FT, k=0 | **63.1%** | 41.7% | 1034 | 24/06 |
| `central@dail_k3` | Qwen-1.5B LoRA FT, DAIL k=3 | 60.2% | 41.6% | 1034 | 24/06 |
| `gemma2b_base` | Gemma-2B, k=0 | 50.8% | 13.9% | 1034 | 24/06 |

> Các arm chính (`local`, `fedavg`, `fedkd`) chưa có số — đang chờ implement KID training loop.

---

## 4. Việc tiếp theo

**Ưu tiên ngay (tuần tới):**

1. **Điều tra regression 29/06** — so sánh git diff giữa `61b7a27` (52.5%) và `5dd4d62` (49.0%) để xác định nguyên nhân
2. **Implement KID training loop** (`lora_trainer.py`): mask+rewrite pipeline → online teacher forward trên BIRD → RKL loss → alpha-decay scheduler
3. **Chạy `local` ×3 + `fedavg` ×3** (gold CE only, không teacher) → lập baseline federation trước khi thêm KD
4. **Chạy `fedkd_teacher_k3` ×3** → full method; đo `fedkd − local` (federation gain) và `fedkd − fedavg` (teacher value)

**Giai đoạn sau:**
- Eval toàn bộ arms trên Spider + BIRD (cross-dataset)
- Ablations: `fedkd_teacher_k0` (no ICL in teacher) vs `fedkd_teacher_k3` (ICL-enhanced teacher)
- Sweep K ∈ {3, 5, 10} clients

---

**Câu hỏi em cần thầy cho ý kiến:** Với kiến trúc KID dùng BIRD làm public KD data, teacher chạy trên BIRD còn student fine-tune trên Spider `Qᵢ` (hai domain khác nhau) — em lo domain gap giữa BIRD (phức tạp hơn Spider) có thể làm soft labels của teacher kém quality trên các mẫu đơn giản. Thầy có gợi ý cách kiểm tra hoặc điều chỉnh tỷ lệ `λ₂` không?

---

# Báo cáo tiến độ FedICL-SQL — 22/06/2026

Chào thầy Hùng,

Em cập nhật tiến độ và kết quả hiện tại của dự án.

## Kiến trúc hiện tại

Hệ thống chạy theo kiến trúc đã chốt:

- **Tại mỗi client (local):** **Teacher** 7B (Qwen2.5-7B) được **LoRA fine-tune (SFT)** trên private set `Qᵢ` của client, sau đó inference trên chính `Qᵢ` để sinh **SQL + Chain-of-Thought (CoT) + top-K logprobs**, qua **exec-filter** (thực thi để lọc) → tạo **KD targets**. Bước này offline, chạy 1 lần trước training.
- **Student** 1.5B (Qwen2.5-1.5B) + **LoRA:** mỗi round khởi tạo từ **global model `M_G`**, train với loss kết hợp **`CE` (gold label) + `soft-KL` (distillation từ teacher) + skeleton-structure loss + exec-filter**.
- **Server:** mỗi client chỉ upload **LoRA delta** (encrypted + nén + **DP noise**); server **FedAvg** → **global SLM `M_G`** → broadcast lại cho round sau.

Raw data, schema và teacher outputs không bao giờ rời client — chỉ **weights (LoRA delta)** được truyền.

Hiện đã chạy xong các **baseline** tham chiếu trên **full test set** (Spider dev, n=1034, 1 seed — mức PoC), tất cả qua **một evaluation pipeline thống nhất** (cùng prompt, cùng exec-scoring) để các số comparable. Phần **client-side KD** trên model gộp và **multi-client federation** còn đang chờ chạy.

## Thực nghiệm đã chạy

Demo ICL lấy **cross-schema** từ train set (k=3), retrieval theo **question similarity** (BGE embedding).

| Config                         | EX        | EM    |
| ------------------------------ | --------- | ----- |
| **Base** (Non-FT), k=0         | 49.3%     | 12.7% |
| **Base** (Non-FT) + ICL, k=3   | 49.5%     | 17.0% |
| **Centralized-FT **, k=0       | **63.0%** | 42.6% |
| **Centralized-FT ** + ICL, k=3 | 57.4%     | 39.3% |

> EX = Execution Accuracy (kết quả query đúng), EM = Exact Match (khớp câu lệnh SQL).

Nhận xét chính:

- **LoRA fine-tune** đưa EX từ 49.3% → **63.0%** — đây là **upper bound (ceiling)** để federation hướng tới.
- **ICL không có contribution, và còn negative trên model đã fine-tune:**
  - Trên **Base (Non-FT)**: ICL **neutral** (+0.2pp; McNemar p>0.6 — không significant).
  - Trên **Centralized-FT**: ICL **−5.6pp** (63.0% → 57.4%; McNemar χ²=17.2, **p<0.001 — significant**). Per-record: ICL phá **127** câu vốn đúng, chỉ cứu **69**.
  - **Error analysis:** ~53% regression do model **over-imitate cấu trúc** SQL của demo (demo từ schema khác → áp sai query shape); đáng chú ý demo **càng similar càng hại** (top-1 similarity nhóm bị phá 0.767 ≥ nhóm được cứu 0.756).

Hiện em chưa tìm được cách để ICL có **positive contribution** về accuracy — đây là vấn đề em đang vướng và mong thầy cho hướng.

## Việc tiếp theo

1. Chạy **client-side KD** (teacher → student) trên train set → đo **KD contribution** (soft-KL + CoT + skeleton), rồi **multi-client federation**.
2. Tiếp tục thử cải thiện ICL — ví dụ **DAIL Selection** (retrieval theo **query-skeleton similarity** thay vì question) — xem có kéo ICL về positive không.

Em nhờ thầy review và gợi ý hướng cho vấn đề ICL đang bị âm. Em đã tìm đọc các paper ICL liên quan, nhưng đa số chứng minh ICL gain trên **LLM lớn** (GPT-3.5/4, ≥7B), hoặc trên model nhỏ nhưng **setting in-domain — demo lấy từ CÙNG schema/database với câu hỏi test**, nên model chỉ cần copy lại pattern gần giống. Setting của em là **cross-schema** (train/test database tách rời, demo từ schema khác hẳn), khó hơn nhiều — và chưa thấy bài nào cho ICL gain trên **SLM ~1.5B + cross-schema** như vậy. Dưới đây là các paper em đã research liên quan.

## Tài liệu liên quan đang research

Em đọc lại literature thì thấy gần như mọi báo cáo "ICL giúp NL2SQL" đều rơi vào **một trong hai điều kiện**: model rất lớn (GPT-4/3.5), hoặc demo **in-domain** (lấy từ cùng database với câu test). Setting của em — SLM 1.5B, cross-schema, lại sau fine-tune — không thuộc cả hai, nên kết quả ICL âm là **nhất quán với literature**, không phải lỗi cài đặt. Em trích vài câu nguyên văn để thầy tiện kiểm:

**(1) ICL chỉ có gain khi model lớn / in-domain:**

- DAIL-SQL (Gao 2023, [arXiv:2308.15363](https://arxiv.org/abs/2308.15363), GPT-4, SOTA Spider 86.6%) — *"While for GPT-3.5-TURBO and TEXT-DAVINCI-003, adding examples may incur drop in execution accuracy due to limited in-context learning capability."*
- SQL-Encoder (Pourreza 2024, [arXiv:2403.16204](https://arxiv.org/abs/2403.16204)) cho CodeLlama-7B +4–8%, nhưng demo *"are from the exact same database as the question at inference time"* (in-domain). Light-SQL ([Springer](https://link.springer.com/chapter/10.1007/978-3-032-21628-1_16)) cũng chỉ chạy trên **1 database** duy nhất.
- DIN-SQL (Pourreza 2023, [arXiv:2304.11015](https://arxiv.org/abs/2304.11015), 85.3 EX) toàn bộ gain dựa vào reasoning của GPT-4.

**(2) ICL không giúp model nhỏ, và còn giảm accuracy sau fine-tune:**

- DAIL-SQL ([arXiv:2308.15363](https://arxiv.org/abs/2308.15363)) — ngay trên Spider, model **sau fine-tune** bị ICL làm hại (đúng domain, mạnh nhất): *"Unexpectedly, the fine-tuned LLMs fail to learn from examples ... adding contextual examples in test prompts incurs sudden decrease in both exact-set-match and execution match accuracy."* → khớp **−5.6pp** của em.
- Open-SQL (Chen 2024, [arXiv:2405.06674](https://arxiv.org/abs/2405.06674), CodeLlama 7B) — few-shot giảm EX sau SFT (45.76% → 37.74% 1-shot → 32.2% 3-shot): *"both models exhibited a decline in performance with additional examples ... becoming overly focused on the zero-shot prompt."*
- Semantic Anchors (2025, [arXiv:2511.21038](https://arxiv.org/abs/2511.21038), 8 model 1–12B) — *"ICL operates as prior refinement, not flexible learning"* (override rate = 0) → khớp **Base+ICL +0.2pp (neutral)** của em. Cùng hướng: Larger-LMs-do-ICL-differently (J. Wei 2023, [arXiv:2303.03846](https://arxiv.org/abs/2303.03846)) và Emergent Abilities (Wei 2022, [arXiv:2206.07682](https://arxiv.org/abs/2206.07682)) — ICL là khả năng **xuất hiện theo scale**, model nhỏ gần như không có.
- SLM-SQL ([arXiv:2507.22478](https://arxiv.org/abs/2507.22478), 1.5B, **76.7% EX Spider chỉ bằng fine-tune, không ICL**) — minh chứng SLM làm SQL mạnh qua FT, không cần ICL.

**Hướng em đang thử để kéo ICL về dương:** DAIL Selection (retrieval theo query-skeleton thay vì question); DCG-SQL (Lee 2025, [arXiv:2505.19956](https://arxiv.org/abs/2505.19956); demo theo schema-link graph; lưu ý paper này đo *vs random*, không vs k=0); và In-Context Learning Distillation (Huang 2022, [arXiv:2212.10670](https://arxiv.org/abs/2212.10670)) — train student **có demo trong prompt** (Meta-ICT / Multitask-ICT) để student biết đọc demo thay vì bỏ qua.

**Federated LLM/SLM + KD:**

- **FedCoLLM** (Fan 2024, [arXiv:2411.11707](https://arxiv.org/abs/2411.11707)) — **[QA, không SQL · server LLaMa2-7B / client SLM 1.3B]** co-tuning: client fine-tune SLM bằng LoRA → server FedAvg, rồi KD hai chiều (CE + λ·KL) giữa server-LLM ↔ SLM trên **auxiliary dataset** ở server; nhờ KD qua tập phụ này, data private không rời client; LLM ở server nên chạy model lớn.
- **FedMKT** (Fan 2024, [arXiv:2406.02224](https://arxiv.org/abs/2406.02224)) — **[generic NLP · LLM↔SLM khác họ tokenizer, vd Bloom↔LLaMa]** truyền **output logits** trên public data lên server để distill hai chiều; căn token bằng **MinED**; **không** FedAvg trọng số.
- **Fed-ICL** (Wang 2025, [arXiv:2506.07440](https://arxiv.org/abs/2506.07440)) — **[QA, không SQL · model-agnostic]** federated ICL: ví dụ in-context ở client; refine câu trả lời qua nhiều vòng client↔server (iterative refinement), không train, không truyền data thô — *parameter-free*.
- **FedAvg / FedProx** (McMahan 2017 / Li 2020, [arXiv:1602.05629](https://arxiv.org/abs/1602.05629) / [arXiv:1812.06127](https://arxiv.org/abs/1812.06127)) — **[lý thuyết, model-agnostic]** FedAvg gộp trọng số trung bình theo lượng data; FedProx thêm proximal term xử lý non-IID; nền lý thuyết hội tụ.

**KD cho NL2SQL:**

- **KID** (Zhong 2024, [arXiv:2410.11371](https://arxiv.org/abs/2410.11371), EMNLP Findings) — **[Spider cross-domain · student Qwen1.5-0.5B ← teacher 7B]** KD từ "imperfect data": mô phỏng cascading effect của inference để giảm train-inference mismatch; +tới **5.83%** trên 5 benchmark; **Reverse KL hợp SQL hơn Forward KL**.
- **CoT-SFT cho SLM** (Solanki 2026, [arXiv:2603.22942](https://arxiv.org/abs/2603.22942)) — **[Spider (600 câu khó) · Qwen-7B + LoRA]** target CoT 5 bước (phân tích → chọn bảng → chọn cột → join → tự kiểm); CoT-SFT **54.5%** so SFT thường 45.3% (**+9.2pp**).
