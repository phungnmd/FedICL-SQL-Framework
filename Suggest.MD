# Fed-ICKD: Federated In-Context Knowledge Distillation for Text-to-SQL

**Kiến trúc chốt + Kế hoạch thực nghiệm (target Q3) + Roadmap từng bước**
*Phần cứng: 1× RTX A5000 24GB — Cập nhật: 07/2026*

---

## 1. Tóm tắt ý tưởng (Abstract draft)

Schema và dữ liệu truy vấn của doanh nghiệp là thông tin nhạy cảm, không thể tập trung để fine-tune. Chúng tôi đề xuất **Fed-ICKD**: framework federated learning cho Text-to-SQL trong đó (1) các client fine-tune SLM 1.5B với **ICL theo DAIL selection** trên dữ liệu riêng, (2) một **teacher 7B toàn cục tại server không bao giờ tiếp xúc dữ liệu client**, thực hiện distillation (KL + RKD) trên **public pool** sau mỗi vòng aggregation để hợp nhất và ổn định global model dưới điều kiện non-IID theo domain. Kết quả: student 1.5B thu hẹp X% khoảng cách tới teacher 7B trong khi bảo toàn quyền riêng tư dữ liệu.

**3 novelty claims:**
1. Federated Text-to-SQL với partition non-IID theo schema/domain (formulation mới, realistic).
2. Server-side distillation (KL + RKD) trên public data như một *consensus regularizer* cho FedAvg — teacher tách biệt hoàn toàn khỏi private data.
3. DAIL-style ICL nhất quán train/inference ở client, kết hợp phân tích ảnh hưởng của chất lượng public pool lên hiệu quả distillation.

---

## 2. Kiến trúc chốt

```
┌──────────────────────── SERVER ────────────────────────┐
│  Teacher Qwen2.5-7B (frozen)     Public Pool P          │
│                                                          │
│  [Phase 1 - offline, 1 lần]                              │
│  DAIL selection trên P → teacher ICL forward             │
│  → cache: top-50 logits + hidden states (SQL tokens)     │
│                                                          │
│  [Phase 3 - mỗi round]                                   │
│  FedAvg(LoRA adapters) → global student                  │
│  → distill trên P: L = β·KL + γ·RKD (vài trăm steps)     │
│  → broadcast adapters                                    │
└────────────▲─────────────────────────┬──────────────────┘
     adapters│(vài MB)                 │adapters
┌────────────┴─────────────────────────▼──────────────────┐
│  CLIENT i (×K)   —  private data: vài domains Spider     │
│                                                          │
│  [Phase 2 - mỗi round]                                   │
│  DAIL selection từ local pool → prompt [k demos +        │
│  schema + question] → Student 1.5B + QLoRA               │
│  → chỉ L_CE với gold SQL, train E epochs                 │
│                                                          │
│  [Phase 4 - inference]                                   │
│  Student + DAIL retrieval local, k giống lúc train       │
└──────────────────────────────────────────────────────────┘
```

**Privacy guarantee:** dữ liệu thô, demos, embeddings của client không bao giờ rời client. Teacher chỉ chạm public pool. Chỉ LoRA adapters được truyền.

### 2.1 DAIL selection (chốt phương pháp ICL)

Theo DAIL-SQL: chọn demos bằng **similarity kép**:
- **Question similarity**: embed câu hỏi đã *mask schema-specific tokens* (tên bảng/cột → placeholder) để so ngữ nghĩa cấu trúc câu hỏi, không bị nhiễu bởi domain.
- **Query similarity**: dùng SQL sơ bộ (từ student hiện tại hoặc skeleton) để so cấu trúc SQL của candidates.
- Xếp hạng candidates thỏa cả hai → lấy top-k.
- Trong prompt: demos ở dạng **question + SQL** (bỏ schema của demo — đúng format DAIL, tiết kiệm token đáng kể, quan trọng cho student 1.5B).

Áp dụng: (a) teacher trên P dùng DAIL trong P; (b) student tại client dùng DAIL trong local pool; (c) server distillation step, student dùng DAIL trong P.

### 2.2 Loss

**Client (Phase 2):** `L = L_CE(gold SQL)` — thuần, nhẹ, không teacher.

**Server distillation (Phase 3):**
`L = β·KL(student ‖ teacher, τ=2, top-50 logits, align theo vị trí SQL output tokens) + γ·L_RKD`

**RKD** (distance-wise + angle-wise) trên quan hệ giữa samples trong batch:
- Embedding mỗi sample = mean-pool hidden states của SQL tokens (student: online; teacher: từ cache).
- Không cần projection layer (hidden dim 1536 vs 3584 không thành vấn đề — RKD chỉ so cấu trúc quan hệ).
- Batch size ≥ 16 tại server (server distill không bị ràng buộc client, thoải mái trên A5000).
- Vai trò: sau FedAvg trên non-IID, không gian representation của global model bị "vỡ" — RKD ép nó khớp lại cấu trúc quan hệ của teacher = consensus ở mức representation, bổ trợ KL ở mức output.

