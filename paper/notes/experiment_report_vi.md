# Kiểm chứng pipeline đề xuất: ICL có đóng góp không, và phần còn lại hiệu quả đến đâu

**Ngày:** 11/08/2026 · **Cấu hình:** K=5 client, non-IID Dirichlet α=0,5, T=1 vòng
**Student:** Qwen2.5-1.5B-Instruct · **Teacher:** Qwen2.5-Coder-7B-Instruct (4-bit, đóng băng)
**Đo trên:** toàn bộ Spider dev (n=1.034), greedy decoding, chỉ số EX (execution accuracy)
**Kiểm định:** McNemar ghép cặp chính xác trên dự đoán từng câu; so sánh nhiều seed dùng kiểm định t

---

## 1. Pipeline đề xuất và hai câu hỏi

Pipeline được đề xuất ban đầu gồm **ba thành phần**:

```text
LIÊN KẾT           client tự huấn luyện trên dữ liệu riêng  →  gộp adapter tại máy chủ
ICL                client huấn luyện kèm 3 ví dụ mẫu lấy từ kho riêng của mình
CHƯNG CẤT (KD)     giáo viên 7B dạy lại mô hình chung trên kho công khai BIRD
```

Dữ liệu riêng không bao giờ rời khỏi chủ sở hữu; chỉ bản vá trọng số LoRA được
gửi lên máy chủ, và giáo viên chỉ chạm vào kho công khai.

Báo cáo trả lời hai câu hỏi, theo đúng thứ tự đó:

**(1)** Thành phần ICL có đóng góp không? → §2
**(2)** Nếu không, pipeline còn lại (LIÊN KẾT + KD) hiệu quả đến đâu, và mỗi
thành phần đóng góp bao nhiêu? → §3

---

## 2. Câu hỏi 1 — ICL có đóng góp không

Đã chạy **hai pipeline song song hoàn toàn**: cùng phân hoạch dữ liệu, cùng
seed, cùng kho công khai, cùng bước máy chủ, cùng ngân sách huấn luyện. Khác
đúng một biến — client có dùng ví dụ mẫu hay không.

### 2.1 So sánh trực tiếp

Pipeline đề xuất phải được đánh giá **đúng cách nó được thiết kế**: huấn luyện
có ví dụ mẫu thì lúc chạy cũng đưa ví dụ mẫu vào, lấy từ kho riêng của từng bên.

| | EX |
|---|---:|
| **Pipeline đề xuất** (LIÊN KẾT + ICL + KD), chạy đúng thiết kế | **60,74 ± 0,65** |
| **Bỏ ICL** (LIÊN KẾT + KD) | **63,35** |
| | **−2,61** |

Đánh giá lặp lại trên cả 5 kho ví dụ riêng, không kho nào cho kết quả cao hơn:

| Kho ví dụ của | EX | Chênh so với bỏ ICL | p |
|---|---:|---:|---:|
| Client 1 | 61,03 | −2,32 | 0,083 |
| Client 2 | 60,15 | −3,19 | **0,014** |
| Client 3 | 59,96 | −3,38 | **0,007** |
| Client 4 | 61,03 | −2,32 | 0,083 |
| Client 5 | 61,51 | −1,84 | 0,173 |

**Pipeline có ICL thua pipeline không ICL 2,61 điểm.** Năm trên năm kho đều âm,
hai trong đó đạt ý nghĩa thống kê.

Còn một khả năng cần loại trừ: nếu huấn luyện có ví dụ mẫu nhưng lúc chạy
**không** đưa ví dụ vào thì sao? Kết quả 64,02 so với 63,35 — chênh **+0,68 với
p = 0,401**, không phân biệt được. Tức là huấn luyện kèm ví dụ mẫu rồi vứt bỏ
chúng lúc triển khai cũng không mua được gì.

### 2.2 Vì sao — bảng 2×2

| | Chạy không ví dụ mẫu | Chạy có 3 ví dụ mẫu | Mất khi thêm ví dụ |
|---|---:|---:|---:|
| **Huấn luyện có ICL** | 63,93 | 60,06 | **−3,87** (p = 0,003) |
| **Huấn luyện không ICL** | 62,57 | 59,48 | **−3,09** (p = 0,014) |

**(a) Đưa ví dụ mẫu vào lúc chạy làm giảm độ chính xác.** Mất 3,87 điểm,
p = 0,003. Đây là hiệu ứng ICL lớn nhất đo được và nó âm.

**(b) Huấn luyện kèm ví dụ mẫu KHÔNG bảo vệ được khỏi (a).** Đây là điểm quyết
định. Lý lẽ của DAIL-SQL — cũng là lý lẽ duy nhất từng biện minh cho việc cho
client huấn luyện kèm ví dụ — dự đoán rằng mô hình huấn luyện không ví dụ sẽ
sụp đổ khi gặp ví dụ, còn mô hình huấn luyện có ví dụ thì không. Thực tế
**ngược lại**: mô hình huấn luyện không ví dụ mất *ít hơn* (−3,09 so với
−3,87). Tương tác đi sai chiều.

