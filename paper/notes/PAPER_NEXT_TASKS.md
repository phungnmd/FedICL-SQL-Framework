# FedLS-SQL — việc còn lại để hoàn thiện paper

> Dashboard ngắn cho vận hành hằng ngày. `PAPER_TODO.md` giữ checklist đầy đủ;
> `PIPELINE_NEXT.md` là nơi duy nhất chứa lệnh PowerShell thực nghiệm.

## Paper hiện đã đủ đến đâu?

| Phần | Trạng thái | Ý nghĩa |
|---|---|---|
| Phương pháp và novelty | Đủ để viết | Method, figure, nearest-work positioning và claim boundary đã chốt. |
| Accuracy và causal evidence | Mạnh | FedLS hơn pure FL ở hai seed T3; matched public-gold/target-CE controls và Gemma portability đã có. |
| Communication/resource | Đủ trong phạm vi đã khai báo | Adapter bytes và deployment inference 1.5B/7B đã đo; không claim training-resource hoặc federated 7B. |
| Privacy boundary | Đủ cho compatibility claim | P1.8 đã replay adapter thật và đo equivalence/overhead; không claim MPC/DP deployment. |
| Reviewer baseline | Đã đóng | FedProx thấp hơn pure FL tại cả T1/T2/T3; không mở FedLS–FedProx. |
| Non-IID sensitivity | Còn thiếu hoặc phải thu hẹp claim | Hiện chỉ có split chính `K=5, alpha=0.5`. |
| Final reliability | Gần đủ | Hai seed T3 đều dương; seed 2 cần cho gói ba-seed mạnh hơn. |
| Paper packaging | Chưa xong | Các bảng/figure cuối, claim audit và artifact freeze còn mở. |

**Đánh giá Q3:** evidence hiện tại đủ để viết một bản thảo có luận điểm rõ và
khả thi, nhưng chưa nên coi là submission-ready. Gói Q3 sẽ vững hơn sau
FedProx-LoRA, một stronger-skew gate hoặc claim RQ3 được thu hẹp rõ, seed 2 nếu
compute cho phép, và reviewer QA. Không có thực nghiệm nào bảo đảm acceptance;
rủi ro chính còn lại là baseline breadth và phạm vi non-IID, không phải EM.

## Danh sách việc tiếp theo

| Thứ tự khoa học | Task | Việc này chứng minh gì? | Compute | Trạng thái |
|---:|---|---|---|---|
| 0 | **P1.8 Secure Sum compatibility** | Chứng minh masked aggregation tương thích weighted FedAvg và lượng hóa overhead riêng. | complete | 18.46M-param replay passed; `6c67e79` |
| 1 | **P1.5 FedProx-LoRA** | Kiểm tra optimizer mạnh hơn FedAvg. | complete | Closed negative: `-1.55` EX, 22/38 gains/losses |
| 2 | **P1.5d FedProx T1/T2 diagnostic** | Kiểm tra FedProx có lợi tạm thời ở round sớm rồi suy giảm hay không. | complete | Không: thấp hơn pure FL `0.87/2.22` EX |
| 3 | **P1.3 stronger-domain-skew T1→T3** | Kiểm tra kết luận dưới domain skew mạnh hơn nhưng quantity skew thấp hơn. | GPU train | T1 passed `+4.06` EX; P1.3d rounds 2–3 ready |
| 4 | **P0.8b seed 2 T3** | Chuyển kết quả cuối từ hai seed dương thành báo cáo ba seed có mean/SD. | GPU train rounds 2–3 + eval | Chờ legacy plaintext setup compatibility |
| 5 | **P2.2 tables/figures** | Biến evidence hiện có thành các bảng và hình của manuscript. | CPU | Có thể làm song song; P1.8 cell đã đóng |
| 6 | **P2.3 reviewer QA/freeze** | Bảo đảm mỗi claim có artifact, limitation và SHA tương ứng. | CPU | Làm sau các gate thực nghiệm |

P1.3 chỉ mở rộng T3 nếu T1 cho tín hiệu dương và diễn giải được. Nếu không,
dừng và giới hạn RQ3 về split chính. Federated 7B, teacher ceiling và các sweep
model/rank/client/public-pool không thuộc gói mặc định.

## GPU queue — nhìn mục này khi GPU vừa trống

### GPU-READY NOW

P1.3c đã qua toàn bộ gate tại `d4d8733`: `+4.06` EX, 129/87 paired
corrections/regressions và giảm execution errors 236→134. P1.3d rounds 2–3
hiện GPU-ready trong `PIPELINE_NEXT.md` thành hai lane độc lập. Chạy cả hai,
publish chung compact results và dừng trước P1.3e evaluation. P0.8b vẫn chờ
backward compatibility với setup plaintext cũ.

### GPU TASKS CHƯA READY

1. **P0.8b — seed 2 final T3**
   - Chờ: legacy plaintext setup compatibility; không chờ Secure Sum.
   - Sau khi mở lại: tiếp tục rounds 2–3, không restart round 1.

2. **P1.5 — complete negative**
   - FedProx thấp hơn pure FL ở T1/T2/T3: `-0.87/-2.22/-1.55` EX.
   - Không chạy OOD, combined FedLS-FedProx, chọn checkpoint hoặc tune `mu`.

3. **P1.3 stronger-domain-skew FL/FedLS T1→T3**
   - Audit passed: cùng 8.659 rows; JSD `0.527→0.805`, entropy `3.029→2.183`.
   - T1 passed all gates; P1.3d independent rounds 2–3 are GPU-ready now.

4. **P1.3e stronger-skew T3 evaluation**
   - Chỉ mở sau khi compact P1.3d training artifacts được pull và review.

## Quy tắc sử dụng GPU trống

- Nếu một job GPU-ready tồn tại, ưu tiên chạy nó thay vì để GPU rảnh chỉ vì
  một task khoa học ưu tiên cao hơn còn mắc ở CPU preflight.
- Không chạy smoke/production chưa có fingerprint và resume contract.
- Không chạy song song hai job nặng trên cùng GPU.
- Sau mỗi job: push compact results, pull về local, phân tích rồi mới kích hoạt
  gate tiếp theo.
