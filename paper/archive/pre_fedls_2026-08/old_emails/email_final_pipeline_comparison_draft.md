# Email nháp — so sánh kết quả cuối cùng

**Tiêu đề:** So sánh kết quả cuối cùng: Centralized, FL và FL-KD

Chào Thầy,

Em đã tổng hợp lại kết quả chính, chỉ giữ ba model cuối cùng: Centralized, FL và
FL-KD. Cả ba đều dùng Qwen2.5-1.5B-Instruct và được so sánh tại ba lượt train
trên Spider data.

## 1. Đề xuất bỏ ICL

- Demo lúc inference làm giảm EX ở cả Centralized (`−5,42`) và Federated
  (`−4,64`); train/eval cùng `k=3` không khắc phục được suy giảm.
- Đây đã là cấu hình ICL tốt nhất trong các phương pháp em thử, và xu hướng
  tương tự xuất hiện trên nhiều model.

Vì vậy, em đề xuất bỏ ICL khỏi method chính và chỉ giữ như negative ablation.

## 2. So sánh kết quả cuối cùng

| Model | Cấu hình cuối | EX | EM | Exec. error |
|---|---|---:|---:|---:|
| Centralized | 3 epoch | 67,60 | **62,67** | 15,76% |
| FL | 3 round, pure-FL ablation | *Pending Block K* | *Pending* | *Pending* |
| **FL-KD** | **3 round** | **69,54** | 38,59 | **9,77%** |

Kết luận:

- FL-KD đạt 69,54 EX, hơn Centralized **1,94 EX**. Chênh lệch với FL sẽ được
  điền sau khi Block K hoàn tất.
- FL-KD cũng có execution error thấp nhất: **9,77%**.
- EM sau KD không so sánh trực tiếp với hai model còn lại vì teacher thay đổi
  cách biểu diễn SQL; vì vậy kết luận chính dựa trên EX và execution error.

Trên các bộ robustness, FL-KD cũng bằng hoặc cao hơn Centralized. Em đính kèm
file tổng hợp đầy đủ metric của ba model để Thầy xem thêm.

Em xin ý kiến Thầy về hai điểm:

1. Có nên bỏ ICL khỏi method chính và giữ như negative ablation không?
2. Sau khi có kết quả FL-only, hướng `FL + KD` có đủ giá trị và nên positioning
   như thế nào?

Trân trọng,

[Tên của bạn]

---

## Lưu ý nội bộ trước khi gửi

Block K trong `PIPELINE_NEXT.md` chạy nhánh FL-only độc lập qua ba round. Không
điền 66,05 vào hàng FL: đó là adapter sau FedAvg của round 3 trong pipeline
FL-KD và đã kế thừa hai server-KD stage trước đó.