Khởi điểm: β=0.5, γ=0.3 (chuẩn hóa sao cho hai loss cùng scale ở step đầu).

### 2.3 Config default (chốt, không tune thêm trừ khi hỏng)

| Thành phần               | Giá trị                                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| Teacher                  | Qwen2.5-Coder-7B-Instruct, FP16, vLLM                                                     |
| Student                  | Qwen2.5-1.5B-Instruct + QLoRA (r=16, α=32, target: attn+MLP)                              |
| k_teacher                | 3 (ablate 5)                                                                              |
| k_student                | 2, **giống nhau train/inference** (ablate 0/1/2)                                          |
| Clients K                | 8                                                                                         |
| Partition                | Non-IID theo database (Dirichlet trên domain groups, α=0.5)                               |
| Rounds T                 | 15; local epochs E = 2                                                                    |
| Server distill           | 300 steps/round trên P, batch 16                                                          |
| Public pool P (default)  | Spider held-out 15% (~1.000 samples, tách theo DB, không trùng client)                    |
| Public pool P (ablation) | BIRD subset ~1.500 samples                                                                |
| Eval                     | Spider dev (EX + EM) + **Spider-Realistic** (robustness, thay cho việc mất BIRD làm eval) |
| Seeds                    | 3 cho main, 1 cho ablation                                                                |

**Lưu ý BIRD:** dùng BIRD làm pool ⇒ không eval trên BIRD được (contamination). Đã bù bằng Spider-Realistic. BIRD-as-pool chỉ là ablation về distribution gap, không phải default.

---

## 3. Kế hoạch thực nghiệm (đã cắt gọn cho 1× A5000)

### Tier 1 — Main results (3 seeds, bắt buộc) — bảng chính của paper

| #   | Config                                           | Mục đích          |
| --- | ------------------------------------------------ | ----------------- |
| M1  | Centralized FT student (toàn bộ data, không FL)  | Upper bound       |
| M2  | FedAvg + ICL, **không** server distill           | Baseline FL chính |
| M3  | **Fed-ICKD full** (FedAvg + ICL + server KL+RKD) | Đề xuất           |
| M4  | Teacher 7B + DAIL ICL, zero fine-tune            | Teacher reference |

→ 4 configs × 3 seeds = 12 runs (M4 chỉ inference, tính là 0.5). **~6-7 ngày GPU.**
Câu chuyện: M3 > M2 (distillation có tác dụng) và M3 tiến gần M1/M4.

### Tier 2 — Ablations (1 seed) — mỗi bảng phục vụ 1 claim

| #   | Ablation                                        | Configs     | Claim phục vụ                |
| --- | ----------------------------------------------- | ----------- | ---------------------------- |
| A1  | Loss: chỉ KL / chỉ RKD / KL+RKD                 | 2 runs thêm | RKD đóng góp gì              |
| A2  | k_student = 0 / 1 / 2                           | 2 runs thêm | ICL ở SLM đáng giá không     |
| A3  | Public pool: Spider held-out / BIRD / mix 50-50 | 2 runs thêm | Distribution gap của P       |
| A4  | Non-IID mức độ: Dirichlet α = 0.1 / 0.5 / IID   | 2 runs thêm | Robustness với heterogeneity |
| A5  | DAIL vs random demo selection                   | 1 run thêm  | Justify DAIL                 |

→ ~9 runs × ~0.7 ngày = **~6-7 ngày GPU.**

### Tier 3 — Nếu còn thời gian (bỏ được, không ảnh hưởng Q3)

- Student 0.5B (thêm 1 cặp model) — nâng độ tin claim
- k-robust training (k ngẫu nhiên) — trick deploy linh hoạt
- FedProx thay FedAvg — nếu A4 cho thấy drift nặng
- DP noise trên adapters — nếu reviewer FL yêu cầu; mặc định xử lý bằng discussion section

### Tổng ngân sách

| Hạng mục                                 | Thời gian                                             |
| ---------------------------------------- | ----------------------------------------------------- |
| Teacher annotation trên P (1 lần, cache) | 0.5-1 ngày                                            |
| Tier 1                                   | 6-7 ngày                                              |
| Tier 2                                   | 6-7 ngày                                              |
| Đệm debug/rerun                          | 3-4 ngày                                              |
| **Tổng**                                 | **~16-19 ngày GPU** — khả thi trong ~1-1.5 tháng lịch |

**Nguyên tắc cắt nếu cháy thời gian:** bỏ A4 trước, rồi A5. A1 và A3 là hai ablation *không được bỏ* (A1 justify RKD — phương pháp bạn đang theo; A3 là finding riêng của paper).

**Kỹ thuật tiết kiệm bắt buộc:**
- Cache teacher logits (top-50) + hidden states — sinh 1 lần duy nhất.
- Cache FAISS index + DAIL rankings.
- vLLM cho mọi inference/eval; HF+PEFT cho training.
- Checkpoint chỉ giữ adapters cuối mỗi config + best (tiết kiệm disk, chuẩn bị ~200GB).
- Eval EX bằng test-suite execution accuracy (chuẩn Spider official).

