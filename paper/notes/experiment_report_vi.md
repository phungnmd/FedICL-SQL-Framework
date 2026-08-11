# Báo cáo hiện trạng thực nghiệm — 12/08/2026

**Setup.** Student Qwen2.5-1.5B-Instruct (LoRA r=16). Teacher
Qwen2.5-Coder-7B-Instruct, 4-bit, frozen. K=5 clients, non-IID Dirichlet
α=0,5, 910–2.749 mẫu/client. T=1 round. Public pool = BIRD, 3.873 mẫu, target
là SQL do teacher sinh và đã execution-verified. Eval trên Spider dev
(n=1.034), greedy, chỉ số EX. Kiểm định McNemar exact trong một seed, paired
t-test giữa các seed.

**Các arm.**

| Arm | Mô tả |
|---|---|
| `base` | Student chưa train |
| `local` | Một client tự train, không federated |
| `fedavg` | Client local FT → FedAvg. Không KD |
| `kd_only` | `base` → server KD trên public pool. Không dùng dữ liệu private |
| `fed_kd` | Client local FT → FedAvg → server KD. **Pipeline không ICL** |
| `fed_kd_icl` | Như `fed_kd`, client train kèm k=3 demonstrations từ private pool. **Pipeline đề xuất ban đầu** |

---

## Phần 1 — Pipeline đề xuất (`fed_kd_icl`)

### 1.1 Kết quả

`fed_kd_icl` được eval đúng deployment mode của nó: k=3 demonstrations lấy từ
private pool của từng client. Đối chiếu `fed_kd` eval zero-shot. Seed 0.

| Private demo pool | `fed_kd_icl` | Δ vs `fed_kd` (63,35) | p |
|---|---:|---:|---:|
| Client 1 | 61,03 | −2,32 | 0,083 |
| Client 2 | 60,15 | −3,19 | 0,014 |
| Client 3 | 59,96 | −3,38 | 0,007 |
| Client 4 | 61,03 | −2,32 | 0,083 |
| Client 5 | 61,51 | −1,84 | 0,173 |
| **Trung bình** | **60,74 ± 0,65** | **−2,61** | 2/5 pool đạt p<0,05 |

**`fed_kd_icl` thấp hơn `fed_kd` 2,61 EX.** Cả 5 private pool đều âm.

### 1.2 ICL cho gain âm ở mọi phép đo

| Phép đo | Δ | p |
|---|---:|---:|
| `fed_kd_icl` vs `fed_kd`, mỗi arm ở deployment mode của nó | −2,61 | 2/5 < 0,05 |
| Thêm demonstrations lúc inference (model train có ICL) | −3,87 | 0,003 |
| Adapter sau FedAvg, trước KD: nhánh ICL vs không ICL | −2,90 | 0,008 |
| Train có ICL rồi eval zero-shot | +0,68 | 0,401 |

Bảng train × eval, giải thích cơ chế:

| Train | Eval k=0 | Eval k=3 | Δ khi thêm demos |
|---|---:|---:|---:|
| Có ICL | 63,93 | 60,06 | −3,87 (p=0,003) |
| Không ICL | 62,57 | 59,48 | −3,09 (p=0,014) |

Giả thuyết train/eval parity của DAIL-SQL dự đoán model train zero-shot sẽ sụt
mạnh hơn khi gặp demonstrations. Quan sát ngược lại: model train zero-shot sụt
**ít hơn** (−3,09 so với −3,87). Interaction lệch 0,78 EX ngược chiều dự đoán.

Mức sụt tương đương đo được trên một centralized model độc lập (−2,71,
2026-07-29). Ba model, ba công thức train khác nhau, cùng sụt ~3 EX khi thêm
demonstrations — đây là đặc tính của student 1,5B, không phải của cách train.

### 1.3 Chi phí của ICL

| | Không ICL | Có ICL | Tỉ lệ |
|---|---:|---:|---:|
| Client training (5 clients) | 4.100 s | 9.651 s | 2,35× |
| Prompt length | 1.568 ký tự | 2.175 ký tự | 1,39× |
| Latency / query | 0,289 s | 1,224 s | 4,23× |
| Peak GPU memory phía client | 25,9 GB | 28,2 GB | +2,3 GB |

Thêm vào đó, mỗi client phải lưu và index private demo pool khi deploy.

### 1.4 Kết luận phần 1

ICL cho **negative gain** ở mọi phép đo, kèm chi phí 2,35× lúc train và 4,23×
lúc inference. Đề xuất **loại ICL khỏi pipeline**. Tên `Fed-ICKD` và
`FedICL-SQL` cần đổi theo.

Phần còn lại của báo cáo đánh giá pipeline không ICL.

---

## Phần 2 — Pipeline `fed_kd`

3 seeds (0, 1, 2). Mỗi seed train lại toàn bộ 5 clients và chạy lại server KD.

### 2.1 Kết quả và baseline

| Arm | EX |
|---|---:|
| `base` | 50,00 |
| `local` (trung bình 5 clients) | 54,99 |
| `local` (client tốt nhất) | 57,64 |
| `fedavg` | 58,19 ± 1,37 |
| `kd_only` | 61,35 ± 0,88 |
| **`fed_kd`** | **62,74 ± 0,53** |
| `central` (gom hết data, centralized training) | 68,28 |
| `teacher` (7B, inference-only) | 78,72 |

`fed_kd` hơn `base` 12,74 EX, lấp 70% khoảng cách tới `central`.