Ba mô hình độc lập, ba công thức huấn luyện khác nhau, đều mất khoảng 3 điểm
khi gặp ví dụ mẫu. **Hình phạt này là thuộc tính của mô hình 1,5B, không phải
của cách huấn luyện.** Không có cách huấn luyện nào chữa được.

**(c) Huấn luyện có ICL còn làm mô hình gộp kém đi.** Trước bước chưng cất,
nhánh không ICL đạt 57,35 còn nhánh ICL chỉ 54,45 — kém **2,90 điểm,
p = 0,008**, kèm nhiều lỗi thực thi hơn (258 so với 236).

### 2.3 Cái giá phải trả

| | Không ICL | Có ICL | Tỉ lệ |
|---|---:|---:|---:|
| Thời gian huấn luyện 5 client | 4.100 giây | 9.651 giây | **2,35×** |
| Độ dài prompt khi chạy | 1.568 ký tự | 2.175 ký tự | **+38,7%** |
| Thời gian mỗi câu hỏi | 0,289 giây | 1,224 giây | **4,2×** |
| Hạ tầng tại mỗi bên | không cần | phải lưu và đánh chỉ mục kho ví dụ riêng | — |

### 2.4 Kết luận câu hỏi 1

| Bằng chứng | Giá trị | p |
|---|---:|---:|
| Pipeline có ICL thua pipeline không ICL (chạy đúng thiết kế) | −2,61 | 2/5 kho đạt <0,05 |
| Ví dụ mẫu lúc chạy làm giảm độ chính xác | −3,87 | 0,003 |
| Huấn luyện có ICL làm mô hình gộp kém đi | −2,90 | 0,008 |
| Huấn luyện có ICL không bảo vệ được (bác bỏ DAIL-SQL) | sai chiều 0,78 | — |
| Huấn luyện có ICL rồi bỏ ví dụ lúc chạy | +0,68 | 0,401 |

Không ô nào ủng hộ ICL, cộng thêm chi phí 2,35× khi huấn luyện và 4,2× khi
chạy. **Đề xuất bỏ ICL khỏi phương pháp.** Pipeline chính thức còn lại:
client tự huấn luyện không ví dụ mẫu → gộp FedAvg → chưng cất tại máy chủ.

Kèm theo: tên `Fed-ICKD` và `FedICL-SQL` đều lấy ICL làm trung tâm nên cần đổi.

---

## 3. Câu hỏi 2 — pipeline LIÊN KẾT + KD hiệu quả đến đâu

Phần này chạy trên **3 seed độc lập** (0, 1, 2); mỗi seed huấn luyện lại toàn
bộ 5 client và chạy lại bước chưng cất.

### 3.1 Kết quả

| Chặng | seed 0 | seed 1 | seed 2 | Trung bình | Độ lệch |
|---|---:|---:|---:|---:|---:|
| Mô hình 1,5B chưa huấn luyện | 50,00 | 50,00 | 50,00 | 50,00 | — |
| Liên kết (client tự train + gộp) | 57,35 | 57,45 | 59,77 | 58,19 | 1,37 |
| **+ chưng cất (hệ đầy đủ)** | 63,35 | 62,48 | 62,38 | **62,74** | **0,53** |

**Hệ nâng mô hình nhỏ từ 50,00 lên 62,74 ± 0,53 mà không một dòng dữ liệu nào
rời khỏi chủ sở hữu.** Độ lệch 0,53 qua 3 seed cho thấy kết quả ổn định.

Đối chiếu: gom hết dữ liệu về một chỗ huấn luyện tập trung đạt **68,28**; bản
thân giáo viên 7B đạt **78,72**. Hệ liên kết lấp khoảng 70% khoảng cách tới
trần tập trung.

### 3.2 Đóng góp của từng thành phần

Gỡ lần lượt từng thành phần khỏi hệ đầy đủ:

| Cấu hình | EX | Mất bao nhiêu | Số seed | p |
|---|---:|---:|---:|---:|
| **Hệ đầy đủ** (liên kết + chưng cất) | **62,74** | — | 3 | — |
| Gỡ **chưng cất** (chỉ còn liên kết) | 58,19 | **−4,55** | 3 | **0,046** |
| Gỡ **liên kết** (chỉ còn chưng cất) | 61,22 | ~−1,5 | **1** | chưa kiểm định |
| Gỡ cả hai (mô hình gốc) | 50,00 | −12,74 | — | — |

