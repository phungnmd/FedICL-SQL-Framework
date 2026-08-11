# Kết quả thực nghiệm: ICL và đóng góp của từng thành phần

## 1. Thiết lập

| Hạng mục | Giá trị |
|---|---|
| Student | Qwen2.5-1.5B-Instruct, LoRA r=16, α=32 |
| Teacher | Qwen2.5-Coder-7B-Instruct, 4-bit, đóng băng |
| Phân hoạch | K=5 client, non-IID Dirichlet α=0,5, 910–2.749 mẫu/client |
| Kho công khai P | BIRD, 3.873 mẫu, nhãn là SQL do teacher sinh và đã kiểm tra bằng thực thi |
| Vòng | T=1 |
| Tập đánh giá | Spider dev, n=1.034, không chung schema với tập huấn luyện |
| Chỉ số | EX (execution accuracy), giải mã greedy |
| Kiểm định | McNemar chính xác trong một seed; kiểm định t ghép cặp giữa các seed |
| Số seed | 3 (0, 1, 2) cho §4; 1 cho §3 |

Ký hiệu cấu hình:

| Ký hiệu | Mô tả |
|---|---|
| `M_base` | Student chưa huấn luyện |
| `M_fed` | Client huấn luyện cục bộ → FedAvg. Không chưng cất |
| `M_kd` | `M_base` → chưng cất trên P. Không dùng dữ liệu riêng |
| `M_full` | Client huấn luyện cục bộ → FedAvg → chưng cất trên P |
| `M_full+ICL` | Như `M_full`, client huấn luyện kèm k=3 ví dụ mẫu từ kho riêng |

---

## 2. Kết quả chính

**Bảng 1.** EX trên Spider dev, trung bình ± độ lệch chuẩn qua 3 seed.

| Cấu hình | EX |
|---|---|
| `M_base` | 50,00 |
| `M_fed` | 58,19 ± 1,37 |
| `M_kd` | 61,35 ± 0,88 |
| **`M_full`** | **62,74 ± 0,53** |
| Huấn luyện tập trung (`central_rkd`) | 68,28 |
| Teacher 7B | 78,72 |

`M_full` đạt 62,74, cao hơn `M_base` 12,74 điểm, và lấp 70% khoảng cách giữa
`M_base` và mốc huấn luyện tập trung.

---

## 3. Ablation 1 — thành phần ICL

Hai pipeline chạy song song, đồng nhất mọi yếu tố trừ việc client có dùng ví dụ
mẫu khi huấn luyện hay không: cùng phân hoạch, seed, kho công khai, bước máy
chủ, ngân sách huấn luyện. Seed 0.

### 3.1 So sánh ở chế độ triển khai tương ứng

`M_full+ICL` được đánh giá với k=3 ví dụ mẫu lấy từ kho riêng của từng client,
đúng chế độ nó được thiết kế; `M_full` đánh giá zero-shot.

**Bảng 2.** `M_full+ICL` theo từng kho ví dụ riêng, đối chiếu `M_full` = 63,35.

| Kho ví dụ | EX | Δ | p |
|---|---:|---:|---:|
| Client 1 | 61,03 | −2,32 | 0,083 |
| Client 2 | 60,15 | −3,19 | 0,014 |
| Client 3 | 59,96 | −3,38 | 0,007 |
| Client 4 | 61,03 | −2,32 | 0,083 |
| Client 5 | 61,51 | −1,84 | 0,173 |
| Trung bình | 60,74 ± 0,65 | −2,61 | — |

Cả 5 kho đều âm; 2 đạt p < 0,05.

Trường hợp không khớp chế độ — huấn luyện có ICL, đánh giá zero-shot — cho
64,02 so với 63,35, Δ = +0,68, p = 0,401.

### 3.2 Tương tác huấn luyện × đánh giá

**Bảng 3.** EX theo cấu hình huấn luyện và cấu hình đánh giá.

| Huấn luyện | Đánh giá k=0 | Đánh giá k=3 | Δ khi thêm ví dụ |
|---|---:|---:|---:|
| Có ICL | 63,93 | 60,06 | −3,87 (p = 0,003) |
| Không ICL | 62,57 | 59,48 | −3,09 (p = 0,014) |

Hai quan sát:

1. Thêm ví dụ mẫu lúc suy luận làm giảm EX ở cả hai cấu hình huấn luyện.
2. Huấn luyện kèm ví dụ mẫu không giảm được mức sụt đó. Giả thuyết
   train/eval-parity của DAIL-SQL dự đoán mô hình huấn luyện zero-shot sẽ sụt
   mạnh hơn; quan sát cho kết quả ngược lại (−3,09 so với −3,87), tương tác
   lệch 0,78 điểm theo chiều ngược dự đoán.

Mức sụt tương tự đo được trên một mô hình centralized độc lập (−2,71,
2026-07-29). Ba mô hình, ba công thức huấn luyện, cùng sụt khoảng 3 điểm khi
thêm ví dụ mẫu.

Trước bước chưng cất, nhánh ICL cho bản gộp kém hơn: 54,45 so với 57,35,
Δ = −2,90, p = 0,008; lỗi thực thi 258 so với 236.

### 3.3 Chi phí

**Bảng 4.** Chi phí bổ sung của thành phần ICL.

| | Không ICL | Có ICL | Tỉ lệ |
|---|---:|---:|---:|
| Huấn luyện 5 client | 4.100 s | 9.651 s | 2,35× |
| Độ dài prompt | 1.568 ký tự | 2.175 ký tự | 1,39× |
| Độ trễ mỗi truy vấn | 0,289 s | 1,224 s | 4,23× |
| Bộ nhớ GPU đỉnh phía client | 25,9 GB | 28,2 GB | +2,3 GB |

Ngoài ra mỗi client phải lưu và đánh chỉ mục kho ví dụ riêng khi triển khai.

### 3.4 Kết luận

Năm phép đo, không phép nào ủng hộ ICL:

| Phép đo | Δ | p |
|---|---:|---:|
| `M_full+ICL` so với `M_full`, mỗi bên ở chế độ tương ứng | −2,61 | 2/5 kho < 0,05 |
| Ví dụ mẫu lúc suy luận (mô hình huấn luyện có ICL) | −3,87 | 0,003 |
| Bản gộp trước chưng cất | −2,90 | 0,008 |
| Tương tác train × eval (bác bỏ DAIL-SQL) | −0,78 | — |
| Huấn luyện có ICL, đánh giá zero-shot | +0,68 | 0,401 |

Đề xuất loại ICL khỏi phương pháp. Tên `Fed-ICKD` và `FedICL-SQL` cần đổi theo.

---

## 4. Ablation 2 — thành phần liên kết và chưng cất

3 seed; mỗi seed huấn luyện lại toàn bộ 5 client và chạy lại bước chưng cất.

**Bảng 5.** Loại bỏ từng thành phần khỏi `M_full`.

| Cấu hình | EX | Δ so với `M_full` | p |
|---|---:|---:|---:|
| `M_full` | 62,74 ± 0,53 | — | — |
| Bỏ chưng cất → `M_fed` | 58,19 ± 1,37 | −4,55 ± 1,75 | 0,046 |
| Bỏ liên kết → `M_kd` | 61,35 ± 0,88 | −1,39 ± 1,12 | 0,165 |
| Bỏ cả hai → `M_base` | 50,00 | −12,74 | — |

**Bảng 6.** Δ (`M_full` − `M_kd`) theo từng seed.

| Seed | `M_full` | `M_kd` | Δ | McNemar trong seed |
|---|---:|---:|---:|---:|
| 0 | 63,35 | 61,22 | +2,13 | 0,017 |
| 1 | 62,48 | 60,54 | +1,94 | 0,025 |
| 2 | 62,38 | 62,28 | +0,10 | 1,000 |

Thành phần chưng cất đạt ý nghĩa thống kê (p = 0,046). Thành phần liên kết
chưa: điểm ước lượng +1,39, dương ở cả 3 seed và đạt ý nghĩa riêng lẻ ở 2 seed,
nhưng biến thiên giữa các seed đủ lớn để p = 0,165 ở n=3. Với độ lớn hiệu ứng
d = 1,24, cần n ≈ 7 để đạt lực thống kê 80%.

`M_kd` không dùng dữ liệu client nhưng vẫn dao động sd = 0,88 giữa các seed;
đây là nhiễu nội tại của bước chưng cất (thứ tự dữ liệu, dropout), không phải
nhiễu của phần liên kết.

