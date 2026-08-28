# FedLS-SQL — việc còn lại để hoàn thiện paper

> Dashboard ngắn cho vận hành hằng ngày. `PAPER_TODO.md` giữ checklist đầy đủ;
> `PIPELINE_NEXT.md` là nơi duy nhất chứa lệnh PowerShell thực nghiệm.

## Paper hiện đã đủ đến đâu?

| Phần | Trạng thái | Ý nghĩa |
|---|---|---|
| Phương pháp và novelty | Đủ để viết | Method, figure, nearest-work positioning và claim boundary đã chốt. |
| Accuracy và causal evidence | Mạnh | FedLS hơn pure FL ở hai seed T3; matched public-gold/target-CE controls và Gemma portability đã có. |
| Communication/resource | Đủ trong phạm vi đã khai báo | Adapter bytes và deployment inference 1.5B/7B đã đo; không claim training-resource hoặc federated 7B. |
| Reviewer baseline | Còn thiếu | Chưa có optimizer baseline mạnh hơn FedAvg; FedProx-LoRA là gap lớn nhất. |
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
| 1 | **P1.5 FedProx-LoRA** | Kiểm tra FedLS có còn lợi thế khi so với optimizer FL mạnh hơn FedAvg. | CPU implement/test, sau đó GPU smoke + production | Active design; chưa có lệnh GPU |
| 2 | **P1.3 stronger-skew T1** | Kiểm tra kết luận có giữ được dưới một mức heterogeneous mạnh hơn. | CPU tạo/audit split, sau đó GPU train/eval | Chưa GPU-ready |
| 3 | **P0.8b seed 2 T3** | Chuyển kết quả cuối từ hai seed dương thành báo cáo ba seed có mean/SD. | GPU train rounds 2–3 + eval | **GPU-ready ngay; độc lập với P1.5/P1.3** |
| 4 | **P2.2 tables/figures** | Biến evidence hiện có thành các bảng và hình của manuscript. | CPU | Có thể làm song song |
| 5 | **P2.3 reviewer QA/freeze** | Bảo đảm mỗi claim có artifact, limitation và SHA tương ứng. | CPU | Làm sau các gate thực nghiệm |

P1.3 chỉ mở rộng T3 nếu T1 cho tín hiệu dương và diễn giải được. Nếu không,
dừng và giới hạn RQ3 về split chính. Federated 7B, teacher ceiling và các sweep
model/rank/client/public-pool không thuộc gói mặc định.

## GPU queue — nhìn mục này khi GPU vừa trống

### GPU-READY NOW

1. **P0.8b — seed 2 final T3**
   - Mục đích: hoàn thiện ba-seed reliability.
   - Lệnh: đã có trong `PIPELINE_NEXT.md`, single-line PowerShell, fail-fast và
     resume đúng lineage T1 hiện có.
   - Chạy: có thể chạy ngay khi đúng GPU trống; không cần chờ FedProx hoặc
     stronger-skew vì kết quả độc lập.
   - Không được: restart round 1 hoặc thay bằng `run --rounds 3`.

### GPU TASKS CHƯA READY

2. **P1.5 FedProx-LoRA smoke + production**
   - Chờ: objective, hệ số không tune trên test, implementation, unit tests và
     checkpoint fingerprint.
   - Chỉ sau đó mới thêm lệnh vào `PIPELINE_NEXT.md`.

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

