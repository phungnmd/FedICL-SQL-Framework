# Email cập nhật tiến độ FedLS-SQL

**Tiêu đề:** Cập nhật tiến độ và kết quả chính của FedLS-SQL

Chào Thầy,

Cc anh Vinh,

Em xin cập nhật tiến độ thực nghiệm FedLS-SQL theo outline Thầy đã gửi. Cấu
hình chính dùng Qwen2.5-1.5B cho student, Qwen2.5-Coder-7B cho teacher, 5
clients và không dùng ICL. Metric chính là Execution Accuracy (EX).

## 1. Kết quả chính trên Spider

Spider dev có 1.034 mẫu. Centralized được train liên tục 3 epoch; FL và
FedLS-SQL chạy 3 federated rounds, mỗi round client train 1 local epoch.

| Model | Cấu hình | EX | EM | Exec. error |
|---|---|---:|---:|---:|
| Centralized | 3 epoch | 67,31 | 64,41 | 14,31% |
| FL | FedAvg-LoRA, 3 round | 64,31 | 57,45 | 18,67% |
| **FedLS-SQL** | FedAvg-LoRA + server KD, 3 round | **69,54** | 38,59 | **9,77%** |

FedLS-SQL cao hơn FL **5,23 EX** với 121 câu cải thiện và 67 câu giảm, kiểm
định paired `p=0,0001`. So với Centralized, FedLS-SQL cao hơn 2,22 EX nhưng
chênh lệch chưa có ý nghĩa thống kê (`p=0,0865`), nên kết luận hiện tại là
FedLS-SQL cạnh tranh được với Centralized và tốt hơn rõ ràng so với FL.

EM được giữ như metric phụ. Teacher sinh target từ BIRD nên có thể tạo SQL đúng
kết quả nhưng khác dạng biểu diễn so với Spider; vì vậy kết luận chính dựa trên
EX và execution error.

## 2. Độ ổn định và non-IID

| Thiết lập | FL EX | FedLS-SQL EX | Chênh lệch | Paired p |
|---|---:|---:|---:|---:|
| Main split, seed 0 | 64,31 | **69,54** | **+5,23** | 0,0001 |
| Main split, seed 1 | 61,99 | **65,76** | **+3,77** | 0,00483 |
| Domain skew mạnh hơn, seed 0 | 63,64 | **68,28** | **+4,64** | 0,000367 |

Kết quả dương ở cả hai training seeds. Với split có semantic-domain skew mạnh
hơn, FedLS-SQL vẫn tăng 4,64 EX và giảm execution error từ 192 xuống 96.

Trên các bộ kiểm tra khác, FedLS-SQL cũng cao hơn FL: Realistic +3,55 EX, Syn
+3,58, DK +5,98 và BIRD +8,67.

## 3. Vai trò của large-to-small transfer

| Model family | FL | Teacher-target CE | Full FedLS-SQL |
|---|---:|---:|---:|
| Qwen 1.5B/7B | 57,35 | 61,32 | **63,35** |
| Gemma 2B/9B | 57,16 | 61,22 | **61,41** |

Teacher-target CE cải thiện EX trên cả Qwen và Gemma. Phần reverse KL tăng
thêm trên Qwen nhưng gần như không tăng trên Gemma, nên đóng góp ổn định nhất
của phương pháp là teacher-generated SQL đã được kiểm tra bằng execution.

FedProx-LoRA cũng đã được chạy làm baseline. Kết quả T3 là 62,77 EX, thấp hơn
FL 64,31 EX, nên hiện tại em giữ FedAvg-LoRA trong method chính.

## 4. Communication và resource

- Mỗi client chỉ train và truyền LoRA adapter gồm 18,46 triệu tham số, khoảng
  70,44 MiB. Tổng upload và broadcast của 5 clients là 704,38 MiB mỗi round,
  tương đương 2,064 GiB qua 3 rounds.
- Trên cùng protocol inference, student 1.5B đạt 0,787 giây/câu, nhanh hơn
  teacher 7B 4-bit 2,09 lần và dùng ít hơn 48,73% peak allocated VRAM.
- Private data và schema vẫn ở client; server chỉ nhận adapter. Secure Sum
  wrapper cũng đã được kiểm tra tương đương số học với weighted FedAvg.

Như vậy, các phần chính trong outline gồm overall performance, ablation,
convergence, non-IID, model-family replication, communication và resource đã
có kết quả. Em đang chuyển sang hoàn thiện bản thảo, bảng, hình và rà soát lại
claim. Seed 2 ở T3 có thể chạy thêm để đủ ba seeds, nhưng hiện không làm thay
đổi định hướng chính của bài.

Em gửi Thầy xem và cho em ý kiến về phạm vi thực nghiệm hiện tại để em chốt bản
thảo.

Trân trọng,

[Tên của bạn]
