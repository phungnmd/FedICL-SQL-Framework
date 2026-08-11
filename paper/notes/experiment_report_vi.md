# ICL vs no-ICL — 12/08/2026

Hai pipeline đồng nhất mọi tham số trừ khối `client ICL`. Giá trị lấy từ
`train_config` trong `metrics.json` của hai run `federated__fedkd__s0__*`.

| | `fed_kd` | `fed_kd_icl` |
|---|---|---|
| `model_id` | `Qwen/Qwen2.5-1.5B-Instruct` | ← |
| `teacher_model` / `teacher_4bit` | `Qwen2.5-Coder-7B-Instruct` / `true`, frozen | ← |
| `lora_r` / `lora_alpha` / `lora_dropout` | 16 / 32 / 0,05 | ← |
| `target_modules` | `q,k,v,o,gate,up,down_proj` | ← |
| `split_dir` | `federated_noniid/alpha_0.5/k5` | ← |
| `n_clients` / `rounds` / `local_epochs` | 5 / 1 / 1 | ← |
| `client_sizes` | 2377, 986, 2749, 1637, 910 | ← |
| `aggregation` | `factor_fedavg`, weighted by `n_i` | ← |
| `lr` / `batch_size` / `grad_accum` / `max_len` | 2e-4 / 1 / 16 / 2560 | ← |
| `schema_style` / `demo_style` | `full` / `never_schema` | ← |
| **`train_k`** | **0** | **3** |
| **`retrieval`** | — | **`dail_weighted`**, private pool của client |
| **`demo_k_fixed`** / **`embedder`** | — | **`true`** / **`bge-small-en-v1.5`** |
| **`tau`** / **`dail_alpha`** / **`dail_shortlist`** | — | **0,85 / 0,6 / 32** |
| Server KD `pool` | BIRD, 3.873 mẫu, teacher-generated, execution-verified | ← |
| Server KD `kd_direction` / `k_teacher` | `rkd` / 0 | ← |
| Server KD `lambda_ft` / `lambda_kd` | 1,0 / 1,0 | ← |
| Eval `test_csv` / `n_eval` | Spider dev / 1034 | ← |
| Eval decoding / `batch_size` / `seed` | greedy / 16 / 0 | ← |
| **Eval `k`** | **0** | **3, `pool_mode=per_client`** |
| **EX** | **63,35** | **60,74 ± 0,65** |

Mỗi pipeline eval đúng deployment mode của nó. **ICL thấp hơn 2,61 EX.**

Eval lặp trên cả 5 private demo pool: 61,03 / 60,15 / 59,96 / 61,03 / 61,51 —
5/5 đều thấp hơn, 2/5 đạt p<0,05.

**Bốn phép đo, không phép nào ủng hộ ICL:**

| | Δ | p |
|---|---:|---:|
| Hai pipeline, mỗi cái ở deployment mode của nó | −2,61 | 2/5 pool <0,05 |
| Thêm demos lúc inference | −3,87 | 0,003 |
| Adapter sau FedAvg, trước server KD | −2,90 | 0,008 |
| Train có ICL rồi eval zero-shot | +0,68 | 0,401 |

Phép đo cuối loại trừ đường lùi "train có ICL vẫn hữu ích nếu bỏ demos lúc
deploy" — không phân biệt được.

**Cơ chế.** Model train zero-shot sụt **ít hơn** khi gặp demos (−3,09) so với
model train có ICL (−3,87). Ngược với giả thuyết train/eval parity của
DAIL-SQL. Ba model độc lập, ba công thức training, cùng sụt ~3 EX — đặc tính
của student 1,5B, không cấu hình training nào khắc phục được.

**Chi phí.** ICL đắt hơn 2,35× lúc training, 4,23× lúc inference, prompt dài
hơn 39%, và mỗi client phải lưu + index private demo pool khi deploy.

**Đề xuất.** Loại ICL khỏi pipeline; tên `Fed-ICKD` / `FedICL-SQL` cần đổi theo.

Kết quả trên 1 seed, nhưng effect 2,6–3,9 EX lớn hơn nhiều so với seed variance
đo được trên pipeline không ICL (sd 0,53 qua 3 seeds).
