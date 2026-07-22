

# Báo cáo tiến độ — 21/07/2026 (giai đoạn 08–21/07)

Kính gửi thầy Hùng,

Hai tuần qua em hoàn thành ba việc: chốt lại kiến trúc, hoàn tất nhóm thực nghiệm distillation, xây xong pipeline federated. Kết luận cốt lõi: distillation tăng độ chính xác mạnh khi huấn luyện trên Spider (điều kiện lý tưởng), nhưng trên bộ dữ liệu công khai (điều kiện thực tế) mức tăng không còn ý nghĩa thống kê — giá trị chắc chắn còn lại là độ tin cậy thực thi (Mục 2). Mọi chỉ số dưới đây đo trên Spider, 1034 câu, độ chính xác thực thi EX (kèm kiểm định McNemar).

## 1. Thay đổi kiến trúc: chuyển teacher lên server, dùng dữ liệu công khai làm proxy KD

- **Client** (mô hình nhỏ 1.5B): chỉ fine-tune trên dữ liệu riêng, gửi bản cập nhật trọng số (~vài MB) lên server. Dữ liệu không rời client.
- **Server** (teacher 7B): gộp trọng số các client, rồi dùng teacher huấn luyện mô hình nhỏ đã gộp trên dữ liệu công khai mỗi vòng.
- **Dữ liệu công khai:** BIRD — tập train ~9.400 câu / ~70 CSDL, tách biệt hoàn toàn với Spider ở client. Chỉ distillation trên **tập cố định 3.873 câu / 69 CSDL** (SQL do teacher tự sinh trên 9.400 câu gốc, lọc giữ câu thực thi khớp đáp án — không dùng SQL gốc của BIRD do chất lượng nhãn thấp: huấn luyện thử trên nhãn gốc chỉ đạt 47.1% EX, dưới cả mô hình chưa huấn luyện 50.0%).

**Phương pháp KD đang dùng** (reverse-KL logit distillation, theo KID [arXiv:2410.11371]): với mỗi câu trong tập công khai, teacher và student cùng chấm trên **một câu SQL mục tiêu** (do teacher sinh) với **cùng ngữ cảnh prompt**. Hàm loss:

```text
L = λ_ft · CE(mục tiêu) + λ_kd · RKL(student ‖ teacher)     (tỉ lệ 1:1)
```

- Dùng **reverse-KL** (mode-seeking) thay vì forward-KL: phù hợp với phân phối token hẹp, xác định của SQL (forward-KL trải xác suất sang các nhánh sai).
- Teacher (Qwen2.5-Coder-7B) **chỉ chấm điểm, không sinh** — mỗi bước một lượt tính trên logit. Vì mục tiêu cố định, **logit teacher được tính sẵn offline một lần** rồi tái dùng mọi vòng, nên vòng lặp federated không phải nạp teacher 7B mỗi vòng.

## 2. Đánh giá hiệu quả của distillation

Ba thí nghiệm, mỗi thí nghiệm là một so sánh có đối chứng (McNemar theo cặp câu).

**Thí nghiệm 1 — distillation có tác dụng không?** (học trên đáp án Spider có sẵn = điều kiện lý tưởng). Hai nhánh **cùng huấn luyện một giai đoạn từ mô hình gốc**, trên cùng dữ liệu Spider, chỉ khác hàm mất mát.

| So sánh (đều từ mô hình gốc)            | Cách suy luận | EX   | Δ EX     | p     |
| --------------------------------------- | ------------- | ---- | -------- | ----- |
| Chỉ Fine-tune thường (chỉ CE)           | greedy        | 62.2 | —        | —     |
| Chỉ distillation (CE + RKL trên đáp án) | greedy        | 68.3 | **+6.1** | 3e-07 |

→ Distillation cho kết quả tốt hơn hẳn finetune.