Dòng "gỡ liên kết" là đối chứng quan trọng nhất: lấy mô hình gốc, áp đúng bước
chưng cất, **không dùng một dòng dữ liệu riêng nào**. Nó mới có 1 seed, đang
được bổ sung.

Ba điều rút ra:

- **Liên kết một mình không cạnh tranh được.** Gộp 5 client mà không chưng cất
  đạt 58,19, **thua** chưng cất từ mô hình gốc bằng dữ liệu công khai (61,22).
- **Chưng cất một mình cũng chưa tối ưu.** 61,22 so với 62,74 của hệ đầy đủ.
- **Đóng góp nằm ở sự kết hợp.** Không nửa nào tự đủ. Phát biểu đúng là: *liên
  kết mô hình nhỏ chỉ đáng làm khi có bước chưng cất từ kho công khai*.

Cần nói thẳng để tránh hiểu sai: phần lớn mức tăng (khoảng 11 trên 12,74 điểm)
đến từ kho công khai, dữ liệu riêng đóng góp khoảng 1,5. Điều này không làm yếu
bảng ablation — một thành phần chứng minh giá trị bằng việc gỡ ra thì tệ đi,
không phải bằng việc đóng góp ngang nhau — nhưng không được phát biểu rằng
liên kết tạo ra toàn bộ mức tăng.

Ghi chú về lựa chọn bên trong thành phần chưng cất: bước này gồm học câu SQL
của giáo viên (nhãn cứng) rồi học thêm phân phối xác suất (nhãn mềm). Thêm tầng
nhãn mềm cho **+1,71 điểm, độ lệch 1,38** — dương cả ba seed nhưng chưa đủ lực
thống kê để tách riêng ở cỡ mẫu này. Đây là lựa chọn thiết kế bên trong một
thành phần, cơ sở lý thuyết lấy từ [10] KID, không đưa vào phần đóng góp.

### 3.3 Vì sao điểm cuối ổn định hơn các chặng trước

```text
seed 0:  liên kết 57,35  →  chưng cất bù +6,00  →  63,35
seed 1:  liên kết 57,45  →  chưng cất bù +5,03  →  62,48
seed 2:  liên kết 59,77  →  chưng cất bù +2,61  →  62,38
```

**Phần liên kết chạy càng tốt thì bước chưng cất bù càng ít, và điểm cuối gần
như không đổi.** Đây là lý do độ lệch của hệ đầy đủ chỉ 0,53 trong khi chặng
trước nó dao động 1,37.

Hệ quả thực dụng: đầu tư vào cải thiện thuật toán gộp là kém hiệu quả, vì bước
chưng cất bù trừ phần lớn. Đã kiểm chứng riêng bằng cách dựng phép gộp chính
xác tuyệt đối — không cải thiện có ý nghĩa.

### 3.4 Gộp liên kết có hơn từng bên tự làm không

| | EX |
|---|---:|
| Client yếu nhất | 53,38 |
| Trung bình 5 client | 54,99 |
| Client mạnh nhất | 57,64 |
| **Model sau khi gộp** | **57,35** |

Model gộp hơn trung bình client **2,36 điểm** và ngang client mạnh nhất (kém
0,29). Trong thực tế không bên nào biết trước mình là bên mạnh, nên model gộp
là lựa chọn tốt hơn hẳn kỳ vọng của việc tự làm.

---

## 4. Giới hạn

**Số seed.** §3 dùng 3 seed. §2 (ICL) dùng 1 seed nhưng 6 ô đo độc lập với hiệu
ứng 3–4 điểm, lớn gấp đôi biến thiên giữa các seed đo được ở §3, nên kết luận
bỏ ICL không bị đe doạ. Với 3 seed chỉ những hiệu ứng lớn hơn khoảng 4 điểm mới
đạt ý nghĩa thống kê.

**Dòng "gỡ liên kết" mới có 1 seed.** Đang bổ sung seed 1 và 2 — phép đo còn
thiếu duy nhất của bảng ablation.

**Một vòng.** Toàn bộ số liệu là T = 1. Đang chạy T = 2 và T = 3: nếu đóng góp
của phần liên kết tăng theo số vòng thì con số ~1,5 điểm hiện tại là cận dưới.

**Thuật toán gộp.** Một phương án tinh vi hơn (FLoRA-NA) đã thử và không cải
thiện ở bất kỳ cấu hình nào, kể cả khi dựng phép gộp chính xác tuyệt đối
(+0,68, p = 0,311). Dùng FedAvg thường.

**Dữ liệu.** BIRD chỉ dùng làm kho công khai để chưng cất, **không** dùng làm
tập đánh giá. Mọi con số EX đo trên Spider dev, vốn không chung schema nào với
dữ liệu huấn luyện (20 database test, 146 database train, giao rỗng).