Phân rã mức tăng: `M_base` → `M_kd` chiếm 11,35 trên tổng 12,74 điểm; phần liên
kết chiếm 1,39. `M_fed` (58,19) thấp hơn `M_kd` (61,35), tức liên kết không tự
đủ; `M_full` cao hơn cả hai.

**Lựa chọn bên trong thành phần chưng cất.** Bước này gồm SeqKD trên SQL của
teacher rồi thêm reverse-KL trên logit. Tầng reverse-KL cho +1,71 ± 1,38
(p = 0,165, 3 seed), dương ở cả ba seed. Đây là lựa chọn thiết kế trong một
thành phần, không phải một thành phần riêng; cơ sở lấy từ [10] KID.

---

## 5. Phân tích

### 5.1 Bước chưng cất hội tụ về một điểm

| Seed | `M_fed` | Δ do chưng cất | `M_full` |
|---|---:|---:|---:|
| 0 | 57,35 | +6,00 | 63,35 |
| 1 | 57,45 | +5,03 | 62,48 |
| 2 | 59,77 | +2,61 | 62,38 |

Mức bù của bước chưng cất tương quan âm với chất lượng bản gộp đầu vào, và
`M_full` hội tụ về khoảng 62,7 bất kể điểm xuất phát. Điều này giải thích vì
sao sd của `M_full` (0,53) nhỏ hơn sd của `M_fed` (1,37), và vì sao đóng góp
của các bước phía trước khó tách.

Hệ quả: cải thiện thuật toán gộp có lợi tức thấp. Thực nghiệm dựng phép gộp
chính xác (rank K·r, sai số tích bằng 0) cho +0,68, p = 0,311; xấp xỉ rank-r
tối ưu cho −0,19, p = 0,851. FLoRA-NA không cải thiện ở bất kỳ cấu hình nào.

### 5.2 Tính bổ sung giữa hai thành phần

**Bảng 7.** Bảng chéo `M_kd` × `M_full`, seed 0, n = 1.034.

| | `M_full` đúng | `M_full` sai |
|---|---:|---:|
| `M_kd` đúng | 605 | 28 |
| `M_kd` sai | 50 | 351 |

Trong 401 câu `M_kd` trả lời sai, `M_fed` trả lời đúng 103 câu (25,7%), nhưng
`M_full` chỉ giữ được 50. Hợp của `M_kd` và `M_fed` đạt 71,18 EX, cao hơn cả
mốc huấn luyện tập trung.

Tức là hai thành phần mang thông tin bổ sung cho nhau, nhưng pipeline hiện tại
— đặt chưng cất ở bước cuối — chỉ khai thác được khoảng một nửa. Đây là hướng
cần thử tiếp: đảo thứ tự để bước liên kết chạy sau.

### 5.3 Gộp so với client đơn lẻ

| | EX |
|---|---:|
| Client yếu nhất | 53,38 |
| Trung bình 5 client | 54,99 |
| Client mạnh nhất | 57,64 |
| `M_fed` (sau gộp) | 57,35 |

Bản gộp cao hơn trung bình client 2,36 điểm và thấp hơn client mạnh nhất 0,29
điểm. Danh tính client mạnh nhất không xác định được trước khi đánh giá.

---

## 6. Giới hạn

1. **Cỡ mẫu.** §4 dùng 3 seed; ở cỡ này chỉ hiệu ứng lớn hơn khoảng 4 điểm mới
   đạt ý nghĩa. §3 dùng 1 seed nhưng 6 phép đo độc lập với độ lớn 3–4 điểm,
   vượt biến thiên seed đo được ở §4.
2. **Số vòng.** Toàn bộ kết quả ở T=1. T=2 và T=3 đang chạy.
3. **Thành phần liên kết chưa đạt ý nghĩa thống kê** (p = 0,165). Cần n ≈ 7,
   hoặc một cấu hình làm hiệu ứng lớn hơn (nhiều vòng, K lớn hơn, α thấp hơn,
   hoặc đảo thứ tự pipeline theo §5.2).
4. **Phạm vi dữ liệu.** BIRD chỉ dùng làm kho chưng cất, không dùng để đánh
   giá. Spider dev không chung schema với tập huấn luyện (20 so với 146
   database, giao rỗng).