**Thí nghiệm 2 — distillation trên dữ liệu công khai (BIRD) có thêm giá trị không?** Đối chứng cùng ngân sách huấn luyện: fine-tune-2-lần (A) so với fine-tune → KD-BIRD → fine-tune (B). Hai nhánh chỉ khác ở khâu KD-BIRD chèn giữa.

| Chỉ số | Cách suy luận     | A (đối chứng) | B (có KD-BIRD) | Δ     | p     |
| ------ | ----------------- | ------------- | -------------- | ----- | ----- |
| EX     | greedy            | 67.0          | 67.3           | +0.29 | 0.83  |
| EX     | +self-consistency | 73.4          | 75.2           | +1.84 | 0.070 |
| EM     | +self-consistency | 67.4          | 69.8           | +2.42 | 0.030 |

→ Greedy **phẳng** (+0.29, p=0.83). Chỉ dưới self-consistency mới có +1.84 EX nhưng **chưa đủ tin cậy** (p=0.070); EM cải thiện có ý nghĩa (+2.42, p=0.030).

**Thí nghiệm 3 — kiểm chứng chéo trên 3 biến thể khó của Spider** (cùng mô hình đã KD-BIRD so với chỉ fine-tune, cả 2 cách suy luận):

| Tập              | n    | EX trước→sau        | Lỗi thực thi trước→sau |
| ---------------- | ---- | ------------------- | ---------------------- |
| Spider-Realistic | 508  | 55.3→56.3 (p=0.70)  | 110→65                 |
| Spider-Syn       | 1034 | 51.1→51.5 (p=0.84)  | 234→154                |
| Spider-DK        | 535  | 46.9→49.9 (p=0.085) | 116→75                 |

- EX: **không tập nào có ý nghĩa thống kê** (chiều dương, trong sai số).
- **Độ tin cậy thực thi: giảm 30–52% số câu lỗi trên cả 3 biến thể × 2 cách suy luận, không ngoại lệ.** Đây là đóng góp chắc chắn và khái quát nhất của distillation-BIRD — sẽ là kết quả chính báo cáo cho phần này. EX chỉ nêu ở mức định hướng.

## 3. Kỹ thuật chọn đáp án khi suy luận (self-consistency)

Sinh 8 phương án SQL, thực thi từng phương án trên CSDL, bỏ phiếu chọn phương án cho kết quả nhất quán nhất.

- Tăng ~4 điểm EX (68.3%→72.3%), **không cần huấn luyện thêm, không cần ví dụ mẫu**.
- Chi phí: suy luận chậm ~1.4× mỗi câu — chấp nhận được (lợi thế hệ thống là mô hình nhỏ, không phải tốc độ từng câu).

## 4. ICL (in-context learning)

Đã thử các phương pháp chọn ví dụ mẫu: random, DAIL, question-similarity, schema-aware… Hiện chưa phương pháp nào cho cải thiện khả quan trên mô hình đã fine-tune (chọn công phu ≈ chọn ngẫu nhiên, McNemar p=1.00). Tạm giữ ICL để nghiên cứu sau.

## 5. Pipeline federated

Ý tưởng: mỗi vòng, các client gửi LoRA adapter lên server để gộp; server distillation adapter đã gộp trên dữ liệu công khai rồi phát lại. Điểm kỹ thuật ở khâu gộp adapter:

- **FedAvg** (McMahan 2017, arXiv:1602.05629) — mốc so sánh chuẩn: gộp trọng số trung bình theo lượng dữ liệu mỗi client. Với LoRA, gộp trung bình từng thừa số A, B sinh **sai số đại số**: (Σpᵢ·Bᵢ)(Σpᵢ·Aᵢ) ≠ Σpᵢ·BᵢAᵢ — sai số này tồn tại cả khi dữ liệu IID.
- **FLoRA-NA** (Nguyen et al., arXiv:2509.26399) — phương pháp gộp chính đề xuất: giải hệ số kết hợp giữa các client để bám sát mục tiêu Σpᵢ·BᵢAᵢ, vẫn xuất ra một adapter rank-r duy nhất → giảm sai số gộp mà giữ nguyên chi phí truyền thông. Em mở rộng thành bản có trọng số theo lượng dữ liệu (client Spider kích thước khác nhau).
- **6 cấu hình so cặp:** {FedAvg, FLoRA-NA} × {không distillation / distillation CE / distillation CE+RKL}. Đo được: giá trị của khâu gộp (FLoRA-NA − FedAvg) và giá trị của teacher (distillation − không distillation).
- Đã implement + kiểm thử end-to-end trên dữ liệu thật (quy mô nhỏ), có lưu/khôi phục khi lỗi. **Chưa chạy quy mô lớn (8 client × 15 vòng)** — kết quả federated đầu tiên của bài báo, ưu tiên cao nhất.

## 6. Bảng kết quả (Spider, 1034 câu)

| Cấu hình                                                            | EX (greedy) | EX (+self-consistency) | Ghi chú                                                                        |
| ------------------------------------------------------------------- | ----------- | ---------------------- | ------------------------------------------------------------------------------ |
| Mô hình nhỏ, chưa huấn luyện                                        | 50.0%       | —                      | sàn                                                                            |
| Fine-tune 1 lần                                                     | 62.2%       | 70.1%                  |                                                                                |
| Fine-tune 2 lần (đối chứng ngân sách)                               | 67.0%       | 73.4%                  | mốc đối chứng cho KD-BIRD                                                      |
| Fine-tune → KD-BIRD (2 giai đoạn)                                   | 65.5%       | 69.3%                  | EM sụt mạnh 57.2→32.5 (lệch văn phong SQL)                                     |
| **Fine-tune → KD-BIRD → Fine-tune (3 giai đoạn, đường triển khai)** | **67.3%**   | **75.2%**              | +SC vượt đối chứng, p=0.070; EM phục hồi 63.9                                  |
| Distillation trên Spider (oracle, từ mô hình gốc, 1 giai đoạn)      | 68.3%       | 72.3%                  | huấn luyện độc lập, không nối tiếp các dòng trên; không phải điều kiện thực tế |
| Teacher 7B (tham chiếu)                                             | 78.7%       | —                      |                                                                                |

- Đường triển khai thật là **Fine-tune → KD-BIRD → Fine-tune**; so với fine-tune-2-lần cùng ngân sách, khâu KD-BIRD hầu như không thêm EX ở greedy nhưng cộng hưởng với self-consistency (75.2 so 73.4).
- Dòng "Distillation trên Spider" chỉ là oracle (học trên đáp án Spider có sẵn), dùng để chứng minh distillation có tác dụng — không đại diện cho hệ thống thật.
- Các cấu hình federated chưa có số — pipeline vừa xong, chờ GPU.

## 7. Kế hoạch tiếp theo

1. Thực nghiệm federated quy mô lớn — số liệu cốt lõi của bài báo.
2. Lặp distillation-BIRD với 2–3 seed để xác nhận số EX (độ tin cậy thực thi đã đủ nhất quán qua 4 tập). Chi phí thấp, mang tính quyết định.
3. Biến thể Spider đã đánh giá xong (Mục 2); sẽ chạy lại trên mô hình federated sau khi có kết quả quy mô lớn.

**Xin ý kiến thầy:** (1) phê duyệt chuyển teacher lên server; (2) nơi công bố — ban đầu nhắm IAJIT, lựa chọn mới gồm KBS / NCA / J. Supercomputing / IEEE Access.

---

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

| Config                     | EX        | EM    | ghi chú                  |
| -------------------------- | --------- | ----- | ------------------------ |
| **k=0** (baseline)         | 49.0%     | 13.2% | —                        |
| question-similarity, k=3   | 47.9%     | 13.3% | neutral/âm (tuần trước)  |
| **DAIL k=1**, never_schema | **53.0%** | 17.2% | gate=77.1% ✅             |
| **DAIL k=3**, never_schema | **52.5%** | 19.3% | gate=74.9% ✅             |
| DAIL k=3, with_schema      | 48.7%     | 14.4% | schema bên ngoài làm hại |

