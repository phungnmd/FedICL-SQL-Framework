# FedLS-SQL: các hướng ứng viên

Cập nhật: 2026-11-04. Trạng thái: **owner chưa chọn hướng**. File này thay
cho hướng 2026-10-28 và đề xuất federated CoT-RL 2026-11-03 (cả hai ở
[archive](../archive/directions_2026-11/)). Bằng chứng nền: [RESEARCH_STATE](RESEARCH_STATE.md)
mục 3; closest work: [LITERATURE](LITERATURE.md).

## 1. Bằng chứng định hướng

- RL bằng execution feedback là đòn bẩy lớn nhất đã đo: +15.38 Spider dev từ
  student chỉ train BIRD (R1), và một mình RL đạt mức Spider SFT (R2).
- CoT thua SQL-only khi cùng route RL (-3.29, p=.014, C1) và tốn compute gấp
  khoảng ba lần (C5).
- Soft label của teacher hơn gold trên Spider dev, không do smoothing hay
  anchoring (K2), nhưng trên Spider test chỉ còn khoảng 0.5 điểm (K3).
- FedAvg bào mòn phần học ở server; replay target của teacher giữ được BIRD (K4).
- Chưa thấy paper federated Text-to-SQL nào có RL. Federated RL với verifiable
  reward đã có ở toán và code (FedMOA, PubSwap), không có teacher.

## 2. Hướng A (khuyến nghị): teacher-anchored federated execution RL

```text
Server, BIRD public:  teacher 7B Hinton KD -> G0
Mỗi global round t:   server gửi Gt
                      mỗi client: sinh K=8 SQL trên Spider local, execution check,
                      DPO + NLL local (+ replay target top-50 của teacher trên public subset)
                      FedAvg -> Gt+1
Deploy:               chỉ SLM, chỉ sinh SQL
```

Ý nghĩa của tổ hợp: client drift trong FL là forgetting cục bộ khi mỗi client
fit dữ liệu non-IID của mình. RL on-policy quên ít hơn SFT (Shenfeld et al.
2025; Chu et al. 2025). Giả thuyết: federated execution RL bị non-IID ít hơn
federated SFT, và giữ phần teacher dạy ở server tốt hơn.

| Claim | Comparator |
|---|---|
| A1. Federated RL hơn FedAvg SFT trên Spider | Cùng G0, cùng số round, local DPO so với local SFT |
| A2. Xuất phát từ teacher KD hơn xuất phát từ gold, sau khi qua federated RL | G0 = Hinton K2 so với gold K2 |
| A3. Replay target của teacher giữ BIRD trong federated RL | Replay teacher so với replay gold so với không replay |
| A4 (phụ). Federated RL gần mức RL centralized | `s1`-style centralized cùng điểm xuất phát |

Điểm yếu reviewer sẽ hỏi: phần teacher trên Spider có thể vẫn nhỏ (K3), khi
đó đóng góp teacher chủ yếu nằm ở BIRD (A3). Hướng này dùng lại thành phần
của hướng 2026-10-28 (Hinton K2, replay) nhưng câu chuyện khác: RL ở client,
teacher là điểm xuất phát và neo kiến thức.

Thí nghiệm đầu tiên, centralized, rẻ, quyết định A2 trước khi xây FL: chạy
route `s1` (P2.62, cùng câu hỏi và cài đặt) từ adapter K2 của `hinton_k2aaa`
(P2.37, `artifacts/protocol_v2/p237_phase_e_s0/hinton_k2aaa_k2` trên server,
Spider dev 62.28) thay cho `sql1_e2`. `sql1_e2` gần như là gold K2 (58.80 so
với 59.09 cùng dữ liệu và lr), nên cặp này tách được phần teacher sau RL.
Khoảng 10 GPU-h, một GPU. Đường dẫn adapter cần kiểm trên server trước khi chạy.

Compute cho FL: một global round SQL-only trên khoảng 7,000 câu tốn khoảng
7 GPU-h, tức khoảng 3.5 h wall-clock trên hai card. Mỗi arm 6-8 round khoảng
1-1.5 ngày; 4 arm x 3 seed khoảng 2-3 tuần.

## 3. Hướng B: CoT làm trục chính

Giữ pipeline federated CoT-DPO của đề xuất 2026-11-03 (teacher CoT trên BIRD,
CoT SFT, DPO tại client). Chỉ nên mở lại nếu Spider test đảo kết quả dev C1,
tức `c1_rl8` (69.12 test) không thua `s1_rl9` trên test. Nếu không, CoT là
kết quả âm có giá trị (CoT tự do không giúp SLM 1.5B khi đã có execution RL)
và đặt ở appendix.

## 4. Hướng C: teacher trong vòng RL (mở rộng của A)

Nếu A2 cho thấy teacher yếu trên Spider, đưa teacher vào trực tiếp trong RL ở
server: student sinh SQL trên BIRD, teacher chấm log-prob từng token làm dense
signal (on-policy distillation, GKD, Agarwal et al. ICLR 2024), xen giữa các
round FL. Một biến thể rẻ hơn: pair DPO trên BIRD với chosen là SQL đúng của
teacher và rejected là SQL sai của student (một round off-policy như ExCoT).
GKD đã bị đóng trước đây vì phân trang memory với `full_bf16`; cần đo lại
VRAM với `target_fp32` trước khi chọn.

## 5. Cần owner quyết

1. Chọn A, B, C hay tổ hợp khác.
2. Có chạy Spider test cho `s1_rl9`, `sql_rl9`, `sql2_e1` không (cần mở rộng
   driver test, hiện chỉ nhận `c1_rlN`). Kết quả này quyết định B.

## 6. Venue

Như trước: Data & Knowledge Engineering, International Journal of Data
Science and Analytics, Neural Processing Letters, Distributed and Parallel
Databases; stretch: Journal of Intelligent Information Systems.