### 2.2 Ablation từng component

| Cấu hình | EX | Δ vs `fed_kd` | p |
|---|---:|---:|---:|
| `fed_kd` | 62,74 ± 0,53 | — | — |
| Bỏ server KD → `fedavg` | 58,19 ± 1,37 | −4,55 ± 1,75 | **0,046** |
| Bỏ federated → `kd_only` | 61,35 ± 0,88 | −1,39 ± 1,12 | 0,165 |
| Bỏ cả hai → `base` | 50,00 | −12,74 | — |

Δ (`fed_kd` − `kd_only`) theo từng seed:

| Seed | `fed_kd` | `kd_only` | Δ | McNemar |
|---|---:|---:|---:|---:|
| 0 | 63,35 | 61,22 | +2,13 | 0,017 |
| 1 | 62,48 | 60,54 | +1,94 | 0,025 |
| 2 | 62,38 | 62,28 | +0,10 | 1,000 |

**Server KD đạt significance** (p=0,046). **Federated component thì chưa**
(p=0,165): dương ở cả 3 seed, significant riêng lẻ ở 2/3 seed, nhưng
seed-to-seed variance đủ lớn để không qua ngưỡng ở n=3. Effect size d=1,24 →
cần n≈7.

Lưu ý `kd_only` không dùng dữ liệu client nào nhưng vẫn dao động sd=0,88 giữa
các seed. Đây là noise nội tại của server KD (data order, dropout).

Phân rã: `base` → `kd_only` chiếm 11,35 trong tổng 12,74 EX; federated chiếm
1,39. `fedavg` (58,19) thấp hơn `kd_only` (61,35) — federated không tự đủ.
`fed_kd` cao hơn cả hai.

**Lựa chọn trong component KD.** Server KD gồm SeqKD trên teacher SQL rồi thêm
reverse-KL trên logits. Tầng reverse-KL cho +1,71 ± 1,38 (p=0,165, 3 seeds),
dương cả 3 seed. Đây là design choice trong một component, cơ sở lấy từ
[10] KID, không tính là component riêng.

### 2.3 Server KD hội tụ về một điểm

| Seed | `fedavg` | Δ do server KD | `fed_kd` |
|---|---:|---:|---:|
| 0 | 57,35 | +6,00 | 63,35 |
| 1 | 57,45 | +5,03 | 62,48 |
| 2 | 59,77 | +2,61 | 62,38 |

Mức bù của server KD tương quan âm với chất lượng adapter đầu vào; `fed_kd` hội
tụ về ~62,7 bất kể xuất phát điểm. Giải thích vì sao sd của `fed_kd` (0,53) nhỏ
hơn sd của `fedavg` (1,37), và vì sao đóng góp của các bước phía trước khó tách.

Hệ quả: tối ưu aggregation có ROI thấp. Đã kiểm chứng — exact aggregation
(rank K·r, product error = 0) cho +0,68 (p=0,311); optimal rank-r approximation
cho −0,19 (p=0,851); FLoRA-NA không cải thiện ở bất kỳ cấu hình nào.

### 2.4 Hai component mang thông tin bổ sung nhau

Cross-tab `kd_only` × `fed_kd`, seed 0, n=1.034:

| | `fed_kd` đúng | `fed_kd` sai |
|---|---:|---:|
| `kd_only` đúng | 605 | 28 |
| `kd_only` sai | 50 | 351 |

Trong 401 câu `kd_only` sai, `fedavg` trả lời đúng **103 câu (25,7%)**, nhưng
`fed_kd` chỉ giữ được **50**. Union của `kd_only` và `fedavg` đạt **71,18 EX**,
cao hơn `central`.

Hai component mang thông tin bổ sung, nhưng stage order hiện tại — đặt server
KD ở bước cuối — chỉ khai thác được khoảng một nửa.

---

## Phần 3 — Hiện trạng và việc tiếp theo

**Đã xác lập:** pipeline `fed_kd` cho 62,74 ± 0,53, ổn định qua 3 seeds. Server
KD là component duy nhất đạt significance. ICL cho negative gain và được đề
xuất loại bỏ.

**Chưa xác lập:** federated component (p=0,165). Đây là rủi ro chính với bài
báo, vì federated learning là tiền đề của đề tài.

**Đang chạy / kế hoạch:**

1. **Đảo stage order** — server KD trước, client FT + FedAvg sau (~1,5 h). Xuất
   phát từ §2.4: stage chạy cuối giữ được đóng góp, stage chạy trước bị ghi đè.
   Quan sát này đã thấy theo cả hai chiều (LAB_LOG 2026-07-20: khi FT chạy
   cuối thì KD stage mất đóng góp, +0,29, p=0,830).
2. **T=2, T=3** (~8 h). Multi-round warm-start là cơ chế để federated
   contribution tích luỹ; T=1 là chỗ nó yếu nhất theo định nghĩa.
3. **Seeds 3–6** (~21 h) nếu (1) và (2) không nâng được effect size.

**Giới hạn hiện tại.** Phần 2 dùng 3 seeds; ở cỡ này chỉ effect > ~4 EX mới đạt
significance. Phần 1 dùng 1 seed nhưng 5 phép đo độc lập với effect 3–4 EX,
vượt seed variance đo được ở phần 2. Toàn bộ kết quả ở T=1. BIRD chỉ dùng làm
public pool cho KD, không dùng để eval; Spider dev không chung schema nào với
tập train (20 vs 146 databases, giao rỗng).
