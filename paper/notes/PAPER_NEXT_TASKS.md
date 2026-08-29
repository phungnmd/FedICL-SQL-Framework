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
| Reviewer baseline | Đã implement, chờ GPU | FedProx-LoRA đã khóa thiết kế/test; còn smoke và một production run. |
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
| 1 | **P1.5 FedProx-LoRA** | Kiểm tra FedLS có còn lợi thế khi so với optimizer FL mạnh hơn FedAvg. | GPU smoke, sau đó một production run | P1.5a-R three-step smoke GPU-ready; `897fb66`, 334 tests pass |
| 2 | **P1.3 stronger-skew T1** | Kiểm tra kết luận có giữ được dưới một mức heterogeneous mạnh hơn. | CPU tạo/audit split, sau đó GPU train/eval | Chưa GPU-ready |
| 3 | **P0.8b seed 2 T3** | Chuyển kết quả cuối từ hai seed dương thành báo cáo ba seed có mean/SD. | GPU train rounds 2–3 + eval | Chờ legacy plaintext setup compatibility |
| 4 | **P2.2 tables/figures** | Biến evidence hiện có thành các bảng và hình của manuscript. | CPU | Có thể làm song song; P1.8 cell đã đóng |
| 5 | **P2.3 reviewer QA/freeze** | Bảo đảm mỗi claim có artifact, limitation và SHA tương ứng. | CPU | Làm sau các gate thực nghiệm |

P1.3 chỉ mở rộng T3 nếu T1 cho tín hiệu dương và diễn giải được. Nếu không,
dừng và giới hạn RQ3 về split chính. Federated 7B, teacher ceiling và các sweep
model/rank/client/public-pool không thuộc gói mặc định.

## GPU queue — nhìn mục này khi GPU vừa trống

### GPU-READY NOW

P1.8a đã xong và không còn chặn GPU. **P1.5a-R là job GPU-ready hiện tại**;
lệnh duy nhất nằm trong `PIPELINE_NEXT.md`. P0.8b vẫn cần backward
compatibility với setup plaintext cũ.

### GPU TASKS CHƯA READY

1. **P0.8b — seed 2 final T3**
   - Chờ: legacy plaintext setup compatibility; không chờ Secure Sum.
   - Sau khi mở lại: tiếp tục rounds 2–3, không restart round 1.

2. **P1.5b FedProx-LoRA production**
   - Chờ: chạy và review P1.5a-R three-step smoke; two-step root chỉ là diagnostic.
   - Sau khi smoke pass mới thêm đúng một lệnh T3 production.

3. **P1.3 stronger-skew FL/FedLS T1**
   - Chờ: split cố định-row được tạo và audit entropy/JSD/client sizes.
   - Production đầu tiên chỉ là T1.

4. **P1.3 stronger-skew T3 extension — conditional**
   - Chỉ chạy nếu T1 qua promotion gate; nếu không thì task bị hủy.

## Quy tắc sử dụng GPU trống

- Nếu một job GPU-ready tồn tại, ưu tiên chạy nó thay vì để GPU rảnh chỉ vì
  một task khoa học ưu tiên cao hơn còn mắc ở CPU preflight.
- Không chạy smoke/production chưa có fingerprint và resume contract.
- Không chạy song song hai job nặng trên cùng GPU.
- Sau mỗi job: push compact results, pull về local, phân tích rồi mới kích hoạt
  gate tiếp theo.