**Nhận xét:** DAIL selection **đảo ngược** kết quả ICL trên base model — từ neutral/âm sang **+4.0pp (k=1)** và **+3.5pp (k=3)**. Quality gate (lọc demo kém similarity) là yếu tố then chốt: giữ lại ~75% demo, loại bỏ nhiễu. Demo style `with_schema` vẫn bị âm vì DDL từ schema khác làm model nhầm cột/bảng.

### Central model (Qwen2.5-1.5B + LoRA fine-tuned trên toàn bộ train, k=0: 63.1%)

| Config            | EX        | EM    |
| ----------------- | --------- | ----- |
| **k=0** (ceiling) | **63.1%** | 41.7% |
| DAIL k=1          | 59.8%     | 41.9% |
| DAIL k=3          | 60.2%     | 41.6% |

**Nhận xét:** DAIL vẫn âm trên model fine-tuned (−2.9 đến −3.3pp), dù ít hại hơn question-similarity (tuần trước −5.6pp). Điều này nhất quán với DAIL-SQL [9] gốc và Open-SQL [arXiv:2405.06674] — model đã fine-tune "quên" cách đọc demo do lệch phân phối train/test. DAIL giảm được mức độ hại chứ chưa đảo ngược được.

### Gemma-2-2B (khảo sát cho slm_swap ablation)

| Config                 | EX    | EM    |
| ---------------------- | ----- | ----- |
| k=0                    | 50.8% | 13.9% |
| DAIL k=3, never_schema | 49.8% | 23.3% |
| DAIL k=3, skeleton     | 48.2% | 16.7% |

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

| Cũ                                                | Mới (KID)                                                  |
| ------------------------------------------------- | ---------------------------------------------------------- |
| Teacher offline inference trên `Qᵢ` (~13h/client) | Teacher online per step trên BIRD public (~100× nhanh hơn) |
| Exec-filter lọc target                            | Không cần (ŷ từ student mask, teacher chỉ score)           |
| CoT generation                                    | Không cần CoT riêng                                        |
| L_struct (skeleton-structure loss)                | Không còn                                                  |
| Forward KL                                        | Reverse KL (per KID)                                       |

### BIRD dataset — vai trò kép (locked 2026-06-29):

1. **Public KD dataset:** teacher distill trên BIRD train — tách hoàn toàn khỏi private Spider `Qᵢ`
2. **Second eval benchmark:** báo cáo EX trên BIRD test → chứng minh cross-dataset generalization

### VRAM:

- Teacher 7B (4-bit) ~8 GB + student 1.5B ~3 GB = **~11 GB** → T4 chạy được (PoC)
- Teacher full precision ~14 GB + student ~3 GB = **~17 GB** → cần A100 40 GB

---

## 3. Scoreboard hiện tại (clean, citable)

| Arm               | Config                      | EX        | EM    | n_eval | run_date |
| ----------------- | --------------------------- | --------- | ----- | ------ | -------- |
| `base`            | Qwen-1.5B, k=0              | 49.0%     | 13.2% | 1034   | 24/06    |
| `base@dail_k1`    | Qwen-1.5B, DAIL k=1         | **53.0%** | 17.2% | 1034   | 24/06    |
| `base@dail_k3`    | Qwen-1.5B, DAIL k=3         | 52.5%     | 19.3% | 1034   | 24/06    |
| `central`         | Qwen-1.5B LoRA FT, k=0      | **63.1%** | 41.7% | 1034   | 24/06    |
| `central@dail_k3` | Qwen-1.5B LoRA FT, DAIL k=3 | 60.2%     | 41.6% | 1034   | 24/06    |
| `gemma2b_base`    | Gemma-2B, k=0               | 50.8%     | 13.9% | 1034   | 24/06    |

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
