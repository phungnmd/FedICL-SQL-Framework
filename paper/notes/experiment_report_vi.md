# ICL vs no-ICL pipeline — 12/08/2026

## 1. Thực nghiệm

Hai pipeline chạy song song, đồng nhất mọi yếu tố trừ một biến: client có train
kèm demonstrations hay không.

| | |
|---|---|
| Student / Teacher | Qwen2.5-1.5B-Instruct (LoRA r=16) / Qwen2.5-Coder-7B-Instruct, 4-bit, frozen |
| Federated | K=5 clients, non-IID Dirichlet α=0,5, T=1 round, FedAvg |
| Server KD | SeqKD + reverse-KL trên public pool BIRD (3.873 mẫu, teacher-generated, execution-verified) |
| Eval | Spider dev, n=1.034, greedy, EX |
| Kiểm định | McNemar exact, ghép cặp trên từng câu |
| Seed | 0 |

| Pipeline | Client training | Inference |
|---|---|---|
| `fed_kd_icl` | k=3 demonstrations từ private pool của client | k=3 demonstrations từ private pool |
| `fed_kd` | zero-shot | zero-shot |

---

## 2. Kết quả

Mỗi pipeline eval đúng deployment mode của nó.

| Pipeline | EX |
|---|---:|
| `fed_kd_icl` | 60,74 ± 0,65 |
| **`fed_kd`** | **63,35** |
| | **−2,61** |

`fed_kd_icl` được eval lặp trên cả 5 private demo pool:

| Private pool | EX | Δ | p |
|---|---:|---:|---:|
| Client 1 | 61,03 | −2,32 | 0,083 |
| Client 2 | 60,15 | −3,19 | **0,014** |
| Client 3 | 59,96 | −3,38 | **0,007** |
| Client 4 | 61,03 | −2,32 | 0,083 |
| Client 5 | 61,51 | −1,84 | 0,173 |

5/5 pool âm, 2/5 đạt p<0,05.

---

## 3. ICL cho gain âm ở mọi phép đo

| Phép đo | Δ | p |
|---|---:|---:|
| Hai pipeline, mỗi cái ở deployment mode của nó | −2,61 | 2/5 pool <0,05 |
| Thêm demonstrations lúc inference (model train có ICL) | −3,87 | 0,003 |
| Adapter sau FedAvg, trước server KD | −2,90 | 0,008 |
| Train có ICL rồi eval zero-shot | +0,68 | 0,401 |

Phép đo cuối loại trừ khả năng "train có ICL vẫn hữu ích nếu bỏ demonstrations
lúc deploy": chênh lệch không phân biệt được.

---

## 4. Cơ chế

| Client training | Eval k=0 | Eval k=3 | Δ khi thêm demos |
|---|---:|---:|---:|
| Có ICL | 63,93 | 60,06 | −3,87 (p=0,003) |
| Không ICL | 62,57 | 59,48 | −3,09 (p=0,014) |

Giả thuyết train/eval parity của DAIL-SQL dự đoán model train zero-shot sụt
mạnh hơn khi gặp demonstrations. Quan sát ngược lại: model train zero-shot sụt
**ít hơn** (−3,09 so với −3,87), interaction lệch 0,78 EX ngược chiều dự đoán.

Mức sụt tương đương đo trên một centralized model độc lập (−2,71, 2026-07-29).
Ba model, ba công thức training khác nhau, cùng sụt ~3 EX khi thêm
demonstrations. Đây là đặc tính của student 1,5B, không phải của cách training,
nên không cấu hình training nào khắc phục được.

---

## 5. Chi phí

| | `fed_kd` | `fed_kd_icl` | Tỉ lệ |
|---|---:|---:|---:|
| Client training (5 clients) | 4.100 s | 9.651 s | 2,35× |
| Prompt length | 1.568 ký tự | 2.175 ký tự | 1,39× |
| Latency / query | 0,289 s | 1,224 s | 4,23× |
| Peak GPU memory phía client | 25,9 GB | 28,2 GB | +2,3 GB |

Thêm vào đó, mỗi client phải lưu và index private demo pool khi deploy.

---

## 6. Kết luận

ICL cho gain âm ở mọi phép đo, kèm chi phí 2,35× lúc training và 4,23× lúc
inference. **Đề xuất loại ICL khỏi pipeline.** Tên `Fed-ICKD` và `FedICL-SQL`
cần đổi theo.

Kết quả trên 1 seed, nhưng dựa trên 4 phép đo độc lập với effect 2,6–3,9 EX —
lớn hơn seed variance đo được trên pipeline không ICL (sd 0,53 qua 3 seeds).