---

## 4. Roadmap từng bước làm paper

### Bước 1 — Nền móng (tuần 1-2)
1. Viết code partition Spider non-IID theo DB + tách public pool P → lưu splits cố định (seed hóa, dùng chung mọi thí nghiệm).
2. Implement DAIL selection (mask question + query similarity) → build index cho P và từng client.
3. Script teacher annotation: vLLM 7B, sinh SQL + top-50 logits + hidden states trên P. **Benchmark throughput trên 100 samples trước** để chốt ước lượng thời gian.
4. Sanity check: teacher + DAIL trên Spider dev phải đạt EX trong khoảng số liệu công bố (~75-80%). Nếu lệch xa → sửa prompt/selection trước khi đi tiếp.

### Bước 2 — Pipeline FL (tuần 2-4)
5. Flower simulation: 8 clients tuần tự trên 1 GPU, QLoRA training loop với L_CE + ICL prompt.
6. Server distillation step: KL alignment theo SQL tokens + RKD batch-wise. Unit test RKD với dummy tensors trước.
7. Chạy 1 round end-to-end với 2 clients, 50 samples/client → xác nhận pipeline không gãy, loss giảm.
8. Chạy M2 (FedAvg no-distill) full 1 seed → có số baseline đầu tiên. **Đây là go/no-go checkpoint**: nếu M2 quá thấp bất thường, dừng lại debug.

### Bước 3 — Main results (tuần 4-6)
9. Chạy M3 1 seed → so M2. Nếu M3 > M2 rõ ràng: chạy nốt 3 seeds cho M1-M3. Nếu không: quay lại tune β/γ, số distill steps (đây là điểm rủi ro cao nhất của toàn bộ paper — dành thời gian ở đây).
10. Chạy M4 (teacher reference) + eval tất cả trên Spider dev + Spider-Realistic.

### Bước 4 — Ablations (tuần 6-8)
11. Chạy Tier 2 theo thứ tự A1 → A3 → A2 → A5 → A4.
12. Vẽ figures: learning curves theo rounds, bảng chính, bar chart ablations, biểu đồ communication cost.

### Bước 5 — Viết paper (tuần 7-10, song song với ablations)
13. Cấu trúc: Intro → Related Work (3 nhánh: federated LLM fine-tuning; KD cho Text-to-SQL; ICL/demonstration selection) → Method (kiến trúc mục 2) → Experiments → Analysis (finding từ A3: chất lượng public pool vs hiệu quả distillation) → Limitations (không DP formal; simulation chứ chưa deploy thật; chỉ Spider-family) → Conclusion.
14. Viết Method + Experiment setup trước (viết được ngay khi code xong, không cần đợi kết quả).
15. Threat model ngắn trong Method: định nghĩa rõ "teacher không thấy private data" nghĩa là gì, adapters truyền đi có rủi ro gì, tại sao chấp nhận được ở mức threat model này.

### Bước 6 — Nộp (tuần 10-12)
16. Target đề xuất (theo thứ tự): *Knowledge-Based Systems* (cao, thử trước), *Neural Computing and Applications*, *Journal of Supercomputing*, *IEEE Access* (chắc ăn). Hoặc conference: PAKDD/DASFAA rồi extend journal.
17. Checklist trước khi nộp: 3 seeds mean±std cho main table; code + splits công khai (GitHub) — điểm cộng lớn với reviewer; báo cáo compute (1× A5000) — thực ra là selling point "reproducible trên single GPU".

---

## 5. Rủi ro & phương án B

| Rủi ro                                   | Dấu hiệu              | Phương án B                                                                                                         |
| ---------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Server distill không cải thiện (M3 ≈ M2) | Bước 9                | Tăng distill steps; thử distill mỗi 2-3 rounds thay vì mỗi round; kiểm tra alignment KL                             |
| RKD không đóng góp (A1)                  | KL-only ≈ full        | Vẫn báo cáo trung thực — negative finding về RKD trong FL setting cũng là finding; chuyển claim sang KL + phân tích |
| BIRD pool phản tác dụng (A3)             | EX giảm khi dùng BIRD | Chính là finding về distribution gap — frame thành phân tích, không giấu                                            |
| ICL hại student 1.5B (A2: k=0 tốt nhất)  | Bước 11               | Báo cáo + chuyển default sang k=0, DAIL vẫn dùng cho teacher; điều chỉnh narrative                                  |
| Thiếu thời gian                          | Tuần 8                | Cắt A4, A5; giữ nguyên Tier 1 + A1 + A3                                                                             |

---

*Nguyên tắc chung: mọi kết quả âm tính đều được frame thành phân tích thay vì giấu — với Q3, một paper trung thực có 1-2 negative findings kèm giải thích thuyết phục hơn một paper toàn số đẹp đáng ngờ.*