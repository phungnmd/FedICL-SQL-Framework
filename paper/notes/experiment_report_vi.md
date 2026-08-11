# ICL vs no-ICL — 12/08/2026

## Setup

Hai pipeline đồng nhất mọi tham số trừ khối `client ICL`. Tên trường lấy đúng
theo `train_config` trong `metrics.json` của từng run.

### Models

| | |
|---|---|
| `model_id` | `Qwen/Qwen2.5-1.5B-Instruct` |
| `teacher_model` | `Qwen/Qwen2.5-Coder-7B-Instruct` |
| `teacher_4bit` | `true` (frozen) |
| `lora_r` / `lora_alpha` / `lora_dropout` | 16 / 32 / 0,05 |
| `target_modules` | `q_proj k_proj v_proj o_proj gate_proj up_proj down_proj` |

### Federated

| | |
|---|---|
| `split_dir` | `SPIDER/federated_noniid/alpha_0.5/k5` |
| `n_clients` / `rounds` / `local_epochs` | 5 / 1 / 1 |
| `client_sizes` | 2377, 986, 2749, 1637, 910 |
| `aggregation` | `factor_fedavg`, trọng số `[0,2745 0,1139 0,3175 0,1891 0,1051]` |
| `init_adapter` | `None` (round 1 từ base) |

### Client training (chung cả hai pipeline)

| | |
|---|---|
| `lr` / `epochs` / `batch_size` / `grad_accum` | 2e-4 / 1 / 1 / 16 |
| `warmup_ratio` / `max_len` / `save_steps` | 0,03 / 2560 / 200 |
| `schema_style` / `demo_style` | `full` / `never_schema` |
| `kd_direction` | `none` (client chỉ CE trên gold) |

### Client ICL — biến duy nhất khác nhau

| | `fed_kd` | `fed_kd_icl` |
|---|---|---|
| `train_k` | 0 | 3 |
| `demo_k_fixed` | — | `true` |
| `retrieval` | — | `dail_weighted` |
| `embedder` | — | `BAAI/bge-small-en-v1.5` |
| `tau` / `dail_alpha` / `dail_shortlist` | — | 0,85 / 0,6 / 32 |
| `demo_loss` | — | `false` |
| Nguồn demo | — | private pool của chính client |

### Server KD (chung cả hai pipeline)

| | |
|---|---|
| `pool` | `BIRD/bootstrap_full_exmatch/train.csv`, 3.873 mẫu |
| Target | SQL do teacher sinh, execution-verified (không dùng BIRD gold) |
| `kd_direction` / `k_teacher` | `rkd` / 0 |
| `lambda_ft` / `lambda_kd` | 1,0 / 1,0 |
| `kl_temperature` / `rkl_skew_lambda` | 1,0 / 0,0 |
| `lr` / `epochs` / `batch_size` / `grad_accum` | 2e-4 / 1 / 1 / 16 |
| `teacher_logit_cache` | `rkd_k0_full` |

### Eval

| | |
|---|---|
| `test_csv` | `SPIDER/centralized/test.csv`, `n_eval` = 1034 |
| Decoding / `overlay` / `batch_size` | greedy / `none` / 16 |
| Chỉ số | EX (execution accuracy) |
| `fed_kd` | `k` = 0 |
| `fed_kd_icl` | `k` = 3, `pool_mode` = `per_client`, `k_clients` = 5 |
| `seed` | 0 |
| Kiểm định | McNemar exact, ghép cặp trên từng câu |

---

## Kết quả

**ICL thấp hơn 2,61 EX.**

| Pipeline | EX |
|---|---:|
| `fed_kd_icl` | 60,74 ± 0,65 |
| `fed_kd` | **63,35** |

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
