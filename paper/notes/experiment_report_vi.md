# ICL vs no-ICL — 12/08/2026

Hai pipeline đồng nhất mọi tham số trừ khối `client ICL`. Giá trị lấy từ
`train_config` trong `metrics.json` của hai run `federated__fedkd__s0__*`.

| | `fed_kd` | `fed_kd_icl` |
|---|---|---|
| Student / Teacher | Qwen2.5-1.5B-Instruct / Qwen2.5-Coder-7B-Instruct, frozen | ← |
| Federated | K=5, non-IID Dirichlet α=0,5, T=1, FedAvg weighted by `n_i` | ← |
| Client training | LoRA r=16, lr 2e-4, 1 epoch, effective batch 16 | ← |
| Server KD | reverse-KL trên BIRD, 3.873 mẫu teacher-generated, execution-verified | ← |
| **Client demos** | **không** | **k=3, `dail_weighted`, private pool** |
| **Eval** | **zero-shot** | **k=3, `pool_mode=per_client`** |
| **EX** | **63,35** | **60,74 ± 0,65** |

Eval: Spider dev, n=1034, greedy, seed 0.

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
